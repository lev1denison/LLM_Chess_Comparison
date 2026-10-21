"""Independently replay saved requests and verify each scored outcome."""
from collections import defaultdict
from pathlib import Path
import json
import chess
import pandas as pd
from run_llm_puzzles import score_move

root = Path(__file__).resolve().parents[1]
exp = root / 'data/experiments/local_pilot_v2'
manifest = json.loads((exp / 'manifest.json').read_text())
features = pd.read_csv(root / 'data/samples/pilot_v1/pilot_puzzles.csv', dtype={'puzzle_id':str}).set_index('puzzle_id')
requests = defaultdict(list)
for line in (exp / 'requests.jsonl').read_text().splitlines():
    row = json.loads(line)
    requests[row['trial_id']].append(row)
outcomes = pd.DataFrame([json.loads(s) for s in (exp / 'outcomes.jsonl').read_text().splitlines()]).drop_duplicates(['puzzle_id','llm_name'],keep='last')
for row in outcomes.itertuples(index=False):
    puzzle = features.loc[row.puzzle_id]
    board = chess.Board(puzzle.solver_fen)
    official = puzzle.official_moves.split()[1:]
    correct = 0
    category = None
    calls = [r for r in requests[row.trial_id] if 'response' in r]
    for i, call in enumerate(calls):
        expected_prompt = manifest['prompt'].format(fen=board.fen(),side='white' if board.turn else 'black')
        assert call['request']['messages'] == [{'role':'user','content':expected_prompt}]
        assert call['request']['model'] == row.llm_name
        payload = call['response']
        category, move = score_move(board, payload['message']['content'], official[2*i])
        if payload.get('done_reason') == 'length':
            category = 'generation_limit'
        if category != 'correct':
            assert i == len(calls)-1
            break
        correct += 1
        board.push_uci(move)
        if 2*i+1 < len(official):
            board.push_uci(official[2*i+1])
    assert correct == row.correct_solver_moves
    if row.status == 'completed':
        expected_success = int(correct == puzzle.total_solver_moves)
        assert row.success == expected_success
        assert row.failure_type == ('success' if expected_success else category)
    else:
        assert pd.isna(row.success)
assert len(outcomes) == 225, f'Expected 225 attempts, got {len(outcomes)}'
assert outcomes.groupby('llm_name').size().eq(75).all()
assert outcomes.groupby('puzzle_id').size().eq(3).all()
result = {'attempts_audited':len(outcomes),'distinct_puzzles':outcomes.puzzle_id.nunique(),
          'request_count':sum(map(len,requests.values())), 'status':'passed'}
(exp / 'audit_summary.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
