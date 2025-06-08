# app/routes.py

from flask import jsonify, request, Blueprint
from app import db 
from app.models import Article, Product 
from datetime import datetime
from sqlalchemy import func # Import nécessaire pour utiliser func.count() et func.lower()
from sqlalchemy import or_

blog_bp = Blueprint('blog_bp', __name__, url_prefix='/api/blog')

# ====================================================================
# Fonctions utilitaires de sérialisation
# ====================================================================

def serialize_article(article):
    return article.to_dict()

def serialize_product(product):
    return product.to_dict()

# ====================================================================
# Routes pour les articles de blog
# ====================================================================

# 1. Route pour OBTENIR TOUS les articles (LISTE) - Supporte le filtrage par catégorie (insensible à la casse)
# 1. Route pour OBTENIR TOUS les articles (LISTE) - Supporte le filtrage par catégorie (insensible à la casse)
# 1. Route pour OBTENIR TOUS les articles (LISTE) - Supporte le filtrage par catégorie (insensible à la casse)
@blog_bp.route('/articles', methods=['GET'])
def get_articles_list():
    category = request.args.get('category') # Récupère le paramètre 'category' de l'URL
    
    query = Article.query # Commence avec la requête de base

    if category:
        # Convertit la catégorie de la requête en minuscules
        search_category_lower = category.lower()
        
        # Filtre les articles en convertissant aussi la catégorie de la DB en minuscules pour la comparaison
        query = query.filter(
            func.lower(Article.category) == search_category_lower
        )
    
    # TRIER TOUJOURS PAR DATE DÉCROISSANTE ---
    articles = query.order_by(Article.date.desc()).all()
    # -------------------------------------------------------------
    
    return jsonify([serialize_article(article) for article in articles])

# NOUVELLE ROUTE : Pour la recherche d'articles
@blog_bp.route('/articles/search', methods=['GET'])
def search_articles():
    query_param = request.args.get('q', '').strip() # Récupère le terme de recherche 'q'
    
    if not query_param:
        return jsonify([]) # Retourne une liste vide si aucun terme de recherche n'est fourni

    # Construit la requête de recherche, insensible à la casse
    # On utilise `ilike` pour une recherche insensible à la casse dans MySQL
    # et `or_` pour chercher dans plusieurs colonnes
    search_results = Article.query.filter(
        or_(
            Article.title.ilike(f'%{query_param}%'),
            Article.content.ilike(f'%{query_param}%'),
            Article.author.ilike(f'%{query_param}%')
        )
    ).order_by(Article.date.desc()).all()
    
    return jsonify([serialize_article(article) for article in search_results])


# 2. Route pour OBTENIR UN SEUL article par ID (DÉTAIL)
@blog_bp.route('/articles/<int:article_id>', methods=['GET'])
def get_article_by_id(article_id):
    article = Article.query.get_or_404(article_id)
    return jsonify(serialize_article(article))

# 2.1. NOUVELLE ROUTE : Pour OBTENIR UN SEUL article par SLUG (DÉTAIL)
@blog_bp.route('/articles/<string:article_slug>', methods=['GET'])
def get_article_by_slug(article_slug):
    article = Article.query.filter_by(slug=article_slug).first_or_404()
    return jsonify(serialize_article(article))

# 3. Route pour CRÉER un article (POST) - Prend en compte toutes les colonnes du modèle
@blog_bp.route('/articles', methods=['POST'])
def create_article():
    data = request.get_json()

    if not all(key in data for key in ['title', 'slug', 'content']):
        return jsonify({'error': 'Missing required fields (title, slug, content)'}), 400

    article_date = None
    if 'date' in data and data['date']:
        try:
            article_date = datetime.fromisoformat(data['date'])
        except ValueError:
            article_date = datetime.utcnow()
    else:
        article_date = datetime.utcnow()

    # Retour à l'ancienne méthode pour la catégorie : stockée telle quelle, avec défauts
    new_article = Article(
        title=data['title'],
        slug=data['slug'],
        content=data['content'],
        author=data.get('author', 'Anonyme'),
        image=data.get('image'),
        date=article_date,
        category=data.get('category', 'General'), # Catégorie stockée telle quelle
        read_time=data.get('readTime', '5 min read'), 
        author_image=data.get('author_image', 'https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg?auto=compress&cs=tinysrgb&w=1600'),
        author_role=data.get('author_role', 'Editor')
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    return jsonify({'message': 'Article créé avec succès', 'article': serialize_article(new_article)}), 201

# Endpoint pour supprimer un article par ID
@blog_bp.route('/articles/<int:article_id>', methods=['DELETE'])
def delete_article_by_id(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return jsonify({'message': f'Article {article_id} supprimé avec succès'}), 200

# Endpoint pour SUPPRIMER TOUS les articles
@blog_bp.route('/articles', methods=['DELETE'])
def delete_all_articles():
    try:
        num_deleted = db.session.query(Article).delete()
        db.session.commit()
        return jsonify({'message': f'{num_deleted} articles supprimés avec succès.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erreur lors de la suppression de tous les articles: {str(e)}'}), 500

# Route pour OBTENIR LES CATÉGORIES ET LEUR COMPTE - Renvoie le nom tel quel de la DB
@blog_bp.route('/categories', methods=['GET'])
def get_categories():
    categories_with_count = db.session.query(
        Article.category, # C'est le nom de catégorie tel que stocké
        func.count(Article.id)
    ).group_by(Article.category).all()

    formatted_categories = []
    for category_name, count in categories_with_count:
        if category_name:
            # Renvoie le nom tel quel. Next.js le mettra en minuscules pour le lien.
            formatted_categories.append({
                'name': category_name, 
                'count': count
            })
    
    formatted_categories.sort(key=lambda x: x['count'], reverse=True)
    
    return jsonify(formatted_categories)

# Route pour OBTENIR LES ARTICLES RÉCENTS
@blog_bp.route('/recent-posts', methods=['GET'])
def get_recent_posts():
    limit = request.args.get('limit', default=3, type=int)
    recent_articles = Article.query.order_by(Article.date.desc()).limit(limit).all()
    return jsonify([serialize_article(article) for article in recent_articles])


# ====================================================================
# Routes pour les produits e-commerce (inchangées)
# ====================================================================

