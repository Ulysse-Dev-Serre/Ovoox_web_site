import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une_super_cle_secrete_que_personne_ne_devinera' # À changer pour une vraie clé secrète en production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False