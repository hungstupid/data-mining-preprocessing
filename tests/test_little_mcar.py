"""Numerical/algorithmic checks; no claimed recovery of a real missingness mechanism."""

import unittest

import numpy as np

from src.little_mcar import little_mcar


class LittleMcarTests(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(42)
        self.x = rng.multivariate_normal([2, 4], [[2, .7], [.7, 3]], size=600)
        self.x[::3, 1] = np.nan

    def test_matches_closed_form_one_incomplete_variable(self):
        # With X fully observed and Y partially observed, Gaussian ML has an
        # analytic regression solution. Little's quadratic reduces to this sum.
        result = little_mcar(self.x, tol=1e-10)
        a = self.x[:, 0]
        complete = ~np.isnan(self.x[:, 1])
        expected = sum(mask.sum() * (a[mask].mean() - a.mean())**2 / a.var(ddof=0)
                       for mask in [complete, ~complete])
        self.assertAlmostEqual(result['statistic'], expected, places=7)
        self.assertEqual(result['degrees_of_freedom'], 1)
        self.assertTrue(np.all(np.diff(result['loglik_history']) >= -1e-7))

    def test_row_order_and_affine_unit_invariance(self):
        original = self.x.copy()
        first = little_mcar(self.x, tol=1e-10)
        transformed = self.x[::-1] * [3, 7] + [5, -2]
        second = little_mcar(transformed, tol=1e-10)
        self.assertAlmostEqual(first['statistic'], second['statistic'], places=6)
        np.testing.assert_equal(self.x, original)

    def test_general_patterns_and_positive_covariance(self):
        rng = np.random.default_rng(19)
        x = rng.normal(size=(500, 3))
        x[:60, 0] = np.nan
        x[60:120, 1] = np.nan
        x[120:180, 2] = np.nan
        result = little_mcar(x)
        self.assertEqual(result['missing_patterns'], 4)
        self.assertEqual(result['degrees_of_freedom'], 6)
        self.assertGreater(np.linalg.eigvalsh(result['covariance_ml']).min(), 0)
        self.assertTrue(0 <= result['p_value'] <= 1)

    def test_invalid_inputs_do_not_return_p_values(self):
        for x in [np.ones((10, 2)), np.full((10, 2), np.nan),
                  np.array([[1, 2], [2, np.inf], [3, np.nan]]),
                  np.arange(20).reshape(10, 2)]:
            with self.subTest(x=x):
                with self.assertRaises((ValueError, np.linalg.LinAlgError)):
                    little_mcar(x)
        with self.assertRaises(RuntimeError):
            little_mcar(self.x, max_iter=1, tol=1e-14)

    def test_singular_complete_support_is_blocked(self):
        x = np.column_stack([np.arange(30, dtype=float), 2 * np.arange(30, dtype=float)])
        x[::4, 1] = np.nan
        with self.assertRaisesRegex(ValueError, "Rank-deficient"):
            little_mcar(x)


if __name__ == '__main__':
    unittest.main()
