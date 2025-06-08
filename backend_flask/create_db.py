# create_db.py
import os
from app import create_app, db # Assurez-vous que 'create_app' et 'db' sont importables de votre 'app'

# Obtenez le chemin absolu du répertoire actuel (backend_flask)
basedir = os.path.abspath(os.path.dirname(__file__))

# Créez l'instance de l'application Flask
app = create_app()

# Configurez la base de données pour pointer vers le fichier app.db dans le même répertoire
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Bonne pratique pour éviter un avertissement

# Exécutez le code dans le contexte de l'application Flask
with app.app_context():
    # Supprime toutes les tables existantes (même si app.db est effacé, c'est une sécurité)
    db.drop_all()
    # Crée toutes les tables définies dans vos modèles (Article, Product, etc.)
    # avec toutes leurs colonnes.
    db.create_all()
print("Base de données app.db recréée avec succès et toutes les colonnes.")