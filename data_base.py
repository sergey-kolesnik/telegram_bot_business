import mysql.connector
from config import USER, PASSWORD, HOST, DATABASE
from loguru import logger

@logger.catch()
def path_mysql_database():
    """Функция передачи аргументов для базы данных"""
    conn = mysql.connector.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        database=DATABASE
    )
    return conn

@logger.catch()
def recording_user_id(user_id: int) -> None:
    """Функция записи id в базу данных
    :param user_id: id клиента
    :type user_id: int
    :return: None"""
    data = []
    try:
        conn = path_mysql_database()

        cur = conn.cursor()
        query = ('SELECT * FROM user_id')
        cur.execute(query)

        for user in cur:
            data.append(user)
        total = (user_id,)
        if not total in data:
            insert_query = ('insert into `user_id`(`id`) values (%s) ')
            val = (int(user_id),)
            cur.execute(insert_query, val)
            conn.commit()

        cur.close()
        conn.close()
    except Exception as error:
        logger.error(error)

