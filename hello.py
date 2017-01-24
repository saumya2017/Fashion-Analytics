from flask import Flask, render_template, request, jsonify
import Twitter1 as analyseTweets
import json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/product/<product_name>')
def renderProductPage(product_name):
    return render_template('result.html', result= analyseTweets.createData(product_name))

@app.route('/topBrands', methods=['GET'])
def getTopBrandsInformation():
    product_name = request.args.get('product')
    data = analyseTweets.createData(product_name)
    return jsonify(**data)

if __name__ == '__main__':
    app.run(debug = True)
