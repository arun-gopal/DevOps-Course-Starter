import pytest
from selenium import webdriver
from threading import Thread
from todo_app import app
from dotenv import load_dotenv, find_dotenv   
import time
import os
from todo_app import app
import requests

@pytest.fixture(scope='module')
def test_app():
       file_path = find_dotenv('.env')
       load_dotenv(file_path, override=True)
       board_id = create_trello_board()
       os.environ['ITEMS_BOARD_ID'] = board_id
       os.environ['TODO_LIST_ID'] = get_list_id_for_board(board_id, "TO DO")
       os.environ['DONE_LIST_ID'] = get_list_id_for_board(board_id, "DONE")

       #Start the application in its own thread
       application = app.create_app()
       thread = Thread(target=lambda: application.run(use_reloader=False))
       thread.daemon = True
       thread.start()
       yield application

       #Delete the test board
       thread.join(1)
       time.sleep(5)
       delete_trello_board(board_id)

@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        driver.implicitly_wait(5)
        yield driver

def testDriver(test_app, driver):
    driver.get('http://127.0.0.1:5000/')
    assert driver.title == 'To-Do App'
    
def create_trello_board():
    API_KEY = os.getenv('TRELLO_API_KEY')
    TOKEN = os.getenv('TRELLO_API_TOKEN')
    url = f"https://api.trello.com/1/boards/"
    query = {"key": API_KEY, "token": TOKEN, "name": 'TestBoard'}
    response = requests.request("POST", url, params=query)
    value = response.json()["id"]
    print("Test board created, id=" + value)
    return value

def delete_trello_board(id):
    API_KEY = os.getenv('TRELLO_API_KEY')
    TOKEN = os.getenv('TRELLO_API_TOKEN')
    url = "https://api.trello.com/1/boards/" + id
    query = {"key": API_KEY, "token": TOKEN}
    requests.request("DELETE", url, params=query)
    print("Test board deleted, id=" + id)

def get_list_id_for_board(board_id, list_name):
    print("Searching for " + list_name)
    API_KEY = os.getenv('TRELLO_API_KEY')
    TOKEN = os.getenv('TRELLO_API_TOKEN')
    url = "https://api.trello.com/1/boards/" + board_id + "/lists/"
    query = {"key": API_KEY, "token": TOKEN}
    response = requests.request("GET", url, params=query).json()
    for item in response:
        if list_name.upper() == item["name"].upper():
            list_id = item["id"]
    print("Found " + list_id)        
    return list_id
    
def test_createTask(test_app, driver):
    testDriver(test_app, driver)
    driver.find_element_by_id("title").send_keys("Selenium is flaky")
    driver.find_element_by_id("description").send_keys("Selenium is flaky")
    driver.find_element_by_id("submit").click()

def test_start_task(test_app, driver):
    driver.find_element_by_xpath("//*[contains(text(),'Start')]").click()

def test_reset_task(test_app, driver):
    driver.find_element_by_xpath("//*[contains(text(),'Reset')]").click()

