from fastapi import APIRouter
from .model.transaction import Transaction
import sys
import psycopg2
from psycopg2 import Error
import jwt

router = APIRouter()


@router.get("/transactions")
async def get_transactions() -> dict:
    return {"data": Transaction}


@router.post("/init_db")
async def init_db():
    create_table_query = f"""
                        create table if not exists transactions (
                            transaction_id SERIAL PRIMARY KEY,
                            sender_id INTEGER NOT NULL,
                            recipient_id INTEGER NOT NULL,
                            amount NUMERIC(7,5) NOT NULL
                        );
                        """
    try:
        connection = psycopg2.connect(
            user="postgres", password="mypassword", host="localhost", port="5432", database="transactions")
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


@router.post("/create_transaction")
async def create_transaction(transaction: Transaction):

    try:
        connection = psycopg2.connect(
            user="postgres", password="mypassword", host="localhost", port="5432", database="transactions")
        cursor = connection.cursor()
        query = f"insert into transactions (sender_id, recipient_id, amount) values ('{transaction.sender_id}', '{transaction.recipient_id}', '{transaction.amount}')"

        cursor.execute(query)
        connection.commit()

    except (Exception, Error) as error:
        print(error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Conn closed successfully")


@router.post("/get_transaction_by_id")
async def get_transaction(transaction_id):

    try:
        connection = psycopg2.connect(
            user="postgres", password="mypassword", host="localhost", port="5432", database="transactions")
        cursor = connection.cursor()
        query = f"select * from transactions where transaction_id = '{transaction_id}';"
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


@router.post("/get_outgoing_transactions")
async def get_outgoing_transactions(user_id):

    try:
        connection = psycopg2.connect(
            user="postgres", password="mypassword", host="localhost", port="5432", database="transactions")
        cursor = connection.cursor()
        query = f"select * from transactions where sender_id = '{user_id}';"
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


@router.post("/get_incoming_transactions")
async def get_incoming_transactions(user_id):

    try:
        connection = psycopg2.connect(
            user="postgres", password="mypassword", host="localhost", port="5432", database="transactions")
        cursor = connection.cursor()
        query = f"select * from transactions where recipient_id = '{user_id}';"
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
