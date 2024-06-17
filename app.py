from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import os, requests
import pandas as pd

from modules.keyphrase_extraction import procesar_archivo
from modules.seasonality_prediction import forecasting, generate_plots
from modules.world_bank import indicators, get_country_data_for_indicator, strings_to_exclude, plot_time_series, plot_heatmap

app = Flask(__name__)

def remove_old_plots():
    temp_images_path = 'static/temp_images'
    files_to_remove = ['original_data.png', 'all_periods_data.png', 'historic_and_prediction_data.png']
    
    for file in files_to_remove:
        file_path = os.path.join(temp_images_path, file)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
        else:
            print(f"File does not exist: {file_path}")

def remove_old_downloads():
    downloads_folder = 'downloads'
    
    if os.path.exists(downloads_folder):
        for filename in os.listdir(downloads_folder):
            file_path = os.path.join(downloads_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
    else:
        print(f"Folder does not exist: {downloads_folder}")

# Llamar a las funciones para eliminar archivos viejos
remove_old_plots()
remove_old_downloads()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mi_cv')
def mi_cv():
    return render_template('mi_cv.html')

@app.route('/keyphrase_extraction')
def keyphrase_extraction():
    return render_template('keyphrase_extraction.html')

@app.route('/keyphrase_extraction_process', methods=['POST'])
def keyphrase_extraction_process():
    file = request.files['file']
    num_tables = int(request.form['num_tables'])
    num_rows = int(request.form['num_rows'])

    if file:
        data = file.read().decode('utf-8')
        results = procesar_archivo(data, num_tables=num_tables, num_rows=num_rows)
        return render_template('keyphrase_extraction.html', results=results)
    return redirect(url_for('keyphrase_extraction'))

@app.route('/seasonality_prediction', methods=['GET', 'POST'])
def seasonality_prediction():
    try:
        existing_plots = []  # Lista para almacenar los nombres de los archivos de imagen existentes
        if request.method == 'POST':
            file = request.files['file']
            periodicity = int(request.form['periodicity'])

            if file:
                df = pd.read_excel(file)
                if len(df.columns) == 1:
                    serie = df[df.columns]
                    forecasted_values_last_period = forecasting(serie.iloc[:-periodicity,:], periodicity=periodicity)
                    forecasted_values_next_period = forecasting(serie, periodicity=periodicity)
                    generate_plots(serie, forecasted_values_last_period, forecasted_values_next_period, periodicity)
                    
                    # Obtener la lista de nombres de archivos de imagen existentes
                    for filename in ['original_data.png', 'all_periods_data.png', 'historic_and_prediction_data.png']:
                        if os.path.exists(os.path.join('static', 'temp_images', filename)):
                            existing_plots.append(filename)
                    
                    return render_template('seasonality_prediction.html', forecast=forecasted_values_next_period, existing_plots=existing_plots, enumerate=enumerate)
                else:
                    return "The Excel file has more than one column"
        return render_template('seasonality_prediction.html')
    except: 
        return render_template('seasonality_prediction_error.html')

@app.route('/world_bank')
def world_bank():
    return render_template('world_bank.html', indicators=indicators)

@app.route('/fetch_options')
def fetch_options():
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

    # Ordenar por 'COUNTRY' de forma ascendente y por 'DATE' de forma descendente
    df = df.sort_values(by=['COUNTRY', 'DATE'], ascending=[True, False])

    df.drop_duplicates(inplace=True)

    return df.to_dict(orient='records')

@app.route('/download_csv')
def download_csv():
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

    # Ordenar por 'COUNTRY' de forma ascendente y por 'DATE' de forma descendente
    df = df.sort_values(by=['COUNTRY', 'DATE'], ascending=[True, False])

    # Crear el archivo CSV
    downloads_folder = 'downloads'
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)
    csv_path = os.path.join(downloads_folder, 'data.csv')
    df.to_csv(csv_path, index=False)

    # Enviar el archivo CSV al cliente
    return send_file(csv_path, mimetype='text/csv', as_attachment=True, download_name='data.csv')

@app.route('/interactive_graph', methods=['POST'])
def interactive_graph():
    indicator = request.form['indicator']
    type = request.form['type']
    option = request.form['option']
    
    # Obtener los datos del país o año seleccionado
    data = get_country_data_for_indicator(indicator)
    
    # Filtrar según el tipo seleccionado (country o year)
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
    
    # Ordenar por 'COUNTRY' de forma ascendente y por 'DATE' de forma descendente
    df = df.sort_values(by=['COUNTRY', 'DATE'], ascending=[True, False])
    
    # Ejecutar la función de gráfico adecuada
    if type == 'country':
        plot_time_series(df, title=option)
    elif type == 'year':
        plot_heatmap(df)
    
    return "Interactive graph generated."

if __name__ == '__main__':
    app.run(debug=True)
  