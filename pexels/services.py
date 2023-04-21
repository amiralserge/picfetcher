import abc
import os
import requests
import shutil

from typing import Any
from .helpers import ResourceRetriever


class BaseResourceDowloader(abc.ABC):

    def __init__(self, retriever: ResourceRetriever) -> None:
        self._retriever = retriever

    def download(self, where_to='./') -> None:
        # create dest folder if not existing already
        dest_folder_exists = os.path.exists(where_to)
        if not dest_folder_exists:
            os.mkdir(where_to)

        try:
            for filename, url in self._retriever.retrieve(self._process_resource):
                if os.path.exists(filename):
                    continue
                self._download_resource(url, filename)
        finally:
            # delete the folder if it didn't exist before
            if not dest_folder_exists:
                self._delete_folder_if_not_empty(where_to)

    @abc.abstractmethod
    def _process_resource(self, res_data) -> Any:
        raise NotImplementedError()

    def _donwload_resource(self, url, dest_filename) -> None:
        with requests.get(url, stream=True) as resp, open(dest_filename, 'wb') as file:
            shutil.copyfileobj(resp.raw, file)

    def _delete_folder_if_not_empty(self, folder_path) -> None:
        if not os.path.isfile(folder_path) and not len(os.listdir(folder_path)):
            os.remove(folder_path)
