from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_simpleldap import LDAP
from datetime import timedelta
import validators


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/links.db'
app.config['SECRET_KEY'] = '0Og1OIeIIl5oj0pl96oy26Oc0O113l024bh9qI9cq47e291t78qsI9wmoIn9I057'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=15)

app.config['LDAP_SCHEMA'] = 'ldaps'
app.config['LDAP_HOST'] = ''
app.config['LDAP_PORT'] = '636'
app.config['LDAP_USE_SSL'] = True
app.config['LDAP_BASE_DN'] = 'OU=Domain Users,DC=cobblepot59,DC=int'
app.config['LDAP_USERNAME'] = ''
app.config['LDAP_PASSWORD'] = ''

db = SQLAlchemy(app)
ldap = LDAP(app)
from models import *


@app.route('/', methods=('GET', 'POST'))
def index():
    if session.get('status'):
        links = Link.query.all()
        return render_template('index.html', links=links)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('status'):
        return redirect(url_for('index'))
    else:
        if request.method == 'GET':
            return render_template('login.html')
        else:
            login = request.form['login']+'@cobblepot59.int' # CHANGE ME
            password = request.form['password']
            q = ldap.bind_user(login, password)
            if password and q == True:
                session['status'] = True
                session['login'] = login.split('@')[0]
                return redirect(url_for('index'))
            else:
                return 'Bad Login'

@app.route('/logout', methods=['GET'])
def logout():
    if session.get('status'):
        session['status'] = False
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add():
    if session.get('status'):
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
            
        str_tags = request.form['tags']
        q = Link.query.filter_by(url=url).first()
        for name in str_tags.split(','):
            new_tag = Tag(name = name.strip().lower(), link_id = q.id)
            db.session.add(new_tag)
            db.session.commit()
        flash('Link has been added', 'success')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/like/<id>')
def like(id):
    if session.get('status'):
        login = session.get('login')
        q = Like.query.filter_by(link_id=id, login=login).first()
        if q is None:
            new_like = Like(login=login, link_id=id)
            db.session.add(new_like)
            db.session.commit()
            return redirect(url_for('index'))
        elif login in q.login:
            Like.query.filter_by(link_id=id, login=login).delete()
            db.session.commit()
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/dislike/<id>')
def dislike(id):
    if session.get('status'):
        login = session.get('login')
        q = Dislike.query.filter_by(link_id=id, login=login).first()
        if q is None:
            new_dislike = Dislike(login=login, link_id=id)
            db.session.add(new_dislike)
            db.session.commit()
            return redirect(url_for('index'))
        elif login in q.login:
            Dislike.query.filter_by(link_id=id, login=login).delete()
            db.session.commit()
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/archive/<id>')
def archive(id):
    if session.get('status'):
        q = Link.query.filter_by(id=id).first()
        q.archive = True
        db.session.commit()
        flash('Link has been archived', 'danger')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/restore/<id>')
def restore(id):
    if session.get('status'):
        q = Link.query.filter_by(id=id).first()
        q.archive = False
        db.session.commit()
        flash('Link has been restored', 'success')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
