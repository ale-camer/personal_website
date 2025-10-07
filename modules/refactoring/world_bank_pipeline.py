# =============================================================================
# IMPORTS
# =============================================================================
import requests
import json
from datetime import datetime

# =============================================================================
# LÓGICA CENTRAL (Adaptada para el pipeline)
# =============================================================================

# Configuración centralizada
CONFIG = {
    "indicator_id": "NY.GDP.MKTP.CD", # GDP
    "urls": {
        "countries": "https://api.worldbank.org/v2/country",
        # URL formateada para llamar por país individualmente
        "indicator_by_country": "https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_id}"
    },
    "params": {
        "countries": {"format": "json", "per_page": 500},
        "indicator": {
            "format": "json",
            "date": f"1960:{datetime.now().year}",
            "per_page": 1000 # Por país, no necesitamos un per_page tan grande
        }
    }
}

def call_api(url: str, params: dict) -> list:
    """Función de ayuda para llamar a la API y manejar errores básicos."""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Lanza un error para códigos 4xx/5xx
        # La API del Banco Mundial devuelve una lista donde el segundo elemento [1] son los datos.
        data = response.json()
        return data[1] if isinstance(data, list) and len(data) > 1 else []
    except requests.exceptions.RequestException:
        # Si hay un error de red o de la API, devuelve una lista vacía.
        return []

# =============================================================================
# PIPELINE (Worker y Combine_fn)
# =============================================================================

def pipeline(country_code: str) -> list:
    """
    Este es el 'worker'. Recibe un código de país (ej: 'AR' para Argentina),
    llama a la API para obtener sus datos de PBI y los procesa.
    """
    url = CONFIG["urls"]["indicator_by_country"].format(
        country_code=country_code,
        indicator_id=CONFIG["indicator_id"]
    )
    
    raw_data = call_api(url, CONFIG["params"]["indicator"])

    # Procesa los datos crudos para extraer solo lo que necesitamos, filtrando valores nulos.
    processed_data = [
        (d['country']['value'], d['date'], d['value'])
        for d in raw_data if d.get('value') is not None
    ]
    
    return processed_data

def combine_results(results: list) -> list:
    """
    Esta es la 'combine_fn'. Recibe una lista de listas (una por cada país)
    y las aplana en una única lista con todos los resultados.
    """
    # [item for sublist in results for item in sublist] es una forma eficiente de aplanar la lista.
    return [item for sublist in results for item in sublist if sublist]

# =============================================================================
# PARAMETERS
# =============================================================================

def get_world_bank_input() -> list[str]:
    """
    Función para obtener los datos de entrada: una lista de códigos de países.
    Esta función se ejecuta una sola vez al principio.
    """
    print("Fetching country list from World Bank API...")
    raw_countries = call_api(CONFIG["urls"]["countries"], CONFIG["params"]["countries"])
    
    # Filtramos para obtener solo países (no agregados como 'América Latina y el Caribe')
    # y devolvemos sus códigos de 2 letras (ej: 'US', 'BR', 'DE').
    country_codes = [
        d['id'] for d in raw_countries
        if d.get('region', {}).get('value') != 'Aggregates'
    ]
    print(f"Found {len(country_codes)} countries.")
    return country_codes

# Parámetros para cargar los datos iniciales
input_params = {
    "func": get_world_bank_input,
}

# Parámetros para el Deployment, listos para ser usados
tester_params = {
    "worker": pipeline,

    "combine_fn": combine_results,
    "input_data": None # Se llenará dinámicamente
}