# web programming frameworks
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# data processing
import os, shutil
import numpy as np
import pandas as pd
from datetime import datetime

# data plotting
import seaborn as sns
import plotly.graph_objs as go

# custom modules
from modules.keyphrase_extraction import procesar_archivo
from modules.seasonality_prediction import forecasting, generate_plots
from modules.world_bank import indicators, get_country_data_for_indicator, plot_time_series, plot_heatmap
from modules.whatsapp import preprocess_whatsapp_data, text_normalizer, sentiment_analysis, generate_wordcloud

# APPs
app = Flask(__name__) # Initialize Flask app
dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/') # Initialize Dash app

# CLEANING FOLDERS
def remove_old_files(folder, files_to_remove=None):
    """
    Removes specific files and folders in a folder or all files and folders if not specified.
    
    :param folder: Folder from which files and folders will be removed.
    :param files_to_remove: List of filenames to remove. If None, all files and folders will be removed.
    """
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    if files_to_remove and filename not in files_to_remove:
                        continue
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Deleted folder: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    else:
        print(f"Folder does not exist: {folder}")
remove_old_files('static/seasonality_prediction')
remove_old_files('static/world_bank')

def delta_time():
    """"Updates the time since the last job was started"""
    today = datetime.now()
    last_year = today.year - 1
    last_august = datetime(year=last_year, month=8, day=1)
    
    if today < last_august: last_august = datetime(year=last_year - 1, month=8, day=1)
    months = (today.year - last_august.year) * 12 + today.month - last_august.month + 1
    
    if months > 12:
        
        years = months // 12
        months = months % 12
        
        if years > 1: year_string = "years"
        else: year_string = "year"
            
        if months > 1: month_string = "months"
        else: month_string = "month"
            
        string = f"{years} {year_string} {months} {month_string}"
    
    return string

# STATIC PAGES
@app.route('/')
def index():
    """Route for the main page"""
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
    """Route for the CV page"""
    delta_time_string = delta_time()
    return render_template('mi_cv.html', delta_time_string=delta_time_string)

# KEYPHRASE EXTRACTION
@app.route('/keyphrase_extraction')
def keyphrase_extraction():
    """Route for the keyphrase extraction page"""
    return render_template('keyphrase_extraction.html')

@app.route('/keyphrase_extraction_process', methods=['POST'])
def keyphrase_extraction_process():
    """Processes the uploaded file for keyphrase extraction"""
    file = request.files.get('file')
    num_tables = int(request.form.get('num_tables', 0))
    num_rows = int(request.form.get('num_rows', 0))

    if file:
        try:
            data = file.read().decode('utf-8')
            results = procesar_archivo(data, num_tables=num_tables, num_rows=num_rows)
            return render_template('keyphrase_extraction.html', results=results)
        except Exception as e:
            print(f"Error processing file: {e}")
    return redirect(url_for('keyphrase_extraction'))

# SEASONALITY PREDICTION
@app.route('/seasonality_prediction', methods=['GET', 'POST'])
def seasonality_prediction():
    """Route for seasonality prediction"""
    try:
        existing_plots = []  # List to store the names of existing image files
        if request.method == 'POST':
            file = request.files.get('file')
            periodicity = int(request.form.get('periodicity'))

            if file:
                try:
                    df = pd.read_excel(file)
                    if len(df.columns) == 1:
                        serie = df[df.columns[0]]
                        
                        print(np.concatenate([serie.values, serie[-periodicity:].values]).ravel())

                        forecasted_values_last_period = forecasting(serie.values[:-periodicity], periodicity=periodicity)
                        
                        # print(serie.values[:-4,:].values.ravel().tolist() + forecasted_values_last_period)
                        # print(serie.values.ravel())
                        # print(forecasted_values_last_period)
                        # print(serie.values[-4:,:].values.ravel())
                        
                        forecasted_values_next_period = forecasting(serie, periodicity=periodicity)
                        # print(range(len(serie) - 1, len(serie) + len(forecasted_values_next_period)))
                        # print(np.concatenate([serie.values[-1].values,forecasted_values_next_period]))
                        # print(range(len(serie)))
                        # print(serie.values.ravel())
                        
                        generate_plots(serie, forecasted_values_last_period, forecasted_values_next_period, periodicity)

                        # Get the list of existing image file names
                        for filename in ['original_data.png', 'all_periods_data.png', 'historic_and_prediction_data.png']:
                            if os.path.exists(os.path.join('static', 'seasonality_prediction', filename)):
                                existing_plots.append(filename)

                        return render_template('seasonality_prediction.html', forecast=forecasted_values_next_period, existing_plots=existing_plots, enumerate=enumerate)
                    else:
                        return "The Excel file has more than one column"
                except Exception as e:
                    print(f"Error processing file: {e}")
                    return render_template('seasonality_prediction_error.html')
        return render_template('seasonality_prediction.html')
    except Exception as e:
        print(f"Error: {e}")
        return render_template('seasonality_prediction_error.html')

