from Colors import Colors
import os
from students import *
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

  
def get_user_input(choice, df):
    """Process user choice using match statement"""
    
    match choice:
        case '1':    
            print_info_message("Seleccionar estudiante por ID")
            student_id = input(f"{Colors.CYAN}🆔 Ingrese el ID del estudiante: {Colors.ENDC}")
            student = get_student_by_id(df, student_id)
            if student is not None:
                print(f"\n✅ Estudiante encontrado:")
                print(student.to_string(index=False))
            wait_for_enter()
            return df, 1
            
        case '2':
            print_info_message("Agregar nuevo estudiante")
            try:
                nombre_estudiante = input(f"{Colors.CYAN}👤 Nombre del estudiante: {Colors.ENDC}")
                id_profesor = input(f"{Colors.CYAN}👨‍🏫 ID del profesor: {Colors.ENDC}")
                aula = input(f"{Colors.CYAN}🏫 Aula: {Colors.ENDC}")
                area = input(f"{Colors.CYAN}📚 Área (Ciencias, Matemáticas, etc.): {Colors.ENDC}")
                asignatura = input(f"{Colors.CYAN}📖 Asignatura: {Colors.ENDC}")
                nota = input(f"{Colors.CYAN}📝 Nota: {Colors.ENDC}")
                df = add_student(df, nombre_estudiante, id_profesor, aula, area, asignatura, nota)
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}⚠️ Operación cancelada{Colors.ENDC}")
            wait_for_enter()
            return df, 2
            
        case '3':
            print_info_message("Eliminar estudiante")
            # First show all students
            list_all_students(df)
            student_id = input(f"{Colors.CYAN}🆔 Ingrese el ID del estudiante a eliminar: {Colors.ENDC}")
            df = delete_student(df, student_id)
            wait_for_enter()
            return df, 3
            
        case '4':
            print_info_message("Modificar estudiante")
            try:
                # Mostrar todos los estudiantes primero
                list_all_students(df)
                
                # Pedir ID del estudiante a modificar
                student_id = input(f"{Colors.CYAN}🆔 Ingrese el ID del estudiante a modificar: {Colors.ENDC}")
                student = get_student_by_id(df, student_id)
                
                if student is None:
                    wait_for_enter()
                    return df, 4
                
                # Mostrar campos disponibles para modificar
                campos = ['nombre_estudiante', 'id_profesor', 'aula', 'area', 'asignatura', 'nota']
                print("\nCampos disponibles para modificar:")
                for i, campo in enumerate(campos, start=1):
                    print(f"{i}. {campo}")
                
                # Seleccionar campo
                opcion = input(f"{Colors.CYAN}Ingrese el número del campo a modificar: {Colors.ENDC}")
                if not opcion.isdigit() or int(opcion) not in range(1, len(campos)+1):
                    print("❌ Opción inválida")
                    wait_for_enter()
                    return df, 4
                
                campo_seleccionado = campos[int(opcion)-1]
                
                # Nuevo valor
                nuevo_valor = input(f"{Colors.CYAN}Ingrese el nuevo valor para {campo_seleccionado}: {Colors.ENDC}")
                
                # Validar tipo si es numérico
                if campo_seleccionado in ['id_profesor', 'nota']:
                    try:
                        nuevo_valor = float(nuevo_valor) if campo_seleccionado == 'nota' else int(nuevo_valor)
                    except ValueError:
                        print("❌ Valor inválido para el campo seleccionado")
                        wait_for_enter()
                        return df, 4
                
                # Llamar a la función de actualización
                df = update_student(df, int(student_id), campo_seleccionado, nuevo_valor)
        
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}⚠️ Operación cancelada{Colors.ENDC}")

            wait_for_enter()
            return df, 4
            
        case '5':
            # print_info_message("Listar estudiantes")
            try:
                if df.empty:
                    print(f"{Colors.YELLOW}❌ No hay estudiantes registrados{Colors.ENDC}")
                else:
                    #dentro de esta opcion estara un mini menu con las sigientes opciones (5,8,9,10)
                    while True:
                        print("[1] Ver todos los estudiantes")
                        print("[2] Ver estudiantes por area")
                        print("[3] Ver estudiantes por asignatura")
                        print("[4] Ver Estudiantes en riego")
                        print("[0] Volver al menú principal")

                        sub_choice = input(f"{Colors.CYAN}Seleccione una opción (0-4): {Colors.ENDC}")
                    
                        if sub_choice == '0':
                            # Volver al menú principal: salir del submenu
                            break
                        elif sub_choice == '1':
                            print_info_message("Listar todos los estudiantes")
                            list_all_students(df)
                            wait_for_enter()
                        elif sub_choice == '2':
                            print_info_message("Ver estudiantes por área")
                            area_input = input(f"{Colors.CYAN}📚 Ingrese el área: {Colors.ENDC}")
                            estudiantes = get_students_by_area(df, area_input)
                            if estudiantes.empty:
                                print(f"❌ No hay estudiantes en el área {area_input}")
                            else:
                                print(f"\n📋 Estudiantes en el área {area_input}:")
                                print(estudiantes.to_string(index=False))
                            wait_for_enter()
                        elif sub_choice == '3':
                             print_info_message("Ver estudiantes por asignatura")
                             subject_input = input(f"{Colors.CYAN}📖 Ingrese la asignatura: {Colors.ENDC}")
                             estudiantes = get_students_by_subject(df, subject_input)
                             if estudiantes.empty:
                                print(f"❌ No hay estudiantes en la asignatura {subject_input}")
                             else:
                                print(f"\n📋 Estudiantes en la asignatura {subject_input}:")
                                print(estudiantes.to_string(index=False))
                             wait_for_enter()
                        elif sub_choice == '4':
                            print_info_message("Ver Estudiantes en riesgo")
                            try:
                                umbral_input = input(f"{Colors.CYAN}⚠️ Ingrese el umbral de riesgo (por defecto 60): {Colors.ENDC}")
                                umbral = float(umbral_input) if umbral_input.strip() != "" else 60
                            except ValueError:
                                print("❌ Valor inválido, se usará el umbral por defecto (60)")
                                umbral = 60
                            riesgo = students_at_risk(df, umbral)
                            if riesgo:
                                print(f"📝 IDs de estudiantes en riesgo: {riesgo}")
                            wait_for_enter()
                        elif sub_choice != '0' and sub_choice != '1' and sub_choice != '2' and sub_choice != '3' and sub_choice != '4':
                            print("❌ Opción inválida, por favor seleccione una opción del 0 al 4.")    
                    
                    # fin while

            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}⚠️ Operación cancelada{Colors.ENDC}")
            # Al salir del submenu volver al menú principal
            return df, 5
            
        #       case '8':
        #     print_info_message("Ver estudiantes por área")
        #     area_input = input(f"{Colors.CYAN}📚 Ingrese el área: {Colors.ENDC}")
        #     estudiantes = get_students_by_area(df, area_input)
            
        #     if estudiantes.empty:
        #         print(f"❌ No hay estudiantes en el área {area_input}")
        #     else:
        #         print(f"\n📋 Estudiantes en el área {area_input}:")
        #         print(estudiantes.to_string(index=False))
            
        #     wait_for_enter()
        #     return df, 8
        
        # case '9':
        #     print_info_message("Ver estudiantes por asignatura")
        #     subject_input = input(f"{Colors.CYAN}📖 Ingrese la asignatura: {Colors.ENDC}")
        #     estudiantes = get_students_by_subject(df, subject_input)
            
        #     if estudiantes.empty:
        #         print(f"❌ No hay estudiantes en la asignatura {subject_input}")
        #     else:
        #         print(f"\n📋 Estudiantes en la asignatura {subject_input}:")
        #         print(estudiantes.to_string(index=False))
            
        #     wait_for_enter()
        #     return df, 9
        
        # case '10':
        #     print_info_message("Estudiantes en riesgo")
            # try:
            #     umbral_input = input(f"{Colors.CYAN}⚠️ Ingrese el umbral de riesgo (por defecto 60): {Colors.ENDC}")
            #     umbral = float(umbral_input) if umbral_input.strip() != "" else 60
            # except ValueError:
            #     print("❌ Valor inválido, se usará el umbral por defecto (60)")
            #     umbral = 60
            # #Arreglo de la funcion students_at_risk (umbral estaba declarado 2 veces por defecto)
            # riesgo = students_at_risk(df, umbral)
            # if riesgo:
            #     print(f"📝 IDs de estudiantes en riesgo: {riesgo}")
            
        #     wait_for_enter()
        #     return df, 10
        #     return df, 5
            
        case '6':
            print_info_message("Predecir calificaciones")
            
            try:
                # Pedir ID del estudiante
                student_id = input(f"{Colors.CYAN}🆔 Ingrese el ID del estudiante para predecir su nota: {Colors.ENDC}")
                student = get_student_by_id(df, student_id)
                
                if student is None:
                    wait_for_enter()
                    return df, 6

                # Mostrar las notas actuales del estudiante
                notas_actuales = student['nota'].tolist()
                print(f"\n📊 Notas actuales del estudiante:")
                print(notas_actuales)

                # Preguntar si quiere simular una nueva nota
                nueva_nota_input = input(f"{Colors.CYAN}📝 Ingrese una nota hipotética para proyectar promedio (ENTER para omitir): {Colors.ENDC}")
                if nueva_nota_input.strip() != "":
                    try:
                        nueva_nota = float(nueva_nota_input)
                        # Llamar a la función de predicción
                        predict_student_score(df, int(student_id), nueva_nota)
                    except ValueError:
                        print("❌ Valor inválido, se ignorará la nota hipotética.")
                else:
                    print("⚠️ No se ingresó nota hipotética, mostrando promedio actual.")
                    promedio_actual = sum(notas_actuales) / len(notas_actuales)
                    print(f"📈 Promedio actual del estudiante: {round(promedio_actual, 2)}")
            
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}⚠️ Operación cancelada{Colors.ENDC}")

            wait_for_enter()
            return df, 6
            
        case '7':
            print_info_message("Ver estadísticas")
            stats = get_database_stats(df)
            if not stats:
                print(f"{Colors.YELLOW}❌ No hay estudiantes registrados{Colors.ENDC}")
                wait_for_enter()
                return df, 7

            # Estadísticas generales
            print("\n📊 ESTADÍSTICAS GENERALES:")
            print("=" * 40)
            print(f"👥 Total estudiantes: {Colors.CYAN}{stats['total_students']}{Colors.ENDC}")
            print(f"📊 Calificación promedio: {Colors.CYAN}{stats['average_score']:.2f}{Colors.ENDC}")
            print(f"🏆 Calificación más alta: {Colors.GREEN}{stats['highest_score']}{Colors.ENDC}")
            print(f"📉 Calificación más baja: {Colors.RED}{stats['lowest_score']}{Colors.ENDC}")
            print("=" * 40)

            # Estadísticas por área
            areas = df['area'].dropna().unique()
            print("\n📚 Promedio por área:")
            for area in areas:
                promedio_area = average_by_area(df, area)
                if promedio_area is not None:
                    print(f"📌 {area}: {Colors.CYAN}{promedio_area:.2f}{Colors.ENDC}")

            # Estadísticas por asignatura
            asignaturas = df['asignatura'].dropna().unique()
            print("\n📖 Promedio por asignatura:")
            for asignatura in asignaturas:
                promedio_asig = average_by_subject(df, asignatura)
                if promedio_asig is not None:
                    print(f"📌 {asignatura}: {Colors.CYAN}{promedio_asig:.2f}{Colors.ENDC}")
            
            wait_for_enter()
            return df, 7
        
        case '8':
            print_info_message("Gráfico de Habilidades del Estudiante")
            try:
                # Mostrar todos los estudiantes primero
                list_all_students(df)
                
                student_id = input(f"{Colors.CYAN}🆔 Ingrese el ID del estudiante para el gráfico: {Colors.ENDC}")
                df = plot_student_skills(df, student_id)
            
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}⚠️ Operación cancelada{Colors.ENDC}")

            wait_for_enter()
            return df, 8
        
        case '9':
            print_info_message("Dashboard Completo del Estudiante")
            try:
                # Mostrar todos los estudiantes primero
                list_all_students(df)
                
                student_id = input(f"{Colors.CYAN}🆔 Ingrese el ID del estudiante para el dashboard completo: {Colors.ENDC}")
                df = plot_student_dashboard(df, student_id)
            
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}⚠️ Operación cancelada{Colors.ENDC}")

            wait_for_enter()
            return df, 9

        case  '0':
            clear_screen()
            print_goodbye()
            print_success_message("Sistema cerrado correctamente")
            return df, 0  # Signal to exit
            
        case _:
            print_error_message("Opción no válida. Por favor, seleccione una opción del 0 al 7.")
            wait_for_enter()
            return df, -1  # Signal invalid option
    


