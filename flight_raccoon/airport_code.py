import requests
import json
from config import TEQUILA_API_KEY

class AirportCode:
    headers = {
        'accept': 'application/json',
        'apikey': ''
    }

    def __init__(self):
        self.headers['apikey'] = TEQUILA_API_KEY

    def get_code(self, code: str) -> str:
        with requests.Session() as session:
            with session.get(f'https://api.tequila.kiwi.com/locations/query?term={code}&locale=en-US&location_types=airport&limit=10&active_only=true', headers=self.headers) as response:
                return json.loads(response.content)['locations'][0]['code']
