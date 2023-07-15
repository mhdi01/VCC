import random
from .config import client

def test_create_setting():
    global setting_name
    setting_name = "TestName_{0}".format(random.randrange(1,5000))
    data = {
        "name": setting_name,
        "SeatType": "VCRoom",
        "MaxCallRate": 9000,
        "OverlayText": True,
        "HostView": "one_main_zero_pips",
        "EnableChat": True,
        "GuestsCanPresent": True,
        "MuteAllGuests": True,
        "Status": True,
        "IsDefault": True
    }
    response = client.post(
        "/api/Settings",
        json=data
    )
    global setting_id 
    setting_id = response.json()['id']
    assert response.status_code == 200
    assert response.json()['name'] == setting_name


def test_get_settings():
    response = client.get(
        "/api/Settings"
    )
    assert response.status_code == 200


def test_retrieve_setting():
    response = client.get(
        "/api/Settings/{0}".format(setting_id)
    )
    assert response.status_code == 200
    assert response.json()['name'] == setting_name


def test_update_setting():
    global setting_name
    setting_name = "TestName_{0}".format(random.randrange(1,5000))
    data = {
        "name": setting_name,
        "SeatType": "VCRoom",
        "MaxCallRate": 9000,
        "OverlayText": True,
        "HostView": "one_main_zero_pips",
        "EnableChat": True,
        "GuestsCanPresent": True,
        "MuteAllGuests": True,
        "Status": True,
        "IsDefault": True
    }
    response = client.put(
        "/api/Settings/{0}".format(setting_id),
        json=data
    )
    assert response.status_code == 200
    assert response.json()['name'] == setting_name


def test_update_setting_partial():
    global setting_name
    setting_name = "TestName_{0}".format(random.randrange(1,5000))
    data = {
        'name': setting_name
    }
    response = client.patch(
        "/api/Settings/{0}".format(setting_id),
        json=data
    )
    assert response.status_code == 200
    assert response.json()['name'] == setting_name


def test_delete_setting():
    reponse = client.delete(
        "/api/Settings/{0}".format(setting_id)
    )
    assert reponse.status_code == 204
