
#this is the data base of students for the project:

import os
import pandas as pd
from datetime import datetime
from Colors import Colors
import unicodedata

# Resolve the Excel file relative to this script's directory so the file
# is found when running commands from any working directory.
ARCHIVO_EXCEL = os.path.join(os.path.dirname(__file__),
                            "Copy of modelo_tidy_estudiantes_actualizado.xlsx")
HOJA = "Sheet1"  # Aqui va el nombre de la hoja

def leer_datos() -> pd.DataFrame:
    """Lee todos los datos desde Excel."""
    columnas = ["id_estudiante", "nombre_estudiante", "id_profesor",
                "aula", "area", "asignatura", "nota", "fecha"]
    try:
        print(f"ℹ️ Leyendo datos desde: {ARCHIVO_EXCEL} (hoja: {HOJA})")
        df = pd.read_excel(ARCHIVO_EXCEL, sheet_name=HOJA)
    except FileNotFoundError:
        print("📁 Archivo no encontrado, creando uno nuevo...")
        df = pd.DataFrame(columns=columnas)
    except ValueError:
        print(f"⚠️ La hoja '{HOJA}' no existe, se creará una nueva hoja.")
        df = pd.DataFrame(columns=columnas)
    return df

def guardar_datos(df: pd.DataFrame):
    """Guarda los datos en el Excel."""
    df.to_excel(ARCHIVO_EXCEL, sheet_name=HOJA, index=False)

#Funcion para quitar acentos al momento de buscar estudiantes
def quitar_acentos(texto):
    if not isinstance(texto, str):
        return texto
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# Temporal database for testing
# students_data = {
#     'ID': [1, 2, 3, 4],
#     'Name': ['Ana', 'Luis', 'Maria', 'Carlos'],
#     'Age': [25, 30, 28, 35],
#     'Score': [89, 71, 91, 85]
# }

#df = pd.DataFrame(students_data)


def get_student_by_id(df, id_estudiante):
    """Find student by ID"""
    try:
        id_estudiante = int(id_estudiante)
        estudiante = df[df['id_estudiante'] == id_estudiante]

        if not estudiante.empty:
            return estudiante
        else:
            print(f"❌ No se encontró estudiante con ID {id_estudiante}")
            return None
    except ValueError:
        print("❌ ID debe ser un número válido")
        return None


def add_student(df, nombre_estudiante, id_profesor, aula, area, asignatura, nota):
    """Add new student to database"""

    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    try:
        id_profesor = int(id_profesor)
        nota = float(nota)
        
        # Get next available ID
        next_id = int(df['id_estudiante'].max() + 1) if not df.empty else 1
        
        new_student = pd.DataFrame({
            'id_estudiante': [next_id],
            'nombre_estudiante': [nombre_estudiante],
            'id_profesor': [id_profesor],
            'aula': [aula],
            'area': [area],
            'asignatura': [asignatura],
            'nota': [nota],
            'fecha': [fecha_actual]
        })

        df = pd.concat([df, new_student], ignore_index=True)
        guardar_datos(df)
        print(f"✅ Estudiante {nombre_estudiante} agregado correctamente con ID {next_id}")
        return df
        
    except ValueError:
        print("❌ Error: el ID del profesor debe ser numérico y la nota un número válido.")
        return None


def delete_student(df, id_estudiante):
    """Delete student by ID"""
    try:
        id_estudiante = int(id_estudiante)
        if id_estudiante in df['id_estudiante'].values:
            student_name = df[df['id_estudiante'] == id_estudiante]['nombre_estudiante'].iloc[0]
            df = df[df['id_estudiante'] != id_estudiante].reset_index(drop=True)
            guardar_datos(df)

            print(f"✅ Estudiante '{student_name}' (ID: {id_estudiante}) eliminado correctamente.")
            return df
        else:
            print(f"❌ No se encontró estudiante con ID {id_estudiante}.")
            return df
    except ValueError:
        print("❌ ID debe ser un número válido.")
        return df


