# =============================================================================
# IMPORTS
# =============================================================================
# Importamos las funciones de cálculo de seasonality y las de utilidades para leer el input
from seasonality import forecast_time_serie, autocorrelations
import utils as ut

# =============================================================================
# PIPELINE
# =============================================================================

def pipeline(serie: list, periodicity: int = 12) -> dict:
    if len(serie) <= 2 * periodicity:
        return {
            "pred_next_period": [],
            "acf_values": [],
            "pacf_values": []
        }

    pred_next_period = forecast_time_serie(serie, periodicity)
    acf_values, pacf_values = autocorrelations(serie)

    return {
        "pred_next_period": pred_next_period,
        "acf_values": acf_values,
        "pacf_values": pacf_values
    }

def combine_results(results: list) -> dict:
    return results[0] if results else {}

# =============================================================================
# PARAMETERS
# =============================================================================

def get_seasonality_input(filename: str) -> list:
    data = ut.read_excel(filename)
    cleaned_data = ut.clean_excel_input(data)
    sheet_name = ut.get_first_sheet_name(cleaned_data)
    serie = ut.get_sheet_values(cleaned_data, sheet_name)
    return ut.data_to_numeric(serie)

input_params = {
    "func": get_seasonality_input,
    "filename": "seasonality_example.xlsx"
}

tester_params = {
    "worker": pipeline,
    "combine_fn": combine_results,
    "input_data": None 
}