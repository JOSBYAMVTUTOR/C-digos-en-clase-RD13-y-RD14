#  RetentIA: Predicción Proactiva de Fuga de Clientes


##  Resumen 
**RetentIA** es un modelo de Machine Learning diseñado para el sector bancario que predice qué clientes están en riesgo de abandonar la entidad (Churn). A diferencia de los enfoques tradicionales reactivos, RetentIA permite actuar de forma **proactiva** e integra **Explainable AI** para entender no solo *quién* se va, sino *por qué*, garantizando decisiones transparentes y libres de sesgos.

---

##Equipo

| Integrante | Rol | Funciones Principales |
| :--- | :--- | :--- |
| **José Cohn** 
| **Anderson Ellian Reyes** 
| **Claiby** | Data Scientist 
| **Gerald Ogando Encarnación** 
| **Luis Roberto Medina** 

---

##  Planteamiento del Problema
La pérdida de clientes (Churn) es uno de los problemas más costosos en la banca.
* **El Dato:** Adquirir un nuevo cliente cuesta hasta **5 veces más** que retener a uno existente.
* **El Dolor:** Los bancos suelen reaccionar demasiado tarde, cuando el cliente ya ha cerrado su cuenta, perdiendo ingresos recurrentes.

##  Objetivos y Solución
Nuestro objetivo es cambiar la estrategia de **Reactiva a Proactiva**.

### La Solución Técnica
Implementamos un ensamble de modelos (**Random Forest**, **XGBoost**, **LightGBM**) entrenado con datos históricos bancarios.
1.  **Detección:** Identifica patrones de comportamiento invisibles al ojo humano.
2.  **Transparencia:** Utilizamos técnicas de "Feature Importance" y librerías de **XAI (SHAP, LIME)** para mitigar sesgos y entender las causas raíz.
3.  **Acción:** Permite al banco dirigir su presupuesto de fidelización eficientemente solo a clientes de "Alto Riesgo".

---

##  Herramientas y Tecnologías (Tech Stack)

El proyecto utiliza un stack robusto de Python para Ciencia de Datos y MLOps:

* **Lenguaje:** Python 3.x
* **Procesamiento y Análisis:** `Pandas`, `Numpy`, `Pandas Profiling` (Reportes automáticos).
* **Visualización:** `Matplotlib`, `Seaborn`.
* **Machine Learning:**
    * `Scikit-Learn` (Preprocesamiento, Pipelines, Random Forest).
    * `XGBoost` y `LightGBM` (Modelos de Boosting para alto rendimiento).
    * `Optuna` (Optimización de hiperparámetros).
* **Explainable AI (XAI):** `SHAP`, `LIME` (Para interpretar las predicciones).
* **Despliegue y Demo Web:** `Streamlit`, `FastAPI`, `Uvicorn`, `Pyngrok` (Túnel para exponer la app).

---

##  Instalación y Ejecución

### 1. Prerrequisitos
Asegúrate de tener Python instalado y el archivo de datos `Churn_Modelling.csv` en el directorio raíz.

### 2. Instalación de Dependencias
Ejecuta el siguiente comando para instalar todas las librerías necesarias:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost lightgbm shap lime optuna fastapi uvicorn pyngrok streamlit pandas-profiling openpyxl
