from sqlmodel import Session

from schug.database import engine


def get_session():
    return Session(engine)
