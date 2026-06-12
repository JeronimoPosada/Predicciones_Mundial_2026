"""
===================================================
config.py - Configuración Central del Proyecto
===================================================
Aquí centralizamos TODAS las constantes y configuraciones.

"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ===================================================
# RUTAS DEL PROYECTO
# ===================================================
# Path.resolve() nos da la ruta absoluta sin importar desde dónde ejecutemos
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Crear directorios si no existen
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ===================================================
# API FOOTBALL-DATA.ORG
# ===================================================
API_BASE_URL = os.getenv("API_BASE_URL", "")
API_TOKEN = os.getenv("API_TOKEN", "")

# Headers para las peticiones a la API
API_HEADERS = {
    "X-Auth-Token": API_TOKEN
}

# Límite de peticiones por minuto (plan gratuito)
API_RATE_LIMIT = 10
API_RATE_DELAY = 6.5  # segundos entre peticiones (para no exceder el límite)

# ===================================================
# COMPETICIONES DISPONIBLES (Plan Gratuito)
# ===================================================
# La API gratuita da acceso a estas competiciones:
COMPETITIONS = {
    "WC": {"id": 2000, "name": "FIFA World Cup"},
    "CL": {"id": 2001, "name": "UEFA Champions League"},
    "PL": {"id": 2021, "name": "Premier League"},
    "BL1": {"id": 2002, "name": "Bundesliga"},
    "SA": {"id": 2019, "name": "Serie A"},
    "PD": {"id": 2014, "name": "La Liga"},
    "FL1": {"id": 2015, "name": "Ligue 1"},
    "DED": {"id": 2003, "name": "Eredivisie"},
    "PPL": {"id": 2017, "name": "Primeira Liga"},
    "ELC": {"id": 2016, "name": "Championship"},
    "BSA": {"id": 2013, "name": "Brasileirão Serie A"},
    "EC": {"id": 2018, "name": "European Championship"},
}

# El Mundial 2026 es el que nos interesa
WORLD_CUP_ID = 2000
WORLD_CUP_CODE = "WC"

# ===================================================
# EQUIPOS DEL MUNDIAL 2026 (48 selecciones)
# ===================================================
WORLD_CUP_2026_TEAMS = {
    # --- GRUPO A ---
    "A": [
        {"name": "México", "code": "MEX", "confederation": "CONCACAF"},
        {"name": "Corea del Sur", "code": "KOR", "confederation": "AFC"},
        {"name": "Sudáfrica", "code": "RSA", "confederation": "CAF"},
        {"name": "República Checa", "code": "CZE", "confederation": "UEFA"},
    ],
    # --- GRUPO B ---
    "B": [
        {"name": "Canadá", "code": "CAN", "confederation": "CONCACAF"},
        {"name": "Suiza", "code": "SUI", "confederation": "UEFA"},
        {"name": "Qatar", "code": "QAT", "confederation": "AFC"},
        {"name": "Bosnia and Herzegovina", "code": "BIH", "confederation": "UEFA"},
    ],
    # --- GRUPO C ---
    "C": [
        {"name": "Brasil", "code": "BRA", "confederation": "CONMEBOL"},
        {"name": "Marruecos", "code": "MAR", "confederation": "CAF"},
        {"name": "Haiti", "code": "HAI", "confederation": "CONCACAF"},
        {"name": "Escocia", "code": "SCO", "confederation": "UEFA"},
    ],
    # --- GRUPO D ---
    "D": [
        {"name": "Estados Unidos", "code": "USA", "confederation": "CONCACAF"},
        {"name": "Paraguay", "code": "PAR", "confederation": "CONMEBOL"},
        {"name": "Australia", "code": "AUS", "confederation": "AFC"},
        {"name": "Turquía", "code": "TUR", "confederation": "UEFA"},
    ],
    # --- GRUPO E ---
    "E": [
        {"name": "Alemania", "code": "GER", "confederation": "UEFA"},
        {"name": "Curazao", "code": "CUW", "confederation": "CONCACAF"},
        {"name": "Costa de Marfil", "code": "CIV", "confederation": "CAF"},
        {"name": "Ecuador", "code": "ECU", "confederation": "CONMEBOL"},
    ],
    # --- GRUPO F ---
    "F": [
        {"name": "Países Bajos", "code": "NED", "confederation": "UEFA"},
        {"name": "Japón", "code": "JPN", "confederation": "AFC"},
        {"name": "Suecia", "code": "SWE", "confederation": "UEFA"},
        {"name": "Túnez", "code": "TUN", "confederation": "CAF"},
    ],
    # --- GRUPO G ---
    "G": [
        {"name": "Bélgica", "code": "BEL", "confederation": "UEFA"},
        {"name": "Egipto", "code": "EGY", "confederation": "CAF"},
        {"name": "Irán", "code": "IRN", "confederation": "AFC"},
        {"name": "Nueva Zelanda", "code": "NZL", "confederation": "OFC"},
    ],
    # --- GRUPO H ---
    "H": [
        {"name": "España", "code": "ESP", "confederation": "UEFA"},
        {"name": "Cabo Verde", "code": "CPV", "confederation": "CAF"},
        {"name": "Arabia Saudita", "code": "KSA", "confederation": "AFC"},
        {"name": "Uruguay", "code": "URU", "confederation": "CONMEBOL"},
    ],
    # --- GRUPO I ---
    "I": [
        {"name": "Francia", "code": "FRA", "confederation": "UEFA"},
        {"name": "Irak", "code": "IRQ", "confederation": "AFC"},
        {"name": "Noruega", "code": "NOR", "confederation": "UEFA"},
        {"name": "Senegal", "code": "SEN", "confederation": "CAF"},
    ],
    # --- GRUPO J ---
    "J": [
        {"name": "Argelia", "code": "ALG", "confederation": "CAF"},
        {"name": "Argentina", "code": "ARG", "confederation": "CONMEBOL"},
        {"name": "Austria", "code": "AUT", "confederation": "UEFA"},
        {"name": "Jordania", "code": "JOR", "confederation": "AFC"},
    ],
    # --- GRUPO K ---
    "K": [
        {"name": "Portugal", "code": "POR", "confederation": "UEFA"},
        {"name": "República Democrática del Congo", "code": "COD", "confederation": "CAF"},
        {"name": "Uzbekistán", "code": "UZB", "confederation": "AFC"},
        {"name": "Colombia", "code": "COL", "confederation": "CONMEBOL"},
    ],
    # --- GRUPO L ---
    "L": [
        {"name": "Inglaterra", "code": "ENG", "confederation": "UEFA"},
        {"name": "Croacia", "code": "CRO", "confederation": "UEFA"},
        {"name": "Ghana", "code": "GHA", "confederation": "CAF"},
        {"name": "Panamá", "code": "PAN", "confederation": "CONCACAF"},
    ],
}

# ===================================================
# ELO RATINGS INICIALES (Aproximados - Junio 2026)
# ===================================================

INITIAL_ELO_RATINGS = {
    "Argentina": 2060, "Francia": 2040, "Brasil": 2000, "Inglaterra": 1990,
    "España": 1985, "Alemania": 1960, "Países Bajos": 1950, "Portugal": 1945,
    "Bélgica": 1940, "Croacia": 1920, "Uruguay": 1910, "Colombia": 1900,
    "Estados Unidos": 1870, "México": 1860, "Marruecos": 1855, "Suiza": 1850,
    "Japón": 1845, "Senegal": 1835, "Turquía": 1830, "Corea del Sur": 1825,
    "Suecia": 1800, "Canadá": 1800, "Ecuador": 1795, "Australia": 1785,
    "Egipto": 1780, "Irán": 1770, "Noruega": 1750, "Austria": 1750,
    "República Checa": 1750, "Argelia": 1750, "Escocia": 1700, "Paraguay": 1755,
    "Costa de Marfil": 1700, "Arabia Saudita": 1710, "Uzbekistán": 1685,
    "Catar": 1680, "Túnez": 1650, "Bosnia y Herzegovina": 1650,
    "Ghana": 1650, "República Democrática del Congo": 1650, "Sudáfrica": 1600, "Cabo Verde": 1600,
    "Nueva Zelanda": 1570, "Irak": 1550, "Jordania": 1550, "Haití": 1500,
    "Curazao": 1450, "Panamá": 1720
}

# ===================================================
# PARÁMETROS DEL MODELO
# ===================================================
# Factor K para el sistema ELO (controla la velocidad de ajuste)
ELO_K_FACTOR = {
    "world_cup": 60,        # Mundiales: máximo peso
    "continental": 50,      # Copas continentales: peso alto
    "qualifier": 40,        # Eliminatorias: peso medio-alto
    "friendly": 20,         # Amistosos: peso bajo
}

# Pesos para el modelo Poisson
POISSON_MAX_GOALS = 8  # Máximo de goles a considerar en la matriz
HOME_ADVANTAGE = 1.15   # Factor de ventaja local (15% más probable de anotar)

# Ajuste Dixon-Coles para empates de bajo marcador
DIXON_COLES_RHO = 0.03  # Factor de corrección para 0-0 y 1-1

# ===================================================
# CONFIGURACIÓN DE DISPLAY
# ===================================================
# Colores para la consola (ANSI escape codes)
COLORS = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "CYAN": "\033[96m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
    "END": "\033[0m",
}


def print_config_status():
    """
    Muestra el estado de la configuración.
    Útil para verificar que todo está bien antes de empezar.
    
    """
    print(f"\n{'='*50}")
    print(f" Predicciones Mundial 2026 - Config Status")
    print(f"{'='*50}")
    print(f" Base dir:      {BASE_DIR}")
    print(f" Data raw:      {RAW_DIR}")
    print(f" Data processed: {PROCESSED_DIR}")
    print(f" API URL:       {API_BASE_URL}")
    print(f" API Token:     {' Configurado' if API_TOKEN else ' NO configurado'}")
    print(f"⚽ Equipos:       {sum(len(v) for v in WORLD_CUP_2026_TEAMS.values())} selecciones")
    print(f"📊 Grupos:        {len(WORLD_CUP_2026_TEAMS)}")
    print(f"{'='*50}\n")

    if not API_TOKEN:
        print("  ADVERTENCIA: No tienes API_TOKEN configurado.")
        print("   1. Regístrate en: https://www.football-data.org/client/register")
        print("   2. Agrega tu token al archivo .env:")
        print("      API_TOKEN=tu_token_aqui\n")


# Si ejecutamos este archivo directamente, muestra el estado
if __name__ == "__main__":
    print_config_status()
