import unittest
from _pytest.monkeypatch import MonkeyPatch
from mock import patch
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}

def test_upload_success():
    filename = 'requirements.txt'
    with open(filename, 'rb') as f:
        text = f.read()
        response = client.post("/upload", files={"files": (filename, text)}, auth=('admin', 'admin'))
        print(response.json())
        assert response.status_code == 200
        assert response.json() == {"message": "Successfully uploaded"}

def test_upload_failure():
    filename = 'requirements.txt'
    with open(filename, 'rb') as f:
        text = f.read()
        response = client.post("/upload", files={"files": (filename, text)}, auth=('admin1', 'admin1'))

        assert response.status_code == 401
        assert response.json() == {'detail': 'Incorrect username or password'}

# class TestClient(unittest.TestCase):
#     def setUp(self):
#         pass
#
#     def test_read_main(self):
#         response = client.get("/")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {"message": "Hello World!"})
