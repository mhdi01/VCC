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


def create_cluster(setting_id):
    global cluster_name
    cluster_name = "TestName_{0}".format(random.randrange(1,5000))
    
    data = {
        "name": cluster_name,
        "SeatType": "VCRoom",
        "MaxLimit": 10000,
        "DefaultFQDN": "string",
        "DefaultSettingId": setting_id,
        "Status": True
    }
    response = client.post(
        "/api/Clusters",
        json=data
    )
    global cluster_id 
    cluster_id = response.json()['id']
    return cluster_id


def delete_cluster(cluster_id):
    reponse = client.delete(
        "/api/Clusters/{0}".format(cluster_id)
    )


def create_profile():
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
    return profile_id


def delete_profile(profile_id):
    reponse = client.delete(
        "/api/Profiles/{0}".format(profile_id)
    )


def create_capacity(profile_id, cluster_id):
    data = {
        "SeatType": "VCRoom",
        "PlanType": "Volume",
        "CapacityLimit": 10000,
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
    capacity_id = response.json()['id']
    return capacity_id


def delete_capacity(profile_id, capacity_id):
   reponse = client.delete(
        "/api/Profiles/{0}/Capacities/{1}".format(profile_id, capacity_id)
    )
