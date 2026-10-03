import numpy as np


def score_trajectory(nodes):
    calibrated, umas, fix = {}, [], []
    for node in sorted(nodes, key=lambda n: n['round']):
        u = 1.0 - np.sum(node['logprobs'])
        if not node['parents']:
            calibrated[node['id']] = u
            continue
        own = [n for n in nodes if n['agent'] == node['agent'] and n['round'] < node['round']]
        if own:
            a = calibrated[max(own, key=lambda n: n['round'])['id']]
        else:
            a = np.mean([calibrated[p] for p in node['parents']])
        w = np.mean([1 / (1 + np.exp(-(calibrated[p] - a) / a)) for p in node['parents']])
        calibrated[node['id']] = (1 - w) * u + w * a
        umas.append(calibrated[node['id']])
        fix.append(u)
    return np.mean(umas), np.mean(fix)
