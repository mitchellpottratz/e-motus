from flask import Flask, g
from flask_login import LoginManager

import models.config
from models.user import User

DEGUB = True # app with log error messages
PORT = 8000 # app runs on port 8000

# instantiates the flask app
app = Flask(__name__)

# apps secret key
app.secret_key = 'kjfdksfjdslfjdslnljkgnaslfjdsjnjewvajiosdhfusuajfhewuofja'

# connects the app to the login_manager
login_manager = LoginManager()
login_manager.init_app(app)


# method for loading users, required by flask_login
@login_manager.user_loader
def load_user(user_id):
	try:
		return models.User.get(models.User.id == user_id)
	except models.DoesNotExist:
 		return None


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


# setup CORS for each resource 
# CORS(user, origins=['http://localhost:3000'], supports_credentials=True)


# index route - apps landing page
@app.route('/')
def index():
	return 'index page'


if __name__ == '__main__':
	# creates database tables
	models.config.initialize()

	# starts the server
	app.run(debug=DEGUB, port=PORT)

