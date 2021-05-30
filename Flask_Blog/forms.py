from flask_wtf import FlaskForm
from wtforms import StringField

class Registration(FlaskForm):
    username = StringField('Username')