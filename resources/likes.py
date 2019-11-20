from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user
from models.user import User
from models.post import Post 
from models.like import Like
from peewee import DoesNotExist


# creates a blueprint for the users resource
likes = Blueprint('likes', 'likes')


# index route - gets all of the likes for a post
@likes.route('/', methods=['GET'])
def get_post_likes():
	try:
		# get data from client - contains a post id
		data = request.get_json()

		# tries to get post by its id
		post = Post.get(Post.id == data['post'], Post.soft_delete == False)

		print(post.likes)

	# exception thrown if the post doesnt exist
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Failure to get resource.'}
		)


# create route - creates a new like for a post
@likes.route('/', methods=['POST'])
@login_required
def create_like():
	try:
		# gets data from the client - contains a post id
		data = request.get_json()

		# tries to get the post by its id
		post = Post.get(Post.id == data['post'], Post.soft_delete == False)
	
		try:
			# checks if a like for that post and user already exists
			Like.get(Like.post == post.id, Like.user == current_user.id, Like.soft_delete == False)

			return jsonify(
				data={},
				status={'code': 401, 'message': 'User has already liked this post'}
			)

		# if the user has not already likes the post
		except DoesNotExist:

			# creates a new like for the post
			like = Like.create(post=post.id, user=current_user.id)

			# convert like to dictionary and remove both users password
			like_dict = model_to_dict(like)
			del like_dict['user']['password']
			del like_dict['post']['user']['password']

			return jsonify(
				data=like_dict,
				status={'code': 201, 'message': 'User successfully liked post.'}
			)

	# exception thrown if the post doesnt exist
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Failure to get resource.'}
		)


# show route - shows a single like
@likes.route('/<like_id>', methods=['GET'])
@login_required
def show_like(like_id):
	try:
		# tries to get the like by its id
		like = Like.get(Like.id == like_id, Like.soft_delete == False)

		# convert to dictionary and remove users passwords
		like_dict = model_to_dict(like)
		del like_dict['user']['password']
		del like_dict['post']['user']['password']

		return jsonify(
			data=like_dict,
			status={'code': 200, 'message': 'Successfully got like.'}
		)

	# exception thrown if the like doesnt exist
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Failure to get resource.'}
		)	


# delete route - allows user to remove a like from a post
@likes.route('/<like_id>', methods=['DELETE'])
@login_required
def delete_like(like_id):
	try:
		# tries to get the like by its id
		like = Like.get(Like.id == like_id, Like.soft_delete == False)

		# if the user is the user of the like
		if like.user.id == current_user.id:

			# set soft_delete to true to delete the like
			like.soft_delete = True 
			like.save()

			# convert to dictionary and remove users passwords
			like_dict = model_to_dict(like)
			del like_dict['user']['password']
			del like_dict['post']['user']['password']

			return jsonify(
				data=like_dict,
				status={'code': 200, 'message': 'Successfully unliked post.'}
			)

		# if the user is not the user of the like
		else:
			return jsonify(
				data={},
				status={'code', 401, 'message', 'User does not have access to this resource.'}
			)

	# exception thrown if the like doesnt exist
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Failure to get resource.'}
		)











