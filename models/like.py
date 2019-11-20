import datetime
from peewee import *
from .user import User
from .post import Post

# database the Like models data will go into
DATABASE = SqliteDatabase('emotus.sqlite')


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






