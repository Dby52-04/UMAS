import gzip
import json
import sys

from sklearn.metrics import roc_auc_score

from umas import score_trajectory

with gzip.open(sys.argv[1], 'rt') as f:
    trajectories = json.load(f)['trajectories']

correct = [t['correct'] for t in trajectories]
umas, fix = zip(*[score_trajectory(t['nodes']) for t in trajectories])

print(f"n={len(correct)}  UMAS_FIX={100 * roc_auc_score(correct, [-s for s in fix]):.2f}  "
      f"UMAS={100 * roc_auc_score(correct, [-s for s in umas]):.2f}")
