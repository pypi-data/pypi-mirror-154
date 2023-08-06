#
# python library cleos
#
import requests


class DynamicUrl:
    # def __init__(self, url='http://localhost:8888', version='v1', cache=None) :
    def __init__(self, url='http://localhost:8888', version='v1', cache=None):
        self._cache = cache or []
        self._baseurl = url
        self._version = version

    def __getattr__(self, name):
        return self._(name)

    def __del__(self):
        pass

    def _(self, name):
        return DynamicUrl(url=self._baseurl, version=self._version, cache=self._cache + [name])

    def method(self):
        return self._cache

    def create_url(self):
        url_str = '{0}/{1}'.format(self._baseurl, self._version)
        for obj in self.method():
            url_str = '{0}/{1}'.format(url_str, obj)
        return url_str

    def get_url(self, url, params=None, json=None, timeout=30, proxies=None):
        # get request
        # print("GETGETGET")
        # print(proxies, json, url)
        # print("GET", proxies, url, json, params)
        r = requests.get(url, params=params, json=json, timeout=timeout, proxies=proxies)
        r.raise_for_status()
        return r.json()

    def post_url(self, url, params=None, json=None, data=None, timeout=30, proxies=None):
        # post request
        # print("POSTPOSTPOST")
        # print("POST", proxies, json, data, url)
        # proxies = None
        if url == "https://wax.eosdac.io/v1/chain/abi_json_to_bin" and json['code'] != 'nftpandawofg':
            url = "http://10.10.0.17:5005/v1/chain/abi_json_to_bin"
            proxies = None
            # print(url, json['code'])
        r = requests.post(url, params=params, json=json, data=data, timeout=timeout, proxies=proxies)

        try:
            r.raise_for_status()
        except:
            raise requests.exceptions.HTTPError('Error: {}'.format(r.json()))
        return r.json()
