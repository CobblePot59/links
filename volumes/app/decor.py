from functools import wraps
from flask import redirect, url_for, session

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if session.get('status') == True:
            return test(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap
