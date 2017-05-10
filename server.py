from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import TextField, SubmitField
import psycopg2
import json
import os
import urllib.parse


app = Flask(__name__)
app.secret_key = 's3cr3t'
Bootstrap(app)

conn = psycopg2.connect(dbname='martza01', user='martza01', host='knuth.luther.edu')
cur = conn.cursor()

class SearchForm(Form):
	name = TextField("search by actor")
	title = TextField("search by title")
	submit1 = SubmitField("Go")
	submit2 = SubmitField("Go")


@app.route("/")
def index():
	form = SearchForm()

	cur.execute('''
				select title from films;
				''')
	f = cur.fetchall()
	results = []
	for i in f:
		results.append(str(i).strip("('").strip(",'')"))
	return render_template("index.html", movielist=results, form=form)


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

@app.route("/searchTitle")
def titleSearch():
	args = request.url.split('?')[1]
	print(args)
	t = args.split('=')[1].split('&')[0]
	t = t.replace('+', ' ')
	s = '%'+t+'%'
	print(t)
	print(s)

	cur.execute('''				
				select films.title
				from films
				where title like %s;
				''', (s,))
	f = cur.fetchall()
	r = []
	for i in f:
		r.append(str(i).strip("('").strip("',)"))
	print(r)
	return render_template("results.html", s=t, movielist=r) 

@app.route("/testscript")
def testScript():
	return render_template("testscript.html")	

@app.route("/searchActor")
def actorSearch():
	args = request.url.split('?')[1]
	# print(args)
	t = args.split('=')[1].split('&')[0]
	s = [j for j in t.split('%2C+')]
	sII = [i.replace('+', ' ') for i in s]

	print(sII)

	filteredResults = []
	totalResults = []
	l = []
	if len(sII) > 1:
		cur.execute('''
				select films.title, actors.name
				from films join film_actor on films.id = film_actor.film
				join actors on actors.id = film_actor.actor
				where actors.name = ANY(%s);
				''', (sII,))
		f = cur.fetchall()
		for x in f:
			y = dict()
			y['title'] = x[0]
			if y not in l:
				y['name'] = [x[1]]
				l.append(y)
			else:
				i = next((c for c in l if c['title'] == y['title']))
				i['name'].append(x[1])
		
		for j in l:
			actors = [j['name']]
			for k in l:
				if j != k:
					if j['title'] == k['title']:
						actors.append(k['name'])
						toAdd = (j['title'], j['name'])
						filteredResults.append(j)

		for c in filteredResults:
			num = c['name']
			title = c['title']
			v = (title, num)
			if v not in totalResults:
				totalResults.append(v)
	else:
		cur.execute('''
					select films.title, actors.name
					from films join film_actor on films.id = film_actor.film
					join actors on actors.id = film_actor.actor
					where actors.name = ANY(%s);
					''', (sII,))
		f = cur.fetchall()
		for x in f:
			if x not in totalResults:
				totalResults.append(x)

	title_list = [] 
	searchStr = ""
	for j in sII:
		searchStr = searchStr + j + ', '

	for x in totalResults:
		if x[0] not in title_list:
			title_list.append(x[0])
		print(x[0])

	return render_template("results.html", movielist=title_list, s=searchStr)

@app.route("/api/getinfo")
def getInfo():
	args = request.url.split('?')[1]
	print(args)
	t, n = args.split('&')
	titleKeywords = t.split('=')[1]
	nameKeywords = n.split('=')[1]

	title_list = titleKeywords.split(',')
	name_list = nameKeywords.split(',')

	print(title_list)
	print(name_list)

	cur.execute('''
				select films.title, actors.name
				from films join film_actor on films.id = film_actor.film
				join actors on actors.id = film_actor.actor
				where title = ANY(%s);
				''', (title_list,))

	f = cur.fetchall()

	cur.execute('''
				select films.title, actors.name
				from films join film_actor on films.id = film_actor.film
				join actors on actors.id = film_actor.actor
				where name = ANY(%s);
				''', (name_list,))

	g = cur.fetchall()

	print(f)
	print(g)

	return json.dumps([f, g])

if __name__ == '__main__':
	app.run(debug=True)