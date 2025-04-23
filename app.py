"""
MODULARIZAR!

Tareas:
  
  1. Seguir comentarios agregados en cada funcion.
  2. Comentar funciones no comentadas.
  3. Todos los comentarios deben estar en ingles y ser simples. 

Proximos pasos:
  
  1. agregar un boton para descargarse los datos en keyphrase extraction y seasonality prediction
  
"""

# web programming frameworks
from flask import Flask, render_template, request, redirect, send_file, jsonify
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# data processing
import os, json
import pandas as pd

# data plotting
import seaborn as sns
import plotly.graph_objs as go

# custom modules
from modules.keyphrase_extraction import process_file
from modules.seasonality_prediction import forecasting, generate_plots
from modules.world_bank import indicators, get_country_data_for_indicator, plot_time_series, plot_heatmap
from modules.whatsapp import preprocess_whatsapp_data, text_normalizer, sentiment_analysis, generate_wordcloud
from modules.generate_readme import generate_readme
from modules.utils import (
    remove_old_files, 
    delta_time, 
    reading_json,
    writing_json,
    wb_data_preprocess
)

# APPs
app = Flask(__name__) # Initialize Flask app
dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/') # Initialize Dash app

# =============================================================================
# CLEANING DIRECTORY
# =============================================================================
list(map(remove_old_files, ['static/seasonality_prediction', 'static/world_bank'])) # removing temporary files
generate_readme(os.path.dirname(os.path.realpath(__file__))) # creating readme file

# =============================================================================
# STATIC PAGES
# =============================================================================
@app.route('/')
def index():
    """Route for the main page"""
    return render_template('index.html')

@app.route('/linear_algebra')
def linear_algebra():
    """Route for the linear algebra page"""
    return render_template('intro_to_linear_algebra_for_data_science.html')

@app.route('/vector_norms')
def vector_norms():
    """Route for the vector norms page"""
    return render_template('vector_norms_applications_in_data_science.html')

@app.route('/algorithmic_trading')
def algorithmic_trading():
    """Route for the algorithmic trading page"""
    return render_template('stock_algorithmic_trading_strategy_backtesting.html')

@app.route('/ds_trends')
def ds_trends():
    """Route for the data science trends page"""
    return render_template('trends_in_data_science_labour_market.html')

@app.route('/arg_macro_spanish')
def arg_macro_spanish():
    """Route for the macroeconomic page in spanish"""
    return render_template('macro_n_employment_spanish.html')

@app.route('/arg_macro_english')
def arg_macro_english():
    """Route for the macroeconomic page in english"""
    return render_template('macro_n_employment_english.html')

@app.route('/mi_cv')
def mi_cv():
    """Route for the CV page"""
    delta_time_string = delta_time()
    return render_template('mi_cv.html', delta_time_string=delta_time_string)

# =============================================================================
# KEYPHRASE EXTRACTION
# =============================================================================
@app.route('/keyphrase_extraction')
def keyphrase_extraction():
    """Route for the keyphrase extraction page"""
    return render_template('keyphrase_extraction.html')

@app.route('/keyphrase_extraction_process', methods=['POST'])
def keyphrase_extraction_process():
    """Processes the uploaded file for keyphrase extraction"""
    file = request.files.get('file')
    num_tables = int(request.form.get('num_tables', 1))
    num_rows = int(request.form.get('num_rows', 1))

    results = process_file(
      file.read().decode('utf-8'), 
      num_tables=num_tables, 
      num_rows=num_rows
    )
    return render_template('keyphrase_extraction.html', results=results)

# =============================================================================
# SEASONALITY PREDICTION
# =============================================================================
@app.route('/seasonality_prediction')
def seasonality_prediction():
    """Route for the seasonality prediction page"""
    return render_template('seasonality_prediction.html')

