from abc import ABC, abstractmethod
from typing import final

import pandas as pd


class MachineLearningBase(ABC):
    """
    Design Pattern : Template Method that contains a skeleton of
    some algorithm, composed of calls to (usually) abstract primitive
    operations.
    
    """
    def __init__(self, file_data_path) -> None:
        self.file_data_path = file_data_path
        
    @final
    def run_prediction(self):
        """ Skeleton of the algorithm, 
        must run steps for AI Model train and persist, and prediction in order """

    @final
    def import_data(self):
        self.raw_data = pd.read_csv(self.file_data_path)

    @abstractmethod
    def clean_data(self):
        pass

    @abstractmethod
    def get_historical_input(self):
        pass

    def transform_historical_input(self):
        """optional step"""
        pass

    @abstractmethod
    def get_historical_output(self):
        pass

    def transform_historical_output(self):
        """optional step"""
        pass

    @final
    def is_existing_model(self):
        """check path created in persist model !"""
        pass

    @abstractmethod
    def train_model(self):
        pass

    @abstractmethod
    def check_model_accuracy(self):
        pass

    @abstractmethod
    def persist_model(self):
        pass

    

    
