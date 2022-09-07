from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from database.dynamodb_handler import dynamodb
from boto3.dynamodb.conditions import Key

import logging


# configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)

# table schemas
tables = [
    {
        "TableName": "users",
        "KeySchema": [
            {
                "AttributeName": "id",
                "KeyType": "Hash"
            }
        ],
        "AttributeDefinition": [
            {
                "AttributeName": "id",
                "AttributeType": "N"
            },
            {
                "AttributeName": "name",
                "AttributeType": "S"
            },
            {
                "AttributeName": "username",
                "AttributeType": "S"
            },
            {
                "AttributeName": "email",
                "AttributeType": "S"
            },
            {
                "AttributeName": "passwdHash",
                "AttributeType": "S"
            }
        ],
    }
]

table = dynamodb.Table("users")


def create_user(user: dict):
    try:
        table.put_item(Item=user)
        return user
    except ClientError as err:
        return JSONResponse(content=err.response["Error"], status_code=500)


def get_user(id: dict):
    try:
        resp = table.query(
            KeyConditionExpression=Key("id").eq(id)
        )
        return resp["Items"]
    except ClientError as err:
        return JSONResponse(content=err.response["Error"], status_code=500)


def get_users():
    try:
        resp = table.scan(
            Limit=5,
            AttributesToGet=["username", "id"]
        )
        return resp["Items"]

    except ClientError as err:
        return JSONResponse(content=err.response["Error"], status_code=500)


def delete_user(user: dict):
    try:
        resp = table.delete_item(
            Key={
                "id": user["id"]
            }
        )
        return resp
    except ClientError as err:
        return JSONResponse(content=err.response["Error"], status_code=500)


def update_user(user: dict):
    try:
        resp = table.update_item(
            Key={
                "id": user["id"]
            },
            UpdateExpression="SET username = :username, age = :age",
            ExpressionAttributeValues={
                ":username": user["username"],
                ":passwdHash":user["passwdHash"]
            }
        )
        return resp
        
    except ClientError as err:
        return JSONResponse(content=err.response["Error"], status_code=500)
