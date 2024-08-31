import base64

from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from flask_login import current_user, login_user, logout_user, login_required, AnonymousUserMixin
from fastnanoid import generate

from app import app, db
from app.forms import  PasteForm
from app.models import User, Paste, File
from app.utils import generate_aesgcm, generate_encryption_key


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PasteForm()
    if form.data['submit']:
        paste = zip(form.data['filename'], form.data['value'])
        paste = save_paste(paste,
                                user=(not isinstance(current_user, AnonymousUserMixin) and current_user))
        return redirect(f"/{paste.get('url')}{paste.get('enc_key')}")
    return render_template('index.html', form=form)


@app.post('/api/save_paste')
def save_paste(pastes: list[dict], user: User | None):
    encryption_key = generate_encryption_key()
    base64_key = base64.urlsafe_b64encode(encryption_key).decode('utf-8')

    p = Paste(id=generate(size=9))

    for filename, value in pastes:
        file = File(filename=filename, paste_id=p.id)
        file.set_value(value, aesgcm=generate_aesgcm(encryption_key), nonce=p.id[6:]+base64_key[:10])
        db.session.add(file)

    if user:
        p.user_id = user.id

    db.session.add(p)
    db.session.commit()

    return {'url': p.id, 'enc_key': base64_key}


@app.get('/<string:paste>')
def get_paste(paste):
    paste_url = paste[:9]
    enc_key = paste[9:]
    nonce = paste_url[6:]+enc_key[:10]
    try:
        aesgcm = generate_aesgcm(base64.urlsafe_b64decode(enc_key))
    except ValueError:
        return render_template('404.html')
    query = sa.select(File).where(File.paste_id.like(paste_url))
    paste = db.session.scalars(query)
    return render_template('paste.html', paste=paste.all(), nonce=nonce, aesgcm=aesgcm)
