import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from exception import CustomException

PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data')  

@dataclass
class data_load_config:
    """Configuration for data loading"""
    raw_data_path: str = os.path.join("artifacts", "raw_data.csv")
    preprocessed_data_path: str = os.path.join("artifacts", "preprocessed_data.csv")

class data_loader:
    """Class to load data from CSV files in the data directory"""
    def __init__(self, path):
        self.data_loader_config = data_load_config()
        self.path = path
    def load_data(self):
        try:
            if not os.path.exists(self.path):
                raise CustomException(f"Data directory not found at path: {self.path}", sys)
            self.cust_data = pd.read_csv(os.path.join(self.path, 'customers.csv'))
            self.acc_data = pd.read_csv(os.path.join(self.path, 'accounts.csv'))
            self.txn_data = pd.read_csv(os.path.join(self.path, 'transactions.csv'))

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":

    df_load = data_loader(PATH)
    df_load.load_data()
    print(df_load.cust_data.shape)
    print(df_load.acc_data.shape)
    print(df_load.txn_data.shape)
