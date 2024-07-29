from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from blogdavi.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário: ', validators=[DataRequired()])
    email = StringField('E-mail: ', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha: ', validators=[DataRequired(), Length(6, 20)])
    confirm_senha = PasswordField('Confirmação da Senha: ', validators=[DataRequired(), EqualTo('senha')])
    botao_criar = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail ja cadastrado, utilize outro email ou faça login")
    
    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError("Nome de Usuário ja cadastrado, utilize outro ou faça login")
        

class FormLogin(FlaskForm):
    email = StringField('E-mail: ', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha: ', validators=[DataRequired(), Length(6, 20)])
    lembrar_login = BooleanField('Lembrar Login')
    botao_login = SubmitField('Fazer Login')


class FormPerfil(FlaskForm):
    username = StringField('Nome de Usuário: ', validators=[DataRequired()])
    email = StringField('E-mail: ', validators=[DataRequired(), Email()])
    botao = SubmitField('Confirmar edição')
    foto_perfil = FileField('Atualizar Foto de Perfil: ', validators=[FileAllowed(['jpg', 'png'])])

    curso_excel = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionadoras')
    curso_sql = BooleanField('SQL Impressionador')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError("E-mail ja cadastrado, utilize outro email")
            
    def validate_username(self, username):
        if current_user.username != username.data:
            usuario = Usuario.query.filter_by(username=username.data).first()
            if usuario:
                raise ValidationError("Nome de Usuário ja cadastrado")
            

class FormPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2,140)])
    corpo = TextAreaField('Escreva seu Post', validators=[DataRequired()])
    botao = SubmitField('Criar Post')