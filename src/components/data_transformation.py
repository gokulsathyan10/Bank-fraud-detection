import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.components.data_load import data_loader    

from exception import CustomException

PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data')


@dataclass
class data_transformation_config:
    """Configuration for data transformation"""
    preprocessor_obj_path: str = os.path.join("artifacts", "preprocessor.pkl")
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    transformed_train_path: str = os.path.join("artifacts", "transformed_train.csv")
    transformed_test_path: str = os.path.join("artifacts", "transformed_test.csv")


class data_cleaning:
    """Class to load raw data from the data folder and clean it"""

    def __init__(self, path=PATH):
        self.path = path

    def load_data(self):
        try:
            if not os.path.exists(self.path):
                raise CustomException(f"Data directory not found at: {self.path}", sys)
            
            self.cust_data,self.acc_data,self.txn_data = data_loader(PATH).load_data()  

        except Exception as e:
            raise CustomException(e, sys)

    def remove_duplicates(self):
        try:
            before = {
                "customers": len(self.cust_data),
                "accounts": len(self.acc_data),
                "transactions": len(self.txn_data),
            }

            self.cust_data = self.cust_data.drop_duplicates().reset_index(drop=True)
            self.acc_data = self.acc_data.drop_duplicates().reset_index(drop=True)
            self.txn_data = self.txn_data.drop_duplicates().reset_index(drop=True)

            after = {
                "customers": len(self.cust_data),
                "accounts": len(self.acc_data),
                "transactions": len(self.txn_data),
            }

            for name in before:
                removed = before[name] - after[name]
                print(f"{name}: removed {removed} duplicate rows ({before[name]} -> {after[name]})")

            return self.cust_data, self.acc_data, self.txn_data
        except Exception as e:
            raise CustomException(e, sys)


# if __name__ == "__main__":
#     cleaner = data_cleaning()
#     cleaner.load_data()
#     cust_df, acc_df, txn_df = cleaner.remove_duplicates()
