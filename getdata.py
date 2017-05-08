from imdb import IMDb
import json

f = open("data.json", 'w')
f.write('[\n')

db = IMDb()
r = db.get_top250_movies()

for i in r:
	title = str(i)
	movie = db.get_movie(i.movieID)
	cast = movie['cast']
	castList = []
	for a in cast:
		castList.append(str(a))

	f.write(json.dumps({"title": title, "cast": castList}) + ',\n')
	print json.dumps({title: castList}) + '\n'

f.write(']')