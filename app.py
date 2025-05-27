"""Web App project file."""

# --- Standard library ---
import os
import warnings

# --- Third-party ---
from flask import Flask, render_template, request, redirect, send_file, jsonify

# --- Project/system ---
import modules.utils as ut
from modules.dash_app import init_dash_app
from modules.keyphrase import NGramExtractor, get_tables_string
from modules.seasonality import SeasonalityPipeline, download_forecast
from modules.whatsapp import layout, WhatsAppService
from modules.world_bank import WorldBankManager

warnings.filterwarnings("ignore")

# =============================================================================
# PATHS
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_DIR = os.path.join(BASE_DIR, 'static')
KEYPHRASE_DIR = os.path.join(STATIC_DIR, 'keyphrase')
JSON_DIR = os.path.join(STATIC_DIR, 'json')

CONFIG_PATH = os.path.join(JSON_DIR, 'config.json')
GEO_DATA_PATH = os.path.join(JSON_DIR, 'world_administrative_boundaries.json')

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

@app.route('/arg_macro_spanish')
def arg_macro_spanish():
    return render_template('macro_n_employment_spanish.html')

@app.route('/arg_macro_english')
def arg_macro_english():
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
# KEYPHRASE EXTRACTION
# =============================================================================
@app.route('/extract_keyphrases', methods=['POST'])
def extract_keyphrases():
    ngrams = NGramExtractor(
      raw_text=request.files.get('file').read().decode('utf-8'),
      max_ngrams=int(request.form.get('num_tables', 1)),
      num_nrows=int(request.form.get('num_rows', 1))
    )
    result = ngrams.analyze()
    ut.write_json(ngrams.summary, KEYPHRASE_INPUT_PATH)
    return render_template('keyphrase.html', results=result)

@app.route('/download_keyphrases')
def download_keyphrases(output_filename: str = "keyphrases.txt"):
    data = ut.read_json(KEYPHRASE_INPUT_PATH)
    keyphrases_string = get_tables_string(data)
    ut.write_txt(keyphrases_string, KEYPHRASE_OUTPUT_PATH)
    return send_file(KEYPHRASE_OUTPUT_PATH, as_attachment=True, download_name=output_filename)

# =============================================================================
# SEASONALITY PREDICTION
# =============================================================================
@app.route('/predict_seasonality', methods=['POST'])
def predict_seasonality():

    template = 'seasonality.html'
    file = request.files.get('file')
    periodicity = int(request.form.get('periodicity'))
    processor = SeasonalityPipeline(file, periodicity)

    error = processor.is_empty
    if error:
        return render_template(template, error_message=error)

    try:
        forecast = processor.forecast()
        return render_template(
            template,
            forecast=forecast,
            existing_plots=config["plot_names"],
            enumerate=enumerate
        )

    except:
        error_message = processor.validation
        return render_template(template, error_message=error_message)

@app.route('/download_predictions', methods=['GET'])
def download_predictions():
    file_path, file_name = download_forecast()
    return send_file(file_path, as_attachment=True, download_name=file_name)

# =============================================================================
# WORLD BANK
# =============================================================================
wb_manager = WorldBankManager(GEO_DATA_PATH)
@app.route('/save_data_to_temp')
def save_data_to_temp():
    indicator_selected = request.args.get('indicator')
    
    data = wb_manager.get_indicator_data(indicator_selected)
    
    temp_file_path = os.path.join('static', 'world_bank', f'{indicator_selected}.json')
    ut.write_json(data, temp_file_path)
    
    return jsonify({'message': 'Data saved successfully', 'file': temp_file_path})

@app.route('/fetch_options')
def fetch_options():
    indicator_selected = request.args.get('indicator')
    type_selected = request.args.get('type')
    
    temp_file_path = os.path.join('static', 'world_bank', f'{indicator_selected}.json')
    data = ut.read_json(temp_file_path)

    return sorted(
        {entry['country']['value'] for entry in data}
        if type_selected == 'country'
        else {entry['date'] for entry in data},
        reverse=(type_selected == 'year')
    )

@app.route('/fetch_data')
def fetch_data():
    indicator_selected = request.args.get('indicator')
    type_selected = request.args.get('type')
    option_selected = request.args.get('option')

    temp_file_path = os.path.join('static', 'world_bank', f'{indicator_selected}.json')
    data = ut.read_json(temp_file_path)
    
    result_df = wb_manager.get_result_data(data, type_selected, option_selected)
    
    return result_df.drop('ISO_CODE', axis=1).to_dict(orient='records')

@app.route('/interactive_graph', methods=['POST'])
def interactive_graph():
    indicator_selected = request.form.get('indicator')
    type_selected = request.form.get('type')
    option_selected = request.form.get('option')
    
    temp_file_path = os.path.join('static', 'world_bank', f'{indicator_selected}.json')
    data = ut.read_json(temp_file_path)
    
    df = wb_manager.get_result_data(data, type_selected, option_selected)
    
    if type_selected == 'country':
        title = f'{option_selected} - {INDICATOR_NAMES.get(indicator_selected)}'
        wb_manager.create_visualization(df, type_selected, title=title)
    elif type_selected == 'year':
        wb_manager.create_visualization(df, type_selected)
    
    return "Interactive graph generated."

# =============================================================================
# WHATSAPP
# =============================================================================
whatsapp_service = WhatsAppService()
dash_app = init_dash_app(app, whatsapp_service, WEEK_DAYS, MONTHS)
@app.route('/whatsapp_dashboard', methods=['POST'])
def whatsapp_dashboard():
    data = whatsapp_service.parse_chat(
        request.files.get('file'),
        request.form.get('selected_language')
    )
    dash_app.layout = layout(data.df)
    return redirect('/dashboard/')