from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from projects_api import mongo

task_blueprint = Blueprint('task_routes', __name__)

@task_blueprint.route('/projects/<project_id>/tasks', methods=['POST'])
def create_task(project_id):
    data = request.json
    required_fields = ['name', 'description', 'priority', 'estimated_completion_date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    task = {
        'name': data['name'],
        'description': data['description'],
        'priority': data['priority'],
        'estimated_completion_date': data['estimated_completion_date'],
        'project_id': ObjectId(project_id)
    }
    result = mongo.db.tasks.insert_one(task)
    return jsonify({'message': 'Task added successfully', 'id': str(result.inserted_id)}), 201


@task_blueprint.route('/projects/<project_id>/tasks', methods=['GET'])
def get_all_tasks(project_id):
    tasks = mongo.db.tasks.find({'project_id': ObjectId(project_id)})
    result = [
        {
            'id': str(task['_id']),
            'name': task['name'],
            'description': task['description'],
            'priority': task['priority'],
            'estimated_completion_date': task['estimated_completion_date']
        }
        for task in tasks
    ]
    return jsonify(result), 200


@task_blueprint.route('/projects/<project_id>/tasks/<task_id>', methods=['GET'])
def get_task(project_id, task_id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id), 'project_id': ObjectId(project_id)})
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    task_details = {
        'id': str(task['_id']),
        'name': task['name'],
        'description': task['description'],
        'priority': task['priority'],
        'estimated_completion_date': task['estimated_completion_date']
    }
    return jsonify(task_details), 200


@task_blueprint.route('/projects/<project_id>/tasks/<task_id>', methods=['PUT'])
def update_task(project_id, task_id):
    data = request.json
    update_fields = {key: value for key, value in data.items() if key in ['name', 'description', 'priority', 'estimated_completion_date']}
    
    if not update_fields:
        return jsonify({'error': 'No valid fields to update'}), 400

    result = mongo.db.tasks.update_one({'_id': ObjectId(task_id), 'project_id': ObjectId(project_id)}, {'$set': update_fields})
    if result.matched_count == 0:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({'message': 'Task updated successfully'}), 200


@task_blueprint.route('/projects/<project_id>/tasks/<task_id>', methods=['DELETE'])
def delete_task(project_id, task_id):
    result = mongo.db.tasks.delete_one({'_id': ObjectId(task_id), 'project_id': ObjectId(project_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({'message': 'Task deleted successfully'}), 200
