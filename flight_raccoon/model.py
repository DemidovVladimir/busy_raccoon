import pandas as pd
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class Model:
    @staticmethod
    def read():
        try:
            res = pd.read_csv('data.csv')
            logger.info(res)
            return res
        except FileNotFoundError:
            logger.warning('File not found')