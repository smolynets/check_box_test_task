from copy import deepcopy

from fastapi import status
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session
from main import app
from database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth import get_current_active_user


payment_data = {
    "pay_type": "cash",
    "amount": 1,
    "products": [
        {
        "name": "string",
        "price_per_unit": 1,
        "quantity": 1
        }
    ],
    "additional_data": {}
    }



@pytest.mark.parametrize("auth", [
    False, True,
])
def test_create_payment_success(client, create_test_user, auth):
    if auth:
        test_user = create_test_user
        app.dependency_overrides[get_current_active_user] = lambda: test_user
    token = "test-token"
    response = client.post(
        "payments/checks/",
        json=payment_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    if auth:
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["pay_type"] == "cash"
        assert data["amount"] == "1.00"
        assert len(data["products"]) == 1
        assert data["products"][0]["name"] == "string"
    else:
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_payment_fail(client, create_test_user):
    test_user = create_test_user
    app.dependency_overrides[get_current_active_user] = lambda: test_user
    token = "test-token"
    copied_payment_data = deepcopy(payment_data)
    copied_payment_data["products"][0]["weight"] = 1
    response = client.post(
        "payments/checks/",
        json=copied_payment_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "Value error, Select quantity or weight - not both of them."
