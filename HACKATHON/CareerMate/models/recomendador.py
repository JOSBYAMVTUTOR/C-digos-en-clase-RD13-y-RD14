from __future__ import annotations

import logging
from typing import Dict, List, Tuple, cast

import numpy as np

from models.carreras import CARRERAS_OBJETIVO
from models.entrenamiento import FEATURE_COLUMNS, obtener_limites_features

SOFT_FEATURES = {
    "Openness", "Conscientousness", "Extraversion", "Agreeableness",
    "Emotional_Range", "Conversation", "Openness to Change",
    "Hedonism", "Self-enhancement", "Self-transcendence"
}

# Derivar features técnicas dinámicamente
TECHNICAL_FEATURES = set(FEATURE_COLUMNS) - SOFT_FEATURES

# Requisitos mínimos por carrera (bloquean incompatibilidades semánticas)
REQUISITOS_MINIMOS: Dict[str, Dict[str, float]] = {
    "AI ML Specialist": {
        "AI ML": 1.8,
        "Programming Skills": 1.6,
        "Data Science": 1.6,
    },
    "Database Administrator": {
        "Database Fundamentals": 1.8,
        "Programming Skills": 1.5,
    },
    "Cyber Security Specialist": {
        "Cyber Security": 1.8,
        "Networking": 1.6,
        "Computer Forensics Fundamentals": 1.5,
    },
    "Information Security Specialist": {
        "Cyber Security": 1.6,
        "Networking": 1.5,
    },
    "Networking Engineer": {
        "Networking": 1.8,
        "Troubleshooting skills": 1.6,
    },
    "Hardware Engineer": {
        "Computer Architecture": 1.6,
        "Troubleshooting skills": 1.5,
    },
    "API Specialist": {
        "Programming Skills": 1.6,
        "Software Development": 1.6,
    },
    "Software Developer": {
        "Programming Skills": 1.6,
        "Software Development": 1.7,
        "Software Engineering": 1.6,
    },
    "Software tester": {
        "Software Engineering": 1.5,
        "Troubleshooting skills": 1.6,
    },
    "Application Support Engineer": {
        "Troubleshooting skills": 1.5,
        "Technical Communication": 1.5,
    },
    "Helpdesk Engineer": {
        "Troubleshooting skills": 1.4,
    },
}

# Clasificación de carreras alineada con el dataset real
MACRO_CARRERAS = {
    "tecnico_analitico": {
        "AI ML Specialist",
        "Cyber Security Specialist",
        "Information Security Specialist",
        "Database Administrator",
    },
    "tecnico_operativo": {
        "Software Developer",
        "API Specialist",
        "Networking Engineer",
        "Hardware Engineer",
        "Application Support Engineer",
        "Helpdesk Engineer",
        "Software tester",
    },
    "creativo": {
        "Graphics Designer",
    },
    "soporte": {
        "Customer Service Executive",
        "Technical Writer",
        "Project Manager",
        "Business Analyst",
    },
}

CREATIVE_CAREERS = MACRO_CARRERAS["creativo"]
SUPPORT_CAREERS = MACRO_CARRERAS["soporte"] | {"Application Support Engineer", "Helpdesk Engineer"}
logger = logging.getLogger(__name__)


def calcular_dominancia_tecnica(perfil: Dict[str, float]) -> float:
    """
    Calcula qué tan especializado técnicamente está el perfil.
    Retorna: 0.0 (generalista) a 1.0 (altamente especializado)
    """
    tech_vals = [perfil[f] for f in TECHNICAL_FEATURES if f in perfil]
    soft_vals = [perfil[f] for f in SOFT_FEATURES if f in perfil]

    if not tech_vals or not soft_vals:
        return 0.5

    tech_mean = np.mean(tech_vals)
    soft_mean = np.mean(soft_vals)
    tech_std = np.std(tech_vals)

    # Dominancia pondera relación técnica/soft y la variabilidad técnica
    ratio = tech_mean / (soft_mean + 0.1)  # evitar división por 0
    spread = min(1.0, tech_std / 1.0)      # acotar variabilidad
    dominancia = max(0.0, min(1.0, ratio * 0.6 + spread * 0.4))

    return float(dominancia)


