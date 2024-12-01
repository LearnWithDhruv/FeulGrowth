import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

class DataRetriever:
    def __init__(self, credentials_path):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_path, scope
        )
        client = gspread.authorize(creds)
        
        self.sheet = client.open_by_url(
            'https://docs.google.com/spreadsheets/d/1Bj4-sd6362GWrFZOPcND3fFo0oroO1pfhkpMJh8iIE4/edit?usp=sharing'
        ).sheet1

    def get_data(self):
        """
        Retrieve data from Google Sheets
        
        :return: DataFrame with video performance data
        """
        data = self.sheet.get_all_records()
        return pd.DataFrame(data)

    def save_data(self, df, output_path='data/processed/performance_data.csv'):
        df.to_csv(output_path, index=False)