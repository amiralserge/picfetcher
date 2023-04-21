import os

from .helpers import ResourceRetriever


class BaseResourceDowloader:

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

    def _process_resource(self, res_data) -> Any:
        pass

    def _donwload_resource(self, url, dest_filename):
        pass

    def _delete_folder_if_not_empty(self, folder_path):
        pass
    