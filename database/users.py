from database.controller import resource
from uuid import uuid4
from .utils import mask_email

users_table = resource.Table('Users')


def create_user(name: str, email_id: str, token: str):
    response = users_table.put_item(
        Item={
            'id': str(uuid4()),
            'name': name,
            'emailId': email_id,
            'authToken': token,
            'authTokens': dict()
        }
    )
    return response


def get_user_details(id):
    response = users_table.get_item(
        Key={
            'id': id
        },
        AttributesToGet=[
            'name',
            'emailId',
            'authTokens',
        ]
    )

    details = response.get('Item', dict())
    user_details = {
        'name' : details.get('name', None),
        'emailId': mask_email(details.get('emailId', '')),
        'domains': list(details.get('authTokens',dict()).keys())
    }
    return user_details


def add_web_token(id: str, domain: str, web_token: str) -> bool:
    res = users_table.update_item(
        Key={
            'id': id
        },
        UpdateExpression=f'SET authTokens.#domain = :token_val',
        ExpressionAttributeNames={
            "#domain": domain
        },
        ExpressionAttributeValues={
            ":token_val": web_token
        },
        ReturnValues="UPDATED_NEW",
    )
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {'domain': domain, 'token': web_token}

    return {'msg': 'token failed to be added'}


def delete_web_token(id: str, domain: str):
    response = users_table.update_item(
        Key={
            'id': id
        },
        UpdateExpression=f'REMOVE authTokens.#domain',
        ExpressionAttributeNames={
            "#domain": domain
        },
        ReturnValues="UPDATED_NEW"
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True

    return False


def email_already_exists(email: str):
    res = users_table.scan(FilterExpression="emailId = :email",
                           ExpressionAttributeValues={":email": email})
    return True if res['Count'] != 0 else False


def get_user_id_from_token(token: str):
    res = users_table.scan(
        FilterExpression="authToken = :token",
        ExpressionAttributeValues={":token": token}
    )

    return res['Items'][0].get('id', 'Not Found')


def validate_user(token: str, user_id: str):
    res = users_table.scan(
        FilterExpression="authToken = :token and id = :user_id",
        ExpressionAttributeValues={
            ":token": token,
            ":user_id": user_id,
        },
    )
    if res['ResponseMetadata']['HTTPStatusCode'] == 200 and res['Count'] == 1:
        return True

    return False
