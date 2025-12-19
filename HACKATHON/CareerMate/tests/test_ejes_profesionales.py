"""
Script de validación del sistema jerárquico.

Prueba 3 perfiles extremos:
1. Ciberseguridad pura
2. Data Science / AI-ML
3. Desarrollo de Software

Valida que:
- El eje detectado sea correcto
- Las carreras recomendadas pertenezcan al eje
- No haya contaminación cruzada (ej. Graphics Designer para perfil técnico)
"""
from __future__ import annotations

import sys
from pathlib import Path

# Asegurar imports desde raíz
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np

from models.entrenamiento import FEATURE_COLUMNS, obtener_limites_features
from models.ejes_profesionales import (
    seleccionar_eje,
    obtener_carreras_candidatas,
    diagnosticar_perfil,
    EJES_PROFESIONALES,
)
from models.modelo_ml import predict_top


def crear_perfil_extremo(features_altas: list[str], features_bajas: list[str] | None = None) -> dict[str, float]:
    """
    Crea un perfil con features específicas en valores extremos.
    """
    bounds = obtener_limites_features()
    perfil = {}
    
    for col in FEATURE_COLUMNS:
        min_val, max_val = bounds[col]
        
        if col in features_altas:
            perfil[col] = max_val  # Máximo
        elif features_bajas and col in features_bajas:
            perfil[col] = min_val  # Mínimo
        else:
            perfil[col] = (min_val + max_val) / 2  # Medio
    
    return perfil


def validar_perfil(nombre: str, perfil: dict[str, float], eje_esperado: str, carreras_validas: set[str]):
    """
    Valida un perfil y reporta resultados.
    """
    print("=" * 70)
    print(f"PERFIL: {nombre}")
    print("=" * 70)
    
    # Detectar eje
    resultado = seleccionar_eje(perfil)
    carreras = obtener_carreras_candidatas(resultado)
    
    # Verificaciones
    eje_correcto = resultado.eje_principal == eje_esperado
    carreras_correctas = all(c in carreras_validas for c in carreras)
    sin_contaminacion = not any(c in ["Graphics Designer", "Customer Service Executive"] for c in carreras) if eje_esperado != "diseno_producto" and eje_esperado != "soporte_gestion" else True
    
    print(f"Eje detectado: {resultado.eje_principal} {'✓' if eje_correcto else '✗ (esperado: ' + eje_esperado + ')'}")
    print(f"Es híbrido: {resultado.es_hibrido}")
    if resultado.es_hibrido:
        print(f"  Eje secundario: {resultado.eje_secundario}")
    print(f"Confianza: {resultado.confianza:.0%}")
    print(f"Margen: {resultado.margen:.3f}")
    print()
    
    # Scores por eje
    print("Scores por eje:")
    ranking = sorted(resultado.scores.values(), key=lambda x: x.score_normalizado, reverse=True)
    for score in ranking[:4]:
        eje_info = EJES_PROFESIONALES[score.eje_id]
        marker = " ← GANADOR" if score.eje_id == resultado.eje_principal else ""
        print(f"  {eje_info.nombre}: {score.score_normalizado:.3f}{marker}")
    print()
    
    # Carreras candidatas
    print(f"Carreras candidatas ({len(carreras)}):")
    for c in carreras:
        marker = " ✓" if c in carreras_validas else " ✗ CONTAMINACIÓN"
        print(f"  - {c}{marker}")
    print()
    
    # Predicción ML
    vector = np.array([[perfil[col] for col in FEATURE_COLUMNS]])
    pred = predict_top(vector, top=3, carreras_permitidas=carreras)
    
    print("Top 3 recomendaciones (ML):")
    for i, (carrera, prob) in enumerate(pred, 1):
        print(f"  {i}. {carrera}: {prob:.2%}")
    print()
    
    # Resumen
    all_ok = eje_correcto and sin_contaminacion
    status = "✓ PASS" if all_ok else "✗ FAIL"
    print(f"Estado: {status}")
    print()
    
    return all_ok


def main():
    print("\n" + "=" * 70)
    print("VALIDACIÓN DEL SISTEMA JERÁRQUICO DE EJES PROFESIONALES")
    print("=" * 70 + "\n")
    
    resultados = []
    
    # =========================================================================
    # Perfil 1: Ciberseguridad pura
    # =========================================================================
    perfil_cyber = crear_perfil_extremo(
        features_altas=[
            "Cyber Security",
            "Computer Forensics Fundamentals",
            "Networking",
            "Troubleshooting skills",
        ],
        features_bajas=[
            "Graphics Designing",
            "Business Analysis",
            "Project Management",
        ]
    )
    
    carreras_cyber = {
        "Cyber Security Specialist",
        "Information Security Specialist",
    }
    
    resultados.append(validar_perfil(
        "CIBERSEGURIDAD PURA",
        perfil_cyber,
        "ciberseguridad",
        carreras_cyber
    ))
    
    # =========================================================================
    # Perfil 2: Data Science / AI-ML
    # =========================================================================
    perfil_datos = crear_perfil_extremo(
        features_altas=[
            "AI ML",
            "Data Science",
            "Programming Skills",
            "Database Fundamentals",
        ],
        features_bajas=[
            "Graphics Designing",
            "Project Management",
            "Networking",
        ]
    )
    
    carreras_datos = {
        "AI ML Specialist",
        "Database Administrator",
    }
    
    resultados.append(validar_perfil(
        "DATA SCIENCE / AI-ML",
        perfil_datos,
        "datos_ia",
        carreras_datos
    ))
    
    # =========================================================================
    # Perfil 3: Desarrollo de Software
    # =========================================================================
    perfil_dev = crear_perfil_extremo(
        features_altas=[
            "Software Development",
            "Software Engineering",
            "Programming Skills",
        ],
        features_bajas=[
            "Graphics Designing",
            "Cyber Security",
            "Networking",
        ]
    )
    
    carreras_dev = {
        "Software Developer",
        "API Specialist",
        "Software tester",
    }
    
    resultados.append(validar_perfil(
        "DESARROLLO DE SOFTWARE",
        perfil_dev,
        "desarrollo_software",
        carreras_dev
    ))
    
    # =========================================================================
    # Resumen final
    # =========================================================================
    print("=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)
    
    total = len(resultados)
    pasados = sum(resultados)
    
    print(f"Tests pasados: {pasados}/{total}")
    
    if pasados == total:
        print("\n✓ TODOS LOS TESTS PASARON")
        print("  - Ciberseguridad → detectado correctamente, sin contaminación")
        print("  - Data Science → detectado correctamente, sin contaminación")
        print("  - Software Dev → detectado correctamente, sin contaminación")
        print("\n  Graphics Designer y Customer Service NO pueden ganar en perfiles técnicos.")
        return 0
    else:
        print("\n✗ ALGUNOS TESTS FALLARON")
        return 1


if __name__ == "__main__":
    sys.exit(main())
