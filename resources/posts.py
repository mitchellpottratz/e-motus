from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required
from peewee import DoesNotExist
from operator import itemgetter 
from models.post import Post 
from models.follow import Follow
from models.like import Like


# creates blueprint for the posts resource
posts = Blueprint('posts', 'posts')


# index route - gets all of the current users post
@posts.route('/', methods=['GET'])
@login_required
def get_users_posts():

	# gets all of the current users posts
	posts = Post.select().where(Post.user == current_user.id,
								Post.soft_delete == False).order_by(Post.timestamp.desc())

	# iterate through all the post to convert each one
	# to a dictionary and remove the users password
	posts_list = []
	for post in posts:
		post_dict = model_to_dict(post, backrefs=True, recurse=True)
		del post_dict['user']['password']
		posts_list.append(post_dict)

	return jsonify(
		data=posts_list,
		status={'code': 200, 'message': 'Successfully got all of the users posts.'}
	)


# this route returns all of the post form the users that 
# the current user follows
@posts.route('/feed', methods=['GET'])
@login_required
def get_feed_posts():

	# gets all of the follow instance where the user matches the followed_by field
	users_followers = Follow.select().where(Follow.followed_by == current_user.id)
		
	# iterate over all of the users that follow the current user and get all
	# of their posts
	users_feed = []
	for user in users_followers:
		posts = Post.select().where(Post.user == user.followed, Post.soft_delete == False)

		# converts each post to a dictionary, removes the password and adds it to
		# users_feed list 
		for post in posts:
			post_dict = model_to_dict(post, backrefs=True, recurse=True)
			del post_dict['user']['password']
			users_feed.append(post_dict)

	# sorts all of the post in the users feed by most recent
	users_feed_sorted = sorted(users_feed, key=itemgetter('timestamp'), reverse=True)

	return jsonify(
		data=users_feed_sorted,
		status={'code': 200, 'message': 'Successfully got the users feed'}
	)

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
		status={'code': 201, 'message': 'Successfully created post.'}
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