# WORLD BANK
@app.route('/world_bank')
def world_bank():
    """Route for the World Bank page"""
    return render_template('world_bank.html', indicators=indicators)

@app.route('/fetch_options')
def fetch_options():
    """Fetches country or year options for a World Bank indicator"""
    indicator_id = request.args.get('indicator')
    type = request.args.get('type')
    data = get_country_data_for_indicator(indicator_id)

    if not data:
        return jsonify([])

    if type == 'country':
        options = sorted({entry['country']['value'] for entry in data})
    elif type == 'year':
        options = sorted({entry['date'] for entry in data}, reverse=True)
    else:
        options = []

    return jsonify(options)

@app.route('/fetch_data')
def fetch_data():
    """Fetches data for a specific country or year"""
    indicator_id = request.args.get('indicator')
    type = request.args.get('type')
    option = request.args.get('option')
    data = get_country_data_for_indicator(indicator_id)

    if not data:
        return jsonify([])

    if type == 'country':
        filtered_data = [entry for entry in data if entry['country']['value'] == option]
    elif type == 'year':
        filtered_data = [entry for entry in data if entry['date'] == option]
    else:
        filtered_data = []

    df = pd.DataFrame([
        (entry['country']['value'], entry['date'], entry['value'])
        for entry in filtered_data
    ], columns=['COUNTRY', 'DATE', 'VALUE'])

    # Sort by 'COUNTRY' in ascending order and by 'DATE' in descending order
    df = df.sort_values(by=['COUNTRY', 'DATE'], ascending=[True, False])
    df.drop_duplicates(inplace=True)

    return df.to_dict(orient='records')

@app.route('/download_csv')
def download_csv():
    """Generates and downloads a CSV file with the filtered data"""
    indicator_id = request.args.get('indicator')
    type = request.args.get('type')
    option = request.args.get('option')
    data = get_country_data_for_indicator(indicator_id)

    if not data:
        return "No data available"

    if type == 'country':
        filtered_data = [entry for entry in data if entry['country']['value'] == option]
    elif type == 'year':
        filtered_data = [entry for entry in data if entry['date'] == option]
    else:
        filtered_data = []

    df = pd.DataFrame([
        (entry['country']['value'], entry['date'], entry['value'])
        for entry in filtered_data
    ], columns=['COUNTRY', 'DATE', 'VALUE'])

    # Sort by 'COUNTRY' in ascending order and by 'DATE' in descending order
    df = df.sort_values(by=['COUNTRY', 'DATE'], ascending=[True, False])

    # Create the CSV file
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    os.makedirs(downloads_folder, exist_ok=True)
    csv_path = os.path.join(downloads_folder, 'data.csv')
    df.to_csv(csv_path, index=False)

    # Send the CSV file to the client
    return send_file(csv_path, mimetype='text/csv', as_attachment=True, download_name='data.csv')

@app.route('/interactive_graph', methods=['POST'])
def interactive_graph():
    """Generates an interactive graph based on the selected indicator, type, and option"""
    indicator = request.form.get('indicator')
    type = request.form.get('type')
    option = request.form.get('option')

    # Get data for the selected country or year
    data = get_country_data_for_indicator(indicator)

    # Filter based on the selected type (country or year)
    if type == 'country':
        filtered_data = [entry for entry in data if entry['country']['value'] == option]
    elif type == 'year':
        filtered_data = [entry for entry in data if entry['date'] == option]
    else:
        return "Invalid type"

    df = pd.DataFrame([
        (entry['countryiso3code'], entry['country']['value'], entry['date'], entry['value'])
        for entry in filtered_data
    ], columns=['ISO_CODE', 'COUNTRY', 'DATE', 'VALUE'])

    # Sort by 'COUNTRY' in ascending order and by 'DATE' in descending order
    df = df.sort_values(by=['COUNTRY', 'DATE'], ascending=[True, False])

    # Execute the appropriate graph function
    if type == 'country':
        plot_time_series(df, title=option)
    elif type == 'year':
        plot_heatmap(df)

    return "Interactive graph generated."

# WHATSAPP
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

def create_dash_layout(df, days_of_the_week, months):
    if df.empty:
        return html.Div([
            html.H1("Cantidad de Mensajes por Emisor"),
            html.P("No data available.")
        ])
    return html.Div([
        html.H1("Choose an issuer in the dropdown menu".capitalize()),
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

days_of_the_week = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday',
                    5: 'Saturday', 6: 'Sunday'}
months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 
        12: 'December'}

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
    
    if selected_issuer == "GENERAL":
    
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

# RUNNING SCRIPT
if __name__ == '__main__':
    app.run(debug=True)
