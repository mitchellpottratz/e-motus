from flask import Blueprint, jsonify, request
from models.post import Post 


# creates blueprint for the posts resource
posts = Blueprint('posts', 'posts')


@posts.route('/')
def test():
	return 'works'


