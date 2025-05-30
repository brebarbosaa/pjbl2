from flask import redirect, url_for
from functools import wraps
from flask_login import current_user

def role_required(*roles):
    """
    Decorator que garante que o usuário autenticado possua uma das funções especificadas.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('user.login'))

            if current_user.role not in roles:
                return "<h1>Acesso negado! Permissão insuficiente.</h1>", 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Decorators específicos para facilitar a leitura nas rotas
admin_required = role_required('admin')
operador_required = role_required('admin', 'operador')
estatistico_required = role_required('admin', 'estatistico')
