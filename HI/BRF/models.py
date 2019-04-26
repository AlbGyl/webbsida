from datetime import datetime
from BRF import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    '''1=vanlig användare, 2=admin'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='1')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Styrelsen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    name = db.Column(db.String(100), nullable=False)
    adress = db.Column(db.String(100), nullable=False, default='adress')
    phone_number = db.Column(db.String(100), nullable=False, default='nummer')
    email = db.Column(db.String(120), nullable=False, default='email')
    ansvarsområde = db.Column(db.String(100), nullable=False, default='ansvarsområda')

    def __repr__(self):
        return f"Styrelsen('{self.name}', '{self.position}')"
