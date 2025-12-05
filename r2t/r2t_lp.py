from ortools.linear_solver import pywraplp
import numpy as np

def truncated_sum_lp(contribs, tau):
    solver = pywraplp.Solver.CreateSolver("GLOP")
    x = [solver.NumVar(0.0, min(c, tau), f"x_{i}") for i, c in enumerate(contribs)]
    objective = solver.Objective()
    for xi in x:
        objective.SetCoefficient(xi, 1.0)
    objective.SetMaximization()
    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        return 0.0
    return sum(xi.solution_value() for xi in x)

def r2t_estimate(contribs, epsilon, tau_values, rng, verbose=False):
    estimates = []
    iterator = tau_values
    if verbose:
        try:
            from tqdm import tqdm
            iterator = tqdm(tau_values, desc="Solving LP over tau-grid")
        except Exception:
            iterator = tau_values
    for tau in iterator:
        tsum = truncated_sum_lp(contribs, tau)
        noise = rng.laplace(0.0, tau / epsilon)
        estimates.append(tsum + noise)
    return max(estimates), estimates

def tau_grid_from_contribs(contribs, k):
    pos = np.array([c for c in contribs if c > 0])
    if len(pos) == 0:
        return list(np.geomspace(1e-3, 1e2, num=k))
    lo = float(np.percentile(pos, 50))
    hi = float(np.percentile(pos, 95))
    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= 0 or lo <= 0:
        return list(np.geomspace(1e-3, 1e2, num=k))
    if hi <= lo:
        hi = lo * 2.0
    grid = np.geomspace(max(lo, 1e-6), max(hi, 1e-6) * 2.0, num=k)
    return list(grid)
