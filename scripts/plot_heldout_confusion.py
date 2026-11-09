"""Render held-out confusion counts with a shared row-percentage color scale."""
from pathlib import Path
import json

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.ticker import PercentFormatter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
COLORS = {
    'GPT-OSS 120B': '#0072B2',
    'Gemini 3.5 Flash-Lite': '#009E73',
    'Claude Haiku 5.5': '#D55E00',
}


def contrast_text(rgba):
    """Choose black/white using relative luminance and contrast ratio."""
    rgb = np.array(rgba[:3])
    linear = np.where(rgb <= .04045, rgb / 12.92, ((rgb + .055) / 1.055) ** 2.4)
    luminance = linear @ np.array([.2126, .7152, .0722])
    return 'black' if (luminance + .05) / .05 >= 1.05 / (luminance + .05) else 'white'


def plot_heldout_confusion(metrics, destination):
    indexed = {metric['Model']: metric for metric in metrics}
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with plt.rc_context({'font.family': 'DejaVu Sans', 'font.size': 11,
                         'pdf.fonttype': 42, 'ps.fonttype': 42,
                         'text.color': '#222222', 'axes.labelcolor': '#333333'}):
        fig, axes = plt.subplots(1, 3, figsize=(13.2, 5.2))
        fig.subplots_adjust(left=.065, right=.98, top=.82, bottom=.31, wspace=.40)
        norm = Normalize(0, 100)
        cmap = plt.get_cmap('Blues')
        for ax, (name, color) in zip(axes, COLORS.items()):
            metric = indexed[name]
            counts = np.asarray(metric['confusion_tn_fp_fn_tp'], dtype=int).reshape(2, 2)
            assert counts.sum() == metric['test_n'] == 200
            assert np.isclose(np.trace(counts) / counts.sum(), metric['accuracy'])
            percentages = 100 * counts / counts.sum(axis=1, keepdims=True)
            im = ax.imshow(percentages, cmap=cmap, norm=norm, aspect='equal', interpolation='nearest')
            for (i, j), count in np.ndenumerate(counts):
                pct = percentages[i, j]
                ax.text(j, i, f'{count} ({pct:.1f}%)', ha='center', va='center',
                        fontsize=11, color=contrast_text(cmap(norm(pct))))
            ax.set(xticks=[0, 1], yticks=[0, 1],
                   xticklabels=['Failure', 'Success'], yticklabels=['Failure', 'Success'],
                   xlabel='Predicted outcome', ylabel='Observed outcome')
            ax.set_title(f"{name} — {metric['accuracy']:.1%} accuracy",
                         color=color, fontsize=11, pad=14, fontweight='bold')
            ax.tick_params(length=0, pad=7)
            ax.xaxis.labelpad = 8
            ax.yaxis.labelpad = 8
            ax.set_xticks([.5], minor=True)
            ax.set_yticks([.5], minor=True)
            ax.grid(which='minor', color='white', linewidth=1.5)
            ax.tick_params(which='minor', length=0)
            for spine in ax.spines.values():
                spine.set_visible(False)
        cax = fig.add_axes([.35, .13, .32, .027])
        colorbar = fig.colorbar(im, cax=cax, orientation='horizontal', ticks=np.arange(0, 101, 20))
        colorbar.ax.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
        colorbar.set_label('Percentage of observed class', fontsize=10, labelpad=4)
        colorbar.ax.tick_params(labelsize=9, length=3)
        colorbar.outline.set_visible(False)
        fig.suptitle('XGBoost prediction of LLM success on held-out puzzles',
                     fontsize=16, fontweight='bold', y=.965)
        for suffix in ('png', 'pdf'):
            fig.savefig(destination / f'heldout_confusion.{suffix}', dpi=400,
                        facecolor='white', bbox_inches='tight', pad_inches=.15)
    return fig


if __name__ == '__main__':
    plt.switch_backend('Agg')
    metrics = json.loads((ROOT / 'data/analysis/one_move_v1/final/heldout_metrics.json').read_text())
    figure = plot_heldout_confusion(metrics, ROOT / 'figures/one_move_v1/final')
    plt.close(figure)
