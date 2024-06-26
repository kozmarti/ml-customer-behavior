import os
import joblib
import pandas as pd

from .constants import (
    COLUMNS_TO_EXCLUDE,
    EDUCATION,
    MARITAL_STATUS,
    MODELS_PATH,
    OUTPUT_COLUMNS,
    PATH_RAW_DATA,
    PRODUCT_CATEGORY_MAPPING,
    PURCHASE_CATEGORY,
    PURCHASE_METHOD,
    PURCHASE_METHOD_MAPPING,
)
from .decision_tree_classifier_model import DecisionTreeClassifierModel
from .graphs import get_histograms, get_pie_charts


def show_data():
    df = get_cleaned_data()
    histograms_html = get_histograms(df, PURCHASE_CATEGORY)
    piecharts_html = get_pie_charts(
        df, ["Teenhome", "Kidhome", "Education", "Marital_Status"]
    )
    return histograms_html, piecharts_html


def predictions(education, marital_status, income, nb_kids_home, nb_teens_home, age):
    predictions = {}
    for column in OUTPUT_COLUMNS:
        if not os.path.exists(MODELS_PATH):
            model = DecisionTreeClassifierModel(PATH_RAW_DATA, MODELS_PATH)
            model.create_model()
        model = joblib.load(f"{MODELS_PATH}/{column}-recommender.joblib")
        #  ['Education', 'Marital_Status', 'Income', 'Kidhome', 'Teenhome', 'age']
        prediction = model.predict(
            [[education, marital_status, income, nb_kids_home, nb_teens_home, age]]
        )
        predictions[column] = prediction[0]

    predictions = translate_output(predictions)

    inputs = {
        "Education_level": EDUCATION[education],
        "MaritalStatus": MARITAL_STATUS[marital_status],
        "Income": income,
        "NumberOfKidsAtHome": nb_kids_home,
        "NumberOfTeensAtHome": nb_teens_home,
        "Age": age,
    }
    return {"Input": inputs, "Output": predictions}


def get_cleaned_data():
    data = pd.read_csv(PATH_RAW_DATA)
    data.dropna(inplace=True)
    data = data.drop(columns=COLUMNS_TO_EXCLUDE)
    data["age"] = 2010 - data["Year_Birth"]
    data = data.drop(columns=["Year_Birth"])
    data["maxPurchaseCategory"] = data[PURCHASE_CATEGORY].idxmax(axis=1)
    data["maxPurchaseMethod"] = data[PURCHASE_METHOD].idxmax(axis=1)
    return data


def translate_output(data):
    df = get_cleaned_data()
    for category in PURCHASE_CATEGORY:
        amount_range = f"{int(df[category].quantile((data[category] - 1)*0.25))}$ - {int(df[category].quantile(data[category]*0.25))}$"
        data[category] = amount_range

    for method in PURCHASE_METHOD:
        amount_range = f"{int(df[method].quantile((data[method] - 1)*0.25))} - {int(df[method].quantile(data[method]*0.25))}"
        data[method] = amount_range

    data["maxPurchaseCategory"] = PRODUCT_CATEGORY_MAPPING[PURCHASE_CATEGORY[data["maxPurchaseCategory"]]]
    data["maxPurchaseMethod"] = PURCHASE_METHOD_MAPPING[PURCHASE_METHOD[data["maxPurchaseMethod"]]]

    return data


def get_products_by_category(predictions):
    products = {}
    for category in PURCHASE_CATEGORY:
        new_key = PRODUCT_CATEGORY_MAPPING[category]
        products[new_key] = predictions[category]
    return products
