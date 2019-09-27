# Before running, call: "python3 -m spacy download en_pytt_bertbaseuncased_lg"

import spacy
import torch
import numpy as np
from price_parser import Price
from itertools import combinations

nlp = spacy.load("en_pytt_bertbaseuncased_lg")

is_using_gpu = spacy.prefer_gpu()
if is_using_gpu:
    torch.set_default_tensor_type("torch.cuda.FloatTensor")

class MenuItem():
    def __init__(self, item_title, item_description, item_price_str):
        self.item_title = item_title.title()
        self.description = item_description
        self.price = Price.fromstring(item_price_str)
        self.title_nlp = nlp(self.item_title)
        self.description_nlp = nlp(self.description)

    def __repr__(self):
        return repr(self.item_title)

    @property
    def vector(self):
        return self.description_nlp.vector

    def similarity(self, other_menu_item):
        assert isinstance(other_menu_item, self.__class__)
        return self.description_nlp.similarity(other_menu_item.description_nlp)


if __name__ == '__main__':
    # TODO load raw documents. Perhaps use regex, or font information to separate??

    menu_items = [
        MenuItem('Onion Rings', 'sweet vidalia onions, deep fried in beer batter, glazed with thyme honey', '$6.50'),
        MenuItem('CHICKEN QUESADILLA', 'with caramelized onions, roasted poblano guacamole, jicama salsa & chipotle', '$8.50'),
        MenuItem('SHRIMP TACOS', 'with mango salsa, jalapeno-lime crème fraîche, guacamole & shredded cabbage', '$8.50'),
        MenuItem('Lamb Burger', 'lamb patty with mint aioli, fresh cucumbers & dill on a home-baked roll', '$10.75')
    ]

    for item_a, item_b in combinations(menu_items, 2):
        print(f'{item_a} has {item_a.similarity(item_b):.2%} similarity to {item_b}')
