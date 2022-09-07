from fastapi import FastAPI
from database.dynamodb_handler import create_tables
from routes.user import routes_user

app = FastAPI()

app.include_router(routes_user, '/user')

