import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
import math

from Util import Globals


def plot(data_all_tech, technique_list, title=None, median_sorted=False, show=False):
    # How it was for VISSOFT
    # fig, axs = plt.subplots(math.ceil(len(technique_list) / 2), 2, sharex=True, sharey=True, figsize=(9, 18))
    # 5 x 3 layout - SIBGRAPI
    fig, axs = plt.subplots(math.ceil(len(technique_list) / 3), 3, sharex=True, sharey=True, figsize=(10, 8))
    fig.tight_layout()

    for i, technique_id in enumerate(technique_list):
        ax = fig.axes[i]
        ax.set_title(Globals.acronyms[technique_id])

        if median_sorted:  # Don't modify the original data
            data = np.copy(data_all_tech[i])
            data = list(data)
            data.sort(key=lambda x: -np.median(x))
        else:
            data = data_all_tech[i]

        bp = ax.boxplot(data, whis=[5, 95], showfliers=False, patch_artist=True, widths=1)

        style_boxplot(bp, fig, ax, len(data) + 1)

    if title is not None:
        fig.suptitle(title, fontsize=14)
        fig.subplots_adjust(top=0.9)

        fig_name = title.replace(' ', '').lower()
        if median_sorted:
            fig_name += '-S'
        fig_name += '.png'

        fig.savefig(Globals.plot_subdir + fig_name, dpi=300)

    if show:
        plt.show()


def plot_with_pearson(data_all_tech, technique_list, pearson, title=None, median_sorted=False, show=False):
    fig, axs = plt.subplots(int(len(technique_list) / 2), 2, sharex=True, sharey=True, figsize=(9, 18))
    fig.tight_layout()

    for i, technique_id in enumerate(technique_list):
        ax = fig.axes[i]
        ax.set_title(Globals.acronyms[technique_id])

        if median_sorted:  # Don't modify the original data
            data = np.copy(data_all_tech[i])
            data = list(data)
            data.sort(key=lambda x: -np.median(x))
        else:
            data = data_all_tech[i]

        bp = ax.boxplot(data, whis=[5, 95], showfliers=False, patch_artist=True, widths=1)

        style_boxplot(bp, fig, ax, len(data) + 1)

        # (over)plot pearson
        x = range(len(pearson[i]))
        ax.scatter(x, pearson[i], color='red', marker='_', linewidth=5, zorder=20)

    if title is not None:
        fig.suptitle(title, fontsize=14)
        fig.subplots_adjust(top=0.95)

        fig_name = title.replace(' ', '').lower()
        if median_sorted:
            fig_name += '-S'
        fig_name += '.png'

        fig.savefig(Globals.plot_subdir + fig_name, dpi=300)

    if show:
        plt.show()


def style_boxplot(bp, fig, ax, n_revisions):
    def get_ax_size(fig, ax):
        bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        width, height = bbox.width, bbox.height
        width *= fig.dpi
        height *= fig.dpi
        return width, height

    for box in bp['boxes']:
        # change outline color
        box.set(color='#1b9e77',
                linewidth=0,
                path_effects=[pe.Stroke(linewidth=0.1, foreground='#1b9e77'), pe.Normal()],
                facecolor='#1b9e77')
        box.set_zorder(10)
    for i, median in enumerate(bp['medians']):
        median.set(color='#000000',
                   linewidth=2,
                   solid_capstyle="butt",
                   ms=(get_ax_size(fig, ax)[0]) / (n_revisions))
        median.set_zorder(11)
        # median.set_xdata([i + 1 - 0.3, i + 1 + 0.3])
    for whisker in bp['whiskers']:
        whisker.set(color='#CCCCCC',
                    linestyle='-',
                    solid_capstyle="butt")
        whisker.set_path_effects([pe.PathPatchEffect(edgecolor='#CCCCCC',
                                                     linewidth=((get_ax_size(fig, ax)[0]) / n_revisions),
                                                     facecolor='black')])
    for cap in bp['caps']:
        cap.set(color='#FFFFFF', linewidth=0)

    font = {'family': 'monospace',
            'weight': 'normal',
            'size': 8}

    # Set only 3 ticks on x
    ax.set_xticks([1, n_revisions / 2, n_revisions-1], minor=False)
    ax.set_xticklabels([str(1), str(int(n_revisions / 2)), str(n_revisions)], fontdict=font, minor=False)

    ax.set_ylim(ymin=-0, ymax=1)
    ax.set_yticks([0, .25, .5, .75, 1], minor=False)
    ax.set_yticklabels(['0', '.25', '.50', '.75', '1.0'], fontdict=font, minor=False)

    # Remove extra spines and ticks
    #ax.spines['top'].set_visible(False)
    #ax.spines['right'].set_visible(False)
    ax.spines['left'].set_zorder(100)
    ax.tick_params(axis='x', which='both', top='off', direction='out')
    ax.tick_params(axis='y', which='both', right='off', left='on', direction='out')
