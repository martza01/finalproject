from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import psycopg2

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def index():
	return render_template("index.html")


if __name__ == '__main__':
	app.run(debug=True)