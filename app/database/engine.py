import logging
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine, exc
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_config

config = get_config()

logger = logging.getLogger(__name__)


def get_database_uri() -> str:
    """Returns the database URL string."""
    return config.DATABASE_URL  # We get DATABASE_URL from our AppConfig instance


def create_engine_instance() -> Engine:
    """Creates and returns the database engine."""
    uri = get_database_uri()
    engine = create_engine(uri, pool_pre_ping=True)
    logger.info("Database engine created at %s", uri)
    return engine


engine = create_engine_instance()
SessionLocal = sessionmaker(bind=engine)


def get_db() -> Iterator[Session]:
    """Provides a session for database operations."""
    db = SessionLocal()
    logger.debug("Database session created at %s", config.DATABASE_URL)
    try:
        yield db
    except exc.SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database operation failed with error: {e}")
        raise e
    finally:
        db.close()


@contextmanager
def session_scope() -> Iterator[Session]:
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except exc.SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database operation failed with error: {e}")
        raise e
    finally:
        session.close()
