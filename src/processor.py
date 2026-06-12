"""
===================================================
processor.py - Fase 2: Procesamiento de Datos
===================================================
Toma los datos crudos (JSON) y los transforma en DataFrames de Pandas,
limpiando valores nulos y formateando las fechas.

"""

import json
import pandas as pd
from pathlib import Path
import sys

# Importar configuración
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import RAW_DIR, PROCESSED_DIR, WORLD_CUP_2026_TEAMS


class DataProcessor:
    """
    Procesador de datos usando Pandas.
    """

    def __init__(self):
        self.raw_dir = RAW_DIR
        self.processed_dir = PROCESSED_DIR

    def _load_json(self, filename):
        """Carga un archivo JSON desde el directorio raw."""
        filepath = self.raw_dir / filename
        if not filepath.exists():
            print(f"  No se encontró {filename}")
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def process_matches(self, input_filename="world_cup_2026_matches.json", output_filename="matches.csv"):
        """
        Procesa el JSON de partidos y crea un CSV limpio.
        """
        print(f"\n🔄 Procesando {input_filename}...")
        
        data = self._load_json(input_filename)
        if not data or "matches" not in data:
            return None
            
        matches_list = []
        for match in data["matches"]:
            # Solo nos interesan partidos que tengan los equipos definidos
            if not match.get("homeTeam", {}).get("name") or not match.get("awayTeam", {}).get("name"):
                continue
                
            # Extraer goles (si el partido ya se jugó)
            home_goals = None
            away_goals = None
            score_data = match.get("score", {}).get("fullTime", {})
            if score_data and score_data.get("home") is not None:
                home_goals = score_data.get("home")
                away_goals = score_data.get("away")
                
            match_dict = {
                "id": match.get("id"),
                "date": match.get("utcDate"),
                "status": match.get("status"),
                "stage": match.get("stage"),
                "group": match.get("group"),
                "home_team": match["homeTeam"]["name"],
                "home_team_code": match["homeTeam"].get("tla"),
                "away_team": match["awayTeam"]["name"],
                "away_team_code": match["awayTeam"].get("tla"),
                "home_goals": home_goals,
                "away_goals": away_goals,
            }
            matches_list.append(match_dict)
            
        if not matches_list:
            print("  No hay partidos válidos para procesar")
            return None
            
        # Crear DataFrame
        df = pd.DataFrame(matches_list)
        
        # 💡 TIP: Convertir a datetime permite hacer filtrados por fecha muy fácilmente
        df["date"] = pd.to_datetime(df["date"])
        
        # Guardar en CSV
        out_path = self.processed_dir / output_filename
        df.to_csv(out_path, index=False)
        print(f"    Guardado {output_filename} ({len(df)} partidos)")
        
        return df

    def get_team_list(self):
        """
        Genera una lista plana de todos los equipos desde config.py
        para ser usada en el modelo.
        """
        teams = []
        for group, team_list in WORLD_CUP_2026_TEAMS.items():
            for team in team_list:
                teams.append({
                    "team_name": team["name"],
                    "team_code": team["code"],
                    "group": group,
                    "confederation": team["confederation"]
                })
        
        df = pd.DataFrame(teams)
        df.to_csv(self.processed_dir / "teams.csv", index=False)
        return df


if __name__ == "__main__":
    print(" Predicciones Mundial 2026 - Procesador de Datos\n")
    processor = DataProcessor()
    
    # Procesar partidos generados o descargados
    matches_df = processor.process_matches("world_cup_2026_matches.json", "wc_2026_matches.csv")
    
    # Generar listado de equipos
    teams_df = processor.get_team_list()
    
    print("\n Fase 2 completada.")
