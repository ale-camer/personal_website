"""Web App project file."""

# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os

# --- Third-party ---
from flask import Flask, render_template, request, redirect, send_file, jsonify, url_for

# --- Project/system ---
import modules.utils as ut
import modules.world_bank_utils as wb_ut
from modules.dash_app import init_dash_app
from modules.keyphrase import NGramModule, get_tables_string, progress
from modules.seasonality_extended import SeasonalityModule, download_forecast
from modules.whatsapp import layout, WhatsAppModule
from modules.world_bank import WorldBankModule

# =============================================================================
# PATHS
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_DIR = os.path.join(BASE_DIR, 'static')
KEYPHRASE_DIR = os.path.join(STATIC_DIR, 'keyphrase')
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
@app.route('/extract_keyphrases', methods=['POST'])
def extract_keyphrases():
    progress["value"] = 0
    ngrams = NGramModule(
      raw_text=request.files.get('file').read().decode('utf-8'),
      max_ngrams=int(request.form.get('num_tables', 1)),
      num_nrows=int(request.form.get('num_rows', 1))
    )
    result = ngrams.analyze()
    ut.write_json(ngrams.summary, KEYPHRASE_INPUT_PATH)
    return render_template('keyphrase.html', results=result)

@app.route('/progress')
def get_progress():
    return jsonify(progress)

@app.route('/download_keyphrases')
def download_keyphrases(output_filename: str = "keyphrases.txt"):
    data = ut.read_json(KEYPHRASE_INPUT_PATH)
    keyphrases_string = get_tables_string(data)
    ut.write_txt(keyphrases_string, KEYPHRASE_OUTPUT_PATH)
    return send_file(KEYPHRASE_OUTPUT_PATH, as_attachment=True, download_name=output_filename)

# =============================================================================
# SEASONALITY
# =============================================================================
@app.route('/predict_seasonality', methods=['GET', 'POST'])
def predict_seasonality():

    if request.method == 'GET': # refresh
        return render_template('seasonality.html')

    template = 'seasonality.html'
    file = request.files.get('file')
    periodicity = int(request.form.get('periodicity'))
    nlags = int(request.form.get('nlags'))

    processor = SeasonalityModule(file, periodicity, nlags)
    error = processor.is_empty(selected_lang)
    if error:
        return render_template(template, error_message=error)

    try:
        forecast, acf, pacf = processor.forecast()
        return render_template(
            template,
            forecast=forecast,
            acf=acf,
            pacf=pacf,
            existing_plots=config["plot_names"],
            enumerate=enumerate
        )
    except:
        return render_template(
            template,
            val_message=processor.validation(selected_lang)
        )

@app.route('/download_predictions', methods=['GET'])
def download_predictions():
    file_path, file_name = download_forecast()
    return send_file(file_path, as_attachment=True, download_name=file_name)

# =============================================================================
# WORLD BANK
# =============================================================================
wb_manager = WorldBankModule(GEO_DATA_PATH)

@app.route('/download_data')
def download_data():
    indicator = request.args.get('indicator')
    data = wb_manager.indicator(indicator)
    ut.write_json(data, wb_ut.get_file_path(indicator))
    return jsonify({'message': 'Data saved successfully', 'file': wb_ut.get_file_path(indicator)})

@app.route('/show_options')
def show_options():
    data = wb_ut.load_data(request.args.get('indicator'))
    return wb_ut.extract_options(data, request.args.get('type'))

@app.route('/show_data')
def show_data():
    args = request.args
    data = wb_ut.load_data(args.get('indicator'), args.get('type'), args.get('option'))
    return data.drop('ISO_CODE', axis=1).to_dict(orient='records')

@app.route('/plot_graph', methods=['POST'])
def plot_graph():
    form = request.form
    indicator, type_selected, option = form.get('indicator'), form.get('type'), form.get('option')
    df = wb_ut.load_data(indicator, type_selected, option)
    title = f'{option} - {INDICATOR_NAMES.get(indicator)}' if type_selected == 'country' else None

    filepath = wb_manager.create_visualization(df, type_selected, title=title)
    relative_path = os.path.relpath(
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