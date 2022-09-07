from boto3 import client, resource
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from os import getenv

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)


# load env vars
load_dotenv()
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = getenv("REGION_NAME")
print(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME)

aws_client = client(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)

dynamodb = resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


def create_tables(tables: list[dict]):
    fails = 0
    for table in tables:
        try:
            table_name = table.get('TableName', None)
            key_schema = table.get('KeySchema', None)
            attribute_defs = table.get('AttributeDefinitions', None)
            if not (table_name and key_schema and attribute_defs):
                logger.warning(
                    f'Not creating table because Table Name| Key Schema| Attr definition is/are missing for {table}')
                continue

            dynamodb.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attribute_defs,
                BillingMode='PAY_PER_REQUEST',
            )
            table.wait_until_exists()
            logger.info(f'{table_name} Table created successfully')
        except ClientError as err:
            logger.error(
                "Couldn't create table %s. Here's why: %s: %s", table_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            fails += 1

        return fails
