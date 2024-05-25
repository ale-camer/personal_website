from flask import Flask, render_template, request, redirect, url_for
import os
from keyphrase_extraction import procesar_archivo

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

if __name__ == '__main__':
    app.run(debug=True)
