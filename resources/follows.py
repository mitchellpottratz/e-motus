from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user
from models.user import User
from models.follow import Follow
from peewee import DoesNotExist


# create blueprint for follows resource
follows = Blueprint('follows', 'follows')


# create route - allows a user to follow another user
@follows.route('/', methods=['POST'])
@login_required
def follow_user():
	try:
		# gets data from client - contains the user the current user wants to follow
		data = request.get_json()

		# gets the user the current user is going to follow
		user_to_follow = User.get(User.id == data['user_followed'], User.soft_delete == False)

		try:
			# checks if the current user is already following this user 
			is_following = Follow.get(Follow.followed_by == current_user.id,
									  Follow.followed == user_to_follow.id,
									  Follow.soft_delete == False)

			return jsonify(
				data={},
				status={'code': 401, 'message': 'User is already following this user'}
			)

		# exception thrown if the current_user is not already followng the user
		except DoesNotExist:

			# create follow model - current user now follows the user
			follow = Follow.create(followed_by=current_user.id, followed=user_to_follow.id)

			# convert follow to dictionary and remove both users password
			follow_dict = model_to_dict(follow)
			del follow_dict['followed_by']['password']
			del follow_dict['followed']['password'] 

			return jsonify(
				data=follow_dict,
				status={'code': 201, 'message': 'User is now following {}.'.format(follow_dict['followed']['email'])}
			)

	# exception thrown if the user_to_follow doesnt exist
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Failure getting resource.'}
		)




