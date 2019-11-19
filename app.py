from flask import Flask, g
import models.config

DEGUB = True # app with log error messages
PORT = 8000 # app runs on port 8000

# instantiates the flask app
app = Flask(__name__)


# called before every request
@app.before_request 
def before_request():
	g.db = models.DATABASE 
	g.db.connect() # connects tot he database


# called after every request
@app.after_request
def after_request(response):
	g.db.close() # closes database connection
	return response # returns response to client


# index route - apps landing page
@app.route('/')
def index():
	return 'index page'


if __name__ == '__main__':
	# creates database tables
	models.config.initialize()

	# starts the server
	app.run(debug=DEGUB, port=PORT)

