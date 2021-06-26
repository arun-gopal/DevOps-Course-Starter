import pytest, os
from dotenv import find_dotenv, load_dotenv
import todo_app.app as app
from unittest.mock import patch, Mock

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    test_app = app.create_app()
    with test_app.test_client() as client: 
        yield client

@patch('requests.get')
def test_index_page(mock_get, client):
    mock_get.side_effect = mock_get_cards
    response = client.get('/')
    assert response.status_code == 200

def mock_get_cards(url, params):

    TODO_LIST_ID = os.getenv('TODO_LIST_ID')
    DONE_LIST_ID = os.getenv('DONE_LIST_ID')

    if url == f'https://trello.com/1/lists/{TODO_LIST_ID}/cards': 
        response = Mock()
        response.json.return_value = sample_trello_cards_response()
        return response

    if url == f'https://trello.com/1/lists/{DONE_LIST_ID}/cards': 
        response = Mock()
        response.json.return_value = sample_trello_cards_response()
        return response
    
    return None

def sample_trello_cards_response():
    return [
    {
        "id": "60969ef0795a5e4c0e063550",
        "checkItemStates": None,
        "closed": False,
        "dateLastActivity": "2021-06-13T13:27:13.664Z",
        "desc": "",
        "descData": None,
        "dueReminder": None,
        "idBoard": "60969ec0352fff8f55154c9b",
        "idList": "60969ec0352fff8f55154c9c",
        "idMembersVoted": [],
        "idShort": 1,
        "idAttachmentCover": None,
        "idLabels": [],
        "manualCoverAttachment": False,
        "name": "Testing",
        "pos": 65535,
        "shortLink": "icDeyrgc",
        "isTemplate": False,
        "cardRole": None,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": False,
            "votes": 0,
            "viewingMemberVoted": False,
            "subscribed": False,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": None,
            "comments": 0,
            "attachments": 0,
            "description": False,
            "due": None,
            "dueComplete": False,
            "start": None
        },
        "dueComplete": False,
        "due": None,
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/icDeyrgc",
        "start": None,
        "subscribed": False,
        "url": "https://trello.com/c/icDeyrgc/1-testing",
        "cover": {
            "idAttachment": None,
            "color": None,
            "idUploadedBackground": None,
            "size": "normal",
            "brightness": "dark",
            "idPlugin": None
        }
    },
    {
        "id": "60969f1f22fb795aa3a9a676",
        "checkItemStates": None,
        "closed": False,
        "dateLastActivity": "2021-06-13T13:27:16.948Z",
        "desc": "",
        "descData": None,
        "dueReminder": None,
        "idBoard": "60969ec0352fff8f55154c9b",
        "idList": "60969ec0352fff8f55154c9c",
        "idMembersVoted": [],
        "idShort": 5,
        "idAttachmentCover": None,
        "idLabels": [],
        "manualCoverAttachment": False,
        "name": "Another Test",
        "pos": 65535,
        "shortLink": "ZUK5nFYH",
        "isTemplate": False,
        "cardRole": None,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": False,
            "votes": 0,
            "viewingMemberVoted": False,
            "subscribed": False,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": None,
            "comments": 0,
            "attachments": 0,
            "description": False,
            "due": None,
            "dueComplete": False,
            "start": None
        },
        "dueComplete": False,
        "due": None,
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/ZUK5nFYH",
        "start": None,
        "subscribed": False,
        "url": "https://trello.com/c/ZUK5nFYH/5-another-test",
        "cover": {
            "idAttachment": None,
            "color": None,
            "idUploadedBackground": None,
            "size": "normal",
            "brightness": "dark",
            "idPlugin": None
        }
    }
]