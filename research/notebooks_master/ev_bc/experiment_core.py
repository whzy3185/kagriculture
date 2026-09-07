"""Original train-only experimental helpers for EV-B and EV-C."""
import hashlib
import time
import warnings
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from threadpoolctl import threadpool_limits

TARGET, ID = "Will_Buy_EV", "id"
SAMPLE_SEED = 20260907
SAMPLE_SIZE = 120000
SEEDS = [17, 43, 91]


def load_sample(path, n=SAMPLE_SIZE, seed=SAMPLE_SEED):
    data = pd.read_csv(path)
    if TARGET not in data or ID not in data or not data[ID].is_unique:
        raise ValueError("Expected unique IDs and a training target")
    if data[TARGET].isna().any() or set(data[TARGET].unique()) != {"Yes", "No"}:
        raise ValueError("Expected Yes/No labels")
    if n < 10 or n > len(data):
        raise ValueError("Sample size must be between 10 and dataset size")
    indices = np.arange(len(data))
    if n < len(data):
        indices, _ = train_test_split(indices, train_size=n, random_state=seed, stratify=data[TARGET])
    sample = data.iloc[indices].sort_values(ID).reset_index(drop=True)
    return sample, len(data)


def split_indices(frame, mode, seed=17, fraction=.2):
    idx = np.arange(len(frame))
    if mode in {"stratified", "shuffled"}:
        tr, va = train_test_split(idx, test_size=fraction, random_state=seed,
                                 stratify=frame[TARGET] if mode == "stratified" else None)
    elif mode in {"id_tail", "id_head"}:
        order = np.argsort(frame[ID].to_numpy(), kind="stable")
        count = int(np.ceil(len(frame) * fraction))
        if mode == "id_tail":
            tr, va = order[:-count], order[-count:]
        else:
            tr, va = order[count:], order[:count]
    else:
        raise ValueError("Unknown validation mode")
    assert len(tr) and len(va) and not np.intersect1d(tr, va).size
    assert len(np.union1d(tr, va)) == len(frame)
    return tr, va


def safe_auc(y, p):
    return float(roc_auc_score(y, p)) if len(np.unique(y)) == 2 else np.nan


def pipeline_for(frame, kind):
    numeric = frame.select_dtypes(include="number").columns.tolist()
    categories = [c for c in frame if c not in numeric]
    numeric_steps = [("impute", SimpleImputer(strategy="median"))]
    if kind == "linear":
        numeric_steps.append(("scale", StandardScaler()))
    prepare = ColumnTransformer([
        ("numeric", Pipeline(numeric_steps), numeric),
        ("categorical", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
            ("encode", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), categories),
    ])
    if kind == "prior":
        model = DummyClassifier(strategy="prior")
    elif kind == "linear":
        model = LogisticRegression(C=1.0, solver="lbfgs", max_iter=500, tol=1e-4)
    elif kind == "tree":
        model = HistGradientBoostingClassifier(max_iter=120, learning_rate=.08,
            max_leaf_nodes=31, min_samples_leaf=40, l2_regularization=1.,
            early_stopping=False, random_state=17)
    else:
        raise ValueError("Unknown model kind")
    return Pipeline([("prepare", prepare), ("model", model)])


def fit_score(sample, tr, va, kind):
    features = [c for c in sample if c not in (TARGET, ID)]
    xtr, xva = sample.iloc[tr][features], sample.iloc[va][features]
    ytr = sample.iloc[tr][TARGET].map({"No": 0, "Yes": 1}).to_numpy()
    yva = sample.iloc[va][TARGET].map({"No": 0, "Yes": 1}).to_numpy()
    if len(np.unique(ytr)) != 2 or len(np.unique(yva)) != 2:
        raise ValueError("Overall training and validation splits must contain both classes")
    model = pipeline_for(xtr, kind)
    with threadpool_limits(limits=2), warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        start = time.perf_counter()
        model.fit(xtr, ytr)
        fit_seconds = time.perf_counter() - start
        start = time.perf_counter()
        predictions = model.predict_proba(xva)[:, list(model.classes_).index(1)]
        predict_seconds = time.perf_counter() - start
    return model, predictions, yva, {
        "train_rows": len(tr), "validation_rows": len(va),
        "train_positive_rate": float(ytr.mean()), "validation_positive_rate": float(yva.mean()),
        "roc_auc": safe_auc(yva, predictions),
        "average_precision": float(average_precision_score(yva, predictions)),
        "log_loss": float(log_loss(yva, predictions, labels=[0, 1])),
        "brier_score": float(brier_score_loss(yva, predictions)),
        "fit_seconds": fit_seconds, "predict_seconds": predict_seconds,
        "convergence_warnings": sum(issubclass(w.category, ConvergenceWarning) for w in caught),
        "other_warnings": sum(not issubclass(w.category, ConvergenceWarning) for w in caught),
    }


def split_fingerprint(sample, tr, va):
    def digest(idx):
        ids = np.sort(sample.iloc[idx][ID].to_numpy()).astype("<i8")
        return hashlib.sha256(ids.tobytes()).hexdigest()
    return {"training_id_sha256": digest(tr), "validation_id_sha256": digest(va)}


def paired_auc_bootstrap(y, candidate, reference, rounds=500, seed=2026):
    y = np.asarray(y)
    positive, negative = np.flatnonzero(y == 1), np.flatnonzero(y == 0)
    if not len(positive) or not len(negative) or rounds < 20:
        raise ValueError("Both labels and at least 20 bootstrap rounds are required")
    rng = np.random.default_rng(seed)
    differences = []
    for _ in range(rounds):
        idx = np.concatenate([rng.choice(positive, len(positive), replace=True),
                              rng.choice(negative, len(negative), replace=True)])
        differences.append(roc_auc_score(y[idx], candidate[idx]) - roc_auc_score(y[idx], reference[idx]))
    return np.asarray(differences)
