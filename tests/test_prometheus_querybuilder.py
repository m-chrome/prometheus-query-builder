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


def test_query_with_label_update():
    query = Query("http_requests_total")
    query.add_label("environment", "production")
    query.add_label("environment", "stage")
    assert str(query) == 'http_requests_total{environment="stage"}'


def test_query_remove_label():
    query = Query("http_requests_total")
    query.add_label("environment", "production")
    assert len(query.labels) == 1
    query.remove_label("environment")
    assert len(query.labels) == 0


def test_query_with_time_duration():
    query = Query("http_requests_total")
    query.add_label("environment", "production")
    query.add_time_duration("5m")
    assert str(query) == 'http_requests_total{environment="production"}[5m]'


def test_query_with_offset():
    query = Query("http_requests_total")
    query.add_offset("5m")
    assert str(query) == 'http_requests_total offset 5m'


def test_query_with_at_modifier():
    query = Query("http_requests_total")
    query.add_at_modifier("1609746000")
    assert str(query) == 'http_requests_total @ 1609746000'


def test_query_with_time_modifiers():
    query = Query("http_requests_total")
    query.add_offset("5m")
    query.add_at_modifier("1609746000")
    assert str(query) == 'http_requests_total offset 5m @ 1609746000'
