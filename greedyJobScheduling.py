import numpy as np

def greedyDiff(l, w):
    assert len(l) == len(w), f"list of job lengths and job weights do not have the same number: {len(l)} and {len(w)}"
    n = len(l)
    diffs = [l[i]-w[i] for i in range(n)]
    schedule = np.argsort(diffs)
    return schedule
  
def greedyRatio(l,w):
    assert len(l) == len(w), f"list of job lengths and job weights do not have the same number: {len(l)} and {len(w)}"
    for i in range(len(w))
        assert w[i] != 0, f"w[{i}] is 0"
    n = len(l)
    ratios = [l[i]/w[i] for i in range(n)]
    schedule = np.argsort(diffs)
    return schedule
    
 greedyRatio(
