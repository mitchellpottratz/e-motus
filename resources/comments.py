from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user
from models.user import User
from models.comment import Comment
from peewee import DoesNotExist

# blueprint for comments resource 
comments = Blueprint('comments', 'comments')


@comments.route('/test', methods=['GET'])
def test():
	return 'comments work'








