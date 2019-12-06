import datetime
from peewee import *
from flask_login import UserMixin
from .config import DATABASE

# database the User models data will go into
# DATABASE = SqliteDatabase('emotus.sqlite')

# user model - clients account
class User(Model, UserMixin):
	image = CharField(null=True)
	first_name = CharField(max_length=75)
	last_name = CharField(max_length=75)
	username = CharField(max_length=75, unique=True)
	email = CharField(max_length=75, unique=True)
	password = CharField(max_length=255)
	soft_delete = BooleanField(default=False)
	timestamp = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

	# returns the users full name
	def get_full_name(self):
		return self.first_name + ' ' + self.last_name









