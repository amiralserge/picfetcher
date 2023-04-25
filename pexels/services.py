import abc
import os
import shutil
from functools import partial
from typing import Any, Tuple

import requests

from .helpers import AbstractResourceRetriever, ListResourceRetriever


class AbstractResourceDownloader(abc.ABC):

    def __init__(self, retriever: AbstractResourceRetriever) -> None:
        self._retiever = retriever

    @abc.abstractmethod
    def download(self, retriever_params, where_to='./', **kwargs) -> None:
        raise NotImplementedError()
    
    def _download_resource(self, url, dest_filename) -> None:
        with requests.get(url, stream=True) as resp, open(dest_filename, 'wb') as file:
            shutil.copyfileobj(resp.raw, file)

    @abc.abstractmethod
    def _process_resource(self, res_data, **kwargs) -> Tuple[str, str]:
        raise NotImplementedError()
 

class SingleResourceDownloader(AbstractResourceDownloader):
    
    def download(self, retriever_params, where_to='./', **kwargs) -> None:
        _process = partial(self._process_resource, **kwargs)
        # create dest folder if not existing already
        dest_folder_exists = os.path.exists(where_to)
        if not dest_folder_exists:
            os.mkdir(where_to)
        
        try:
            filename, url = self._retiever.retrieve(retriever_params, _process)
            dest_file = os.path.join(where_to, filename)
            if not os.path.exists(dest_file):
                self._download_resource(url, dest_file)
        finally:
            # delete the folder if it didn't exist before
            if not dest_folder_exists:
                self._delete_folder_if_not_empty(where_to)

    def _delete_folder_if_not_empty(self, folder_path) -> None:
        if not os.path.isfile(folder_path) and not len(os.listdir(folder_path)):
            os.remove(folder_path)


class ListResourceDowloader(AbstractResourceDownloader):

    def __init__(self, retriever: ListResourceRetriever) -> None:
        self._retriever = retriever

    def download(self, retriever_params, where_to='./', **kwargs) -> None:
        # create dest folder if not existing already
        dest_folder_exists = os.path.exists(where_to)
        if not dest_folder_exists:
            os.mkdir(where_to)

        _process = partial(self._process_resource, **kwargs)
        try:
            for filename, url in self._retriever.retrieve(retriever_params, _process):
                dest_file = os.path.join(where_to, filename)
                if os.path.exists(dest_file):
                    continue
                self._download_resource(url, dest_file)
        finally:
            # delete the folder if it didn't exist before
            if not dest_folder_exists:
                self._delete_folder_if_not_empty(where_to)

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

    def download(self, retriever_params, where_to='./', quality:Quality=Quality.ORIGINAL) -> None:
        return super().download(retriever_params, where_to, quality=quality)

    def _process_resource(self, res_data, **kwargs) -> Any:
        quality = kwargs.get('quality')
        image_url = res_data['src'][quality]
        filename = image_url.split('?')[0].split('/')[-1]
        return filename, image_url
