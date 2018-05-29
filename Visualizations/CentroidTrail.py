import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import numpy as np
import math
from Util import Globals, Parser

technique_list = Parser.list_techniques(sibgrapi=True)


def compute_centroids(dfs):
    centroids = {}  # Holds arrays with centroids indexed by cell id
    # Add entries to dict
    for revision, df in enumerate(dfs):
        for index, row in df.iterrows():
            c_x = row['x'] + row['w'] / 2
            c_y = row['y'] + row['h'] / 2
            if index in centroids:
                centroids[index].append((c_x, c_y))  # Append tuple
            else:
                centroids[index] = [(c_x, c_y)]  # Initialize list for a new entry
    return centroids


def plot(dataset_id):

    fig, axs = plt.subplots(math.ceil(len(technique_list) / 5), 5)
    fig.suptitle("Centroid Trail - " + dataset_id)

    norm = math.sqrt(1000**2 + 1000**2)  # Assuming we are plotting the treemap in a 1000x1000 pixel frame

    for i, technique_id in enumerate(technique_list):
        ax = fig.axes[i]
        ax.set_title(Globals.acronyms[technique_id])
        history = Parser.parse_rectangles(technique_id, dataset_id)
        centroids = compute_centroids(history)

        lines = []
        colors = []
        for key, centroid_list in centroids.items():
            for i in range(len(centroid_list) - 1):
                a = centroid_list[i]
                b = centroid_list[i + 1]
                lines.append((a, b))  # Add line segment
                alpha = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2) / norm
                alpha = alpha / math.sqrt(len(centroid_list))
                colors.append((0, 0, 0, alpha))  # Set color for line segment

        lc = mc.LineCollection(lines, colors=colors, linewidths=1)
        ax.add_collection(lc)
        ax.set_xlim(0, 1000)
        ax.set_ylim(0, 1000)
        ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
        ax.set_aspect('equal', adjustable='box')

    fig.savefig(Globals.plot_subdir + dataset_id + '.png', dpi=500)
