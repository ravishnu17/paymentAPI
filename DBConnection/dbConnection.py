from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Configurations.config import secret

sql_url = f"postgresql://{secret.dbuser}:{secret.dbpassword}@{secret.host}:{secret.port}/{secret.dbname}"
engine = create_engine(sql_url)
session_local = sessionmaker(autocommit=False , autoflush=False , bind = engine)

Base  =declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()