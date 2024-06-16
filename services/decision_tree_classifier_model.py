import joblib
import numpy as np
import os
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from services.constants import (
    COLUMNS_TO_EXCLUDE,
    INPUT_COLUMNS,
    OUTPUT_COLUMNS,
    PURCHASE_CATEGORY,
    PURCHASE_METHOD,
)
from .machine_learning_base import MachineLearningBase
import logging

logger = logging.getLogger(__name__)


class DecisionTreeClassifierModel(MachineLearningBase):
    def clean_data(self):
        self.raw_data.dropna(inplace=True)
        data = self.raw_data.drop(columns=COLUMNS_TO_EXCLUDE)
        data["age"] = 2010 - data["Year_Birth"]
        data = data.drop(columns=["Year_Birth"])
        data["maxPurchaseCategory"] = data[PURCHASE_CATEGORY].idxmax(axis=1)
        data["maxPurchaseMethod"] = data[PURCHASE_METHOD].idxmax(axis=1)
        self.data = data

    def get_historical_input(self):
        self.input_data = self.data.drop(columns=OUTPUT_COLUMNS)

    def transform_historical_input(self):
        self.input_data = self.input_data.replace(
            ["PhD", "Master", "Graduation", "Basic", "2n Cycle"], [0, 1, 2, 3, 4]
        )
        self.input_data = self.input_data.replace(
            [
                "Single",
                "Together",
                "Married",
                "Divorced",
                "Widow",
                "Alone",
                "Absurd",
                "YOLO",
            ],
            [0, 1, 2, 3, 4, 5, 6, 7],
        )

    def get_historical_output(self):
        self.output_data = self.data.drop(columns=INPUT_COLUMNS)

    def transform_historical_output(self):
        self.output_data = self.output_data.replace(PURCHASE_CATEGORY, [0, 1, 2, 3, 4, 5])
        self.output_data = self.output_data.replace(PURCHASE_METHOD, [0, 1, 2])
        self.transform_to_category(self.output_data, PURCHASE_CATEGORY + PURCHASE_METHOD)

    @classmethod
    def transform_to_category(self, df, columns):
        for column in columns:
            df[column] = np.where(
                df[column] > df[column].quantile(0.75), -3, df[column]
            )
            df[column] = np.where(df[column] > df[column].quantile(0.5), -2, df[column])
            df[column] = np.where(
                df[column] > df[column].quantile(0.25), -1, df[column]
            )
            df[column] = np.where(df[column] > 0, 0, df[column])
            df[column] = df[column].replace([-3, -2, -1], [3, 2, 1])

    def train_model(self):
        for column in OUTPUT_COLUMNS:
            output_data = self.output_data[column]
            input_train, input_test, output_train, output_test = train_test_split(
                self.input_data, output_data, test_size=0.2
            )

            model = DecisionTreeClassifier()
            model.fit(input_train, output_train)
            predictions = model.predict(input_test)
            score = accuracy_score(output_test, predictions)
            self.scores[column] = score

    def check_model_accuracy(self):
        accuracy = True
        for column, score in self.scores.items():
            if score <= 0.5:
                logger.warning(f"Model for {column} score {score} is not accurate enough")
                accuracy = False
        return accuracy

    def persist_model(self):
        logger.warning("PERSISTING")
        for column in OUTPUT_COLUMNS:
            output_data = self.output_data[column]
            model = DecisionTreeClassifier()
            model.fit(self.input_data, output_data)
            if not os.path.exists(self.model_files_path):
                os.makedirs(self.model_files_path)
            joblib.dump(model, f"{self.model_files_path}/{column}-recommender.joblib")
            logger.warning(f"Model for {column} persisted successfully")