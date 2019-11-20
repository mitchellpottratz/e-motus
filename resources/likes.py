from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user
from models.user import User
from models.post import Post 
from models.like import Like
from peewee import DoesNotExist


# creates a blueprint for the users resource
likes = Blueprint('likes', 'likes')


# gets all of the likes for a post
@likes.route('/<post_id>', methods=['GET'])
def get_posts_likes():
	pass


# create route - creates a new like for a post
@likes.route('/', methods=['POST'])
@login_required
def create_like():
	try:
		# gets data from the client - this data only contains a post id
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
			status={'code': 404, 'message': 'Failure to get resource'}
		)


# delete route - deletes a like by changing soft_delete field to true
@likes.route('/', methods=['GET'])
@login_required
def delete_like():
	try:
		# gets data from the client - this data only contains a like id
		data = request.get_json()

		# tries to get the like by its id
		like = Post.get(Like.id == data['like'], Like.soft_delete == False)

		# set soft_delete to true to delete the like
		like.soft_delete = True 
		like.save()

		# convert to dictionary and remove users passwords
		like_dict = model_to_dict(like)
		del like_dict['user']['password']
		del like_dict['post']['user']['password']

		return jsonify({})

	# exception thrown if the like doesnt exist
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Failure to get resource'}
		)











