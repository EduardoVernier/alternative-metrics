import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

import Metrics
import Parser
import Globals

#technique_list = ['SliceAndDice', 'SquarifiedTreeMap']
technique_list = Parser.list_techniques()

def plot_time_boxplot(dataset_id):

    fig, axs = plt.subplots(int(len(technique_list) / 2), 2, sharex=True, sharey=True, figsize=(20, 44))

    for i, technique_id in enumerate(technique_list):
        ax = fig.axes[i]
        ax.set_title(Globals.acronyms[technique_id])

        data = []
        history = Parser.parse_rectangles(technique_id, dataset_id)
        for revision in range(len(history) - 1):
            un_mov = Metrics.compute_unavoidable_movement(history[revision], history[revision + 1])
            delta_vis = Metrics.compute_delta_vis(history[revision], history[revision + 1])

            diff = delta_vis - un_mov
            data.append(diff)

        bp = ax.boxplot(data, whis=[5, 95], showfliers=False, patch_artist=True, widths=1)

        ax.set_ylim(ymin=-0, ymax=1)
        ax.set_yticks([0, .25, .5, .75, 1], minor=False)
        ax.set_yticklabels([0, .25, .5, .75, 1], fontdict=None, minor=False)
        styleBoxplot(bp, fig, ax, len(history) - 1)

    plt.show()


def styleBoxplot(bp, fig, ax, n_revisions):
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
                                                     linewidth=((get_ax_size(fig, ax)[0]) / (n_revisions)) * 1.08,
                                                     facecolor='black')])
    for cap in bp['caps']:
        cap.set(color='#FFFFFF', linewidth=0)

    # Set only 3 ticks on x
    ax.set_xticks([1, n_revisions / 2, n_revisions], minor=False)
    ax.set_xticklabels([1, int(n_revisions / 2), n_revisions], fontdict=None, minor=False)
    # ax.set_xticklabels(["", "", ""], fontdict=None, minor=False)

    # Remove extra spines and ticks
    #ax.spines['top'].set_visible(False)
    #ax.spines['right'].set_visible(False)
    ax.spines['left'].set_zorder(100)
    ax.tick_params(axis='x', which='both', top='off', direction='out')
    ax.tick_params(axis='y', which='both', right='off', left='on', direction='out')

def unavoidable_matrix(dataset_ids):

    matrix = []
    for dataset_id in dataset_ids:
        dataset_values = []
        for technique_id in technique_list:
            history = Parser.parse_rectangles(technique_id, dataset_id)
            all_unavoidable = np.array([])
            for revision in range(len(history) - 1):
                un_mov = Metrics.compute_unavoidable_movement(history[revision], history[revision + 1])
                delta_vis = Metrics.compute_delta_vis(history[revision], history[revision + 1])

                diff = delta_vis - un_mov
                all_unavoidable = np.append(all_unavoidable, diff.values)

            dataset_values.append(all_unavoidable.mean())
            print(Globals.acronyms[technique_id], dataset_id, all_unavoidable.mean())
        matrix.append(dataset_values)

    matrix = np.array(matrix).transpose()
    plot_matrix(matrix, dataset_ids, technique_list)
    return None

def plot_matrix(matrix, dataset_ids, technique_ids):

    fig = plt.figure()
    ax = fig.add_subplot(111)
    mat = ax.matshow(matrix, cmap=plt.cm.viridis)

    # Ticks, labels and grids
    ax.set_xticklabels(dataset_ids, rotation='vertical')
    ax.set_xticks(range(len(dataset_ids)), minor=False)
    ax.set_yticklabels([Globals.acronyms[t] for t in technique_ids])
    ax.set_yticks(range(len(technique_ids)), minor=False)
    ax.set_xticks([x - 0.5 for x in plt.gca().get_xticks()][1:], minor='true')
    ax.set_yticks([y - 0.5 for y in plt.gca().get_yticks()][1:], minor='true')
    plt.grid(which='minor', color='#999999', linestyle='-', linewidth=1)
    ax.tick_params(axis=u'both', which=u'both', length=0)

    # Add the text
    x_start = 0.0
    x_end = len(dataset_ids)
    y_start = 0.0
    y_end = len(technique_ids)

    jump_x = (x_end - x_start) / (2.0 * len(dataset_ids))
    jump_y = (y_end - y_start) / (2.0 * len(technique_ids))
    x_positions = np.linspace(start=x_start - 0.5, stop=x_end - 0.5, num=len(dataset_ids), endpoint=False)
    y_positions = np.linspace(start=y_start - 0.5, stop=y_end - 0.5, num=len(technique_ids), endpoint=False)

    for y_index, y in enumerate(y_positions):
        for x_index, x in enumerate(x_positions):
            label = "{0:.3f}".format(matrix[y_index][x_index]).lstrip('0')
            text_x = x + jump_x
            text_y = y + jump_y
            ax.text(text_x, text_y, label, color='black', ha='center', va='center', fontsize=9)

    fig.colorbar(mat)
    fig.tight_layout()
    # fig.savefig('matrices/matrix-'+ metric_id +'.png', dpi=600)
    plt.show()