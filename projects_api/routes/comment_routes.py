from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from projects_api import mongo

comment_blueprint = Blueprint('comment_routes', __name__)

@comment_blueprint.route('/projects/<project_id>/tasks/<task_id>/comments', methods=['POST'])
def add_comment(project_id, task_id):
    data = request.json
    required_fields = ['user_id', 'content']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id), 'project_id': ObjectId(project_id)})
    if not task:
        return jsonify({'error': 'Task not found in the project'}), 404

    comment = {
        'user_id': ObjectId(data['user_id']),
        'task_id': ObjectId(task_id),
        'project_id': ObjectId(project_id),
        'content': data['content']
    }
    result = mongo.db.comments.insert_one(comment)
    return jsonify({'message': 'Comment added successfully', 'id': str(result.inserted_id)}), 201


@comment_blueprint.route('/projects/<project_id>/tasks/<task_id>/comments', methods=['GET'])
def get_comments(project_id, task_id):
    comments = mongo.db.comments.find({'task_id': ObjectId(task_id), 'project_id': ObjectId(project_id)})
    result = []
    for comment in comments:
        user = mongo.db.users.find_one({'_id': comment['user_id']})
        result.append({
            'id': str(comment['_id']),
            'user_id': str(comment['user_id']),
            'username': user['username'] if user else 'Unknown',
            'content': comment['content']
        })
    return jsonify(result), 200


@comment_blueprint.route('/projects/<project_id>/tasks/<task_id>/comments/<comment_id>', methods=['DELETE'])
def delete_comment(project_id, task_id, comment_id):
    result = mongo.db.comments.delete_one({
        '_id': ObjectId(comment_id),
        'task_id': ObjectId(task_id),
        'project_id': ObjectId(project_id)
    })
    if result.deleted_count == 0:
        return jsonify({'error': 'Comment not found'}), 404
    
    return jsonify({'message': 'Comment deleted successfully'}), 200
