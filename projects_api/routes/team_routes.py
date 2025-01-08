from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from projects_api import mongo

team_blueprint = Blueprint('team_routes', __name__)


@team_blueprint.route('/members', methods=['POST'])
def create_member():
    data = request.json
    required_fields = ['username', 'email']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    existing_user = mongo.db.users.find_one({'$or': [{'username': data['username']}, {'email': data['email']}]})
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    new_user = {
        'username': data['username'],
        'email': data['email'],
        'project_id': None
    }
    result = mongo.db.users.insert_one(new_user)
    return jsonify({'message': 'User created successfully', 'id': str(result.inserted_id)}), 201


@team_blueprint.route('/members', methods=['GET'])
def get_all_members():
    users = mongo.db.users.find()
    result = [{'id': str(user['_id']), 'username': user['username']} for user in users]
    return jsonify(result), 200


@team_blueprint.route('/members/<user_id>', methods=['GET'])
def get_member(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    result = {
        'id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
        'project_id': str(user['project_id']) if user['project_id'] else None
    }
    return jsonify(result), 200


@team_blueprint.route('/members/<user_id>', methods=['DELETE'])
def delete_member(user_id):
    result = mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'message': 'User deleted successfully'}), 200


@team_blueprint.route('/projects/<project_id>/members/<user_id>', methods=['POST'])
def assign_member_to_project(project_id, user_id):
    project = mongo.db.projects.find_one({'_id': ObjectId(project_id)})
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    mongo.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'project_id': ObjectId(project_id)}}
    )
    return jsonify({'message': 'User assigned to project successfully'}), 200


@team_blueprint.route('/projects/<project_id>/members', methods=['GET'])
def get_project_members(project_id):
    users = mongo.db.users.find({'project_id': ObjectId(project_id)})
    result = [{'id': str(user['_id']), 'username': user['username']} for user in users]
    return jsonify(result), 200


@team_blueprint.route('/projects/<project_id>/members/<user_id>', methods=['DELETE'])
def remove_member_from_project(project_id, user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id), 'project_id': ObjectId(project_id)})
    if not user:
        return jsonify({'error': 'User not found in this project'}), 404

    mongo.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'project_id': None}}
    )
    return jsonify({'message': 'User removed from project successfully'}), 200
