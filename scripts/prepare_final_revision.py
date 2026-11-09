from pathlib import Path
import json, hashlib, shutil
from datetime import datetime, timezone
import nbformat

ROOT=Path(__file__).resolve().parents[1]
CFG=ROOT/'experiments/one_move_v1'
BASE=ROOT/'data/experiments/one_move_v1'
book=ROOT/'notebooks/06_final_analysis.ipynb'
archive=BASE/'final_three_model_revision'
archive.mkdir(exist_ok=True)
assert not (CFG/'final_three_model_plan.json').exists(), 'Revision already prepared.'
shutil.copy2(book,archive/book.name)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
plan=json.loads((CFG/'final_analysis_plan.json').read_text())
plan.update(id='final_three_model_v1',recorded_utc=datetime.now(timezone.utc).isoformat(),
 status='Recorded after all collection and inspection of aggregate/early results, before final model fitting and held-out predictive evaluation. Not an original preregistration.',
 relationship_to_pilot_plan='Extends final_analysis_plan.json to Claude and tolerant solution_mention_v1 scoring. Original plans, collection manifest and raw logs remain unchanged.',
 models=['gpt_oss','gemini','claude_haiku'],reference_model='gpt_oss',
 primary_regression='Pooled binomial GLM on 3000 answers: frozen full predictors plus Gemini and Claude identity indicators (GPT-OSS reference); puzzle-clustered covariance over 1000 puzzles. No interactions or predictor selection.',
 scoring='solution_mention_v1; post-hoc scoring amendment applies identically to all deployments. Strict results retained for descriptive sensitivity comparison.',
 original_final_plan_sha256=sha(CFG/'final_analysis_plan.json'),
 original_notebook_sha256=sha(archive/book.name),
 descriptive_outputs='Overall Wilson intervals, rating-band accuracy, strict versus tolerant counts. No additional model fitting or hypothesis selection based on these tables.',
 interpretation='Primary rating test is inherited from original plan. Model/theme contrasts and deployment differences are secondary associations. Holdout is reserved for predictive evaluation, not for the pooled association regression.')
(CFG/'final_three_model_plan.json').write_text(json.dumps(plan,indent=2)+'\n')
nb=nbformat.read(book,as_version=4)
for c in nb.cells:
 if c.cell_type!='code':continue
 s=c.source
 s=s.replace("PLAN=json.loads((CFG/'final_analysis_plan.json').read_text())", "PLAN=json.loads((CFG/'final_three_model_plan.json').read_text())\nCONFIG['models']['claude_haiku']=json.loads((CFG/'claude_pilot.json').read_text())['model_spec']\nassert list(CONFIG['models'])==PLAN['models']")
 s=s.replace("('analysis_code_sha256','06_final_analysis.ipynb'),",'')
 s=s.replace("assert sha(BASE/'puzzles.csv')", "binding=json.loads((CFG/'final_three_model_binding.json').read_text())\nassert binding['code_sha256']==code_sha(BOOK)\nassert binding['plan_sha256']==sha(CFG/'final_three_model_plan.json')\nassert binding['original_manifest_sha256']==sha(BASE/'manifest.json')\nassert sha(BASE/'puzzles.csv')",1)
 s=s.replace('READY=len(frames)==2','READY=len(frames)==len(PLAN[\'models\'])')
 s=s.replace("sha(CFG/'final_analysis_plan.json')", "sha(CFG/'final_three_model_plan.json')")
 s=s.replace("d.assign(is_gemini=int(name=='gemini'),model_key=name)","d.assign(is_gemini=int(name=='gemini'),is_claude=int(name=='claude_haiku'),model_key=name)")
 s=s.replace("names=predictors+['is_gemini']", "names=predictors+['is_gemini','is_claude']")
 s=s.replace("['#2563eb','#16a34a'][i]", "['#2563eb','#16a34a','#9333ea'][i]")
 s=s.replace('xticks=[0,1]', 'xticks=list(range(len(rows)))')
 s=s.replace("[('gpt_oss','#2563eb'),('gemini','#16a34a')]", "[('gpt_oss','#2563eb'),('gemini','#16a34a'),('claude_haiku','#9333ea')]")
 s=s.replace("grid['is_gemini']=int(name=='gemini')", "grid['is_gemini']=int(name=='gemini');grid['is_claude']=int(name=='claude_haiku')")
 s=s.replace('plt.subplots(1,2,figsize=(12,5)', 'plt.subplots(1,3,figsize=(18,5)')
 s=s.replace("zip(axes,CONFIG['models'],['#2563eb','#16a34a'])", "zip(axes,CONFIG['models'],['#2563eb','#16a34a','#9333ea'])")
 s=s.replace('Official solution-move accuracy','Official solution-move mention success')
 # Expose unexpected fit failures rather than silently continuing with incomplete analysis.
 s=s.replace("reasons.append('Regression checks failed: '+type(error).__name__)","reasons.append('Regression checks failed: '+type(error).__name__+': '+str(error))")
 c.source=s
 c.outputs=[];c.execution_count=None
