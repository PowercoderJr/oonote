from app import db


# noinspection PyUnresolvedReferences
def main():
    from models.note import Note
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    main()
