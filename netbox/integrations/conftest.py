from os import environ

import pytest
import pynetbox

@pytest.fixture(scope="session")
def nb():
    url = "http://localhost:8000"
    # load the token from env var
    token = environ.get("NETBOX_TEST_API_TOKEN")
    client = pynetbox.api(url, token=token)
    return client