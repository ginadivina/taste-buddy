# Before running, call: "python3 -m spacy download en_pytt_bertbaseuncased_lg"

import spacy
import torch
import numpy as np
import pandas as pd
from price_parser import Price
from itertools import combinations

nlp = spacy.load("en_pytt_bertbaseuncased_lg")

is_using_gpu = spacy.prefer_gpu()
if is_using_gpu:
    torch.set_default_tensor_type("torch.cuda.FloatTensor")

class MenuItem():
    def __init__(self, item_title, item_description, item_price_str, restaurant_id):
        self.item_title = item_title.title()
        self.description = item_description
        self.price = Price.fromstring(item_price_str)
        self.title_nlp = nlp(self.item_title)
        self.description_nlp = nlp(self.description)
        self.restaurant_id = restaurant_id

    def __repr__(self):
        return repr(self.item_title)

    @property
    def vector(self):
        return self.description_nlp.vector

    def similarity(self, other_menu_item):
        assert isinstance(other_menu_item, self.__class__)
        return self.description_nlp.similarity(other_menu_item.description_nlp)

def import_menu_csv(csv_path):
    print('Importing menu...')
    menu = []
    df = pd.read_csv(csv_path)
    print(df)
    if not (set(['name', 'description', 'price', 'restaurant_id']).issubset(set(df.keys()))):
        raise Exception("Menu CSV must have columns 'name', 'description', 'price'")

    for index, row in df.iterrows():
        tup = (row['name'], row['description'], row['price'], row['restaurant_id'])
        menu.append(MenuItem(*tup))

    return menu


if __name__ == '__main__':
    menu_items = import_menu_csv('dummy_menu.csv')
    print(menu_items[0].vector.dtype)

    for item_a, item_b in combinations(menu_items, 2):
        print('{} has {:.2%} similarity to {}'.format(item_a, item_a.similarity(item_b), item_b))
