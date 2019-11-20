import datetime
from peewee import *
from .user import User


# database the Like models data will go into
DATABASE = SqliteDatabase('emotus.sqlite')

# this model is responsible for allowing users to follow eachother
class Follow(Model):

	# the user who followed the other user
	followed_by = ForeignKeyField(User, backref='following')

	# the user the other user is following
	followed = ForeignKeyField(User, backref='followers')

	soft_delete = BooleanField(default=False)
	timestamp = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE


	# removes the password from the followed_by and 
	# followed user
	@staticmethod
	def remove_passwords(follow_dict):
		del follow_dict['followed_by']['password']
		del follow_dict['followed']['password']









