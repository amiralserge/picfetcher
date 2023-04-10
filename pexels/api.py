from .base import BaseEndpoint


class PhotosSearchEndpoint(BaseEndpoint):
    api_path = 'search'
    required_params = ['query']


class PhotoEndpoint(BaseEndpoint):
    api_path = 'photos/{id}'


class CuratedPhotosEndpoint(BaseEndpoint):
    api_path = 'curated'


class VideosSearchEndpoint(BaseEndpoint):
    api_path = 'videos/search'
    required_params = ['query']


class PopularVideosEndpoint(BaseEndpoint):
    api_path = 'videos/popular'


class VideoEndpoint(BaseEndpoint):
    api_path = 'videos/{id}'


class MyCollectionsEndpoint(BaseEndpoint):
    api_path = 'collections'


class FeaturedCollectionsEndpoint(BaseEndpoint):
    api_path = 'collections/featured'


class CollectionMediaEndpoint(BaseEndpoint):
    api_path = 'collections/{id}'
