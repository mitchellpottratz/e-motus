# module import 
from flask import Flask, g


DEGUB = True # app with log error messages
PORT = 8000 # app runs on port 8000


# instantiates the flask app
app = Flask(__name__)


# index route - apps landing page
@app.route('/')
def index():
	return 'index page'


if __name__ == '__main__':
	# starts the server
	app.run(debug=DEGUB, port=PORT)

