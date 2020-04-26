import requests


class AzuracastClient:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

    def get_headers(self):
        return {
            'Authorization': 'Bearer %s' % self.api_key
        }

    def add_mount(self, station_id, data):
        r = requests.post('%s/api/station/%d/mounts' % (self.url, station_id), headers=self.get_headers(), data=data)
        if r.status_code != 200:
            raise Exception('Failed to add mount')
        return r.json()
