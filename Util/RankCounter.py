import pandas as pd
from Util import Globals


def count_to_csv(csv_paths):

    dfs = []
    for path in csv_paths:
        dfs.append(pd.read_csv(path, index_col=0))

    # Initialize counter
    columns = [str(i + 1) for i in range(len(dfs[0].index))]
    counter = pd.DataFrame(0, index=dfs[0].index, columns=columns)

    # Count
    for df in dfs:
        for column in df.columns:
            sorted = df.sort_values(column, ascending=False)
            for position, tech in enumerate(sorted.index):
                counter[str(position + 1)][tech] += 1

    counter.index = [Globals.acronyms[i] for i in counter.index]

    # Sort according to score
    for key, row in counter.iterrows():
        score = 0
        for pos, value in enumerate(row):
            score += (pos + 1) * value
        counter.loc[key, 'score'] = score

    counter = counter.sort_values('score', ascending=True)
    counter.drop(columns='score', inplace=True)

    counter.to_csv(Globals.plot_subdir + 'table.csv')
