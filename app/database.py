import sqlite3
import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "db.db")


def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        db = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return db


def db_search():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        db = create_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT Address FROM Restaurants''')
        restaurant_1 = cursor.fetchone()  # Retrieve the first row

    except Exception as e:
        print(e)

    return restaurant_1[0]