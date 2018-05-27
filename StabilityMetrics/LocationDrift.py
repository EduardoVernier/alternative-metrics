import numpy as np
import pandas as pd
import math

from Visualizations import MatrixPlot
from Util import Parser, Globals

technique_list = Parser.list_techniques(False)


def point_distance(x0, y0, x1, y1):
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


def compute_location_drift(dfs):
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

    mean_drift = 0  # Over all cells
    n_unique = len(centroids)

    for index, centroid_list in centroids.items():
        x_mean = 0
        y_mean = 0
        active_revisions = len(centroid_list)
        # Compute centroid for a given index
        for x, y in centroid_list:
            x_mean += x / active_revisions
            y_mean += y / active_revisions

        # Calculate average drift for given cell
        cell_drift = 0
        for x, y in centroid_list:
            cell_drift += point_distance(x, y, x_mean, y_mean) / (math.sqrt(1000**2 + 1000**2) * active_revisions)
        # Calculate drift over all cells
        mean_drift += cell_drift / n_unique
    return mean_drift


def plot_matrix(dataset_ids):
    matrix = []
    for dataset_id in dataset_ids:
        dataset_values = []
        for technique_id in technique_list:
            history = Parser.parse_rectangles(technique_id, dataset_id)
            avg = compute_location_drift(history)
            dataset_values.append(avg)
            print(Globals.acronyms[technique_id], dataset_id, avg)
        matrix.append(dataset_values)

    matrix = np.array(matrix).transpose()

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=False,
                    cell_text=True,
                    invert_colormap=True,
                    title='Location Drift')