from clients.models import Client


def test_get_clients(client, db, bake_clients):
    client_num = 10
    bake_clients(client_num)

    response = client.get("/api/clients/")
    assert response.status_code == 200
    response_json = response.json()

    assert len(response_json) == client_num
    for i, response_client in enumerate(response_json):
        assert response_client["personal_tax_number"] == i
        assert response_client["account"] == 100


def test_pay_from_client(client, db, bake_clients):
    client_num = 4
    bake_clients(client_num)

    from_ptn = 0
    to_ptn = [1, 2, 3]
    amount = 30.30
    response = client.post(
        "/api/clients/transact",
        data={"from_ptn": from_ptn, "to_ptn": to_ptn, "amount": amount},
    )
    assert response.status_code == 200
    response_json = response.json()

    assert response_json[from_ptn]["personal_tax_number"] == 0
    assert response_json[from_ptn]["account"] == 100 - amount

    for i in to_ptn:
        assert response_json[i]["personal_tax_number"] == i
        assert response_json[i]["account"] == 100 + amount/len(to_ptn)


def test_pay_from_client_round(client, db, bake_clients):
    client_num = 4
    bake_clients(client_num)

    from_ptn = 0
    to_ptn = [1, 2, 3]
    amount = 10
    response = client.post(
        "/api/clients/transact",
        data={"from_ptn": from_ptn, "to_ptn": to_ptn, "amount": amount},
    )
    assert response.status_code == 200
    response_json = response.json()

    assert response_json[from_ptn]["personal_tax_number"] == 0
    assert response_json[from_ptn]["account"] == 100 - 9.99

    for i in to_ptn:
        assert response_json[i]["personal_tax_number"] == i
        assert response_json[i]["account"] == 100 + 3.33
