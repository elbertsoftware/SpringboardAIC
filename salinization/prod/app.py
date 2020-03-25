from flask import Flask, jsonify, request, send_file

from salinization import config, data, models, visualization as viz

# create a flask app
app = Flask(__name__)

# retrieve list of top station endpoint
@app.route('/station', methods=['GET'])
def get_stations():
    stations = data.load_stations()

    return jsonify({'stations': stations.tolist()})


# forecast endpoint
@app.route('/forecast/<string:code>/<int:start>/<int:end>', methods=['GET'])
def forecast(code, start, end):
    result = models.forecast(code, start, end)

    return jsonify(result)


# stream chart image endpoint
@app.route('/chart/<string:file>', methods=['GET'])
def stream_chart(file):
    return send_file(f'{viz.IMAGE_TEMP_LOC}/{file}')


# cleanup chart images endpoint
@app.route('/admin/chart/clean', methods=['DELETE'])
def clean_up_charts():
    count = viz.clean_up_charts()
    return jsonify({'count': count})


# driver function
if __name__ == '__main__':
    port = config.get_config()['rest']['port'].get()
    debug = config.get_config()['rest']['debug'].get(True)

    # host 0.0.0.0 allows the app running on host machine ip
    app.run(host='0.0.0.0', port=port, debug=debug)
