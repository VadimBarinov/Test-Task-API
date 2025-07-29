from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from db_config import DATABASE


engine = create_engine(
    f"postgresql+psycopg2://{DATABASE['USER']}:{DATABASE['PASSWORD']}@{DATABASE['HOST']}/{DATABASE['NAME']}"
)


Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    db = Session()
    try:
        yield db
    finally:
        db.close()