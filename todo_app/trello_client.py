import os
import requests
import json
from datetime import datetime

def get_cards_from_all_lists():
    items = []
    items.extend(get_cards_from_list("TODO", os.getenv('TODO_LIST_ID')))
    items.extend(get_cards_from_list("DONE", os.getenv('DONE_LIST_ID')))
    return items 

def get_cards_from_list(list_name, list_id):
    url = f"https://trello.com/1/lists/{list_id}/cards"
    query = {"key": os.getenv('TRELLO_API_KEY'), "token": os.getenv('TRELLO_API_TOKEN')}
    response = requests.get(url, params=query)
    response.raise_for_status()
    items = []
    for item in response.json():
        items.append(Item(item["id"], item["name"], item["desc"], item["dateLastActivity"], list_name))
    return items

def create_card_on_todo_list(card_name, description=None):
    return create_card("TODO", os.getenv('TODO_LIST_ID'), card_name, description)

def create_card(list_name, list_id, card_name, description=None):
    url = f"https://api.trello.com/1/cards"
    query = {"name": card_name, "desc": description,"idList": list_id, "key": os.getenv('TRELLO_API_KEY'), "token": os.getenv('TRELLO_API_TOKEN')}
    response = requests.post(url, params=query)
    response.raise_for_status()
    return Item(response.json()["id"], response.json()["name"], response.json()["desc"], response.json()["dateLastActivity"], list_name)

def move_card_to_done_list(id):
    return move_card_to_list("DONE", os.getenv('DONE_LIST_ID'), id)

def move_card_to_todo_list(id):
    return move_card_to_list("TODO", os.getenv('TODO_LIST_ID'), id)

def move_card_to_list(list_name, list_id, id):
    url = f"https://api.trello.com/1/cards/{id}"
    headers = {"Accept": "application/json"}
    query = {"key": os.getenv('TRELLO_API_KEY'), "token": os.getenv('TRELLO_API_TOKEN'), "idList":list_id}
    response = requests.put(url, headers=headers, params=query)
    response.raise_for_status()
    return Item(response.json()["id"], response.json()["name"], response.json()["desc"], response.json()["dateLastActivity"], list_name)

class Item:

  def __init__(self, identity, name, desc, last_modified, list_name):
    self.identity = identity  
    self.name = name
    self.desc = desc
    self.last_modified = datetime.strptime(last_modified, "%Y-%m-%dT%H:%M:%S.%fZ").date()
    self.list_name = list_name

class ItemViewModel:

    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def to_do_items(self):
        items_to_do=[]
        for item in self._items:
            if item.list_name.upper() == "TODO":
                items_to_do.append(item)
        return items_to_do

    @property
    def done_items(self):
        items_done=[]
        for item in self._items:
            if item.list_name.upper() == "DONE":
                items_done.append(item)
        return items_done

    @property
    def count_of_done_items(self):
        self._n_done = len(self.done_items)
        return self._n_done

    @property
    def recent_done_items(self):
        items_done=[]
        for item in self.done_items:
            if item.last_modified >= datetime.today().date():
                items_done.append(item)
        return items_done
    
    @property
    def count_of_recent_done_items(self):
        self._n_recent_done = len(self.recent_done_items)
        return self._n_recent_done 

    @property
    def older_done_items(self):
        items_done=[]
        for item in self.done_items:
            if item.last_modified < datetime.today().date():
                items_done.append(item)
        return items_done
    
    @property
    def should_show_all_done_items(self):
        if (self.count_of_done_items <=5):
            return True
        else:
            return False
    