"""
warning: 
    this library is not a commercial product
        the author was bored, he worked with OpenData Mos 
            a library created out of boredom
"""

import requests

class OpenData:
    # Init func
    def __init__(self, token):
        self.token = token
        self.base_url = "https://apidata.mos.ru/v1/datasets/"
    """
    Get information by id (Dataset ID)
    """
    def get_info(self, id, top=None, skip=None, order_by="global_id"):
        url = self.base_url + f"{id}/rows?&api_key={self.token}&$order_by={order_by}"
        if top == None:
            pass
        else:
            url = url + f"&$top={top}"
        if skip == None:
            pass
        else:
            url = url + f"&$skip={skip}"
        return requests.get(url).json()

