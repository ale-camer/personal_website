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
    if request.method == 'POST':
        file = request.files['file']
        periodicity = int(request.form['periodicity'])

        if file:
            # Leer el archivo Excel directamente desde la solicitud
            df = pd.read_excel(file)
            
            # Asegurarse de que el DataFrame tiene una columna de valores de serie temporal
            if 'value' in df.columns:
                serie = df['value']

                # Aplicar la función de forecasting
                forecasted_values = forecasting(serie, periodicity=periodicity)
                
                # Generar y guardar los gráficos
                generate_plots(serie, forecasted_values, periodicity)

                # Pasar los resultados a la plantilla
                return render_template('seasonality_prediction.html', forecast=forecasted_values, enumerate=enumerate)
            else:
                return "El archivo Excel no tiene una columna llamada 'value'."
    return render_template('seasonality_prediction.html')

if __name__ == '__main__':
    app.run(debug=True)
 