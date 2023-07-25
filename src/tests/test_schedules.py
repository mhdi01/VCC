import random
from .config import client
from .tools import create_cluster, create_profile, delete_cluster, delete_profile, create_setting, delete_setting, create_capacity, delete_capacity


setting_id = create_setting()
cluster_id = create_cluster(setting_id)
profile_id = create_profile()
capacity_id = create_capacity(profile_id, cluster_id)

def test_create_schedule():
    data = {
        "SeatType": "VCRoom",
        "Conference": "123123",
        "SeatLimit": 1000,
        "ProfileId": profile_id,
        "ClusterId": cluster_id,
        "StartTime": "2022-12-12 12:00",
        "EndTime": "2022-12-12 14:00",
        "Status": True
}
    response = client.post(
        "/api/Profiles/{0}/Capacities/{1}/Schedules/".format(profile_id, capacity_id),
        json=data
    )
    global schedule_id 
    schedule_id = response.json()['id']
    assert response.status_code == 200


def test_get_schedules():
    response = client.get(
        "/api/Profiles/{0}/Capacities/{1}/Schedules/".format(profile_id, capacity_id),
    )
    assert response.status_code == 200


def test_retrieve_schedule():
    response = client.get(
        "/api/Profiles/{0}/Capacities/{1}/Schedules/{2}/".format(profile_id, capacity_id, schedule_id),
    )
    assert response.status_code == 200


def test_update_schedule():
    data = {
        "SeatType": "VCRoom",
        "Conference": "4422",
        "SeatLimit": 2000,
        "ProfileId": profile_id,
        "ClusterId": cluster_id,
        "StartTime": "2022-12-12 13:00",
        "EndTime": "2022-12-12 14:00",
        "Status": True
}
    response = client.put(
        "/api/Profiles/{0}/Capacities/{1}/Schedules/{2}/".format(profile_id, capacity_id, schedule_id),
        json=data
    )
    assert response.status_code == 200


def test_update_schedule_partial():
    data = {
        "CapacityLimit": 1000,
        "StartTime": "2022-12-13 15:00:00",
        "EndTime": "2022-12-13 18:00:00",
    }
    response = client.patch(
        "/api/Profiles/{0}/Capacities/{1}/Schedules/{2}/".format(profile_id, capacity_id, schedule_id),
        json=data
    )
    assert response.status_code == 200


def test_delete_schedule():
    reponse = client.delete(
        "/api/Profiles/{0}/Capacities/{1}/Schedules/{2}/".format(profile_id, capacity_id, schedule_id),
    )
    delete_profile(profile_id)
    delete_cluster(cluster_id)
    delete_setting(setting_id)
    delete_capacity(profile_id, capacity_id)
    assert reponse.status_code == 204
    


