"""Little's (1988) mean-pattern MCAR statistic with Gaussian ML estimates.

Original NumPy/SciPy implementation of the Gaussian EM sufficient-statistic
updates and Little's pattern-weighted quadratic form (not pairwise covariance).
Algorithm references:
  Little (1988), doi:10.1080/01621459.1988.10478722.
  naniar::mcar_test, https://naniar.njtierney.com/reference/mcar_test.html
  https://github.com/njtierney/naniar/blob/master/R/mcar-test.R

The reference implementation also estimates mean/covariance by ML before the
pattern statistic. This code is independently written, not a translation of R.
It returns parameters/diagnostics, never a completed or transformed dataset.
Numerical success does not establish normality, independence, or global MCAR.
"""

import numpy as np
from scipy import stats


def little_mcar(values, *, tol=1e-8, max_iter=2000):
    """Return ML/EM mean-pattern test and diagnostics; raise on invalid scope.

    Rows are observational units; columns must be appropriate numerical variables.
    NaN means missing. Infinities, unobserved/constant columns, unidentifiable
    covariance, insufficient df and nonconvergence are errors, not p-values.
    No ridge regularization, pseudoinverse or silent row/column deletion is used.
    """
    x = np.array(values, dtype=float, copy=True)
    if x.ndim != 2 or min(x.shape) < 2:
        raise ValueError("Need at least two rows and two numerical variables")
    if np.isinf(x).any():
        raise ValueError("Infinite observed values")
    if tol <= 0 or max_iter < 1:
        raise ValueError("Invalid convergence settings")
    n, p = x.shape
    observed = ~np.isnan(x)
    if (observed.sum(axis=0) < 2).any():
        raise ValueError("Each variable needs at least two observed values")
    if (~observed.any(axis=1)).any():
        raise ValueError("Entirely missing rows: choose and disclose scope; no silent deletion")
    if (np.nanvar(x, axis=0) <= 0).any():
        raise ValueError("Zero observed variance")
    if not np.all(observed.astype(int).T @ observed.astype(int) >= 2):
        raise ValueError("Covariance not identifiable: insufficient joint observations")
    complete_rows = x[observed.all(axis=1)]
    if len(complete_rows) >= p + 1 and np.linalg.matrix_rank(
        complete_rows - complete_rows.mean(axis=0)
    ) < p:
        raise ValueError("Rank-deficient complete-pattern support; Gaussian ML covariance can be singular")

    masks, pattern_id = np.unique(observed, axis=0, return_inverse=True)
    groups = [(mask, x[pattern_id == j]) for j, mask in enumerate(masks)]
    degrees_of_freedom = int(sum(mask.sum() for mask in masks) - p)
    if degrees_of_freedom <= 0:
        raise ValueError("No positive test degrees of freedom")

    # Deterministic start. EM estimates the full observed-data likelihood;
    # initial marginal moments are not used as the final test covariance.
    mean = np.nanmean(x, axis=0)
    covariance = np.diag(np.nanvar(x, axis=0))
    ll_history = []

    def observed_loglik(mu, cov):
        ll = 0.0
        for mask, rows in groups:
            observed_rows = rows[:, mask]
            subcov = cov[np.ix_(mask, mask)]
            np.linalg.cholesky(subcov)
            difference = observed_rows - mu[mask]
            quadratic = np.sum(difference * np.linalg.solve(subcov, difference.T).T)
            ll -= 0.5 * (len(rows) * (mask.sum() * np.log(2 * np.pi)
                                     + np.linalg.slogdet(subcov)[1]) + quadratic)
        return float(ll)

    ll_history.append(observed_loglik(mean, covariance))
    for iteration in range(1, max_iter + 1):
        expected_sum = np.zeros(p)
        expected_crossproducts = np.zeros((p, p))
        for mask, rows in groups:
            obs, mis = np.flatnonzero(mask), np.flatnonzero(~mask)
            expectation = np.zeros((len(rows), p))
            expectation[:, obs] = rows[:, obs]
            conditional_covariance = np.zeros((p, p))
            if len(mis):
                sigma_oo = covariance[np.ix_(obs, obs)]
                beta = np.linalg.solve(sigma_oo, covariance[np.ix_(obs, mis)]).T
                expectation[:, mis] = mean[mis] + (rows[:, obs] - mean[obs]) @ beta.T
                conditional_covariance[np.ix_(mis, mis)] = (
                    covariance[np.ix_(mis, mis)] - beta @ covariance[np.ix_(obs, mis)]
                )
            expected_sum += expectation.sum(axis=0)
            expected_crossproducts += (expectation.T @ expectation
                                       + len(rows) * conditional_covariance)
        new_mean = expected_sum / n
        new_covariance = expected_crossproducts / n - np.outer(new_mean, new_mean)
        new_covariance = (new_covariance + new_covariance.T) / 2
        np.linalg.cholesky(new_covariance)  # Fail rather than patch singular covariance.
        if np.linalg.cond(new_covariance) > 1e12:
            raise ValueError("Ill-conditioned covariance (>1e12); no regularization applied")
        loglik = observed_loglik(new_mean, new_covariance)
        if loglik < ll_history[-1] - 1e-7 * (1 + abs(ll_history[-1])):
            raise ArithmeticError("EM observed likelihood decreased")
        mean_change = np.max(np.abs(new_mean - mean) / (1 + np.abs(mean)))
        cov_change = np.max(np.abs(new_covariance - covariance)) / (1 + np.max(np.abs(covariance)))
        mean, covariance = new_mean, new_covariance
        ll_history.append(loglik)
        likelihood_change = abs(ll_history[-1] - ll_history[-2]) / (1 + abs(ll_history[-2]))
        if max(mean_change, cov_change, likelihood_change) < tol:
            break
    else:
        raise RuntimeError(f"Gaussian EM did not converge in {max_iter} iterations")

    statistic = 0.0
    pattern_details = []
    for mask, rows in groups:
        difference = rows[:, mask].mean(axis=0) - mean[mask]
        subcov = covariance[np.ix_(mask, mask)]
        contribution = float(len(rows) * difference @ np.linalg.solve(subcov, difference))
        statistic += contribution
        pattern_details.append({"observed_mask": mask.tolist(), "n_rows": len(rows),
                                "observed_dimensions": int(mask.sum()), "contribution": contribution})
    if not np.isfinite(statistic) or statistic < 0:
        raise ArithmeticError("Invalid Little statistic")
    p_value = float(stats.chi2.sf(statistic, degrees_of_freedom))
    if not np.isfinite(p_value):
        raise ArithmeticError("Invalid chi-square reference probability")
    return {"statistic": statistic, "degrees_of_freedom": degrees_of_freedom,
            "p_value": p_value, "missing_patterns": len(groups), "n_rows": n,
            "iterations": iteration, "converged": True, "mean_ml": mean,
            "covariance_ml": covariance, "covariance_condition": float(np.linalg.cond(covariance)),
            "loglik_history": np.array(ll_history), "pattern_details": pattern_details}
