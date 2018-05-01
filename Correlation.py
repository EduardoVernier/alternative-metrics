import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.colors import Normalize
from matplotlib.colors import LogNorm
from matplotlib import cm

import Metrics
import Parser
import Globals

# Use this dummy technique list for now
# technique_list = ['SliceAndDice', 'SquarifiedTreeMap']
technique_list = Parser.list_techniques()


def scatter(dataset_id):

    fig, axs = plt.subplots(int(len(technique_list)/2), 2, sharex=True, sharey=True, figsize=(20, 44))

    xlim = 0
    for i, technique_id in enumerate(technique_list):
        # print(Globals.acronyms[technique_id])
        ax = fig.axes[i]

        history = Parser.parse_rectangles(technique_id, dataset_id)
        # Compute all delta_vis and delta_data values for a dataset (1 pair per cell)
        all_delta_data = np.array([])
        all_delta_vis = np.array([])
        for revision in range(len(history) - 1):
            delta_data = Metrics.compute_delta_data(history[revision], history[revision + 1])
            all_delta_data = np.append(all_delta_data, delta_data)

            delta_vis = Metrics.compute_delta_vis(history[revision], history[revision + 1])
            all_delta_vis = np.append(all_delta_vis, delta_vis)

        # Compute linear regression and draw regression line
        slope, intercept, r_value, p_value, std_err = stats.linregress(all_delta_data, all_delta_vis)

        if xlim == 0:
            xlim = np.percentile(all_delta_data, 99.99)  # Remove outliers

        # If there are too many points to handle, first we draw all of them in black (alpha),
        # then subsample the space, perform kde, and draw the colored subsample
        # over the original points
        sample_size = 10000
        if len(all_delta_data) > sample_size:
            ax.scatter(all_delta_data, all_delta_vis, color='k', s=1, alpha=.25)

            # matrix = df[['delta_data', 'delta_vis']].sample(sample_size).T.as_matrix()
            indices = np.random.choice(len(all_delta_vis), sample_size)
            matrix = np.vstack([all_delta_data[indices], all_delta_vis[indices]])
            dens = stats.gaussian_kde(matrix)
            dens_pt = dens(matrix)
            colours = make_colors(dens_pt, 'inferno')
            ax.scatter(matrix[0], matrix[1], color=colours, s=3, alpha=.05)
        else:
            matrix = np.vstack([all_delta_data, all_delta_vis])
            dens = stats.gaussian_kde(matrix)
            dens_pt = dens(matrix)
            colours = make_colors(dens_pt, 'inferno')
            ax.scatter(matrix[0], matrix[1], color=colours, s=3, alpha=.25)

        line = np.poly1d([slope, intercept])(all_delta_data)
        ax.plot(all_delta_data, line, 'r-', lw=.5)

        print(Globals.acronyms[technique_id], r_value)

        title = Globals.acronyms[technique_id]
        title += r"  $\alpha = $" + "{0:.2f}".format(intercept)
        title += r"  $\beta = $" + "{0:.2f}".format(slope)
        title += r"  $r = $" + "{0:.3f}".format(r_value)
        title += r"  $s_e = $" + "{0:.3f}".format(std_err)
        ax.set_title(title)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='x', which='both', top='off')
        ax.tick_params(axis='y', which='both', right='off')
        ax.set_xlim(xmin=0, xmax=xlim)
        ax.set_ylim(ymin=0)

    plt.show()
    return None


def make_colors(vals, cmap):
    norm = Normalize(vmin=vals.min(), vmax=vals.max())
    colors = [cm.ScalarMappable(norm=norm, cmap=cmap).to_rgba(val) for val in vals]
    return colors


def pearson_matrix(dataset_ids):
    r_matrix = []
    for dataset_id in dataset_ids:
        dataset_values = []
        for technique_id in technique_list:
            # print(Globals.acronyms[technique_id], dataset_id)
            history = Parser.parse_rectangles(technique_id, dataset_id)
            # Compute all delta_vis and delta_data values for a dataset (1 pair per cell)
            all_delta_data = np.array([])
            all_delta_vis = np.array([])
            for revision in range(len(history) - 1):
                delta_data = Metrics.compute_delta_data(history[revision], history[revision + 1])
                all_delta_data = np.append(all_delta_data, delta_data)

                delta_vis = Metrics.compute_delta_vis(history[revision], history[revision + 1])
                all_delta_vis = np.append(all_delta_vis, delta_vis)

            # Compute linear regression statistics
            slope, intercept, r_value, p_value, std_err = stats.linregress(all_delta_data, all_delta_vis)

            dataset_values.append(r_value)
            print(Globals.acronyms[technique_id], dataset_id, r_value)
        r_matrix.append(dataset_values)

    r_matrix = np.array(r_matrix).transpose()
    plot_matrix(r_matrix, dataset_ids, technique_list)
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
    x_positions = np.linspace(start=x_start-0.5, stop=x_end-0.5, num=len(dataset_ids), endpoint=False)
    y_positions = np.linspace(start=y_start-0.5, stop=y_end-0.5, num=len(technique_ids), endpoint=False)

    for y_index, y in enumerate(y_positions):
        for x_index, x in enumerate(x_positions):
            label = "{0:.3f}".format(matrix[y_index][x_index]).lstrip('0')
            text_x = x + jump_x
            text_y = y + jump_y
            ax.text(text_x, text_y, label, color='black', ha='center', va='center', fontsize=9)

    fig.colorbar(mat)
    fig.tight_layout()
    #fig.savefig('matrices/matrix-'+ metric_id +'.png', dpi=600)
    plt.show()
