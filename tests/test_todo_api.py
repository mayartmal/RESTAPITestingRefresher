import requests
import pytest


ENDPOINT = 'https://todo.pixegami.io/'

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    pass

def test_can_create_task():
    payload = {
        "content": "test content",
        "user_id": "test user",
        "is_done": False
    }
    create_task_response = requests.put(ENDPOINT + '/create-task', json=payload)
    assert create_task_response.status_code == 200

    create_task_data = create_task_response.json()
    task_id = create_task_data['task']['task_id']
    get_task_response = requests.get(ENDPOINT + f'/get-task/{task_id}')

    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    assert get_task_data['content'] == payload['content']
    assert get_task_data['user_id'] == payload['user_id']
    print(get_task_data)
