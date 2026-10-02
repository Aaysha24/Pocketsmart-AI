from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


# SQLite database
DATABASE_URL = "sqlite:///./pocket_smartai.db"


# Database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


# Base class for database models
Base = declarative_base()