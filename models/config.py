from peewee import *
from .user import User
from .post import Post
from .like import Like
from .follow import Follow
from .comment import Comment

# database being used for this app
DATABASE = SqliteDatabase('emotus.sqlite')


# this method is called when the server starts
def initialize():
	DATABASE.connection() # establish database connection
	DATABASE.create_tables([User, Post, Like, Follow, Comment], safe=True) # creates the database tables
	print('tables created')
	DATABASE.close() # closes the database connection


