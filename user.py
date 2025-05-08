from flask import Blueprint, request, render_template, redirect, session, url_for
from decorators import admin_required

user = Blueprint("user", __name__, template_folder="templates")

user.secret_key = "admin123@@"

users = {
    "admin": {"password": "admin123", "is_admin": True},
    "user1": {"password": "123", "is_admin": False},
    "user2": {"password": "1234", "is_admin": False}
}

@user.route('/register_user')
def register_user():
    if not session.get('is_admin'):
        return '<h1>Acesso negado! Apenas administradores.</h1>'
    return render_template('register_user.html')


@user.route('/add_user', methods=['POST'])
def add_user():
    global users
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
    else:
        user = request.args.get('user', None)
        password = request.args.get('password', None)
    users[user] = password
    return render_template('users.html', devices=users)

@admin_required
@user.route('/list_users')
def list_users():
    global users
    return render_template('users.html', devices=users)

@user.route('/remove_user')
def remove_user():
    global users
    return render_template('remove_user.html', devices=users)

@user.route('/del_user', methods=['GET', 'POST'])
def del_user():
    global users
    if request.method == 'POST':
        user = request.form['user']
    else:
        user = request.args.get('user', None)
    users.pop(user)
    return render_template('users.html', devices=users)


@user.route('/validated_user', methods=['POST'])
def validated_user():
    user_input = request.form['user']
    password_input = request.form['password']
    if user_input in users and users[user_input]["password"] == password_input:
        session['username'] = user_input
        session['is_admin'] = users[user_input]["is_admin"]
        return redirect(url_for('user.home'))
    else:
        return '<h1>Invalid Credentials!</h1>'

@user.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('user.validated_user'))
    return render_template('home.html', user=session['username'])

@user.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect('http://localhost:8081')
