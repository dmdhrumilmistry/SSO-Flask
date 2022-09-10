import json
from flask import Flask, request, jsonify
import database.controller as db
import database.movies as movies_db

app = Flask(__name__)

@app.before_first_request
def init_app():
    try:
        db.create_table()
    except Exception as e:
        if e.__class__.__name__ == 'ResourceInUseException':
            pass
        else: raise


@app.route('/')
def root_route():
    return jsonify({'message':'Flask-SSO'})


@app.route('/movie', methods=['POST'])
def add_movie():
    movie = request.get_json()
    response = movies_db.write_to_movie(movie['title'], movie['director'])
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'message': 'ok',
        }
    return {
        'msg': 'error occurred',
        'response': response
    }


@app.route('/movie/<id>', methods=['GET'])
def get_movie(id):
    # sanitize id
    id = str(id)

    response = movies_db.read_from_movie(id)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        if ('Item' in response):
            return {'Item': response['Item']}
        return {'msg': 'Item not found!'}
    return {
        'msg': 'error occurred',
        'response': response
    }


@app.route('/movie/all', methods=['GET'])
def get_all_movies():
    return jsonify(movies_db.get_all_movies())


@app.route('/movie/<id>', methods=['DELETE'])
def delete_movie(id):
    response = movies_db.delete_from_movie(id)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Delete successful',
        }
    return {
        'msg': 'error occurred',
        'response': response
    }


@app.route('/movie/<id>', methods=['PUT'])
def update_movie(id):

    data = request.get_json()
    response = movies_db.update_in_movie(id, data)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'update successful',
            # 'response': response['ResponseMetadata'],
            # 'ModifiedAttributes': response['Attributes']
        }
    return {
        'msg': 'error occurred',
        'response': response
    }


@app.route('/movie/<id>/upvote', methods=['GET'])
def upvote_movie(id):
    response = movies_db.upvote_a_movie(id)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Upvote successful',
            # 'response': response['ResponseMetadata'],
            # 'Upvotes': response['Attributes']['upvotes']
        }
    return {
        'msg': 'error occurred',
        'response': response
    }


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
