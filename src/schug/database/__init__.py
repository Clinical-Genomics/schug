from sqlmodel import create_engine, SQLModel

from schug.config import settings

engine = create_engine(settings.db_uri, echo=True)

SQLModel.metadata.create_all(engine)
