from app import app,db


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False, unique=True)
    archive = db.Column(db.Boolean, nullable=False, default=False)
    likes = db.relationship('Like', backref='link', lazy=True)
    dislikes = db.relationship('Dislike', backref='link', lazy=True)
    categories = db.relationship('Category', backref='link', lazy=True)
    types = db.relationship('Type', backref='link', lazy=True)
    tags = db.relationship('Tag', backref='link', lazy=True)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))

class Dislike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))

class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))

    
def insert_data():
    # Insert Categories
    categories = ['tools', 'courses']
    for category in categories:
        db.session.add(Category(name=category))

    # Insert Types
    types = ['network', 'blue', 'red', 'purple','dev', 'system','online', 'others', 'devops']
    for type in types:
        db.session.add(Type(name=type))

    # Insert Tags
    tags = ['mitm', 'dos', 'web', 'exploit', 'privesc', 'lateral', 'se', 'forensics', 'osint', 'ctf', 'reverse', 'iot', 'isc','python', 'windows', 'android', 'linux', 'ios', 'docker', 'password']
    for tag in tags:
        db.session.add(Tag(name=tag))

    db.session.commit()

    
with app.app_context():
    db.create_all()
#     try:
#         insert_data()
#     except IntegrityError:
#         pass
