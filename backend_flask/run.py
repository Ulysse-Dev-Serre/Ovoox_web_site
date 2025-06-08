# run.py
from app import create_app, db # Importe create_app et db depuis app/__init__.py

app = create_app()

if __name__ == '__main__':
    with app.app_context(): # Ceci assure que 'db' est dans le contexte de l'application
        db.create_all() # Crée les tables si elles n'existent pas
    app.run(debug=True)