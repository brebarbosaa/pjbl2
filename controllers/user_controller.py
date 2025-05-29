from flask import Blueprint, request, render_template, redirect, session, url_for
from models.users.user_model import User
from models.db import db
from decorators import admin_required

user = Blueprint("user", __name__, template_folder="templates")

@user.route('/register_user')
@admin_required
def register_user():
    if not session.get('is_admin'):
        return '<h1>Acesso negado! Apenas administradores.</h1>'
    return render_template('register_user.html')

@user.route('/add_user', methods=['POST'])
@admin_required
def add_user():
    username = request.form['user']
    password = request.form['password']
    new_user = User(username=username, password=password, is_admin=False)
    db.session.add(new_user)
    db.session.commit()
    users = User.query.all()
    return render_template('users.html', users=users)

@user.route('/list_users')
@admin_required
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@user.route('/remove_user')
@admin_required
def remove_user():
    global users
    return render_template('remove_users.html', users=users)

@user.route('/del_user', methods=['POST'])
@admin_required
def del_user():
    username = request.form['user']
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    users = User.query.all()
    return render_template('users.html', users=users)

@user.route('/validated_user', methods=['POST'])
def validated_user():
    username = request.form['user']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        # Se o usuário for admin, verifique se já existe outro admin logado (opcional, se quiser garantir 1 admin logado)
        session['username'] = user.username
        session['is_admin'] = user.is_admin
        return redirect(url_for('user.home'))

    return render_template("login.html", error="Credenciais inválidas.")


@user.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('user.login'))
    return render_template('home.html', user=session['username'])

# adicionei essa linha só pra conseguir rodar o login.html no meu computador, não sei se ela é realmente necessária - brenda
@user.route('/login')
def login():
    return render_template('login.html')


@user.route('/logout')
def logout():
    session.clear()
    return redirect('/')