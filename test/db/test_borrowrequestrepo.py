from bumerang.db.borrowrequestrepo import BorrowRequestRepo
from bumerang.db.databasequery import DatabaseQuery
from bumerang.request.hydrator import Hydrator

from pytest import fixture as _fixture

from unittest.mock import patch as _patch
from unittest.mock import sentinel as _s


@_fixture
def borrow_repo():
    return BorrowRequestRepo(_s.db, 'my_table')


@_patch.object(Hydrator, 'to_borrow_request', return_value=_s.borrow_request)
@_patch.object(DatabaseQuery, 'select', return_value=[(_s.id,)])
@_patch.object(DatabaseQuery, '__init__', return_value=None)
def test_find_one_by_id(db_query, select, to_borrow_request, borrow_repo):
    res = borrow_repo.find_one_by_id(_s.id)

    db_query.assert_called_once_with(_s.db)
    to_borrow_request.call_count == 1, 'wrong amount of calls'

    (_, select_id_arg,) = select.call_args[0]
    assert select_id_arg.get('id') == _s.id, \
        'the query select returned the wrong result'

    assert res == _s.borrow_request, \
        'wrong return value, expected _s.id, got{}'.format(res)
