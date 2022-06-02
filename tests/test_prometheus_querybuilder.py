from prometheus_query_builder.query import Query
from prometheus_query_builder.label import Label, SUPPORTED_MATCH_OPERATORS

import pytest


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
    with pytest.raises(ValueError) as ex:
        query.add_label("environment", "production", "!===")
    assert "'match_operator' must be in ('=', '!=', '=~', '!~') (got '!===')" == ex.value.args[0]


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
    query = Query("http_requests_total", time_duration="5m")
    assert str(query) == 'http_requests_total[5m]'


def test_query_with_offset():
    query = Query("http_requests_total", offset="1w")
    assert str(query) == 'http_requests_total offset 1w'


def test_query_with_at_modifier():
    query = Query("http_requests_total", time_modifier="1609746000")
    assert str(query) == 'http_requests_total @ 1609746000'


def test_query_with_func():
    query = Query("http_requests_total", func="round")
    assert str(query) == 'round(http_requests_total)'


def test_query_with_all_options():
    query = Query(
        "http_requests_total", offset="1w", time_modifier="1609746000", time_duration="5m", func="abs"
    )
    query.add_label("environment", "production", "!=")
    assert str(query) == 'abs(http_requests_total{environment!="production"}[5m] offset 1w @ 1609746000)'


def test_query_with_mapped_labels():
    query = Query("http_requests_total")
    query.add_labels({"method": "GET", "status": ("done", "!=")})
    assert str(query) == 'http_requests_total{method="GET",status!="done"}'


def test_create_query_with_labels():
    query = Query("http_requests_total", labels={Label("method", "GET"), Label("status", "done", "!=")})
    assert str(query) == 'http_requests_total{method="GET",status!="done"}'


def test_create_label():
    for operator in SUPPORTED_MATCH_OPERATORS:
        label = Label("method", "GET", operator)
        assert str(label) == f"method{operator}\"GET\""