@app.route('/seasonality_prediction_process', methods=['POST'])
def seasonality_prediction_process():
    """Processes the uploaded file for seasonality prediction"""
    template = 'seasonality_prediction.html'
      
    try:
      serie = pd.read_excel(request.files.get('file')) # reading inputs
      periodicity = int(request.form.get('periodicity'))
  
      if serie.empty: # checking if file is empty
        error_message = "File it's empty."
        return render_template(template, error_message=error_message)

      else: # processing inputs
        col_name = serie.columns[0]
        forecasted_values_last_period = forecasting(serie[col_name].iloc[:-periodicity], periodicity=periodicity)
        forecasted_values_next_period = forecasting(serie[col_name], periodicity=periodicity)
        generate_plots(serie[col_name], forecasted_values_last_period, forecasted_values_next_period, periodicity)

        existing_plots = []
        for filename in ['original_data.png', 'all_periods_data.png', 'historic_and_prediction_data.png']:
            if os.path.exists(os.path.join('static', 'seasonality_prediction', filename)):
                existing_plots.append(filename)

        return render_template(
            template,
            forecast=forecasted_values_next_period,
            existing_plots=existing_plots,
            enumerate=enumerate
        )

    except: # potential errors
      reminder = round(len(serie) % int(periodicity))
      details = [
          f"<li>Data format: {'OK' if pd.api.types.is_numeric_dtype(serie.iloc[:, 0]) else 'Not OK. Data is not numeric.'}</li>",
          f"<li>Number of columns: {'OK' if serie.shape[1] == 1 else f'Not OK. There are {serie.shape[1]} columns instead of one.'}</li>",
          f"<li>Series length: {len(serie)}</li>",
          f"<li>Periodicity: {'OK' if periodicity > 1 else f'Not OK. The value of the periodicity is {periodicity} and has to be higher than one and when dividing the length of the serie the reminder must be zero.'}</li>",
          f"<li>Remainder: {'OK' if reminder == 0 else f'Not OK. The value of the reminder is {reminder} instead of zero.'}</li>"
      ]
      error_message = f"<ul>{''.join(details)}</ul>"

      return render_template(template, error_message=error_message)
      
# =============================================================================
# WORLD BANK
# =============================================================================
@app.route('/world_bank')
def world_bank():
    """Route for the World Bank page"""
    return render_template('world_bank.html', indicators=indicators)

@app.route('/save_data_to_temp')
def save_data_to_temp():
    """Downloads data for the selected indicator and saves it as a temporary JSON file."""
    indicator_selected = request.args.get('indicator') # reading user input
    data = get_country_data_for_indicator(indicator_selected) # reading API
    temp_file_path = os.path.join('static', 'world_bank', f'{indicator_selected}.json')
    writing_json(data, temp_file_path) # writing temporary file
    
    print(f"Data of the indicator {indicator_selected} Downloaded")
    return jsonify({'message': 'Data saved successfully', 'file': temp_file_path})

@app.route('/fetch_options')
def fetch_options():
    """Returns a list of available countries or years based on the selected type and indicator."""
    indicator_selected = request.args.get('indicator') # reading user inputs
    type_selected = request.args.get('type')
    temp_file_path = os.path.join('static', 'world_bank', f'{indicator_selected}.json')
    data = reading_json(temp_file_path) # reading temporary file

    return sorted( # returning list
        {entry['country']['value'] for entry in data}
        if type_selected == 'country'
        else {entry['date'] for entry in data},
        reverse=(type_selected == 'year')
    )
    
@app.route('/fetch_data')
def fetch_data():
    """Fetches data for a specific country or year"""
    indicator_selected = request.args.get('indicator') # reading user inputs
    type_selected = request.args.get('type')
    option_selected = request.args.get('option')
    
    temp_file_path = os.path.join('static', 'world_bank', f'{indicator_selected}.json') # printing data requested
    data = reading_json(temp_file_path)
    return wb_data_preprocess(data, type_selected, option_selected).drop('ISO_CODE', axis=1).to_dict(orient='records')

@app.route('/download_csv')
def download_csv():
    """Generates and downloads a CSV file with the filtered data"""
    indicator_selected = request.args.get('indicator') # reading user inputs
    type_selected = request.args.get('type')
    option_selected = request.args.get('option')
    
    temp_file_path = os.path.join('static', 'world_bank', f'{indicator_selected}.json') # reading data
    data = reading_json(temp_file_path)
    df = wb_data_preprocess(data, type_selected, option_selected).drop('ISO_CODE', axis=1)
    
    csv_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'data.csv') # printing data requested
    df.to_csv(csv_path, index=False)
    return send_file(csv_path, mimetype='text/csv', as_attachment=True, download_name='data.csv')

