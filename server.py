from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import psycopg2
import os
import urllib.parse


app = Flask(__name__)
Bootstrap(app)

conn = psycopg2.connect(dbname='martza01', user='martza01', host='knuth.luther.edu')
cur = conn.cursor()


@app.route("/")
def index():
	cur.execute('''
				select title from films;
				''')
	f = cur.fetchall()
	results = []
	for i in f:
		results.append(str(i).strip("('").strip(",'')"))
	return render_template("index.html", movielist=results)


@app.route("/film/<title>")
def filmPage(title):
	cur.execute('''
				select films.title, actors.name
				from films join film_actor on films.id = film_actor.film
				join actors on actors.id = film_actor.actor
				where title like %s;
				''', (title,))
	f = cur.fetchall()
	cast = []
	for i in f:
		# print(i)
		cast.append(i[1])
	return render_template("movie.html", title=title, cast=cast)

@app.route("/actor/<name>")
def actorPage(name):
	cur.execute('''
				select actors.name, films.title
				from films join film_actor on films.id = film_actor.film
				join actors on actors.id = film_actor.actor
				where name like %s;
				''', (name,))
	f = cur.fetchall()
	films = []
	for i in f:
		# print(i)
		films.append(i[1])
	return render_template("actor.html", name=name, films=films)


if __name__ == '__main__':
	app.run(debug=True)