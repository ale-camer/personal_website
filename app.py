"""Main project file."""

# --- Standard library ---
import os
import warnings
import zipfile

# --- Third-party ---
import pandas as pd
from flask import Flask, render_template, request, redirect, send_file, jsonify
from dash import Dash
from dash.dependencies import Input, Output

# --- Project/system ---
from modules.keyphrase import text_to_ngrams, get_tables_string
from modules.seasonality import SeasonalityProcessor
from modules.whatsapp import build_layout, WhatsAppService, ChartGenerator
from modules.world_bank import WorldBankManager
from modules.utils import (
    remove_old_files,
    delta_time,
    reading_json,
    writing_json,
    writing_txt
)

warnings.filterwarnings("ignore")

# APPs
app = Flask(__name__)  # Initialize Flask app
dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/') # Initialize Dash app

# =============================================================================
# CLEANING DIRECTORY
# =============================================================================
config = reading_json(os.path.join('static', 'json', 'config.json'))
folders_to_clean = ['static/seasonality',
                    'static/world_bank', 'static/keyphrase']
list(map(remove_old_files, folders_to_clean))  # removing temporary files

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
    delta_time_string = delta_time()
    return render_template('mi_cv.html', delta_time_string=delta_time_string)
# =============================================================================
# KEYPHRASE EXTRACTION
# =============================================================================
keyphrase_input_file_path = os.path.join(
    'static', 'keyphrase', 'raw_keyphrases_results.json')
keyphrase_output_file_path = os.path.join(
    'static', 'keyphrase', 'processed_keyphrases_results.txt')


@app.route('/keyphrase_extraction')
def keyphrase_extraction():
    return render_template('keyphrase.html')


@app.route('/keyphrase_extraction_process', methods=['POST'])
def keyphrase_extraction_process():

    file = request.files.get('file')  # inputs
    max_ngram = int(request.form.get('num_tables', 1))
    num_rows = int(request.form.get('num_rows', 1))

    results = text_to_ngrams(  # process
        file.read().decode('utf-8'),
        max_ngram=max_ngram,
        num_rows=num_rows
    )
    results_formatted = {k: v.to_dict(orient='records')
                         for k, v in results.items()}
    writing_json(results_formatted, keyphrase_input_file_path)
    return render_template('keyphrase.html', results=results)


@app.route('/download_keyphrases')
def download_keyphrases(output_filename: str = "keyphrases_results.txt"):
    data = reading_json(keyphrase_input_file_path)
    keyphrases_string = get_tables_string(data)
    writing_txt(keyphrases_string, keyphrase_output_file_path)
    return send_file(keyphrase_output_file_path, as_attachment=True, download_name=output_filename)

# =============================================================================
# SEASONALITY PREDICTION
# =============================================================================
@app.route('/seasonality_prediction')
def seasonality_prediction():
    return render_template('seasonality.html')

@app.route('/seasonality_prediction_process', methods=['POST'])
def seasonality_prediction_process():
    template = 'seasonality.html'
    
    try:
        file = request.files.get('file')
        periodicity = int(request.form.get('periodicity'))
        
        processor = SeasonalityProcessor(periodicity)
        results = processor.process_file(file)
        
        processor.save_predictions_csv(results['forecasted_next_period'])
        
        existing_plots = config["plot_names"]
        
        return render_template(
            template,
            forecast=results['forecasted_next_period'],
            existing_plots=existing_plots,
            enumerate=enumerate
        )
    
    except Exception:
        serie = pd.read_excel(request.files.get('file'))
        periodicity = int(request.form.get('periodicity'))
        
        processor = SeasonalityProcessor(periodicity)
        error_message = processor.get_validation_details(serie, periodicity)
        
        return render_template(template, error_message=error_message)

@app.route('/download_predictions', methods=['GET'])
def download_predictions():
    processor = SeasonalityProcessor()
    zip_path = processor.create_predictions_zip()
    
    return send_file(zip_path, as_attachment=True, download_name='predictions.zip')

# =============================================================================
# WORLD BANK
# =============================================================================
indicators = dict(sorted(config["indicators"].items()))
indicator_names = {v: k for k, v in indicators.items()}
geo_data_file_path = os.path.join('static', 'json', 'world_administrative_boundaries.json')
wb_manager = WorldBankManager(geo_data_file_path)

@app.route('/world_bank')
def world_bank():
    return render_template('world_bank.html', indicators=indicators)

@app.route('/save_data_to_temp')
def save_data_to_temp():
    """Downloads data for the selected indicator and saves it as a temporary JSON file."""
    indicator_selected = request.args.get('indicator')
    
    data = wb_manager.get_indicator_data(indicator_selected)
    
    temp_file_path = os.path.join('static', 'world_bank', f'{indicator_selected}.json')
    writing_json(data, temp_file_path)
    
    return jsonify({'message': 'Data saved successfully', 'file': temp_file_path})

@app.route('/fetch_options')
def fetch_options():
    indicator_selected = request.args.get('indicator')
    type_selected = request.args.get('type')
    
    temp_file_path = os.path.join('static', 'world_bank', f'{indicator_selected}.json')
    data = reading_json(temp_file_path)

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
    data = reading_json(temp_file_path)
    
    result_df = wb_manager.get_result_data(data, type_selected, option_selected)
    
    return result_df.drop('ISO_CODE', axis=1).to_dict(orient='records')

@app.route('/interactive_graph', methods=['POST'])
def interactive_graph():
    indicator_selected = request.form.get('indicator')
    type_selected = request.form.get('type')
    option_selected = request.form.get('option')
    
    print(f"La función fue llamada para las siguientes opciones: "
          f"{indicator_selected}, {type_selected} y {option_selected}")

    temp_file_path = os.path.join('static', 'world_bank', f'{indicator_selected}.json')
    data = reading_json(temp_file_path)
    
    df = wb_manager.get_result_data(data, type_selected, option_selected)
    
    if type_selected == 'country':
        title = f'{option_selected} - {indicator_names.get(indicator_selected)}'
        wb_manager.create_visualization(df, type_selected, title=title)
    elif type_selected == 'year':
        wb_manager.create_visualization(df, type_selected)
    
    return "Interactive graph generated."

# =============================================================================
# WHATSAPP
# =============================================================================
WEEK_DAYS = {int(k): v for k, v in config["days_of_the_week"].items()}
MONTHS = {int(k): v for k, v in config["months"].items()}

whatsapp_service = WhatsAppService()
dash_app.layout = build_layout()

@app.route('/whatsapp')
def whatsapp():
    return render_template('whatsapp.html')

@app.route('/whatsapp_dashboard', methods=['POST'])
def whatsapp_dashboard():
    whatsapp_data = whatsapp_service.process_file(
        request.files.get('file'),
        request.form.get('selected_language')
    )
    dash_app.layout = build_layout(whatsapp_data.df)
    return redirect('/dashboard/')

@dash_app.callback(
    [Output('general-charts', 'children'),
     Output('hour-chart', 'figure'),
     Output('dow-chart', 'figure'),
     Output('dom-chart', 'figure'),
     Output('month-chart', 'figure'),
     Output('sentiment-analysis', 'figure'),
     Output('wordcloud', 'src')],
    [Input('issuer-dropdown', 'value')]
)
def update_charts(selected_issuer: str):

    charts = ChartGenerator.generate_all_charts(
        whatsapp_service.current_data,
        selected_issuer,
        weekdays_mapper=WEEK_DAYS,
        months_mapper=MONTHS
    )
    return tuple(charts.values())

# =============================================================================
# RUNNING SCRIPT
# =============================================================================
if __name__ == '__main__':
    app.run(debug=True)
