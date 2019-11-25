from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user
from models.user import User
from models.follow import Follow
from peewee import DoesNotExist


# create blueprint for follows resource
follows = Blueprint('follows', 'follows')


# shows all of the current users followers
@follows.route('/followers', methods=['GET'])
@login_required
def get_all_followers():

	# gets all of the users followers
	followers = Follow.select().where(Follow.followed == current_user.id)

	# iterate over all of the users followers to 
	# convert each follower instance to a dictionary
	# and remove the users passwords
	followers_list = []	
	for follower in followers:
		follow_dict = model_to_dict(follower, backrefs=True, recurse=True)
		Follow.remove_passwords(follow_dict)
		followers_list.append(follow_dict)


	return jsonify(
		data=followers_list,
		status={'code': 200, 'message': 'Successfully got all the followers'}
	)


# gets all of the users the current user is following
@follows.route('/following', methods=['GET'])
@login_required
def get_all_following():

	# gets all the users the current user is followng
	following = Follow.select().where(Follow.followed_by == current_user.id)

	# iterate all of the users following the current user, convert
	# each following instance to a dictionary and remove the users
	# password
	following_list = []	
	for follow in following:
		following_dict = model_to_dict(follow.followed)
		del following_dict['password']
		following_list.append(following_dict)

	return jsonify(
		data=following_list,
		status={'code': 200, 'message': 'Successfully got all of the users the current user is following'}
	)

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
									  Follow.followed == user_to_follow)

		# exception thrown if the current_user is not already followng the user
		except DoesNotExist:

			# create follow model - current user now follows the user
			follow = Follow.create(followed_by=current_user.id, followed=user_to_follow)

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


# delete route
@follows.route('/<user_id>', methods=['DELETE'])
@login_required
def unfollow_user(user_id):
	try:
		# gets the user the current user is going to unfollow
		followed_user = User.get(User.id == user_id)

		# deletes the follow instance (unfollow the user)
		Follow.delete().where(Follow.followed == followed_user,
							  Follow.followed_by == current_user.id).execute()

		return jsonify(
			data={},
			status={'code': 200, 'message': 'Successfully unfollowed user.'}
		)

	# exception thrown if the model exists
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Failure getting resource.'}		
		)





