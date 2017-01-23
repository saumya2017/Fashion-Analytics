from flask import Flask, render_template
import Twitter1
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result')
def result():
    return render_template('result.html', result = Twitter1.dictionary)

if __name__ == '__main__':
    app.run(debug = True)
