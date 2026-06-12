"""
===================================================
main.py - Entry Point del Proyecto
===================================================
Este es el archivo principal que el usuario ejecutará.
Proporciona una interfaz de línea de comandos (CLI) interactiva.
"""

import sys
import os
from pathlib import Path

# Asegurar que los imports funcionen desde la raíz
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.collector import DataCollector, create_fallback_data
from src.processor import DataProcessor
from src.features import FeatureEngineer
from src.predictor import WorldCupPredictor
from config import WORLD_CUP_2026_TEAMS, COLORS, print_config_status


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    print(f"{COLORS['GREEN']}")
    print(r"""
  __  __                 _ _       _   ___   ___ ___   ___  
 |  \/  |               | (_)     | | |__ \ / _ \__ \ /   \
 | \  / |_   _ _ __   __| |_  __ _| |    ) | | | | )  |___
 | |\/| | | | | '_ \ / _` | |/ _` | |   / /| | | |/ / |   \
 | |  | | |_| | | | | (_| | | (_| | |  / /_| |_| / /_ |   |
 |_|  |_|\__,_|_| |_|\__,_|_|\__,_|_| |____|\___/____ \___/ 
                                                            
                PREDICTOR ESTADÍSTICO
    """)
    print(f"{COLORS['END']}")


def menu_update_data():
    """Ejecuta las fases 1 a 3 para actualizar los datos."""
    print(f"\n{COLORS['YELLOW']}=== ACTUALIZANDO DATOS ==={COLORS['END']}")
    
    # 1. Recolectar
    collector = DataCollector()
    if collector.headers.get("X-Auth-Token"):
        collector.collect_all_world_cup_data()
    else:
        create_fallback_data()
        
    # 2. Procesar
    processor = DataProcessor()
    processor.process_matches()
    processor.get_team_list()
    
    # 3. No hace falta correr features explícitamente aquí,
    # el predictor lo hace al inicializarse.
    print(f"{COLORS['GREEN']} Datos actualizados correctamente.{COLORS['END']}")
    input("\nPresiona Enter para continuar...")


def menu_predict_match(predictor):
    """Interfaz para predecir un partido específico."""
    print(f"\n{COLORS['YELLOW']}=== PREDECIR PARTIDO ==={COLORS['END']}")
    
    # Mostrar equipos disponibles por grupo
    print("\nEquipos disponibles:")
    for group, teams in WORLD_CUP_2026_TEAMS.items():
        team_names = [t["name"] for t in teams]
        print(f"Grupo {group}: {', '.join(team_names)}")
        
    home = input("\nNombre del equipo Local (ej: Mexico): ").strip()
    away = input("Nombre del equipo Visitante (ej: Argentina): ").strip()
    
    try:
        predictor.display_prediction(home, away)
    except Exception as e:
        print(f"\n{COLORS['RED']} Error: Asegúrate de escribir el nombre exactamente como en la lista.{COLORS['END']}")
        print(f"Detalle: {e}")
        
    input("\nPresiona Enter para continuar...")


def menu_group_stage(predictor):
    """Predice todos los partidos de un grupo."""
    print(f"\n{COLORS['YELLOW']}=== PREDECIR GRUPO ==={COLORS['END']}")
    group = input("Ingresa la letra del grupo (A-L): ").strip().upper()
    
    if group not in WORLD_CUP_2026_TEAMS:
        print(f"{COLORS['RED']} Grupo no válido.{COLORS['END']}")
        input("\nPresiona Enter para continuar...")
        return
        
    teams = [t["name"] for t in WORLD_CUP_2026_TEAMS[group]]
    
    # Generar todos los cruces
    matches = []
    for i in range(len(teams)):
        for j in range(i+1, len(teams)):
            matches.append((teams[i], teams[j]))
            
    print(f"\nPrediciendo partidos del Grupo {group}...")
    for home, away in matches:
        predictor.display_prediction(home, away)
        
    input("\nPresiona Enter para continuar...")


def main():
    """Función principal (Bucle del menú)."""
    # Intentar inicializar el predictor
    try:
        predictor = WorldCupPredictor()
    except Exception as e:
        print(f"Error al inicializar el modelo. Por favor actualiza los datos primero.")
        predictor = None

    while True:
        clear_screen()
        print_banner()
        print("Selecciona una opción:")
        print("1. 🔄 Actualizar Datos (Fase 1-2)")
        print("2. ⚽ Predecir un Partido Específico")
        print("3. 📊 Predecir un Grupo Completo")
        print("4. ⚙️  Ver Estado de Configuración")
        print("5. 🚪 Salir")
        
        choice = input(f"\n{COLORS['CYAN']}Opción > {COLORS['END']}").strip()
        
        if choice == '1':
            menu_update_data()
            # Reinicializar predictor después de actualizar
            try:
                predictor = WorldCupPredictor()
            except:
                pass
        elif choice == '2':
            if predictor:
                menu_predict_match(predictor)
            else:
                print("Primero debes actualizar los datos (Opción 1)")
                input("\nPresiona Enter para continuar...")
        elif choice == '3':
            if predictor:
                menu_group_stage(predictor)
            else:
                print("Primero debes actualizar los datos (Opción 1)")
                input("\nPresiona Enter para continuar...")
        elif choice == '4':
            print_config_status()
            input("\nPresiona Enter para continuar...")
        elif choice == '5':
            print("\n¡Gracias por usar el Predictor del Mundial 2026!\n")
            break
        else:
            print("Opción no válida.")
            input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    main()
