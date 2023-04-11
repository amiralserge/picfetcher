from . import v1


class __Config:
    __api_key = None

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, val):
        self.__api_key = val

Config = __Config()
