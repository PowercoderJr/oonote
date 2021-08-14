from flask import request, render_template, redirect, url_for, session

from app import app
from handlers.note import create_note, hash_password


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and len(text := request.form['text'].strip()) > 0:
        password = request.form['password']
        password = hash_password(password) if len(password) > 0 else None
        note = create_note(text[:500], password)
        session['password'] = note.password
        return redirect(url_for('.details', note_id=note.id_))
    return render_template('index.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def handler_404(e):
    return render_template('error/404.html'), 404
