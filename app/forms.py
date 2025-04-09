from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired()])

class UploadForm(FlaskForm):
    layout = StringField("Layout", validators=[DataRequired()])
    periodo = StringField("Período", validators=[DataRequired()])
    file = FileField("Planilha", validators=[FileAllowed(['xls', 'xlsx'], 'Somente arquivos .xls ou .xlsx!')])
