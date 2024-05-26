import joblib
import pandas as pd

from services.constants import COLUMNS_TO_EXCLUDE, EDUCATION, MARITAL_STATUS, OUTPUT_COLUMNS, INPUT_COLUMNS, PATH_RAW_DATA, PURCHASE_CATEGORY, PURCHASE_METHOD
from services.graphs import get_histograms, get_pie_charts


def show_data():
    df = get_cleaned_data()
    histograms_html = get_histograms(df, PURCHASE_CATEGORY)
    piecharts_html = get_pie_charts(df, ['Teenhome', 
                                         'Kidhome', 'Education', 
                                         'Marital_Status'])
    return df.to_html(), histograms_html, piecharts_html


def predictions(education, marital_status, income, nb_kids_home, nb_teens_home, age):
    predictions = []
    for column in OUTPUT_COLUMNS:
        model = joblib.load(f"models/{column}-recommender.joblib")
        #  ['Education', 'Marital_Status', 'Income', 'Kidhome', 'Teenhome', 'age']
        prediction = model.predict([[education, marital_status, income, nb_kids_home, nb_teens_home, age]])
        predictions.append({column: prediction})
    inputs = {"Education_level": EDUCATION[education],
             "MaritalStatus": MARITAL_STATUS[marital_status], "Income": income,
             "NumberOfKidsAtHome" : nb_kids_home,
             "NumberOfTeensAtHome": nb_teens_home,
             "Age": age}
    return {"Input": inputs, "Output": predictions}


def get_cleaned_data():
    data = pd.read_csv(PATH_RAW_DATA, dtype={'Education': str})
    data.dropna(inplace=True)
    data = data.drop(columns=COLUMNS_TO_EXCLUDE)
    data["age"] = 2010 - data['Year_Birth']
    data = data.drop(columns=['Year_Birth'])
    data['maxPurchaseCategory'] = data[PURCHASE_CATEGORY].idxmax(axis=1)
    data['maxPurchaseMethod'] = data[PURCHASE_METHOD].idxmax(axis=1)
    return data



