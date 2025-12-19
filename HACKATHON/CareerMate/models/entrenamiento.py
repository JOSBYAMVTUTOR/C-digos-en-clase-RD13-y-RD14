from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

FEATURE_COLUMNS = [
    "Database Fundamentals",
    "Computer Architecture",
    "Distributed Computing Systems",
    "Cyber Security",
    "Networking",
    "Software Development",
    "Programming Skills",
    "Project Management",
    "Computer Forensics Fundamentals",
    "Technical Communication",
    "AI ML",
    "Software Engineering",
    "Business Analysis",
    "Communication skills",
    "Data Science",
    "Troubleshooting skills",
    "Graphics Designing",
    "Openness",
    "Conscientousness",
    "Extraversion",
    "Agreeableness",
    "Emotional_Range",
    "Conversation",
    "Openness to Change",
    "Hedonism",
    "Self-enhancement",
    "Self-transcendence",
]

TARGET_COLUMN = "Role"
_ALT_TARGET_COLUMNS = ("Role", "career")
_BOUNDS_CACHE: dict[str, tuple[float, float]] | None = None


def _get_base_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def _resolve_target_column(df: pd.DataFrame) -> str:
    for c in _ALT_TARGET_COLUMNS:
        if c in df.columns:
            return c
    raise ValueError(f"No se encontró columna objetivo. Se esperaba una de: {_ALT_TARGET_COLUMNS}")


def cargar_datos(csv_path: str | os.PathLike | None = None) -> pd.DataFrame:
    base_dir = _get_base_dir()
    if csv_path is None:
        csv_path = base_dir / "CareerMap.csv"

    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"No se encontró el dataset CSV en: {csv_path}")

    df = pd.read_csv(csv_path)

    target_in_df = _resolve_target_column(df)
    if target_in_df != TARGET_COLUMN:
        df = df.rename(columns={target_in_df: TARGET_COLUMN})

    missing_cols = [c for c in FEATURE_COLUMNS + [TARGET_COLUMN] if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Faltan columnas en el CSV: {missing_cols}")

    return df


def obtener_limites_features(csv_path: str | os.PathLike | None = None) -> dict[str, tuple[float, float]]:
    global _BOUNDS_CACHE
    if _BOUNDS_CACHE is not None and csv_path is None:
        return _BOUNDS_CACHE

    df = cargar_datos(csv_path)
    bounds: dict[str, tuple[float, float]] = {}
    for c in FEATURE_COLUMNS:
        s = df[c]
        bounds[c] = (float(s.min()), float(s.max()))

    if csv_path is None:
        _BOUNDS_CACHE = bounds
    return bounds
