import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv(override=True)


@dataclass(frozen=True)
class Config:

    postgres_user: str = field(default=os.getenv("POSTGRES_USER", ""))
    postgres_password: str = field(default=os.getenv("POSTGRES_PASSWORD", ""))
    postgres_db: str = field(default=os.getenv("POSTGRES_DB", ""))
    postgres_host: str = field(default=os.getenv("POSTGRES_HOST", "localhost"))
    postgres_port: str = field(default=os.getenv("POSTGRES_PORT", "5432"))
    app_host: str = field(default=os.getenv("APP_HOST", "127.0.0.1"))
    app_port: int = field(default=int(os.getenv("APP_PORT", "8080")))
    app_debug: bool = field(default=bool(os.getenv("APP_DEBUG", "0")))

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )
