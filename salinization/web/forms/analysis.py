from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired

from utils.rest import invoke_get_request


class AnalysisForm(FlaskForm):
    stations = sorted(invoke_get_request('/station').get('stations'))

    station = SelectField('Station', choices=[(station, station) for station in stations])
    start = IntegerField('Start Year', default=2012, validators=[DataRequired('Start Year is required')])
    end = IntegerField('End Year', validators=[DataRequired('End Year is required')])
    submit = SubmitField('Forecast')
