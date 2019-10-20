import sqlite3
import os.path
from app.menu_analysis import import_menu_csv

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
        cursor.execute('''SELECT FullAddress, RestaurantName FROM Restaurants''')
        restaurants = cursor.fetchall()  # Retrieve all results

    except Exception as e:
        print(e)

    return restaurants


def add_menu(menu_csv_path):
    for menu_item in import_menu_csv(menu_csv_path):
        try:
            db = create_connection()
            cursor = db.cursor()

            food_tup = (menu_item.item_title, menu_item.vector.tostring(), menu_item.description)

            # Insert foodItem
            sql = ''' INSERT INTO FoodItems(FoodName,SemanticVec,Description)
                    VALUES(?,?,?) '''
            cursor.execute(sql, food_tup)

            food_id = cursor.lastrowid

            restaurant_food = (menu_item.restaurant_id, food_id, None)
            print(menu_item.item_title, food_id, restaurant_food)

            # Insert restaurantFood
            sql = ''' INSERT INTO RestaurantFoods(RestaurantID,FoodID,UniqueFoodID)
                    VALUES(?,?,?) '''
            cursor.execute(sql, restaurant_food)
            db.commit()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    add_menu('dummy_menu.csv')
