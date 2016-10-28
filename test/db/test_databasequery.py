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

    args, kw_args = _mutator_query.call_args
    expected_args = (args[0], args[1],)
    assert expected_args == params, '_mutator_query called with wrong args'
    assert database_query._db.cursor.close.call_count == 1, \
        'close has the wrong number of calls'


@_patch.object(
    DatabaseQuery,
    '_mutator_query',
    side_effect=DatabaseError('foo')
)
def test_create_table_throws_invalid_query_error(
        _mutator_query, database_query):
    """Test that a database error throws an invalid query error"""
    with _raises(InvalidQueryError):
        database_query.create_table(_s.query)

    assert database_query._db.cursor.close.call_count == 1, \
        'close has the wrong number of calls'

    assert database_query._db.rollback.call_count == 1, \
        'rollback has the wrong number of calls'


@_mark.parametrize('input, params', [
    ((_s.query,), (_s.query, None,)),
    ((_s.query, _s.params,), (_s.query, _s.params))
])
@_patch.object(DatabaseQuery, '_mutator_query')
def test_insert(_mutator_query, input, params, database_query):
    """Test basic insert functionality"""
    assert database_query.insert(*input) == _s.record, \
        'Insert has wrong record value'

    args, kw_args = _mutator_query.call_args
    expected_args = (args[0], args[1],)
    assert expected_args == params, '_mutator called with wrong args'
    assert database_query._db.cursor.close.call_count == 1, \
        'close has the wrong number of calls'


@_patch.object(
    DatabaseQuery,
    '_mutator_query',
    side_effect=DatabaseError('foo')
)
def test_insert_throws_invalid_query_error(_mutator_query, database_query):
    """Test that on a DatabaseError, an InvalidQueryError is thrown."""
    with _raises(InvalidQueryError):
        database_query.insert(_s.query)

    assert database_query._db.cursor.close.call_count == 1, \
        'close has the wrong number of calls'

    assert database_query._db.rollback.call_count == 1, \
        'rollback has the wrong number of calls'


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


def test__mutator_query(database_query):
    """Test basic functionality of the mutator query."""
    cur = _mock(name='cur')
    database_query._mutator_query(_s.query, _s.params, cur)

    cur.execute.assert_called_once_with(_s.query, _s.params)
    assert database_query._db.commit.call_count == 1, \
        'commit has the wrong number of calls'


def test__mutator_query_throws_database_error(database_query):
    """Test that the method throws the Database error if the query raises

       one.
    """
    cur = _mock(name='cur', execute=_mock(side_effect=DatabaseError('foo')))
    with _raises(DatabaseError):
        database_query._mutator_query(_s.query, _s.params, cur)
