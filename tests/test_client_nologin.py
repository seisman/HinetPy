"""Tests with a non-login client."""

import pytest
from HinetPy import Client
from HinetPy.client import _parse_code


# http://docs.pytest.org/en/latest/fixture.html
# @pytest.fixture is better, but pytest prior 2.10 doesn't support
@pytest.yield_fixture(scope="module")
def client():
    client = Client()
    yield client


class TestClientOthersClass:
    def test_parse_code(self, client):
        assert _parse_code("0101") == ("01", "01", "0")
        assert _parse_code("0103A") == ("01", "03A", "0")
        assert _parse_code("010503") == ("01", "05", "010503")
        assert _parse_code("030201") == ("03", "02", "030201")

        with pytest.raises(ValueError):
            _parse_code("01013")

    def test_info(self, client):
        client.info()
        client.info("0101")

    def test_string(self, client):
        print(client)
