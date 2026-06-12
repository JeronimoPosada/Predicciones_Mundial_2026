from src.collector import DataCollector
# Crear una instancia del colector
collector = DataCollector()

# Recolectar todos los datos del Mundial 2026
collector.collect_all_world_cup_data()

# Imprimir los datos recolectados
print("\n=== DATOS RECOLECTADOS ===")
print(f"Total de partidos: {len(collector.matches)}")
print(f"Fechas disponibles: {sorted(collector.date_range)}")