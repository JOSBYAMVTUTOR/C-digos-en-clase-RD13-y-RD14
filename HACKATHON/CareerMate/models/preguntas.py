from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

TipoPregunta = Literal["tecnica", "blanda"]
Dificultad = Literal["intermedia", "avanzada"]


@dataclass(frozen=True)
class Opcion:
    texto: str
    pesos: dict[str, float]

    def to_dict(self):
        return {"texto": self.texto, "pesos": self.pesos}


@dataclass(frozen=True)
class Pregunta:
    id: int
    texto: str
    tipo: TipoPregunta
    feature_principal: str
    dificultad: Dificultad
    informatividad: float
    opciones: tuple[Opcion, ...]

    def to_dict(self):
        return {
            "id": self.id,
            "texto": self.texto,
            "tipo": self.tipo,
            "feature_principal": self.feature_principal,
            "dificultad": self.dificultad,
            "informatividad": self.informatividad,
            "opciones": [o.to_dict() for o in self.opciones],
        }


LIKERT = (
    ("Totalmente en desacuerdo", -0.3),
    ("En desacuerdo", -0.15),
    ("Neutral", 0.0),
    ("De acuerdo", 0.15),
    ("Totalmente de acuerdo", 0.3),
)


def tecnica(id, texto, feature, opciones):
    pesos = (-0.2, 0.1, 0.35, 0.6)
    return Pregunta(
        id=id,
        texto=texto,
        tipo="tecnica",
        feature_principal=feature,
        dificultad="intermedia",
        informatividad=0.8,
        opciones=tuple(
            Opcion(opciones[i], {feature: pesos[i]}) for i in range(4)
        ),
    )

def blanda(id, texto, feature):
    return Pregunta(
        id=id,
        texto=texto,
        tipo="blanda",
        feature_principal=feature,
        dificultad="avanzada",
        informatividad=0.65,
        opciones=tuple(Opcion(t, {feature: w}) for t, w in LIKERT),
    )


P = []
i = 0

P.append(tecnica(i,"¿Cómo describirías tu capacidad para diseñar, optimizar y mantener bases de datos relacionales?","Database Fundamentals",[
    "Evito o tengo dificultades con tareas relacionadas con bases de datos.",
    "Puedo ejecutar consultas básicas y entender esquemas simples.",
    "Diseño esquemas eficientes, optimizo consultas y manejo la integridad de datos.",
    "Arquitecto y gestiono sistemas de bases de datos complejos, distribuidos o de alto rendimiento."
])); i+=1

P.append(tecnica(i,"¿Cuál es tu nivel de comprensión y experiencia con los componentes internos de hardware y su interacción con el software?","Computer Architecture",[
    "No es un área de mi interés o conocimiento.",
    "Conozco los componentes básicos (CPU, RAM) a nivel de usuario.",
    "Comprendo en detalle cómo la arquitectura afecta el rendimiento del software y puedo realizar configuraciones básicas de sistema.",
    "Optimizo sistemas a nivel de hardware, analizo rendimiento a bajo nivel o diseño soluciones considerando restricciones físicas."
])); i+=1

P.append(tecnica(i,"¿Cómo te sientes trabajando con sistemas que procesan datos a través de múltiples servidores o nodos coordinados?","Distributed Computing Systems",[
    "Prefiero sistemas y aplicaciones que se ejecuten en una sola máquina.",
    "Entiendo los conceptos básicos, pero no he trabajado en la práctica con tales sistemas.",
    "He desarrollado o contribuido a aplicaciones que se ejecutan en entornos distribuidos (ej. cloud, clusters).",
    "Diseño, implemento y soluciono problemas de arquitecturas distribuidas complejas y escalables."
])); i+=1

P.append(tecnica(i,"¿Cuál es tu experiencia y nivel de proactividad en la identificación y mitigación de vulnerabilidades de seguridad en sistemas digitales?","Cyber Security",[
    "La seguridad cibernética no es un foco en mi trabajo actual.",
    "Sigo políticas de seguridad básicas (contraseñas, actualizaciones).",
    "Activamente implemento medidas de seguridad, realizo análisis de riesgos o pruebas básicas de penetración.",
    "Dirijo evaluaciones de seguridad ofensiva/defensiva, diseño estrategias de seguridad integrales para organizaciones."
])); i+=1

P.append(tecnica(i,"¿Cuál es tu dominio en el diseño, configuración y solución de problemas de redes de comunicaciones de datos?","Networking",[
    "Tengo un conocimiento limitado a conectarme a una red WiFi/Internet.",
    "Entiendo modelos como TCP/IP y puedo diagnosticar problemas de conectividad básicos.",
    "Configuro routers, switches, firewalls y entiendo en profundidad protocolos de red.",
    "Diseño infraestructuras de red empresariales complejas, optimizo el rendimiento y la seguridad de la red."
])); i+=1

