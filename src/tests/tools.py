import random
from .config import client

def create_setting():
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
    return setting_id


def delete_setting(setting_id):
    reponse = client.delete(
        "/api/Settings/{0}".format(setting_id)
    )
