# 🎓 Sistema Inteligente de Calificaciones Estudiantiles

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-orange.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-green.svg)
![Status](https://img.shields.io/badge/Status-Activo-success.svg)

Un Sistema Inteligente de Evaluación y Orientación Académica.

## 🌟 Características Principales

### 📊 Gestión de Estudiantes
- **Agregar nuevos estudiantes** con información completa
- **Modificar datos** existentes de estudiantes
- **Eliminar estudiantes** del sistema
- **Búsqueda por ID** para acceso rápido
- **Listado completo** de todos los estudiantes registrados

### 📈 Análisis y Predicción
- **Predicción de calificaciones** basada en histórico
- **Identificación de estudiantes en riesgo** académico
- **Estadísticas generales** del sistema
- **Promedios por área y asignatura**
- **Análisis comparativo** de rendimiento

### 🎨 Visualización Avanzada
- **Gráfico de Radar de Habilidades** - Visualización individual por áreas
- **Dashboard Completo** - Vista integral con múltiples subgráficos
- **Transformación automática** de escalas (0-100 a 0-10)
- **Interfaz intuitiva** con colores y formato mejorado

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
# Clonar el repositorio
git clone https://github.com/BreakingCode-Sic/SistemadeEvaluacionPrediccionEstudiantil.git
cd sistema-calificaciones
git checkout release

# Instalar dependencias
pip install pandas matplotlib numpy openpyxl
```

### Estructura del Proyecto
```
sistema-calificaciones/
│
├── main.py                 # Programa principal
├── Menu_functions.py       # Funciones del menú y lógica
├── students.py             # Gestión de datos estudiantiles
├── Colors.py               # Configuración de colores para terminal
├── Copy of modelo_tidy_estudiantes_actualizado.xlsx  # Base de datos
└── README.md               # Este archivo
```

## 🎯 Uso del Sistema

### Menú Principal
El sistema ofrece un menú interactivo con las siguientes opciones:

| Opción | Icono | Descripción |
|--------|-------|-------------|
| **1** | 🔍 | Seleccionar estudiante por ID |
| **2** | ➕ | Agregar nuevo estudiante |
| **3** | 🗑️ | Eliminar estudiante |
| **4** | ✏️ | Modificar datos de estudiante |
| **5** | 📃 | Listar todos los estudiantes |
| **6** | 🔮 | Predecir calificaciones y posibles fortalezas |
| **7** | 📊 | Ver estadísticas generales |
| **8** | 📈 | Gráfico de habilidades del estudiante |
| **9** | 🎯 | Dashboard completo del estudiante |
| **0** | 🚪 | Salir del sistema |

### Funcionalidades Detalladas

#### 📈 Gráfico de Habilidades (Opción 8)
- Visualización en formato radar de las competencias por área
- Promedios calculados automáticamente
- Diseño limpio y profesional
- Escala adaptativa 0-10

#### 🎯 Dashboard Completo (Opción 9)
- Vista principal de áreas académicas
- Subgráficos por campo específico:
  - Historia
  - Matemáticas
  - Ciencias
  - Tecnología
  - Lenguas
  - Educación Física
- Estadísticas detalladas del estudiante

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+** - Lenguaje de programación principal
- **Pandas** - Manipulación y análisis de datos
- **Matplotlib** - Visualización de datos y gráficos
- **NumPy** - Cálculos numéricos y matemáticos
- **OpenPyXL** - Manejo de archivos Excel

## 📋 Funciones Principales

### Gestión de Datos (`students.py`)
- `leer_datos()` - Carga datos desde Excel
- `guardar_datos()` - Guarda cambios en Excel
- `get_student_by_id()` - Búsqueda por ID
- `add_student()` - Agregar nuevo estudiante
- `update_student()` - Modificar datos existentes

### Visualización (`Menu_functions.py`)
- `chart()` - Gráfico de radar básico
- `plot_student_skills()` - Visualización individual
- `plot_student_dashboard()` - Dashboard completo
- `student_grade_chat()` - Gráficos múltiples
- `segmentacion()` - Cálculo de ángulos para radar

### Análisis (`Menu_functions.py`)
- `predict_student_score()` - Predicción de notas
- `students_at_risk()` - Identificación de riesgo
- `get_database_stats()` - Estadísticas generales
- `average_by_area()` - Promedios por área
- `average_by_subject()` - Promedios por asignatura

## 🎨 Personalización

### Colores de la Interfaz
El sistema utiliza la clase `Colors` para una interfaz colorida:

```python
# Ejemplo de uso
print(f"{Colors.GREEN}✅ Operación exitosa{Colors.ENDC}")
print(f"{Colors.RED}❌ Error detectado{Colors.ENDC}")
print(f"{Colors.CYAN}📊 Mostrando estadísticas{Colors.ENDC}")
```


## 🔧 Solución de Problemas

### Error: "No se puede importar matplotlib"
```bash
pip install matplotlib
```

### Error: "Archivo Excel no encontrado"
- Verificar que el archivo esté en la ruta correcta
- Confirmar que el nombre del archivo coincida
- Revisar permisos de lectura/escritura

### Error: "Estudiante no encontrado"
- Verificar que el ID exista en el sistema
- Usar la opción 5 para listar todos los estudiantes
- Confirmar que no haya espacios en blanco en el ID

## 📈 Ejemplos de Uso

### Agregar un nuevo estudiante
```
👤 Nombre del estudiante: María González
👨‍🏫 ID del profesor: 105
🏫 Aula: Aula 2
📚 Área: Ciencias
📖 Asignatura: Biología
📝 Nota: 85
```

### Generar dashboard completo
```
🆔 Ingrese el ID del estudiante para el dashboard completo: 3
📊 Generando dashboard completo para: Ana Pérez (ID: 3)
✅ Se crearon 7/7 gráficos correctamente
```
Admin- Rushaner Minaya
Miembro- Cristian Beltre
Miembro- Francis Céspedes
Miembro- Anderson Frias
Miembro- Wilnel Pérez

## 👥 Autores

- **Rushaner Minaya** - [RushanerM](https://github.com/RushanerM)
- **Cristian Beltree** - [p0lquer](https://github.com/p0lquer)
- **Francis Céspedes** - [Francis-Manuel374](https://github.com/Francis-Manuel374)
- **Anderson Frias** - [anderj14](https://github.com/anderj14)
- **Wilnel Pérez** - 

## 🙏 Agradecimientos
Este proyecto fue desarrollado como parte del programa **Samsung Innovation Campus**, cuyo apoyo y recursos fueron fundamentales para la realización de este sistema de gestión académica.

**Agradecimientos especiales a:**
- **Samsung Innovation Campus** - Por la oportunidad de aprendizaje y desarrollo
- **Instructores y mentores del programa** - Por su guía y conocimientos compartidos
- **Compañeros del programa** - Por el intercambio de ideas y colaboración

**⭐ Proyecto desarrollado en el marco de Samsung Innovation Campus**
---

**¿Preguntas o problemas?** Abre un [issue](https://github.com/BreakingCode-Sic/SistemadeEvaluacionPrediccionEstudiantil/issues) en GitHub.

**¿Te gustó el proyecto?** ¡Dale una ⭐ en GitHub!
