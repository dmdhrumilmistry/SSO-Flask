from flask import Flask, request, jsonify
from database.utils import is_valid_email, generate_token, generate_web_token

import database.controller as db
import database.users as users_db


app = Flask(__name__)


@app.before_first_request
def init_app():
    try:
        db.create_table('Users')
    except Exception as e:
        if e.__class__.__name__ == 'ResourceInUseException':
            pass
        else:
            raise


@app.route('/')
def root_route():
    return jsonify({'repo': 'SSO-Flask', 'URL': 'https://github.com/dmdhrumilmistry/SSO-Flask'})


@app.route('/api/user/generate', methods=['POST'])
def add_user():
    response = {'msg': 'json data required'}
    code = 400

    if request.is_json:
        data = request.get_json()
        name = data.get('name', None)
        email = data.get('emailId', None)

        # verify email
        is_email_valid = is_valid_email(email)
        if not is_email_valid:
            response = {'msg': 'invalid email'}
            code = 400

        elif name and email and is_email_valid and not users_db.email_already_exists(email):
            token = generate_token()
            res = users_db.create_user(name, email, token)

            if res['ResponseMetadata']['HTTPStatusCode'] == 200:
                response = {
                    'msg': 'user created. Auth token will cannot be generated again. keep it secure!', 'token': token}
                code = 200
            else:
                response = {'msg': 'error'}
                code = 500

        else:
            response = {
                'msg': 'name and emailId parameters are required or user already exists'}
            code = 400

    return jsonify(response), code


@app.route('/api/user/getId', methods=['POST'])
def get_user_id():
    response = {'msg': 'json data required'}
    code = 400

    if request.is_json:
        data = request.get_json()
        auth_token = data.get('authToken', None)

        if auth_token:
            response = {'id': users_db.get_user_id_from_token(auth_token)}
            code = 200
        else:
            response = {'msg': 'authToken required'}
            code = 400

    return jsonify(response), code


@app.route('/api/user/details', methods=['POST'])
def get_all_info():
    response = {'msg': 'json data required'}
    code = 400

    if request.is_json:
        data = request.get_json()
        auth_token = data.get('authToken', None)
        user_id = data.get('id', None)

        is_valid_user = users_db.validate_user(auth_token, user_id)
        if not is_valid_user:
            response = {'msg': 'User not authorized'}
            code = 403

        elif auth_token and user_id and is_valid_user:
            response = users_db.get_user_details(user_id)
            code = 200
        else:
            response = {'msg': 'authToken and id are required'}
            code = 400

    return jsonify(response), code


@app.route('/api/user/token/generate', methods=['POST'])
def generate_website_token():
    response = {'msg': 'json data required'}
    code = 400

    if request.is_json:
        data = request.get_json()
        auth_token = data.get('authToken', None)
        user_id = data.get('id', None)
        domain = data.get('domain', None)

        is_valid_user = users_db.validate_user(auth_token, user_id)
        if not is_valid_user:
            response = {'msg': 'User not authorized'}
            code = 403

        elif auth_token and user_id and domain and is_valid_user:
            web_token = generate_web_token()
            response = users_db.add_web_token(user_id, domain, web_token)
            code = 200
        else:
            response = {'msg': 'authToken, id and domain are required'}
            code = 400

    return jsonify(response), code


@app.route('/api/user/token/release', methods=['POST'])
def delete_web_token():
    response = {'msg': 'json data required'}
    code = 400

    if request.is_json:
        data = request.get_json()
        auth_token = data.get('authToken', None)
        user_id = data.get('id', None)
        domain = data.get('domain', None)

        is_valid_user = users_db.validate_user(auth_token, user_id)
        if not is_valid_user:
            response = {'msg': 'User not authorized'}
            code = 403

        elif auth_token and user_id and domain and is_valid_user:
            response = {'releasedStatus': users_db.delete_web_token(user_id, domain)}
            code = 200

        else:
            response = {'msg': 'authToken, id and domain are required'}
            code = 400

    return jsonify(response), code


@app.route('/api/user/token/status', methods=['POST'])
def get_token_status():
    response = {'msg': 'json data required'}
    code = 400

    if request.is_json:
        data = request.get_json()
        auth_token = data.get('authToken', None)
        user_id = data.get('id', None)
        domain = data.get('domain', None)
        domain_auth_token = data.get('domainAuthToken', None)

        is_valid_user = users_db.validate_user(auth_token, user_id)
        if not is_valid_user:
            response = {'msg': 'User not authorized'}
            code = 403

        elif auth_token and user_id and domain and is_valid_user:
            response = {'tokenStatus': users_db.get_web_token_status(user_id, domain, domain_auth_token)}
            code = 200

        else:
            response = {'msg': 'authToken, id, domain, and domainToken are required'}
            code = 400

    return jsonify(response), code
