from blogdavi import app, database, bcrypt
from flask import render_template, flash, redirect, url_for, request, abort
from blogdavi.forms import FormCriarConta, FormLogin, FormPerfil, FormPost
from blogdavi.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image
import secrets
import os


@app.route("/")
def homepage():
    posts = Post.query.order_by(Post.id.desc())
    return render_template("homepage.html", posts=posts)


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template("usuarios.html", lista_usuarios= lista_usuarios)


@app.route('/login', methods=["POST", "GET"])
def login():
    if not current_user.is_authenticated:
        form_login = FormLogin()
        form_criar = FormCriarConta()

        if form_login.validate_on_submit() and 'botao_login' in request.form:
            usuario = Usuario.query.filter_by(email= form_login.email.data).first()
            if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
                login_user(usuario, remember=form_login.lembrar_login.data)
                flash('Login realizado com sucesso!', 'alert-success') #f'Login realizado com sucesso em: {form_login.email.data}'
                par_next = request.args.get('next')
                if par_next:
                    return redirect(par_next)
                else:
                    return redirect(url_for('homepage'))
            else:
                flash('Falha no Login, Email ou Senha incorretos!', 'alert-danger')

        if form_criar.validate_on_submit() and 'botao_criar' in request.form:
            senha_cript = bcrypt.generate_password_hash(form_criar.senha.data)
            usuario = Usuario(username= form_criar.username.data, email= form_criar.email.data, senha= senha_cript)
            database.session.add(usuario)
            database.session.commit()
            flash('Conta criada com sucesso!', 'alert-success')
            return redirect(url_for('login'))

        return render_template("login.html", form_login = form_login, form_criar = form_criar)
    else:
        return redirect(url_for('perfil'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'alert-success')
    return redirect(url_for('homepage'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil= foto_perfil)


@app.route('/post/criar', methods=["POST", "GET"])
@login_required
def criar_post():
    form = FormPost()
    if form.validate_on_submit():
        post = Post(titulo= form.titulo.data, corpo= form.corpo.data, autor= current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com sucesso!', 'alert-success')
        return redirect(url_for('homepage'))
    return render_template('criarpost.html', form= form)


def atualizar_cursos(formulario):
    lista_cursos = []
    for campo in formulario:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)

# Adicionar um codigo aleatorio ao nome do arquivo, reduzir para o tamanho da minha exibição, salvar a imagem na pasta static/fotos_perfil
def salvar_imagem(imagem):

    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_completo = nome + codigo + extensao

    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_completo)

    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    imagem_reduzida.save(caminho_completo)

    return nome_completo


@app.route('/perfil/editar', methods=["POST", "GET"])
@login_required
def editar():
    form = FormPerfil()
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')

    if form.validate_on_submit():

        ant_cursos = current_user.cursos
        ant_foto = current_user.foto_perfil
        ant_username = current_user.username
        ant_email = current_user.email

        current_user.email = form.email.data
        current_user.username = form.username.data

        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem

        current_user.cursos = atualizar_cursos(form)

        database.session.commit()

        if ant_email != current_user.email or ant_username != current_user.username or ant_cursos != current_user.cursos or ant_foto != current_user.foto_perfil:
            flash('Perfil atualizado com sucesso!', 'alert-success')

        return redirect(url_for('perfil'))
    
    elif request.method == "GET":

        form.email.data = current_user.email
        form.username.data = current_user.username

    return render_template('editarperfil.html', foto_perfil= foto_perfil, form= form)


@app.route('/post/<post_id>', methods=["POST", "GET"])
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormPost()

        if form.validate_on_submit():

            ant_titulo = post.titulo
            ant_corpo = post.corpo

            post.titulo = form.titulo.data
            post.corpo = form.corpo.data

            database.session.commit()

            if ant_titulo != post.titulo or ant_corpo != post.corpo:
                flash('Post atualizado com sucesso!', 'alert-success')
                return redirect(url_for('homepage'))
        
        elif request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo

    else:
        form = None
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=["POST", "GET"])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post deletado com sucesso!', 'alert-success')
        return redirect(url_for('homepage'))
    else:
        abort(403)