def clasificar_macro_perfil(perfil: Dict[str, float]) -> str:
    """
    Clasifica al usuario en uno de los 4 macro-perfiles.
    """
    tech_vals = [perfil[f] for f in TECHNICAL_FEATURES if f in perfil]
    soft_vals = [perfil[f] for f in SOFT_FEATURES if f in perfil]

    tech_mean = np.mean(tech_vals) if tech_vals else 1.5
    soft_mean = np.mean(soft_vals) if soft_vals else 0.9

    core_seguridad = np.mean([
        perfil.get("Cyber Security", 1.5),
        perfil.get("Networking", 1.5),
        perfil.get("Computer Forensics Fundamentals", 1.5),
        perfil.get("Troubleshooting skills", 1.5),
    ])

    core_datos = np.mean([
        perfil.get("Data Science", 1.5),
        perfil.get("AI ML", 1.5),
        perfil.get("Programming Skills", 1.5),
    ])

    core_dev = np.mean([
        perfil.get("Software Development", 1.5),
        perfil.get("Software Engineering", 1.5),
    ])

    grafico = perfil.get("Graphics Designing", 1.0)

    # Umbrales alineados al rango típico (1.6–2.2)
    if tech_mean >= 2.0 and max(core_seguridad, core_datos, core_dev) >= 2.1:
        return "tecnico_analitico"

    if tech_mean >= 1.8:
        return "tecnico_operativo"

    if grafico >= 2.0 and grafico >= tech_mean and grafico >= soft_mean:
        return "creativo"

    if soft_mean - tech_mean >= 0.2 or soft_mean >= 1.8:
        return "soporte"

    # Fallback seguro hacia técnico operativo para no degradar perfiles técnicos
    return "tecnico_operativo"


def normalizar_minmax(vector: np.ndarray) -> np.ndarray:
    """
    Normaliza el vector al rango [0,1] usando límites del CSV.
    Esto reduce el ruido de escala y mejora la compatibilidad con el modelo.
    """
    try:
        bounds = obtener_limites_features()
        mins = np.array([bounds[col][0] for col in FEATURE_COLUMNS], dtype=float)
        maxs = np.array([bounds[col][1] for col in FEATURE_COLUMNS], dtype=float)
        rango = maxs - mins
        rango[rango < 1e-6] = 1.0
        return (vector - mins) / rango
    except Exception:
        return vector


def desnormalizar_minmax(vector: np.ndarray) -> np.ndarray:
    """
    Revierte la normalización min-max al rango original.
    """
    try:
        bounds = obtener_limites_features()
        mins = np.array([bounds[col][0] for col in FEATURE_COLUMNS], dtype=float)
        maxs = np.array([bounds[col][1] for col in FEATURE_COLUMNS], dtype=float)
        return vector * (maxs - mins) + mins
    except Exception:
        return vector


def normalizar_por_especializacion(vector: np.ndarray, perfil: Dict[str, float]) -> np.ndarray:
    """
    Amplifica la señal de especialización técnica en espacio normalizado.
    """
    dominancia = calcular_dominancia_tecnica(perfil)

    if dominancia < 0.35:
        return vector

    vector_norm = normalizar_minmax(vector)
    mean_val = np.mean(vector_norm)

    if mean_val < 0.01:
        return vector

    above_mean = np.maximum(0.0, vector_norm - mean_val)
    relative = above_mean / (mean_val + 1e-6)
    factor_amplificacion = 1.0 + 0.3 * dominancia * relative
    vector_ajustado = vector_norm * factor_amplificacion
    vector_ajustado = np.clip(vector_ajustado, 0.0, 1.0)

    return desnormalizar_minmax(vector_ajustado)


def filtrar_carreras_por_perfil(macro_perfil: str, dominancia: float) -> List[str]:
    """
    Retorna las carreras candidatas según el macro-perfil.
    Si la dominancia técnica es alta (>0.7), excluye carreras creativas.
    """
    candidatas = set(MACRO_CARRERAS.get(macro_perfil, set()))

    # Si el perfil es técnico analítico, permitir también operativas
    if macro_perfil == "tecnico_analitico":
        candidatas |= MACRO_CARRERAS["tecnico_operativo"]

    # Restringir por dominancia técnica
    if dominancia >= 0.65:
        candidatas -= CREATIVE_CAREERS
        candidatas -= SUPPORT_CAREERS

    # Fallback: si no hay candidatas, usar todas
    if not candidatas:
        candidatas = set(CARRERAS_OBJETIVO)

    return list(candidatas & set(CARRERAS_OBJETIVO))


