from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from pepy.domain.model import ProjectName


class SearchForm(FlaskForm):
    project_name = StringField('Project name', validators=[
        DataRequired(),
        Length(max=ProjectName.MAX_LENGTH, min=ProjectName.MIN_LENGTH)
    ])
