from sqlalchemy import create_engine, MetaData
from databases import Database
from models import users, notes  # Importe as tabelas do arquivo models

DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
metadata.create_all(engine, tables=[users, notes])  # Chame create_all com as tabelas
