from json import load
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

film_actor = Table('film_actor', 
					Base.metadata,
					Column('film', String, ForeignKey('film.id')),
					Column('actor', String, ForeignKey('actor.id')))

class Film(Base):
	#SQLAlchemy object to represent a film

	__tablename__ = 'films'

	id = Column(Integer, primary_key=True)
	title = Column(String)
	related = relationship("Actor",
							secondary = film_actor,
							back_populates ="satisfied_by")

	def __repr__(self):
		return "Film({}, {})".format(self.id, self.title)


class Actor(Base):
	#SQLAlchemy object to represent an actor

	__tablename__ = 'actors'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	satisfied_by = relationship("Film",
								secondary = film_actor,
								back_populates ="related")


	def __repr__(self):
		return "Actor({}, {})".format(self.id, self.name)


engine = create_engine('postgresql://nelser05:knuth.luther.edu/finalorm')
Session = sessionmaker(bind=engine)

db = Session()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
