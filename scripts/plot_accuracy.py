"""Render the manuscript success plot from unchanged saved estimates."""
from pathlib import Path
import ast
import csv

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, PercentFormatter

ROOT = Path(__file__).resolve().parents[1]
COLORS = {
    'GPT-OSS 120B': '#0072B2',
    'Gemini 3.5 Flash-Lite': '#009E73',
    'Claude Haiku 5.5': '#D55E00',
}


def plot_accuracy(rows, destination):
    """Use exact saved Wilson bounds; return the figure for notebook display."""
    indexed = {row['Model']: row for row in rows}
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with plt.rc_context({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'pdf.fonttype': 42, 'ps.fonttype': 42,
                         'axes.labelcolor': '#333333', 'text.color': '#222222'}):
        fig, ax = plt.subplots(figsize=(7.6, 2.9))
        fig.subplots_adjust(left=.255, right=.97, top=.81, bottom=.22)
        for y, (name, color) in enumerate(COLORS.items()):
            row = indexed[name]
            value = float(row['Accuracy']) * 100
            bounds = row['wilson_95']
            if isinstance(bounds, str):
                bounds = ast.literal_eval(bounds)
            low, high = (float(bound) * 100 for bound in bounds)
            ax.errorbar(value, y, xerr=[[value-low], [high-value]],
                        fmt='o', color=color, markersize=7.5,
                        elinewidth=1.8, capsize=4, capthick=1.5, zorder=3)
            ax.annotate(f'{value:.1f}%', (high, y), xytext=(8, 0),
                        textcoords='offset points', va='center', fontsize=10,
                        fontweight='medium', color=color)
        ax.set(xlim=(30, 65), ylim=(2.45, -.45),
               yticks=range(3), yticklabels=list(COLORS),
               xlabel='Official move mention success (%)')
        ax.xaxis.set_major_locator(MultipleLocator(5))
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
        ax.grid(axis='x', color='#E5E7EB', linewidth=.65)
        ax.set_axisbelow(True)
        ax.tick_params(axis='y', length=0, pad=9)
        ax.tick_params(axis='x', length=3, color='#AAAAAA')
        ax.xaxis.labelpad = 10
        ax.yaxis.labelpad = 12
        for side in ('top', 'right', 'left'):
            ax.spines[side].set_visible(False)
        ax.spines['bottom'].set_color('#BBBBBB')
        ax.spines['bottom'].set_linewidth(.6)
        fig.suptitle('Overall success on 1,000 shared chess puzzles',
                     x=.52, y=.94, fontsize=11.5, fontweight='bold')
        for suffix in ('png', 'pdf'):
            fig.savefig(destination / f'accuracy.{suffix}', dpi=400,
                        facecolor='white', bbox_inches='tight', pad_inches=.12)
    return fig


if __name__ == '__main__':
    plt.switch_backend('Agg')
    with (ROOT / 'writing/final_tables/accuracy.csv').open(newline='', encoding='utf-8') as source:
        rows = list(csv.DictReader(source))
    figure = plot_accuracy(rows, ROOT / 'figures/one_move_v1/final')
    plt.close(figure)
