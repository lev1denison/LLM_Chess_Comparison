"""Restyle conditional predictions from the saved pooled regression; never fit."""
from pathlib import Path
import json

import joblib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, PercentFormatter
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
DEPLOYMENTS = {
    'gpt_oss': ('GPT-OSS 120B', '#0072B2'),
    'gemini': ('Gemini 3.5 Flash-Lite', '#009E73'),
    'claude_haiku': ('Claude Haiku 5.5', '#D55E00'),
}


def prediction_curves(fit, features, recipe, rating_min, rating_max):
    """Retain the notebook's 200-point grid and conditional reference position."""
    assert fit.cov_type == 'cluster'
    ratings = np.linspace(rating_min, rating_max, 200)
    reference = {k: 0. for k in recipe['full']}
    for k in recipe['core']:
        reference[k] = float(features.loc[features.split.eq('train'), k].median())
    curves = {}
    for name in DEPLOYMENTS:
        grid = pd.DataFrame({k: np.full(200, v) for k, v in reference.items()})
        grid['rating_500'] = (ratings - 1500) / 500
        grid['is_gemini'] = int(name == 'gemini')
        grid['is_claude'] = int(name == 'claude_haiku')
        grid = sm.add_constant(grid, has_constant='add')[fit.model.exog_names]
        curves[name] = fit.get_prediction(grid).summary_frame(alpha=.05)
    return ratings, curves


def plot_logistic_regression(fit, features, recipe, rating_min, rating_max, destination):
    ratings, curves = prediction_curves(fit, features, recipe, rating_min, rating_max)
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with plt.rc_context({'font.family': 'DejaVu Sans', 'font.size': 11,
                         'pdf.fonttype': 42, 'ps.fonttype': 42,
                         'text.color': '#222222', 'axes.labelcolor': '#333333'}):
        fig, ax = plt.subplots(figsize=(8, 4.8))
        for name, (_, color) in DEPLOYMENTS.items():
            prediction = curves[name]
            ax.fill_between(ratings, prediction['mean_ci_lower'], prediction['mean_ci_upper'],
                            color=color, alpha=.13, linewidth=0, zorder=2)
        for name, (label, color) in DEPLOYMENTS.items():
            ax.plot(ratings, curves[name]['mean'], color=color, label=label,
                    linewidth=2.5, linestyle='-', zorder=3)
        ax.set(xlim=(rating_min, rating_max), ylim=(0, 1),
               xlabel='Lichess puzzle rating', ylabel='Predicted official move mention (%)',
               title='Predicted LLM success by chess puzzle rating')
        ax.title.set_fontsize(14)
        ax.title.set_fontweight('bold')
        ax.title.set_position((.5, 1.035))
        ax.yaxis.set_major_locator(MultipleLocator(.2))
        ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
        ax.xaxis.set_major_locator(MultipleLocator(400))
        ax.grid(axis='y', color='#E5E7EB', linewidth=.7)
        ax.set_axisbelow(True)
        ax.legend(loc='upper right', frameon=False, fontsize=10, handlelength=2.8,
                  borderaxespad=.9, labelspacing=.6)
        ax.xaxis.labelpad = 10
        ax.yaxis.labelpad = 10
        ax.tick_params(length=3, color='#AAAAAA')
        for side in ('top', 'right'):
            ax.spines[side].set_visible(False)
        for side in ('left', 'bottom'):
            ax.spines[side].set_color('#BBBBBB')
            ax.spines[side].set_linewidth(.6)
        fig.tight_layout(pad=1.3)
        for suffix in ('png', 'pdf'):
            fig.savefig(destination / f'logistic_regression.{suffix}', dpi=400,
                        facecolor='white', bbox_inches='tight', pad_inches=.12)
    return fig


if __name__ == '__main__':
    plt.switch_backend('Agg')
    out = ROOT / 'data/analysis/one_move_v1/final'
    base = ROOT / 'data/experiments/one_move_v1'
    fit = joblib.load(out / 'logistic_regression.joblib')
    features = pd.read_csv(base / 'analysis_features.csv', dtype={'puzzle_id': str})
    recipe = json.loads((base / 'feature_recipe.json').read_text())
    pooled = pd.concat([pd.read_csv(out / f'{name}_inputs.csv') for name in DEPLOYMENTS])
    figure = plot_logistic_regression(fit, features, recipe, pooled.puzzle_rating.min(),
                                     pooled.puzzle_rating.max(), ROOT / 'figures/one_move_v1/final')
    plt.close(figure)
