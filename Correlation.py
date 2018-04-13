import Metrics
import Parser

# Use this dummy technique list for now
technique_list = ['SliceAndDice', 'SquarifiedTreeMap']


def scatter(dataset_id):

    for technique_id in technique_list:
        history = Parser.parse_rectangles(technique_id, dataset_id)

        for revision in range(len(history) - 1):
            delta_data = Metrics.compute_delta_data(history[revision], history[revision + 1])
            break

    return None