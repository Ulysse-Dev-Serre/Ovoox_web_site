from app import create_app, db
from app.models import User, Article

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """
    Configure le contexte du shell Flask pour un débogage facile.
    Permet d'accéder à la base de données et aux modèles directement
    en utilisant la commande 'flask shell'.
    """
    return {'db': db, 'User': User, 'Article': Article}

if __name__ == '__main__':
    app.run(debug=True)