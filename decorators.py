from flask import session, redirect, url_for, flash
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Acesso permitido apenas para administradores.", "danger")
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated_function
