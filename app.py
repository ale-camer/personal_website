"""Web App project file."""

# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os

# --- External Library ---
from flask import (
    Flask, render_template, request, redirect, send_file, jsonify, url_for, 
    make_response
)

# --- Project Modules ---
import modules.utils as ut
from modules.dash_app import init_dash_app
from modules.whatsapp import layout, WhatsAppModule

import modules.keyphrase as kp
import modules.seasonality as seas
import modules.world_bank as wb

import modules.common.utils as ut1
import modules.common.validations as val1
import modules.common.decorators as dec1

# =============================================================================
# PATHS
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_DIR = os.path.join(BASE_DIR, 'static')
KEYPHRASE_DIR = os.path.join(STATIC_DIR, 'keyphrase')
SEASONALITY_DIR = os.path.join(STATIC_DIR, 'seasonality')
WORLD_BANK_DIR = os.path.join(STATIC_DIR, 'world_bank')
JSON_DIR = os.path.join(STATIC_DIR, 'json')

CONFIG_PATH = os.path.join(JSON_DIR, 'config.json')
GEO_DATA_PATH = os.path.join(JSON_DIR, 'world_administrative_boundaries.json')
LANG_PATH = os.path.join(JSON_DIR, 'lang')

KEYPHRASE_INPUT_PATH = os.path.join(KEYPHRASE_DIR, 'raw_keyphrases_results.json')
KEYPHRASE_OUTPUT_PATH = os.path.join(KEYPHRASE_DIR, 'processed_keyphrases_results.txt')

# =============================================================================
# CONSTANTS
# =============================================================================
config = ut.read_json(CONFIG_PATH)
INDICATORS = dict(sorted(config["indicators"].items()))
INDICATOR_NAMES = {v: k for k, v in INDICATORS.items()}
WEEK_DAYS = {int(k): v for k, v in config["days_of_the_week"].items()}
MONTHS = {int(k): v for k, v in config["months"].items()}

# =============================================================================
# APPs Instantiation
# =============================================================================
app = Flask(__name__)
app.before_request(ut.load_language_texts)
app.context_processor(ut.inject_texts_and_languages)

with app.app_context():
    selected_lang = ut.inject_texts_and_languages()['selected_lang']

# =============================================================================
# STATIC PAGES
# =============================================================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/linear_algebra')
def linear_algebra():
    return render_template('intro_to_linear_algebra_for_data_science.html')

@app.route('/vector_norms')
def vector_norms():
    return render_template('vector_norms_applications_in_data_science.html')

@app.route('/algorithmic_trading')
def algorithmic_trading():
    return render_template('stock_algorithmic_trading_strategy_backtesting.html')

@app.route('/ds_trends')
def ds_trends():
    return render_template('trends_in_data_science_labour_market.html')

@app.route('/arg_macro')
def arg_macro():
    return render_template('macro_n_employment_english.html')

@app.route('/mi_cv')
def mi_cv():
    return render_template('mi_cv.html', delta_time_string=ut.job_duration())

@app.route('/keyphrase_extraction')
def keyphrase_extraction():
    return render_template('keyphrase.html')

@app.route('/seasonality_prediction')
def seasonality_prediction():
    return render_template('seasonality.html')

@app.route('/world_bank')
def world_bank():
    return render_template('world_bank.html', indicators=INDICATORS)

@app.route('/whatsapp')
def whatsapp():
    return render_template('whatsapp.html')

# =============================================================================
# KEYPHRASE
# =============================================================================
progress = {"value": 0}

@app.route('/extract_keyphrases', methods=['POST'])
@dec1.validate_file_size(template_on_error='keyphrase.html')
def extract_keyphrases(uploaded_file):

    results = kp.pipeline(
        raw_text=uploaded_file.read().decode('utf-8'),
        progress=progress,
        top_k=int(request.form.get('num_rows', 1)),
        max_n=int(request.form.get('num_tables', 1))
    )

    summary = {
        label: [{"Keywords": d[0], "# Appearances": d[1]} for d in data]
        for label, data in results.items()
    }

    ut1.write_json(summary, KEYPHRASE_INPUT_PATH)
    return render_template('keyphrase.html', results=results)

@app.route('/progress')
def get_progress():
    return jsonify(progress)

