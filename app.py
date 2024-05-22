from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mi_cv')
def mi_cv():
    return render_template('mi_cv.html')
    
if __name__ == '__main__':
    app.run(debug=True)
