import sqlite3
import os.path
import numpy as np
from app.menu_analysis import import_menu_csv, nlp

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

def get_n_most_similar(query_id, N=5):

    try:
        db = create_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM FoodItems''')
        items = cursor.fetchall()

        # Perform Fetch and Conversion
        vecs = {}
        food_items = {}
        for food_id, food_name, semantic_vec_blob, description in items:
            if semantic_vec_blob is not None:
                vecs[food_id] = np.fromstring(semantic_vec_blob, dtype=np.float32)
                food_items[food_id] = {
                    'food_id': food_id,
                    'food_name': food_name,
                    'description': description
                }

        
        # Perform Exhaustive Search
        query_vec = vecs.pop(query_id)
        similarities = []
        for food_id, vec in vecs.items():
            # Compute the cosine similarity
            a, b = query_vec, vec
            cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
            similarities.append((food_id, cos_sim))

        result = []
        for _id, score in sorted(similarities, key=lambda x: x[1], reverse=True)[:N]:
            result.append({
                'food_item': food_items[_id],
                'similarity_score': str(score)
            })
        return result

    except Exception as e:
        print(e)
        return []

if __name__ == '__main__':
    # add_menu('dummy_menu.csv')
    print(get_n_most_similar(query_id=11, N=10))
