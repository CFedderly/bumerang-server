from bumerang.db.borrowrequestrepo import BorrowRequestRepo
from bumerang.db.databasequery import DatabaseQuery
from bumerang.error import InvalidIDConstraintError
from bumerang.request.hydrator import Hydrator

from pytest import fixture as _fixture
from pytest import raises as _raises

from unittest.mock import Mock as _Mock
from unittest.mock import patch as _patch
from unittest.mock import sentinel as _s


@_fixture
def borrow_repo():
    return BorrowRequestRepo(_s.db, 'my_table')


@_patch.object(Hydrator, 'to_borrow_request', return_value=_s.borrow_request)
@_patch.object(Hydrator, '__init__', return_value=None)
@_patch.object(DatabaseQuery, 'select', return_value=[_s.record])
@_patch.object(DatabaseQuery, '__init__', return_value=None)
def test_find_one_by_id(
        db_query, select, hydrator,
        to_borrow_request, borrow_repo):
    """Test basic functionality"""
    res = borrow_repo.find_one_by_id(_s.id)

    db_query.assert_called_once_with(_s.db)
    (_, select_id_arg,) = select.call_args[0]
    assert select_id_arg.get('id') == _s.id, \
        'the query select was called with the wrong id'

    hydrator.assert_called_once_with(_s.record)

    assert res == _s.borrow_request, \
        'wrong return value, expected _s.id, got{}'.format(res)


@_patch.object(DatabaseQuery, 'select', return_value=[])
@_patch.object(DatabaseQuery, '__init__', return_value=None)
def test_find_one_by_id_returns_zero(db_query, select, borrow_repo):
    """Test that an empty result causes a zero result"""
    res = borrow_repo.find_one_by_id(_s.id)

    db_query.assert_called_once_with(_s.db)
    (_, select_id_arg,) = select.call_args[0]
    assert select_id_arg.get('id') == _s.id, \
        'the query select was called with the wrong id'

    assert res == None


@_patch.object(DatabaseQuery, 'select',
    return_value=[_s.record1,  _s.record2]
)
@_patch.object(DatabaseQuery, '__init__', return_value=None)
def test_find_one_by_id_raises_InvalidIDConstraintError(
        db_query, select, borrow_repo):
    """Test that multiple results raises an error"""
    with _raises(InvalidIDConstraintError):
        borrow_repo.find_one_by_id(_s.id)
