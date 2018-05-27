import pandas as pd
import math
import numpy as np

from Visualizations import TimeBoxplot, MatrixPlot
from Util import Parser, Globals

technique_list = Parser.list_techniques(sibgrapi=True)


# Schneiderman-Wattember metric
def compute_shneiderman(t0, t1):
    base_width = (t0['x'] + t0['w']).max()
    base_height = (t0['y'] + t0['h']).max()
    # Normalize by sqrt(W^2 + H^2 + W^2 + H^2), where W and H are the base Width and Heights of the canvas
    norm = math.sqrt(2 * (base_width ** 2) + 2 * (base_height ** 2))

    df = pd.merge(t0, t1, how='inner', left_index=True, right_index=True)
    df.columns = ['x0', 'y0', 'w0', 'h0', 'x1', 'y1', 'w1', 'h1']
    return df.apply(lambda r: 1 - shneiderman(*list(r)) / norm, axis=1)


def shneiderman(*args):
    x0, y0, w0, h0, x1, y1, w1, h1 = args
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2 + (w0 - w1) ** 2 + (h0 - h1) ** 2)


def plot_time_boxplot(dataset_id):
    data = []
    for i, technique_id in enumerate(technique_list):
        technique_data = []
        history = Parser.parse_rectangles(technique_id, dataset_id)
        for revision in range(len(history) - 1):
            shneiderman = compute_shneiderman(history[revision], history[revision + 1])
            technique_data.append(shneiderman)
        data.append(technique_data)

    TimeBoxplot.plot(data, technique_list,
                     title="Shneiderman - " + dataset_id)


def plot_matrix(dataset_ids):
    matrix = []
    for dataset_id in dataset_ids:
        dataset_values = []
        for technique_id in technique_list:
            history = Parser.parse_rectangles(technique_id, dataset_id)
            all_ratios = np.array([])
            for revision in range(len(history) - 1):
                distances = compute_shneiderman(history[revision], history[revision + 1])
                all_ratios = np.append(all_ratios, distances.values)

            dataset_values.append(all_ratios.mean())
            print(Globals.acronyms[technique_id], dataset_id, all_ratios.mean())
        matrix.append(dataset_values)

    matrix = np.array(matrix).transpose()

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    cell_text=True,
                    title='Shneiderman-Wattenberg')