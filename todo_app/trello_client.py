import os
import requests
import json

TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_API_TOKEN = os.getenv('TRELLO_API_TOKEN')
BOARD_ID = os.getenv('ITEMS_BOARD_ID')
TODO_LIST_ID = os.getenv('TODO_LIST_ID')
DONE_LIST_ID = os.getenv('DONE_LIST_ID')

print(TRELLO_API_KEY, TRELLO_API_TOKEN, BOARD_ID, TODO_LIST_ID, DONE_LIST_ID)

def get_cards_from_board_items():
    return get_cards_from_board(BOARD_ID)

def get_cards_from_board(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    query = {"key": TRELLO_API_KEY, "token": TRELLO_API_TOKEN}
    response = requests.request("GET", url, params=query)
    response.raise_for_status()
    return response.json()

def create_card_on_todo_list(card_name, description=None):
    return create_card(TODO_LIST_ID, card_name, description)

def create_card(list_id, card_name, description=None):
    url = f"https://api.trello.com/1/cards"
    query = {"name": card_name, "desc": description,"idList": list_id, "key": TRELLO_API_KEY, "token": TRELLO_API_TOKEN}
    response = requests.request("POST", url, params=query)
    response.raise_for_status()
    card_id = response.json()["id"]
    return card_id


