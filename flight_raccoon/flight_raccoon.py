from config import API_KEY
from flight_raccoon.flights import Flights
from pprint import pprint

def give_me_flights(data: str) -> str:
    data = data.split(',')
    result = ''
    data = [x.strip() for x in data]
    fd = Flights()
    try:
        res_data = fd.get_round_prices(*data)
        if (len(res_data) > 0):
            res_data = [x for x in res_data]
            result = res_data[0:5]
    except Exception as e:
        print(e)
        
    
    return result

def give_me_accomodation(data: str) -> str:
    res = []
    for i in range(10):
        res.append(i)
        
    return res