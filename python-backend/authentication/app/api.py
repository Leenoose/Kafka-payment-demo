from fastapi import APIRouter
from .model.user import User
import sys
import psycopg2
from psycopg2 import Error
import jwt

router = APIRouter()

@router.onevent("startup")
async def startup():
    pass

@router.onevent("shutdown")
async def shutdown():
    pass


@router.get("/users")
async def get_users() -> dict:
    return {"data": User}


@router.post("/init_db")
async def init_db():
    create_table_query = f"""
                        create table if not exists users (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            password VARCHAR(255) NOT NULL,
                            jwt VARCHAR(255)
                        );
                        """
    try:
        connection = psycopg2.connect(
            user="postgres", password="mypassword", host="localhost", port="5432", database="users")
        cursor = connection.cursor()
        connection.autocommit = True
        cursor.execute(create_table_query)

    except (Exception, Error) as error:
        print(error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Conn closed successfully")


@router.post("/create_user")
async def create_user(user: User):
    username = user.name
    password = user.password
    try:
        connection = psycopg2.connect(
            user="postgres", password="mypassword", host="localhost", port="5432", database="users")
        cursor = connection.cursor()
        query = f"insert into users (name, password) values ('{username}', crypt('{password}', gen_salt('md5')))"

        cursor.execute(query)
        connection.commit()

    except (Exception, Error) as error:
        print(error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Conn closed successfully")


@router.post("/generate_jwt")
async def generate_jwt():
    # generate JWT and update database
    # https://stackoverflow.com/questions/72975593/where-to-store-tokens-secrets-with-fastapi-python
    # https://testdriven.io/blog/fastapi-jwt-auth/
    return
