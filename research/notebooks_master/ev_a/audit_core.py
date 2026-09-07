"""Original aggregate-only audit helpers for S6E9. No network or data export."""

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp


def check_contract(train, test, sample, target="Will_Buy_EV", identifier="id"):
    if any(df.empty for df in (train, test, sample)):
        raise ValueError("Inputs must not be empty")
    if any(not df.columns.is_unique for df in (train, test, sample)):
        raise ValueError("Duplicate column names")
    if target not in train or target in test:
        raise ValueError("Target must occur only in the training input")
    features = [c for c in train if c not in (target, identifier)]
    if not features or set(test.columns) != set(features + [identifier]):
        raise ValueError("Training and test feature schemas differ")
    for df in (train, test, sample):
        if identifier not in df or df[identifier].isna().any() or not df[identifier].is_unique:
            raise ValueError("IDs must be present, non-null and unique")
    if len(sample) != len(test) or not np.array_equal(sample[identifier], test[identifier]):
        raise ValueError("Sample IDs must match test IDs in row order")
    if set(sample.columns) != {identifier, target}:
        raise ValueError("Unexpected sample submission schema")
    if train[identifier].isin(test[identifier]).any():
        raise ValueError("Train/test IDs overlap")
    if train[target].isna().any() or set(train[target].unique()) != {"No", "Yes"}:
        raise ValueError("Expected non-null Yes/No labels; inspect a changed data version")
    return features


def duplicate_audit(train, test, features, target="Will_Buy_EV"):
    # MultiIndex compares full tuples, without relying on a row-hash collision assumption.
    train_key = pd.MultiIndex.from_frame(train[features])
    test_key = pd.MultiIndex.from_frame(test[features])
    duplicated = train.duplicated(features, keep=False)
    conflicts = 0
    if duplicated.any():
        counts = train.loc[duplicated].groupby(features, dropna=False)[target].nunique()
        conflicts = int((counts > 1).sum())
    return {
        "train_extra_duplicate_feature_rows": int(train_key.duplicated().sum()),
        "test_extra_duplicate_feature_rows": int(test_key.duplicated().sum()),
        "test_rows_matching_any_train_feature_tuple": int(test_key.isin(train_key).sum()),
        "train_feature_groups_with_conflicting_labels": conflicts,
    }


def numeric_shift(train, test, columns):
    rows = []
    for col in columns:
        a = train[col].to_numpy(dtype=float, na_value=np.nan)
        b = test[col].to_numpy(dtype=float, na_value=np.nan)
        x, y = a[np.isfinite(a)], b[np.isfinite(b)]
        stat = float(ks_2samp(x, y, method="asymp").statistic) if len(x) and len(y) else np.nan
        outside = float(((y < x.min()) | (y > x.max())).mean()) if len(x) and len(y) else np.nan
        rows.append({"feature": col, "ks_distance": stat,
                     "train_nonfinite_rate": float(1 - len(x) / len(a)),
                     "test_nonfinite_rate": float(1 - len(y) / len(b)),
                     "test_outside_train_range_rate": outside})
    return pd.DataFrame(rows).set_index("feature")


def categorical_shift(train, test, columns):
    rows = []
    for col in columns:
        a, b = train[col].astype("string"), test[col].astype("string")
        missing = "__AUDIT_MISSING__"
        while a.eq(missing).any() or b.eq(missing).any():
            missing += "_"
        a, b = a.fillna(missing), b.fillna(missing)
        p, q = a.value_counts(normalize=True), b.value_counts(normalize=True)
        support = p.index.union(q.index)
        tv = float((p.reindex(support, fill_value=0) - q.reindex(support, fill_value=0)).abs().sum() / 2)
        rows.append({"feature": col, "total_variation": tv,
                     "test_unseen_category_rate": float((~b.isin(p.index)).mean()),
                     "train_levels_including_missing": len(p),
                     "test_levels_including_missing": len(q)})
    return pd.DataFrame(rows).set_index("feature")
