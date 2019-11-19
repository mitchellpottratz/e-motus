from flask import Blueprint, jsonify, request

# creates a blueprint for the users resource
users = Blueprint('users', 'users')


@users.route('/login')
def login():
	return jsonify({'msg': 'works'})








