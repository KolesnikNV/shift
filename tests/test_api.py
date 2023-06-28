import pytest
import requests
from shift.main import populate_admin


@pytest.fixture(scope="module")
async def get_admin_id():
    user = await populate_admin()
    user_id = str(user[0])
    return user_id


@pytest.fixture(scope="module")
async def get_admin_password():
    user = await populate_admin()
    password = user[1]
    return password


@pytest.fixture(scope="module")
async def admin_credentials(get_admin_id, get_admin_password):
    return {"user_id": get_admin_id, "password": get_admin_password}


@pytest.fixture(scope="module")
def created_user(admin_credentials):
    url = "http://127.0.0.1:8000/login/"
    admin_response = requests.post(url, json=admin_credentials)
    access_token = admin_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "http://127.0.0.1:8000/user/create/"
    user_data = {
        "name": "name",
        "surname": "string",
        "email": "test1@mail.ru",
        "password": "password",
        "is_admin": False,
        "salary": 0,
        "salary_increase_date": "string",
    }
    response = requests.post(url, headers=headers, json=user_data)
    assert response.status_code == 200
    user_id = response.json()["user_id"]
    user_password = user_data["password"]
    yield {"user_id": user_id, "password": user_password}
    url = f"http://127.0.0.1:8000/user/{user_id}/"


@pytest.fixture(scope="module")
def user_credentials(created_user):
    user_id = created_user["user_id"]
    password = created_user["password"]
    return {"user_id": user_id, "password": password}


def test_admin_login(admin_credentials):
    url = "http://127.0.0.1:8000/login/"
    response = requests.post(url, json=admin_credentials)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_user_as_admin(admin_credentials):
    url = "http://127.0.0.1:8000/login/"
    admin_response = requests.post(url, json=admin_credentials)
    access_token = admin_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "http://127.0.0.1:8000/user/create/"
    user_data = {
        "name": "string",
        "surname": "string",
        "email": "test2222@mail.ru",
        "password": "password",
        "is_admin": False,
        "salary": 0,
        "salary_increase_date": "string",
    }
    response = requests.post(url, headers=headers, json=user_data)
    user_id = response.json()["user_id"]
    assert response.status_code == 200
    assert response.json()["name"] == user_data["name"]
    assert response.json()["surname"] == user_data["surname"]
    assert response.json()["email"] == user_data["email"]
    assert response.json()["password"] == user_data["password"]
    assert response.json()["salary"] == user_data["salary"]
    assert (
        response.json()["salary_increase_date"]
        == user_data["salary_increase_date"]
    )
    assert response.status_code == 200
    url = f"http://127.0.0.1:8000/user/{user_id}/"
    response = requests.delete(url, headers=headers)


def test_create_user_as_non_admin(user_credentials):
    url = "http://127.0.0.1:8000/login/"
    user_response = requests.post(url, json=user_credentials)
    assert user_response.status_code == 200
    access_token = user_response.json()["access_token"]

    url = "http://127.0.0.1:8000/user/create/"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_data = {
        "name": "string",
        "surname": "string",
        "email": "test3@mail.ru",
        "password": "password",
        "is_admin": False,
        "salary": 0,
        "salary_increase_date": "string",
    }
    response = requests.post(url, headers=headers, json=user_data)
    assert response.status_code == 403
    response = requests.delete(url, headers=headers)


def test_patch_user_as_admin(admin_credentials):
    url = "http://127.0.0.1:8000/login/"
    admin_response = requests.post(url, json=admin_credentials)
    assert admin_response.status_code == 200
    access_token = admin_response.json()["access_token"]

    url = "http://127.0.0.1:8000/user/create/"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_data = {
        "name": "Test",
        "surname": "Usessr",
        "email": "test4@mail.ru",
        "password": "password",
        "is_admin": False,
        "salary": 1000,
        "salary_increase_date": "2023-01-01",
    }
    create_response = requests.post(url, headers=headers, json=user_data)
    assert create_response.status_code == 200
    user_id = create_response.json()["user_id"]

    url = f"http://127.0.0.1:8000/user/{user_id}/"
    headers = {"Authorization": f"Bearer {access_token}"}
    updated_user_data = {
        "name": "Update",
        "surname": "surname",
        "email": "test5@mail.ru",
        "password": "password",
        "is_admin": False,
        "salary": 1000,
        "salary_increase_date": "2023-01-01",
    }
    patch_response = requests.patch(
        url, headers=headers, json=updated_user_data
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["name"] == "Update"
    patch_response = requests.delete(url, headers=headers)


def test_get_user_by_id_as_non_admin(user_credentials, admin_credentials):
    url = "http://127.0.0.1:8000/login/"
    admin_response = requests.post(url, json=admin_credentials)
    assert admin_response.status_code == 200
    access_token = admin_response.json()["access_token"]
    url = "http://127.0.0.1:8000/user/create/"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_data = {
        "name": "Test",
        "surname": "User",
        "email": "test6@mail.ru",
        "password": "password",
        "is_admin": False,
        "salary": 1000,
        "salary_increase_date": "2023-01-01",
    }
    create_response = requests.post(url, headers=headers, json=user_data)
    assert create_response.status_code == 200
    user_id = create_response.json()["user_id"]
    password = create_response.json()["password"]
    url = "http://127.0.0.1:8000/login/"
    new_user_data = {"user_id": user_id, "password": password}
    user_response = requests.post(url, json=new_user_data)
    assert user_response.status_code == 200
    access_token = user_response.json()["access_token"]
    url = f"http://127.0.0.1:8000/user/{user_id}/"
    headers = {"Authorization": f"Bearer {access_token}"}
    get_response = requests.get(url, headers=headers)
    assert get_response.status_code == 403
    get_response = requests.delete(url, headers=headers)


def test_delete_user_as_admin(admin_credentials, user_credentials):
    url = "http://127.0.0.1:8000/login/"
    admin_response = requests.post(url, json=admin_credentials)
    assert admin_response.status_code == 200
    access_token = admin_response.json()["access_token"]
    user_id = user_credentials["user_id"]
    url = f"http://127.0.0.1:8000/user/{user_id}/"
    headers = {"Authorization": f"Bearer {access_token}"}
    delete_response = requests.delete(url, headers=headers)
    assert delete_response.status_code == 200
