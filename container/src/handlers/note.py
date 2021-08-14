import datetime
import hashlib
import logging
import random

from app import db
from models.note import Note
from my_secrets import salt

logger = logging.getLogger('oonote.handlers.note')
_id_alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
_id_length = 16


def create_note(text, password):
    note = Note(id_=_generate_unique_id(), text=text,
        created_at=datetime.datetime.utcnow(), password=password)
    db.session.add(note)
    db.session.commit()
    return note


def get_note(id_):
    return Note.query.filter_by(id_=id_).first()


def mark_read(note):
    note.read_at = datetime.datetime.utcnow()
    note.text = None
    db.session.commit()


def add_response(note, response):
    note.response = response
    db.session.commit()


def hash_password(password):
    f = hashlib.new('sha256')
    f.update((password + salt).encode('utf-8'))
    return f.hexdigest()


def _generate_unique_id():
    while True:
        id_ = ''.join(random.sample(_id_alphabet, _id_length, counts=[_id_length] * len(_id_alphabet)))
        note = Note.query.filter_by(id_=id_).first()
        if note is not None:
            logger.debug(f'Generated id "{id_}" already exist')
        else:
            logger.debug(f'Generated id "{id_}" is unique')
            return id_
