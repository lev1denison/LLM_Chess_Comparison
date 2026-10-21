"""Resumable local pilot. python code/run_llm_puzzles.py --stage smoke|pilot

Smoke is a fixed five-puzzle subset. With identical manifest it is reused in pilot.
Only the current board and side reach a model. Official-line scoring is strict.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import re
import time
import uuid

import chess
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/experiments/local_pilot_v2'


def score_move(board, raw, expected):
    text = raw.strip()
    if not re.fullmatch(r'[a-h][1-8][a-h][1-8][qrbn]?', text):
        return 'unparseable', None
    move = chess.Move.from_uci(text)
    if move not in board.legal_moves:
        return 'illegal_move', text
    return ('correct' if text == expected else 'legal_incorrect'), text


def append(path, row):
    with path.open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(row) + '\n')
        stream.flush()


def records(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', choices=['smoke', 'pilot'], default='smoke')
    args = parser.parse_args()
    config_path = ROOT / 'code/llm_config.json'
    config = json.loads(config_path.read_text())
    template = (ROOT / 'code' / config['prompt_file']).read_text()
    sample_path = ROOT / 'data/samples/pilot_v1/pilot_puzzles.csv'
    puzzles = pd.read_csv(sample_path, dtype={'puzzle_id': str}).sort_values('puzzle_id')
    # Predetermine coverage, without looking at model responses.
    smoke_ids = []
    for group, size in [('low', 2), ('middle', 2), ('high', 1)]:
        smoke_ids.extend(puzzles.loc[puzzles.rating_stratum.eq(group)].head(size).puzzle_id)
    selected = puzzles.loc[puzzles.puzzle_id.isin(smoke_ids)] if args.stage == 'smoke' else puzzles
    OUT.mkdir(parents=True, exist_ok=True)
    versions = {}
    for model in config['models']:
        response = requests.get(model['base_url'] + '/api/tags', timeout=15)
        response.raise_for_status()
        tags = {m['name']: m for m in response.json()['models']}
        if model['model'] not in tags:
            raise RuntimeError('Missing model: ' + model['model'])
        response = requests.post(model['base_url'] + '/api/show', json={'model': model['model']}, timeout=15)
        response.raise_for_status()
        details = response.json()
        versions[model['model']] = {'digest': tags[model['model']]['digest'],
                                    'details': details.get('details'),
                                    'parameters': details.get('parameters'),
                                    'capabilities': details.get('capabilities')}
    manifest = {'config': config, 'prompt': template,
                'sample_sha256': hashlib.sha256(sample_path.read_bytes()).hexdigest(),
                'models': versions, 'smoke_ids': smoke_ids,
                'protocol_notes': ['Direct answer, no tools, Qwen thinking explicitly disabled.',
                                   'Fresh current-position request at every solver turn.',
                                   'Exact official-line matching, alternatives are not engine-adjudicated.',
                                   'At most 128 generated tokens per move; budget exhaustion counts as failure.',
                                   'Smoke outcomes reused only under identical frozen protocol.']}
    manifest_path = OUT / 'manifest.json'
    if manifest_path.exists():
        if json.loads(manifest_path.read_text()) != manifest:
            raise RuntimeError('Protocol or model changed. Use a new experiment directory.')
    else:
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    completed = {(r['puzzle_id'], r['llm_name']) for r in records(OUT / 'outcomes.jsonl')
                 if r['status'] == 'completed'}
    for model in config['models']:
        name = model['model']
        for row in selected.itertuples(index=False):
            if (row.puzzle_id, name) in completed:
                continue
            trial_id = str(uuid.uuid4())
            board = chess.Board(row.solver_fen)
            official = row.official_moves.split()[1:]
            assert len(official[::2]) == row.total_solver_moves
            started = time.perf_counter()
            correct = 0
            category = 'success'
            status = 'completed'
            for index in range(0, len(official), 2):
                prompt = template.format(fen=board.fen(), side='white' if board.turn else 'black')
                body = {'model': name, 'messages': [{'role': 'user', 'content': prompt}],
                        'stream': False, 'options': model['options'], 'keep_alive': '5m'}
                if 'think' in model:
                    body['think'] = model['think']
                payload = None
                for retry in range(2):
                    call_started = time.perf_counter()
                    log = {'trial_id': trial_id, 'puzzle_id': row.puzzle_id, 'llm_name': name,
                           'solver_turn': index // 2 + 1, 'retry': retry,
                           'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'request': body}
                    try:
                        response = requests.post(model['base_url'] + '/api/chat', json=body, timeout=(10, 300))
                        response.raise_for_status()
                        payload = response.json()
                        if not payload.get('done') or 'content' not in payload.get('message', {}):
                            raise ValueError('Incomplete or malformed provider response')
                        log['response'] = payload
                    except (requests.RequestException, ValueError) as error:
                        log['error_type'] = type(error).__name__
                        log['http_status'] = getattr(getattr(error, 'response', None), 'status_code', None)
                    log['elapsed_seconds'] = time.perf_counter() - call_started
                    append(OUT / 'requests.jsonl', log)
                    if 'error_type' not in log:
                        break
                    payload = None
                if payload is None:
                    status, category = 'infrastructure_error', 'request_failed'
                    break
                category, move = score_move(board, payload['message']['content'], official[index])
                if payload.get('done_reason') == 'length':
                    category = 'generation_limit'
                if category != 'correct':
                    break
                board.push_uci(move)
                correct += 1
                if index + 1 < len(official):
                    board.push_uci(official[index + 1])
            if status == 'completed' and correct == row.total_solver_moves:
                category = 'success'
            result = {'trial_id': trial_id, 'puzzle_id': row.puzzle_id, 'llm_name': name,
                      'status': status, 'success': int(category == 'success') if status == 'completed' else None,
                      'failure_type': category, 'correct_solver_moves': correct,
                      'required_solver_moves': row.total_solver_moves,
                      'elapsed_seconds': round(time.perf_counter() - started, 3),
                      'stage_collected': args.stage}
            append(OUT / 'outcomes.jsonl', result)
            print(f'{name} {row.puzzle_id}: {category}; {result["elapsed_seconds"]:.1f}s', flush=True)
        # Release this model before loading another, avoiding three resident models.
        response = requests.post(model['base_url'] + '/api/generate',
                                 json={'model': name, 'keep_alive': 0}, timeout=60)
        response.raise_for_status()
    outcomes = pd.DataFrame(records(OUT / 'outcomes.jsonl')).drop_duplicates(['puzzle_id', 'llm_name'], keep='last')
    outcomes.to_csv(OUT / 'outcomes.csv', index=False)
    print(outcomes.groupby(['llm_name', 'status']).agg(n=('puzzle_id','size'), successes=('success','sum')))


if __name__ == '__main__':
    main()
