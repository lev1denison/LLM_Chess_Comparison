"""Render observed rating-band proportions and their saved Wilson intervals."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, PercentFormatter
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
COLORS = {
    'GPT-OSS 120B': '#0072B2',
    'Gemini 3.5 Flash-Lite': '#009E73',
    'Claude Haiku 5.5': '#D55E00',
}


def plot_rating_band_accuracy(bands, destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with plt.rc_context({'font.family': 'DejaVu Sans', 'font.size': 11,
                         'pdf.fonttype': 42, 'ps.fonttype': 42,
                         'text.color': '#222222', 'axes.labelcolor': '#333333'}):
        fig, ax = plt.subplots(figsize=(8, 4.8))
        for (name, color), offset in zip(COLORS.items(), [-.18, 0, .18]):
            table = bands.loc[bands.Model.eq(name)].set_index('rating_band').loc[['low', 'middle', 'high']]
            assert table.n.tolist() == [334, 333, 333]
            np.testing.assert_allclose(table.accuracy, table.correct / table.n, rtol=0, atol=1e-15)
            assert table.ci_low.min() >= .20 and table.ci_high.max() <= .85
            ax.errorbar(np.arange(3) + offset, table.accuracy,
                        yerr=[table.accuracy - table.ci_low, table.ci_high - table.accuracy],
                        fmt='o', linestyle='none', markersize=7.5, capsize=4,
                        elinewidth=1.7, capthick=1.5, color=color, label=name, zorder=3)
        ax.set(xticks=[0, 1, 2], xticklabels=['Easy', 'Medium', 'Difficult'],
               xlim=(-.45, 2.45), ylim=(.20, .85), xlabel='Chess puzzle difficulty',
               ylabel='Official move mention success (%)',
               title='Observed LLM success across puzzle difficulty levels')
        ax.title.set_fontsize(14)
        ax.title.set_fontweight('bold')
        ax.title.set_position((.5, 1.035))
        ax.yaxis.set_major_locator(MultipleLocator(.1))
        ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
        ax.grid(axis='y', color='#E5E7EB', linewidth=.7)
        ax.set_axisbelow(True)
        ax.legend(loc='upper right', frameon=False, fontsize=10,
                  borderaxespad=.8, labelspacing=.6)
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
            fig.savefig(destination / f'rating_band_accuracy.{suffix}', dpi=400,
                        facecolor='white', bbox_inches='tight', pad_inches=.12)
    return fig


if __name__ == '__main__':
    plt.switch_backend('Agg')
    bands = pd.read_csv(ROOT / 'writing/final_tables/rating_band_accuracy.csv')
    figure = plot_rating_band_accuracy(bands, ROOT / 'figures/one_move_v1/final')
    plt.close(figure)
