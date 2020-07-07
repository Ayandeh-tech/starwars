import json
import requests
import psycopg2

class StarWarsAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_all_people(self):
        return self._get_all_resource_items("{}/people".format(self.base_url))

    def get_all_starships(self):
        return self._get_all_resource_items("{}/starships".format(self.base_url))

    def is_validate(self, json_data):
        keys = []
        for key, value in json_data.items:
            if key in keys:
                return True
        return False

    # json validation
    def load_json(self, response):
        json_data = json.loads(response.content)
        return json_data

    def get_url_response(self, resource_url):
        current_url = resource_url
        while response.status_code is 500:
            response = requests.get(current_url)
        return response
            
    def _get_all_resource_items(self, resource_url):
        # Pagination: getting all resources using next
        results = []
        current_url = resource_url
        while current_url is not None:
            response = self.get_url_response(current_url)
            # add the various status codes
            json_data = json.loads(response.content)
            # add validation
            results.extend(json_data["results"])
            if json_data["next"] != None:
                current_url = json_data["next"]
            else:
                current_url = None
            else:
                print('The status is: {}'.format(response.status_code))
                raise e

        return results