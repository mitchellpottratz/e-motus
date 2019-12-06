# module imports 
import os
from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager

# model import 
import models.config
from models.user import User
from peewee import DoesNotExist

# resource imports 
from resources.users import users
from resources.posts import posts
from resources.likes import likes
from resources.follows import follows
from resources.comments import comments

if 'ORIGIN' in os.environ:
	origin = os.environ['ORIGIN']
else:
	origin = 'http://localhost:3000'

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
		return User.get(User.id == user_id)
	except DoesNotExist:
 		return None

# called before every request
@app.before_request 
def before_request():
	g.db = models.config.DATABASE 
	g.db.connect() # connects tot he database

# called after every request
@app.after_request
def after_request(response):
	g.db.close() # closes database connection
	return response # returns response to client

# setup CORS for each resource here
CORS(users, origins=[origin], supports_credentials=True)
CORS(posts, origins=[origin], supports_credentials=True)
CORS(likes, origins=[origin], supports_credentials=True)
CORS(follows, origins=[origin], supports_credentials=True)
CORS(comments, origins=[origin], supports_credentials=True)

# setup blueprints here
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(posts, url_prefix='/api/v1/posts')
app.register_blueprint(likes, url_prefix='/api/v1/likes')
app.register_blueprint(follows, url_prefix='/api/v1/follows')
app.register_blueprint(comments, url_prefix='/api/v1/comments')


# ADD THESE THREE LINES -- because in production the app will be run with 
# gunicorn instead of by the three lines below, so we want to initialize the
# tables in that case as well
if 'ON_HEROKU' in os.environ: 
  print('\non heroku!')
  models.config.initialize()


if __name__ == '__main__':
	# creates database tables
	models.config.initialize()

	# starts the server
	app.run(debug=DEGUB, port=PORT)

