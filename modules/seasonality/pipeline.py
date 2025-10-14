# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
from threading import Thread

# --- Third-party ---

# --- Project ---
from .core import forecast_time_serie, autocorrelations
from .visuals import plot_forecasts, plot_acf_pacf
from modules.common.utils import (
    read_excel, clean_excel_input, get_first_sheet_name, get_sheet_values, 
    data_to_numeric, timed_run
)
from modules.common.validations import (
    validate_number_of_columns, validate_number_of_sheets,
    NonNumericValueError, TooManyColumnsError, TooManySheetsError, 
    validate_data_type
)

# =============================================================================
# CORE
# =============================================================================
def load_and_clean(file: str) -> list:

    data = read_excel(file)
    try:
        validate_number_of_sheets(data)
    except TooManySheetsError as e:
        print("Caught error:", e)

    cleaned_data = clean_excel_input(data)
    try:
        validate_number_of_columns(cleaned_data)
    except TooManyColumnsError as e:
        print("Caught error:", e)

    sheet_name = get_first_sheet_name(cleaned_data)
    serie = get_sheet_values(cleaned_data, sheet_name)
    try:
        validate_data_type(serie)
    except NonNumericValueError as e:
        print("Caught error:", e)

    return data_to_numeric(serie)

def pipeline(file: str, p: int, nlags: int, save_dir: str):

    print("\nINITIATING DATA VALIDATION")
    # results, serie = {}, load_and_clean(file)
    results = {}
    serie = timed_run(
        load_and_clean, file,
        process_str="Data Loading & Cleaning", in_seconds=True
    )

    print("\nINITIATING PROCESS")
    print("Calculating Predictions")
    # def forecast_last():
    #     results['pred_last'] = forecast_time_serie(serie[:-p], p)
    # def forecast_next():
    #     results['pred_next'] = forecast_time_serie(serie, p)
    # def acf_pacf():
    #     results['acf'], results['pacf'] = autocorrelations(serie, nlags)
    def forecast_last():
        results['pred_last'] = timed_run(
            forecast_time_serie, serie[:-p], p,
            process_str="Calculation: Forecast Last Period", in_seconds=True
        )

    def forecast_next():
        results['pred_next'] = timed_run(
            forecast_time_serie, serie, p,
            process_str="Calculation: Forecast Next Period", in_seconds=True
        )

    def acf_pacf():
        acf_vals, pacf_vals = timed_run(
            autocorrelations, serie, nlags,
            process_str="Calculation: ACF/PACF", in_seconds=True
        )

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
    timed_run(
        plot_forecasts, serie, results['pred_last'], results['pred_next'], p, save_dir,
        process_str="Plotting: Forecasts", in_seconds=True
    )
    timed_run(
        plot_acf_pacf, results['acf'], results['pacf'], save_dir,
        process_str="Plotting: ACF/PACF", in_seconds=True
    )
    # plot_forecasts(serie, results['pred_last'], results['pred_next'], p, save_dir)
    # plot_acf_pacf(results['acf'], results['pacf'], save_dir)
    print("PROCESS COMPLETED")

    return results['pred_last'], results['acf'], results['pacf']
