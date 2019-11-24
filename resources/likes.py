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
@login_required
def get_posts_likes():
	try:
		# get data from client - contains a post id
		data = request.get_json()

		# tries to get post by its id
		post = Post.get(Post.id == data['post'], Post.soft_delete == False)

		# iterate through all of the posts likes, convert each like
		# to a dictionary, remove the users password, and append to the list
		likes_list = []
		for like in post.likes:
			like_dict = model_to_dict(like)
			Like.remove_passwords(like_dict)
			likes_list.append(like_dict)

		return jsonify(
			data=likes_list,
			status={'code': 200, 'message': 'Succesfully got likes.'}
		)

	# exception thrown if the post doesnt exist
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Failure to get resource.'}
		)


# returns a list of all the posts the user has liked
@likes.route('/user', methods=['GET'])
def get_users_liked_posts():
	
	# gets all of the currents users likes
	likes = Like.select().where(Like.user == current_user.id)

	# iterate through all the likes, get the post from the like, convert each like
	# to a dictionary, remove the users password
	users_liked_posts = []
	for like in likes:
		post_dict = model_to_dict(like.post)
		print('liked post:', post_dict)
		del post_dict['user']['password']
		users_liked_posts.append(post_dict)	

	return jsonify(
		data=users_liked_posts,
		status={'code': 200, 'message': 'Successfully got users likes.'}
	)


# create route - creates a new like for a post
@likes.route('/', methods=['POST'])
@login_required
def create_like():
	try:
		# gets data from the client - contains a post id
		data = request.get_json()

		# tries to get the post by its id
		post_id = Post.get(Post.id == data['postId'])
	
		try:
			# checks if a like for that post and user already exists
			like = Like.get(Like.post == post_id, Like.user == current_user.id)

		# if the user has not already likes the post
		except DoesNotExist:

			# creates a new like for the post
			like = Like.create(post=post_id, user=current_user.id)

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
		like = Like.get(Like.id == like_id)

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
@likes.route('/<post_id>', methods=['DELETE'])
@login_required
def delete_like(post_id):
	try:

		# gets the post the like is related to
		post = Post.get(Post.id == post_id)

		# gets the like instance by the post and current user
		Like.delete().where(Like.post == post, Like.user == current_user.id).execute()

		return jsonify(
			data={},
			status={'code': 200, 'message': 'Successfully unliked post.'}
		)

	# exception thrown if the like doesnt exist
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Failure to get resource.'}
		)











