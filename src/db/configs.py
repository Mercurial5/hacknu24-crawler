from __future__ import annotations

from dataclasses import dataclass
from os import environ


@dataclass
class PostgresConfigs:
    host: str
    port: int
    username: str
    password: str
    database: str

    @staticmethod
    def from_environ() -> PostgresConfigs:
        return PostgresConfigs(
            host=environ['POSTGRES_HOST'],
            port=int(environ['POSTGRES_PORT']),
            username=environ['POSTGRES_USERNAME'],
            password=environ['POSTGRES_PASSWORD'],
            database=environ['POSTGRES_DATABASE']
        )

    @property
    def connection_url(self) -> str:
        return f'postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
