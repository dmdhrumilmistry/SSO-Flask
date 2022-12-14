from boto3 import resource
from dotenv import load_dotenv
from os import getenv

# load aws config
load_dotenv()
AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = getenv('AWS_REGION_NAME')


resource = resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)


def create_table(table_name:str='Users'):
    table = resource.create_table(
        TableName=table_name,  # Name of the table
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # RANGE = sort key, HASH = partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',  # Name of the attribute
                'AttributeType': 'S'   # N = Number (B= Binary, S = String)
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    table.wait_until_exists()
    return table
