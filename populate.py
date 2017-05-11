import json
from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

film_actor = Table('film_actor', 
					Base.metadata,
					Column('film', Integer, ForeignKey('films.id')),
					Column('actor', Integer, ForeignKey('actors.id')))

class Film(Base):
	#SQLAlchemy object to represent a film

	__tablename__ = 'films'

	id = Column(Integer, primary_key=True)
	title = Column(String)
	related = relationship("Actor", secondary = film_actor, back_populates ="satisfied_by")

	def __repr__(self):
		return "Film({}, {})".format(self.id, self.title)


class Actor(Base):
	#SQLAlchemy object to represent an actor

	__tablename__ = 'actors'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	satisfied_by = relationship("Film", secondary = film_actor, back_populates ="related")


	def __repr__(self):
		return "Actor({}, {})".format(self.id, self.name)

# use whoever's database
engine = create_engine('postgres://pnrgtpqlgcszoe:dc26564d4fc0023c38def80aa0d76a18881adde8e00eff3d24aa5b20a0be10c2@ec2-54-163-254-76.compute-1.amazonaws.com:5432/d67pd9eo07qkke')
Session = sessionmaker(bind=engine)

db = Session()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with open('data.json') as jsonData:
	d = json.load(jsonData)

actor_set = set()
title_dict = {}

for m in d:
	for c in m['cast']:
		actor_set.add(c)

for a in actor_set:
	new_actor = Actor(name=a)
	db.add(new_actor)
	title_dict[a] = new_actor

for m in d:
	new_title = Film(title=m['title'], related=[title_dict[g] for g in m['cast']])
	db.add(new_title)

db.commit()