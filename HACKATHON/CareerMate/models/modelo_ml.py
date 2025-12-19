from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import numpy as np
from joblib import dump, load
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV

from models.entrenamiento import FEATURE_COLUMNS, TARGET_COLUMN, cargar_datos
from models.buffer import load_buffer, clear_buffer


@dataclass(frozen=True)
class ModelArtifacts:
    scaler: StandardScaler
    classifier: CalibratedClassifierCV
    classes_: np.ndarray


def _artifact_dir() -> Path:
    return Path(__file__).resolve().parent / "artifacts"


def _paths() -> dict[str, Path]:
    d = _artifact_dir()
    return {
        "dir": d,
        "scaler": d / "career_scaler.joblib",
        "model": d / "career_model.joblib",
        "meta": d / "career_meta.json",
    }


def _load_meta() -> dict:
    p = _paths()["meta"]
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _save_meta(meta: dict) -> None:
    p = _paths()["meta"]
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


def artifacts_exist() -> bool:
    ps = _paths()
    return ps["scaler"].exists() and ps["model"].exists() and ps["meta"].exists()


# =========================
# TRAINING
# =========================

def train_and_save(csv_path: str | None = None) -> ModelArtifacts:
    df = cargar_datos(csv_path)

    X = df[FEATURE_COLUMNS].to_numpy(dtype=float)
    y = df[TARGET_COLUMN].astype(str).to_numpy()

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    base_clf = SGDClassifier(
        loss="log_loss",
        penalty="l2",
        alpha=5e-5,
        max_iter=5000,
        tol=1e-4,
        random_state=42,
    )

    clf = CalibratedClassifierCV(base_clf, method="sigmoid", cv=3)
    clf.fit(Xs, y)

    ps = _paths()
    ps["dir"].mkdir(parents=True, exist_ok=True)
    dump(scaler, ps["scaler"])
    dump(clf, ps["model"])

    _save_meta(
        {
            "trained_at": datetime.utcnow().isoformat() + "Z",
            "n_samples": int(X.shape[0]),
            "feature_columns": list(FEATURE_COLUMNS),
            "target_column": TARGET_COLUMN,
            "classes": clf.classes_.tolist(),
            "calibrated": True,
        }
    )

    return ModelArtifacts(scaler=scaler, classifier=clf, classes_=clf.classes_)


def load_or_train(csv_path: str | None = None) -> ModelArtifacts:
    if not artifacts_exist():
        return train_and_save(csv_path)

    meta = _load_meta()
    if not meta.get("calibrated", False):
        return train_and_save(csv_path)

    ps = _paths()
    scaler: StandardScaler = load(ps["scaler"])
    clf: CalibratedClassifierCV = load(ps["model"])
    classes_ = np.array(meta.get("classes", []), dtype=str)

    return ModelArtifacts(scaler=scaler, classifier=clf, classes_=classes_)


# =========================
# PREDICTION
# =========================

def predict_top(X: np.ndarray, top: int = 3, carreras_permitidas: List[str] | None = None) -> List[Tuple[str, float]]:
    """
    Predice las top N carreras más probables.
    
    Args:
        X: Vector de features (1, n_features)
        top: Número de recomendaciones
        carreras_permitidas: Lista opcional de carreras a considerar
    
    Returns:
        Lista de tuplas (carrera, probabilidad)
    """
    art = load_or_train()

    Xs = art.scaler.transform(X)
    proba = art.classifier.predict_proba(Xs)[0]
    labels = art.classifier.classes_.astype(str)

    # Aplicar filtro de carreras antes de cualquier ranking
    if carreras_permitidas is not None:
        mask = np.isin(labels, np.array(carreras_permitidas, dtype=str))
        labels = labels[mask]
        proba = proba[mask]

    pairs = [(labels[i], float(proba[i])) for i in range(len(labels))]

    # Si hay filtro, no apliques umbral para no vaciar resultados; de lo contrario usa 0.05
    if carreras_permitidas is None:
        pairs = [(c, p) for c, p in pairs if p >= 0.05]

    pairs.sort(key=lambda x: x[1], reverse=True)

    if len(pairs) >= 2:
        p1, p2 = pairs[0][1], pairs[1][1]
        if abs(p1 - p2) < 0.25:
            total = p1 + p2
            if total > 0:
                return [
                    (pairs[0][0], p1 / total),
                    (pairs[1][0], p2 / total),
                ]

    return pairs[:top]


# =========================
# BUFFER RETRAINING
# =========================

def retrain_from_buffer() -> bool:
    buffer_data = load_buffer()
    if not buffer_data:
        return False

    df = cargar_datos()
    X_base = df[FEATURE_COLUMNS].to_numpy(dtype=float)
    y_base = df[TARGET_COLUMN].astype(str).to_numpy()

    X_extra, y_extra = [], []

    for item in buffer_data:
        for label in item["labels"]:
            X_extra.append(item["features"])
            y_extra.append(label)

    if not X_extra:
        return False

    X = np.vstack([X_base, np.array(X_extra)])
    y = np.concatenate([y_base, np.array(y_extra)])

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    base_clf = SGDClassifier(
        loss="log_loss",
        alpha=5e-5,
        max_iter=5000,
        random_state=42,
    )

    clf = CalibratedClassifierCV(base_clf, method="sigmoid", cv=3)
    clf.fit(Xs, y)

    ps = _paths()
    dump(scaler, ps["scaler"])
    dump(clf, ps["model"])

    clear_buffer()
    return True
