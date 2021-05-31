from todo_app.trello_client import Item
from todo_app.trello_client import ItemViewModel

import pytest
from datetime import datetime

def get_items():
    items = [
        Item("1", "Item 1", "Description", "2020-05-01T00:00:00.000Z", "TODO"),
        Item("2", "Item 2", "Description", "2020-05-11T00:00:00.000Z", "TODO"),
        Item("3", "Item 3", "Description", "2020-05-21T00:00:00.000Z", "TODO"),
        Item("4", "Item 4", "Description", "2020-05-24T00:00:00.000Z", "TODO"),
        Item("5", "Item 5", "Description", "2020-05-30T00:00:00.000Z", "DONE"),
        Item("6", "Item 6", "Description", "2020-05-30T00:00:00.000Z", "DONE"),
        Item("7", "Item 7", "Description", "2020-05-24T00:00:00.000Z", "DONE"),
        Item("8", "Item 8", "Description", "2020-05-02T00:00:00.000Z", "DONE"),
        Item("9", "Item 9", "Description", datetime.now().strftime("%Y-%m-%d") + "T00:00:00.000Z", "DONE"),
        Item("10", "Item 10", "Description", datetime.now().strftime("%Y-%m-%d") + "T00:00:00.000Z", "DONE")
    ]
    return items

def get_four_done_items():
    items = [
        Item("7", "Item 7", "Description", "2020-05-24T00:00:00.000Z", "DONE"),
        Item("8", "Item 8", "Description", "2020-05-02T00:00:00.000Z", "DONE"),
        Item("9", "Item 9", "Description", datetime.now().strftime("%Y-%m-%d") + "T00:00:00.000Z", "DONE"),
        Item("10", "Item 10", "Description", datetime.now().strftime("%Y-%m-%d") + "T00:00:00.000Z", "DONE")
    ]
    return items

def test_items():
    viewmodel = ItemViewModel(get_items())
    result = viewmodel.items
    assert result != None
    assert len(result) == 10

def test_todo_items():
    viewmodel = ItemViewModel(get_items())
    result = viewmodel.to_do_items
    assert result != None
    assert len(result) == 4

def test_done_items():
    viewmodel = ItemViewModel(get_items())
    result = viewmodel.done_items
    assert result != None
    assert len(result) == 6

def test_count_of_done_items():
    viewmodel = ItemViewModel(get_items())
    result = viewmodel.done_items
    assert result != None
    assert len(result) == viewmodel.count_of_done_items

def test_recent_done_items():
    viewmodel = ItemViewModel(get_items())
    result = viewmodel.recent_done_items
    assert result != None
    assert len(result) == 2

def test_count_of_recent_done_items():
    viewmodel = ItemViewModel(get_items())
    result = viewmodel.recent_done_items
    assert result != None
    assert len(result) == viewmodel.count_of_recent_done_items

def test_older_done_items():
    viewmodel = ItemViewModel(get_items())
    result = viewmodel.older_done_items
    assert result != None
    assert len(result) == 4
   
def test_should_show_all_done_items_when_done_count_less_than_five():
    viewmodel = ItemViewModel(get_four_done_items())
    result = viewmodel.should_show_all_done_items
    assert result == True

def test_should_show_all_done_items_when_done_count_more_than_five():
    viewmodel = ItemViewModel(get_items())
    result = viewmodel.should_show_all_done_items
    assert result == False
