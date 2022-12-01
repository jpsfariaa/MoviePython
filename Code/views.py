from flask import render_template, request, redirect, session, flash, url_for, jsonify
from . import app, db
from .models import Filmes, Plataformas, Comentarios, Usuarios
import os, json, mysql.connector, zipfile as zip
from mysql.connector import errorcode
import urllib.request

# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/conectar', methods = ['POST'])
def conectar():
    usuario = Usuarios.query.filter_by(email=request.form['email']).first()

    if usuario:
        if request.form['senha'] != usuario.senha:
            flash('A Senha Inserida está Incorreta!', category = 'error')
            return redirect(url_for('/login'))
        if request.form['senha'] == usuario.senha:
            flash('O Usuário' + usuario.nome_usuario + ' foi Logado com Sucesso!')
            return redirect()
    else:
        flash('[ERRO]: Falha no LogIn de Usuário.')
        return redirect(url_for('login'))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/criar-usuario', methods = ['POST'])
def criar_usuario():
    email = request.form['email']
    nome_usuario = request.form['nome_usuario']
    senha = request.form['senha']

    usuario = Usuarios.query.filter_by(email = email).first()

    if usuario:
        flash('O Usuário Inserido já Existe.', category = 'error')
        return redirect(url_for('login'))
    else:
        novo_usuario = Usuarios(email = email, nome_usuario = nome_usuario, senha = senha)

        db.session.add(novo_usuario)
        db.session.commit()

        flash('O Usuário foi Criado com Sucesso!', category = 'success')
        return redirect(url_for('login'))
    
@app.route('/desconectar')
def desconectar():
    session['logged_user'] = None
    flash('Você foi Desconectado...', category = 'message')
    return redirect(url_for('login'))

@app.route('/infos')
def infos():
    return render_template('info_app.html')

@app.route('/exportar/<nome_tabela>')
def exportar(nome_tabela):
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('index'))

    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '12345'
        )
    except mysql.connector.Error as erro:
        if erro.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('[ERRO]: Verifique seu Nome de Usuário e Senha.')
        else:
            print(erro)

    cursor = connection.cursor(dictionary = True)
    cursor.execute("USE bancofilmes;")
    cursor.execute('''SELECT *
    FROM {0})'''.format(nome_tabela))

    select = cursor.fetchall()

    with open("export_data.json", "w", encoding = 'utf8') as export_archive:
        json.dump(select, export_archive)

    arquivo_zip = zip.ZipFile('{0}.zip'.format(nome_tabela), 'w')
    arquivo_zip.write('export_data.json')
    arquivo_zip.close()
    flash('O Arquivo em ZIP, foi Baixado com Sucesso!')

    return redirect(url_for(nome_tabela.lower()))

# Rotas com o Modelo "Usuários"
@app.route('/deletarusuario/<int:id_usuario>')
def deletarusuario(id_usuario):
    flash('O Usuário foi Removido com Sucesso!')
    return redirect(url_for('usuarios'))


# Rotas com o Modelo "Filmes"
@app.route('/filmes')
def filmes():
    lista_filmes = Filmes.query.order_by(Filmes.id_filme)
    return render_template('filmes.html', filmes = lista_filmes)
    
@app.route('/novofilme')
def novofilme():
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('index'))
    return render_template('novo_filme.html')

@app.route('/adicionarfilme', methods = ['POST'])
def adicionarfilme():
    nome_filme = request.form['nome_filme']
    data_lancamento = request.form['data_lancamento']
    nome_diretor = request.form['nome_diretor']
    nome_ator = request.form['nome_ator']

    novo_filme = Filmes(nome_filme = nome_filme, data_lancamento = data_lancamento, nome_diretor = nome_diretor, nome_ator = nome_ator)

    db.session.add(novo_filme)
    db.session.commit()

    return redirect(url_for('filmes'))

@app.route('/editarfilme/<int:id_filme>')
def editarfilme(id_filme):
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('index'))
    filme = Filmes.query.filter_by(id_filme = id_filme).first()
    return render_template('editar_filme.html')

