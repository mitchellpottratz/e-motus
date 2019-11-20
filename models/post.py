import datetime
from peewee import *
from .user import User

# database the User models data will go into
DATABASE = SqliteDatabase('emotus.sqlite')


# this is the model for posts
class Post(Model):
	# user that created the post
	user = ForeignKeyField(User, backref='posts')

	# text content of the post
	content = CharField(max_length=300, null=False)

	# text emotion
	emotion = CharField(max_length=50, null=False)

	# holds the 'emoji code'
	emoji = CharField(max_length=50, null=False)

	soft_delete = BooleanField(default=False)
	timestamp = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

