import pandas as pd
import math


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
    def area_change(item):
        return abs(item['w0'] * item['h0'] - item['w1'] * item['h1'])

    base_width = (t0['x'] + t0['w']).max()
    base_height = (t0['y'] + t0['h']).max()
    norm = base_height * base_width  # Normalize by base area

    df = pd.merge(t0, t1, how='inner', left_index=True, right_index=True)
    df.columns = ['x0', 'y0', 'w0', 'h0', 'x1', 'y1', 'w1', 'h1']
    return df.apply(lambda r: area_change(r) / norm, axis=1)


#
def compute_unavoidable_movement(t0, t1):
    pass

