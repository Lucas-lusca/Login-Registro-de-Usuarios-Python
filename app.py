# EXEMPLO DE LOGINPAGE

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'sua chave'
bcrypt = Bcrypt(app) # Usado para encriptar a senha
registered_users = {} # Lista que guarda os usuarios temporariamente

@app.route("/")
def index():
    return render_template('html/home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # resquest.form depende do name do input
        useremail = request.form['useremail']
        userpassword = request.form['userpassword']

        # Verifica se o email corresponde com a senha
        if useremail in registered_users and bcrypt.check_password_hash(registered_users[useremail], userpassword):
            # Define uma flag de autenticação na sessão do usuário
            session['logged_in'] = True
            return redirect(url_for('userpage'))
        else:
            flash('Senha ou email não compativeis.', 'error')
            return redirect(url_for('login'))
    else:
        # Lógica para lidar com a solicitação GET para a rota /login
        return render_template('html/login.html')
    
@app.route("/userpage", methods=['GET'])
def userpage():
    if 'logged_in' in session and session['logged_in']:
        return render_template('html/user.html')
    else:
        return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        useremail = request.form['useremail']
        userpassword = request.form['userpassword']

        if useremail == ''or userpassword == '':
            flash('Por favor, preencha todos os campos.', 'error')
            return redirect(url_for('register'))

        # Verifica se o usuario ja esta na lista
        if useremail in registered_users:
            flash('Usuário já cadastrado.', 'error')
            return redirect(url_for('register'))

        else:
            # Adiciona o usuario a lista
            hashed_password = bcrypt.generate_password_hash(userpassword).decode('utf-8')
            registered_users[useremail] = hashed_password
            flash('Cadastro realizado com sucesso!', 'info')
            return redirect(url_for('login'))
    else:
        return render_template('html/register.html')
    
if __name__ == '__main__':
    app.run(debug=True)