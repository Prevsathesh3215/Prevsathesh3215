import gspread
import pandas as pd

class Emails:
    def __init__(self):
        self.data = []
        gc = gspread.service_account(filename='mineral-hangar-423610-j6-e72de96ac996.json')
        sh = gc.open("Flight Deals")

        worksheet = sh.get_worksheet(0)

        read_df = pd.DataFrame(worksheet.get_all_records())
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

        for i in range(len(read_df)):
            self.data.append(read_df['Enter your email address.'][i])

        print(self.data)



