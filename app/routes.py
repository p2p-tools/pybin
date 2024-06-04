from uuid import uuid4

from flask import render_template, flash, redirect, url_for
import sqlalchemy as sa

from app import app, db
from app.forms import LoginForm, PasteForm

# @todo: registration, login
from app.models import User, Paste


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PasteForm()
    if form.validate_on_submit():
        paste_uuid = save_paste(paste=form.paste.data)
        return redirect(f'/{paste_uuid}')
    return render_template('index.html', form=form)


@app.post('/api/save_paste')
def save_paste(paste: str, user: str = None):
    paste_uuid = uuid4()
    p = Paste(id=paste_uuid, value=f"""{paste}""", author=user)
    print(paste, '\n==============/n',p.value)
    db.session.add(p)
    db.session.commit()

    return f'{paste_uuid}'


@app.get('/<uuid:paste_url>')
def get_paste(paste_url):
    query = sa.select(Paste).where(Paste.id.like(paste_url))
    paste = db.session.scalar(query)
    return render_template('paste.html', paste=paste)


@app.route('/login', methods=['GET', 'POST'])
def login():
    u = User(username='susan')
    db.session.add(u)
    db.session.commit()

    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', form=form)
