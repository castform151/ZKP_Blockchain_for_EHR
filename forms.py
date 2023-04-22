
from wtforms import Form, StringField, TextAreaField, PasswordField, BooleanField, SubmitField, validators
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class  ViewReportForm(Form):
    username=StringField('Username',[validators.Length(min=4,max=25)])

class SignupUser(Form):
    username =StringField('Userame',[validators.Length(min=4,max=25)])
    password =StringField('Password',[validators.Length(min=4,max=25)])
    submit =SubmitField('Signup')

class SignIn(Form):
    username =StringField('Userame',[validators.Length(min=4,max=25)])
    password =StringField('Password',[validators.Length(min=4,max=25)])
    remember_me =BooleanField('Remember me')
    submit =SubmitField('Login')

class AddReportForm(Form):
    report = TextAreaField('Report', [validators.length(min=8, max=200)])


class  ViewTransactionForm(Form):
    username=StringField('Username',[validators.Length(min=4,max=25)])


class SendReportForm(Form):
    recipient= StringField('Recipient Username', [validators.Length(min=4, max=25)])
    report = TextAreaField('Report', [validators.length(min=8, max=200)])
    # report = SelectField('Reports',)




    




