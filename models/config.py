from playhouse.db_url import connect
import os
from peewee import *

if 'ON_HEROKU' in os.environ: 
  DATABASE = connect(os.environ.get('DATABASE_URL')) 
else:
  DATABASE = SqliteDatabase('emotus.sqlite')

# models from other files
from .user import User
from .post import Post
from .like import Like
from .follow import Follow
from .comment import Comment


# this method is called when the server starts
def initialize():
	DATABASE.connection() # establish database connection
	DATABASE.create_tables([User, Post, Like, Follow, Comment], safe=True) # creates the database tables
	DATABASE.close() # closes the database connection