nb.cells[0].source='''# 06 - Final three-model regression and XGBoost analysis

All three deployments completed the same 1,000 puzzles. I analyze tolerant solution-move mention success, using the frozen features and shared 800/200 split. The pooled association regression uses all 3,000 answers with 1,000 puzzle clusters. Separate XGBoost models use only training outcomes and cached held-out evaluation.

`final_three_model_plan.json` extends the original two-model plan after collection and inspected early results, before final fitting. This is a disclosed amendment, not an original preregistration. I preserve the original plans, collection manifest and historical notebooks/figures. No API calls, parameter searches or early stopping occur here.'''
audit=nbformat.v4.new_code_cell('''# Verify result metadata against the frozen sample and retain file hashes.
assert READY
data_audit={'passed':True,'new_api_requests':0,'files':{},'models':{}}
for name in PLAN['models']:
    result=pd.read_csv(BASE/name/'results.csv',dtype={'puzzle_id':str})
    assert result.trial_id.nunique()==1000
    assert result.scoring_version.eq('solution_mention_v1').all()
    assert result.strict_success.isin([0,1]).all()
    joined=features.merge(result,on='puzzle_id',suffixes=('_f','_r'),validate='one_to_one')
    for col in ['split','solver_fen','official_first_move','collection_order']:
        assert joined[col+'_f'].equals(joined[col+'_r']), (name,col)
    assert result.returned_model.eq(CONFIG['models'][name]['model']).all()
    assert result.groupby('split').size().to_dict()=={'test':200,'train':800}
    data_audit['models'][name]={'n':1000,'train_n':800,'test_n':200,'strict_correct':int(result.strict_success.sum()),'tolerant_correct':int(result.success.sum())}
    for filename in ['results.csv','outcomes.jsonl','requests.jsonl','audit.json','summary.json']:
        path=BASE/name/filename
        data_audit['files'][str(path.relative_to(ROOT))]=sha(path)
for filename in ['puzzles.csv','analysis_features.csv','feature_recipe.json','manifest.json']:
    data_audit['files'][str((BASE/filename).relative_to(ROOT))]=sha(BASE/filename)
audit_path=OUT/'final_data_audit.json'
if audit_path.exists():assert json.loads(audit_path.read_text())==data_audit
else:save(audit_path,data_audit)
display(pd.DataFrame(data_audit['models']).T)
''')
nb.cells.insert(4,nbformat.v4.new_markdown_cell('## Final data integrity and scoring checks'))
nb.cells.insert(5,audit)
extra=nbformat.v4.new_code_cell('''# Descriptive tables use fixed rating bands; no changes to the fitted models.
band_rows=[];sensitivity=[]
for name,d in frames.items():
    raw=pd.read_csv(BASE/name/'results.csv',dtype={'puzzle_id':str})
    sensitivity.append({'Model':CONFIG['models'][name]['label'],'n':len(raw),'strict_correct':int(raw.strict_success.sum()),'tolerant_correct':int(raw.success.sum()),'additional_correct':int((raw.success-raw.strict_success).sum()),'multiple_move_answers':int(raw.multiple_legal_moves_mentioned.sum())})
    for band in ['low','middle','high']:
        subset=d.loc[d.rating_stratum.eq(band)];k=int(subset.success.sum());lo,hi=wilson(k,len(subset))
        band_rows.append({'Model':CONFIG['models'][name]['label'],'rating_band':band,'n':len(subset),'correct':k,'accuracy':k/len(subset),'ci_low':lo,'ci_high':hi})
bands=pd.DataFrame(band_rows);bands.to_csv(OUT/'rating_band_accuracy.csv',index=False)
pd.DataFrame(sensitivity).to_csv(OUT/'scoring_sensitivity.csv',index=False)
fig,ax=plt.subplots(figsize=(9,5))
for (name,color),offset in zip(zip(PLAN['models'],['#2563eb','#16a34a','#9333ea']),[-.18,0,.18]):
    t=bands.loc[bands.Model.eq(CONFIG['models'][name]['label'])]
    ax.errorbar(np.arange(3)+offset,t.accuracy,yerr=[t.accuracy-t.ci_low,t.ci_high-t.accuracy],fmt='o',capsize=4,color=color,label=CONFIG['models'][name]['label'])
ax.set(xticks=[0,1,2],xticklabels=['Low (<=1157)','Middle (1158–1700)','High (>1700)'],ylim=(0,1),ylabel='Solution-move mention success',xlabel='Frozen human rating band',title='Observed success by puzzle difficulty; Wilson 95% intervals')
ax.legend();fig.tight_layout();fig.savefig(FIG/'rating_band_accuracy.png',dpi=180);plt.show()
fig,axes=plt.subplots(1,3,figsize=(12,4))
for ax,metric in zip(axes,metrics):
    matrix=np.array(metric['confusion_tn_fp_fn_tp']).reshape(2,2)
    ax.imshow(matrix,cmap='Blues',vmin=0,vmax=200)
    for (i,j),v in np.ndenumerate(matrix):ax.text(j,i,str(v),ha='center',va='center')
    ax.set(title=metric['Model'],xticks=[0,1],yticks=[0,1],xticklabels=['Failure','Success'],yticklabels=['Failure','Success'],xlabel='Predicted',ylabel='Observed')
fig.suptitle('Held-out XGBoost classification of LLM success (200 puzzles/model)');fig.tight_layout();fig.savefig(FIG/'heldout_confusion.png',dpi=180);plt.show()
display(bands);display(pd.DataFrame(sensitivity))
assert fit is not None and len(boosters)==3 and len(metrics)==3, 'Final analysis incomplete; inspect status.'
''')
nb.cells.insert(-1,nbformat.v4.new_markdown_cell('## Descriptive difficulty, scoring sensitivity and held-out results'))
nb.cells.insert(-1,extra)
nbformat.write(nb,book)
code_hash=hashlib.sha256('\n\n'.join(c.source for c in nb.cells if c.cell_type=='code' and 'run_control' not in c.metadata.get('tags',[])).encode()).hexdigest()
binding={'code_sha256':code_hash,'plan_sha256':sha(CFG/'final_three_model_plan.json'),'original_manifest_sha256':sha(BASE/'manifest.json'),'original_notebook_sha256':sha(archive/book.name)}
(CFG/'final_three_model_binding.json').write_text(json.dumps(binding,indent=2)+'\n')
print('Three-model revision prepared; original notebook archived.')
