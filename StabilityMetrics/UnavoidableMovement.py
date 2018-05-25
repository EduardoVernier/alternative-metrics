import numpy as np
import pandas as pd
import math
import scipy

from StabilityMetrics import DeltaMetrics
from Util import Globals, Parser
from Visualizations import MatrixPlot, TimeBoxplot

technique_list = Parser.list_techniques()


# Unavoidable movement
def compute_unavoidable_movement(t0, t1):
    base_width = (t0['x'] + t0['w']).max()
    base_height = (t0['y'] + t0['h']).max()
    # Normalize by 4 * hypotenuse
    norm = 4 * math.sqrt(base_width ** 2 + base_height ** 2)

    df = pd.merge(t0, t1, how='inner', left_index=True, right_index=True)
    df.columns = ['x0', 'y0', 'w0', 'h0', 'x1', 'y1', 'w1', 'h1']
    return df.apply(lambda r: unavoidable_travel(*list(r)) / norm, axis=1)


def point_hyperbole_dist(x, w, h, a):
    # Distance between a point (w,h) and a hyperbole y = a/4x where a is the area we are trying to reach
    return math.sqrt((x - w / 2) ** 2 + (a / (4 * x) - h / 2) ** 2)


def unavoidable_travel(*args):
    x0, y0, w0, h0, x1, y1, w1, h1 = args
    if h0 * w0 - w1 * h1 < 0.00001:
        return 0
    else:
        result = scipy.optimize.minimize(point_hyperbole_dist, x0=w0, args=(w0, h0, w1 * h1))
        optimum_x = result.x[0]
        # Minimum corner travel is 4 times the minimum point-hyperbole distance
        return point_hyperbole_dist(optimum_x, w0, h0, w1 * h1) * 4


# Visualizations
def plot_time_boxplot(dataset_id):
    # data 1st level = technique, 2nd = list of revisions, 3rd = list of observations
    data = []
    for i, technique_id in enumerate(technique_list):
        technique_results = []
        history = Parser.parse_rectangles(technique_id, dataset_id)
        for revision in range(len(history) - 1):
            un_mov = compute_unavoidable_movement(history[revision], history[revision + 1])
            delta_vis = DeltaMetrics.compute_delta_vis(history[revision], history[revision + 1])

            diff = 1 - (delta_vis - un_mov)
            technique_results.append(diff)

        data.append(technique_results)

    TimeBoxplot.plot(data, technique_list,
                     title="Unavoidable Movement - " + dataset_id)

    TimeBoxplot.plot(data, technique_list,
                     median_sorted=True,
                     title="Unavoidable Movement - " + dataset_id)


def unavoidable_matrix(dataset_ids):
    matrix = []
    for dataset_id in dataset_ids:
        dataset_values = []
        for technique_id in technique_list:
            history = Parser.parse_rectangles(technique_id, dataset_id)
            all_unavoidable = np.array([])
            for revision in range(len(history) - 1):
                un_mov = compute_unavoidable_movement(history[revision], history[revision + 1])
                delta_vis = DeltaMetrics.compute_delta_vis(history[revision], history[revision + 1])

                diff = 1 - (delta_vis - un_mov)
                all_unavoidable = np.append(all_unavoidable, diff.values)

            dataset_values.append(all_unavoidable.mean())
            print(Globals.acronyms[technique_id], dataset_id, all_unavoidable.mean())
        matrix.append(dataset_values)

    matrix = np.array(matrix).transpose()

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=False,
                    cell_text=True,
                    title='Unavoidable')

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=True,
                    cell_text=True,
                    title='Unavoidable')

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=False,
                    cell_text=False,
                    title='Unavoidable')

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=True,
                    cell_text=False,
                    title='Unavoidable')
