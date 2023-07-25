import random
from .config import client
from .tools import create_cluster, create_profile, delete_cluster, delete_profile, create_setting, delete_setting


setting_id = create_setting()
cluster_id = create_cluster(setting_id)
profile_id = create_profile()

def test_create_capacity():
    data = {
        "SeatType": "VCRoom",
        "PlanType": "Fixed",
        "CapacityLimit": 2000,
        "ProfileId": profile_id,
        "ClusterId": cluster_id,
        "StartTime": "2022-12-12 12:00:00",
        "EndTime": "2022-12-12 18:00:00",
        "Status": True
    }
    response = client.post(
        "/api/Profiles/{0}/Capacities/".format(profile_id),
        json=data
    )
    global capacity_id 
    print(response.json())
    capacity_id = response.json()['id']
    assert response.status_code == 200


def test_get_capacities():
    response = client.get(
        "/api/Profiles/{profile_id}/Capacities"
    )
    assert response.status_code == 200


def test_retrieve_capacity():
    response = client.get(
        "/api/Profiles/{0}/Capacities/{1}".format(profile_id, capacity_id)
    )
    assert response.status_code == 200


def test_update_capacity():
    data = {
        "SeatType": "VCRoom",
        "PlanType": "Fixed",
        "CapacityLimit": 3000,
        "ProfileId": profile_id,
        "ClusterId": cluster_id,
        "StartTime": "2022-12-12 15:00:00",
        "EndTime": "2022-12-12 18:00:00",
        "Status": True
    }
    response = client.put(
        "/api/Profiles/{0}/Capacities/{1}".format(profile_id, capacity_id),
        json=data
    )
    assert response.status_code == 200


def test_update_capacity_partial():
    data = {
        "CapacityLimit": 1000,
        "StartTime": "2022-12-13 15:00:00",
        "EndTime": "2022-12-13 18:00:00",
    }
    response = client.patch(
        "/api/Profiles/{0}/Capacities/{1}".format(profile_id, capacity_id),
        json=data
    )
    assert response.status_code == 200


def test_delete_capacity():
    reponse = client.delete(
        "/api/Profiles/{0}/Capacities/{1}".format(profile_id, capacity_id)
    )
    delete_profile(profile_id)
    delete_cluster(cluster_id)
    delete_setting(setting_id)
    assert reponse.status_code == 204
    


