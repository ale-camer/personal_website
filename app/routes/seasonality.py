# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os

# --- Third-party ---
from flask import Blueprint, request, render_template, send_file

# --- Project ---
from modules.seasonality import pipeline
from modules.common.utils import export_zip, FileExporter, write_txt
from modules.common.decorators import validate_file_size
from config import SEASONALITY_DIR

# =============================================================================
# cONFIGURATION
# =============================================================================
bp = Blueprint('seasonality', __name__)

# =============================================================================
# ROUTES
# =============================================================================
@bp.route('/predict_seasonality', methods=['GET', 'POST'])
@validate_file_size(template_on_error='seasonality.html')
def predict_seasonality(uploaded_file):

    if request.method == 'GET':
        return render_template('seasonality.html')

    upload_path = os.path.join(SEASONALITY_DIR, uploaded_file.filename)
    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
    uploaded_file.save(upload_path)

    periodicity = int(request.form.get('periodicity', 12))
    nlags = int(request.form.get('nlags', 10))

    try:
        forecast, acf, pacf = pipeline(
            upload_path, p=periodicity, nlags=nlags, save_dir=SEASONALITY_DIR
        )
        
        forecast_data = [(i+1, v) for i, v in enumerate(forecast)]
        acf_data = [(i+1, v) for i, v in enumerate(acf)]
        pacf_data = [(i+1, v) for i, v in enumerate(pacf)]

        cols_forecast = ["Period", "Forecast"]
        cols_acf_pacf = ["Lag", "Correlation (%)"]

        forecast_exporter = FileExporter({"Forecast": forecast_data}, cols_forecast)
        acf_exporter = FileExporter({"ACF": acf_data}, cols_acf_pacf)
        pacf_exporter = FileExporter({"PACF": pacf_data}, cols_acf_pacf)

        txt_output = "\n\n".join([
            forecast_exporter.to_txt_string(),
            acf_exporter.to_txt_string(),
            pacf_exporter.to_txt_string()
        ])

        txt_path = os.path.join(SEASONALITY_DIR, "seasonality_results.txt")
        write_txt(txt_output, txt_path)
        
        return render_template(
            'seasonality.html',
            forecast=forecast,
            acf=acf,
            pacf=pacf,
            existing_plots=['forecast_plot.png', 'acf_pacf_plot.png'],
            enumerate=enumerate
        )
    except Exception as e:
        return render_template(
            'seasonality.html',
            execution_exception=str(e).capitalize()
        )

@bp.route('/download_predictions', methods=['GET'])
def download_predictions():
    file_path, file_name = export_zip(SEASONALITY_DIR, not_format='xlsx')
    return send_file(file_path, as_attachment=True, download_name=file_name)