@app.route('/interactive_graph', methods=['POST'])
def interactive_graph():
    """Generates an interactive graph based on the selected indicator, type, and option"""
    indicator_selected = request.form.get('indicator') # reading user inputs
    type_selected = request.form.get('type')
    option_selected = request.form.get('option')
    
    temp_file_path = os.path.join('static', 'world_bank', f'{indicator_selected}.json') # reading data
    data = reading_json(temp_file_path)
    df = wb_data_preprocess(data, type_selected, option_selected)

    if type_selected == 'country': plot_time_series(df, title=option_selected) # printing graph requested
    elif type_selected == 'year': plot_heatmap(df)
    return "Interactive graph generated."

# =============================================================================
# WHATSAPP
# =============================================================================
days_of_the_week = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday',
                    5: 'Saturday', 6: 'Sunday'}
months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November',
        12: 'December'}

dash_app.layout = html.Div([
    html.H1("Dashboard will be displayed after data upload.".capitalize()),
    html.P("Please upload a file to view the dashboard.".capitalize()),
    dcc.Dropdown(
        id='issuer-dropdown',
        options=[],  # This will be dynamically populated
        value=None
    ),
    html.Div(id='general-charts', style={'width': '100%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='hour-chart'),
        dcc.Graph(id='dow-chart'),
        dcc.Graph(id='dom-chart'),
        dcc.Graph(id='month-chart'),
        dcc.Graph(id='sentiment-analysis'),
        html.Img(id='wordcloud', style={'width': '100%', 'height': 'auto'})
    ])
])

