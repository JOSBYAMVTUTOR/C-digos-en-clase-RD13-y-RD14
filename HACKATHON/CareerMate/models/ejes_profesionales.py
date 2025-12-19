"""
Sistema Jerárquico de Ejes Profesionales (Hierarchical Decision System)

Arquitectura:
1. Detección de Eje Profesional (matemática explicable, NO ML)
2. Filtrado de carreras por eje (elimina contaminación cruzada)
3. Ranking fino dentro del eje (ML o scoring)

Este módulo reemplaza la lógica monolítica por un sistema de dos etapas
que garantiza coherencia humana antes de precisión estadística.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
import numpy as np

from models.entrenamiento import FEATURE_COLUMNS


@dataclass(frozen=True)
class EjeProfesional:
    """Define un eje profesional con sus features y carreras asociadas."""
    id: str
    nombre: str
    descripcion: str
    features_primarias: Tuple[str, ...]      # Features con peso 1.0
    features_secundarias: Tuple[str, ...]    # Features con peso 0.5
    carreras: Tuple[str, ...]                # Carreras permitidas en este eje
    

# Definición formal de los 6 ejes profesionales
EJES_PROFESIONALES: Dict[str, EjeProfesional] = {
    "datos_ia": EjeProfesional(
        id="datos_ia",
        nombre="Datos & Inteligencia Artificial",
        descripcion="Análisis de datos, machine learning, estadística aplicada",
        features_primarias=(
            "AI ML",
            "Data Science",
            "Programming Skills",
        ),
        features_secundarias=(
            "Database Fundamentals",
            "Distributed Computing Systems",
        ),
        carreras=(
            "AI ML Specialist",
            "Database Administrator",
        ),
    ),
    
    "desarrollo_software": EjeProfesional(
        id="desarrollo_software",
        nombre="Desarrollo de Software",
        descripcion="Construcción, diseño e ingeniería de aplicaciones",
        features_primarias=(
            "Software Development",
            "Software Engineering",
            "Programming Skills",
        ),
        features_secundarias=(
            "Database Fundamentals",
            "Distributed Computing Systems",
        ),
        carreras=(
            "Software Developer",
            "API Specialist",
            "Software tester",
        ),
    ),
    
    "infraestructura_redes": EjeProfesional(
        id="infraestructura_redes",
        nombre="Infraestructura & Redes",
        descripcion="Redes, sistemas distribuidos, hardware, conectividad",
        features_primarias=(
            "Networking",
            "Computer Architecture",
            "Distributed Computing Systems",
        ),
        features_secundarias=(
            "Troubleshooting skills",
            "Hardware Engineer",
        ),
        carreras=(
            "Networking Engineer",
            "Hardware Engineer",
            "Application Support Engineer",
        ),
    ),
    
    "ciberseguridad": EjeProfesional(
        id="ciberseguridad",
        nombre="Ciberseguridad",
        descripcion="Seguridad informática, forense digital, protección de sistemas",
        features_primarias=(
            "Cyber Security",
            "Computer Forensics Fundamentals",
            "Networking",
        ),
        features_secundarias=(
            "Troubleshooting skills",
            "Database Fundamentals",
        ),
        carreras=(
            "Cyber Security Specialist",
            "Information Security Specialist",
        ),
    ),
    
    "diseno_producto": EjeProfesional(
        id="diseno_producto",
        nombre="Diseño & Producto",
        descripcion="Diseño visual, experiencia de usuario, comunicación gráfica",
        features_primarias=(
            "Graphics Designing",
        ),
        features_secundarias=(
            "Technical Communication",
            "Communication skills",
            "Openness",
        ),
        carreras=(
            "Graphics Designer",
        ),
    ),
    
    "soporte_gestion": EjeProfesional(
        id="soporte_gestion",
        nombre="Soporte & Gestión",
        descripcion="Gestión de proyectos, soporte técnico, análisis de negocio",
        features_primarias=(
            "Project Management",
            "Business Analysis",
            "Communication skills",
            "Technical Communication",
        ),
        features_secundarias=(
            "Troubleshooting skills",
            "Conscientousness",
            "Extraversion",
        ),
        carreras=(
            "Project Manager",
            "Business Analyst",
            "Technical Writer",
            "Customer Service Executive",
            "Helpdesk Engineer",
        ),
    ),
}


def construir_mapeo_features_ejes() -> Dict[str, List[Tuple[str, float]]]:
    """
    Construye mapeo inverso: feature → [(eje_id, peso), ...]
    Esto permite saber qué ejes afecta cada feature y con qué intensidad.
    """
    mapeo: Dict[str, List[Tuple[str, float]]] = {f: [] for f in FEATURE_COLUMNS}
    
    for eje_id, eje in EJES_PROFESIONALES.items():
        for feat in eje.features_primarias:
            if feat in mapeo:
                mapeo[feat].append((eje_id, 1.0))
        for feat in eje.features_secundarias:
            if feat in mapeo:
                mapeo[feat].append((eje_id, 0.5))
    
    return mapeo

FEATURE_TO_EJES = construir_mapeo_features_ejes()


@dataclass
class ScoreEje:
    """Score calculado para un eje profesional."""
    eje_id: str
    score_raw: float           # Score sin normalizar
    score_normalizado: float   # Score normalizado [0, 1]
    features_contribuyentes: List[Tuple[str, float]] = field(default_factory=list)
    
    
def calcular_scores_ejes(perfil: Dict[str, float]) -> Dict[str, ScoreEje]:
    """
    Calcula el score de cada eje profesional usando media ponderada.
    
    Fórmula por eje:
        score = Σ(feature_value * peso) / Σ(peso)
        
    Donde:
        - features_primarias tienen peso 1.0
        - features_secundarias tienen peso 0.5
    """
    scores: Dict[str, ScoreEje] = {}
    
    for eje_id, eje in EJES_PROFESIONALES.items():
        suma_ponderada = 0.0
        suma_pesos = 0.0
        contribuciones: List[Tuple[str, float]] = []
        
        # Features primarias (peso 1.0)
        for feat in eje.features_primarias:
            if feat in perfil:
                valor = perfil[feat]
                suma_ponderada += valor * 1.0
                suma_pesos += 1.0
                contribuciones.append((feat, valor * 1.0))
        
        # Features secundarias (peso 0.5)
        for feat in eje.features_secundarias:
            if feat in perfil:
                valor = perfil[feat]
                suma_ponderada += valor * 0.5
                suma_pesos += 0.5
                contribuciones.append((feat, valor * 0.5))
        
        score_raw = suma_ponderada / suma_pesos if suma_pesos > 0 else 0.0
        
        # Ordenar contribuciones por impacto
        contribuciones.sort(key=lambda x: x[1], reverse=True)
        
        scores[eje_id] = ScoreEje(
            eje_id=eje_id,
            score_raw=score_raw,
            score_normalizado=0.0,  # Se calcula después
            features_contribuyentes=contribuciones[:5]  # Top 5
        )
    
    # Normalizar scores usando min-max sobre todos los ejes
    all_scores = [s.score_raw for s in scores.values()]
    min_score = min(all_scores) if all_scores else 0.0
    max_score = max(all_scores) if all_scores else 1.0
    rango = max_score - min_score if max_score > min_score else 1.0
    
    for score in scores.values():
        score.score_normalizado = (score.score_raw - min_score) / rango
    
    return scores


@dataclass
class ResultadoEje:
    """Resultado de la detección de eje profesional."""
    eje_principal: str
    eje_secundario: Optional[str]
    es_hibrido: bool
    confianza: float                     # 0.0 a 1.0
    margen: float                        # Diferencia con el segundo
    scores: Dict[str, ScoreEje]
    explicacion: str


def seleccionar_eje(perfil: Dict[str, float], umbral_hibrido: float = 0.15) -> ResultadoEje:
    """
    Selecciona el eje profesional dominante.
    
    Args:
        perfil: Diccionario feature → valor
        umbral_hibrido: Si la diferencia entre top-1 y top-2 es menor, se considera híbrido
        
    Returns:
        ResultadoEje con el eje principal, posible secundario, y explicación
    """
    scores = calcular_scores_ejes(perfil)
    
    # Ordenar por score normalizado
    ranking = sorted(scores.values(), key=lambda x: x.score_normalizado, reverse=True)
    
    if len(ranking) < 2:
        return ResultadoEje(
            eje_principal=ranking[0].eje_id if ranking else "soporte_gestion",
            eje_secundario=None,
            es_hibrido=False,
            confianza=1.0,
            margen=1.0,
            scores=scores,
            explicacion="Único eje disponible"
        )
    
    top1 = ranking[0]
    top2 = ranking[1]
    
    margen = top1.score_normalizado - top2.score_normalizado
    es_hibrido = margen < umbral_hibrido
    
    # Calcular confianza basada en el margen
    confianza = min(1.0, margen / 0.3)  # 0.3 = margen para confianza máxima
    
    # Construir explicación
    eje_info = EJES_PROFESIONALES[top1.eje_id]
    top_features = [f[0] for f in top1.features_contribuyentes[:3]]
    
    if es_hibrido:
        eje2_info = EJES_PROFESIONALES[top2.eje_id]
        explicacion = (
            f"Perfil híbrido: {eje_info.nombre} + {eje2_info.nombre}. "
            f"Features dominantes: {', '.join(top_features)}"
        )
    else:
        explicacion = (
            f"Eje dominante: {eje_info.nombre} (confianza: {confianza:.0%}). "
            f"Features dominantes: {', '.join(top_features)}"
        )
    
    return ResultadoEje(
        eje_principal=top1.eje_id,
        eje_secundario=top2.eje_id if es_hibrido else None,
        es_hibrido=es_hibrido,
        confianza=confianza,
        margen=margen,
        scores=scores,
        explicacion=explicacion
    )


def obtener_carreras_candidatas(resultado_eje: ResultadoEje) -> List[str]:
    """
    Retorna las carreras candidatas según el eje detectado.
    Elimina contaminación cruzada: solo carreras del eje (o ejes si es híbrido).
    """
    carreras: set = set()
    
    # Agregar carreras del eje principal
    eje_principal = EJES_PROFESIONALES.get(resultado_eje.eje_principal)
    if eje_principal:
        carreras.update(eje_principal.carreras)
    
    # Si es híbrido, agregar carreras del eje secundario
    if resultado_eje.es_hibrido and resultado_eje.eje_secundario:
        eje_secundario = EJES_PROFESIONALES.get(resultado_eje.eje_secundario)
        if eje_secundario:
            carreras.update(eje_secundario.carreras)
    
    return list(carreras)


def calcular_afinidad_carrera(
    perfil: Dict[str, float],
    carrera: str,
    eje_id: str
) -> Tuple[float, List[str]]:
    """
    Calcula la afinidad de un perfil con una carrera específica.
    
    Usa las features del eje para calcular un score de compatibilidad.
    Retorna (score, razones).
    """
    eje = EJES_PROFESIONALES.get(eje_id)
    if not eje:
        return (0.5, ["Eje no encontrado"])
    
    # Calcular score basado en features del eje
    score = 0.0
    total_peso = 0.0
    razones: List[str] = []
    
    for feat in eje.features_primarias:
        if feat in perfil:
            valor = perfil[feat]
            score += valor * 1.0
            total_peso += 1.0
            if valor > 1.8:  # Valor alto
                razones.append(f"Fuerte en {feat}")
    
    for feat in eje.features_secundarias:
        if feat in perfil:
            valor = perfil[feat]
            score += valor * 0.5
            total_peso += 0.5
    
    score_final = score / total_peso if total_peso > 0 else 0.5
    
    return (score_final, razones[:3])


@dataclass
class RecomendacionJerarquica:
    """Resultado completo del sistema jerárquico."""
    carrera: str
    compatibilidad: int                  # 0-100
    eje_profesional: str
    eje_nombre: str
    es_hibrido: bool
    razones: List[str]
    explicacion_eje: str


def recomendar_jerarquico(
    perfil: Dict[str, float],
    top: int = 3
) -> List[RecomendacionJerarquica]:
    """
    Sistema de recomendación jerárquico de dos etapas:
    
    1. Detecta el eje profesional (matemática explicable)
    2. Rankea carreras dentro del eje (scoring o ML)
    
    Args:
        perfil: Diccionario feature → valor
        top: Número de recomendaciones a retornar
        
    Returns:
        Lista de RecomendacionJerarquica ordenadas por compatibilidad
    """
    # Etapa 1: Detección del eje
    resultado_eje = seleccionar_eje(perfil)
    
    # Etapa 2: Obtener carreras candidatas (sin contaminación)
    carreras_candidatas = obtener_carreras_candidatas(resultado_eje)
    
    if not carreras_candidatas:
        # Fallback: usar eje de soporte
        carreras_candidatas = list(EJES_PROFESIONALES["soporte_gestion"].carreras)
    
    # Etapa 3: Calcular afinidad para cada carrera candidata
    resultados: List[Tuple[str, float, List[str]]] = []
    
    for carrera in carreras_candidatas:
        # Determinar a qué eje pertenece esta carrera
        eje_carrera = resultado_eje.eje_principal
        if resultado_eje.es_hibrido and resultado_eje.eje_secundario:
            # Verificar si la carrera está en el eje secundario
            eje_sec = EJES_PROFESIONALES.get(resultado_eje.eje_secundario)
            if eje_sec and carrera in eje_sec.carreras:
                eje_carrera = resultado_eje.eje_secundario
        
        score, razones = calcular_afinidad_carrera(perfil, carrera, eje_carrera)
        resultados.append((carrera, score, razones))
    
    # Ordenar por score
    resultados.sort(key=lambda x: x[1], reverse=True)
    
    # Normalizar scores a compatibilidad 0-100
    max_score = 0.0
    min_score = 0.0
    rango = 0.1
    
    if resultados:
        max_score = resultados[0][1]
        min_score = resultados[-1][1] if len(resultados) > 1 else max_score - 0.1
        rango = max_score - min_score if max_score > min_score else 0.1
    
    # Construir recomendaciones finales
    recomendaciones: List[RecomendacionJerarquica] = []
    eje_info = EJES_PROFESIONALES.get(resultado_eje.eje_principal)
    
    for carrera, score, razones in resultados[:top]:
        # Mapear score a compatibilidad (60-100 range para top carreras)
        compat_raw = (score - min_score) / rango if rango > 0 else 0.5
        compatibilidad = int(60 + compat_raw * 40)
        compatibilidad = min(100, max(0, compatibilidad))
        
        # Agregar razón del eje
        razones_completas = razones.copy()
        razones_completas.append(f"Eje: {eje_info.nombre if eje_info else resultado_eje.eje_principal}")
        
        recomendaciones.append(RecomendacionJerarquica(
            carrera=carrera,
            compatibilidad=compatibilidad,
            eje_profesional=resultado_eje.eje_principal,
            eje_nombre=eje_info.nombre if eje_info else resultado_eje.eje_principal,
            es_hibrido=resultado_eje.es_hibrido,
            razones=razones_completas,
            explicacion_eje=resultado_eje.explicacion
        ))
    
    return recomendaciones


def diagnosticar_perfil(perfil: Dict[str, float]) -> str:
    """
    Genera un diagnóstico legible del perfil y su clasificación.
    Útil para debugging y explicabilidad.
    """
    resultado = seleccionar_eje(perfil)
    
    lineas = [
        "=" * 60,
        "DIAGNÓSTICO DE PERFIL",
        "=" * 60,
        "",
        f"Eje Principal: {EJES_PROFESIONALES[resultado.eje_principal].nombre}",
        f"Híbrido: {'Sí' if resultado.es_hibrido else 'No'}",
    ]
    
    if resultado.es_hibrido and resultado.eje_secundario:
        lineas.append(f"Eje Secundario: {EJES_PROFESIONALES[resultado.eje_secundario].nombre}")
    
    lineas.extend([
        f"Confianza: {resultado.confianza:.0%}",
        f"Margen: {resultado.margen:.3f}",
        "",
        "Scores por Eje:",
    ])
    
    # Ordenar ejes por score
    ranking = sorted(resultado.scores.values(), key=lambda x: x.score_normalizado, reverse=True)
    for score in ranking:
        eje_info = EJES_PROFESIONALES[score.eje_id]
        lineas.append(f"  {eje_info.nombre}: {score.score_normalizado:.3f} (raw: {score.score_raw:.3f})")
    
    lineas.extend([
        "",
        "Carreras Candidatas:",
    ])
    
    carreras = obtener_carreras_candidatas(resultado)
    for c in carreras:
        lineas.append(f"  - {c}")
    
    lineas.extend([
        "",
        f"Explicación: {resultado.explicacion}",
        "=" * 60,
    ])
    
    return "\n".join(lineas)
