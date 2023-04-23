import abc
import os
import requests
import shutil

from typing import Any
from functools import partial
from .helpers import ListResourceRetriever


class AbstractResourceDownloader(abc.ABC):

    @abc.abstractmethod
    def download(self, where_to='./', **kwargs) -> None:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def _download_resource(self, url, dest_filename) -> None:
        raise NotImplementedError()


class ListResourceDowloader(AbstractResourceDownloader):

    def __init__(self, retriever: ListResourceRetriever) -> None:
        self._retriever = retriever

    def download(self, where_to='./', **kwargs) -> None:
        # create dest folder if not existing already
        dest_folder_exists = os.path.exists(where_to)
        if not dest_folder_exists:
            os.mkdir(where_to)

        _process = partial(self._process_resource, **kwargs)
        try:
            for filename, url in self._retriever.retrieve(_process):
                dest_file = os.path.join(where_to, filename)
                if os.path.exists(dest_file):
                    continue
                self._download_resource(url, dest_file)
        finally:
            # delete the folder if it didn't exist before
            if not dest_folder_exists:
                self._delete_folder_if_not_empty(where_to)

    @abc.abstractmethod
    def _process_resource(self, res_data, **kwargs) -> Any:
        raise NotImplementedError()

    def _download_resource(self, url, dest_filename) -> None:
        with requests.get(url, stream=True) as resp, open(dest_filename, 'wb') as file:
            shutil.copyfileobj(resp.raw, file)

    def _delete_folder_if_not_empty(self, folder_path) -> None:
        if not os.path.isfile(folder_path) and not len(os.listdir(folder_path)):
            os.remove(folder_path)


class ImageSearchDownloader(ListResourceDowloader):
    class Quality:
        MEDIUM = 'medium'
        ORIGINAL = 'original'
        LARGE2X = 'large2x'
        LARGE = 'large'
        SMALL = 'small'
        LANDSCAPE = 'landscape'
        PORTRAIT = 'tiny'

    def download(self, where_to='./', quality:Quality=Quality.ORIGINAL) -> None:
        return super().download(where_to, quality=quality)

    def _process_resource(self, res_data, **kwargs) -> Any:
        quality = kwargs.get('quality')
        image_url = res_data['src'][quality]
        filename = image_url.split('?')[0].split('/')[-1]
        return filename, image_url
