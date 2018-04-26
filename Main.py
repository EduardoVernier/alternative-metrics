import sys
import os

import Correlation
import UnavoidableEnvelope
import UnavoidableMovement
import DeltaMetrics
import AspectRatio

action = sys.argv[1]

# Create dir to store plots
base_path = 'plots/' + action + '/'
os.makedirs(base_path, exist_ok=True)

# Choose which vis to create
# Correlation based
if action == 'correlation-scatter':
    dataset_id = sys.argv[2]
    Correlation.scatter(dataset_id)

elif action == 'correlation-matrix':
    dataset_ids = sys.argv[2:]
    Correlation.pearson_matrix(dataset_ids)

# Unavoidable movement
elif action == 'unavoidable-envelope':
    UnavoidableEnvelope.unavoidable_envelope()

elif action == 'unavoidable-boxplots':
    dataset_id = sys.argv[2]
    UnavoidableMovement.plot_time_boxplot(dataset_id)

elif action == 'unavoidable-matrix':
    dataset_ids = sys.argv[2:]
    print(dataset_ids)
    UnavoidableMovement.unavoidable_matrix(dataset_ids)

# Delta vis and delta data combination
elif action == 'delta-ratio-matrix':
    dataset_ids = sys.argv[2:]
    DeltaMetrics.delta_ratio_matrix(dataset_ids)

elif action == 'delta-diff-matrix':
    dataset_ids = sys.argv[2:]
    DeltaMetrics.delta_diff_matrix(dataset_ids)

# Aspect Ratio
elif action == 'ar-boxplots':
    dataset_id = sys.argv[2]
    AspectRatio.plot_time_boxplot(dataset_id)

elif action == 'ar-matrix':
    dataset_ids = sys.argv[2:]
    AspectRatio.plot_ar_matrix(dataset_ids)
