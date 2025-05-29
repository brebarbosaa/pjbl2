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
    # FAKE LOGIN TEMPORÁRIO
    session['username'] = request.form['user']
    session['is_admin'] = True
    return redirect(url_for('user.home'))

    # código original:
    # username = request.form['user']
    # password = request.form['password']
    # ...

@user.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('user.login'))
    return render_template('home.html', user=session['username'])

@user.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@user.route('/home_direct')
def home_direct():
    session['username'] = 'teste'
    session['is_admin'] = True
    return redirect(url_for('user.home'))