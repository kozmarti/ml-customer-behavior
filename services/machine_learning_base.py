from abc import ABC, abstractmethod
import os
from typing import final

import pandas as pd
import logging

logger = logging.getLogger(__name__)


class MachineLearningBase(ABC):
    """
    Design Pattern : Template Method that contains a skeleton of
    some algorithm, composed of calls to (usually) abstract primitive
    operations.

    """
    def __init__(self, file_data_path, model_files_path) -> None:
        self.file_data_path = file_data_path
        self.model_files_path = model_files_path
        self.model = None
        self.data = None
        self.input_data = None
        self.output_data = None
        self.scores = {}

    @final
    def create_model(self):
        """ Skeleton of the algorithm, 
        must run steps for AI Model train and persist, and prediction in order """
        if self.is_existing_model():
            logger.warning("Stop model creating process")
            return
        self.import_data()
        self.clean_data()
        self.get_historical_input()
        self.transform_historical_input()
        self.get_historical_output()
        self.transform_historical_output()
        self.train_model()
        if self.check_model_accuracy():
            self.persist_model()

    @final
    def import_data(self):
        self.raw_data = pd.read_csv(self.file_data_path)
        return self.raw_data

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
        try:
            if os.listdir(self.model_files_path):
                logger.warning("Model already exists")
                return True
        except FileNotFoundError:
            return False

    @abstractmethod
    def train_model(self):
        pass

    @abstractmethod
    def check_model_accuracy(self):
        pass

    @abstractmethod
    def persist_model(self):
        pass


