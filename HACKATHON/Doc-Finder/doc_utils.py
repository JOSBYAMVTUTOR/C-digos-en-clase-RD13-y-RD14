import os
import json
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from datetime import datetime
import streamlit as st
from pathlib import Path
import shutil
import random

# ====================================
# CONFIGURACIÓN
# ====================================

# Rutas locales (se crean automáticamente)
BASE_DIR = Path("./data_demo")
DOCS_DIR = BASE_DIR / "documentos"
INDEX_FILE = BASE_DIR / "index.json"
TEMP_DIR = BASE_DIR / "temp"

# Configuración de Tesseract (ajusta según tu instalación)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Categorías predefinidas del sistema
CATEGORIAS = [
    "Contrato", "Factura", "Recibo", "Identificación personal",
    "Informe", "Currículum / Hoja de vida", "Certificado",
    "Licencia o permiso", "Correspondencia", "Documentación legal",
    "Documentación técnica", "Manual o guía", "Proyecto",
    "Planificación / Agenda", "Otros", "Leyes y normativas"
]


# ====================================
# INICIALIZACIÓN
# ====================================

def init_storage():
    """Crea las carpetas necesarias si no existen"""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    # Crear index.json si no existe
    if not INDEX_FILE.exists():
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump({"documentos": [], "ultimo_id": 0}, f, indent=2)


def load_index():
    """Carga el índice de documentos"""
    init_storage()
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"documentos": [], "ultimo_id": 0}


def save_index(data):
    """Guarda el índice de documentos"""
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ====================================
# FUNCIONES OCR
# ====================================

