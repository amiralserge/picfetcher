
from .base import BaseEndpoint


class PhotoSearchEndpoint(BaseEndpoint):
    api_path = 'search'
    required_params = ['query']
