from fastapi import APIRouter
from .model.balance import Balance
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import sys
import psycopg2
from psycopg2 import Error
import asyncio
import os
import json
router = APIRouter()

KAKFA_HOSTNAME = os.environ.get('KAFKA_HOSTNAME', 'localhost')

PSQL_DATABASE_HOSTNAME = os.environ.get('DB_HOSTNAME', 'localhost')
PSQL_USERNAME = os.environ.get('DB_USER', 'postgres')
PSQL_PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')
PSQL_DATABASE_NAME = os.environ.get('DB_NAME', 'balances')

KAFKA_INSTANCE = KAKFA_HOSTNAME + ":9092"

loop = asyncio.get_event_loop()

aioproducer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_INSTANCE)

consumer = AIOKafkaConsumer("transactions", bootstrap_servers=KAFKA_INSTANCE)


async def consume():
    await consumer.start()
    try:
        async for msg in consumer:
            value = json.loads(msg.value)
            await update_user_balance(value['sender_id'], value['recipient_id'], value['amount'])
    finally:
        await consumer.stop()


@router.on_event("startup")
async def startup():
    await aioproducer.start()
    loop.create_task(consume())


@router.on_event("shutdown")
async def shutdown():
    await aioproducer.stop()
    await consumer.stop()


@router.get("/balance")
async def get_balances() -> dict:
    return {"data": Balance}


@router.post("/get_user_balance")
async def get_user_balance(user_id):
    try:
        connection = psycopg2.connect(
            user=PSQL_USERNAME, password=PSQL_PASSWORD, host=PSQL_DATABASE_HOSTNAME, port="5432", database=PSQL_DATABASE_NAME)
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
            user=PSQL_USERNAME, password=PSQL_PASSWORD, host=PSQL_DATABASE_HOSTNAME, port="5432", database=PSQL_DATABASE_NAME)
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
async def update_user_balance(sender_id: int, recipient_id: int, amount: float):

    try:
        connection = psycopg2.connect(
            user=PSQL_USERNAME, password=PSQL_PASSWORD, host=PSQL_DATABASE_HOSTNAME, port="5432", database=PSQL_DATABASE_NAME)
        cursor = connection.cursor()
        query = f"update balances set balance = balance - {amount} where user_id='{sender_id}'; update balances set balance = balance + {amount} where user_id='{recipient_id}';"

        cursor.execute(query)
        connection.commit()

    except (Exception, Error) as error:
        print(error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Conn closed successfully")


async def produce_transaction(msg: Balance):
    await aioproducer.send('balances', json.dumps(msg.dict()).encode("ascii"))
