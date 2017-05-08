from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Film(Base):
	__tablename__ = 'films'

	id = Column(Integer, primary_key=True)
	title = Column(String)


class Actor(Base):
	__tablename__ = 'actors'
	id = Column(Integer, primary_key=True)
	name = Column(String)