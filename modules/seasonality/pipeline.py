# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
from threading import Thread

# --- Third-party ---

# --- Project ---
from . import core
from . import visuals as viz
import modules.common.utils as ut
import modules.common.validations as val

# =============================================================================
# CORE
# =============================================================================
def load_and_clean(file: str) -> list:

    data = ut.read_excel(file)
    try:
        val.validate_number_of_sheets(data)
    except val.TooManySheetsError as e:
        print("Caught error:", e)

    cleaned_data = ut.clean_excel_input(data)
    try:
        val.validate_number_of_columns(cleaned_data)
    except val.TooManyColumnsError as e:
        print("Caught error:", e)

    sheet_name = ut.get_first_sheet_name(cleaned_data)
    serie = ut.get_sheet_values(cleaned_data, sheet_name)
    try:
        val.validate_data_type(serie)
    except val.NonNumericValueError as e:
        print("Caught error:", e)

    return ut.data_to_numeric(serie)

def pipeline(file: str, p: int, nlags: int, save_dir: str):

    print("\nINITIATING DATA VALIDATION")
    results, serie = {}, load_and_clean(file)

    print("\nINITIATING PROCESS")
    print("Calculating Predictions")
    def forecast_last():
        results['pred_last'] = core.forecast_time_serie(serie[:-p], p)
    def forecast_next():
        results['pred_next'] = core.forecast_time_serie(serie, p)
    def acf_pacf():
        results['acf'], results['pacf'] = core.autocorrelations(serie, nlags)

    threads = [
        Thread(target=forecast_last),
        Thread(target=forecast_next),
        Thread(target=acf_pacf)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("Printing Plots")
    viz.plot_forecasts(serie, results['pred_last'], results['pred_next'], p, save_dir)
    viz.plot_acf_pacf(results['acf'], results['pacf'], save_dir)
    print("PROCESS COMPLETED")

    return results['pred_last'], results['acf'], results['pacf']
