from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from ..models import User
from wtforms import ValidationError
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField


class QuestionForm(FlaskForm):
    title = StringField('Question title')
    category = SelectField('Question Category', choices=[('product', 'product'),
                                                         ('service', 'service'),         ('promotion', 'promotion'),     ('interview', 'interview')])
    content = TextAreaField('ask your question')

    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    content = TextAreaField('comment')
    submit = SubmitField('Submit')
