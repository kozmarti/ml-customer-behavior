PATH_RAW_DATA = 'static/marketing_campaign.csv'
COLUMNS_TO_EXCLUDE = [
       'Dt_Customer', 'Recency', 'NumDealsPurchases', 'NumWebVisitsMonth',
       'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1',
       'AcceptedCmp2', 'Complain', 'Z_CostContact', 'Z_Revenue', 'Response', 'ID']
PURCHASE_METHOD = ['NumWebPurchases',
                   'NumCatalogPurchases', 'NumStorePurchases']
PURCHASE_CATEGORY = ['MntWines', 'MntFruits', 'MntMeatProducts',
                     'MntFishProducts', 'MntSweetProducts',
                     'MntGoldProds']
OUTPUT_COLUMNS = PURCHASE_METHOD + PURCHASE_CATEGORY + ['maxPurchaseCategory',
                                                        'maxPurchaseMethod']
INPUT_COLUMNS = ['Education', 'Marital_Status',
                'Income', 'Kidhome', 'Teenhome']

COLORS = ['#9DD2DF', '#98A0D0', '#D0A0C3', '#D3CCE7', '#B65899', '#C6B5C7', '#AAAFC9', '#A07D9C']


MARITAL_STATUS = {
    0: 'Single',
    1: 'Together',
    2: 'Married',
    3: 'Divorced', 
    4: 'Widow',
    5: 'Alone',
    6: 'Absurd',
    7: 'YOLO'
}

EDUCATION = {
    0: 'PhD',
    1: 'Master',
    2: 'Graduation',
    3: 'Basic',
    4: '2n Cycle'
}