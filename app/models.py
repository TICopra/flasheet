from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(255))
    saved_filename = db.Column(db.String(255))
    filepath = db.Column(db.String(255))
    layout = db.Column(db.String(100))
    periodo = db.Column(db.String(100))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com o usuário
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='uploads')