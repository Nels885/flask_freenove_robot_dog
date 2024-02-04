from flask import url_for


def test_conf_global(client):
    for url in ["/conf/all/", url_for("main.all")]:
        response = client.get(url)
        assert b"- Global config</title>" in response.data
        assert response.status_code == 200


def test_conf_network(client):
    for url in ["/conf/network/", url_for("main.network")]:
        response = client.get("/conf/network/")
        assert b"- Network config</title>" in response.data
        assert response.status_code == 200
