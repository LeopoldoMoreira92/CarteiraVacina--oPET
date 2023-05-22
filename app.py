from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'alura'

class jogos:
    def __init__(self,nome,categoria,console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = jogos("Tibia","RPG","PC")
jogo2 = jogos("Ragnarok","RPG","PC")
jogo3 = jogos("Gun Bound","Estratégia","PC")
lista = [jogo1,jogo2,jogo3]

class Usuario:
    def __init__(self,nome, nickname,senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Leopoldo','Fujiro','Tibiao')
usuario2 = Usuario('Camila Ferreira','Cafe','Pao')
usuario3 = Usuario('Guilherme','Louro','cake')

usuarios = {usuario1.nickname : usuario1,
            usuario2.nickname : usuario2,
            usuario3.nickname : usuario3}   

@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('index')))
    else:
        return render_template('lista.html',nome="Jogos",jogos = lista, titulo ='Jogoteca')

@app.route('/novojogo')
def novojogo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Você precisa logar')
        return redirect(url_for('login',proxima=url_for('novojogo')))
    else:
        return render_template('novojogo.html', titulo="Novo Jogo")
        
@app.route('/criar', methods =["POST",])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = jogos(nome,categoria,console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=["POST",])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash( f'{usuario.nickname} logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina) 
    else:
        flash('Usuario não logado')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

app.run(debug=True)