# app/models.py

from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(60), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image = db.Column(db.String(255), nullable=True)

    # --- CES LIGNES DOIVENT ÊTRE PRÉSENTES ET DÉCOMMENTÉES ---
    category = db.Column(db.String(60), nullable=True)
    read_time = db.Column(db.String(20), nullable=True)
    author_image = db.Column(db.String(255), nullable=True)
    author_role = db.Column(db.String(60), nullable=True)
    # --------------------------------------------------------

    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'author': self.author,
            'image': self.image,
            'date': self.date.isoformat() if self.date else None,
            # --- CES LIGNES DOIVENT ÊTRE MODIFIÉES POUR RÉFÉRER À 'self.' ---
            'category': self.category,
            'readTime': self.read_time,
            'author_image': self.author_image,
            'author_role': self.author_role,
            # -------------------------------------------------------------
        }

    def __repr__(self):
        return f'<Article {self.title}>'
    












    

# La classe Product est laissée telle quelle si vous ne voulez pas la modifier maintenant
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(255), nullable=True) # GARDÉ COMME AVANT

    def __repr__(self):
        return f'<Product {self.name}>'

    def to_dict(self): # Ajouté la méthode to_dict pour Product si vous l'utilisez dans routes.py
        return {
            'id': str(self.id),
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'image_url': self.image_url
        }