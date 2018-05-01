import matplotlib.pyplot as plt
import numpy as np

import Globals


def plot(matrix, dataset_ids, technique_ids, shared_cm, cell_text, title=None, show=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    if shared_cm:
        # The colormap range is independent for each column
        for col in range(matrix.shape[1]):
            # Make all rows invalid (fill with 1) except the target one (col)
            m = np.ones_like(matrix)
            m[:, col] = 0
            masked = np.ma.masked_array(matrix, m)
            ax.matshow(masked, cmap=plt.cm.viridis)
    else:
        # All column share same colormap range
        mat = ax.matshow(matrix, cmap=plt.cm.viridis)
        fig.colorbar(mat)

    # Ticks, labels and grids
    ax.set_xticklabels(dataset_ids, rotation='vertical')
    ax.set_xticks(range(len(dataset_ids)), minor=False)
    ax.set_yticklabels([Globals.acronyms[t] for t in technique_ids])
    ax.set_yticks(range(len(technique_ids)), minor=False)
    ax.set_xticks([x - 0.5 for x in plt.gca().get_xticks()][1:], minor='true')
    ax.set_yticks([y - 0.5 for y in plt.gca().get_yticks()][1:], minor='true')
    plt.grid(which='minor', color='#999999', linestyle='-', linewidth=1)
    ax.tick_params(axis=u'both', which=u'both', length=0)

    x_start = 0.0
    x_end = len(dataset_ids)
    y_start = 0.0
    y_end = len(technique_ids)

    # Add the text
    if cell_text:
        jump_x = (x_end - x_start) / (2.0 * len(dataset_ids))
        jump_y = (y_end - y_start) / (2.0 * len(technique_ids))
        x_positions = np.linspace(start=x_start - 0.5, stop=x_end - 0.5, num=len(dataset_ids), endpoint=False)
        y_positions = np.linspace(start=y_start - 0.5, stop=y_end - 0.5, num=len(technique_ids), endpoint=False)

        for y_index, y in enumerate(y_positions):
            for x_index, x in enumerate(x_positions):
                label = "{0:.3f}".format(matrix[y_index][x_index]).lstrip('0')
                text_x = x + jump_x
                text_y = y + jump_y
                ax.text(text_x, text_y, label, color='black', ha='center', va='center', fontsize=5)

    # fig.tight_layout()

    if title is not None:
        ax.text(x_end / 2, y_end * 1.2, title, color='black', ha='center', va='center', fontsize=12)

        filename = title.replace(' ', '').lower()
        filename += '-'
        filename += 'I' if shared_cm else 'S'
        filename += '-'
        filename += 'T' if cell_text else 'NT'
        filename += '.png'
        fig.savefig(Globals.plot_subdir + filename, dpi=500)

    if show:
        plt.show()