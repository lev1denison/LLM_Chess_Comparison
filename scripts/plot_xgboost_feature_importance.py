"""Compare saved normalized training gains without loading or retraining models."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEPLOYMENTS = {
    'gpt_oss': ('GPT-OSS 120B', '#0072B2'),
    'gemini': ('Gemini 3.5 Flash-Lite', '#009E73'),
    'claude_haiku': ('Claude Haiku 5.5', '#D55E00'),
}
LABELS = {
    'puzzle_rating': 'Lichess rating',
    'theme_hangingPiece': 'Hanging piece',
    'theme_kingsideAttack': 'Kingside attack',
    'theme_pin': 'Pin',
    'piece_count': 'Piece count',
    'legal_moves': 'Legal move count',
    'material_balance': 'Material balance',
    'phase_opening': 'Opening',
    'phase_endgame': 'Endgame',
}


def ordered_gains(source):
    columns = {}
    for name in DEPLOYMENTS:
        table = pd.read_csv(Path(source) / f'{name}_xgboost_feature_importance.csv')
        assert len(table) == 9 and set(table.feature) == set(LABELS)
        columns[name] = table.set_index('feature').normalized_gain
    values = pd.DataFrame(columns)
    assert not values.isna().any().any()
    np.testing.assert_allclose(values.sum(), 1, atol=1e-12)
    order = values.mean(axis=1).sort_values(ascending=False, kind='stable').index
    return values.loc[order]


def plot_xgboost_feature_importance(source, destination):
    values = ordered_gains(source)
    maximum = float(values.max().max())
    xmax = max(.32, np.ceil(maximum * 1.05 / .02) * .02)
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with plt.rc_context({'font.family': 'DejaVu Sans', 'font.size': 10.5,
                         'pdf.fonttype': 42, 'ps.fonttype': 42,
                         'text.color': '#222222', 'axes.labelcolor': '#333333'}):
        fig, axes = plt.subplots(3, 1, figsize=(7.4, 7.7))
        fig.subplots_adjust(left=.30, right=.97, bottom=.08, top=.91, hspace=.32)
        for ax, (name, (label, color)) in zip(axes, DEPLOYMENTS.items()):
            gains = values[name].to_numpy()
            ax.barh(np.arange(9), gains, color=color, height=.65, zorder=3)
            ax.set(yticks=np.arange(9), yticklabels=[LABELS[k] for k in values.index],
                   xlim=(0, xmax), ylim=(8.65, -.65))
            ax.set_title(label, loc='left', color=color, fontsize=11, fontweight='bold', pad=7)
            ax.xaxis.set_major_locator(MultipleLocator(.08))
            ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            ax.grid(axis='x', color='#E5E7EB', linewidth=.6)
            ax.set_axisbelow(True)
            ax.tick_params(axis='y', length=0, pad=8)
            ax.tick_params(axis='x', length=3, color='#AAAAAA', labelsize=9)
            for side in ('top', 'right', 'left'):
                ax.spines[side].set_visible(False)
            ax.spines['bottom'].set_color('#BBBBBB')
            ax.spines['bottom'].set_linewidth(.6)
        fig.suptitle('XGBoost feature importance across LLM deployments',
                     fontsize=13, fontweight='bold', x=.51, y=.978)
        fig.supxlabel('Normalized training gain', fontsize=11, x=.635, y=.025)
        fig.supylabel('Chess position characteristic', fontsize=11, x=.025, y=.50)
        for suffix in ('png', 'pdf'):
            fig.savefig(destination / f'xgboost_feature_importance.{suffix}', dpi=400,
                        facecolor='white', bbox_inches='tight', pad_inches=.12)
    return fig


if __name__ == '__main__':
    plt.switch_backend('Agg')
    figure = plot_xgboost_feature_importance(ROOT / 'data/analysis/one_move_v1/final',
                                           ROOT / 'figures/one_move_v1/final')
    plt.close(figure)
