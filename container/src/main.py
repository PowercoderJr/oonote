import logging

from app import app


# noinspection PyUnresolvedReferences
def init():
    logging.getLogger('oonote').setLevel(logging.DEBUG)
    import views


def main():
    app.run()


init()
if __name__ == '__main__':
    main()
