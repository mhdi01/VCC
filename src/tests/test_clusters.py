import random
from .config import client
from .tools import create_setting, delete_setting


setting_id = create_setting()

def test_create_cluster():
    global cluster_name
    cluster_name = "TestName_{0}".format(random.randrange(1,5000))
    
    data = {
        "name": cluster_name,
        "SeatType": "VCRoom",
        "MaxLimit": 7,
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
    assert response.status_code == 200
    assert response.json()['name'] == cluster_name


def test_get_clusters():
    response = client.get(
        "/api/Clusters"
    )
    assert response.status_code == 200


def test_retrieve_cluster():
    response = client.get(
        "/api/Clusters/{0}".format(cluster_id)
    )
    assert response.status_code == 200
    assert response.json()['name'] == cluster_name


def test_update_cluster():
    global cluster_name
    cluster_name = "TestName_{0}".format(random.randrange(1,5000))
    data = {
        "name": cluster_name,
        "SeatType": "VCRoom",
        "MaxLimit": 7,
        "DefaultFQDN": "string",
        "DefaultSettingId": setting_id,
        "Status": True
    }
    response = client.put(
        "/api/Clusters/{0}".format(cluster_id),
        json=data
    )
    assert response.status_code == 200
    assert response.json()['name'] == cluster_name


def test_update_cluster_partial():
    global cluster_name
    cluster_name = "TestName_{0}".format(random.randrange(1,5000))
    data = {
        'name': cluster_name
    }
    response = client.patch(
        "/api/Clusters/{0}".format(cluster_id),
        json=data
    )
    assert response.status_code == 200
    assert response.json()['name'] == cluster_name


def test_delete_cluster():
    reponse = client.delete(
        "/api/Clusters/{0}".format(cluster_id)
    )
    delete_setting(setting_id)
    assert reponse.status_code == 204
    


