import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor
from datetime import datetime

def predict(date, total_volume, small_hass, large_hass, xlarge_hass, total_bags, small_bags, large_bags, xlarge_bags, avocado_type, year, region):
    encoder = LabelEncoder()
    encoder.classes_ = np.load('avocadopml\\data\\region_classes.npy', allow_pickle=True)
    region = encoder.transform(np.expand_dims(region, -1))[0]
    encoder.classes_ = np.load('avocadopml\\data\\type_classes.npy', allow_pickle=True)
    avocado_type = encoder.transform(np.expand_dims(avocado_type, -1))[0]

    input = pd.DataFrame({'Date': [date], 
                          'Total Volume': [total_volume], 
                          '4046': [small_hass], '4225': [large_hass], '4770': [xlarge_hass], 
                          'Total Bags': [total_bags], 'Small Bags': [small_bags], 'Large Bags': [large_bags], 'XLarge Bags': [xlarge_bags], 
                          'type': [avocado_type], 
                          'year': [year], 
                          'region': [region]})
    input.set_index('Date', inplace=True)
    model = XGBRegressor(n_estimators=1000, learning_rate=0.05, n_jobs=4)
    model.load_model('avocadopml\\data\\avocado_model.json')
    prediction = model.predict(input)
    return prediction[0]
    
a = predict(datetime.strptime('12/27/2015', '%m/%d/%Y'), 64236.62, 1036.74, 54454.85, 48.16, 8696.87, 8603.62, 93.25, 0, 'conventional', 2015, 'Albany')
print(round(a, 2))