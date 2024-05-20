from fastapi import APIRouter
from .model.transaction import Transaction
import sys
from aiokafka import AIOKafkaProducer
import psycopg2
import json
from psycopg2 import Error
import os
router = APIRouter()

KAKFA_HOSTNAME = os.environ.get('KAFKA_HOSTNAME', 'localhost')

PSQL_DATABASE_HOSTNAME = os.environ.get('DB_HOSTNAME', 'localhost')
PSQL_USERNAME = os.environ.get('DB_USER', 'postgres')
PSQL_PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')
PSQL_DATABASE_NAME = os.environ.get('DB_NAME', 'transactions')

KAFKA_INSTANCE = KAKFA_HOSTNAME + ":9092"

loop = asyncio.get_event_loop()

aioproducer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_INSTANCE)


@router.get("/transactions")
async def get_transactions() -> dict:
    return {"data": Transaction}


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
            await produce_transaction(transaction)
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


async def produce_transaction(msg: Transaction):
    await aioproducer.send('transactions', json.dumps(msg.dict()).encode("ascii"))
