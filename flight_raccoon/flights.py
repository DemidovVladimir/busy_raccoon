from pprint import pprint
import requests
from config import TEQUILA_API_KEY, TEQUILA_API
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class Flights:
    url = ""
    headers = {
        'accept': 'application/json',
        'apikey': ''
    }

    def __init__(self):
        self.headers['apikey'] = TEQUILA_API_KEY
        self.url = f"{TEQUILA_API}/search?technical_stops=0&sort=price"

    def get_prices(self, fly_to, date_from, date_to, price_from, price_to) -> dict:
        self.url = f"{self.url}&fly_to={fly_to}&dateFrom={date_from}&dateTo={date_to}&price_from={price_from}&price_to={price_to}"
        try: 
            with requests.Session() as session:
                with session.get(self.url, headers=self.headers) as response:
                    data = response.json()
                    data = [{x: y for x, y in n.items() if x in ['cityTo', 'conversion', 'countryTo', 'has_airport_change', 'price', 'local_departure', 'local_arrival']} for n in data.get('data') if (n.get('pnr_count') < 3) and (n.get('availability').get('seats') is not None) and int(n.get('availability').get('seats', 0)) > 3]
                    return data
        except Exception as e:
            logger.warning(e)
            return {}

    def get_round_prices(self, date_from, date_to, fly_from, fly_to, price_to, nights_in_dst_from, nights_in_dst_to, max_fly_duration,) -> dict:
        self.url = f"{self.url}&fly_from={fly_from}&fly_to={fly_to}&dateFrom={date_from}&dateTo={date_to}&price_to={price_to}&nights_in_dst_from={nights_in_dst_from}&nights_in_dst_to={nights_in_dst_to}&max_fly_duration={max_fly_duration}"
        try: 
            with requests.Session() as session:
                with session.get(self.url, headers=self.headers) as response:
                    data = response.json()
                    data = [{x: y for x, y in n.items() if x in ['deep_link', 'conversion']} for n in data.get('data') if (n.get('pnr_count') < 3) and (n.get('availability').get('seats') is not None) and int(n.get('availability').get('seats', 0)) > 3]
                    return data
        except Exception as e:
            logger.warning(e)
            return {}