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
@comments.route('/<post_id>', methods=['GET'])
@login_required
def get_post_comment(post_id):
	try:
		# gets post by its id
		post = Post.get(Post.id == post_id, Post.soft_delete == False)
	
		# iterate through all of the posts comments and convert each post
		# to a dictionary
		comment_list = []
		for comment in post.comments:
			comment_list.append(model_to_dict(comment, backrefs=True, recurse=True))

		return jsonify(
			data=comment_list,
			status={'code': 200, 'message': 'successfully created comment.'}
		)

	# if the queried post doesnt exist
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Resource does not exist.'}
		)


# this route gets all of the comments create by the current
# user for a single post
@comments.route('/user/<post_id>', methods=['GET'])
@login_required
def get_users_comments_for_post(post_id):
	try:
		# gets post by its id
		post = Post.get(Post.id == post_id, Post.soft_delete == False)

		# gets all of the users comments for this post
		users_comments = Comment.select().where(Comment.post == post,
											    Comment.user == current_user.id)

		# convert all of the user comments to a dictionary
		users_comments_dict = [model_to_dict(comment) for comment in users_comments]

		return jsonify(
			data=users_comments_dict,
			status={'code': 200, 'message': 'Successfully got the users comments for this post.'}
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


# delete route - deletes a comment by its id
@comments.route('/<comment_id>', methods=['DELETE'])
@login_required
def delete_one_comment(comment_id):
	try:
		# deletes the comment
		Comment.delete().where(Comment.id == comment_id).execute()

		return jsonify(
			data={},
			status={'code': 200, 'message': 'successfully deleted comment.'}			
		)

	# if the queried comment doesnt exist
	except DoesNotExist:
		return jsonify(
			data={},
			status={'code': 404, 'message': 'Resource does not exist.'}
		)






