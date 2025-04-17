from sqlalchemy import create_engine #connecting the database
from sqlalchemy.orm import sessionmaker #talking to DB (query)
from sqlalchemy.ext.declarative import declarative_base #base class used to define database (tables)

#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/NoteApplicationDatabase"
SQLALCHEMY_DATABASE_URL = "sqlite:///./notesapp.db"

#engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()