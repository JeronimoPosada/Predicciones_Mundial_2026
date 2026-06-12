"""
===================================================
features.py - Fase 3: Feature Engineering
===================================================
Calcula las características (features) de cada equipo como su
rating ELO y sus fortalezas de ataque y defensa.

Las redes neuronales no sirven de nada si le das datos sin procesar.
Aquí creamos el sistema ELO, un método matemático probado.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import PROCESSED_DIR, INITIAL_ELO_RATINGS, ELO_K_FACTOR


class FeatureEngineer:
    def __init__(self):
        self.processed_dir = PROCESSED_DIR
        self.elo_ratings = INITIAL_ELO_RATINGS.copy()

    def update_elo(self, home_team, away_team, home_goals, away_goals, match_type="friendly"):
        """
        Actualiza el ELO rating de dos equipos después de un partido.
        
        Fórmula: Rn = Ro + K * (W - We)
        Ro: Rating anterior
        W: Resultado (1 victoria, 0.5 empate, 0 derrota)
        We: Resultado esperado = 1 / (1 + 10^((opp_Ro - Ro)/400))
        """
        # Si no conocemos el equipo, le asignamos 1500 por defecto
        home_elo = self.elo_ratings.get(home_team, 1500)
        away_elo = self.elo_ratings.get(away_team, 1500)
        
        # Calcular resultado esperado
        home_we = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))
        away_we = 1 / (1 + 10 ** ((home_elo - away_elo) / 400))
        
        # Determinar el resultado real W
        if home_goals > away_goals:
            home_w, away_w = 1, 0
        elif home_goals < away_goals:
            home_w, away_w = 0, 1
        else:
            home_w, away_w = 0.5, 0.5
            
        # Factor K
        k = ELO_K_FACTOR.get(match_type, 20)
        
        # Nuevo ELO
        new_home_elo = home_elo + k * (home_w - home_we)
        new_away_elo = away_elo + k * (away_w - away_we)
        
        self.elo_ratings[home_team] = new_home_elo
        self.elo_ratings[away_team] = new_away_elo

    def get_current_elo(self):
        """Devuelve un DataFrame con los ELO actuales."""
        df = pd.DataFrame(list(self.elo_ratings.items()), columns=["Team", "ELO"])
        return df.sort_values(by="ELO", ascending=False).reset_index(drop=True)

    def calculate_attack_defense_strengths(self, matches_df):
        """
        Calcula la fuerza ofensiva y defensiva de cada equipo
        basado en el promedio de goles anotados y recibidos frente al promedio global.
        
        Este es el corazón del modelo de Poisson. Necesitamos
        saber si un equipo anota más que el promedio (fuerza ofensiva > 1)
        o recibe menos (fuerza defensiva < 1).
        """
        if matches_df is None or matches_df.empty:
            return pd.DataFrame()
            
        # Solo usamos partidos jugados
        played = matches_df.dropna(subset=['home_goals', 'away_goals']).copy()
        
        if played.empty:
            print("  No hay partidos jugados para calcular fortalezas. Usando defaults (1.0).")
            # Generar defaults de los equipos que aparezcan
            teams = pd.concat([matches_df['home_team'], matches_df['away_team']]).unique()
            default_strengths = pd.DataFrame({
                'Team': teams,
                'Attack_Strength': 1.0,
                'Defense_Strength': 1.0
            })
            return default_strengths

        # Promedio global de goles (Local y Visitante)
        avg_home_scored = played['home_goals'].mean()
        avg_away_scored = played['away_goals'].mean()

        # Evitar división por cero
        if avg_home_scored == 0: avg_home_scored = 1
        if avg_away_scored == 0: avg_away_scored = 1

        # Goles anotados y recibidos por equipo como local
        home_stats = played.groupby('home_team').agg(
            home_scored=('home_goals', 'mean'),
            home_conceded=('away_goals', 'mean')
        )
        
        # Goles anotados y recibidos por equipo como visitante
        away_stats = played.groupby('away_team').agg(
            away_scored=('away_goals', 'mean'),
            away_conceded=('home_goals', 'mean')
        )

        # Unir estadísticas
        stats = pd.merge(home_stats, away_stats, left_index=True, right_index=True, how='outer').fillna(0)
        
        # Calcular fuerzas (si es > 1.0, es más fuerte que el promedio)
        stats['Attack_Strength'] = ((stats['home_scored'] / avg_home_scored) + (stats['away_scored'] / avg_away_scored)) / 2
        stats['Defense_Strength'] = ((stats['home_conceded'] / avg_away_scored) + (stats['away_conceded'] / avg_home_scored)) / 2
        
        # Limitar valores extremos y asegurar que nadie tenga 0
        stats['Attack_Strength'] = stats['Attack_Strength'].clip(lower=0.1, upper=3.0)
        stats['Defense_Strength'] = stats['Defense_Strength'].clip(lower=0.1, upper=3.0)
        
        stats = stats.reset_index().rename(columns={'index': 'Team'})
        return stats[['Team', 'Attack_Strength', 'Defense_Strength']]


if __name__ == "__main__":
    print(" Predicciones Mundial 2026 - Feature Engineer\n")
    fe = FeatureEngineer()
    
    try:
        matches_df = pd.read_csv(PROCESSED_DIR / "wc_2026_matches.csv")
        strengths = fe.calculate_attack_defense_strengths(matches_df)
        print("Fortalezas calculadas. Ejemplo:")
        print(strengths.head())
        elo_df = fe.get_current_elo()
        print("\nTop 5 ELO Ratings:")
        print(elo_df.head())
        
    except FileNotFoundError:
        print("  No se encontró wc_2026_matches.csv. Ejecuta processor.py primero.")
    
    print("\n Fase 3 completada.")
