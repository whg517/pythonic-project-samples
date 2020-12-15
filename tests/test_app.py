"""Test index"""


def test_index(test_client):
    """test index view"""
    response = test_client.get('/')
    assert response.status_code == 200
    assert response.text == '"Hello world"'
