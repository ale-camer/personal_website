from flask import Flask, render_template, request, redirect, url_for, send_file
from keyphrase_extraction import procesar_archivo
from seasonality_prediction import forecasting, generate_plots
import os, requests
import pandas as pd
from world_bank import indicators, get_country_data_for_indicator

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
remove_old_plots()

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

@app.route('/fetch_data')
def fetch_data():
    indicator_id = request.args.get('indicator')
    data = get_country_data_for_indicator(indicator_id)

    if not data:
        return jsonify([])

    df = pd.DataFrame([
        (entry['country']['value'], entry['date'], entry['value'])
        for entry in data[1] if entry['value'] is not None
    ], columns=['COUNTRY', 'DATE', 'VALUE'])

    df.drop_duplicates(inplace=True)
    return df.to_dict(orient='records')

@app.route('/download_csv')
def download_csv():
    indicator = request.args.get('indicator')
    indicator_id = indicators[indicator]
    data = get_country_data_for_indicator(indicator_id)

    if not data:
        return "No data available", 404

    df = pd.DataFrame([
        (entry['country']['value'], entry['date'], entry['value'])
        for entry in data[1] if entry['value'] is not None
    ], columns=['COUNTRY', 'DATE', 'VALUE'])

    df.drop_duplicates(inplace=True)
    csv_path = '/tmp/indicator_data.csv'
    df.to_csv(csv_path, index=False)

    return send_file(csv_path, as_attachment=True, download_name=f'{indicator}.csv')

if __name__ == '__main__':
    app.run(debug=True)
  