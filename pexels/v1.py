from .base import BaseEndpoint


class PhotosSearchEndpoint(BaseEndpoint):
    api_path = 'v1/search'
    required_params = ['query']


class PhotoEndpoint(BaseEndpoint):
    api_path = 'v1/photos/{id}'


class CuratedPhotosEndpoint(BaseEndpoint):
    api_path = 'v1/curated'


class VideosSearchEndpoint(BaseEndpoint):
    api_path = 'v1/videos/search'
    required_params = ['query']


class PopularVideosEndpoint(BaseEndpoint):
    api_path = 'v1/videos/popular'


class VideoEndpoint(BaseEndpoint):
    api_path = 'v1/videos/{id}'


class MyCollectionsEndpoint(BaseEndpoint):
    api_path = 'v1/collections'


class FeaturedCollectionsEndpoint(BaseEndpoint):
    api_path = 'v1/collections/featured'


class CollectionMediaEndpoint(BaseEndpoint):
    api_path = 'v1/collections/{id}'
