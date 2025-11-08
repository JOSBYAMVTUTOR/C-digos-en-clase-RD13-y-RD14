import pandas as pd
from Colors import Colors
from datetime import datetime
from Menu_functions import *


def print_header():
    header = f"""
{Colors.CYAN}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🎓 SISTEMA INTELIGENTE DE CALIFICACIONES 🎓           ║
║                                                              ║
║              📊 Predicción de Notas Estudiantiles 📊         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.YELLOW}📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}{Colors.ENDC}
{Colors.GREEN}🖥️  Sistema: Predictor de Calificaciones v1.0{Colors.ENDC}
"""
    print(header)

def print_menu():
    menu = f"""
{Colors.BLUE}
┌───────────────────────────────────────────────────────────────────┐
│                         {Colors.BOLD}🏠 MENÚ PRINCIPAL{Colors.ENDC}{Colors.BLUE}                         │
└───────────────────────────────────────────────────────────────────┘{Colors.ENDC}

{Colors.GREEN}📋 OPCIONES DISPONIBLES:{Colors.ENDC}

{Colors.CYAN}   🔍 [1]{Colors.ENDC} {Colors.BOLD}Seleccionar estudiante por ID{Colors.ENDC}
{Colors.CYAN}   ➕ [2]{Colors.ENDC} {Colors.BOLD}Agregar nuevo estudiante{Colors.ENDC}
{Colors.CYAN}   🗑️  [3]{Colors.ENDC} {Colors.BOLD}Eliminar estudiante{Colors.ENDC}
{Colors.CYAN}   ✏️  [4]{Colors.ENDC} {Colors.BOLD}Modificar datos de estudiante por ID{Colors.ENDC}
{Colors.CYAN}   📃 [5]{Colors.ENDC} {Colors.BOLD}Listar todos los estudiantes{Colors.ENDC}
{Colors.CYAN}   🔮 [6]{Colors.ENDC} {Colors.BOLD}Predecir calificaciones y posibles fortalezas{Colors.ENDC}
{Colors.CYAN}   📊 [7]{Colors.ENDC} {Colors.BOLD}Ver estadísticas generales{Colors.ENDC}
{Colors.CYAN}   📈 [8]{Colors.ENDC} {Colors.BOLD}Gráfico de habilidades del estudiante{Colors.ENDC}
{Colors.CYAN}   🎯 [9]{Colors.ENDC} {Colors.BOLD}Dashboard completo del estudiante{Colors.ENDC}
{Colors.RED}   🚪 [0]{Colors.ENDC} {Colors.BOLD}Salir del sistema{Colors.ENDC}


"""
    print(menu)

#Valida la opcion del menu
def valid_menu_input(opcion, opciones_validas):

    try:
        option_num = int(opcion)
        if option_num not in opciones_validas:
            return False, f"Opcion debe estar entre {min(opciones_validas)} y {max(opciones_validas)}"
        return True, ""
    except ValueError:
        return False, "La opcion debe ser un numero valido"

def valid_dataframe(df):
     # Valida que el DataFrame sea usable

    if df is None:
        return False, "No se pudo cargar los datos del sistema"

    if df.empty:
        return False, "El sistema no tiene datos de estudiantes registrados"

    # Verificar columnas esenciales

    columnas_esenciales = ['nombre_estudiante', 'area', 'nota']
    for col in columnas_esenciales:
        if col not in df.columns:
            return False, f"Falta la columna esencial '{col}' en los datos"

    return True, ""

def main():
    try:
        print(f"{Colors.YELLOW}Cargando datos del sistema...{Colors.ENDC}")
        df = leer_datos()

        is_valid, message = valid_dataframe(df)

        if not is_valid:
            print(f"{Colors.RED}{message}{Colors.ENDC}")
            input(f"{Colors.YELLOW}Presiona Enter para salir...{Colors.ENDC}")
            return

    except Exception as e:
        print(f"{Colors.RED}Error critico al iniciar el sistema: {e}{Colors.ENDC}")
        input(f"{Colors.YELLOW}Presiona Enter para salir...{Colors.ENDC}")
        return

    valid_options = [0 , 1, 2, 3, 4, 5, 6, 7, 8, 9]
    while True:
        try:
            clear_screen()
            print_header()
            print_menu()


            # Get user input
            prompt = f"{Colors.CYAN}🎯 Seleccione una opción (0-9): {Colors.ENDC}"
            choice = input(prompt).strip()

            is_valid, message = valid_menu_input(choice, valid_options)

            if not is_valid:
                print(f"{Colors.RED}{message}{Colors.ENDC}")
                input(f"{Colors.YELLOW}Presiona Enter para continuar...{Colors.ENDC}")


            # Process the choice using match statement
            df, result = get_user_input(choice, df)

            if result == 0:
                break
        except Exception as e:
            print(f"{Colors.RED}Error inesperado: {e}{Colors.ENDC}")
            input(f"{Colors.YELLOW}Presiona Enter para continuar...{Colors.ENDC}")


if __name__ == "__main__":
    main()
