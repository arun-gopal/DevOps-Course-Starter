import os
import requests
import json
from datetime import datetime


TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_API_TOKEN = os.getenv('TRELLO_API_TOKEN')
BOARD_ID = os.getenv('ITEMS_BOARD_ID')
TODO_LIST_ID = os.getenv('TODO_LIST_ID')
DONE_LIST_ID = os.getenv('DONE_LIST_ID')

def get_cards_from_todo_list():
    return get_cards_from_list(TODO_LIST_ID)

def get_cards_from_done_list():
    return get_cards_from_list(DONE_LIST_ID)

def get_cards_from_list(list_id):
    url = f"https://trello.com/1/lists/{list_id}/cards?key={TRELLO_API_KEY}&token={TRELLO_API_TOKEN}"
    query = {"key": TRELLO_API_KEY, "token": TRELLO_API_TOKEN}
    response = requests.request("GET", url, params=query)
    response.raise_for_status()
    items = []
    for item in response.json():
        items.append(Item(item["id"], item["name"], item["desc"], item["dateLastActivity"]))
    return items

def create_card_on_todo_list(card_name, description=None):
    return create_card(TODO_LIST_ID, card_name, description)

def create_card(list_id, card_name, description=None):
    url = f"https://api.trello.com/1/cards"
    query = {"name": card_name, "desc": description,"idList": list_id, "key": TRELLO_API_KEY, "token": TRELLO_API_TOKEN}
    response = requests.request("POST", url, params=query)
    response.raise_for_status()
    return Item(response.json()["id"], response.json()["name"], response.json()["desc"], response.json()["dateLastActivity"])

def move_card_to_done_list(id):
    return move_card_to_list(DONE_LIST_ID, id)

def move_card_to_todo_list(id):
    return move_card_to_list(TODO_LIST_ID, id)

def move_card_to_list(list_id, id):
    url = f"https://api.trello.com/1/cards/{id}"
    headers = {"Accept": "application/json"}
    query = {"key": TRELLO_API_KEY, "token": TRELLO_API_TOKEN, "idList":list_id}
    response = requests.request("PUT", url, headers=headers, params=query)
    response.raise_for_status()
    return Item(response.json()["id"], response.json()["name"], response.json()["desc"], response.json()["dateLastActivity"])

class Item:

  def __init__(self, identity, name, desc, last_modified):
    self.identity = identity  
    self.name = name
    self.desc = desc
    self.last_modified = datetime.strptime(last_modified, "%Y-%m-%dT%H:%M:%S.%fZ").date()

class ItemViewModel:

    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items
