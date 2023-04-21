from .base import BaseEndpoint


class PhotosSearchEndpoint(BaseEndpoint):
    api_path = 'v1/search'
    required_params = ['query']


class PhotoEndpoint(BaseEndpoint):
    api_path = 'v1/photos/{id}'


class CuratedPhotosEndpoint(BaseEndpoint):
    api_path = 'v1/curated'


class VideosSearchEndpoint(BaseEndpoint):
    api_path = 'videos/search'
    required_params = ['query']


class PopularVideosEndpoint(BaseEndpoint):
    api_path = 'videos/popular'


class VideoEndpoint(BaseEndpoint):
    api_path = 'videos/{id}'


class MyCollectionsEndpoint(BaseEndpoint):
    api_path = 'v1/collections'


class FeaturedCollectionsEndpoint(BaseEndpoint):
    api_path = 'v1/collections/featured'


class CollectionMediaEndpoint(BaseEndpoint):
    api_path = 'v1/collections/{id}'


class Pexels:

    @staticmethod
    def init(api_key):
        from . import Config
        Config.api_key = api_key

    def __init__(self, api_key=None) -> None:
        self.api_key = api_key or self._get_global_api_key()

        self.photo = PhotoEndpoint(self.api_key)
        self.photo_search = PhotosSearchEndpoint(self.api_key)
        self.curated_photos = CuratedPhotosEndpoint(self.api_key)

        self.video = VideoEndpoint(self.api_key)
        self.video_search = VideosSearchEndpoint(self.api_key)
        self.popular_videos = PopularVideosEndpoint(self.api_key)
        
        self.collection_media = CollectionMediaEndpoint(self.api_key)
        self.featured_collections = FeaturedCollectionsEndpoint(self.api_key)
        self.my_collections = MyCollectionsEndpoint(self.api_key)

    @classmethod
    def _get_global_api_key(cls):
        from . import Config
        return Config.api_key
