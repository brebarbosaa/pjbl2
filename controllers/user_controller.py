from flask import Blueprint, request, render_template, redirect, session, url_for
from models.users.user_model import User
from models.db import db
from decorators import admin_required
from flask_login import login_user

user = Blueprint("user", __name__, template_folder="templates")

@user.route('/register_user')
@admin_required
def register_user():
    return render_template('register_user.html')

@user.route('/add_user', methods=['POST'])
@admin_required
def add_user():
    username = request.form['user']
    password = request.form['password']
    role = request.form['role']  # 'operador', 'estatistico', 'comum'

    # Nunca deve ser possível criar outro admin
    if role == 'admin':
        return "Não é permitido criar outro administrador.", 403

    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('user.list_users'))


@user.route('/list_users')
@admin_required
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@user.route('/remove_user')
@admin_required
def remove_user():
    users = User.query.all()
    return render_template('remove_users.html', users=users)


@user.route('/del_user', methods=['POST'])
@admin_required
def del_user():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    if user and user.role != 'admin':
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('user.list_users'))


@user.route('/edit_user/<int:user_id>')
@admin_required
def edit_user(user_id):
    user_obj = User.query.get_or_404(user_id)
    if user_obj.role == 'admin':
        return "Administrador não pode ser editado.", 403
    return render_template('update_user.html', user=user_obj)

@user.route('/update_user/<int:user_id>', methods=['POST'])
@admin_required
def update_user(user_id):
    user_obj = User.query.get_or_404(user_id)
    if user_obj.role == 'admin':
        return "Administrador não pode ser editado.", 403

    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    user_obj.username = username
    if password:  # só muda se não for vazio
        user_obj.password = password
    user_obj.role = role
    db.session.commit()
    return redirect(url_for('user.list_users'))


@user.route('/validated_user', methods=['POST'])
def validated_user():
    username = request.form['user']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        login_user(user)
        return redirect(url_for('user.home'))

    return render_template("login.html", error="Credenciais inválidas.")


@user.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('user.login'))
    return render_template('home.html', user=session['username'], role=session.get('role'))


@user.route('/login')
def login():
    return render_template('login.html')


@user.route('/logout')
def logout():
    session.clear()
    return redirect('/')
