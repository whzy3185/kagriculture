import unittest
import numpy as np
import pandas as pd
from experiment_core import split_indices, safe_auc, pipeline_for, split_fingerprint, paired_auc_bootstrap


class ExperimentsTests(unittest.TestCase):
    def setUp(self):
        self.frame = pd.DataFrame({"id": np.arange(100), "x": np.arange(100) % 9,
            "c": ["a", "b"] * 50, "Will_Buy_EV": ["No", "Yes"] * 50})

    def test_all_split_modes_are_disjoint_and_complete(self):
        for mode in ("stratified", "shuffled", "id_tail", "id_head"):
            tr, va = split_indices(self.frame, mode)
            self.assertEqual((len(tr), len(va)), (80, 20))
            self.assertEqual(len(set(tr) & set(va)), 0)
            self.assertEqual(len(set(tr) | set(va)), 100)

    def test_order_stress_is_not_random(self):
        tr, va = split_indices(self.frame, "id_tail")
        self.assertLess(self.frame.iloc[tr].id.max(), self.frame.iloc[va].id.min())
        tr, va = split_indices(self.frame, "id_head")
        self.assertGreater(self.frame.iloc[tr].id.min(), self.frame.iloc[va].id.max())

    def test_split_fingerprints_are_reproducible(self):
        a, b = split_indices(self.frame, "stratified", seed=17)
        c, d = split_indices(self.frame, "stratified", seed=17)
        self.assertEqual(split_fingerprint(self.frame, a, b), split_fingerprint(self.frame, c, d))

    def test_undefined_subgroup_auc(self):
        self.assertTrue(np.isnan(safe_auc(np.zeros(3), [.1, .2, .3])))

    def test_preprocessing_uses_training_only(self):
        x = self.frame[["x", "c"]]
        m = pipeline_for(x, "linear")
        m.fit(x, np.arange(100) % 2)
        encoded = m.named_steps["prepare"].named_transformers_["categorical"].named_steps["encode"]
        self.assertNotIn("unseen", encoded.categories_[0])
        self.assertTrue(np.isfinite(m.predict_proba(pd.DataFrame({"x": [500], "c": ["unseen"]}))).all())
        scale = m.named_steps["prepare"].named_transformers_["numeric"].named_steps["scale"]
        self.assertAlmostEqual(scale.mean_[0], x.x.mean())

    def test_bootstrap_identical_predictions(self):
        y = np.array([0, 1] * 20)
        p = np.linspace(.1, .9, 40)
        np.testing.assert_array_equal(paired_auc_bootstrap(y, p, p, rounds=20), np.zeros(20))

    def test_bootstrap_known_ordering(self):
        y = np.array([0, 1] * 20)
        np.testing.assert_array_equal(paired_auc_bootstrap(y, y.astype(float), 1-y.astype(float), rounds=20), np.ones(20))

    def test_bootstrap_rejects_one_class(self):
        with self.assertRaises(ValueError):
            paired_auc_bootstrap(np.zeros(5), np.zeros(5), np.zeros(5), rounds=20)


if __name__ == "__main__":
    unittest.main()
