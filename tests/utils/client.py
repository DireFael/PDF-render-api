#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests

API_SERVER = os.environ.get('CONF_API_ADDRESS', "http://localhost:5000/")

class APIClient:

    def __init__(self):

        self.address = API_SERVER

    def _get_url(self, module):

        return f"{self.address}{module}"

    def post(self, module, data=None):

        url = self._get_url(module)

        response = requests.post(url=url, files=data, verify=False).json()

        return response

    def get(self, module):

        url = self._get_url(module)

        response = requests.get(url=url).json()

        return response
    
    def get_file(self, module):

        url = self._get_url(module)

        response = requests.get(url=url, stream=True)
        
        return {"status_code": response.status_code, "status_message": response.reason}