from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user, login_required
from flask_bcrypt import generate_password_hash, check_password_hash
from models.user import User
from peewee import DoesNotExist

# creates a blueprint for the users resource
users = Blueprint('users', 'users')

# registration route
@users.route('/register', methods=['POST'])
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
			status={'code': 201, 'message': 'Successfully registered {}.'.format(user_dict['email'])}
		)


# login route
@users.route('/login', methods=['POST'])
def login():
	# gets the clients data
	data = request.get_json()

	try:
		# query user by email
		user = User.get(User.email == data['email'])
		
		# if the password is correct
		if check_password_hash(user.password, data['password']):
			# login the user
			login_user(user)

			# convert to dicitonary and remove password
			user_dict = model_to_dict(user)
			del user_dict['password']

			return jsonify(
				data=user_dict,
				status={'code': 200, 'message': 'Successfully logged in {}.'.format(user_dict['email'])}
			)

		# if the password is incorrect
		else:
			return jsonify(
				data={},
				status={'code': 401, 'message': 'Email or password is incorrect.'}
			)

	# if email doesnt exist	
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 401, 'message': 'Email or password is incorrect.'}
		)


# logout route
@users.route('/logout', methods=['GET'])
@login_required
def logout():
	# logs out the user
	logout_user()

	return jsonify(
		data={},
		status={'code': 200, 'message': 'Successfully logged out.'}
	)


# route for searching for other users
@users.route('/find', methods=['POST'])
@login_required
def find_users():
	# gets data from the client 
	data = request.get_json()

	# query the user by the search string
	results = User.select().where(
		(User.username.contains(data['value']))
		)

	# iterate through all of the results and convert the
	# results to a dictionary and remove the password
	results_list = []
	for result in results:
		result_dict = model_to_dict(result)
		del result_dict['password']
		results_list.append(result_dict)

	return jsonify(
		data=results_list,
		status={'code': 200, 'message': 'Successfully got the search results'}
	) 












