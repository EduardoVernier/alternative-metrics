import sys
import Correlation
import UnavoidableEnvelope
import UnavoidableMovement
import DeltaMetrics

action = sys.argv[1]

# Correlation based visualizations
if action == 'correlation-scatter':
    dataset_id = sys.argv[2]
    Correlation.scatter(dataset_id)

elif action == 'pearson-matrix':
    dataset_ids = sys.argv[2:]
    Correlation.pearson_matrix(dataset_ids)

elif action == 'unavoidable-envelope':
    UnavoidableEnvelope.unavoidable_envelope()

elif action == 'unavoidable-boxplots':
    dataset_id = sys.argv[2]
    UnavoidableMovement.plot_time_boxplot(dataset_id)

elif action == 'unavoidable-matrix':
    dataset_ids = sys.argv[2:]
    UnavoidableMovement.unavoidable_matrix(dataset_ids)

elif action == 'delta-ratio-matrix':
    dataset_ids = sys.argv[2:]
    DeltaMetrics.delta_ratio_matrix(dataset_ids)

elif action == 'delta-diff-matrix':
    dataset_ids = sys.argv[2:]
    DeltaMetrics.delta_diff_matrix(dataset_ids)
