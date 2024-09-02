# -*- coding: utf-8 -*-

"""
API Class
"""

__title__ = "societe.com-api"
__version__ = "1.0.0"
__author__ = "Loubna SEMLALI"

from requests import request
from json import dumps as jsonencode
from time import time
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode


class API(object):
    """
        This class provides methods to interact with the Societe.com API,
        allowing for GET requests to fetch company and executive data.
        It handles the construction of request URLs, manages authentication,
        and processes HTTP requests.
    """

    def __init__(self, token, version=1):
        self.url = "https://api.societe.com/api/v1"
        self.token = token

    def __get_url(self, endpoint):
        """ Get URL for requests """
        url = self.url
        if url.endswith("/") is False:
            url = f"{url}/"
        return f"{url}{endpoint}"

    def __request(self, method, endpoint, data, params=None, **kwargs):
        """ Do requests """
        if params is None:
            params = {}
        url = self.__get_url(endpoint)
        headers = {
            "X-Authorization": "socapi %s"%(self.token)
        }
        return request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            **kwargs
        )

    def get(self, endpoint, **kwargs):
        """ Get requests """
        return self.__request("GET", endpoint, None, **kwargs)
