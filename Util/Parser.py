import glob
import os
import re

import pandas as pd

from Util import Globals


def parse_rectangles(technique_id, dataset_id):
    path = Globals.rectangle_dir + '/' + technique_id + '/' + dataset_id
    files = [filename for filename in glob.iglob(path + '**/*.rect', recursive=True)]
    files = natural_sort(files)
    # Read each file into a dataframe
    dfs = [pd.read_csv(file, names=['id', 'x', 'y', 'w', 'h'], index_col='id') for file in files]
    return dfs


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def list_techniques(sibgrapi=False):
    techniques = natural_sort(os.listdir(Globals.rectangle_dir))
    if not sibgrapi:
        if 'IncrementalLayoutWithMoves' in techniques:
            techniques.remove('IncrementalLayoutWithMoves')
        if 'IncrementalLayoutWithoutMoves' in techniques:
            techniques.remove('IncrementalLayoutWithoutMoves')
        if 'git' in techniques:
            techniques.remove('git')

    # Sort according to acronym
    aux = [(Globals.acronyms[t], t) for t in techniques]
    aux.sort(key=lambda tup: tup[0])
    techniques = [tup[1] for tup in aux]
    return techniques
