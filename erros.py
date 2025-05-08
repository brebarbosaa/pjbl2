from flask import Blueprint, render_template

erros_bp = Blueprint('erros', __name__)

@erros_bp.app_errorhandler(401)
def erro_401(error):
    return render_template('erro_generico.html',
                           codigo=401,
                           titulo="Não autorizado",
                           mensagem="Você precisa fazer login para acessar esta página."), 401

@erros_bp.app_errorhandler(403)
def erro_403(error):
    return render_template('erro_generico.html',
                           codigo=403,
                           titulo="Acesso proibido",
                           mensagem="Você não tem permissão para acessar este recurso."), 403

@erros_bp.app_errorhandler(404)
def erro_404(error):
    return render_template('erro_generico.html',
                           codigo=404,
                           titulo="Página não encontrada",
                           mensagem="A página que você está procurando não existe."), 404

@erros_bp.app_errorhandler(408)
def erro_408(error):
    return render_template('erro_generico.html',
                           codigo=408,
                           titulo="Tempo de requisição esgotado",
                           mensagem="O servidor demorou demais para responder."), 408

@erros_bp.app_errorhandler(429)
def erro_429(error):
    return render_template('erro_generico.html',
                           codigo=429,
                           titulo="Muitas requisições",
                           mensagem="Você fez muitas requisições em pouco tempo. Tente novamente mais tarde."), 429

@erros_bp.app_errorhandler(500)
def erro_500(error):
    return render_template('erro_generico.html',
                           codigo=500,
                           titulo="Erro interno do servidor",
                           mensagem="Ocorreu um erro inesperado. Estamos trabalhando para resolver isso."), 500

@erros_bp.app_errorhandler(503)
def erro_503(error):
    return render_template('erro_generico.html',
                           codigo=503,
                           titulo="Serviço indisponível",
                           mensagem="O servidor está temporariamente indisponível. Tente novamente em instantes."), 503
