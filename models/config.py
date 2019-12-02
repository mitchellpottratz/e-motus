from playhouse.db_url import connect
import os
from peewee import *


if 'ON_HEROKU' in os.environ: # later we will manually add this env var 
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this 
                                                     # env var for you 
                                                     # when you provision the
                                                     # Heroku Postgres Add-on
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
	print('tables created')
	DATABASE.close() # closes the database connection


