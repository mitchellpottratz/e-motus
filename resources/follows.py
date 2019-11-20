from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user
from models.user import User
from peewee import DoesNotExist


# create blueprint for follows resource
follows = Blueprint('follows', 'follows')


print('works')

