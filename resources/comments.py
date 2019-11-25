from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user
from models.user import User
from models.post import Post
from models.comment import Comment
from peewee import DoesNotExist

# blueprint for comments resource 
comments = Blueprint('comments', 'comments')


# index route - gets all of the comments for a post
@comments.route('/', methods=['GET'])
@login_required
def get_post_comment():

	# gets json data from client
	data = request.get_json()

	try:
		# gets post by its id
		post = Post.get(Post.id == data['post_id'], Post.soft_delete == False)
	
		# iterate through all of the posts comments and convert each post
		# to a dictionary
		comment_list = []
		for comment in post.comments:
			comment_list.append(model_to_dict(comment))

		return jsonify(
			data=comment_list,
			status={'code': 201, 'message': 'successfully created comment.'}
		)

	# if the queried post doesnt exist
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Resource does not exist.'}
		)


# create route - creates a new comment
@comments.route('/', methods=['POST'])
@login_required
def create_comment():

	# gets json data from client
	data = request.get_json()

	try:
		# gets post by its id
		post = Post.get(Post.id == data['post_id'], Post.soft_delete == False)

		# creates a new comments
		comment = Comment.create(**data, user=current_user.id, post=post)

		# converts model to dictionary
		comment_dict = model_to_dict(comment)

		return jsonify(
			data=comment_dict,
			status={'code': 201, 'message': 'successfully created comment.'}
		)

	# if the queried post doesnt exist
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Resource does not exist.'}
		)






