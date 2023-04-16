import pytest
from unittest import mock

from ..helpers import ResourceRetriever
from ..base import BaseEndpoint


class TestReourceRetriever:

    PAGE_1 = dict(
        page=1, 
        per_page=1, 
        photos=[dict(src=dict(original='http://a.pic/page1-photo-1.jpeg'))],
        next_page='http://a.pic/search/?page=2&per_page=1&query=tomato'
    )

    PAGE_2 = dict(
        page=2, 
        per_page=1, 
        photos=[dict(src=dict(original='http://a.pic/page2-photo-2.jpeg'))],
        next_page='http://a.pic/search/?page=3&per_page=1&query=tomato'
    )

    PAGE_3 = dict(
        page=3, 
        per_page=1, 
        photos=[dict(src=dict(original='http://a.pic/page3-photo-3.jpeg'))],
        next_page=None
    )

    @pytest.mark.parametrize('params,endpoint_return,expected_result', [
        (dict(query='tomato'), [PAGE_1, PAGE_2, PAGE_3], ['http://a.pic/page1-photo-1.jpeg', 
                                                          'http://a.pic/page2-photo-2.jpeg', 
                                                          'http://a.pic/page3-photo-3.jpeg']),
        (dict(query='tomato', max=2), [PAGE_1, PAGE_2],['http://a.pic/page1-photo-1.jpeg', 
                                                        'http://a.pic/page2-photo-2.jpeg']),
        (dict(query='tomato', max=1), [PAGE_1],['http://a.pic/page1-photo-1.jpeg'])
    ]) 
    def test_retrieve(self, params, endpoint_return, expected_result):
        with mock.patch.object(ResourceRetriever, '_fetch') as _fetch_mock:
            _fetch_mock.side_effect = endpoint_return
            endpoint = BaseEndpoint(api_key=None)
            _process = lambda data: data.get('src').get('original')
            
            result = list(
                ResourceRetriever(endpoint, 'photos').retrieve(params=params, processing_method=_process)
            )
            assert result == expected_result

        