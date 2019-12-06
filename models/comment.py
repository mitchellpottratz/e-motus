import datetime
import os
from peewee import *
from .user import User
from .post import Post
from playhouse.db_url import connect


# database the Like models data will go into
if 'ON_HEROKU' in os.environ: 
  DATABASE = connect(os.environ.get('DATABASE_URL')) 
else:
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




