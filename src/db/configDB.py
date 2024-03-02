from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ
from dotenv import load_dotenv

load_dotenv()

sqlite_url = f"sqlite:///{environ.get('DATABASE_PATH', 'sqlite.db')}"

engine = create_engine(
    sqlite_url, echo=False
)  # Para que aparezcan los comandos ejecutados internamente por sql en la terminal, poner en true el echo

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
