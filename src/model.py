"""
===================================================
model.py - Fase 4: Modelo Predictivo
===================================================
Implementa la Regresión de Poisson con ajuste Dixon-Coles
para predecir el resultado de los partidos.

"""

import numpy as np
from scipy.stats import poisson
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import POISSON_MAX_GOALS, HOME_ADVANTAGE, DIXON_COLES_RHO


class PoissonModel:
    def __init__(self, strengths_df, elo_df):
        self.strengths = strengths_df.set_index('Team') if not strengths_df.empty else pd.DataFrame()
        self.elo = elo_df.set_index('Team') if not elo_df.empty else pd.DataFrame()
        
        # Promedio global estimado de goles por partido en mundiales
        self.avg_goals = 1.3  # Goles por equipo por partido (aprox)

    def _get_team_stats(self, team_name):
        """Obtiene las estadísticas de un equipo, usando defaults si no existen."""
        attack = 1.0
        defense = 1.0
        elo_diff_factor = 1.0
        
        if not self.strengths.empty and team_name in self.strengths.index:
            attack = self.strengths.loc[team_name, 'Attack_Strength']
            defense = self.strengths.loc[team_name, 'Defense_Strength']
            
        return attack, defense

    def _calculate_lambda(self, home_team, away_team, is_neutral=True):
        """
        Calcula el valor Lambda (λ) esperado para cada equipo.
        λ = Promedio_Goles * Ataque_Propio * Defensa_Rival * (Ventaja_Local)
        """
        home_attack, home_defense = self._get_team_stats(home_team)
        away_attack, away_defense = self._get_team_stats(away_team)
        
        # Ajuste basado en ELO
        home_elo = self.elo.loc[home_team, 'ELO'] if not self.elo.empty and home_team in self.elo.index else 1500
        away_elo = self.elo.loc[away_team, 'ELO'] if not self.elo.empty and away_team in self.elo.index else 1500
        
        # El ELO modifica ligeramente el ataque esperado
        elo_diff = (home_elo - away_elo) / 400
        home_elo_factor = 10 ** (elo_diff / 2)
        away_elo_factor = 10 ** (-elo_diff / 2)
        
        # En el Mundial, casi todos los partidos son en campo neutral
        # Solo México, USA y Canadá tendrían Home Advantage
        ha_factor = HOME_ADVANTAGE if not is_neutral else 1.0
        
        home_lambda = self.avg_goals * home_attack * away_defense * ha_factor * home_elo_factor
        away_lambda = self.avg_goals * away_attack * home_defense * away_elo_factor
        
        return home_lambda, away_lambda

    def _rho_correction(self, x, y, lambda_x, lambda_y, rho=DIXON_COLES_RHO):
        """
        Ajuste de Dixon-Coles. 
        Corrige la subestimación de empates de bajo marcador (0-0, 1-1, 0-1, 1-0).
        """
        if x == 0 and y == 0:
            return 1 - (lambda_x * lambda_y * rho)
        elif x == 0 and y == 1:
            return 1 + (lambda_x * rho)
        elif x == 1 and y == 0:
            return 1 + (lambda_y * rho)
        elif x == 1 and y == 1:
            return 1 - rho
        return 1.0

    def predict_match(self, home_team, away_team, is_neutral=True):
        """
        Genera la matriz de probabilidades para el partido.
        
        Returns:
            - Probs de W/D/L
            - Marcador más probable
            - Matriz de probabilidades
        """
        home_lambda, away_lambda = self._calculate_lambda(home_team, away_team, is_neutral)
        
        # Crear matriz de probabilidades (ej: 8x8)
        prob_matrix = np.zeros((POISSON_MAX_GOALS, POISSON_MAX_GOALS))
        
        for x in range(POISSON_MAX_GOALS):
            for y in range(POISSON_MAX_GOALS):
                # Poisson puro
                p = poisson.pmf(x, home_lambda) * poisson.pmf(y, away_lambda)
                # Ajuste Dixon-Coles
                p *= self._rho_correction(x, y, home_lambda, away_lambda)
                prob_matrix[x, y] = p
                
        # Normalizar para que sume 1 (por si cortamos la matriz muy pequeña)
        prob_matrix = prob_matrix / np.sum(prob_matrix)
        
        # Calcular probabilidades de resultados (Win, Draw, Loss)
        home_win_prob = np.sum(np.tril(prob_matrix, -1))
        draw_prob = np.sum(np.diag(prob_matrix))
        away_win_prob = np.sum(np.triu(prob_matrix, 1))
        
        # Encontrar el marcador más probable
        flat_idx = np.argmax(prob_matrix)
        most_likely_home, most_likely_away = np.unravel_index(flat_idx, prob_matrix.shape)
        
        return {
            'home_win': home_win_prob,
            'draw': draw_prob,
            'away_win': away_win_prob,
            'most_likely_score': (most_likely_home, most_likely_away),
            'home_lambda': home_lambda,
            'away_lambda': away_lambda,
            'matrix': prob_matrix
        }


if __name__ == "__main__":
    print(" Predicciones Mundial 2026 - Modelo de Regresión Poisson\n")
    
    # Datos simulados para prueba
    import pandas as pd
    sim_strengths = pd.DataFrame({
        'Team': ['Argentina', 'Mexico'],
        'Attack_Strength': [1.5, 1.1],
        'Defense_Strength': [0.7, 1.2]  # Menor = mejor defensa
    })
    sim_elo = pd.DataFrame({
        'Team': ['Argentina', 'Mexico'],
        'ELO': [2060, 1860]
    })
    
    model = PoissonModel(sim_strengths, sim_elo)
    result = model.predict_match('Argentina', 'Mexico')
    
    print(f"Partido: Argentina vs Mexico")
    print(f"Victoria Argentina: {result['home_win']*100:.1f}%")
    print(f"Empate:             {result['draw']*100:.1f}%")
    print(f"Victoria Mexico:    {result['away_win']*100:.1f}%")
    score = result['most_likely_score']
    print(f"Marcador probable:  Argentina {score[0]} - {score[1]} Mexico")
