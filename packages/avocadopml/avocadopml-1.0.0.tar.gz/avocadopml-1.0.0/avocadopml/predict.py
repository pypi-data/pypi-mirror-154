import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor

class AvocadoPricePredictor:
    def __init__(self):
        curr_path = os.path.dirname(__file__)

        self.region_encoder = LabelEncoder()
        self.type_encoder = LabelEncoder()
        self.region_encoder.classes_ = np.load(os.path.join(curr_path, 'data', 'region_classes.npy'), allow_pickle=True)
        self.type_encoder.classes_ = np.load(os.path.join(curr_path, 'data', 'type_classes.npy'), allow_pickle=True)
        self.model = XGBRegressor()
        self.model.load_model(os.path.join(curr_path, 'data', 'avocado_model.json'))


    def prepare_data(self, date, total_volume, small_hass, large_hass, xlarge_hass, total_bags, small_bags, large_bags, xlarge_bags, avocado_type, year, region):
        region = self.region_encoder.transform(np.expand_dims(region, -1))[0]
        avocado_type = self.type_encoder.transform(np.expand_dims(avocado_type, -1))[0]
        input = pd.DataFrame({'Date': [date], 
                              'Total Volume': [total_volume], 
                              '4046': [small_hass], '4225': [large_hass], '4770': [xlarge_hass], 
                              'Total Bags': [total_bags], 'Small Bags': [small_bags], 'Large Bags': [large_bags], 'XLarge Bags': [xlarge_bags], 
                              'type': [avocado_type], 
                              'year': [year], 
                              'region': [region]})

        input.set_index('Date', inplace=True)
        return input

    def predict(self, date, total_volume, small_hass, large_hass, xlarge_hass, total_bags, small_bags, large_bags, xlarge_bags, avocado_type, year, region):
        params = locals()
        del params['self']
        input = self.prepare_data(**params)
        prediction = self.model.predict(input)
        return prediction[0]