@app.route('/download_keyphrases', methods=['GET'])
def download_keyphrases():
    
    results_data = ut1.read_results(KEYPHRASE_INPUT_PATH)    
    exporter = ut1.FileExporter(results_data, cols=["Keywords", "# Appearances"])
    
    file_format = request.args.get('format', 'txt')
    match file_format:
        case 'txt': output_content = exporter.to_txt_string()
        case 'md': output_content = exporter.to_md_string()
        case 'pdf': output_content = exporter.to_pdf_bytes()
    
    response = make_response(output_content)
    response.headers['Content-Type'] = f"application/{file_format}" if file_format == 'pdf' else f"text/{file_format}"
    response.headers['Content-Disposition'] = f'attachment; filename={f"keyphrase_results.{file_format}"}'
    
    return response

# =============================================================================
# SEASONALITY
# =============================================================================
@app.route('/predict_seasonality', methods=['GET', 'POST'])
def predict_seasonality():

    if request.method == 'GET':  # refresh
        return render_template('seasonality.html')

    file = request.files.get('file')
    periodicity = int(request.form.get('periodicity', 12))
    nlags = int(request.form.get('nlags', 10))

    upload_path = os.path.join(SEASONALITY_DIR, file.filename)
    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
    file.save(upload_path)

    print("\n=== STARTING SEASONALITY PIPELINE ===")
    forecast, acf, pacf = seas.pipeline(
        upload_path, p=periodicity, nlags=nlags, save_dir=SEASONALITY_DIR
    )
    return render_template(
        'seasonality.html',
        forecast=forecast,
        acf= acf,
        pacf= pacf,
        existing_plots=['forecast_plot.png', 'acf_pacf_plot.png'],
        enumerate=enumerate
    )

@app.route('/download_predictions', methods=['GET'])
def download_predictions():
    file_path, file_name = ut1.export_zip(SEASONALITY_DIR)
    return send_file(file_path, as_attachment=True, download_name=file_name)

# =============================================================================
# WORLD BANK
# =============================================================================
def get_params():
    return (
        request.args.get('indicator') or request.form.get('indicator') or None, 
        request.args.get('type') or request.form.get('type') or None, 
        request.args.get('option') or request.form.get('option') or None
    )

def get_data_downloaded(indicator):
    return ut1.read_json(os.path.join(WORLD_BANK_DIR, f'{indicator}.json'))

def get_filtered_data(data, type, option):
    return wb.filter_data(data, type, option)

@app.route('/download_data')
def download_data():
    indicator = get_params()[0]
    data = wb.download_indicator_data(indicator)
    ut.write_json(data, os.path.join(WORLD_BANK_DIR, f'{indicator}.json'))
    return jsonify({'message': 'Data saved successfully'})

@app.route('/show_options')
def show_options():
    indicator, type, _ = get_params()
    data = get_data_downloaded(indicator)
    options = wb.extract_options(data, type)
    return jsonify(options)

@app.route('/show_data')
def show_data():
    indicator, type, option = get_params()
    data = get_data_downloaded(indicator)
    filtered_data = get_filtered_data(data, type, option)
    return jsonify(filtered_data)

@app.route('/plot_graph', methods=['POST'])
def plot_graph():
    indicator, type, option = get_params()
    data = get_data_downloaded(indicator)
    filtered_data = get_filtered_data(data, type, option)

    country_map = wb.create_country_iso_map(data) # refactorizar
    title = f'{option} - {INDICATOR_NAMES.get(indicator)}' if type == 'country' else None
    filepath = wb.create_visualization(
        filtered_data, type, GEO_DATA_PATH, country_map, title=title
    )

    relative_path = os.path.relpath( # refactorizar
        os.path.abspath(filepath),
        os.path.abspath(app.static_folder)
    )
    plot_url = url_for('static', filename=relative_path.replace(os.sep, '/'))
        
    return jsonify({'message': 'Interactive graph generated.', 'plot_url': plot_url})

# =============================================================================
# WHATSAPP
# =============================================================================
whatsapp_service = WhatsAppModule()
dash_app = init_dash_app(app, whatsapp_service, WEEK_DAYS, MONTHS)

@app.route('/whatsapp_dashboard', methods=['POST'])
def whatsapp_dashboard():
    data = whatsapp_service.parse_chat(
        request.files.get('file'),
        request.form.get('selected_language')
    )
    dash_app.layout = layout(data.df)
    return redirect('/dashboard/')