"""
===================================================
predictor.py - Fase 5: Motor de Predicciones
===================================================
Unifica todo: carga datos, extrae features, corre el modelo
y muestra los resultados formateados en consola.
"""

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.features import FeatureEngineer
from src.model import PoissonModel
from config import WORLD_CUP_2026_TEAMS, PROCESSED_DIR, COLORS


class WorldCupPredictor:
    def __init__(self):
        self.fe = FeatureEngineer()
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """Carga datos procesados e inicializa el modelo Poisson."""
        try:
            matches_df = pd.read_csv(PROCESSED_DIR / "wc_2026_matches.csv")
            strengths = self.fe.calculate_attack_defense_strengths(matches_df)
        except FileNotFoundError:
            # Si no hay CSV, usamos DF vacío y el modelo usará defaults + ELO
            strengths = pd.DataFrame()

        elo_df = self.fe.get_current_elo()
        self.model = PoissonModel(strengths, elo_df)

    def _draw_progress_bar(self, percentage, width=20):
        """Dibuja una barra de progreso estilo retro para consola."""
        filled = int(width * percentage)
        empty = width - filled
        return "█" * filled + "░" * empty

    def display_prediction(self, home_team, away_team, is_neutral=True):
        """Ejecuta y muestra la predicción de manera elegante en consola."""
        if not self.model:
            print(" Error: Modelo no inicializado.")
            return

        result = self.model.predict_match(home_team, away_team, is_neutral)
        
        home_elo = self.fe.elo_ratings.get(home_team, 1500)
        away_elo = self.fe.elo_ratings.get(away_team, 1500)
        
        # Determinar de qué grupo son para mostrar info extra
        group_h = next((g for g, t in WORLD_CUP_2026_TEAMS.items() if any(x["name"] == home_team for x in t)), "?")
        group_a = next((g for g, t in WORLD_CUP_2026_TEAMS.items() if any(x["name"] == away_team for x in t)), "?")

        print(f"\n{COLORS['CYAN']}╔{'═'*58}╗{COLORS['END']}")
        print(f"{COLORS['CYAN']}║{COLORS['BOLD']}        PREDICCIÓN MUNDIAL 2026 - Grupo {group_h} vs {group_a}          {COLORS['CYAN']}║{COLORS['END']}")
        print(f"{COLORS['CYAN']}╠{'═'*58}╣{COLORS['END']}")
        
        # Encabezado partido
        match_str = f"{home_team} vs {away_team}"
        padding = (56 - len(match_str)) // 2
        print(f"{COLORS['CYAN']}║{COLORS['END']} {' '*padding}{COLORS['BOLD']}{match_str}{COLORS['END']}{' '*padding} {COLORS['CYAN']}║{COLORS['END']}")
        print(f"{COLORS['CYAN']}║{' '*58}║{COLORS['END']}")
        
        # Probabilidades
        h_prob = result['home_win']
        d_prob = result['draw']
        a_prob = result['away_win']
        
        h_bar = self._draw_progress_bar(h_prob)
        d_bar = self._draw_progress_bar(d_prob)
        a_bar = self._draw_progress_bar(a_prob)
        
        print(f"{COLORS['CYAN']}║{COLORS['END']}  Victoria {home_team:<15} {h_prob*100:4.1f}%  {COLORS['GREEN']}{h_bar}{COLORS['END']}       {COLORS['CYAN']}║{COLORS['END']}")
        print(f"{COLORS['CYAN']}║{COLORS['END']}  Empate {' '*15} {d_prob*100:4.1f}%  {COLORS['YELLOW']}{d_bar}{COLORS['END']}       {COLORS['CYAN']}║{COLORS['END']}")
        print(f"{COLORS['CYAN']}║{COLORS['END']}  Victoria {away_team:<15} {a_prob*100:4.1f}%  {COLORS['RED']}{a_bar}{COLORS['END']}       {COLORS['CYAN']}║{COLORS['END']}")
        
        print(f"{COLORS['CYAN']}║{' '*58}║{COLORS['END']}")
        
        # Marcador y stats
        score = result['most_likely_score']
        print(f"{COLORS['CYAN']}║{COLORS['END']}  {COLORS['BOLD']}Marcador más probable: {home_team} {score[0]} - {score[1]} {away_team}{COLORS['END']}        {COLORS['CYAN']}║{COLORS['END']}")
        print(f"{COLORS['CYAN']}║{COLORS['END']}  ELO: {home_team} {int(home_elo)} | {away_team} {int(away_elo)}{' '*15} {COLORS['CYAN']}║{COLORS['END']}")
        print(f"{COLORS['CYAN']}╚{'═'*58}╝{COLORS['END']}")


if __name__ == "__main__":
    predictor = WorldCupPredictor()
    predictor.display_prediction("Mexico", "Sudafrica", is_neutral=False) # México es local
    predictor.display_prediction("Argentina", "France", is_neutral=True)
