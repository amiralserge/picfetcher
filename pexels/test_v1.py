import uuid

from .v1 import Pexels


class TestPexelsClass:

    def test_get_global_api_key(self):
        api_key = uuid.uuid4().hex
        Pexels.init(api_key=api_key)
        assert Pexels._get_global_api_key() == api_key
    
    def test__init__(self):
        api_key1 = uuid.uuid4().hex
        api_key2 = uuid.uuid4().hex

        endpoints = ['collection_media', 'curated_photos', 'featured_collections', 'my_collections', 
                'photo', 'photo_search', 'popular_videos', 'video', 'video_search']

        Pexels.init(api_key=api_key1)
        instance1 = Pexels()
        instance2 = Pexels(api_key=api_key2)


        for endpoint in endpoints:
            assert getattr(instance1, endpoint).api_key == api_key1
            assert getattr(instance2, endpoint).api_key == api_key2
