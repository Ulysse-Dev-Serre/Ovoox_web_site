# routes_auth.py

from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

# Le préfixe /api est ajouté pour une meilleure organisation
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Crée un nouvel utilisateur en utilisant SQLAlchemy, hache son mot de passe,
    et le sauvegarde dans la base de données.
    """
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Tous les champs sont requis'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Ce courriel est déjà utilisé'}), 409

    password_hash = generate_password_hash(password)
    new_user = User(name=name, email=email, password_hash=password_hash)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Erreur de base de données: {str(e)}"}), 500

    return jsonify({'message': f'Utilisateur {name} créé avec succès'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Connecte un utilisateur en vérifiant ses identifiants avec SQLAlchemy.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Courriel et mot de passe requis'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Courriel ou mot de passe incorrect'}), 401

    user_info = {
        'id': user.id,
        'name': user.name,
        'email': user.email
    }
    
    return jsonify({
        'message': 'Connexion réussie',
        'user': user_info
    }), 200

# --- NOUVELLE ROUTE POUR LA MISE À JOUR DU PROFIL ---
@auth_bp.route('/user/update/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    """
    Met à jour les informations de l'utilisateur (nom, email) ou son mot de passe.
    """
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    # --- Mise à jour des informations personnelles ---
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        # Vérifier si le nouvel email n'est pas déjà pris par un autre utilisateur
        if data['email'] != user.email:
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return jsonify({'error': 'Ce courriel est déjà utilisé par un autre compte.'}), 409
        user.email = data['email']

    # --- Mise à jour du mot de passe ---
    if 'currentPassword' in data and 'newPassword' in data:
        current_password = data['currentPassword']
        new_password = data['newPassword']

        # 1. Vérifier si le mot de passe actuel est correct
        if not check_password_hash(user.password_hash, current_password):
            return jsonify({'error': 'Le mot de passe actuel est incorrect.'}), 401
        
        # 2. Hacher et sauvegarder le nouveau mot de passe
        user.password_hash = generate_password_hash(new_password)
        
    try:
        db.session.commit()
        # Retourner les informations mises à jour de l'utilisateur
        updated_user_info = {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
        return jsonify({
            'message': 'Profil mis à jour avec succès.',
            'user': updated_user_info
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Erreur lors de la mise à jour : {str(e)}"}), 500


