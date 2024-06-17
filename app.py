from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import os
import pandas as pd

from modules.keyphrase_extraction import procesar_archivo
from modules.seasonality_prediction import forecasting, generate_plots
from modules.world_bank import indicators, get_country_data_for_indicator, strings_to_exclude, plot_time_series, plot_heatmap

app = Flask(__name__)

# Function to remove old files
def remove_old_files(folder, files_to_remove=None):
    """
    Removes specific files in a folder or all files in a folder if not specified.
    
    :param folder: Folder from which files will be removed.
    :param files_to_remove: List of filenames to remove. If None, all files will be removed.
    """
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            if files_to_remove and filename not in files_to_remove:
                continue
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")
            else:
                print(f"File does not exist: {file_path}")
    else:
        print(f"Folder does not exist: {folder}")

# Call the function to remove old files in specific folders
remove_old_files('static/temp_images')
remove_old_files('downloads')

# Application routes

@app.route('/')
def index():
    """Route for the main page"""
    return render_template('index.html')

@app.route('/mi_cv')
def mi_cv():
    """Route for the CV page"""
    return render_template('mi_cv.html')

@app.route('/keyphrase_extraction')
def keyphrase_extraction():
    """Route for the keyphrase extraction page"""
    return render_template('keyphrase_extraction.html')

@app.route('/keyphrase_extraction_process', methods=['POST'])
def keyphrase_extraction_process():
    """Processes the uploaded file for keyphrase extraction"""
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
    """Route for seasonality prediction"""
    try:
        existing_plots = []  # List to store the names of existing image files
        if request.method == 'POST':
            file = request.files['file']
            periodicity = int(request.form['periodicity'])

            if file:
                df = pd.read_excel(file)
                if len(df.columns) == 1:
                    serie = df[df.columns]
                    forecasted_values_last_period = forecasting(serie.iloc[:-periodicity, :], periodicity=periodicity)
                    forecasted_values_next_period = forecasting(serie, periodicity=periodicity)
                    generate_plots(serie, forecasted_values_last_period, forecasted_values_next_period, periodicity)

                    # Get the list of existing image file names
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
    downloads_folder = 'downloads'
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)
    csv_path = os.path.join(downloads_folder, 'data.csv')
    df.to_csv(csv_path, index=False)

    # Send the CSV file to the client
    return send_file(csv_path, mimetype='text/csv', as_attachment=True, download_name='data.csv')

@app.route('/interactive_graph', methods=['POST'])
def interactive_graph():
    """Generates an interactive graph based on the selected indicator, type, and option"""
    indicator = request.form['indicator']
    type = request.form['type']
    option = request.form['option']

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

if __name__ == '__main__':
    app.run(debug=True)
