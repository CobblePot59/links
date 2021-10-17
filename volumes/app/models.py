from app import db


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False, unique=True)
    archive = db.Column(db.Boolean, nullable=False, default=False)
    likes = db.relationship('Like', backref='link', lazy=True)
    dislikes = db.relationship('Dislike', backref='link', lazy=True)
    tags = db.relationship('Tag', backref='link', lazy=True)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))

class Dislike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))

db.create_all()
