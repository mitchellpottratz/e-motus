# module imports 
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

DEGUB = True # app with log error messages
PORT = 8000 # app runs on port 8000

# instantiates the flask app
app = Flask(__name__)

# folder images will upload into
app.config['UPLOAD_FOLDER'] = './static/images/'

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
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
CORS(posts, origins=['http://localhost:3000'], supports_credentials=True)
CORS(likes, origins=['http://localhost:3000'], supports_credentials=True)
CORS(follows, origins=['http://localhost:3000'], supports_credentials=True)

# setup blueprints here
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(posts, url_prefix='/api/v1/posts')
app.register_blueprint(likes, url_prefix='/api/v1/likes')
app.register_blueprint(follows, url_prefix='/api/v1/follows')


if __name__ == '__main__':
	# creates database tables
	models.config.initialize()

	# starts the server
	app.run(debug=DEGUB, port=PORT)

