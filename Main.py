import sys
import Correlation

action = sys.argv[1]

# Correlation based visualizations
if action == 'correlation-scatter':
    dataset_id = sys.argv[2]
    Correlation.scatter(dataset_id)
