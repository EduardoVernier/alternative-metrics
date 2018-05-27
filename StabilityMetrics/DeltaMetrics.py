import numpy as np
import pandas as pd
import math

from Util import Globals, Parser
from Visualizations import MatrixPlot, TimeBoxplot

technique_list = Parser.list_techniques(sibgrapi=True)

# delta_vis has the same definition as the normalized corner travel from the vis18 paper
def compute_delta_vis(t0, t1):
    base_width = (t0['x'] + t0['w']).max()
    base_height = (t0['y'] + t0['h']).max()
    # Normalize by 4 * hypotenuse
    norm = 4 * math.sqrt(base_width ** 2 + base_height ** 2)

    df = pd.merge(t0, t1, how='inner', left_index=True, right_index=True)
    df.columns = ['x0', 'y0', 'w0', 'h0', 'x1', 'y1', 'w1', 'h1']
    return df.apply(lambda r: corner_travel(*list(r)) / norm, axis=1)


def corner_travel(*args):
    x0, y0, w0, h0, x1, y1, w1, h1 = args
    return point_distance(x0, y0, x1, y1)   \
        + point_distance(x0 + w0, y0, x1 + w1, y1)   \
        + point_distance(x0, y0 + h0, x1, y1 + h1)   \
        + point_distance(x0 + w0, y0 + h0, x1 + w1, y1 + h1)


def point_distance(x0, y0, x1, y1):
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


# delta_data is the change in the normalized area of a cell
def compute_delta_data(t0, t1):
    base_width = (t0['x'] + t0['w']).max()
    base_height = (t0['y'] + t0['h']).max()
    norm = base_height * base_width  # Normalize by base area

    df = pd.merge(t0, t1, how='inner', left_index=True, right_index=True)
    df.columns = ['x0', 'y0', 'w0', 'h0', 'x1', 'y1', 'w1', 'h1']
    return (abs(df['w0'] * df['h0'] - df['w1'] * df['h1'])) / norm


# from the eurovis proposal
#  ratio = (1-delta_vis)/(1-delta_data)
def delta_ratio_matrix(dataset_ids):
    matrix = []
    for dataset_id in dataset_ids:
        dataset_values = []
        for technique_id in technique_list:
            history = Parser.parse_rectangles(technique_id, dataset_id)
            all_ratios = np.array([])
            for revision in range(len(history) - 1):
                delta_vis = compute_delta_vis(history[revision], history[revision + 1])
                delta_data = compute_delta_data(history[revision], history[revision + 1])
                ratio = (1 - delta_vis) / (1 - delta_data)
                all_ratios = np.append(all_ratios, ratio.values)

            dataset_values.append(all_ratios.mean())
            print(Globals.acronyms[technique_id], dataset_id, all_ratios.mean())
        matrix.append(dataset_values)

    matrix = np.array(matrix).transpose()

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=False,
                    cell_text=True,
                    title='Delta ratio')

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=True,
                    cell_text=True,
                    title='Delta ratio')

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=False,
                    cell_text=False,
                    title='Delta ratio')

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=True,
                    cell_text=False,
                    title='Delta ratio')


def delta_ratio_boxplots(dataset_id):
    data = []
    for i, technique_id in enumerate(technique_list):
        technique_data = []
        history = Parser.parse_rectangles(technique_id, dataset_id)
        for revision in range(len(history) - 1):
            delta_vis = compute_delta_vis(history[revision], history[revision + 1])
            delta_data = compute_delta_data(history[revision], history[revision + 1])
            ratios = (1 - delta_vis) / (1 - delta_data)
            technique_data.append(ratios)
        data.append(technique_data)

    TimeBoxplot.plot(data, technique_list,
                     title="Delta Ratio - " + dataset_id)

    TimeBoxplot.plot(data, technique_list,
                     median_sorted=True,
                     title="Delta Ratio - " + dataset_id)


#  mod = 1 - abs(delta_vis - delta_data)
def delta_diff_matrix(dataset_ids):
    matrix = []
    for dataset_id in dataset_ids:
        dataset_values = []
        for technique_id in technique_list:
            history = Parser.parse_rectangles(technique_id, dataset_id)
            all_diffs = np.array([])
            for revision in range(len(history) - 1):
                delta_vis = compute_delta_vis(history[revision], history[revision + 1])
                delta_data = compute_delta_data(history[revision], history[revision + 1])
                diffs = 1 - abs(delta_vis - delta_data)
                all_diffs = np.append(all_diffs, diffs.values)

            dataset_values.append(all_diffs.mean())
            print(Globals.acronyms[technique_id], dataset_id, all_diffs.mean())
        matrix.append(dataset_values)

    matrix = np.array(matrix).transpose()

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=False,
                    cell_text=True,
                    title='Delta diff')

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=True,
                    cell_text=True,
                    title='Delta diff')

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=False,
                    cell_text=False,
                    title='Delta diff')

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=True,
                    cell_text=False,
                    title='Delta diff')


def delta_diff_boxplots(dataset_id):
    data = []
    for i, technique_id in enumerate(technique_list):
        technique_data = []
        history = Parser.parse_rectangles(technique_id, dataset_id)
        for revision in range(len(history) - 1):
            delta_vis = compute_delta_vis(history[revision], history[revision + 1])
            delta_data = compute_delta_data(history[revision], history[revision + 1])
            diffs = 1 - abs(delta_vis - delta_data)
            technique_data.append(diffs)
        data.append(technique_data)

    TimeBoxplot.plot(data, technique_list,
                     title="Delta Diff - " + dataset_id)

    TimeBoxplot.plot(data, technique_list,
                     median_sorted=True,
                     title="Delta Diff - " + dataset_id)
