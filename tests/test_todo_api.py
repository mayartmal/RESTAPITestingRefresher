import requests
import pytest


ENDPOINT = 'https://todo.pixegami.io/'

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    pass

def test_can_create_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200

    create_task_data = create_task_response.json()
    task_id = create_task_data['task']['task_id']
    get_task_response = get_task(task_id)

    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    assert get_task_data['content'] == payload['content']
    assert get_task_data['user_id'] == payload['user_id']
    print(get_task_data)

def test_can_update_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]
    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "new content",
        "is_done": True
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    #get and validate changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data['content'] == new_payload['content']
    assert get_task_data['user_id'] == new_payload['user_id']

def create_task(payload):
    return requests.put(ENDPOINT + '/create-task', json=payload)

def update_task(payload):
    return requests.put(ENDPOINT + '/update-task', json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f'/get-task/{task_id}')

def new_task_payload():
    return {
        "content": "test content",
        "user_id": "test user",
        "is_done": False
    }