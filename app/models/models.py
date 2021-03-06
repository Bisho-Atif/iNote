from app import db
from datetime import datetime
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(64), index = True, unique=True)
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))
    notes = db.relationship('Note', backref='user')
    
class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(64), index = True)
    content = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 

db.create_all()