# SE EJECUTA UNA SOLA VEZ. ESO ESTA BIEN.
def create_dash_layout(df, days_of_the_week, months):
    if df.empty:
        return html.Div([
            html.H1("Cantidad de Mensajes por Emisor"),
            html.P("No data available.")
        ])
    return html.Div([
        html.H1("choose an issuer".capitalize()),
        dcc.Dropdown(
            id='issuer-dropdown',
            options=[{'label': issuer, 'value': issuer} for issuer in df['ISSUER'].unique()],
            value=df['ISSUER'].unique()[0] if not df.empty else None
        ),
        html.Div(id='general-charts', style={'width': '100%', 'display': 'inline-block'}),
        html.Div([
            html.Div(dcc.Graph(id='hour-chart'), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(id='dow-chart'), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(id='dom-chart'), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(id='month-chart'), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(id='sentiment-analysis'), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(html.Img(id='wordcloud', style={'width': '100%', 'height': 'auto'}), style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'})
        ])
    ])

# LA VARIABLE df DEBERIA GENERARSE POR FUERA DE LA FUNCION
# ¿PORQUE ESTOY TENIENDO VARIABLES GLOBALES? VER SI SE PUEDEN ELIMINAR
# ¿PARA QUE TENGO EL METODO GET?
@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
    global df, file_content, language
    if request.method == 'POST':
        file = request.files.get('file')
        language = request.form.get('selected_language')
        print('Selected language:', language)

        if file:
            file_content = preprocess_whatsapp_data(file)

            df = file_content.groupby(['ISSUER', 'HOUR', 'dow', 'dom', 'month'])['MESSAGE'].count().reset_index()
            df_ = file_content.groupby(['HOUR', 'dow', 'dom', 'month'])['MESSAGE'].count().reset_index()
            df_['ISSUER'] = 'GENERAL'
            df = pd.concat([df, df_])

            print("Issuers: ", df['ISSUER'].unique())  # Verificar el contenido procesado

            # Update Dash app layout
            dash_app.layout = create_dash_layout(df, days_of_the_week, months)

            # Redirigir al dashboard
            return redirect('/dashboard/')

    return render_template("whatsapp.html")

# ¿QUE HACE ESTA FUNCION?
# PARTICIONARLA PARA ENTENDERLA
# VER QUE SE PUEDE SIMPLIFICAR
@dash_app.callback( # Dash callback
    [Output('general-charts', 'children'),
     Output('hour-chart', 'figure'),
     Output('dow-chart', 'figure'),
     Output('dom-chart', 'figure'),
     Output('month-chart', 'figure'),
     Output('sentiment-analysis', 'figure'),
     Output('wordcloud', 'src')],
    [Input('issuer-dropdown', 'value')]
)
def update_charts(selected_issuer):
    # Ensure df is available globally or adjust logic to access updated df
    if selected_issuer is None:
        return (html.P("No data available."), {}, {}, {}, {}, {}, '')

    if df.empty:
        return (html.P("No data available."), {}, {}, {}, {}, {}, '')

    # Prepare the figures and other data
    # Placeholder examples
    hour_chart = go.Figure()
    dow_chart = go.Figure()
    dom_chart = go.Figure()
    month_chart = go.Figure()
    sentiment_fig = sentiment_analysis(file_content, selected_issuer)
    wordcloud_img = generate_wordcloud(text_normalizer(file_content, 'english'))

    print(f"Selected issuer: {selected_issuer}")

    # Inicializar filtered_df como un DataFrame vacío
    filtered_df = pd.DataFrame()
    # print(selected_issuer, type(selected_issuer))

    if selected_issuer == "GENERAL":

        # if df.empty:
        #     return (html.P("No data available for 'GENERAL'."), {}, {}, {}, {}, {}, '')
        print(df.shape)
        filtered_df = df.copy()

        # General charts
        issuer_messages = text_normalizer(file_content, language=language)
        sentiment_fig = sentiment_analysis(file_content)
        issuer_counts = file_content['ISSUER'].value_counts().reset_index()
        issuer_counts.columns = ['ISSUER', 'COUNT']

        # Gráfico de pie para la cantidad de mensajes por emisor
        pie_chart_messages = dcc.Graph(
            figure={
                'data': [go.Pie(labels=issuer_counts['ISSUER'], values=issuer_counts['COUNT'], hole=.5)],
                'layout': go.Layout(title='proportion of messages by issuer'.title())
            }
        )

        # Calcular la suma de la longitud de mensajes por emisor
        message_length_sum = file_content.groupby('ISSUER')['len_message'].sum().reset_index()

        # Gráfico de pie para la longitud de mensajes por emisor
        pie_chart_message_length = dcc.Graph(
            figure={
                'data': [go.Pie(labels=message_length_sum['ISSUER'], values=message_length_sum['len_message'], hole=.5)],
                'layout': go.Layout(title='proportion of words by issuer'.title())
            }
        )

        general_charts = html.Div([
            html.Div(pie_chart_messages, style={'width': '48%', 'display': 'inline-block'}),
            html.Div(pie_chart_message_length, style={'width': '48%', 'display': 'inline-block'})
        ], style={'display': 'flex', 'justify-content': 'space-between'})

    else:

        filtered_df = df[df['ISSUER'] == selected_issuer]
        issuer_messages = text_normalizer(file_content[file_content['ISSUER'] == selected_issuer], language=language)
        sentiment_fig = sentiment_analysis(file_content, selected_issuer)
        general_charts = ""

    print(f"Filtered DataFrame shape: {filtered_df.shape}")

    bar_colors = sns.color_palette("husl", n_colors=31).as_hex()

    # Gráfico de mensajes por hora
    hour_data = filtered_df.groupby('HOUR')['MESSAGE'].count().reset_index()
    hour_chart = {
        'data': [go.Bar(x=hour_data['HOUR'], y=hour_data['MESSAGE'], marker={'color': bar_colors})],
        'layout': go.Layout(title='amount of messages per hour'.title())
    }

    # Gráfico de mensajes por día de la semana
    dow_data = filtered_df.groupby('dow')['MESSAGE'].count().reset_index()
    dow_data['dow'] = dow_data['dow'].map(days_of_the_week)
    dow_chart = {
        'data': [go.Bar(x=dow_data['dow'], y=dow_data['MESSAGE'], marker={'color': bar_colors})],
        'layout': go.Layout(title='amount of messages per day of the week'.title())
    }

    # Gráfico de mensajes por día del mes
    dom_data = filtered_df.groupby('dom')['MESSAGE'].count().reset_index()
    dom_chart = {
        'data': [go.Bar(x=dom_data['dom'], y=dom_data['MESSAGE'], marker={'color': bar_colors})],
        'layout': go.Layout(title='amount of messages per day of the month'.title())
    }

    # Gráfico de mensajes por mes
    month_data = filtered_df.groupby('month')['MESSAGE'].count().reset_index()
    month_data['month'] = month_data['month'].map(months)
    month_chart = {
        'data': [go.Bar(x=month_data['month'], y=month_data['MESSAGE'], marker={'color': bar_colors})],
        'layout': go.Layout(title='amount of messages per month'.title())
    }

    # Generar nube de palabras
    wordcloud_img = generate_wordcloud(issuer_messages)

    return (general_charts, hour_chart, dow_chart, dom_chart, month_chart, sentiment_fig, wordcloud_img)

# =============================================================================
# RUNNING SCRIPT
# =============================================================================
if __name__ == '__main__':
    app.run(debug=True)
