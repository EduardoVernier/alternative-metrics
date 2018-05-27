from scipy.stats import stats

from Util import Globals, Parser
from Visualizations import TimeBoxplot

technique_list = Parser.list_techniques()
#technique_list = ['SliceAndDice', 'SquarifiedTreeMap']

def plot_mean_boxplot(dataset_id):
    data = []
    for i, technique_id in enumerate(technique_list):
        print(Globals.acronyms[technique_id], end=' ', flush=True)
        technique_data = []
        history = Parser.parse_rectangles(technique_id, dataset_id)
        for revision in range(len(history) - 1):
            delta_vis = RawMetrics.compute_delta_vis(history[revision], history[revision + 1])
            delta_data = RawMetrics.compute_delta_data(history[revision], history[revision + 1])
            un_mov = RawMetrics.compute_unavoidable_movement(history[revision], history[revision + 1])

            ratios = (1 - delta_vis) / (1 - delta_data)
            diffs = 1 - abs(delta_vis - delta_data)
            unavoidable = 1 - (delta_vis - un_mov)

            mean = (ratios + diffs + unavoidable) / 3
            technique_data.append(mean)
        data.append(technique_data)

    TimeBoxplot.plot(data, technique_list,
                     title='Mean - ' + dataset_id)

    TimeBoxplot.plot(data, technique_list,
                     median_sorted=True,
                     title='Mean - ' + dataset_id)


def plot_mean_boxplot_with_pearson(dataset_id):
    data = []
    pearson = []
    for i, technique_id in enumerate(technique_list):
        print(Globals.acronyms[technique_id], end=' ', flush=True)
        technique_pearson = []
        technique_data = []
        history = Parser.parse_rectangles(technique_id, dataset_id)
        for revision in range(len(history) - 1):
            delta_vis = RawMetrics.compute_delta_vis(history[revision], history[revision + 1])
            delta_data = RawMetrics.compute_delta_data(history[revision], history[revision + 1])
            un_mov = RawMetrics.compute_unavoidable_movement(history[revision], history[revision + 1])

            ratios = (1 - delta_vis) / (1 - delta_data)
            diffs = 1 - abs(delta_vis - delta_data)
            unavoidable = 1 - (delta_vis - un_mov)
            mean = (ratios + diffs + unavoidable) / 3
            technique_data.append(mean)

            # Compute linear regression statistics
            _, _, r_value, _, _= stats.linregress(delta_data, delta_vis)
            technique_pearson.append(r_value if r_value > 0 else 0)

        data.append(technique_data)
        pearson.append(technique_pearson)

    TimeBoxplot.plot_with_pearson(data, technique_list, pearson,
                                  title='Mean with Pearson - ' + dataset_id)

