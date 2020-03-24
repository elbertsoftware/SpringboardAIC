from flask import Flask, jsonify, request, send_file

from salinization import models
from salinization.visualization import IMAGE_TEMP_LOC

# create a flask app
app = Flask(__name__)

# forecast endpoint
@app.route('/forecast/<string:code>/<int:start>/<int:end>', methods=['GET', 'POST'])
def forecast(code, start, end):
    result = models.forecast(code, start, end)

    return jsonify(result)


# stream chart image
@app.route('/chart/<string:file>', methods=['GET', 'POST'])
def chart(file):
    return send_file(f'{IMAGE_TEMP_LOC}/{file}')


# driver function
if __name__ == '__main__':
    app.run(port=5000, debug=True)
