from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy.orm import sessionmaker, Session

from db.configs import PostgresConfigs


class PostgresDB:

    def __init__(self, configs: PostgresConfigs):
        engine = create_engine(configs.connection_url, pool_pre_ping=True)
        self._session = sessionmaker(bind=engine, expire_on_commit=False)

        self._current_session: Session | None = None

    @contextmanager
    def session_scope(self) -> Session:
        if self._current_session:
            yield self._current_session
            return

        session = self._session()
        self._current_session = session
        try:
            session.begin()
            yield session
            session.commit()
        except IntegrityError as e:
            print(f"IntegrityError with DB - {e}")
            session.rollback()
            raise
        except StatementError as e:
            print(f'StatementError with DB - {e}')
            session.rollback()
            raise
        finally:
            session.expunge_all()
            session.close()
            self._current_session = None
