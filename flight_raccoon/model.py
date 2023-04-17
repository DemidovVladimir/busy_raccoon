import pandas as pd
from pprint import pprint

class Model:
    @staticmethod
    def read():
        try:
            res = pd.read_csv('data.csv')
            pprint(res)
            return res
        except FileNotFoundError:
            print('File not found')