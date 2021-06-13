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
    print(response.data.decode())
    assert response.status_code == 200

def mock_get_cards(url, params=None):

    if url == f'https://trello.com/1/lists/todo_list_id/cards?key=test_key&token=test_token': 
        response = Mock()
        response.json.return_value = sample_trello_cards_response()
        return response

    if url == f'https://trello.com/1/lists/done_list_id/cards?key=test_key&token=test_token': 
        response = Mock()
        response.json.return_value = sample_trello_cards_response()
        return response
    
    return None

def sample_trello_cards_response():
    return [
    {
        "id": "60969ef0795a5e4c0e063550",
        "checkItemStates": null,
        "closed": false,
        "dateLastActivity": "2021-06-13T13:27:13.664Z",
        "desc": "",
        "descData": null,
        "dueReminder": null,
        "idBoard": "60969ec0352fff8f55154c9b",
        "idList": "60969ec0352fff8f55154c9c",
        "idMembersVoted": [],
        "idShort": 1,
        "idAttachmentCover": null,
        "idLabels": [],
        "manualCoverAttachment": false,
        "name": "Testing",
        "pos": 65535,
        "shortLink": "icDeyrgc",
        "isTemplate": false,
        "cardRole": null,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": false,
            "votes": 0,
            "viewingMemberVoted": false,
            "subscribed": false,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": null,
            "comments": 0,
            "attachments": 0,
            "description": false,
            "due": null,
            "dueComplete": false,
            "start": null
        },
        "dueComplete": false,
        "due": null,
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/icDeyrgc",
        "start": null,
        "subscribed": false,
        "url": "https://trello.com/c/icDeyrgc/1-testing",
        "cover": {
            "idAttachment": null,
            "color": null,
            "idUploadedBackground": null,
            "size": "normal",
            "brightness": "dark",
            "idPlugin": null
        }
    },
    {
        "id": "60969f1f22fb795aa3a9a676",
        "checkItemStates": null,
        "closed": false,
        "dateLastActivity": "2021-06-13T13:27:16.948Z",
        "desc": "",
        "descData": null,
        "dueReminder": null,
        "idBoard": "60969ec0352fff8f55154c9b",
        "idList": "60969ec0352fff8f55154c9c",
        "idMembersVoted": [],
        "idShort": 5,
        "idAttachmentCover": null,
        "idLabels": [],
        "manualCoverAttachment": false,
        "name": "Another Test",
        "pos": 65535,
        "shortLink": "ZUK5nFYH",
        "isTemplate": false,
        "cardRole": null,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": false,
            "votes": 0,
            "viewingMemberVoted": false,
            "subscribed": false,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": null,
            "comments": 0,
            "attachments": 0,
            "description": false,
            "due": null,
            "dueComplete": false,
            "start": null
        },
        "dueComplete": false,
        "due": null,
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/ZUK5nFYH",
        "start": null,
        "subscribed": false,
        "url": "https://trello.com/c/ZUK5nFYH/5-another-test",
        "cover": {
            "idAttachment": null,
            "color": null,
            "idUploadedBackground": null,
            "size": "normal",
            "brightness": "dark",
            "idPlugin": null
        }
    }
]