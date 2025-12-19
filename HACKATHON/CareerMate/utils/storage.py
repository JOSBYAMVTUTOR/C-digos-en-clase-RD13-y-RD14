import json
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

HISTORIAL_FILE = "historial.json"
ESTADISTICAS_FILE = "estadisticas.json"
MUESTRAS_FILE = "muestras_entrenamiento.jsonl"


def guardar_historial(historial: Any) -> bool:
    try:
        Path(HISTORIAL_FILE).write_text(
            json.dumps(historial, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return True
    except Exception:
        return False


def cargar_historial() -> list[dict]:
    try:
        p = Path(HISTORIAL_FILE)
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        pass
    return []


def agregar_al_historial(
    historial: list[dict],
    carreras: list[str],
    compatibilidades: list[int],
    features: list[float] | None = None,
) -> list[dict]:
    nuevo_test = {
        "fecha": datetime.now().isoformat(),
        "carreras": carreras,
        "compatibilidades": compatibilidades,
        "features": features,
    }
    historial.append(nuevo_test)
    guardar_historial(historial)
    return historial


def agregar_muestra_entrenamiento(features: Sequence[float], label: str, fuente: str = "auto") -> bool:
    try:
        row = {
            "ts": datetime.now().isoformat(),
            "label": str(label),
            "fuente": str(fuente),
            "features": [float(x) for x in features],
        }
        p = Path(MUESTRAS_FILE)
        if not p.exists():
            p.touch()
        with p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        return True
    except Exception:
        return False


def limpiar_historial():
    guardar_historial([])
    return []


def guardar_estadisticas(estadisticas: Any) -> bool:
    try:
        Path(ESTADISTICAS_FILE).write_text(
            json.dumps(estadisticas, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return True
    except Exception:
        return False


def cargar_estadisticas() -> dict:
    try:
        p = Path(ESTADISTICAS_FILE)
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}
