from prometheus_querybuilder import __version__
from prometheus_querybuilder.query import Query

import pytest


def test_version():
    assert __version__ == '0.1.0'


def test_query():
    """ Test query with only metric name """
    query = Query("http_requests_total")
    assert str(query) == "http_requests_total"


def test_query_with_label():
    query = Query("http_requests_total")
    query.add_label("environment", "production")
    assert str(query) == 'http_requests_total{environment="production"}'


def test_query_with_label_operators():
    query = Query("http_requests_total")
    query.add_label("environment", "production", "!=")
    assert str(query) == 'http_requests_total{environment!="production"}'


def test_query_with_unsupported_operator():
    query = Query("http_requests_total")
    with pytest.raises(ValueError):
        query.add_label("environment", "production", "!===")


def test_query_with_labels():
    query = Query("http_requests_total")
    query.add_label("environment", "production")
    query.add_label("method", "GET")
    assert str(query) == 'http_requests_total{environment="production",method="GET"}'


def test_query_with_label_change():
    query = Query("http_requests_total")
    query.add_label("environment", "production")
    query.add_label("environment", "stage")
    assert str(query) == 'http_requests_total{environment="stage"}'
