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
	followers = Follow.select().where(Follow.followed == current_user.id,
						   			  Follow.soft_delete == False)

	print(followers)

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
	following = Follow.select().where(Follow.followed_by == current_user.id,
						   			  Follow.soft_delete == False)

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
									  Follow.followed == user_to_follow.id)

			# if the user has previously followed this user before
			if is_following.soft_delete == True:

				# set soft_delete to false and save
				is_following.soft_delete = False
				is_following.save()

				# convert to dictionary and remove the users password
				follow_dict = model_to_dict(is_following)
				Follow.remove_passwords(follow_dict)

				return jsonify(
					data=follow_dict,
					status={'code': 201, 'message': 'User is now following {}.'.format(follow_dict['followed']['email'])}
				)
				
			# if the user is currently already following this user
			else:
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


# delete route
@follows.route('/<user_id>', methods=['DELETE'])
@login_required
def unfollow_user(user_id):
	try:
		# gets the follow by its id
		follow = Follow.get(Follow.followed == user_id,
							Follow.followed_by == current_user.id,
					        Follow.soft_delete == False)

		# deletes the follow with soft delete and saves it
		follow.soft_delete = True
		follow.save()

		# converts to dictionary and removes users passwords
		follow_dict = model_to_dict(follow)
		Follow.remove_passwords(follow_dict)

		return jsonify(
			data=follow_dict,
			status={'code': 200, 'message': 'Successfully unfollowed {}.'.format(follow_dict['followed']['email'])}
		)

	# exception thrown if the model exists
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Failure getting resource.'}		
		)





