import modules.common.utils as ut
import modules.common.validations as val
from . import core

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

def pipeline(file: str, p: int, nlags: int, save_dir: str) -> None:

    print("\nINITIATING DATA VALIDATION")
    serie = load_and_clean(file)

    print("\nINITIATING PROCESS")
    print("Calculating Predictions")
    pred_last_period = core.forecast_time_serie(serie[:-p], p)
    pred_next_period = core.forecast_time_serie(serie, p)
    print(pred_last_period, pred_next_period)

    print("Printing Forecast Plot")
    plot_forecasts_inputs = (serie, pred_last_period, pred_next_period, p, save_dir)
    core.plot_forecasts(*plot_forecasts_inputs)

    print("Printing Autocorrelation Plot")
    acf_values, pacf_values = core.autocorrelations(serie, nlags)
    core.plot_acf_pacf(acf_values, pacf_values, save_dir)

    return pred_last_period, acf_values, pacf_values