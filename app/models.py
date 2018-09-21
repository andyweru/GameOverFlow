from app import create_app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    question = db.relationship('Question', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='comment', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User {self.id}, {self.name}, {self.username}, {self.image}, {self.email}, {self.pitches}, {self.comment}'


class Comment(db.Model, UserMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    ratings = db.Column(db.Integer)
    like = db.Column(db.Integer)
    dislike = db.Column(db.Integer)
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)
    pitch_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f'Comment {self.id}, {self.ratings}, {self.like}, {self.dislike}, {self.content}'


class Question(db.Model, UserMixin):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text)
    category = db.Column(db.String)
    comments_id = db.relationship(
        'Comment', backref='comments', lazy='dynamic')
    time = db.Column(db.DateTime)

    def __repr__(self):
        return f'Pitch {self.id}, {self.category}, {self.title}, {self.author}, {self.content}, {self.comment}'
