from bumerang.error import InvalidRecordError
from bumerang.request.borrowrequest import BorrowRequest
from bumerang.request.hydrator import Hydrator

from mock import sentinel as _s
import pytest as _pytest


@_pytest.fixture
def hydrator():
    """Create our mock borrow request"""
    record = (_s.id, _s.title, _s.description, _s.distance, _s.duration,)
    return Hydrator(record)


def test_to_borrow_request(hydrator):
    """Check that the hyrator creates a BorrowRequest from the db record"""
    assert hydrator.to_borrow_request() == \
        BorrowRequest(
            _s.id, _s.title, _s.description,
            _s.distance, _s.duration
        ), 'A borrow request was not correctly created'


def test_to_borrow_request_throw_invalid_record_error():
    """Check that the borrow request will throw an invalid record error

       if a record with the wrong number of fields goes in
    """
    invalid_record = (_s.foo, _s.bar,)
    hydrator = Hydrator(invalid_record)
    with _pytest.raises(InvalidRecordError):
        hydrator.to_borrow_request()
