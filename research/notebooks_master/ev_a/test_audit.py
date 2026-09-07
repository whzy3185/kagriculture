import unittest
import numpy as np
import pandas as pd
from audit_core import check_contract, duplicate_audit, numeric_shift, categorical_shift


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.train = pd.DataFrame({"id": [0, 1, 2, 3], "x": [1, 1, 2, 3],
                                   "cat": ["a", "a", "b", "c"], "Will_Buy_EV": ["No", "Yes", "No", "Yes"]})
        self.test = pd.DataFrame({"id": [4, 5], "x": [1, 4], "cat": ["a", "d"]})
        self.sample = pd.DataFrame({"id": [4, 5], "Will_Buy_EV": [.5, .5]})

    def test_contract(self):
        self.assertEqual(check_contract(self.train, self.test, self.sample), ["x", "cat"])

    def test_sample_order(self):
        with self.assertRaises(ValueError):
            check_contract(self.train, self.test, self.sample.iloc[::-1])

    def test_target_leak(self):
        with self.assertRaises(ValueError):
            check_contract(self.train, self.test.assign(Will_Buy_EV="Yes"), self.sample)

    def test_unknown_label(self):
        with self.assertRaises(ValueError):
            check_contract(self.train.assign(Will_Buy_EV="Maybe"), self.test, self.sample)

    def test_conflicts_and_overlap(self):
        out = duplicate_audit(self.train, self.test, ["x", "cat"])
        self.assertEqual(out["train_extra_duplicate_feature_rows"], 1)
        self.assertEqual(out["train_feature_groups_with_conflicting_labels"], 1)
        self.assertEqual(out["test_rows_matching_any_train_feature_tuple"], 1)

    def test_identifier_negative_control(self):
        out = numeric_shift(self.train, self.test, ["id"])
        self.assertEqual(out.loc["id", "ks_distance"], 1.0)

    def test_constant_and_nonfinite(self):
        a, b = pd.DataFrame({"x": [1., 1., np.nan]}), pd.DataFrame({"x": [1., np.inf]})
        out = numeric_shift(a, b, ["x"])
        self.assertEqual(out.loc["x", "ks_distance"], 0)
        self.assertEqual(out.loc["x", "test_nonfinite_rate"], .5)
        empty = numeric_shift(pd.DataFrame({"x": [np.nan]}), b, ["x"])
        self.assertTrue(np.isnan(empty.loc["x", "ks_distance"]))

    def test_unseen_category_and_missing_sentinel(self):
        a = pd.DataFrame({"c": ["__AUDIT_MISSING__", None]})
        b = pd.DataFrame({"c": ["__AUDIT_MISSING__", "new"]})
        out = categorical_shift(a, b, ["c"])
        self.assertEqual(out.loc["c", "total_variation"], .5)
        self.assertEqual(out.loc["c", "test_unseen_category_rate"], .5)


if __name__ == "__main__":
    unittest.main()