def list_all_students(df):
    """Display all students in a formatted way"""
    if df.empty:
        print("❌ No hay estudiantes registrados")
        return
    
    print("\n📋 LISTA DE ESTUDIANTES:")
    print("=" * 50)
    for _, student in df.iterrows():
        print(f"🆔 ID Estudiante: {student.get('id_estudiante', 'N/A')}")
        print(f"👤 Nombre: {student.get('nombre_estudiante', 'N/A')}")
        print(f"🏫 Área: {student.get('area', 'N/A')}")
        print(f"📘 Asignatura: {student.get('asignatura', 'N/A')}")
        print(f"🧮 Nota: {student.get('nota', 'N/A')}")
        print(f"👨‍🏫 ID Profesor: {student.get('id_profesor', 'No asignado')}")
        print("=" * 50)



def get_database_stats(df):
    """Obtiene estadísticas generales de la base de datos."""

    if df.empty:
        print("❌ No hay estudiantes registrados.")
        return None
    
    try:
        promedio = round(df['nota'].mean(), 2)
        mayor = df['nota'].max()
        menor = df['nota'].min()
        total = df['id_estudiante'].nunique()


        return {
            'total_students': total,
            'average_score': promedio,
            'highest_score': mayor,
            'lowest_score': menor
        }

    except Exception as e:
        print(f"⚠️ Error al calcular estadísticas: {e}")
        return None


def update_student(df, id_estudiante, campo, nuevo_valor):
    """Actualiza un campo de un estudiante por su ID."""
    if id_estudiante in df['id_estudiante'].values:
        df.loc[df['id_estudiante'] == id_estudiante, campo] = nuevo_valor
        guardar_datos(df)
        print(f"✅ Estudiante ID {id_estudiante} actualizado: {campo} -> {nuevo_valor}")
        return df
    else:
        print(f"❌ No se encontró estudiante con ID {id_estudiante}")
        return df

def get_students_by_area(df, area):
    area_normalizada = quitar_acentos(area.lower())
    return df[df['area'].apply(lambda x: quitar_acentos(str(x).lower()) == area_normalizada)]

def get_students_by_subject(df, asignatura):
    asignatura_normalizada = quitar_acentos(asignatura.lower())
    return df[df['asignatura'].apply(lambda x: quitar_acentos(str(x).lower()) == asignatura_normalizada)]

def predict_student_score(df, id_estudiante, nueva_nota):
    student_notes = df[df['id_estudiante'] == id_estudiante]['nota'].tolist()
    if not student_notes:
        print("❌ Estudiante no encontrado")
        return None
    student_notes.append(float(nueva_nota))
    prediccion = sum(student_notes) / len(student_notes)
    print(f"📊 Predicción de nota promedio con nueva nota {nueva_nota}: {round(prediccion, 2)}")
    return prediccion

def students_at_risk(df, umbral):
    promedios = df.groupby('id_estudiante')['nota'].mean()
    riesgo = promedios[promedios < umbral].index.tolist()
    if not riesgo:
        print("✅ Ningún estudiante está en riesgo")
    else:
        print(f"⚠️ Estudiantes en riesgo (promedio < {umbral}): ")
        df_riesgo = df[df['id_estudiante'].isin(riesgo)][['id_estudiante', 'nombre_estudiante']].drop_duplicates()
        for _, row in df_riesgo.iterrows():
            print(f"🆔 ID: {row['id_estudiante']} - 👤 Nombre: {row['nombre_estudiante']}")
    return riesgo

def average_by_subject(df, asignatura):
    notas = df[df['asignatura'] == asignatura]['nota']
    if notas.empty:
        print("❌ No hay notas registradas para esa asignatura")
        return None
    return round(notas.mean(), 2)

def average_by_area(df, area):
    notas = df[df['area'] == area]['nota']
    if notas.empty:
        print("❌ No hay notas registradas para esa área")
        return None
    return round(notas.mean(), 2)


