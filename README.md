# 🏆 Predictor del Mundial 2026

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Un sistema de predicción estadística basado en **Regresión de Poisson** y **ratings ELO** para pronosticar resultados de partidos del Mundial de Fútbol 2026. El modelo combina metodología tradicional de análisis deportivo con técnicas de machine learning para generar predicciones probabilísticas realistas.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Instalación](#instalación)
- [Uso Rápido](#uso-rápido)
- [Arquitectura](#arquitectura)
- [Modelo Matemático](#modelo-matemático)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [API](#api)
- [Configuración](#configuración)
- [Testing](#testing)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## 🚀 Características

| Característica | Descripción |
|---|---|
| **Recolección de Datos** | Consumo automatizado de la API de [football-data.org](https://www.football-data.org) con manejo de límites de rate |
| **ETL Completo** | Limpieza, validación y transformación de datos usando `pandas` |
| **Feature Engineering** | Cálculo automático de fuerzas ofensivas/defensivas, sistema ELO dinámico y estadísticas por equipo |
| **Modelo Predictivo** | Regresión de Poisson con ajuste Dixon-Coles para precisión en empates |
| **Interfaz CLI** | Menú interactivo fácil de usar para predicciones sin necesidad de escribir código |
| **Modo Fallback** | Generación de datos sintéticos cuando no hay acceso a API |
| **Escalable** | Arquitectura modular preparada para extensiones futuras |

## 💻 Instalación

### Requisitos Previos
- Python 3.10 o superior
- pip o conda
- Git (opcional)

### Pasos

#### 1. Clonar o descargar el repositorio
```bash
git clone https://github.com/tu-usuario/predicciones_mundial.git
cd predicciones_mundial
```

#### 2. Crear un entorno virtual
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 4. (Opcional pero Recomendado) Configurar API Key

Crea un archivo `.env` en la raíz del proyecto:

```env
# .env
API_TOKEN=tu_token_gratuito_aqui
API_BASE_URL=https://api.football-data.org/v4
```

Obtén tu token gratuito en: [football-data.org/client/register](https://www.football-data.org/client/register)

**Sin API Key:** El sistema generará datos de simulación automáticamente.

## 🏃‍♂️ Uso Rápido

### Iniciar la interfaz interactiva
```bash
python main.py
```

### Menú Principal
```
═══════════════════════════════════════
   MUNDIAL 2026 - PREDICTOR ESTADÍSTICO
═══════════════════════════════════════

1. Actualizar Datos
2. Predecir Partido Individual
3. Predecir Todos los Partidos de un Grupo
4. Salir

Selecciona una opción (1-4):
```

### Ejemplos de Uso

**Opción 1: Actualizar Datos**
- Descarga los últimos resultados y estadísticas
- Recalcula fuerzas ofensivas/defensivas
- Actualiza ratings ELO de todos los equipos
- ⏱️ Tiempo: ~10-20 segundos con API

**Opción 2: Predecir Partido**
```
Equipo Local: Argentina
Equipo Visitante: Mexico

═══════════════════════════════════════
📊 PREDICCIÓN: Argentina vs Mexico
═══════════════════════════════════════

Probabilidades:
  🏆 Victoria Argentina:  68.5%
  🤝 Empate:            18.2%
  🔴 Victoria Mexico:   13.3%

Marcador Esperado:
  Argentina: 2.1 goles
  Mexico:   0.9 goles

Top 5 Marcadores Más Probables:
  1. 2-0 (15.4%)
  2. 1-0 (13.8%)
  3. 2-1 (11.2%)
  4. 3-0 (9.7%)
  5. 1-1 (8.3%)
```

**Opción 3: Predecir Grupo**
- Simula todos los encuentros de un grupo (6 partidos)
- Muestra probabilidades para cada encuentro
- Estima puntos finales y clasificados

## 🏛️ Arquitectura

```
predicciones_mundial/
├── main.py                      # Entry point - CLI interactiva
├── config.py                    # Configuración centralizada
├── requirements.txt             # Dependencias
├── .env                         # Variables de entorno (no versionado)
├── .gitignore
├── README.md                    # Este archivo
│
├── src/                         # Módulos principales
│   ├── __init__.py
│   ├── collector.py             # [Fase 1] Recolección de datos
│   ├── processor.py             # [Fase 2] Limpieza y procesamiento
│   ├── features.py              # [Fase 3] Ingeniería de características
│   ├── model.py                 # [Fase 4] Modelo predictivo
│   └── predictor.py             # [Fase 5] Interfaz de predicción
│
├── data/
│   ├── raw/                     # Datos descargados de API
│   │   └── world_cup_2026_matches.json
│   └── processed/               # Datos transformados
│       ├── matches.csv
│       └── teams.csv
│
└── tests/
    ├── __init__.py
    └── test_model.py            # Tests unitarios del modelo
```

### Pipeline de Procesamiento

```
[1. Collector] → Descarga datos de API
      ↓
[2. Processor] → Limpia y valida datos (CSV)
      ↓
[3. Features] → Calcula fuerzas y ELO
      ↓
[4. Model] → Genera predicciones
      ↓
[5. Predictor] → Interfaz de usuario
```

## 🧠 Modelo Matemático

El sistema utiliza metodología estándar en la industria del análisis deportivo:

### 1️⃣ Sistema ELO

Actualiza la "fuerza general" de cada selección tras cada partido:

$$E_i = E_i^{old} + K \cdot (R - P)$$

Donde:
- $E_i$ = Rating ELO del equipo
- $K$ = Factor de ajuste (32 para mundiales)
- $R$ = Resultado real (1=victoria, 0.5=empate, 0=derrota)
- $P$ = Probabilidad esperada de victoria

### 2️⃣ Cálculo de Lambda (λ) - Goles Esperados

$$\lambda_{home} = \lambda_0 \cdot \text{Ataque}_{home} \cdot \text{Defensa}_{away} \cdot e^{0.0065 \cdot (ELO_{home} - ELO_{away})} \cdot 1.3_{ventaja\_local}$$

Donde:
- $\lambda_0$ = Media global de goles (~1.3 en mundiales)
- Ataque/Defensa = Fuerzas relativas de cada equipo
- ELO = Diferencia de ratings entre equipos

### 3️⃣ Distribución de Poisson

Probabilidad de exactamente $k$ goles:

$$P(X=k) = \frac{e^{-\lambda} \lambda^k}{k!}$$

Se calcula para ambos equipos y se genera matriz de probabilidades de marcadores.

### 4️⃣ Ajuste Dixon-Coles

Corrección para empates de bajo marcador (0-0, 1-1) que Poisson puro subestima:

$$P(x,y) = P_{\text{Poisson}}(x,y) \cdot \rho^{x,y}$$

Donde $\rho$ es un factor de ajuste (~0.03 en fútbol).

## 📁 Estructura del Proyecto

### Módulos Principales

#### `collector.py` - Recolección de Datos
```python
# Descarga datos de football-data.org
collector = DataCollector()
collector.collect_all_world_cup_data()  # Requiere API Key

# O genera datos sintéticos
create_fallback_data()
```

#### `processor.py` - Procesamiento
```python
# Limpia y valida datos
processor = DataProcessor()
processor.process_matches()      # CSV limpio de partidos
processor.get_team_list()        # Extrae lista de equipos
```

#### `features.py` - Feature Engineering
```python
# Calcula estadísticas y ELO
engineer = FeatureEngineer()
engineer.calculate_team_strengths()    # Fuerzas ofensivas/defensivas
engineer.calculate_elo_ratings()       # Ratings dinámicos
```

#### `model.py` - Modelo Predictivo
```python
# Realiza predicciones
model = PoissonModel(strengths_df, elo_df)
prediction = model.predict_match('Argentina', 'Mexico')
# {'home_win': 0.685, 'draw': 0.182, 'away_win': 0.133, ...}
```

#### `predictor.py` - Interfaz
```python
# Orquesta todo el flujo
predictor = WorldCupPredictor()
predictor.display_prediction('Argentina', 'Mexico')
```

## 🔌 API de Uso Programático

Para usar el predictor en tu propio código:

```python
from src.processor import DataProcessor
from src.features import FeatureEngineer
from src.model import PoissonModel

# 1. Cargar datos procesados
processor = DataProcessor()
matches_df = processor.process_matches()

# 2. Calcular características
engineer = FeatureEngineer()
strengths = engineer.calculate_team_strengths()
elo = engineer.calculate_elo_ratings()

# 3. Crear modelo
model = PoissonModel(strengths, elo)

# 4. Predecir
result = model.predict_match('Argentina', 'Mexico', is_neutral=False)

print(f"Victoria Argentina: {result['home_win']:.1%}")
print(f"Empate: {result['draw']:.1%}")
print(f"Victoria Mexico: {result['away_win']:.1%}")
```

## ⚙️ Configuración

Edita `config.py` para ajustar parámetros:

```python
# Rutas de datos
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Parámetros del modelo
POISSON_MAX_GOALS = 10              # Máximo de goles en matriz
HOME_ADVANTAGE = 1.3                # Factor de ventaja local
DIXON_COLES_RHO = 0.03              # Ajuste para empates 0-0
ELO_K_FACTOR = 32                   # Ajuste ELO en mundiales

# API
API_RATE_LIMIT = 10                 # Requests por minuto
API_RATE_DELAY = 6.5                # Segundos entre requests
```

## 🧪 Testing

Ejecutar tests unitarios:

```bash
# Todos los tests
python -m pytest tests/

# Tests específicos
python -m pytest tests/test_model.py -v

# Con coverage
python -m pytest tests/ --cov=src
```

Tests disponibles:
- ✅ Probabilidades suman a 1.0
- ✅ Equipo fuerte tiene mayor probabilidad de ganar
- ✅ Ajuste Dixon-Coles aplicado correctamente

## 📊 Datos Esperados

### Carpeta `data/processed/`

**`matches.csv`**
```
Date,Home_Team,Away_Team,Home_Goals,Away_Goals,Home_xG,Away_xG,Competition
2023-01-15,Argentina,Mexico,2,1,1.8,0.9,WC Qualifier
...
```

**`teams.csv`**
```
Team,Matches_Played,Wins,Draws,Losses,Goals_For,Goals_Against
Argentina,45,28,10,7,95,42
Mexico,48,20,12,16,68,55
...
```

## 🔍 Limitaciones Conocidas

1. **Dependencia de API:** Requiere API Key para datos reales (plan gratuito limitado a 10 req/min)
2. **Datos históricos:** Precisión depende de historial de partidos disponibles
3. **Equipos nuevos:** Selecciones sin historial usan valores por defecto
4. **No considera:** Lesiones, cambios de entrenador, fatiga por viajes
5. **Partidos neutrales:** El modelo asume ventaja local; usar `is_neutral=True` para neutralizar

## 🚀 Mejoras Futuras

- [ ] Integración de más fuentes de datos (Elo.football, WhoScored)
- [ ] Dashboard web interactivo (Flask/Streamlit)
- [ ] Predicción de alineaciones probables
- [ ] Análisis de tendencias históricas
- [ ] Machine Learning (XGBoost, Neural Networks)
- [ ] API REST para integración externa
- [ ] Docker container para deployment

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Agrega mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para detalles.

## 👤 Autor
**Jerónimo Posada Gil**
**Desarrollado como proyecto de Data Science**

## 📞 Soporte

Si encuentras problemas:
1. Revisa el archivo `.env` (API Key correcta)
2. Verifica que `data/processed/` exista con archivos CSV
3. Ejecuta `python main.py` y selecciona "Actualizar Datos"

---

**Última actualización:** Junio 2026  
**Estado:** ✅ Funcional y listo para producción
