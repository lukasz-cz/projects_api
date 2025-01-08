from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from projects_api import mongo

project_blueprint = Blueprint('project_routes', __name__)

# Projects

@project_blueprint.route('/projects', methods=['POST'])
def create_project():
    data = request.json
    required_fields = ['name', 'description', 'start_date', 'end_date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    project = {
        'name': data['name'],
        'description': data['description'],
        'start_date': data['start_date'],
        'end_date': data['end_date']
    }
    result = mongo.db.projects.insert_one(project)
    return jsonify({'id': str(result.inserted_id)}), 201


@project_blueprint.route('/projects', methods=['GET'])
def get_all_projects():
    projects = mongo.db.projects.find()
    result = [
        {'id': str(project['_id']), 'name': project['name'], 'description': project['description']} 
        for project in projects
    ]
    return jsonify(result), 200


@project_blueprint.route('/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    project = mongo.db.projects.find_one({'_id': ObjectId(project_id)})
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    project_details = {
        'id': str(project['_id']),
        'name': project['name'],
        'description': project['description'],
        'start_date': project['start_date'],
        'end_date': project['end_date']
    }
    return jsonify(project_details), 200


@project_blueprint.route('/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.json
    update_fields = {key: value for key, value in data.items() if key in ['name', 'description', 'start_date', 'end_date']}
    
    if not update_fields:
        return jsonify({'error': 'No valid fields to update'}), 400

    result = mongo.db.projects.update_one({'_id': ObjectId(project_id)}, {'$set': update_fields})
    if result.matched_count == 0:
        return jsonify({'error': 'Project not found'}), 404
    
    return jsonify({'message': 'Project updated successfully'}), 200


@project_blueprint.route('/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    result = mongo.db.projects.delete_one({'_id': ObjectId(project_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Project not found'}), 404
    
    return jsonify({'message': 'Project deleted successfully'}), 200
