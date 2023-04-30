from flight_raccoon.flights import Flights, InvalidArguments
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def give_me_flights(data: str) -> str:
    data = data.split(',')
    if len(data) != 8:
        raise InvalidArguments
    result = ''
    data = [x.strip() for x in data]
    fd = Flights()
    try:
        res_data = fd.get_round_prices(*data)
        if (len(res_data) > 0):
            res_data = [x for x in res_data]
            result = res_data[0:5]
    except Exception as e:
        logger.warning(e)
        
    
    return result

def give_me_accomodation(data: str) -> str:
    res = []
    for i in range(10):
        res.append(i)
        
    return res