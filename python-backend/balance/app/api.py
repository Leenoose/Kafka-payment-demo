from fastapi import APIRouter
from app.model.balance import Balance
import sys
import psycopg2
from psycopg2 import Error
import jwt

router = APIRouter()


@router.get("/balance")
async def get_balances() -> dict:
    return {"data": Balance}


@router.post("/init_db")
async def init_db():
    create_table_query = f"""
                        create table if not exists balances (
                            user_id INTEGER PRIMARY KEY,
                            balance DECIMAL(10,2) NOT NULL
                        );
                        """
    try:
        connection = psycopg2.connect(
            user="postgres", password="mypassword", host="localhost", port="5432", database="balances")
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


@router.post("/get_user_balance")
async def get_user_balance(user_id):

    try:
        connection = psycopg2.connect(
            user="postgres", password="mypassword", host="localhost", port="5432", database="balances")
        cursor = connection.cursor()
        query = f"select * from balances where user_id = '{user_id}';"
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    except (Exception, Error) as error:
        print(error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Conn closed successfully")


@router.post("/create_new_user_balance")
async def create_new_user_balance(user_id):

    try:
        connection = psycopg2.connect(
            user="postgres", password="mypassword", host="localhost", port="5432", database="balances")
        cursor = connection.cursor()
        query = f"insert into balances (user_id, balance) values ('{user_id}', '0')"

        cursor.execute(query)
        connection.commit()

    except (Exception, Error) as error:
        print(error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Conn closed successfully")


@router.post("/update_user_balance")
async def update_user_balance(balance: Balance):
    try:
        connection = psycopg2.connect(
            user="postgres", password="mypassword", host="localhost", port="5432", database="balances")
        cursor = connection.cursor()
        query = f"select * from balances where balance_id = '{balance_id}';"
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    except (Exception, Error) as error:
        print(error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Conn closed successfully")


@router.post("/update_user_balance")
async def update_user_balance(balance: Balance):

    try:
        connection = psycopg2.connect(
            user="postgres", password="mypassword", host="localhost", port="5432", database="balances")
        cursor = connection.cursor()
        query = f"update balances set balance = {balance.balance} where user_id='{balance.user_id}')"

        cursor.execute(query)
        connection.commit()

    except (Exception, Error) as error:
        print(error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Conn closed successfully")