def cumple_requisitos_minimos(carrera: str, perfil: Dict[str, float]) -> Tuple[bool, str | None]:
    """
    Valida requisitos no compensables para cada carrera.
    Retorna (True, None) si cumple; de lo contrario, False con el motivo.
    """
    requisitos = REQUISITOS_MINIMOS.get(carrera)
    if not requisitos:
        return True, None

    for feature, minimo in requisitos.items():
        valor = perfil.get(feature, 0.0)
        if valor < minimo:
            return False, f"{feature}: {valor:.2f} < {minimo:.2f}"

    return True, None


def construir_vector_usuario(respuestas: List[Tuple[int, int]]) -> np.ndarray:
    """
    Construye el vector de usuario con:
    - Ponderación por informatividad de cada pregunta
    - Suavizado Laplace para evitar valores extremos
    - Filtrado z-score para reducir ruido/outliers
    """
    from models.preguntas import obtener_pregunta

    personality_features = {
        "Openness", "Conscientousness", "Extraversion", "Agreeableness",
        "Emotional_Range", "Conversation", "Openness to Change",
        "Hedonism", "Self-enhancement", "Self-transcendence"
    }

    soft_features = set(personality_features)
    technical_features = set(FEATURE_COLUMNS) - soft_features

    # Inicializar acumuladores con suavizado Laplace (prior débil)
    perfil_sum: Dict[str, float] = {col: 0.0 for col in FEATURE_COLUMNS}
    perfil_weight: Dict[str, float] = {col: 0.0 for col in FEATURE_COLUMNS}
    LAPLACE_ALPHA = 0.1

    for idx_pregunta, idx_opcion in respuestas:
        pregunta = obtener_pregunta(idx_pregunta)
        if not pregunta:
            continue

        opciones = pregunta.get("opciones", [])
        if not (0 <= idx_opcion < len(opciones)):
            continue

        opcion = opciones[idx_opcion]
        pesos = cast(Dict[str, float], opcion.get("pesos", {}))
        informatividad = float(pregunta.get("informatividad", 0.5))

        tipo = cast(str, pregunta.get("tipo", ""))
        if tipo == "tecnica":
            allowed_features = technical_features
        elif tipo == "blanda":
            allowed_features = soft_features
        else:
            allowed_features = set(FEATURE_COLUMNS)

        for feature_name, delta in pesos.items():
            if feature_name in perfil_sum and feature_name in allowed_features:
                perfil_sum[feature_name] += float(delta) * informatividad
                perfil_weight[feature_name] += informatividad

    # Calcular perfil base ponderado por informatividad + Laplace
    perfil: Dict[str, float] = {}
    for col in FEATURE_COLUMNS:
        base = 0.8 if col in personality_features else 1.5
        total_weight = perfil_weight[col] + LAPLACE_ALPHA
        perfil[col] = base + (perfil_sum[col] + LAPLACE_ALPHA * 0.0) / total_weight

    # Construir vector crudo
    vector = np.array([perfil[col] for col in FEATURE_COLUMNS], dtype=float)

    # Reducción de ruido: amortiguar outliers con z-score clipping
    mean_v = np.mean(vector)
    std_v = np.std(vector)
    if std_v > 0.01:
        z_scores = (vector - mean_v) / std_v
        Z_THRESHOLD = 2.5
        vector = np.where(
            np.abs(z_scores) > Z_THRESHOLD,
            mean_v + np.sign(z_scores) * Z_THRESHOLD * std_v,
            vector
        )

    # Aplicar límites del CSV
    try:
        bounds = obtener_limites_features()
        mins = np.array([bounds[col][0] for col in FEATURE_COLUMNS], dtype=float)
        maxs = np.array([bounds[col][1] for col in FEATURE_COLUMNS], dtype=float)
        vector = np.clip(vector, mins, maxs)
    except Exception:
        pass

    return vector.reshape(1, -1)