@app.route('/alterarfilme', methods = ['POST'])
def alterarfilme():
    filme = Filmes.query.filter_by(id_filme = request.form['id_filme']).first()

    filme.nome_filme = request.form['nome_filme']
    filme.data_lancamento = request.form['data_lancamento']
    filme.nome_diretor = request.form['nome_diretor']
    filme.nome_ator = request.form['nome_ator']

    db.session.add(filme)
    db.session.commit()

    return redirect(url_for('filmes'))

@app.route('/deletarfilme/<int:id_filme>')
def deletarfilme(id_filme):
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('index'))
    filme = Filmes.query.filter_by(id_filme = id_filme).delete()
    db.session.commit()
    flash('O Filme foi Removido com Sucesso!')

    return redirect(url_for('filmes'))


# Rotas com o Modelo "Plataformas"
@app.route('/plataformas')
def plataformas():
    lista_plataformas = Plataformas.query.order_by(Plataformas.nome_plataforma)
    return render_template('plataformas.html', plataformas = lista_plataformas)

@app.route('/novaplataforma')
def novaplataforma():
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('index'))
    return render_template('nova_plataforma.html')

@app.route('/adicionarplataforma', methods = ['POST'])
def adicionarplataforma():
    nome_plataforma = request.form['nome_plataforma']

    nova_plataforma = Plataformas(nome_plataforma = nome_plataforma)

    db.session.add(nova_plataforma)
    db.session.commit()

    return redirect(url_for('plataformas'))

@app.route('/editarplataforma/<int:id_plataforma>')
def editarplataforma(id_plataforma):
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('index'))
    plataforma = Plataformas.query.filter_by(Plataformas.nome_plataforma).first()
    return render_template('editar_plataforma.html')

@app.route('/alterarplataforma', methods = ['POST'])
def alterarplataforma():
    plataforma = Plataformas.query.filter_by(nome_plataforma = request.form['nome_plataforma']).first()

    plataforma.nome_plataforma = request.form['nome_plataforma']

    db.session.add(plataforma)
    db.session.commit()

    return redirect(url_for('plataformas'))

@app.route('/deletarplataforma/<int:id_plataforma>')
def deletarplataforma(id_plataforma):
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('index'))
    plataforma = Plataformas.query.filter_by(id_plataforma = id_plataforma).delete()
    db.session.commit()
    flash('A Plataforma foi Removida com Sucesso!')

    return redirect(url_for('plataformas'))


# Rotas com o Modelo "Comentários"
@app.route('/comentarios')
def comentarios():
    lista_comentarios = Comentarios.query.order_by(Comentarios.id_comentario)
    return render_template('comentarios.html', comentarios = lista_comentarios)

@app.route('/novocomentario')
def novocomentario():
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('index'))
    return render_template('novo_comentario.html')

@app.route('/adicionarcomentario', methods = ['POST'])
def adicionarcomentario():
    nome_comentario = request.form['nome_comentario']

    novo_comentario = Comentarios(comentario = comentario)

    db.session.add(novo_comentario)
    db.session.commit()

    return redirect(url_for('comentarios'))

@app.route('/editarcomentario/<int:id_comentario>')
def editarcomentario(id_comentario):
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('index'))
    plataforma = Plataformas.query.filter_by(id_comentario = id_comentario).first()
    return render_template('editar_comentario.html')

@app.route('/alterarcomentario', methods = ['POST'])
def alterarcomentario():
    comentarioo = Comentarios.query.filter_by(comentario = request.form['comentario']).first()

    comentarioo.comentario = request.form['comentario']

    db.session.add(comentarioo)
    db.session.commit()

    return redirect(url_for('comentarios'))

@app.route('/deletarcomentario/<int:id_comentario>')
def deletarcomentario(id_comentario):
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('index'))
    comentario = Comentarios.query.filter_by(id_comentario = id_comentario).delete()
    db.session.commit()
    flash('O Comentário foi Removido com Sucesso!')

    return redirect(url_for('comentarios'))