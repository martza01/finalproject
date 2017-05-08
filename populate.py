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


engine = create_engine('postgresql://martza01:@knuth.luther.edu/martza01')
Session = sessionmaker(bind=engine)

db = Session()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with open('data.json') as jsonData:
	d = json.load(jsonData)

actor_set = set()
title_list = []

for m in d:
	title_list.append(m['title'])
	for n in m['cast']:
		actor_set.add(n)

for a in actor_set:
	new_actor = Actor(name=a)
	db.add(new_actor)

for t in title_list:
	new_title = Film(title=t)
	db.add(new_title)

db.commit()