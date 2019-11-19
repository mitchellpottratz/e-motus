from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from models.user import User
from peewee import DoesNotExist

# creates a blueprint for the users resource
users = Blueprint('users', 'users')

# registration route
@users.route('/register')
def register():
	# gets the clients registration data
	data = request.get_json()

	# convert email to lowercase
	data['email'].lower()

	try:
		# queries a user by the provided email
		User.get(User.email == data['email'])

		# queries a user by the provided username
		User.get(User.username == data['username'])

		# returns error if the email or username exists
		return jsonify(
			data={},
			status={'code': 401, 'message': 'A user with that email or username already exists'}
		)

	# the following code runs if the emal and username doesnt exist
	except DoesNotExist:
		# encrypts the password
		data['password'] = generate_password_hash(data['password'])

		# creates the user
		user = User.create(**data)

		# logs in the user
		login_user(user)

		# convert user to dictionary and remove password
		user_dict = model_to_dict(user)
		del user_dict['password']

		return jsonify(
			data=user_dict,
			status={'code': 201, 'message': 'Successfully registered {}'.format(user_dict['username'])}
		)


# login route
@users.route('/login')
def login():
	return jsonify({'msg': 'works'})








