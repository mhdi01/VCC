import random
from .config import client

def test_create_profile():
    global profile_name
    profile_name = "TestName_{0}".format(random.randrange(1,5000))
    data = {
        "name": profile_name,
        "ProfileTag": "string",
        "ReservedAliases": ["string"],
        "ProfileFQDN": "string",
        "Status": True
    }
    response = client.post(
        "/api/Profiles",
        json=data
    )
    global profile_id 
    profile_id = response.json()['id']
    assert response.status_code == 200
    assert response.json()['name'] == profile_name


def test_get_profiles():
    response = client.get(
        "/api/Profiles"
    )
    assert response.status_code == 200


def test_retrieve_profile():
    response = client.get(
        "/api/Profiles/{0}".format(profile_id)
    )
    assert response.status_code == 200
    assert response.json()['name'] == profile_name


def test_update_profile():
    global profile_name
    profile_name = "TestName_{0}".format(random.randrange(1,5000))
    data = {
        "name": profile_name,
        "ProfileTag": "string",
        "ReservedAliases": ["string"],
        "ProfileFQDN": "string",
        "Status": True
    }
    response = client.put(
        "/api/Profiles/{0}".format(profile_id),
        json=data
    )
    assert response.status_code == 200
    assert response.json()['name'] == profile_name


def test_update_profile_partial():
    global profile_name
    profile_name = "TestName_{0}".format(random.randrange(1,5000))
    data = {
        'name': profile_name
    }
    response = client.patch(
        "/api/Profiles/{0}".format(profile_id),
        json=data
    )
    assert response.status_code == 200
    assert response.json()['name'] == profile_name


def test_delete_profile():
    reponse = client.delete(
        "/api/Profiles/{0}".format(profile_id)
    )
    assert reponse.status_code == 204
    
    
