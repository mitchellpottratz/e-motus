import datetime
from peewee import *
from .user import User
from .post import Post
from .config import DATABASE

# database the Like models data will go into
# DATABASE = SqliteDatabase('emotus.sqlite')


# this model is used for liking posts
class Like(Model):

	# post that is liked
	post = ForeignKeyField(Post, backref='likes')

	# user that liked th post
	user = ForeignKeyField(User, backref='likes')
	
	soft_delete = BooleanField(default=False)
	timestamp = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

	# removes the passwords for both of the users
	# in a like dictionary
	@staticmethod
	def remove_passwords(like_dict):
		del like_dict['user']['password']
		del like_dict['post']['user']['password']






