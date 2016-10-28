from bumerang.request.borrowrequest import BorrowRequest
from unittest.mock import sentinel as _s
import pytest as _pytest


@_pytest.fixture
def borrow_request():
    """The test request"""
    return BorrowRequest(
        id=_s.id,
        title=_s.title,
        description=_s.description,
        distance=_s.distance,
        duration=_s.duration
    )


def test___eq__(borrow_request):
    """Test two objects that are equal"""
    assert borrow_request == \
        BorrowRequest(
            _s.id,
            _s.title,
            _s.description,
            _s.distance,
            _s.duration
        )


def test_not__eq__(borrow_request):
    """Test two objects that are not equal"""
    assert borrow_request != \
        BorrowRequest(
            _s.new_id,
            _s.new_title,
            _s.new_description,
            _s.new_distance,
            _s.new_duration
        )


def test___repr__(borrow_request):
    """A simple representation test of the request"""
    assert repr(borrow_request) == (
            'BorrowRequest("sentinel.title", "sentinel.description", '
            'sentinel.distance, sentinel.duration)'
        ), 'The represenation of the bumerang request is incorrect'


def test__to_node_(borrow_request):
    """To node"""
    assert borrow_request.to_node() == {
        'request': {
            'id': _s.id,
            'title': _s.title,
            'description': _s.description,
            'distance': _s.distance,
            'duration': _s.duration,
            'tags': []
        }
    }, 'to_node is not producing the correct output'


def test_add_unique_tag(borrow_request):
    """Test that adding tags to the request works as expected"""
    assert borrow_request.tags == set(), \
        'The bumerang tag is not the emptyset after initialization'
    borrow_request.add_tag(_s.tag_one)
    borrow_request.add_tag(_s.tag_two)
    assert borrow_request.tags == {_s.tag_one, _s.tag_two}, \
        'add_tag did not append the correct tag'


def test_remove_tag(borrow_request):
    """Test that tags can be removed from the request structure"""
    borrow_request.add_tag(_s.tag_one)
    borrow_request.add_tag(_s.tag_two)
    assert borrow_request.tags == {_s.tag_one, _s.tag_two}, \
        'Tag initialization failed through adding tags'

    borrow_request.remove_tag(_s.tag_two)
    assert borrow_request.tags == {_s.tag_one}, \
        'remove_tag did not remove the tag'
