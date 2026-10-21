"""Create preliminary descriptive results and grouped-holdout classifiers."""
from pathlib import Path
import json
import warnings
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import accuracy_score, balanced_accuracy_score, roc_auc_score, brier_score_loss

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / 'data/experiments/local_pilot_v2'
OUT = ROOT / 'data/analysis/local_pilot_v2'
FIG = ROOT / 'figures/local_pilot_v2'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(s) for s in (EXP / 'outcomes.jsonl').read_text().splitlines() if s.strip()]
    outcomes = pd.DataFrame(rows).drop_duplicates(['puzzle_id', 'llm_name'], keep='last')
    features = pd.read_csv(ROOT / 'data/samples/pilot_v1/pilot_puzzles.csv', dtype={'puzzle_id': str})
    frame = outcomes.merge(features, on='puzzle_id', validate='many_to_one')
    frame.to_csv(OUT / 'all_attempts.csv', index=False)
    data = frame.loc[frame.status.eq('completed')].copy()
    data['success'] = data.success.astype(int)
    data['rating_100'] = data.puzzle_rating / 100
    data.to_csv(OUT / 'modeling_table.csv', index=False)
    summary = data.groupby('llm_name').agg(attempts=('success','size'), solved=('success','sum'),
                    solve_rate=('success','mean'), mean_seconds=('elapsed_seconds','mean'))
    summary.to_csv(OUT / 'solve_rates.csv')
    failures = pd.crosstab(data.llm_name, data.failure_type)
    failures.to_csv(OUT / 'failure_counts.csv')
    fig, ax = plt.subplots(figsize=(9,4))
    failures.plot.barh(stacked=True, ax=ax, colormap='Set2')
    ax.set(xlabel='Puzzle attempts', ylabel='', title='Outcome categories under the direct-UCI protocol')
    ax.legend(title='Outcome', bbox_to_anchor=(1.02,1), loc='upper left')
    fig.tight_layout(); fig.savefig(FIG / 'failure_breakdown.png', dpi=160); plt.close(fig)
    by_rating = data.groupby(['llm_name','rating_stratum']).agg(n=('success','size'), solved=('success','sum'), solve_rate=('success','mean'))
    by_rating.to_csv(OUT / 'solve_rates_by_rating.csv')
    fig, ax = plt.subplots(figsize=(8,4))
    summary.solve_rate.plot.bar(ax=ax, color=['#4c78a8','#f58518','#54a24b'])
    ax.set(ylabel='Full official-line solve rate', xlabel='', ylim=(0,1), title='75-puzzle local LLM pilot')
    ax.tick_params(axis='x', rotation=0)
    for i, row in enumerate(summary.itertuples()):
        ax.text(i, row.solve_rate + .025, f'{row.solved}/{row.attempts}', ha='center')
    fig.tight_layout(); fig.savefig(FIG / 'solve_rates.png', dpi=160); plt.close(fig)
    notes = [
        'Preliminary, balanced rating-stratum sample; not population-weighted.',
        'Official-line exact matching; legal alternatives have not been engine-adjudicated.',
        'Direct-answer FEN-only protocol; Qwen thinking disabled; 128-token output cap.',
        'Model family, size, quantization, and reasoning behavior differ; effects are associations.',
        'Malformed answers count as unsuccessful under this protocol; infrastructure errors are excluded.',
        'Smoke outcomes are included because the protocol was not changed after inspecting them.'
    ]
    report = {'planned_attempts': len(features)*3, 'recorded_attempts': len(frame),
              'scored_attempts': len(data), 'infrastructure_errors': int(frame.status.ne('completed').sum()),
              'distinct_puzzles': int(data.puzzle_id.nunique()), 'notes': notes}
    if len(data) == 0 or data.success.nunique() < 2:
        report['model_status'] = 'Not fitted: outcome has fewer than two classes. Collect a revised, separately versioned pilot or more observations.'
    else:
        numeric = ['rating_100','total_solver_moves','legal_moves','piece_count','material_balance']
        categorical = ['llm_name']
        columns = numeric + categorical
        split = GroupShuffleSplit(n_splits=1, test_size=.2, random_state=401)
        train_idx, test_idx = next(split.split(data, groups=data.puzzle_id))
        train, test = data.iloc[train_idx], data.iloc[test_idx]
        assert not set(train.puzzle_id) & set(test.puzzle_id)
        assignment = data[['puzzle_id']].drop_duplicates().copy()
        assignment['partition'] = np.where(assignment.puzzle_id.isin(train.puzzle_id), 'train','test')
        assignment.to_csv(OUT / 'puzzle_split.csv', index=False)
        report['train_puzzles'] = train.puzzle_id.nunique()
        report['test_puzzles'] = test.puzzle_id.nunique()
        report['train_successes'] = int(train.success.sum())
        report['test_successes'] = int(test.success.sum())
        if train.success.nunique() < 2:
            report['model_status'] = 'Not fitted: the fixed training partition contains only one class; split was not redrawn based on outcomes.'
        else:
            models = {'majority_baseline': DummyClassifier(strategy='most_frequent'),
                      'logistic_regression': LogisticRegression(max_iter=2000, random_state=401),
                      'decision_tree': DecisionTreeClassifier(max_depth=3, min_samples_leaf=10, random_state=401)}
            metrics = []
            predictions = test[['puzzle_id','llm_name','success']].copy()
            for name, estimator in models.items():
                prep = ColumnTransformer([('numeric', StandardScaler(), numeric),
                    ('categorical', OneHotEncoder(handle_unknown='ignore', drop='first'), categorical)])
                pipeline = Pipeline([('features',prep),('model',estimator)])
                pipeline.fit(train[columns], train.success)
                prob = pipeline.predict_proba(test[columns])[:,1]
                pred = pipeline.predict(test[columns])
                auc = float(roc_auc_score(test.success,prob)) if test.success.nunique() == 2 else None
                metrics.append({'model':name, 'test_n':len(test), 'accuracy':accuracy_score(test.success,pred),
                    'balanced_accuracy':balanced_accuracy_score(test.success,pred), 'roc_auc':auc,
                    'brier_score':brier_score_loss(test.success,prob)})
                predictions[name+'_probability'] = prob
                joblib.dump(pipeline, OUT / (name+'.joblib'))
                names = pipeline.named_steps['features'].get_feature_names_out()
                if name == 'logistic_regression':
                    pd.DataFrame({'feature':names, 'standardized_penalized_coefficient':estimator.coef_[0]}).to_csv(OUT / 'logistic_coefficients.csv', index=False)
                if name == 'decision_tree':
                    fig, ax = plt.subplots(figsize=(16,7))
                    plot_tree(estimator, feature_names=names, class_names=['failure','success'], filled=True, ax=ax, rounded=True)
                    ax.set_title('Pilot decision tree (numeric splits use training-standardized features)')
                    fig.tight_layout(); fig.savefig(FIG / 'decision_tree.png', dpi=160); plt.close(fig)
            pd.DataFrame(metrics).to_csv(OUT / 'model_metrics.csv', index=False)
            predictions.to_csv(OUT / 'test_predictions.csv', index=False)
            report['model_status'] = 'Fitted L2-regularized predictive logistic regression and depth-3 decision tree on a fixed puzzle-grouped training partition.'
            report['metrics'] = metrics
            # Statistical rating association is separate from held-out predictive evaluation.
            # Avoid unstable significance claims when an LLM has only one outcome class.
            if data.groupby('llm_name').success.nunique().min() < 2 or min(data.success.value_counts()) < 20:
                report['clustered_inference_status'] = 'Deferred: sparse outcomes or a single outcome class within an LLM; unpenalized pooled coefficients and clustered intervals may be unstable.'
            else:
                try:
                    with warnings.catch_warnings(record=True) as caught:
                        fit = smf.glm('success ~ rating_100 + C(llm_name)', data=data,
                                      family=sm.families.Binomial()).fit(cov_type='cluster',cov_kwds={'groups':data.puzzle_id})
                    if not fit.converged or caught:
                        raise ValueError('Convergence or inference warnings')
                    ci = fit.conf_int()
                    pd.DataFrame({'coefficient':fit.params,'odds_ratio':np.exp(fit.params),
                        'or_ci_lower':np.exp(ci[0]),'or_ci_upper':np.exp(ci[1]),'p_value':fit.pvalues}).to_csv(OUT / 'clustered_rating_logistic.csv')
                    report['clustered_inference_status'] = 'Rating + LLM GLM fitted to full pilot with puzzle-clustered standard errors; exploratory association, not held-out prediction.'
                except Exception as error:
                    report['clustered_inference_status'] = 'Deferred: ' + type(error).__name__
    (OUT / 'results_summary.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(summary.to_string())
    print('\nFailure categories:\n'+failures.to_string())
    print('\n'+json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    main()
