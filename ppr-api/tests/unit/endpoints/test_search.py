import datetime

import fastapi
import pytest

import endpoints.search
import models.financing_statement
import models.search


def test_read_search_returns_value():
    search_record = models.search.Search(id=27, type_code='REGISTRATION_NUMBER', criteria={
                                         'value': '1234'}, creation_date_time=datetime.datetime.now())
    repo = MockSearchRepository(search_record)
    actual = endpoints.search.read_search(27, repo)

    assert search_record == actual


def test_read_search_not_found():
    repo = MockSearchRepository(None)
    try:
        endpoints.search.read_search(27, repo)
    except fastapi.HTTPException as ex:
        assert ex.status_code == 404
    else:
        pytest.fail('A Not Found error was expected')


def test_read_search_results_not_found():
    repo = MockSearchRepository(None)
    try:
        endpoints.search.read_search_results(27, repo)
    except fastapi.HTTPException as ex:
        assert ex.status_code == 404
    else:
        pytest.fail('A Not Found error was expected')


def test_read_search_results_is_empty():
    search_record = models.search.Search(results=[])
    repo = MockSearchRepository(search_record)

    results = endpoints.search.read_search_results(27, repo)
    assert results == []


def test_read_search_results_has_exact_match():
    stub_fin_stmt = stub_financing_statement_event('123456A')
    search_record = models.search.Search(results=[models.search.SearchResult(exact=True, selected=True,
                                                                             registration_number='123456A',
                                                                             financing_statement_event=stub_fin_stmt)])
    repo = MockSearchRepository(search_record)

    results = endpoints.search.read_search_results(27, repo)
    assert len(results) == 1
    assert results[0].type == 'EXACT'


def test_read_search_results_has_inexact_match():
    stub_fin_stmt = stub_financing_statement_event('123456A')
    search_record = models.search.Search(results=[models.search.SearchResult(exact=False, selected=True,
                                                                             registration_number='123456A',
                                                                             financing_statement_event=stub_fin_stmt)])
    repo = MockSearchRepository(search_record)

    results = endpoints.search.read_search_results(27, repo)
    assert len(results) == 1
    assert results[0].type == 'SIMILAR'


def stub_financing_statement_event(reg_number: str):
    return models.financing_statement.FinancingStatementEvent(
        registration_number=reg_number, base_registration_number=reg_number, document_number='A1234567',
        registration_date=datetime.datetime.now(), base_registration=models.financing_statement.FinancingStatement(
            registration_number='123456A', registration_type_code='SA'
        )
    )


class MockSearchRepository:
    def __init__(self, search_result):
        self.search = search_result

    def get_search(self, search_id: int):
        return self.search
