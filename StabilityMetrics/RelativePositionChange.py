import pandas as pd
import numpy as np
from Util import Parser, Globals
from Visualizations import TimeBoxplot, MatrixPlot

technique_list = Parser.list_techniques(sibgrapi=True)


def plot_time_boxplot(dataset_id):
    data = []
    for i, technique_id in enumerate(technique_list):
        technique_data = []
        history = Parser.parse_rectangles(technique_id, dataset_id)
        for revision in range(len(history) - 1):
            rpc = relative_position_change_wrapper(history[revision], history[revision + 1])
            technique_data.append(rpc)
        data.append(technique_data)
        print(Globals.acronyms[technique_id], end=' ', flush=True)

    TimeBoxplot.plot(data, technique_list,
                     title="RPC - " + dataset_id)


def plot_matrix(dataset_ids):
    matrix = []
    for dataset_id in dataset_ids:
        dataset_values = []
        for technique_id in technique_list:
            history = Parser.parse_rectangles(technique_id, dataset_id)
            all_ratios = np.array([])
            for revision in range(len(history) - 1):
                distances = relative_position_change_wrapper(history[revision], history[revision + 1])
                all_ratios = np.append(all_ratios, distances.values)

            dataset_values.append(all_ratios.mean())
            print(Globals.acronyms[technique_id], dataset_id, all_ratios.mean())
        matrix.append(dataset_values)

    matrix = np.array(matrix).transpose()

    MatrixPlot.plot(matrix, dataset_ids, technique_list,
                    cell_text=True,
                    title='RPC')

# Relative Position Change Metric from 'Stable Treemaps via Local Moves' 2017
#  Contains a list of the rectangles in the current and in the new iteration. Only those rectangles present in both are
#  there a object in the list should contain "x1","x2","y1","y2" values
def relative_position_change_wrapper(df1, df2):
    df = pd.merge(df1, df2, how='inner', left_index=True, right_index=True)  # Retain only rows in both sets
    df.columns = ['x1', 'y1', 'w1', 'h1', 'x2', 'y2', 'w2', 'h2']

    df['w1'] = df['x1'] + df['w1']
    df['h1'] = df['y1'] + df['h1']

    df['w2'] = df['x2'] + df['w2']
    df['h2'] = df['y2'] + df['h2']

    # Coords from 1st revision and coords from 2nd revision
    df.columns = ['x11', 'y11', 'x12', 'y12', 'x21', 'y21', 'x22', 'y22']

    scores = get_relative_score(df)
    return scores


def get_relative_score(df):
    m = df.as_matrix()
    N = len(m)
    scores = pd.Series(np.zeros(N), index=df.index)

    revision_stability = 0
    for i in range(N):
        item_stability = 0
        for j in range(N):
            if i != j:
                old_percentage = getRelativePositions(m[i][0], m[i][2], m[i][1], m[i][3],
                                                      m[j][0], m[j][2], m[j][1], m[j][3])
                new_percentage = getRelativePositions(m[i][4], m[i][6], m[i][5], m[i][7],
                                                      m[j][4], m[j][6], m[j][5], m[j][7])
                pair_stability = getQuadrantStability(old_percentage, new_percentage)
                item_stability += pair_stability
                revision_stability += pair_stability
        if N > 1:
            scores.iloc[i] = (item_stability / (N - 1))
        else:
            scores.iloc[i] = 0
    # revision_stability = revision_stability / (pow(N, 2) - N)
    return scores


def getQuadrantStability(percentagesOld, percentagesNew):
    stability = 0
    for i in range(0, 8):
        oldPercentage = percentagesOld[i]
        newPercentage = percentagesNew[i]
        stability += abs(oldPercentage - newPercentage) / 2
    return stability


# gets the relative positions per quadrant from r1 to r2
def getRelativePositions(x11, x12, y11, y12, x21, x22, y21, y22):
    E = 0
    NE = 0
    N = 0
    NW = 0
    W = 0
    SW = 0
    S = 0
    SE = 0

    if (x21 >= x12):
        # Strictly east
        if (y21 < y11):
            # at least partially in NE
            # get the percentage that r2 is in NE
            NE = (y11 - y21) / (y22 - y21)
            NE = min(1, NE)

        if (y22 > y12):
            # at least partiall in SE
            SE = (y22 - y12) / (y22 - y21)
            SE = min(1, SE)

            # remainder is in east
            E = 1 - NE - SE
    elif (x22 <= x11):
        # strictly west
        if (y21 < y11):
            # at least partially in NW
            # get the percentage that r2 is in NW
            NW = (y11 - y21) / (y22 - y21)
            NW = min(1, NW)

        if (y22 > y12):
            # at least partiall in SW
            SW = (y22 - y12) / (y22 - y21)
            SW = min(1, SW)

            # remainder is in west
            W = 1 - NW - SW
    elif (y22 <= y11):
        # strictly North
        if (x21 < x11):
            # at least partially in NW
            # get the percentage that r2 is in NW
            NW = (x11 - x21) / (x22 - x21)
            NW = min(1, NW)

        if (x22 > x12):
            # at least partiall in SW
            NE = (x22 - x12) / (x22 - x21)
            NE = min(1, NE)

            # remainder is in west
            N = 1 - NW - NE
    else:
        # strictly south
        if (x21 < x11):
            # at least partially in SW
            # get the percentage that r2 is in NW
            SW = (x11 - x21) / (x22 - x21)
            SW = min(1, SW)

        if (x22 > x12):
            # at least partiall in SE
            SE = (x22 - x12) / (x22 - x21)
            SE = min(1, SE)

            # remainder is in west
            S = 1 - SW - SE

    quadrant = []
    quadrant.append(E)
    quadrant.append(NE)
    quadrant.append(N)
    quadrant.append(NW)
    quadrant.append(W)
    quadrant.append(SW)
    quadrant.append(S)
    quadrant.append(SE)
    return quadrant
