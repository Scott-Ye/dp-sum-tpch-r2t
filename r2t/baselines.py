import numpy as np

def naive_laplace_sum(baseline_sum: float, epsilon: float, tau_bound: float, rng):
    noise = rng.laplace(0.0, tau_bound / epsilon)
    return baseline_sum + noise

def local_sensitivity_bound(contribs):
    return float(max(contribs) if contribs else 0.0)

def smooth_like_bound(contribs, beta: float = 0.1):
    # Practical approximation: use a high percentile as a smoothed bound
    if not contribs:
        return 0.0
    arr = np.array(contribs)
    p95 = float(np.percentile(arr, 95))
    p99 = float(np.percentile(arr, 99))
    return max(p95, p99 * np.exp(-beta))

def smooth_like_laplace_sum(baseline_sum: float, epsilon: float, contribs, rng, beta: float = 0.1):
    b = smooth_like_bound(contribs, beta)
    noise = rng.laplace(0.0, b / epsilon)
    return baseline_sum + noise