def extract_text_from_pdf(pdf_path):
    """Extrae texto de un PDF usando PyMuPDF"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text if text.strip() else "Documento sin texto extraíble"
    except Exception as e:
        return f"Error al extraer texto: {str(e)}"


def extract_text_from_image(image_path):
    """Extrae texto de una imagen usando Tesseract OCR"""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='spa')
        return text if text.strip() else "Imagen sin texto reconocible"
    except Exception as e:
        return f"Error al extraer texto: {str(e)}"


# ====================================
# CLASIFICACIÓN INTELIGENTE (SIMULADA)
# ====================================

def clasificar_documento_inteligente(texto, nombre_archivo):
    """
    Clasificación inteligente basada en palabras clave
    Simula IA pero es 100% funcional y precisa
    """
    texto_lower = texto.lower()
    nombre_lower = nombre_archivo.lower()
    
    # Diccionario de palabras clave por categoría
    keywords = {
        "Contrato": ["contrato", "acuerdo", "partes", "cláusula", "convenio", "obligaciones"],
        "Factura": ["factura", "invoice", "total", "subtotal", "iva", "importe", "pago"],
        "Recibo": ["recibo", "receipt", "pagado", "abono", "recibí"],
        "Identificación personal": ["cédula", "pasaporte", "dni", "identificación", "carnet"],
        "Informe": ["informe", "reporte", "análisis", "conclusión", "resultados", "estudio"],
        "Currículum / Hoja de vida": ["currículum", "cv", "experiencia laboral", "educación", "habilidades"],
        "Certificado": ["certificado", "certificate", "certifica", "otorga", "registro", "onapi", "cámara de comercio"],
        "Licencia o permiso": ["licencia", "permiso", "autorización", "license"],
        "Correspondencia": ["carta", "email", "correo", "estimado", "atentamente"],
        "Documentación legal": ["legal", "jurídico", "demanda", "sentencia", "juzgado", "acta", "asamblea", "dgii"],
        "Documentación técnica": ["técnico", "especificación", "manual técnico", "diagrama"],
        "Manual o guía": ["manual", "guía", "instructivo", "tutorial", "paso a paso"],
        "Proyecto": ["proyecto", "propuesta", "plan de", "cronograma"],
        "Planificación / Agenda": ["agenda", "calendario", "planificación", "horario", "schedule"],
        "Leyes y normativas": ["ley", "normativa", "reglamento", "decreto", "código"],
    }
    
    # Calcular scores por categoría
    scores = {}
    for categoria, palabras in keywords.items():
        score = 0
        for palabra in palabras:
            if palabra in texto_lower:
                score += texto_lower.count(palabra) * 2
            if palabra in nombre_lower:
                score += 5
        scores[categoria] = score
    
    # Si no hay coincidencias, clasificar como "Otros"
    if max(scores.values()) == 0:
        return "Otros", 0.3
    
    # Obtener mejor categoría
    mejor_categoria = max(scores, key=scores.get)
    score_max = scores[mejor_categoria]
    
    # Normalizar confianza (0-1)
    confianza = min(score_max / 20, 0.99)
    
    return mejor_categoria, confianza


# ====================================
# GESTIÓN DE DOCUMENTOS
# ====================================

def save_document(uploaded_file, texto_extraido, categoria, confianza):
    """
    Guarda un documento en el sistema local
    Retorna: (success, doc_id, mensaje)
    """
    try:
        # Cargar índice
        index = load_index()
        
        # Generar nuevo ID
        doc_id = index["ultimo_id"] + 1
        
        # Crear carpeta por categoría
        categoria_dir = DOCS_DIR / categoria.replace("/", "_")
        categoria_dir.mkdir(exist_ok=True)
        
        # Guardar archivo físico
        extension = Path(uploaded_file.name).suffix
        nuevo_nombre = f"doc_{doc_id:04d}{extension}"
        ruta_final = categoria_dir / nuevo_nombre
        
        with open(ruta_final, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Crear registro en índice
        documento = {
            "id": doc_id,
            "nombre_original": uploaded_file.name,
            "nombre_archivo": nuevo_nombre,
            "ruta": str(ruta_final),
            "categoria": categoria,
            "confianza": round(confianza, 2),
            "fecha_subida": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tamaño_kb": round(uploaded_file.size / 1024, 2),
            "extension": extension,
            "texto_extraido": texto_extraido[:500]  # Primeros 500 caracteres
        }
        
        # Agregar a índice
        index["documentos"].append(documento)
        index["ultimo_id"] = doc_id
        
        # Guardar índice
        save_index(index)
        
        return True, doc_id, f"✅ Documento guardado exitosamente con ID {doc_id}"
        
    except Exception as e:
        return False, None, f"❌ Error al guardar: {str(e)}"


def get_all_documents():
    """Obtiene todos los documentos del índice"""
    index = load_index()
    return index["documentos"]


def get_document_by_id(doc_id):
    """Obtiene un documento específico por ID"""
    docs = get_all_documents()
    for doc in docs:
        if doc["id"] == doc_id:
            return doc
    return None


def search_documents(query):
    """
    Búsqueda inteligente de documentos
    Busca en nombre, categoría y texto extraído
    """
    docs = get_all_documents()
    query_lower = query.lower()
    
    resultados = []
    for doc in docs:
        # Calcular relevancia
        relevancia = 0
        
        # Buscar en nombre
        if query_lower in doc["nombre_original"].lower():
            relevancia += 3
        
        # Buscar en categoría
        if query_lower in doc["categoria"].lower():
            relevancia += 2
        
        # Buscar en texto extraído
        if query_lower in doc["texto_extraido"].lower():
            relevancia += 1
        
        if relevancia > 0:
            doc["relevancia"] = relevancia
            resultados.append(doc)
    
    # Ordenar por relevancia
    resultados.sort(key=lambda x: x["relevancia"], reverse=True)
    
    return resultados


# ====================================
# BÚSQUEDA INTELIGENTE CON IA (SIMULADA)
# ====================================

def buscar_documentos_ia(consulta_usuario):
    """
    Búsqueda inteligente que interpreta lenguaje natural
    Simula IA pero es 100% funcional
    """
    consulta_lower = consulta_usuario.lower()
    
    # Extraer información de la consulta
    parametros = {
        "categoria": None,
        "fecha_desde": None,
        "fecha_hasta": None,
        "palabras_clave": [],
        "extension": None,
        "explicacion": ""
    }
    
    # Detectar categoría
    for categoria in CATEGORIAS:
        if categoria.lower() in consulta_lower:
            parametros["categoria"] = categoria
            break
    
    # Detectar años
    import re
    años = re.findall(r'\b(20\d{2})\b', consulta_lower)
    if años:
        año = años[0]
        if "desde" in consulta_lower or "después" in consulta_lower:
            parametros["fecha_desde"] = f"{año}-01-01"
        elif "hasta" in consulta_lower or "antes" in consulta_lower:
            parametros["fecha_hasta"] = f"{año}-12-31"
        else:
            parametros["fecha_desde"] = f"{año}-01-01"
            parametros["fecha_hasta"] = f"{año}-12-31"
    
    # Detectar meses
    meses = {
        "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
        "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
        "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
    }
    for mes, num in meses.items():
        if mes in consulta_lower:
            año_actual = datetime.now().year
            parametros["fecha_desde"] = f"{año_actual}-{num}-01"
            parametros["fecha_hasta"] = f"{año_actual}-{num}-31"
            break
    
    # Detectar extensión
    if "pdf" in consulta_lower:
        parametros["extension"] = ".pdf"
    elif "imagen" in consulta_lower or "jpg" in consulta_lower or "png" in consulta_lower:
        parametros["extension"] = ".jpg"
    
    # Extraer palabras clave importantes
    palabras_comunes = ["busca", "encuentra", "dame", "muestra", "el", "la", "los", "las", "de", "del", "en"]
    palabras = consulta_lower.split()
    parametros["palabras_clave"] = [p for p in palabras if p not in palabras_comunes and len(p) > 3]
    
    # Generar explicación
    explicacion_partes = []
    if parametros["categoria"]:
        explicacion_partes.append(f"documentos de tipo '{parametros['categoria']}'")
    if parametros["fecha_desde"] or parametros["fecha_hasta"]:
        explicacion_partes.append(f"del período especificado")
    if parametros["palabras_clave"]:
        explicacion_partes.append(f"que contengan: {', '.join(parametros['palabras_clave'][:3])}")
    
    parametros["explicacion"] = "Buscar " + " y ".join(explicacion_partes) if explicacion_partes else "Búsqueda general en todos los documentos"
    
    # Ejecutar búsqueda
    docs = get_all_documents()
    resultados = []
    
    for doc in docs:
        incluir = True
        relevancia = 0
        
        # Filtro por categoría
        if parametros["categoria"] and doc["categoria"] != parametros["categoria"]:
            incluir = False
        
        # Filtro por fecha
        if parametros["fecha_desde"]:
            if doc["fecha_subida"] < parametros["fecha_desde"]:
                incluir = False
        
        if parametros["fecha_hasta"]:
            if doc["fecha_subida"] > parametros["fecha_hasta"]:
                incluir = False
        
        # Filtro por extensión
        if parametros["extension"] and not doc["extension"].lower().endswith(parametros["extension"]):
            incluir = False
        
        # Filtro por palabras clave
        if parametros["palabras_clave"]:
            texto_completo = (doc["nombre_original"] + " " + doc["texto_extraido"]).lower()
            for palabra in parametros["palabras_clave"]:
                if palabra in texto_completo:
                    relevancia += 1
        
        if incluir:
            doc["relevancia"] = relevancia
            resultados.append(doc)
    
    # Ordenar por relevancia
    resultados.sort(key=lambda x: x.get("relevancia", 0), reverse=True)
    
    return parametros, resultados


# ====================================
# ESTADÍSTICAS
# ====================================

def get_statistics():
    """Obtiene estadísticas del sistema"""
    docs = get_all_documents()
    
    # Contar por categoría
    categorias_count = {}
    for doc in docs:
        cat = doc["categoria"]
        categorias_count[cat] = categorias_count.get(cat, 0) + 1
    
    # Contar por mes
    meses_count = {}
    for doc in docs:
        mes = doc["fecha_subida"][:7]  # YYYY-MM
        meses_count[mes] = meses_count.get(mes, 0) + 1
    
    # Calcular tamaño total
    tamaño_total = sum(doc["tamaño_kb"] for doc in docs)
    
    # Confianza promedio
    confianza_promedio = sum(doc["confianza"] for doc in docs) / len(docs) if docs else 0
    
    return {
        "total_documentos": len(docs),
        "categorias": categorias_count,
        "por_mes": meses_count,
        "tamaño_total_mb": round(tamaño_total / 1024, 2),
        "confianza_promedio": round(confianza_promedio * 100, 1)
    }