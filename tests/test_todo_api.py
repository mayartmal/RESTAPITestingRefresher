import requests
import pytest
import uuid


ENDPOINT = 'https://todo.pixegami.io/'

#tests
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

def test_can_list_tasks():
    #create 3 tasks for 1 user
    #verify get same info
    n = 3
    payload = new_task_payload()
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200
    user_id = payload["user_id"]
    list_task_response = list_task(user_id)
    assert list_task_response.status_code == 200
    data = list_task_response.json()
    tasks = data['tasks']
    assert len(tasks) == n

def test_can_delete_task():
    # delete 1 task
    # validate
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()['task']['task_id']

    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404



    pass


#aux functions:
def create_task(payload):
    return requests.put(ENDPOINT + '/create-task', json=payload)

def update_task(payload):
    return requests.put(ENDPOINT + '/update-task', json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f'/get-task/{task_id}')

def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    return {
        "content": content,
        "user_id": user_id,
        "is_done": False
    }

def list_task(user_id):
    return requests.get(ENDPOINT + f'/list-tasks/{user_id}')

def delete_task(task_id):
    return requests.delete(ENDPOINT + f'/delete-task/{task_id}')