def print_success_message(message):
    """ success message with green styling"""
    print(f"\n{Colors.GREEN}✅ {message}{Colors.ENDC}")

def print_error_message(message):
    """error message with red styling"""
    print(f"\n{Colors.RED}❌ {message}{Colors.ENDC}")


def print_info_message(message):
    """ info message with blue styling"""
    print(f"\n{Colors.BLUE}ℹ️  {message}{Colors.ENDC}")


def wait_for_enter():
    """Wait for user to press Enter"""
    input(f"\n{Colors.YELLOW}📱 Presione Enter para continuar...{Colors.ENDC}")

def print_goodbye():
    """Print a goodbye message"""
 
    goodbye = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                       ¡HASTA LUEGO! 👋                       ║
║                                                              ║
║          Gracias por usar el Sistema de Predicción           ║
║                    de Calificaciones                         ║
║                                                              ║
║                 ¡Que tengas un buen día!                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(goodbye)
    

def plot_student_skills(df, student_id):
    """Generate a radar chart of the student's skills using the chart function"""
    try:
        
        # # Search for student by ID to get name
        student = get_student_by_id(df, student_id)
        if student is None:
            print(f"❌ No se encontró estudiante con ID {student_id}")
            return df
        
        student_name = student['nombre_estudiante'].iloc[0]
        
        print(f"📊 Generando gráfico para: {student_name} (ID: {student_id})")
        
        # Call your existing chart function
        ax, errors = chart(df, student_name, 'area', 'nota', 'nombre_estudiante')
        
        # Check for errors
        if errors:
            for error in errors:
                print(f"❌ {error}")
            return df
        
        if ax is None:
            print("❌ No se pudo generar el gráfico")
            return df
        
        # Customize the chart
        plt.title(f'Habilidades del Estudiante: {student_name}\n(ID: {student_id})', 
                 size=16, y=1.08, fontweight='bold', color='darkblue')
        
        # Show additional information
        student_data = df[df['id_estudiante'] == int(student_id)]
        promedio_general = student_data['nota'].mean().round(2)
        
        # If the average is on a 0-100 scale, transform it
        if promedio_general > 10:
            promedio_general = promedio_general / 10
        
        # Add text with the average
        plt.figtext(0.5, 0.02, f'📈 Promedio General: {promedio_general}/10', 
                   ha='center', fontsize=12, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
        print(f"✅ Gráfico de habilidades generado exitosamente para {student_name}")
        return df
        
    except ImportError as e:
        print(f"❌ Error: No se pueden importar las librerías necesarias: {e}")
        print("💡 Asegúrate de tener matplotlib instalado: pip install matplotlib")
        return df
    except Exception as e:
        print(f"❌ Error al generar el gráfico: {e}")
        return df

def chart(df, name, cat, grade, col_name):
    """Esta funcion crea un grafico de radar para visualizar
    de manera mas intuitiva las habilidades del estudiante"""
    errors = []

    df = df.copy()
    if grade in df.columns:
        # Check if the notes are in 0-100 scale and transform to 0-10
        if df[grade].max() > 10:
            df[grade] = df[grade] / 10
            print(f"📝 Notas transformadas de escala 0-100 a 0-10")

    if df.empty:
        errors.append(f"El DataFrame esta vacio")

    if not name or not isinstance(name, str):
        errors.append(f"El nombre del estudiante no es valido")

    if not cat or not isinstance(cat, str):
        errors.append(f"La columna '{cat}' no existe en el DataFrame")

    if not grade or not isinstance(grade, str):
        errors.append(f"La columna '{grade}' no existe en el DataFrame")

    if not col_name or not isinstance(col_name, str):
        errors.append(f"La columna '{col_name}' no existe en el DataFrame")

    # selecting and lenning the unique values from the column cat;
    skill_ct = list(df[cat].unique())
    l_skill_ct = len(skill_ct)

    #filter the data frame by the name of the student
    df1 = df[df[col_name] == name]

    if df1.empty:
        errors.append(f"El estudiante '{name}' no existe en los datos")
        print(f"Estudiantes disponibles: {list(df[col_name].unique())[:5]}")

    df1 = df1.groupby([col_name, cat], as_index=False)[grade].mean().round(1)

    if df1.empty:
        errors.append(f"El estudiante '{name}' no existe calificaciones en '{grade}'")

    #listing the grade
    nota = list(df1[grade])

    if not nota:
        errors.append(f"No hay notas disponibles para graficar")

    #compute the angles
    angle = np.linspace(0, 2 * np.pi, l_skill_ct, endpoint=False).tolist()
    nota += nota[:1]
    angle += angle[:1]

    while len(nota) != len(angle):
        if len(angle) > len(nota):
            nota += nota[:1]  #close the angle
            #TODO Arreglo de la funcion nota =- nota[:1]
        elif len(nota) > len(angle):
            del nota[:1]

    # -- plot --
    try:
        plt.style.use('ggplot')

        # Increase the size of the figure for better visibility
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

        # Improve the display of lines
        ax.plot(angle, nota, color='blue', linewidth=3, linestyle="-", marker='o', 
                markersize=8, markerfacecolor='red', markeredgecolor='darkblue', markeredgewidth=2)
        ax.fill(angle, nota, color='orange', alpha=0.3)

        # Better configure the axes
        ax.set_ylim(0, 10)
        ax.set_yticks(range(0, 11, 2))
        ax.set_yticklabels([f'{i}' for i in range(0, 11, 2)], fontsize=10)
        
        # Improve area labels
        ax.set_xticks(angle[:-1])
        ax.set_xticklabels(skill_ct, fontsize=11, fontweight='bold')
        
        # Add grid for better reading
        ax.grid(True, alpha=0.3)

        plt.title(f'Estudiante {name}', size=14, y=1.08, fontweight='bold')

        print(f"✅ Gráfico generado exitosamente para {name}")

        return ax, errors
    except Exception as e:
        print(f"❌ Error al generar el gráfico: {e}")
        return None, [f"Error al generar gráfico: {e}"]      

def plot_student_dashboard(df, student_id):
    """Genera un dashboard completo con gráfico principal y subgráficos por áreas"""
    try:
        
        # Buscar el estudiante por ID para obtener el nombre
        student = get_student_by_id(df, student_id)
        if student is None:
            print(f"❌ No se encontró estudiante con ID {student_id}")
            return df
        
        student_name = student['nombre_estudiante'].iloc[0]
        # Obtener el aula del estudiante (asumimos que todos sus registros están en el mismo aula)
        aula = student['aula'].iloc[0] if 'aula 1' in student.columns else 'Aula 1'
        
        print(f"📊 Generando dashboard completo para: {student_name} (ID: {student_id})")
        
        # Transformar notas si están en escala 0-100
        df_transformed = df.copy()
        if 'nota' in df_transformed.columns and df_transformed['nota'].max() > 10:
            df_transformed['nota'] = df_transformed['nota'] / 10
            print("📝 Notas transformadas de escala 0-100 a 0-10")
        
        # Llamar a tu función student_grade_chat
        ax1, ax2, ax3, ax4, ax5, ax6, ax7 = student_grade_chat(
            df=df_transformed,
            name=student_name,
            grade='nota',
            cl_name='nombre_estudiante',
            cat='area',
            asg='asignatura',
            aula=aula
        )
        
        # Adjust layout and display
        plt.tight_layout()
        plt.show()
        
        # Show additional statistics
        student_data = df_transformed[df_transformed['id_estudiante'] == int(student_id)]
        promedio_general = student_data['nota'].mean().round(2)
        
        print(f"\n📈 ESTADÍSTICAS DE {student_name}:")
        print("=" * 40)
        print(f"🎯 Promedio General: {promedio_general}/10")
        print(f"🏆 Mejor Nota: {student_data['nota'].max()}/10")
        print(f"📉 Peor Nota: {student_data['nota'].min()}/10")
        print(f"📚 Total Asignaturas: {len(student_data)}")
        
        # Show average by area        
        print(f"\n📊 Promedio por Área:")
        areas_promedio = student_data.groupby('area')['nota'].mean().round(2)
        for area, prom in areas_promedio.items():
            print(f"   • {area}: {prom}/10")
        
        print("=" * 40)
        
        print(f"✅ Dashboard completo generado exitosamente para {student_name}")
        return df
        
    except ImportError as e:
        print(f"❌ Error: No se pueden importar las librerías necesarias: {e}")
        return df
    except Exception as e:
        print(f"❌ Error al generar el dashboard: {e}")
        return df

def segmentacion(df,name,cat, nt, col_name):
    """Esta funcion calcula y ajusta, el angulo y la posicion 
    donde se colocaran en el grafico
    #df- DataFrame
    # name(str) - nombre del estudiante 
    # cat (str) - columan de las categoria que evaluara en el grafico
    # nt (str)- columna donde se encuentra las notas(float) o parametro evaluativo
    # col_name (str)- columna que donde se encuentra los nombres"""

    errors = []

    if df.empty:
        errors.append(f"No hay notas disponibles para graficar")
        
    if not name or not isinstance(name, str):
        errors.append(f"El nombre del estudiante no es valido")

    if not cat or not isinstance(cat, str):
        errors.append(f"La columna '{cat}' no existe en el DataFrame")

    if not nt or not isinstance(nt, str):
        errors.append(f"La columna '{nt}' no existe en el DataFrame")

    if not col_name or not isinstance(col_name, str):
        errors.append(f"La columna '{col_name}' no existe en el DataFrame")
    
    # selecting and lenning the unique values from the column cat;
    skill_ct= list(df[cat].unique())
    l_skill_ct = len(skill_ct)
    
    if l_skill_ct == 0:
        errors.append(f"Error: No hay categorías en la columna '{cat}'")
    
    #filter the data frame by the name of the student
    df1= df[(df[col_name] == name)]
    
    if df1.empty:
        errors.append(f"El estudiante '{name}' no existe en los datos")
        print(f"Estudiantes disponibles: {list(df[col_name].unique())[:5]}")

    df1= df1.groupby( [col_name ,cat], as_index= False)[nt].mean().round(1)
    
    if df1.empty:
        errors.append(f"El estudiante '{name}' no existe calificaciones en '{nt}'")

    #listing the grade 
    nota = list(df1[nt])
    
    #compute the angles
    
    angle= np.linspace(0,2 *np.pi, l_skill_ct, endpoint= False).tolist()
    nota += nota[:1]
    angle += angle[:1]
    
        # check the variables 
    if len(nota) == 0 or len(angle) == 0:
        print("Error: nota o angle están vacíos")
    else:
        # exective if all of them have values
        while len(nota) != len(angle):
            if len(angle) > len(nota):
                nota += nota[:1]
            elif len(nota) > len(angle):
                nota = nota[:len(angle)]
            
    return angle, nota, skill_ct
    

def student_grade_chat(df,name,grade, cl_name, cat, asg, aula ):
    
    """Esta funcion crea la platilla y el grafico principal por area
    y los sub grafico por campos
    #df- DataFrame
    # name(str) - nombre del estudiante 
    # cat (str) - columan de las categoria que evaluara en el grafico
    # grande (str)- columna donde se encuentra las notas(float) o parametro evaluativo
    # col_name (str)- columna que donde se encuentra los nombres
    # asg (str)- columna de la sub areas, 
    # aula(str)- columna del aula que esta evaluando"""
    
    errors = []

    # Selecting and counting the unique values from the column 'area'
    skill_ct = list(df[cat].unique())
    l_skill_ct = len(skill_ct)
    
    if l_skill_ct == 0:
        errors.append(f"Error: No hay categorías en la columna '{cat}'")

    # Filter the dataframe by the student's name
    df1 = df[(df[cl_name] == name) & (df['aula'] == aula)]

    if df1.empty:
        errors.append(f"El estudiante '{name}' o el '{aula}' no existe en los datos")
        print(f"Estudiantes disponibles: {list(df[cl_name].unique())[:5]}")

    df1 = df1.groupby([cl_name, cat], as_index=False)[ grade].mean().round(1)

    if df1.empty:
        errors.append(f"El estudiante '{name}' no existe calificaciones en '{grade}'")

    # Listing the grades
    nota = list(df1[grade])

    # Compute the angles
    angle = np.linspace(0, 2 * np.pi, l_skill_ct, endpoint=False).tolist()

    # Close the circle
    nota += nota[:1]
    angle += angle[:1]

    # Adjust lengths in case they differ
    while len(nota) != len(angle):
        if len(angle) > len(nota):
            nota += nota[:1]  # close the angle
        elif len(nota) > len(angle):
            nota = nota[:len(angle)]

    # Set the style of the chat
    plt.style.use("ggplot")
    
    fig = plt.figure( figsize= (20,12)) # Create the figure where all the grafic will be layout 

    #Select the part of the fig, it's worked as a arrays
    fig_g= GridSpec(4,6, figure= fig)
    ax1= fig.add_subplot(fig_g[1:3, 2:4], polar= True)
    ax2= fig.add_subplot(fig_g[1,0],polar= True)
    ax3= fig.add_subplot(fig_g[2,1],polar= True)
    ax4= fig.add_subplot(fig_g[3,0],polar= True)
    ax5= fig.add_subplot(fig_g[1,5],polar= True)
    ax6= fig.add_subplot(fig_g[2,4],polar= True)
    ax7= fig.add_subplot(fig_g[3,5],polar= True)

    #Plot the first chat and the principal 
    ax1.plot(angle, nota, color = 'blue', linewidth= 0.5, linestyle = "--", marker= 'o') #plot the fig 
    ax1.fill(angle, nota, color= 'orange', alpha= 0.2)
        
        #set the ticks labes 
    ax1.set_yticks(range(1,11))
    ax1.set_yticklabels([])
    ax1.set_xticks(angle[:-1])
    ax1.set_xticklabels(skill_ct, fontsize= 8)
    ax1.tick_params(axis='x', pad=8)
    ax1.set_title (f'Estudiante {name} del {aula}', pad= 25, fontsize= 16)

    #Filter the df by one of the area
    df2= df[df[cat]== "Historia"]
    #Check if the values name is in df 
    if name in df2[cl_name].values:
        angle_2, nota_2, skill_as2 = segmentacion(df2, name= name ,
                                         cat= asg ,
                                         col_name= cl_name,
                                         nt= grade 
                                         ) #this function return the values to compute the data
        
        #Plot the chat 
        ax2.plot(angle_2, nota_2, color = 'blue', linewidth= 0.5, linestyle = "--", marker= 'o') #plot the fig 
        ax2.fill(angle_2, nota_2, color= 'orange', alpha= 0.2)
            
            #set the ticks labes 
        ax2.set_yticks(range(1,11))
        ax2.set_yticklabels([])
        ax2.set_xticks(angle_2[:-1])
        ax2.set_xticklabels(skill_as2, rotation= 45)
        ax2.tick_params(axis='x', pad=8)
        ax2.set_title (f'Campo de Historia', pad= 25)
    else: 
        ax2.set_title (f'Campo de Historia', pad= 25)
        pass #jump to the othe line of code if the name is not on df 


    df3= df[df['area'] == "Matemáticas"]
    #Check if the values name is in df 
    if name in df3[cl_name].values:
        angle_3, nota_3, skill_as3= segmentacion(df3, name= "Ana Pérez",
                                        cat= 'asignatura',
                                        col_name= 'nombre_estudiante',
                                        nt= 'nota'
                                        )
        ax3.plot(angle_3, nota_3, color = 'blue', linewidth= 0.5, linestyle = "--", marker= 'o') #plot the fig 
        ax3.fill(angle_3, nota_3, color= 'orange', alpha= 0.2)
            
            #set the ticks labes 
        ax3.set_yticks(range(1,11))
        ax3.set_yticklabels([])
        ax3.set_xticks(angle_3[:-1])
        ax3.set_xticklabels(skill_as3)
        ax3.tick_params(axis='x', pad=8)
        ax3.set_title (f'Campo de Matematicas', pad= 25)
    else:
        ax3.set_title(f'Campo de Matematicas', pad= 25)
        pass

    #Filte the dataframe
    df4= df[df['area'] == "Ciencias"]

    if name in df4[cl_name].values:
        #Get the variable from the seg function 
        angle_4, nota_4, skill_as4= segmentacion(df4, name= name,
                                        cat= asg,
                                        col_name= cl_name,
                                        nt= grade
                                        )
        #set the plot 
        ax4.plot(angle_4, nota_4, color = 'blue', linewidth= 0.5, linestyle = "--", marker= 'o') #plot the fig 
        ax4.fill(angle_4, nota_4, color= 'orange', alpha= 0.2)
            
            #set the ticks labes 
        ax4.set_yticks(range(1,11))
        ax4.set_yticklabels([])
        ax4.set_xticks(angle_4[:-1])
        ax4.set_xticklabels(skill_as4)
        ax4.tick_params(axis='x', pad=8)
        ax4.set_title (f'Campo de Ciencias', pad= 25)
    else: 
        ax4.set_title (f'Campo de Ciencias', pad= 25)
        pass

    #filter the dataframe
    df5= df[df['area'] == "Tecnología"]

    if name in df5[cl_name].values:

        angle_5, nota_5, skill_as5 = segmentacion(df5, name= name,
                                        cat= asg,
                                        col_name= cl_name,
                                        nt= grade
                                        )
        ax5.plot(angle_5, nota_5, color = 'blue', linewidth= 0.5, linestyle = "--", marker= 'o') #plot the fig 
        ax5.fill(angle_5, nota_5, color= 'orange', alpha= 0.2)
            
            #set the ticks labes 
        ax5.set_yticks(range(1,11))
        ax5.set_yticklabels([])
        ax5.set_xticks(angle_5[:-1])
        ax5.set_xticklabels(skill_as5)
        ax5.tick_params(axis='x', pad=8)
        ax5.set_title (f'Campo de Tecnologia', pad= 25)
    else:
        ax5.set_title (f'Campo de Tecnologia', pad= 25)
        pass

    #filter the dataframe
    df6= df[df['area'] == "Lenguas"]

    #check if the name of the student is in the df
    if name in df6[cl_name].values:

        angle_6, nota_6, skill_as6 = segmentacion(df6, name= name,
                                        cat= asg,
                                        col_name= cl_name,
                                        nt= grade
                                        )
        ax6.plot(angle_6, nota_6, color = 'blue', linewidth= 0.5, linestyle = "--", marker= 'o') #plot the fig 
        ax6.fill(angle_6, nota_6, color= 'orange', alpha= 0.2)
            
            #set the ticks labes 
        ax6.set_yticks(range(1,11))
        ax6.set_yticklabels([])
        ax6.set_xticks(angle_6[:-1])
        ax6.set_xticklabels(skill_as6)
        ax6.tick_params(axis='x', pad=8)
        ax6.set_title (f'Campo de Lenguas', pad= 15)
    else:
        pass

    #filter the dataframe 
    df7= df[df['area'] == "Educación Física"]

    #check if the name of the student is in the df
    if name in df7[cl_name].values:

        angle_7, nota_7, skill_as7 = segmentacion(df7, name= name,
                                        cat= asg,
                                        col_name= cl_name,
                                        nt= grade
                                        )
        ax7.plot(angle_7, nota_7, color = 'blue', linewidth= 0.5, linestyle = "--", marker= 'o') #plot the fig 
        ax7.fill(angle_7, nota_7, color= 'orange', alpha= 0.2)
            
            #set the ticks labes 
        ax7.set_yticks((range(1,11)))
        ax7.set_yticklabels([])
        ax7.set_xticks(angle_7[:-1])
        ax7.set_xticklabels(skill_as7)
        ax7.tick_params(axis='x', pad=8)
        ax7.set_title (f'Campo de Educación Fisica', pad= 15)
    else:
        ax7.set_title (f'Campo de Educación Fisica', pad= 15)
        pass
    
    return ax1, ax2, ax3, ax4, ax5, ax6, ax7

