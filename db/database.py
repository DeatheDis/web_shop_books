from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from db.models import Base
from contextlib import contextmanager
from config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = scoped_session(session_factory=sessionmaker(autocommit=False, bind=engine, expire_on_commit=False))


def init_db():
    Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
