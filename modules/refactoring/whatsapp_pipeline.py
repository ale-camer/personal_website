# =============================================================================
# IMPORTS
# =============================================================================
import re
from datetime import datetime
from collections import Counter

# Importamos las funciones necesarias de tus otros módulos
from utils import read_txt
from deployment import get_generic_output

# =============================================================================
# LÓGICA CENTRAL (Copiada de whatsapp.py para mantenerlo autocontenido)
# =============================================================================

def clean_message(data: list[str]) -> iter:
    """
    Toma una lista de líneas (un fragmento del chat) y las procesa,
    validando y parseando cada una. Devuelve un generador con los datos parseados.
    """
    SPLIT_STR = r'^(\d{1,2}/\d{1,2}/\d{2,4}), ([^ ]+) - ([^:]+): (.+)$'
    PARSE_STR = r".*\/.*\/.*,.*:.* - .*"

    def is_valid(line: str) -> bool:
        generic_match = re.compile(PARSE_STR).match(line)
        specific_match = re.compile(SPLIT_STR).match(line)

        if not (generic_match and specific_match):
            return False

        _, _, _, msg = specific_match.groups()
        if msg.strip().startswith('<') and msg.strip().endswith('>'):
            return False
        return True

    def parse_line(line: str) -> tuple:
        generic_match = re.compile(SPLIT_STR).match(line)
        date, time, issuer, msg = generic_match.groups()
        date = datetime.strptime(date, "%d/%m/%Y")
        return (
            date, int(time[:2]), issuer.strip(), msg.strip(),
            date.weekday(), date.day, date.month, msg.count(" ")+1
        )

    # Devuelve un generador para ser eficiente en memoria
    yield from (parse_line(d) for d in data if is_valid(d))

def groupby_dict(data: list) -> Counter:
    """
    Toma los datos ya parseados de un fragmento y realiza la operación de conteo.
    Se ha eliminado tqdm ya que el executor se encarga de la barra de progreso.
    """
    return Counter(
        f"{prefix}{'_'.join(str(row[i]) for i in idxs)}"
        for row in data
        for prefix, idxs in [("", [2,1,4,5,6]), ("GENERAL_", [1,4,5,6])]
    )

# =============================================================================
# PIPELINE (Worker y Combine_fn)
# =============================================================================

def pipeline(data_chunk: list[str]) -> Counter:
    """
    Este es el 'worker'. Procesa un fragmento del archivo de WhatsApp.
    Primero limpia y parsea los mensajes, y luego los agrupa y cuenta.
    """
    # Usamos list() para consumir el generador de clean_message
    cleaned_data = list(clean_message(data_chunk))
    
    # Si el fragmento no contiene mensajes válidos, devuelve un Counter vacío
    if not cleaned_data:
        return Counter()
    
    # Devuelve el Counter con los datos agrupados para este fragmento
    return groupby_dict(cleaned_data)

def combine_results(results: list) -> dict:
    """
    Esta es la 'combine_fn'. Recibe una lista de Counters (uno por cada worker)
    y los suma para obtener un único Counter final.
    """
    final_counter = Counter()
    # Itera sobre cada Counter parcial devuelto por los workers
    for partial_counter in results:
        # El método .update() de Counter está diseñado para sumar los conteos
        final_counter.update(partial_counter)
    
    # Devuelve el Counter final y unificado
    return final_counter

# =============================================================================
# PARAMETERS
# =============================================================================

def get_whatsapp_input(filename: str) -> list[str]:
    """Función de ayuda para leer el archivo y dividirlo en líneas."""
    return read_txt(filename).splitlines()

# Parámetros para cargar los datos iniciales
input_params = {
    "func": get_whatsapp_input,
    "filename": "whatsapp_chat.txt"
}

# Parámetros para el Deployment, listos para ser usados
tester_params = {
    "worker": pipeline,
    "combine_fn": combine_results,
    "input_data": None  # Se llenará dinámicamente al ejecutar
}