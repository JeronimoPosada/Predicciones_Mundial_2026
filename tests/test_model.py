import unittest
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.model import PoissonModel


class TestPoissonModel(unittest.TestCase):
    def setUp(self):
        self.sim_strengths = pd.DataFrame({
            'Team': ['Argentina', 'Mexico'],
            'Attack_Strength': [1.5, 1.1],
            'Defense_Strength': [0.7, 1.2]
        })
        self.sim_elo = pd.DataFrame({
            'Team': ['Argentina', 'Mexico'],
            'ELO': [2060, 1860]
        })
        self.model = PoissonModel(self.sim_strengths, self.sim_elo)

    def test_probabilities_sum_to_one(self):
        """Las probabilidades de victoria, empate y derrota deben sumar aprox 1.0"""
        result = self.model.predict_match('Argentina', 'Mexico')
        total_prob = result['home_win'] + result['draw'] + result['away_win']
        self.assertAlmostEqual(total_prob, 1.0, places=2)

    def test_stronger_team_higher_prob(self):
        """Un equipo con mejor ataque y defensa debe tener mayor prob de ganar"""
        result = self.model.predict_match('Argentina', 'Mexico')
        self.assertGreater(result['home_win'], result['away_win'])

    def test_dixon_coles_adjustment(self):
        """Verifica que el ajuste de Dixon-Coles se aplique a los empates 0-0"""
        rho = 0.03
        lambdax = 1.0
        lambday = 1.0
        adj = self.model._rho_correction(0, 0, lambdax, lambday, rho)
        self.assertLess(adj, 1.0) # Con rho positivo, 0-0 debería tener un ajuste negativo o viceversa dependiendo de la formula
        

if __name__ == '__main__':
    unittest.main()
