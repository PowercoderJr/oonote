from app import db


class Note(db.Model):
    id_ = db.Column(db.String(16), primary_key=True)
    text = db.Column(db.Text)
    response = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)
    password = db.Column(db.String(64))
