from flask import render_template, request, flash, redirect, url_for, session, jsonify
from sqlalchemy.exc import IntegrityError
from app import app, ldap, db
from models import Link, Like, DIslike, Category, Type, Tag
from decor import login_required
import validators

@app.route('/', methods=('GET', 'POST'))
@login_required
def index():
    links = Link.query.all()
    categories = Category.query.with_entities(Category.name).group_by(Category.name).all()
    types = Type.query.with_entities(Type.name).group_by(Type.name).all()
    tags = Tag.query.with_entities(Tag.name).group_by(Tag.name).all()
    return render_template('index.html', links=links, categories=categories, types=types, tags=tags)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('status'):
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('login.html')

    login = request.form['login']
    password = request.form['password']
    if str(ldap.authenticate(login+'@'+app.config['LDAP_DOMAIN'], password).status) == 'AuthenticationResponseStatus.success':
        session.update({'status':True, 'login':login})
        return redirect(url_for('index'))
    else:
        flash('Bad login', 'danger')
        return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
    session['status'] = False
    return redirect(url_for('login'))

def sdata(q):
    str_category = request.form['category']
    new_category = Category(name = str_category.strip().lower(), link_id = q.id)
    db.session.add(new_category)

    str_type = request.form['type']
    new_type = Type(name = str_type.strip().lower(), link_id = q.id)
    db.session.add(new_type)

    db.session.commit()

    str_tags = request.form['tags']
    for name in str_tags.split(','):
        new_tag = Tag(name = name.strip().lower(), link_id = q.id)
        db.session.add(new_tag)
        db.session.commit()

@app.route('/add', methods=['POST'])
@login_required
def add():
    url = request.form['url']

    if not validators.url(url):
        flash('A valid URL is required!', 'danger')
        return redirect(url_for('index'))

    try:
        new_link = Link(url = url)
        db.session.add(new_link)
        db.session.commit()
    except IntegrityError:
        flash('URL already registred', 'danger')
        return redirect(url_for('index'))

    q = Link.query.filter_by(url=url).first()
    sdata(q)
    flash('Link has been added', 'success')
    return redirect(url_for('index'))

@app.route('/edit/<id>', methods=['POST'])
@login_required
def edit(id):
    Category.query.filter_by(link_id=id).delete()
    Type.query.filter_by(link_id=id).delete()
    Tag.query.filter_by(link_id=id).delete()
    q = Link.query.filter_by(id=id).first()
    sdata(q)
    flash('Link has been modified', 'success')
    return redirect(url_for('index'))

@app.route('/like/<id>')
@login_required
def like(id):
    login = session.get('login')
    q = Like.query.filter_by(link_id=id, login=login).first()
    if q is None:
        new_like = Like(login=login, link_id=id)
        db.session.add(new_like)
        db.session.commit()
    elif login in q.login:
        Like.query.filter_by(link_id=id, login=login).delete()
        db.session.commit()
    res = {'nb': len(Link.query.filter_by(id=id).first().likes), 'users': [x[0] for x in Like.query.with_entities(Like.login).filter_by(link_id=id).all()]}
    return jsonify(res)

@app.route('/dislike/<id>')
@login_required
def dislike(id):
    login = session.get('login')
    q = Dislike.query.filter_by(link_id=id, login=login).first()
    if q is None:
        new_dislike = Dislike(login=login, link_id=id)
        db.session.add(new_dislike)
        db.session.commit()
    elif login in q.login:
        Dislike.query.filter_by(link_id=id, login=login).delete()
        db.session.commit()
    res = {'nb': len(Link.query.filter_by(id=id).first().dislikes), 'users': [x[0] for x in Dislike.query.with_entities(Dislike.login).filter_by(link_id=id).all()]}
    return jsonify(res)

@app.route('/archive/<id>')
@login_required
def archive(id):
    q = Link.query.filter_by(id=id).first()
    if q.archive:
        q.archive = False
        res = {'restore': True}
        #flash('Link has been restored', 'success')
    else:
        q.archive = True
        res = {'archive': True}
        #flash('Link has been archived', 'success')
    db.session.commit()
    return jsonify(res)

@app.route('/delete/<id>', methods=['POST'])
@login_required
def delete(id):
    Link.query.filter_by(id=id).delete()
    Category.query.filter_by(link_id=id).delete()
    Type.query.filter_by(link_id=id).delete()
    Tag.query.filter_by(link_id=id).delete()
    db.session.commit()
    flash('Link has been deleted', 'danger')
    return redirect(url_for('index'))
