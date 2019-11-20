from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from models.user import User
from models.post import Post 
from models.like import Like
from peewee import DoesNotExist

# creates a blueprint for the users resource
likes = Blueprint('likes', 'likes')