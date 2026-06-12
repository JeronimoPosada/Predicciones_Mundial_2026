"""
===================================================
collector.py - Fase 1: Recolección de Datos
===================================================
Este módulo se encarga de obtener datos de la API football-data.org
y guardarlos en archivos JSON para su posterior procesamiento.

"""

import json
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Importamos la configuración central

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import (
    API_BASE_URL, API_HEADERS, API_TOKEN,
    API_RATE_DELAY, RAW_DIR, WORLD_CUP_ID,
    WORLD_CUP_2026_TEAMS, COMPETITIONS
)


class DataCollector:
    
    #Recolector de datos de football-data.org API v4.

    def __init__(self):
        # Inicializa el collector.
        self.base_url = API_BASE_URL
        self.headers = API_HEADERS
        self.raw_dir = RAW_DIR
        self.request_count = 0
        
        # Verificar que tenemos API token
        if not API_TOKEN:
            print("ADVERTENCIA: No tienes API_TOKEN configurado.")
            print("   El programa puede funcionar con datos de respaldo,")
            print("   pero para datos en vivo necesitas registrarte en:")
            print("   https://www.football-data.org/client/register\n")

    def _make_request(self, endpoint, params=None):
        """
        Hace una petición GET a la API con control de rate limiting.
        
        Args:
            endpoint (str): La ruta del endpoint (ej: "/competitions/WC/matches")
            params (dict): Parámetros query opcionales
            
        Returns:
            dict: Los datos JSON de la respuesta, o None si hay error
        """
        url = f"{self.base_url}{endpoint}"
        
        # Rate limiting: esperar entre peticiones
        if self.request_count > 0:
            print(f"   Esperando {API_RATE_DELAY}s (rate limiting)...")
            time.sleep(API_RATE_DELAY)
        
        try:
            print(f"   GET {url}")
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            self.request_count += 1
            
            # Verificar el código de estado HTTP
            # 200 = OK, 401 = No autorizado, 403 = Prohibido, 429 = Demasiadas peticiones
            if response.status_code == 200:
                print(f"   Respuesta exitosa ({response.status_code})")
                return response.json()
            elif response.status_code == 429:
                print(f"   Rate limit alcanzado. Esperando 60s...")
                time.sleep(60)
                return self._make_request(endpoint, params)  # Reintentar
            elif response.status_code == 403:
                print(f"   Error 403: Recurso no disponible en plan gratuito")
                print(f"      Endpoint: {endpoint}")
                return None
            else:
                print(f"   Error HTTP {response.status_code}: {response.text[:200]}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"   Timeout: La petición tardó más de 30 segundos")
            return None
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Error de conexión: Verifica tu internet")
            return None
        except Exception as e:
            # 💡 TIP: Siempre captura excepciones genéricas como último
            # recurso, pero intenta capturar las específicas primero.
            print(f"   Error inesperado: {e}")
            return None

    def _save_json(self, data, filename):
        """
        Guarda datos en un archivo JSON.
        
        Args:
            data: Los datos a guardar
            filename (str): Nombre del archivo (sin ruta)
        """
        filepath = self.raw_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        # Calcular tamaño del archivo para feedback
        size_kb = filepath.stat().st_size / 1024
        print(f"   Guardado: {filename} ({size_kb:.1f} KB)")

    # ===========================================
    # MÉTODOS DE RECOLECCIÓN PRINCIPALES
    # ===========================================

    def fetch_competitions(self):
        """
        Obtiene la lista de competiciones disponibles.
        Útil para explorar qué datos tenemos acceso.
        
        Returns:
            dict: Lista de competiciones
        """
        print("\n Obteniendo lista de competiciones...")
        data = self._make_request("/competitions")
        if data:
            self._save_json(data, "competitions.json")
            count = data.get("count", 0)
            print(f"    {count} competiciones encontradas")
        return data

    def fetch_world_cup_matches(self):
        """
        Obtiene TODOS los partidos del Mundial 2026.
        Este es el dato más importante para nuestras predicciones.
        
        La API nos da partidos pasados Y futuros.
        Los pasados tienen marcador, los futuros están como "SCHEDULED".
        
        Returns:
            dict: Datos de partidos del Mundial
        """
        print("\n Obteniendo partidos del Mundial 2026...")
        data = self._make_request(f"/competitions/{WORLD_CUP_ID}/matches")
        if data:
            self._save_json(data, "world_cup_2026_matches.json")
            matches = data.get("matches", [])
            
            # Contar partidos por estado
            scheduled = sum(1 for m in matches if m.get("status") == "SCHEDULED")
            finished = sum(1 for m in matches if m.get("status") == "FINISHED")
            live = sum(1 for m in matches if m.get("status") in ["IN_PLAY", "PAUSED"])
            
            print(f"    Total: {len(matches)} partidos")
            print(f"       Finalizados: {finished}")
            print(f"       En vivo: {live}")
            print(f"       Programados: {scheduled}")
        return data

    def fetch_world_cup_standings(self):
        """
        Obtiene las tablas de posiciones actuales del Mundial.
        
        Returns:
            dict: Standings por grupo
        """
        print("\n Obteniendo tablas de posiciones del Mundial...")
        data = self._make_request(f"/competitions/{WORLD_CUP_ID}/standings")
        if data:
            self._save_json(data, "world_cup_2026_standings.json")
        return data

    def fetch_world_cup_teams(self):
        """
        Obtiene información de todos los equipos del Mundial.
        Incluye plantillas (jugadores) y datos del equipo.
        
        Returns:
            dict: Datos de equipos
        """
        print("\n Obteniendo equipos del Mundial...")
        data = self._make_request(f"/competitions/{WORLD_CUP_ID}/teams")
        if data:
            self._save_json(data, "world_cup_2026_teams.json")
            teams = data.get("teams", [])
            print(f"    {len(teams)} equipos encontrados")
        return data

    def fetch_world_cup_scorers(self):
        """
        Obtiene la tabla de goleadores del Mundial.
        
        Returns:
            dict: Lista de goleadores
        """
        print("\n🥅 Obteniendo tabla de goleadores del Mundial...")
        data = self._make_request(f"/competitions/{WORLD_CUP_ID}/scorers")
        if data:
            self._save_json(data, "world_cup_2026_scorers.json")
        return data

    def fetch_team_recent_matches(self, team_id, limit=20):
        """
        Obtiene los últimos partidos de un equipo específico.
        Esto nos sirve para calcular la forma reciente.
        
        La "forma reciente" es uno de los mejores
        predictores de rendimiento futuro en fútbol.
        
        Args:
            team_id (int): ID del equipo en la API
            limit (int): Número máximo de partidos
            
        Returns:
            dict: Partidos recientes del equipo
        """
        print(f"\n Obteniendo partidos recientes del equipo {team_id}...")
        data = self._make_request(
            f"/teams/{team_id}/matches",
            params={"limit": limit, "status": "FINISHED"}
        )
        if data:
            self._save_json(data, f"team_{team_id}_matches.json")
        return data

    def fetch_head_to_head(self, match_id):
        """
        Obtiene el historial de enfrentamientos directos
        para un partido específico.
        
        Los enfrentamientos directos (head-to-head) son
        valiosos porque algunas selecciones tienen "complejos"
        contra otras. Ejemplo: México vs Argentina en mundiales.
        
        Args:
            match_id (int): ID del partido en la API
            
        Returns:
            dict: Datos del partido incluyendo head-to-head
        """
        print(f"\n Obteniendo head-to-head del partido {match_id}...")
        data = self._make_request(f"/matches/{match_id}")
        if data:
            self._save_json(data, f"match_{match_id}_h2h.json")
        return data

    def fetch_competition_matches(self, competition_code, season=None):
        """
        Obtiene partidos de una competición específica.
        Útil para recolectar datos históricos de ligas.
        
        Args:
            competition_code (str): Código de la competición (PL, BL1, etc.)
            season (int): Año de la temporada (ej: 2024 para 2024/25)
            
        Returns:
            dict: Partidos de la competición
        """
        comp_id = COMPETITIONS.get(competition_code, {}).get("id")
        if not comp_id:
            print(f"    Competición '{competition_code}' no encontrada")
            return None
        
        params = {}
        if season:
            params["season"] = season
        
        comp_name = COMPETITIONS[competition_code]["name"]
        season_str = f" (temporada {season})" if season else ""
        print(f"\n Obteniendo partidos de {comp_name}{season_str}...")
        
        data = self._make_request(f"/competitions/{comp_id}/matches", params=params)
        if data:
            filename = f"competition_{competition_code}"
            if season:
                filename += f"_{season}"
            filename += "_matches.json"
            self._save_json(data, filename)
        return data

    # ===========================================
    # MÉTODO PRINCIPAL: RECOLECCIÓN COMPLETA
    # ===========================================

    def collect_all_world_cup_data(self):
        """
        Ejecuta la recolección completa de datos del Mundial.
        
        
        Returns:
            dict: Resumen de datos recolectados
        """
        print("=" * 60)
        print(" RECOLECCIÓN DE DATOS - MUNDIAL 2026")
        print("=" * 60)
        start_time = time.time()
        
        results = {
            "competitions": None,
            "matches": None,
            "standings": None,
            "teams": None,
            "scorers": None,
        }
        
        # 1. Competiciones disponibles
        results["competitions"] = self.fetch_competitions()
        
        # 2. Partidos del Mundial
        results["matches"] = self.fetch_world_cup_matches()
        
        # 3. Tablas de posiciones
        results["standings"] = self.fetch_world_cup_standings()
        
        # 4. Equipos y plantillas
        results["teams"] = self.fetch_world_cup_teams()
        
        # 5. Goleadores
        results["scorers"] = self.fetch_world_cup_scorers()
        
        # Resumen final
        elapsed = time.time() - start_time
        successful = sum(1 for v in results.values() if v is not None)
        
        print(f"\n{'=' * 60}")
        print(f" RECOLECCIÓN COMPLETADA")
        print(f"   Exitosas: {successful}/{len(results)}")
        print(f"   Peticiones: {self.request_count}")
        print(f"   Tiempo: {elapsed:.1f} segundos")
        print(f"   Datos guardados en: {self.raw_dir}")
        print(f"{'=' * 60}\n")
        
        return results

    def collect_historical_data(self):
        """
        Recolecta datos históricos de mundiales anteriores
        para mejorar el modelo.
        
        Más datos históricos = mejor modelo.
        Pero cuidado: datos muy antiguos (pre-2010) pueden
        no ser representativos del fútbol moderno.
        """
        print("=" * 60)
        print(" RECOLECCIÓN DE DATOS HISTÓRICOS")
        print("=" * 60)
        
        # Mundiales anteriores disponibles en la API
        historical_seasons = [2022, 2018, 2014]
        
        for season in historical_seasons:
            print(f"\n--- Mundial {season} ---")
            data = self._make_request(
                f"/competitions/{WORLD_CUP_ID}/matches",
                params={"season": season}
            )
            if data:
                self._save_json(data, f"world_cup_{season}_matches.json")
                matches = data.get("matches", [])
                print(f"    {len(matches)} partidos encontrados")
        
        print(f"\n Datos históricos completados")


# ===================================================
# DATOS DE RESPALDO (por si no tienes API key)
# ===================================================
# Si la API falla o no tienes key, el programa debe
# seguir funcionando con datos de respaldo.

def create_fallback_data():
    """
    Crea datos mínimos de respaldo si no se puede acceder a la API.
    Estos datos son aproximados pero permiten que el modelo funcione.
    """
    print("\n Creando datos de respaldo...")
    
    # Generar los partidos de la fase de grupos basados en config
    matches = []
    match_id = 1
    
    # Fechas del Mundial 2026 (fase de grupos)
    group_dates = {
        1: "2026-06-11",  # Jornada 1
        2: "2026-06-16",  # Jornada 2
        3: "2026-06-21",  # Jornada 3
    }
    
    for group_letter, teams in WORLD_CUP_2026_TEAMS.items():
        # Cada grupo tiene 6 partidos (4 equipos, todos contra todos... 
        # no, son 3 jornadas: 2 partidos por jornada)
        # Jornada 1: 1v4, 2v3
        # Jornada 2: 1v3, 4v2
        # Jornada 3: 1v2, 3v4
        group_matches = [
            (0, 3, 1), (1, 2, 1),  # Jornada 1
            (0, 2, 2), (3, 1, 2),  # Jornada 2
            (0, 1, 3), (2, 3, 3),  # Jornada 3
        ]
        
        for home_idx, away_idx, matchday in group_matches:
            matches.append({
                "id": match_id,
                "utcDate": f"{group_dates[matchday]}T18:00:00Z",
                "status": "SCHEDULED",
                "matchday": matchday,
                "stage": "GROUP_STAGE",
                "group": f"GROUP_{group_letter}",
                "homeTeam": {
                    "id": match_id * 100 + home_idx,
                    "name": teams[home_idx]["name"],
                    "tla": teams[home_idx]["code"]
                },
                "awayTeam": {
                    "id": match_id * 100 + away_idx,
                    "name": teams[away_idx]["name"],
                    "tla": teams[away_idx]["code"]
                },
                "score": {
                    "winner": None,
                    "fullTime": {"home": None, "away": None},
                    "halfTime": {"home": None, "away": None}
                }
            })
            match_id += 1
    
    fallback = {
        "count": len(matches),
        "competition": {
            "id": 2000,
            "name": "FIFA World Cup",
            "code": "WC"
        },
        "matches": matches,
        "_source": "fallback_generated",
        "_generated_at": datetime.now().isoformat()
    }
    
    filepath = RAW_DIR / "world_cup_2026_matches.json"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(fallback, f, indent=4, ensure_ascii=False)
    
    print(f"   Generados {len(matches)} partidos de fase de grupos")
    print(f"   Guardado en: {filepath}")
    
    return fallback


# ===================================================
# EJECUCIÓN DIRECTA
# ===================================================

if __name__ == "__main__":
    print(" Predicciones Mundial 2026 - Recolector de Datos\n")
    
    collector = DataCollector()
    
    if API_TOKEN:
        print(" API Token detectado. Recolectando datos en vivo...\n")
        collector.collect_all_world_cup_data()
    else:
        print("  Sin API Token. Generando datos de respaldo...\n")
        print("   Para obtener datos reales:")
        print("   1. Regístrate en https://www.football-data.org/client/register")
        print("   2. Agrega API_TOKEN=tu_token al archivo .env")
        print("   3. Vuelve a ejecutar este script\n")
        create_fallback_data()
    
    print("\n Fase 1 completada. Ejecuta processor.py para la Fase 2.")
