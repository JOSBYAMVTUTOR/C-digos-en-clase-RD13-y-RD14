from __future__ import annotations

"""Script standalone: vectores sintéticos + predicción top-3.

Requisitos:
- Construye 3 perfiles (Data Science, Cyber Security, híbrido 50/50)
- Llama predict_top(top=3)
- Imprime resultados legibles
- Calcula std(vector_usuario) y marca WARNING si std < 0.4 o std > 1.2

Ejecución (desde la raíz del repo):
	python tests/test_vectores_sinteticos.py
"""

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np


# Permite ejecutar el script desde cualquier CWD sin requerir instalación del paquete.
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
	sys.path.insert(0, str(_ROOT))


from models.entrenamiento import FEATURE_COLUMNS, obtener_limites_features  # noqa: E402
from models.modelo_ml import predict_top  # noqa: E402


@dataclass(frozen=True, slots=True)
class PerfilSintetico:
	nombre: str
	foco_a: str
	foco_b: str | None = None
	mezcla: float = 1.0  # 1.0 => 100% foco_a; 0.5 => mitad/mitad con foco_b


def _build_vector(perfil: PerfilSintetico) -> np.ndarray:
	"""Construye un vector (1, n_features) usando límites del dataset.

	Estrategia:
	- Usa el mínimo para todas las features.
	- Sube a máximo las features de foco (o mezcla entre ambas).
	Esto mantiene compatibilidad con FEATURE_COLUMNS y con el escalado del modelo.
	"""

	bounds = obtener_limites_features()
	mins = np.array([bounds[c][0] for c in FEATURE_COLUMNS], dtype=float)
	maxs = np.array([bounds[c][1] for c in FEATURE_COLUMNS], dtype=float)

	x = mins.copy()

	def set_feature(feature: str, value: float) -> None:
		idx = FEATURE_COLUMNS.index(feature)
		x[idx] = float(value)

	if perfil.foco_b is None or perfil.mezcla >= 0.999:
		set_feature(perfil.foco_a, maxs[FEATURE_COLUMNS.index(perfil.foco_a)])
	else:
		# Mezcla lineal: cada foco recibe (mezcla) y (1-mezcla) del rango min->max.
		a_min, a_max = bounds[perfil.foco_a]
		b_min, b_max = bounds[perfil.foco_b]
		set_feature(perfil.foco_a, a_min + (a_max - a_min) * float(perfil.mezcla))
		set_feature(perfil.foco_b, b_min + (b_max - b_min) * float(1.0 - perfil.mezcla))

	return x.reshape(1, -1)


def _print_resultado(perfil: PerfilSintetico, vector: np.ndarray) -> None:
	std = float(np.std(vector))
	warn = "WARNING" if (std < 0.4 or std > 1.2) else "OK"

	print("=" * 72)
	print(f"Perfil: {perfil.nombre}")
	print(f"Vector std: {std:.4f} [{warn}]")

	top3 = predict_top(vector, top=3)
	print("Top-3 carreras:")
	for i, (carrera, prob) in enumerate(top3, start=1):
		print(f"  {i}. {carrera:<35}  prob={prob:.4f}")


def main() -> int:
	perfiles = [
		PerfilSintetico(nombre="100% Data Science", foco_a="Data Science"),
		PerfilSintetico(nombre="100% Cyber Security", foco_a="Cyber Security"),
		PerfilSintetico(nombre="Híbrido 50/50 (Data Science + Cyber Security)", foco_a="Data Science", foco_b="Cyber Security", mezcla=0.5),
	]

	# Validaciones mínimas para evitar fallos silenciosos si cambia FEATURE_COLUMNS.
	for p in perfiles:
		if p.foco_a not in FEATURE_COLUMNS:
			raise ValueError(f"Feature no existe en FEATURE_COLUMNS: {p.foco_a}")
		if p.foco_b is not None and p.foco_b not in FEATURE_COLUMNS:
			raise ValueError(f"Feature no existe en FEATURE_COLUMNS: {p.foco_b}")

	for p in perfiles:
		v = _build_vector(p)
		_print_resultado(p, v)

	print("=" * 72)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())

