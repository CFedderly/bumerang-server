from bumerang.db.databasequery import DatabaseQuery
from bumerang.error import InvalidQueryError

from psycopg2 import DatabaseError

from pytest import fixture as _fixture
from pytest import mark as _mark
from pytest import raises as _raises

from unittest.mock import Mock as _mock
from unittest.mock import patch as _patch
from unittest.mock import sentinel as _s


@_fixture
def database_query():
    db_mock = _mock(name='db')
    db_mock.cursor = _mock
    db_mock.cursor.close = _mock(name='close')
    db_mock.cursor.execute = _mock(name='execute')
    db_mock.cursor.fetchall = _mock(name='fetch_all', return_value=_s.records)
    db_mock.cursor.fetchone = _mock(name='fetch_one', return_value=_s.record)
    db_mock.rollback = _mock(name='rollback')
    return DatabaseQuery(db_mock)


@_mark.parametrize('input, params', [
    ((_s.query,), (_s.query, None,)),
    ((_s.query, _s.params,), (_s.query, _s.params))
])
@_patch.object(DatabaseQuery, '_mutator_query')
def test_create_table(_mutator_query, input, params, database_query):
    """Test basic functionality of creating tables"""
    database_query.create_table(*input)
    _mutator_query.assert_called_once_with(
        *params,
        return_value=False
    )


@_mark.parametrize('input, params', [
    ((_s.query,), (_s.query, None,)),
    ((_s.query, _s.params,), (_s.query, _s.params))
])
@_patch.object(DatabaseQuery, '_mutator_query')
def test_insert(_mutator_query, input, params, database_query):
    """Test basic insert functionality"""
    database_query.insert(*input)
    _mutator_query.assert_called_once_with(
        *params,
        return_value=True
    )


@_mark.parametrize('input, params', [
    ((_s.query,), (_s.query, None,)),
    ((_s.query, _s.params,), (_s.query, _s.params))
])
def test_select(input, params, database_query):
    """Test basic select functioanlity"""
    assert database_query.select(*input) == _s.records, \
        'Incorrect return value'

    assert database_query._db.cursor.close.call_count == 1, \
        'close has the wrong number of calls'
    database_query._db.cursor.execute.assert_called_once_with(*params)


def test_select_raises_invalid_query_error(database_query):
    """Test that select will raise and invalid query error"""
    database_query._db.cursor.execute.side_effect = DatabaseError('foo')
    with _raises(InvalidQueryError):
        database_query.select(_s.query)


@_mark.skip(reason='Waiting for the refactor')
def test__mutator_query(database_query):
    """Test basic functionality of the mutator query."""
    cur = _mock(name='cur')
    database_query._mutator_query(_s.query, _s.params, cur)

    cur.execute.assert_called_once_with(_s.query, _s.params)
    assert database_query._db.commit.call_count == 1, \
        'commit has the wrong number of calls'


@_mark.skip(reason='Waiting for the refactor')
def test__mutator_query_throws_database_error(database_query):
    """Test that the method throws the Database error if the query raises

       one.
    """
    with _raises(DatabaseError):
        database_query._mutator_query(_s.query, _s.params, cur)
