import datetime
from peewee import *
from .user import User
from .post import Post


# database the Like models data will go into
DATABASE = SqliteDatabase('emotus.sqlite')


# model for posting comments on a post
class Comment(Model):

	# user who created the comment
	user = ForeignKeyField(User, backref='comments')

	# post the comment is for
	post = ForeignKeyField(Post, backref='comments')

	# the text of the comment
	content = CharField(max_length=350, null=False)

	

	soft_delete = BooleanField(default=False)
	timestamp = DateTimeField(default=datetime.datetime.now())

	class Meta:
		database = DATABASE