P.append(tecnica(i,"¿Con qué frecuencia y complejidad desarrollas aplicaciones o scripts funcionales desde cero?","Software Development",[
    "Rara vez escribo código o lo hago sólo para tareas muy simples y personales.",
    "Modifico código existente o desarrollo pequeños scripts para automatizar tareas.",
    "Desarrollo aplicaciones completas y mantenibles siguiendo buenas prácticas.",
    "Lidero el desarrollo de sistemas de software complejos, tomando decisiones clave de arquitectura."
])); i+=1

P.append(tecnica(i,"Evalúa tu fluidez y profundidad en el uso de lenguajes de programación para resolver problemas.","Programming Skills",[
    "Tengo conocimientos muy básicos o nulos de programación.",
    "Conozco la sintaxis de uno o dos lenguajes y puedo resolver problemas algorítmicos sencillos.",
    "Tengo soltura en múltiples lenguajes y paradigmas, escribiendo código eficiente y bien estructurado.",
    "Dominio lenguajes especializados, patrones de diseño avanzados y optimización de código a bajo nivel."
])); i+=1

P.append(tecnica(i,"¿Cuál es tu experiencia en la planificación, ejecución y entrega de proyectos tecnológicos dentro de plazo y presupuesto?","Project Management",[
    "Prefiero enfocarme en tareas técnicas individuales, no en la gestión de proyectos.",
    "He gestionado pequeñas tareas o mi propio trabajo usando listas de pendientes.",
    "He gestionado proyectos completos, coordinando recursos, plazos y comunicándome con stakeholders.",
    "Gestiono portafolios de proyectos complejos, utilizando metodologías avanzadas (Agile/Scrum, Waterfall) y métricas."
])); i+=1

P.append(tecnica(i,"¿Qué tan familiarizado estás con las técnicas para investigar y analizar evidencias digitales después de un incidente de seguridad?","Computer Forensics Fundamentals",[
    "No tengo conocimientos en esta área.",
    "Entiendo el concepto general y su importancia.",
    "He utilizado herramientas básicas de análisis forense o he participado en simulacros de respuesta a incidentes.",
    "He dirigido o participado activamente en investigaciones forenses digitales reales, preservando la cadena de custodia."
])); i+=1

P.append(tecnica(i,"¿Cómo evalúas tu habilidad para explicar conceptos técnicos complejos a audiencias no técnicas o documentar sistemas claramente?","Technical Communication",[
    "Me resulta difícil traducir ideas técnicas a un lenguaje sencillo.",
    "Puedo explicar mis propias tareas de trabajo a colegas.",
    "Produzco documentación técnica clara y realizo presentaciones efectivas para diferentes audiencias.",
    "Creo manuales, informes o materiales de formación complejos que son referencia en mi organización."
])); i+=1

P.append(tecnica(i,"¿Cuál es tu nivel de experiencia práctica en el desarrollo e implementación de modelos de inteligencia artificial o aprendizaje automático?","AI ML",[
    "No trabajo con AI/ML y tengo un conocimiento teórico limitado.",
    "Comprendo los conceptos básicos y he experimentado con tutoriales o cursos.",
    "He entrenado, evaluado y desplegado modelos para resolver problemas empresariales específicos.",
    "Investigo, diseño y optimizo arquitecturas de modelos avanzados (ej. deep learning) para aplicaciones de vanguardia."
])); i+=1

P.append(tecnica(i,"¿Hasta qué punto aplicas principios de ingeniería en el ciclo de vida del software?","Software Engineering",[
    "Me centro principalmente en que el código funcione, más que en los procesos de ingeniería.",
    "Utilizo control de versiones y escribo algunas pruebas unitarias.",
    "Diseño siguiendo patrones, implemento pipelines de integración/despliegue y me preocupo por la calidad a largo plazo.",
    "Defino y hago cumplir estándares de arquitectura y calidad en equipos grandes, optimizando todo el ciclo de vida DevOps."
])); i+=1

P.append(tecnica(i,"¿Con qué frecuencia y profundidad analizas necesidades del negocio para traducirlas en requisitos técnicos funcionales?","Business Analysis",[
    "Raramente interactúo con el lado comercial o de usuarios finales.",
    "Recibo requisitos ya definidos y los implemento.",
    "Activamente entrevisto a stakeholders, documento requisitos y propongo soluciones técnicas que alineen con objetivos de negocio.",
    "Realizo análisis estratégicos de procesos de negocio para identificar oportunidades de transformación digital."
])); i+=1

P.append(tecnica(i,"¿Cómo valoras tu eficacia en la comunicación oral y escrita dentro de un entorno profesional tecnológico?","Communication skills",[
    "Mi comunicación es a veces poco clara o tengo dificultades para expresar mis ideas en equipo.",
    "Me comunico adecuadamente en mi círculo técnico inmediato.",
    "Me adapto a mi audiencia (técnica/no técnica) y facilito reuniones productivas y debates claros.",
    "Negocio, persuado o median conflictos complejos a través de una comunicación excepcionalmente clara y estratégica."
])); i+=1

