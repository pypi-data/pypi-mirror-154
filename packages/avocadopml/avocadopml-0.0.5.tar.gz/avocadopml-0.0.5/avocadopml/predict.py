import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor

def predict(date, total_volume, small_hass, large_hass, xlarge_hass, total_bags, small_bags, large_bags, xlarge_bags, avocado_type, year, region):
    encoder = LabelEncoder()
    print(os.path.join(os.path.dirname(__file__), '', 'data', 'region_classes.npy'))
    encoder.classes_ = np.load(os.path.join(os.path.dirname(__file__), '', 'data', 'region_classes.npy'), allow_pickle=True)
    region = encoder.transform(np.expand_dims(region, -1))[0]
    encoder.classes_ = np.load(os.path.join(os.path.dirname(__file__), '', 'data', 'type_classes.npy'), allow_pickle=True)
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
    model.load_model(os.path.join(os.path.dirname(__file__), '', 'data', 'avocado_model.json'))
    prediction = model.predict(input)
    return prediction[0]