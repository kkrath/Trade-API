from pytest import fail

from tests.helpers import json_of_response


def test_create_trade(client, app):
    trade_params = dict(
        type="buy",
        user_id=1,
        symbol="USD",
        shares=30,
        price=90,
        timestamp=1531522701000
    )

    response = client.post("/trades", json=trade_params)
    assert response.status_code == 201
    assert json_of_response(response) == dict(id=1, **trade_params)

    response = client.get("/trades")
    assert json_of_response(response) == [dict(id=1, **trade_params)]


def test_create_trade_error_when_type_is_invalid(client, app):
    trade_params = dict(
        type="INVALID",
        user_id=1,
        symbol="USD",
        shares=30,
        price=90,
        timestamp=1531522701000
    )

    response = client.post("/trades", json=trade_params)
    assert response.status_code == 400

    response = client.get("/trades")
    assert json_of_response(response) == []


def test_create_trade_error_when_shares_is_more_than_100(client, app):
    trade_params = dict(
        type="buy",
        user_id=1,
        symbol="USD",
        shares=101,
        price=90,
        timestamp=1531522701000
    )

    response = client.post("/trades", json=trade_params)
    assert response.status_code == 400

    response = client.get("/trades")
    assert json_of_response(response) == []


def test_create_trade_error_when_shares_is_less_than_0(client, app):
    trade_params = dict(
        type="buy",
        user_id=1,
        symbol="USD",
        shares=-1,
        price=90,
        timestamp=1531522701000
    )

    response = client.post("/trades", json=trade_params)
    assert response.status_code == 400

    response = client.get("/trades")
    assert json_of_response(response) == []


def test_all_trades_returns_all_trades_json_ordered_by_id(client, app):
    trades_params = [
        dict(
            type="buy",
            user_id=1,
            symbol="USD",
            shares=30,
            price=90,
            timestamp=1531522701000
        ),
        dict(
            type="sell",
            user_id=2,
            symbol="EUR",
            shares=40,
            price=95,
            timestamp=1531522701001
        )
    ]

    for trade_params in trades_params:
        response = client.post("/trades", json=trade_params)

        if response.status_code != 201:
            fail('POST /trades is not implemented')

    response = client.get("/trades")

    expected = [dict(id=index, **trade_params) for index, trade_params in enumerate(trades_params, start=1)]

    assert response.status_code == 200
    assert json_of_response(response) == expected


def test_all_trades_filtered_by_type(client, app):
    trades_params = [
        dict(
            type="buy",
            user_id=1,
            symbol="USD",
            shares=30,
            price=90,
            timestamp=1531522701000
        ),
        dict(
            type="sell",
            user_id=2,
            symbol="EUR",
            shares=40,
            price=95,
            timestamp=1531522701001
        )
    ]

    for trade_params in trades_params:
        response = client.post("/trades", json=trade_params)

        if response.status_code != 201:
            fail('POST /trades is not implemented')

    response = client.get("/trades?type=buy")

    expected = [dict(id=1, **trades_params[0])]

    assert response.status_code == 200
    assert json_of_response(response) == expected


def test_all_trades_filtered_by_user_id(client, app):
    trades_params = [
        dict(
            type="buy",
            user_id=1,
            symbol="USD",
            shares=30,
            price=90,
            timestamp=1531522701000
        ),
        dict(
            type="sell",
            user_id=2,
            symbol="EUR",
            shares=40,
            price=95,
            timestamp=1531522701001
        )
    ]

    for trade_params in trades_params:
        response = client.post("/trades", json=trade_params)

        if response.status_code != 201:
            fail('POST /trades is not implemented')

    response = client.get("/trades?user_id=2")

    expected = [dict(id=2, **trades_params[1])]

    assert response.status_code == 200
    assert json_of_response(response) == expected


def test_all_trades_returns_empty_list_when_no_trades_in_database(client, app):
    response = client.get("/trades")
    assert response.status_code == 200
    assert json_of_response(response) == []


def test_get_trade_returns_trade_json_when_exists(client, app):
    trade_params = dict(
        type="buy",
        user_id=25,
        symbol="USD",
        shares=15,
        price=250,
        timestamp=1531522702301
    )

    post_response = client.post("/trades", json=trade_params)

    if post_response.status_code != 201:
        fail('POST /trades is not implemented')

    get_response = client.get(f"/trades/{json_of_response(post_response).get('id')}")

    expected = dict(id=1, **trade_params)
    assert get_response.status_code == 200
    assert json_of_response(get_response) == expected


def test_get_trade_returns_status_404_when_does_not_exist(client, app):
    trade_params = dict(
        type="buy",
        user_id=25,
        symbol="USD",
        shares=15,
        price=250,
        timestamp=1531522702301
    )

    post_response = client.post("/trades", json=trade_params)

    if post_response.status_code != 201:
        fail('POST /trades is not implemented')

    response = client.get(f"/trades/999")
    assert response.status_code == 404


def test_patch_trade_returns_status_405(client, app):
    trade_params = dict(
        type="buy",
        user_id=25,
        symbol="USD",
        shares=15,
        price=250,
        timestamp=1531522702301
    )

    post_response = client.post("/trades", json=trade_params)

    if post_response.status_code != 201:
        fail('POST /trades is not implemented')

    response = client.patch(f"/trades/{json_of_response(post_response).get('id')}")
    assert response.status_code == 405


def test_put_trade_returns_status_405(client, app):
    trade_params = dict(
        type="buy",
        user_id=25,
        symbol="USD",
        shares=15,
        price=250,
        timestamp=1531522702301
    )

    post_response = client.post("/trades", json=trade_params)

    if post_response.status_code != 201:
        fail('POST /trades is not implemented')

    response = client.put(f"/trades/{json_of_response(post_response).get('id')}")
    assert response.status_code == 405


def test_delete_trade_returns_status_405(client, app):
    trade_params = dict(
        type="buy",
        user_id=25,
        symbol="USD",
        shares=15,
        price=250,
        timestamp=1531522702301
    )

    post_response = client.post("/trades", json=trade_params)

    if post_response.status_code != 201:
        fail('POST /trades is not implemented')

    response = client.delete(f"/trades/{json_of_response(post_response).get('id')}")
    assert response.status_code == 405
