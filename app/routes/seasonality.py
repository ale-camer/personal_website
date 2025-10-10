# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os

# --- Third-party ---
from flask import Blueprint, request, render_template, send_file

# --- Project ---
from modules.seasonality import pipeline
from modules.common.utils import export_zip
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
    forecast, acf, pacf = pipeline(
        upload_path, p=periodicity, nlags=nlags, save_dir=SEASONALITY_DIR
    )
    
    return render_template(
        'seasonality.html',
        forecast=forecast,
        acf=acf,
        pacf=pacf,
        existing_plots=['forecast_plot.png', 'acf_pacf_plot.png'],
        enumerate=enumerate
    )

@bp.route('/download_predictions', methods=['GET'])
def download_predictions():
    file_path, file_name = export_zip(SEASONALITY_DIR)
    return send_file(file_path, as_attachment=True, download_name=file_name)