from bumerang.request.bumerangrequest import BumerangRequest
from unittest.mock import sentinel as _s
import pytest as _pytest


@_pytest.fixture
def bumerang_request():
    """The test request"""
    return BumerangRequest(
        title=_s.title,
        description=_s.description,
        distance=_s.distance,
        duration=_s.duration
    )


def test___repr__(bumerang_request):
    """A simple representation test of the request"""
    assert repr(bumerang_request) == (
            'BumerangRequest("sentinel.title", "sentinel.description", '
            'sentinel.distance, sentinel.duration)'
        ), 'The represenation of the bumerang request is incorrect'


def test_add_unique_tag(bumerang_request):
    """Test that adding tags to the request works as expected"""
    assert bumerang_request.tags == set(), \
        'The bumerang tag is not the emptyset after initialization'
    bumerang_request.add_tag(_s.tag_one)
    bumerang_request.add_tag(_s.tag_two)
    assert bumerang_request.tags == {_s.tag_one, _s.tag_two}, \
        'add_tag did not append the correct tag'


def test_remove_tag(bumerang_request):
    """Test that tags can be removed from the request structure"""
    bumerang_request.add_tag(_s.tag_one)
    bumerang_request.add_tag(_s.tag_two)
    assert bumerang_request.tags == {_s.tag_one, _s.tag_two}, \
        'Tag initialization failed through adding tags'

    bumerang_request.remove_tag(_s.tag_two)
    assert bumerang_request.tags == {_s.tag_one}, \
        'remove_tag did not remove the tag'
