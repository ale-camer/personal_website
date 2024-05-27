from flask import Flask, render_template, request, redirect, url_for
from keyphrase_extraction import procesar_archivo
from seasonality_prediction import forecasting, generate_plots
import os
import pandas as pd

app = Flask(__name__)

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
    existing_plots = []  # Lista para almacenar los nombres de los archivos de imagen existentes
    if request.method == 'POST':
        file = request.files['file']
        periodicity = int(request.form['periodicity'])

        if file:
            df = pd.read_excel(file)
            if len(df.columns) == 1:
                serie = df[df.columns]
                forecasted_values = forecasting(serie, periodicity=periodicity)
                generate_plots(serie, forecasted_values, periodicity)
                
                # Obtener la lista de nombres de archivos de imagen existentes
                for filename in ['original_data.png', 'all_periods_data.png', 'historic_and_prediction_data.png']:
                    if os.path.exists(os.path.join('static', 'temp_images', filename)):
                        existing_plots.append(filename)
                
                return render_template('seasonality_prediction.html', forecast=forecasted_values, existing_plots=existing_plots, enumerate=enumerate)
            else:
                return "The Excel file has more than one column"
    return render_template('seasonality_prediction.html')

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

if __name__ == '__main__':
    app.run(debug=True)
  