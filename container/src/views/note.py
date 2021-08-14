import copy
import datetime

from flask import request, render_template, abort, flash, session

from app import app
from handlers.note import get_note, mark_read, add_response, hash_password


@app.route('/<note_id>', methods=['GET', 'POST'])
def display(note_id):
    note = get_note(note_id)
    note_copy = copy.copy(note)
    if request.method == 'GET':
        if note is None:
            return render_template('note/no_such_note.html')
        elif note.password is not None:
            return render_template('note/password_page.html', note=note)
        elif note.read_at is None:
            return render_template('note/confirmation_page.html', note=note)
        else:
            return render_template('note/note.html', note=note)
    elif request.method == 'POST':
        request_type = request.form['type']
        if request_type == 'password':
            if hash_password(request.form['password']) == note.password:
                mark_read(note)
                return render_template('note/note.html', note=note_copy)
            else:
                flash('Неверный пароль')
                return render_template('note/password_page.html', note=note)
        elif request_type == 'confirmation':
            mark_read(note)
            return render_template('note/note.html', note=note_copy)
        elif request_type == 'response':
            if len(response := request.form['response'].strip()) > 0:
                add_response(note, response[:100])
            return render_template('note/note.html', note=note)
        else:
            abort(500)
    else:
        abort(405)


@app.route('/<note_id>/details', methods=['GET', 'POST'])
def details(note_id):
    note = get_note(note_id)
    if request.method == 'GET':
        if note is None:
            return render_template('note/no_such_note.html')
        else:
            session_password = None
            if 'password' in session:
                session_password = session.pop('password')
            if note.password is not None and session_password != note.password:
                return render_template('note/password_page.html', note=note)
            else:
                return render_template('note/details.html', note=note,
                    tz_offset=datetime.timedelta(hours=3), tz_name='МСК')
    elif request.method == 'POST':
        if hash_password(request.form['password']) == note.password:
            return render_template('note/details.html', note=note,
                tz_offset=datetime.timedelta(hours=3), tz_name='МСК')
        else:
            flash('Неверный пароль')
            return render_template('note/password_page.html', note=note)
    else:
        abort(405)