P.append(tecnica(i,"¿Qué experiencia tienes en el análisis exploratorio, la limpieza de datos y la extracción de insights accionables usando estadística?","Data Science",[
    "No suelo trabajar directamente con análisis de datos.",
    "Uso herramientas básicas (ej. Excel) para resumir datos.",
    "Utilizo lenguajes como Python/R para limpiar, visualizar y analizar conjuntos de datos complejos, encontrando tendencias.",
    "Diseño experimentos, realizo análisis estadísticos avanzados y construyo pipelines de datos para guiar la toma de decisiones estratégicas."
])); i+=1

P.append(tecnica(i,"Ante un sistema complejo que falla, ¿cómo describirías tu método para diagnosticar y resolver la causa raíz del problema?","Troubleshooting skills",[
    "Me frustro fácilmente y suelo requerir ayuda significativa.",
    "Sigo procedimientos establecidos o busco soluciones conocidas.",
    "Metódicamente aíslo variables, pruebo hipótesis y uso herramientas de diagnóstico para resolver problemas novedosos.",
    "Soy experto en diagnosticar fallos críticos y ambiguos en sistemas en producción, a menudo bajo presión de tiempo."
])); i+=1

P.append(tecnica(i,"¿Cuál es tu competencia en la creación o manipulación de elementos visuales (UI, gráficos, diagramas) para comunicar ideas?","Graphics Designing",[
    "No tengo habilidades ni interés en diseño gráfico.",
    "Uso herramientas básicas para crear diagramas simples o modificar imágenes de forma elemental.",
    "Creo interfaces de usuario atractivas, infografías o materiales de marketing con herramientas profesionales (ej. Adobe Suite, Figma).",
    "Diseño sistemas de identidad visual complejos, experiencias de usuario (UX) o gráficos por computadora de alto nivel."
])); i+=1

P.append(tecnica(i,"¿Con qué frecuencia participas en todo el ciclo de desarrollo de una característica, desde la idea hasta el despliegue y mantenimiento?","Software Development",[
    "Usualmente trabajo en partes aisladas de un proyecto más grande.",
    "He completado el ciclo algunas veces en proyectos pequeños personales o académicos.",
    "Es mi actividad principal: regularmente entrego características completas listas para producción.",
    "He estado involucrado en el ciclo completo de múltiples proyectos de gran escala a lo largo de los años."
])); i+=1

P.append(blanda(i,"Me caracterizo por ser organizado, confiable y meticuloso con los detalles en mi trabajo.","Conscientousness")); i+=1
P.append(blanda(i,"Estoy abierto a probar nuevas metodologías de trabajo, incluso si significan salir de mi zona de confort establecida.","Openness to Change")); i+=1
P.append(blanda(i,"Suelo experimentar estrés o frustración cuando enfrento plazos ajustados o críticas técnicas a mi trabajo.","Emotional_Range")); i+=1
P.append(blanda(i,"Priorizo mantener un ambiente de trabajo armonioso y colaborativo, a veces cediendo en mis preferencias técnicas.","Agreeableness")); i+=1
P.append(blanda(i,"Disfruto y busco activamente la interacción y el intercambio de ideas con colegas en entornos de grupo.","Extraversion")); i+=1
P.append(blanda(i,"Me siento cómodo iniciando conversaciones y construyendo rapport con personas nuevas en un contexto profesional.","Conversation")); i+=1
P.append(blanda(i,"Me motiva alcanzar reconocimiento personal, demostrar mi competencia y progresar en mi carrera por méritos propios.","Self-enhancement")); i+=1
P.append(blanda(i,"Valoro que mi trabajo sea entretenido, variado y me permita disfrutar del proceso creativo o resolutivo inmediato.","Hedonism")); i+=1
P.append(blanda(i,"Me importa que mi trabajo contribuya a un bien mayor o tenga un impacto positivo en otras personas o en la sociedad.","Self-transcendence")); i+=1
P.append(blanda(i,"Tengo una curiosidad natural por aprender cómo funcionan las cosas, incluso fuera de mi especialidad inmediata.","Openness")); i+=1
P.append(blanda(i,"Establezco metas personales ambiciosas y persevero hasta completar las tareas, incluso si son desafiantes o tediosas.","Conscientousness")); i+=1
P.append(blanda(i,"Prefiero trabajar en equipo y encontrar consenso, antes que imponer mi punto de vista para ganar una discusión técnica.","Agreeableness")); i+=1


PREGUNTAS_BASE = [p.to_dict() for p in P]

def obtener_pregunta(i):
    return PREGUNTAS_BASE[i] if 0 <= i < len(PREGUNTAS_BASE) else None

def obtener_todas_preguntas():
    return PREGUNTAS_BASE

def contar_preguntas():
    return len(PREGUNTAS_BASE)
