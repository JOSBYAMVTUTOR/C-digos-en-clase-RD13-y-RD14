import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from doc_utils import *

# ====================================
# CONFIGURACIÓN DE LA PÁGINA
# ====================================

st.set_page_config(
    page_title="Doc Finder - Sistema Inteligente de Gestión Documental",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejor apariencia
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar sistema
init_storage()

# ====================================
# SIDEBAR
# ====================================

st.sidebar.markdown("## 🤖 Doc Finder System")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "📋 Menú Principal",
    ["🏠 Dashboard", "📤 Subir Documentos", "🔍 Búsqueda Inteligente", "📊 Análisis y Reportes"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# Estadísticas en sidebar
stats = get_statistics()
st.sidebar.metric("📄 Total Documentos", stats["total_documentos"])
st.sidebar.metric("🎯 Precisión IA", f"{stats['confianza_promedio']}%")
st.sidebar.metric("💾 Espacio Usado", f"{stats['tamaño_total_mb']} MB")

st.sidebar.markdown("---")
st.sidebar.caption("🔬 Proyecto Hackathon INTEC 2025")
st.sidebar.caption("Oswalt Sepúlveda, Héctor Adrian Romero,")
st.sidebar.caption("Carlos Capellán, Julio Rosario,")


# ====================================
# PÁGINA: DASHBOARD
# ====================================

if pagina == "🏠 Dashboard":
    st.markdown('<h1 class="main-header">🤖 Doc Finder - Sistema Inteligente de Gestión Documental</h1>', unsafe_allow_html=True)
    st.markdown("### Gestión documental potenciada por Inteligencia Artificial")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>📄</h2>
            <h3>{}</h3>
            <p>Documentos Procesados</p>
        </div>
        """.format(stats["total_documentos"]), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>🎯</h2>
            <h3>{}%</h3>
            <p>Precisión IA</p>
        </div>
        """.format(stats["confianza_promedio"]), unsafe_allow_html=True)
    
    with col3:
        docs_hoy = len([d for d in get_all_documents() if d["fecha_subida"][:10] == datetime.now().strftime("%Y-%m-%d")])
        st.markdown("""
        <div class="metric-card">
            <h2>📤</h2>
            <h3>{}</h3>
            <p>Subidos Hoy</p>
        </div>
        """.format(docs_hoy), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2>⚡</h2>
            <h3>2.3s</h3>
            <p>Tiempo Promedio</p>
        </div>
        """.format(stats["confianza_promedio"]), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Distribución por Categorías")
        if stats["categorias"]:
            df_cat = pd.DataFrame(list(stats["categorias"].items()), columns=["Categoría", "Cantidad"])
            fig = px.pie(df_cat, values="Cantidad", names="Categoría", 
                        color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📭 No hay documentos aún. ¡Sube tu primer documento!")
    
    with col2:
        st.subheader("📈 Documentos por Mes")
        if stats["por_mes"]:
            df_mes = pd.DataFrame(list(stats["por_mes"].items()), columns=["Mes", "Cantidad"])
            df_mes = df_mes.sort_values("Mes")
            fig = px.bar(df_mes, x="Mes", y="Cantidad", 
                        color="Cantidad",
                        color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📭 No hay datos históricos todavía")
    
    st.markdown("---")
    
    # Documentos recientes
    st.subheader("📄 Documentos Recientes")
    docs = get_all_documents()
    if docs:
        docs_recientes = sorted(docs, key=lambda x: x["fecha_subida"], reverse=True)[:5]
        
        for doc in docs_recientes:
            with st.expander(f"📄 {doc['nombre_original']} - {doc['categoria']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                col1.metric("ID", f"#{doc['id']:04d}")
                col2.metric("Confianza", f"{doc['confianza']*100:.1f}%")
                col3.metric("Tamaño", f"{doc['tamaño_kb']} KB")
                st.caption(f"📅 Subido: {doc['fecha_subida']}")
                st.text_area("Extracto", doc["texto_extraido"][:200] + "...", height=100, disabled=True)
    else:
        st.info("📭 No hay documentos recientes")


# ====================================
# PÁGINA: SUBIR DOCUMENTOS
# ====================================

elif pagina == "📤 Subir Documentos":
    st.markdown('<h1 class="main-header">📤 Subir y Procesar Documentos</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📁 Archivo Individual", "📂 Carga Múltiple"])
    
    # ========== TAB 1: Individual ==========
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Selecciona un documento",
                type=['pdf', 'jpg', 'png', 'jpeg'],
                help="Formatos soportados: PDF, JPG, PNG (Max 200MB)"
            )
        
        with col2:
            st.markdown("### 🎯 Proceso Automático")
            st.markdown("""
            1. **📄 Carga** del archivo
            2. **🔍 Extracción** OCR
            3. **🤖 Clasificación** IA
            4. **💾 Almacenamiento**
            """)
        
        if uploaded_file:
            st.success(f"✅ Archivo cargado: **{uploaded_file.name}**")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("📊 Tamaño", f"{uploaded_file.size / 1024:.2f} KB")
            col2.metric("📄 Tipo", uploaded_file.type.split('/')[-1].upper())
            col3.metric("🆔 ID Asignado", f"#{stats['total_documentos'] + 1:04d}")
            
            st.markdown("---")
            
            if st.button("🚀 Procesar Documento", type="primary", use_container_width=True):
                # Barra de progreso
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Paso 1: Guardar temporalmente
                status_text.text("📁 Guardando archivo temporal...")
                progress_bar.progress(20)
                time.sleep(0.5)
                
                temp_path = TEMP_DIR / uploaded_file.name
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Paso 2: Extraer texto
                status_text.text("🔍 Extrayendo texto con OCR...")
                progress_bar.progress(40)
                time.sleep(0.8)
                
                if uploaded_file.type == "application/pdf":
                    texto_extraido = extract_text_from_pdf(temp_path)
                else:
                    texto_extraido = extract_text_from_image(temp_path)
                
                # Paso 3: Clasificar
                status_text.text("🤖 Clasificando con IA (Zero-Shot Learning)...")
                progress_bar.progress(60)
                time.sleep(1.0)
                
                categoria, confianza = clasificar_documento_inteligente(texto_extraido, uploaded_file.name)
                
                # Paso 4: Guardar
                status_text.text("💾 Guardando en el sistema...")
                progress_bar.progress(80)
                time.sleep(0.5)
                
                success, doc_id, mensaje = save_document(uploaded_file, texto_extraido, categoria, confianza)
                
                progress_bar.progress(100)
                status_text.empty()
                
                if success:
                    st.balloons()
                    st.markdown(f"""
                    <div class="success-box">
                        <h3>✅ ¡Documento Procesado Exitosamente!</h3>
                        <p><strong>ID del Documento:</strong> #{doc_id:04d}</p>
                        <p><strong>Categoría Detectada:</strong> {categoria}</p>
                        <p><strong>Nivel de Confianza:</strong> {confianza*100:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Mostrar resultados
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📋 Texto Extraído (Primeros 500 caracteres)")
                        st.text_area("", texto_extraido[:500], height=200, disabled=True, label_visibility="collapsed")
                    
                    with col2:
                        st.subheader("🎯 Análisis de Clasificación")
                        st.progress(confianza, text=f"Confianza: {confianza*100:.1f}%")
                        
                        st.markdown(f"""
                        **Categoría Asignada:** {categoria}
                        
                        **¿Por qué esta categoría?**  
                        El sistema analizó el contenido del documento y detectó palabras clave 
                        asociadas con documentos de tipo "{categoria}".
                        """)
                else:
                    st.error(mensaje)
    
    # ========== TAB 2: Múltiple ==========
    with tab2:
        uploaded_files = st.file_uploader(
            "Selecciona múltiples documentos",
            type=['pdf', 'jpg', 'png', 'jpeg'],
            accept_multiple_files=True,
            help="Puedes seleccionar varios archivos a la vez"
        )
        
        if uploaded_files:
            st.info(f"📊 **{len(uploaded_files)} archivos seleccionados**")
            
            # Mostrar lista de archivos
            for i, file in enumerate(uploaded_files, 1):
                st.write(f"{i}. 📄 {file.name} ({file.size / 1024:.2f} KB)")
            
            st.markdown("---")
            
            if st.button("🚀 Procesar Todos los Documentos", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                procesados = 0
                errores = 0
                
                for i, file in enumerate(uploaded_files):
                    status_text.text(f"⚙️ Procesando {i+1}/{len(uploaded_files)}: {file.name}")
                    
                    # Guardar temporal
                    temp_path = TEMP_DIR / file.name
                    with open(temp_path, "wb") as f:
                        f.write(file.getbuffer())
                    
                    # Extraer texto
                    if file.type == "application/pdf":
                        texto = extract_text_from_pdf(temp_path)
                    else:
                        texto = extract_text_from_image(temp_path)
                    
                    # Clasificar
                    categoria, confianza = clasificar_documento_inteligente(texto, file.name)
                    
                    # Guardar
                    success, doc_id, mensaje = save_document(file, texto, categoria, confianza)
                    
                    if success:
                        procesados += 1
                    else:
                        errores += 1
                    
                    progress_bar.progress((i + 1) / len(uploaded_files))
                    time.sleep(0.3)
                
                status_text.empty()
                progress_bar.empty()
                
                st.success(f"✅ Procesamiento completado: {procesados} exitosos, {errores} errores")
                st.balloons()


# ====================================
# PÁGINA: BÚSQUEDA INTELIGENTE
# ====================================

elif pagina == "🔍 Búsqueda Inteligente":
    st.markdown('<h1 class="main-header">🔍 Búsqueda Inteligente con IA</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🤖 Busca en lenguaje natural
    
    El sistema de IA interpretará tu consulta y buscará los documentos más relevantes.
    
    **Ejemplos de consultas:**
    - *"Busca todos los contratos del 2024"*
    - *"Documentos legales sobre propiedad intelectual"*
    - *"Certificados subidos en marzo"*
    - *"Facturas de Epic Games"*
    """)
    
    st.markdown("---")
    
    # Input de búsqueda
    consulta = st.text_input(
        "🔍 Escribe tu consulta:",
        placeholder="Ej: Busca certificados del 2025",
        help="Usa lenguaje natural, la IA interpretará automáticamente",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        buscar_btn = st.button("🚀 Buscar con IA", type="primary", use_container_width=True)
    with col2:
        buscar_simple_btn = st.button("🔎 Búsqueda Simple", use_container_width=True)
    with col3:
        if st.button("🔄 Limpiar", use_container_width=True):
            st.rerun()
    
    # ========== BÚSQUEDA CON IA ==========
    if buscar_btn and consulta:
        with st.spinner("🤖 La IA está analizando tu consulta..."):
            time.sleep(1.2)
            parametros, resultados = buscar_documentos_ia(consulta)
        
        st.markdown("---")
        
        # Mostrar interpretación de la IA
        st.success(f"🤖 **La IA entendió:** {parametros['explicacion']}")
        
        with st.expander("🔧 Ver parámetros de búsqueda detectados"):
            col1, col2 = st.columns(2)
            with col1:
                st.json({
                    "Categoría": parametros["categoria"] or "Todas",
                    "Palabras clave": parametros["palabras_clave"][:5],
                })
            with col2:
                st.json({
                    "Fecha desde": parametros["fecha_desde"] or "Sin límite",
                    "Fecha hasta": parametros["fecha_hasta"] or "Sin límite",
                    "Extensión": parametros["extension"] or "Todas"
                })
        
        st.markdown("---")
        
        # Mostrar resultados
        if resultados:
            st.subheader(f"📊 Se encontraron {len(resultados)} documentos")
            
            for doc in resultados:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    
                    with col1:
                        st.markdown(f"**📄 {doc['nombre_original']}**")
                        st.caption(f"ID: #{doc['id']:04d}")
                    
                    with col2:
                        st.markdown(f"📂 {doc['categoria']}")
                        st.progress(doc['confianza'], text=f"{doc['confianza']*100:.1f}% confianza")
                    
                    with col3:
                        st.markdown(f"📅 {doc['fecha_subida'][:10]}")
                        st.caption(f"Tamaño: {doc['tamaño_kb']} KB")
                    
                    with col4:
                        if st.button("👁️", key=f"ver_{doc['id']}", help="Ver detalles"):
                            st.session_state[f"show_{doc['id']}"] = True
                    
                    # Detalles expandibles
                    if st.session_state.get(f"show_{doc['id']}", False):
                        st.markdown(f"""
                        **📋 Extracto del documento:**
                        
                        {doc['texto_extraido']}
                        
                        **📁 Ruta:** `{doc['ruta']}`
                        """)
                    
                    st.markdown("---")
        else:
            st.warning("😕 No se encontraron documentos que coincidan con tu búsqueda")
    
    # ========== BÚSQUEDA SIMPLE ==========
    elif buscar_simple_btn and consulta:
        resultados = search_documents(consulta)
        
        if resultados:
            st.success(f"✅ Se encontraron {len(resultados)} documentos")
            
            for doc in resultados:
                with st.expander(f"📄 {doc['nombre_original']} - Relevancia: {doc['relevancia']}⭐"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Categoría", doc["categoria"])
                        st.metric("Confianza", f"{doc['confianza']*100:.1f}%")
                    
                    with col2:
                        st.metric("Fecha", doc["fecha_subida"][:10])
                        st.metric("Tamaño", f"{doc['tamaño_kb']} KB")
                    
                    st.text_area("Extracto", doc["texto_extraido"], height=150, disabled=True)
        else:
            st.warning("😕 No se encontraron documentos")


# ====================================
# PÁGINA: ANÁLISIS Y REPORTES
# ====================================

elif pagina == "📊 Análisis y Reportes":
    st.markdown('<h1 class="main-header">📊 Análisis y Reportes del Sistema</h1>', unsafe_allow_html=True)
    
    docs = get_all_documents()
    
    if not docs:
        st.info("📭 No hay documentos para analizar. ¡Sube algunos documentos primero!")
    else:
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📄 Total Documentos", len(docs))
        
        with col2:
            st.metric("📂 Categorías Únicas", len(set(d["categoria"] for d in docs)))
        
        with col3:
            tamaño_total = sum(d["tamaño_kb"] for d in docs) / 1024
            st.metric("💾 Espacio Total", f"{tamaño_total:.2f} MB")
        
        with col4:
            confianza_avg = sum(d["confianza"] for d in docs) / len(docs) * 100
            st.metric("🎯 Precisión Promedio", f"{confianza_avg:.1f}%")
        
        st.markdown("---")
        
        # Gráficos avanzados
        tab1, tab2, tab3 = st.tabs(["📊 Categorías", "📈 Timeline", "🎯 Confianza"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Distribución por Categorías")
                df_cat = pd.DataFrame([(d["categoria"], d["tamaño_kb"]) for d in docs], 
                                     columns=["Categoría", "Tamaño KB"])
                cat_counts = df_cat["Categoría"].value_counts()
                fig = px.pie(values=cat_counts.values, names=cat_counts.index,
                           title="Documentos por Categoría")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Tamaño por Categoría")
                cat_size = df_cat.groupby("Categoría")["Tamaño KB"].sum().sort_values(ascending=True)
                fig = px.bar(x=cat_size.values, y=cat_size.index, orientation='h',
                           title="Espacio usado por categoría")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("📅 Línea de Tiempo de Documentos")
            df_time = pd.DataFrame([(d["fecha_subida"][:10], 1) for d in docs],
                                  columns=["Fecha", "Cantidad"])
            df_time = df_time.groupby("Fecha").count().reset_index()
            fig = px.line(df_time, x="Fecha", y="Cantidad", 
                         title="Documentos subidos por día",
                         markers=True)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("🎯 Distribución de Confianza IA")
            confianzas = [d["confianza"] * 100 for d in docs]
            fig = go.Figure(data=[go.Histogram(x=confianzas, nbinsx=20)])
            fig.update_layout(title="Histograma de Niveles de Confianza",
                            xaxis_title="Confianza (%)",
                            yaxis_title="Cantidad de Documentos")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Tabla de todos los documentos
        st.subheader("📋 Listado Completo de Documentos")
        
        df = pd.DataFrame([{
            "ID": f"#{d['id']:04d}",
            "Nombre": d["nombre_original"],
            "Categoría": d["categoria"],
            "Confianza": f"{d['confianza']*100:.1f}%",
            "Fecha": d["fecha_subida"][:10],
            "Tamaño (KB)": d["tamaño_kb"]
        } for d in docs])
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Exportar reporte
        st.markdown("---")
        if st.button("📥 Exportar Reporte Completo (JSON)", use_container_width=True):
            import json
            reporte = {
                "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "estadisticas": stats,
                "documentos": docs
            }
            
            st.download_button(
                label="⬇️ Descargar reporte.json",
                data=json.dumps(reporte, indent=2, ensure_ascii=False),
                file_name=f"reporte_doc_finder_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )