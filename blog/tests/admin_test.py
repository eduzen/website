# from .factories import DataCollectorFactory


def test_root_admin(rf, admin_client):
    response = admin_client.get("/eduardo")
    assert response.status_code == 200


# def test_datacollectors_admin(rf, admin_client):
#     response = admin_client.get("/datacollectors/datacollector/")
#     assert response.status_code == 200


# def test_datacollectors_admin__add(rf, admin_client):
#     response = admin_client.get("/datacollectors/datacollector/add/")
#     assert response.status_code == 200


# def test_datacollectors_admin__get(rf, admin_client):
#     data_collector = DataCollectorFactory.create()
#     response = admin_client.get(f"/datacollectors/datacollector/{data_collector.pk}/change/")
#     assert response.status_code == 200
