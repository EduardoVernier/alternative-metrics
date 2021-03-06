import numpy as np

from Util import Globals, Parser
from Visualizations import MatrixPlot, TimeBoxplot

technique_list = Parser.list_techniques(sibgrapi=True)


# Aspect ratio computation
def compute_aspect_ratios(t):
    return t[['w', 'h']].min(axis=1) / t[['w', 'h']].max(axis=1)


def plot_time_boxplot(dataset_id):
    data = []
    for i, technique_id in enumerate(technique_list):
        technique_data = []
        history = Parser.parse_rectangles(technique_id, dataset_id)
        for revision in range(len(history)):
            ratios = compute_aspect_ratios(history[revision]).tolist()
            technique_data.append(ratios)
        data.append(technique_data)

    TimeBoxplot.plot(data, technique_list,
                     title="Aspect Ratios - " + dataset_id)

    TimeBoxplot.plot(data, technique_list,
                     median_sorted=True,
                     title="Aspect Ratios - " + dataset_id)


def plot_ar_matrix(dataset_ids):
    matrix = []
    for dataset_id in dataset_ids:
        dataset_values = []
        for technique_id in technique_list:
            history = Parser.parse_rectangles(technique_id, dataset_id)
            all_ratios = np.array([])
            for revision in range(len(history) - 1):
                ratios = compute_aspect_ratios(history[revision])
                all_ratios = np.append(all_ratios, ratios.values)

            dataset_values.append(all_ratios.mean())
            print(Globals.acronyms[technique_id], dataset_id, all_ratios.mean())
        matrix.append(dataset_values)

    matrix = np.array(matrix).transpose()

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=False,
                    cell_text=True,
                    title='Aspect ratio')

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=True,
                    cell_text=True,
                    title='Aspect ratio')

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=False,
                    cell_text=False,
                    title='Aspect ratio')

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    shared_cm=True,
                    cell_text=False,
                    title='Aspect ratio')
