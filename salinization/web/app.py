import requests

from flask import Flask, request, render_template

from forms.analysis import AnalysisForm
from utils.rest import invoke_get_request, get_chart_url
from utils import config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ebs-salinization-bentre'

@app.route('/')
@app.route('/index')
def home():
    form = AnalysisForm()
    return render_template('home.html', form=form)


@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    if request.method == 'GET':
        station = request.args.get('station')
        start = request.args.get('start')
        end = request.args.get('end')
    else:
        station = request.form['station']
        start = request.form['start']
        end = request.form['end']

    result = invoke_get_request(f'/forecast/{station}/{start}/{end}')

    return render_template('result.html', station=station, result=result, len=len(result.get('data')), chart=f'/chart/{result.get("chart")}')    


@app.route('/chart/<string:file>', methods=['GET'])
def stream_chart(file):
    return requests.get(get_chart_url(file)).content


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    debug = config.get_config()['rest']['debug'].get(True)

    # host 0.0.0.0 allows the app running on host machine ip
    app.run(host='0.0.0.0', port=5000, debug=debug)