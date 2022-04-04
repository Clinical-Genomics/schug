from sqlmodel import Session

from schug.database import engine


def get_session():
    yield Session(engine)
