import pytest


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


@pytest.mark.parametrize(
    "amount, expected",
    (
        (30.30, (100 - 30.30, 100 + 10.10)),
        (10., (100 - 9.99, 100 + 3.33)),
    ),
)
def test_pay_from_client(client, db, bake_clients, amount, expected):
    client_num = 4
    bake_clients(client_num)

    from_ptn = 0
    to_ptn = [1, 2, 3]
    response = client.post(
        "/api/clients/transact",
        data={
            "from_ptn": from_ptn,
            "to_ptn": ",".join(map(str, to_ptn)),
            "amount": amount,
        },
    )
    assert response.status_code == 200
    response_json = response.json()

    donor_result_account, recipient_result_account = expected
    assert response_json[from_ptn]["personal_tax_number"] == 0
    assert response_json[from_ptn]["account"] == donor_result_account

    for i in to_ptn:
        assert response_json[i]["personal_tax_number"] == i
        assert response_json[i]["account"] == recipient_result_account
