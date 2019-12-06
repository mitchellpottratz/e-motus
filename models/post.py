import datetime
import os
from peewee import *
from .user import User
from playhouse.db_url import connect

# database the Post model data will go into
if 'ON_HEROKU' in os.environ: 
  DATABASE = connect(os.environ.get('DATABASE_URL')) 
else:
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

