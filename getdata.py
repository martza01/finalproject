from imdb import IMDb
import json

f = open("data.json", 'w')

db = IMDb()
r = db.get_top250_movies()

for i in r:
	title = str(i)
	movie = db.get_movie(i.movieID)
	cast = movie['cast']
	castList = []
	for a in cast:
		castList.append(str(a))

	f.write(json.dumps({title: castList}) + '\n')
	print json.dumps({title: castList}) + '\n'