def generar_razones_recomendacion(perfil: Dict[str, float], carrera: str, macro_perfil: str) -> List[str]:
    """
    Genera razones humanas para explicar por qué se recomienda una carrera.
    """
    razones = []
    
    # Obtener top 5 features del usuario
    features_ordenadas = sorted(perfil.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Mapeo de features a texto legible
    feature_nombres = {
        "AI ML": "Inteligencia Artificial y Machine Learning",
        "Data Science": "Ciencia de Datos",
        "Cyber Security": "Ciberseguridad",
        "Computer Forensics Fundamentals": "Forense Digital",
        "Networking": "Redes y Conectividad",
        "Programming Skills": "Lenguajes de Programación",
        "Software Development": "Desarrollo de Software",
        "Software Engineering": "Ingeniería de Software",
        "Troubleshooting skills": "Resolución de Problemas",
        "Database Fundamentals": "Bases de Datos",
        "Technical Communication": "Comunicación Técnica",
        "Graphics Designing": "Diseño Gráfico",
        "Openness": "Apertura a Experiencias",
        "Conscientousness": "Responsabilidad",
        "Extraversion": "Extroversión",
        "Agreeableness": "Amabilidad",
        "Emotional_Range": "Estabilidad Emocional",
        "Conversation": "Habilidad de Conversación",
        "Openness to Change": "Apertura al Cambio",
        "Hedonism": "Búsqueda de Placer",
        "Self-enhancement": "Autosuperación",
        "Self-transcendence": "Autotrascendencia"
    }
    
    # Agregar razones por features destacadas
    for feature, valor in features_ordenadas[:3]:
        nombre_legible = feature_nombres.get(feature, feature)
        razones.append(f"Alto nivel en {nombre_legible}")
    
    # Agregar razón contextual según macro-perfil
    contexto_perfil = {
        "tecnico_analitico": "Perfil orientado a análisis técnico y resolución de problemas complejos",
        "tecnico_operativo": "Perfil orientado a desarrollo e implementación de soluciones",
        "creativo": "Perfil orientado a diseño y creatividad",
        "soporte": "Perfil orientado a gestión y coordinación de proyectos"
    }
    
    if macro_perfil in contexto_perfil:
        razones.append(contexto_perfil[macro_perfil])
    
    return razones[:4]  # Limitar a 4 razones máximo


def recomendar_carreras(respuestas: List[Tuple[int, int]], top: int = 3):
    """
    Sistema de recomendación jerárquico de dos etapas:
    
    1. Detección del eje profesional (matemática explicable, sin ML)
    2. Ranking de carreras dentro del eje (scoring + ML refinado)
    
    Esto elimina la contaminación cruzada entre dominios incompatibles.
    """
    from models.carreras import DESCRIPCIONES, obtener_imagen_carrera
    from models.modelo_ml import predict_top
    from models.ejes_profesionales import (
        seleccionar_eje,
        obtener_carreras_candidatas,
        EJES_PROFESIONALES,
    )

    if not respuestas:
        return []

    # 1. Construir vector y perfil
    vector_usuario = construir_vector_usuario(respuestas)
    perfil: Dict[str, float] = {}
    for i, col in enumerate(FEATURE_COLUMNS):
        perfil[col] = float(vector_usuario[0, i])

    # 2. ETAPA 1: Detección del eje profesional (matemática, NO ML)
    resultado_eje = seleccionar_eje(perfil)
    eje_info = EJES_PROFESIONALES.get(resultado_eje.eje_principal)

    # 3. Obtener carreras candidatas (sin contaminación cruzada)
    carreras_candidatas = obtener_carreras_candidatas(resultado_eje)

    if not carreras_candidatas:
        carreras_candidatas = list(EJES_PROFESIONALES["soporte_gestion"].carreras)

    # 4. Normalizar vector para ML
    vector_ajustado = normalizar_por_especializacion(vector_usuario, perfil)

    # 5. ETAPA 2: Ranking fino dentro del eje usando ML
    top_k = min(len(carreras_candidatas), max(top * 4, top))
    pred = predict_top(
        vector_ajustado,
        top=top_k,
        carreras_permitidas=carreras_candidatas
    )

    candidatos_filtrados: List[Tuple[str, float]] = []
    exclusiones_internas: List[str] = []

    for carrera, prob in pred:
        cumple, motivo = cumple_requisitos_minimos(carrera, perfil)
        if cumple:
            candidatos_filtrados.append((carrera, prob))
            if len(candidatos_filtrados) >= top:
                break
        else:
            if motivo:
                exclusiones_internas.append(f"Excluida {carrera}: {motivo}")

    if exclusiones_internas:
        logger.info(
            "Carreras filtradas por requisitos mínimos: %s",
            "; ".join(exclusiones_internas),
        )

    # 6. Construir resultados con explicabilidad
    resultados = []
    for carrera, prob in candidatos_filtrados:
        compatibilidad = int(round(max(0.0, min(1.0, prob)) * 100))

        # Generar razones explicativas
        razones = generar_razones_recomendacion(perfil, carrera, resultado_eje.eje_principal)
        
        # Agregar explicación del eje
        razones.append(f"Eje profesional: {eje_info.nombre if eje_info else resultado_eje.eje_principal}")
        if resultado_eje.es_hibrido and resultado_eje.eje_secundario:
            eje_sec = EJES_PROFESIONALES.get(resultado_eje.eje_secundario)
            razones.append(f"Perfil híbrido con: {eje_sec.nombre if eje_sec else resultado_eje.eje_secundario}")
        razones.append(f"Confianza del eje: {resultado_eje.confianza:.0%}")

        resultados.append(
            {
                "carrera": carrera,
                "compatibilidad": compatibilidad,
                "descripcion": DESCRIPCIONES.get(carrera, "Sin descripción disponible."),
                "imagen": obtener_imagen_carrera(carrera),
                "indice": CARRERAS_OBJETIVO.index(carrera) if carrera in CARRERAS_OBJETIVO else -1,
                "probabilidad": float(prob),
                "razones": razones,
                "eje_profesional": resultado_eje.eje_principal,
                "eje_nombre": eje_info.nombre if eje_info else resultado_eje.eje_principal,
                "es_hibrido": resultado_eje.es_hibrido,
            }
        )

    resultados.sort(key=lambda x: x["probabilidad"], reverse=True)
    return resultados[:top]


def calcular_estadisticas(historial):
    if not historial:
        return {
            "total_tests": 0,
            "compatibilidad_promedio": 0,
            "carrera_popular": None,
            "tasa_completacion": 0,
            "por_carrera": {}
        }
    
    total_tests = len(historial)
    compatibilidad_total = 0
    conteo_carreras = {carrera: 0 for carrera in CARRERAS_OBJETIVO}
    compatibilidad_carrera = {carrera: [] for carrera in CARRERAS_OBJETIVO}
    
    total_recomendaciones = 0
    for test in historial:
        carreras = test.get('carreras', [])
        compatibilidades = test.get('compatibilidades', [])
        for i, carrera in enumerate(carreras):
            if i >= len(compatibilidades):
                continue
            compatibilidad = compatibilidades[i]
            if carrera not in conteo_carreras:
                conteo_carreras[carrera] = 0
                compatibilidad_carrera[carrera] = []
            conteo_carreras[carrera] += 1
            compatibilidad_carrera[carrera].append(compatibilidad)
            compatibilidad_total += compatibilidad
            total_recomendaciones += 1

    compatibilidad_promedio = int(compatibilidad_total / total_recomendaciones) if total_recomendaciones > 0 else 0
    carrera_popular = max(conteo_carreras.items(), key=lambda item: item[1])[0] if conteo_carreras else None

    por_carrera = {}
    for carrera, compatibilidades in compatibilidad_carrera.items():
        if compatibilidades:
            por_carrera[carrera] = {
                "count": conteo_carreras[carrera],
                "promedio": int(sum(compatibilidades) / len(compatibilidades))
            }
        else:
            por_carrera[carrera] = {"count": 0, "promedio": 0}
    
    return {
        "total_tests": total_tests,
        "compatibilidad_promedio": compatibilidad_promedio,
        "carrera_popular": carrera_popular,
        "tasa_completacion": 100,
        "por_carrera": por_carrera
    }
