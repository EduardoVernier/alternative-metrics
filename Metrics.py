import pandas as pd
import math


# delta_vis has the same definition as the normalized corner travel from the vis18 paper
def compute_delta_vis(t0, t1):
    pass


# delta_data is the change in the normalized area of a cell
def compute_delta_data(t0, t1):
    def area_change(item):
        return abs(item['w1'] * item['h1'] - item['w2'] * item['h2'])

    base_width = (t0['x'] + t0['w']).max()
    base_height = (t0['y'] + t0['h']).max()
    norm = base_height * base_width  # Normalize by base area

    df = pd.merge(t0, t1, how='inner', left_index=True, right_index=True)
    df.columns = ['x1', 'y1', 'w1', 'h1', 'x2', 'y2', 'w2', 'h2']
    delta_data = df.apply(lambda r: area_change(r) / norm, axis=1)
    return delta_data


#
def compute_unavoidable_movement(t0, t1):
    pass

