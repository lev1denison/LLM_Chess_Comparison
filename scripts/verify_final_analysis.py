"""Verify cached evaluation, source preservation and notebook replay without new fits."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import numpy as np
import pandas as pd
import nbformat
from nbclient import NotebookClient
from sklearn.metrics import accuracy_score, balanced_accuracy_score, roc_auc_score, brier_score_loss, confusion_matrix

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/analysis/one_move_v1/final'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audit=json.loads((OUT/'final_data_audit.json').read_text())
assert audit['passed']
for relative,expected in audit['files'].items():assert sha(ROOT/relative)==expected,relative
protected=list(OUT.glob('*_xgboost.ubj'))+list(OUT.glob('*_xgboost_training.json'))+list(OUT.glob('*_heldout_predictions.csv'))+list(OUT.glob('*_heldout_evaluation.json'))
assert len(protected)==12
before={str(p.relative_to(ROOT)):(sha(p),p.stat().st_mtime_ns) for p in protected}
book=ROOT/'notebooks/06_final_analysis.ipynb'
nb=nbformat.read(book,as_version=4)
NotebookClient(nb,timeout=600,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute()
assert not [o for c in nb.cells if c.cell_type=='code' for o in c.outputs if o.output_type=='error']
nbformat.write(nb,book)
after={str(p.relative_to(ROOT)):(sha(p),p.stat().st_mtime_ns) for p in protected}
assert before==after,'Replay changed a frozen fit or evaluation.'
for relative,expected in audit['files'].items():assert sha(ROOT/relative)==expected,relative
features=pd.read_csv(ROOT/'data/experiments/one_move_v1/analysis_features.csv',dtype={'puzzle_id':str})
for name in ['gpt_oss','gemini','claude_haiku']:
 inputs=pd.read_csv(OUT/f'{name}_inputs.csv',dtype={'puzzle_id':str})
 train=inputs.loc[inputs.split=='train']
 receipt=json.loads((OUT/f'{name}_heldout_evaluation.json').read_text())
 p=pd.read_csv(OUT/f'{name}_heldout_predictions.csv',dtype={'puzzle_id':str})
 assert len(p)==p.puzzle_id.nunique()==200
 assert set(p.puzzle_id)==set(features.loc[features.split=='test','puzzle_id'])
 assert not set(p.puzzle_id)&set(train.puzzle_id)
 truth=inputs.loc[inputs.split=='test',['puzzle_id','success']].merge(p,on='puzzle_id',validate='one_to_one')
 assert truth.success.equals(truth.truth)
 assert p.probability.between(0,1).all()
 assert np.array_equal(p.prediction,(p.probability>=.5).astype(int))
 m=receipt['metrics']
 computed={'accuracy':accuracy_score(p.truth,p.prediction),'balanced_accuracy':balanced_accuracy_score(p.truth,p.prediction),'roc_auc':roc_auc_score(p.truth,p.probability),'brier':brier_score_loss(p.truth,p.probability),'majority_baseline_accuracy':float((p.truth==int(train.success.mean()>=.5)).mean())}
 for key,value in computed.items():assert np.isclose(value,m[key],rtol=1e-6,atol=1e-8),(name,key)
 assert confusion_matrix(p.truth,p.prediction,labels=[0,1]).ravel().tolist()==m['confusion_tn_fp_fn_tp']
 coefficients=pd.read_csv(OUT/'logistic_coefficients.csv')
 assert np.isfinite(coefficients.select_dtypes('number').to_numpy()).all()
 assert np.allclose(np.exp(coefficients.coefficient),coefficients.odds_ratio)
assert set(coefficients.term)=={'const','rating_500','legal_moves_10','piece_count_10','material_balance','theme_pin','theme_kingsideAttack','theme_hangingPiece','phase_endgame','phase_opening','is_gemini','is_claude'}
for md in [ROOT/'README.md',ROOT/'writing/final_report.md',ROOT/'writing/README.md']:
 for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',md.read_text(encoding='utf-8')):
  if not target.startswith(('https:','http:','#')):assert (md.parent/target).exists(),(md,target)
result={'passed':True,'verified_utc':datetime.now(timezone.utc).isoformat(),'source_files_unchanged':True,'notebook_replay_passed':True,'frozen_model_and_evaluation_hashes_and_mtimes_unchanged':True,'metrics_recomputed_from_cached_predictions':True,'local_report_links_valid':True,'models_verified':3,'new_api_requests':0,'protected_sha256':{k:v[0] for k,v in before.items()}}
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: source hashes, notebook replay, unchanged frozen fits/evaluations, cached metrics and report links.')
