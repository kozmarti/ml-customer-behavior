import joblib
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from services.constants import INPUT_COLUMNS, OUTPUT_COLUMNS, PURCHASE_CATEGORY, PURCHASE_METHOD


def transform_to_category(df, columns):
    for column in columns:
        df[column] = np.where(df[column] > df[column].quantile(.75), -3, df[column])
        df[column] = np.where(df[column] > df[column].quantile(.5), -2, df[column])
        df[column] = np.where(df[column] > df[column].quantile(.25), -1, df[column])
        df[column] = np.where(df[column] > 0, 0, df[column])
        df[column] = df[column].replace([-3, -2, -1], [3, 2, 1])


def persist_model(data):
    input_data = get_inputs(data)
    output_df = get_outputs(data)
    for column in OUTPUT_COLUMNS:
        output_data = output_df[column]
        model = DecisionTreeClassifier()
        model.fit(input_data, output_data)
        joblib.dump(model, f"{column}-recommender.joblib")


def test_model(data):
    scores = []
    input_data = get_inputs(data)
    output_df = get_outputs(data)
    for column in OUTPUT_COLUMNS:
        output_data = output_df[column]
        input_train, input_test, output_train, output_test = train_test_split(input_data,
                                                                              output_data,
                                                                              test_size=0.2)

        model = DecisionTreeClassifier()
        model.fit(input_train, output_train)
        predictions = model.predict(input_test)
        score = accuracy_score(output_test, predictions)
        scores.append((column, score))
    return scores


def get_inputs(data):
    data = data.drop(columns=(OUTPUT_COLUMNS))
    data = data.replace(['PhD', 'Master', 'Graduation', 'Basic', '2n Cycle'], [0, 1, 2, 3, 4])
    data = data.replace(['Single', 'Together', 'Married', 'Divorced', 'Widow', 'Alone', 'Absurd', 'YOLO'], [0, 1, 2, 3, 4, 5, 6, 7])
    return data


def get_outputs(data):
    output = data.drop(columns=INPUT_COLUMNS)
    data = data.replace(PURCHASE_CATEGORY, [0, 1, 2, 3, 4, 5])
    data = data.replace(PURCHASE_METHOD, [0, 1, 2])
    transform_to_category(output, PURCHASE_CATEGORY + PURCHASE_METHOD)
    return output
