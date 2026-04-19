from Backend.database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    favorites     = db.relationship('Favorite', backref='user', lazy=True)

class Favorite(db.Model):
    __tablename__  = 'favorites'
    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    listing_id     = db.Column(db.String(32), nullable=False)
    title          = db.Column(db.String(512))
    platform       = db.Column(db.String(128))
    price          = db.Column(db.String(64))
    url            = db.Column(db.String(1024))
    condition = db.Column(db.String(32), default='NONE')
    image          = db.Column(db.String(1024))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'listing_id', name='unique_user_listing'),
    )