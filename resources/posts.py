from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required
from peewee import DoesNotExist
from models.post import Post 


# creates blueprint for the posts resource
posts = Blueprint('posts', 'posts')


# create route
@posts.route('/', methods=['POST'])
@login_required
def create_post():
	# gets post data from client
	data = request.get_json()

	# creates the post
	post = Post.create(**data, user=current_user.id)

	# convert to dictionary and remove users password
	post_dict = model_to_dict(post)
	del post_dict['user']['password']

	return jsonify(
		data=post_dict,
		status={'code': 200, 'message': 'Successfully created post'}
	)


# show route
@posts.route('/<id>', methods=['GET'])
@login_required
def get_one_post(id):
	try:
		# queries post by id
		post = Post.get(Post.id == id, Post.soft_delete == False)

		# convert to dictionary and remove user password
		post_dict = model_to_dict(post)
		del post_dict['user']['password']

		return jsonify(
			data=post_dict,
			status={'code': 200, 'message': 'Successfully got resource.'}
		)

	# if the resource doesnt exists
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Failure to get resource'}
		)


# update route
@posts.route('/<id>', methods=['PUT'])
@login_required
def update_one_post(id):
	try:
		# gets post data from client
		data = request.get_json()

		# queries post by id
		post = Post.get(Post.id == id, Post.soft_delete == False)

		# if the current user is the user of the post
		if current_user.id == post.user.id:

			# updates any of the fields of the post if they are provided in 
			# the data dictionary and saves the post
			post.content = data['content'] if 'content' in data else None
			post.emotion = data['emotion'] if 'emotion' in data else None
			post.emoji = data['emoji'] if 'emoji' in data else None
			post.save()

			# convert to dictionary and remove user password
			post_dict = model_to_dict(post)
			del post_dict['user']['password']

			return jsonify(
				data=post_dict,
				status={'code': 200, 'message': 'Successfully updated post.'}
			)

		# if the current user is not the user of the post
		else:
			return jsonify(
				data={},
				status={'code': 401, 'message': 'You do not have access to this post.'}
			)

	# if he post does not exist
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Failure to get resource'}
		)


# delete route
@posts.route('/<id>', methods=['DELETE'])
@login_required
def delete_one_post(id):
	try:
		# gets post data from client
		data = request.get_json()

		# queries post by id
		post = Post.get(Post.id == id, Post.soft_delete == False)

		# if the current user is the user of the post
		if current_user.id == post.user.id:
			# set soft_delete to true and save the post
			post.soft_delete = True 
			post.save()

			# convert to dictionary and remove user password
			post_dict = model_to_dict(post)
			del post_dict['user']['password']

			return jsonify(
				data=post_dict,
				status={'code': 200, 'message': 'Successfully deleted post.'}
			)

		# if the current user is not the user of the post
		else:
			return jsonify(
				data={},
				status={'code': 401, 'message': 'User does not have access to this resource.'}
			)

	# if he post does not exist
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Failure to get resource'}
		)




