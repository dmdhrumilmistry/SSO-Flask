from database.controller import resource
from uuid import uuid4

MovieTable = resource.Table('Movie')


def write_to_movie(title, director):
    # write
    response = MovieTable.put_item(
        Item={
            'id': str(uuid4()),
            'title': title,
            'director': director,
            'upvotes': 0
        }
    )
    return response


def read_from_movie(id):
    # read
    response = MovieTable.get_item(
        Key={
            'id': id
        },
        AttributesToGet=[
            'title', 'director'
        ]
    )
    return response


def update_in_movie(id, data: dict):
    # update
    response = MovieTable.update_item(
        Key={
            'id': id
        },
        AttributeUpdates={
            'title': {
                'Value': data['title'],
                'Action': 'PUT'
            },
            'director': {
                'Value': data['director'],
                'Action': 'PUT'
            }
        },

        ReturnValues="UPDATED_NEW"  # returns the new updated values
    )

    return response


def upvote_a_movie(id):
    # update
    response = MovieTable.update_item(
        Key={
            'id': id
        },
        AttributeUpdates={
            'upvotes': {
                'Value': 1,
                'Action': 'ADD'
            }
        },

        ReturnValues="UPDATED_NEW"
    )

    response['Attributes']['upvotes'] = int(response['Attributes']['upvotes'])

    return response


def delete_from_movie(id):
    # delete
    response = MovieTable.delete_item(
        Key={
            'id': id
        }
    )

    return response


def get_all_movies():
    response = MovieTable.scan(
        Limit=5,
        AttributesToGet=["title", "id"]
    )
    
    return response.get("Items", None)