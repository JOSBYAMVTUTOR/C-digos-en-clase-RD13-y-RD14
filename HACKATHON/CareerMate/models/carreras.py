CARRERAS_OBJETIVO = [
    "AI ML Specialist",
    "API Specialist",
    "Application Support Engineer",
    "Business Analyst",
    "Customer Service Executive",
    "Cyber Security Specialist",
    "Database Administrator",
    "Graphics Designer",
    "Hardware Engineer",
    "Helpdesk Engineer",
    "Information Security Specialist",
    "Networking Engineer",
    "Project Manager",
    "Software Developer",
    "Software tester",
    "Technical Writer",
]

DESCRIPCIONES = {
    "AI ML Specialist": "Diseñas y entrenas modelos de IA/ML, experimentas con datos y mejoras la precisión con iteraciones continuas.",
    "API Specialist": "Diseñas, construyes y mantienes APIs robustas; te enfocas en integraciones, contratos, seguridad y rendimiento.",
    "Application Support Engineer": "Aseguras que las aplicaciones funcionen en producción: monitoreo, incidentes, análisis de logs y mejoras operativas.",
    "Business Analyst": "Traducís necesidades del negocio a requerimientos claros, analizas métricas y propones soluciones basadas en evidencia.",
    "Customer Service Executive": "Eres el puente con usuarios: entiendes problemas, gestionas casos y elevas hallazgos para mejorar el producto.",
    "Cyber Security Specialist": "Proteges sistemas y datos: hardening, detección de amenazas, respuesta a incidentes y buenas prácticas de seguridad.",
    "Database Administrator": "Administras bases de datos: backups, performance tuning, seguridad, disponibilidad y optimización de consultas.",
    "Graphics Designer": "Creas piezas visuales y diseño gráfico; priorizas comunicación visual, consistencia y claridad estética.",
    "Hardware Engineer": "Trabajas con arquitectura y componentes físicos: diagnóstico, integración, pruebas y optimización de hardware.",
    "Helpdesk Engineer": "Soporte técnico de primera línea: resolución de tickets, troubleshooting, guías y escalamiento eficiente.",
    "Information Security Specialist": "Gobierno y controles de seguridad: políticas, auditorías, riesgos, cumplimiento y gestión de accesos.",
    "Networking Engineer": "Diseñas y operas redes: routing, switching, conectividad, performance, monitoreo y disponibilidad.",
    "Project Manager": "Planificas y coordinas proyectos: alcance, tiempos, riesgos, comunicación y entrega de valor.",
    "Software Developer": "Construyes software: diseño, implementación, pruebas, mantenimiento y colaboración en equipo.",
    "Software tester": "Aseguras calidad: casos de prueba, automatización, reportes de bugs y validación de entregas.",
    "Technical Writer": "Documentas de forma clara: guías, manuales, documentación técnica y comunicación para distintos públicos.",
}

IMAGENES_CARRERA = {
    "ai": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=60",
    "ml": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=60",
    "api": "https://images.unsplash.com/photo-1526378722445-7e9f4a9c1c22?auto=format&fit=crop&w=800&q=60",
    "support": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=800&q=60",
    "business": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=800&q=60",
    "customer": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=800&q=60",
    "cyber": "https://images.unsplash.com/photo-1510511459019-5dda7724fd87?auto=format&fit=crop&w=800&q=60",
    "security": "https://images.unsplash.com/photo-1510511459019-5dda7724fd87?auto=format&fit=crop&w=800&q=60",
    "database": "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?auto=format&fit=crop&w=800&q=60",
    "graphics": "https://images.unsplash.com/photo-1561070791-2526d30994b5?auto=format&fit=crop&w=800&q=60",
    "hardware": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=60",
    "helpdesk": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=800&q=60",
    "network": "https://images.unsplash.com/photo-1582719478248-7e0ec3965d92?auto=format&fit=crop&w=800&q=60",
    "project": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=800&q=60",
    "developer": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=60",
    "tester": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=800&q=60",
    "writer": "https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=800&q=60",
}

def obtener_imagen_carrera(carrera_nombre: str) -> str:
    key = carrera_nombre.strip().lower()
    for palabra_clave, url in IMAGENES_CARRERA.items():
        if palabra_clave in key:
            return url
    return "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=60"
