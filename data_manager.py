import pandas as pd
import gspread
import matplotlib.pyplot as plt
import notification_manager as nm

# flight_data = {'PAR': {'2024-10-07': {'price': 1615.0, 'departure time': '21:35:00', 'duration': '16H10M', 'airline code': 'EY'}, '2024-10-08': {'price': 1546.0, 'departure time': '15:00:00', 'duration': '25H55M', 'airline code': 'UL'}, '2024-10-09': {'price': 1607.0, 'departure time': '14:40:00', 'duration': '22H15M', 'airline code': 'MF'}}, 'FRA': {'2024-10-07': {'price': 1705.0, 'departure time': '21:35:00', 'duration': '15H40M', 'airline code': 'EY'}, '2024-10-08': {'price': 1546.0, 'departure time': '15:00:00', 'duration': '28H40M', 'airline code': 'UL'}, '2024-10-09': {'price': 1596.0, 'departure time': '09:45:00', 'duration': '27H30M', 'airline code': 'EY'}}, 'HND': {'2024-10-07': {'price': 2827.0, 'departure time': '21:45:00', 'duration': '19H15M', 'airline code': 'MH'}, '2024-10-08': {'price': 3850.0, 'departure time': '14:15:00', 'duration': '7H', 'airline code': 'NH'}, '2024-10-09': {'price': 3850.0, 'departure time': '14:15:00', 'duration': '7H', 'airline code': 'NH'}}, 'HKG': {'2024-10-07': {'price': 3691.0, 'departure time': '19:50:00', 'duration': '4H', 'airline code': 'MH'}, '2024-10-08': {'price': 280.0, 'departure time': '10:15:00', 'duration': '4H', 'airline code': 'OD'}, '2024-10-09': {'price': 280.0, 'departure time': '10:15:00', 'duration': '4H', 'airline code': 'OD'}}, 'IST': {'2024-10-07': {'price': 1809.0, 'departure time': '23:05:00', 'duration': '10H45M', 'airline code': 'TK'}, '2024-10-08': {'price': 1543.0, 'departure time': '08:50:00', 'duration': '10H55M', 'airline code': 'TK'}, '2024-10-09': {'price': 1543.0, 'departure time': '08:50:00', 'duration': '10H55M', 'airline code': 'TK'}}}

class DataManager:
    def __init__(self, flight_data):
        self.flight_data = flight_data

        self.flight_df = self.create_table()
        self.send_to_sheets()
        self.create_scatter()

    def create_table(self):

        '''CREATE THE DATAFRAME TEMPLATE TO PUT THE OBTAINED API VALUES IN'''

        flight_deals_dict = {
            'City': ['Paris', 'Frankfurt', 'Tokyo', 'Hong Kong', 'Istanbul'],
            'IATA Code': ['PAR', 'FRA', 'HND', 'HKG', 'IST'],
            'Lowest Price': [2000, 2000, 2000, 2000, 2000],
            'Departure Time': [str(i) for i in range(0, 5)],
            'Duration': [str(i) for i in range(0, 5)],
            'Airline Code': [str(i) for i in range(0, 5)],
            'Date': [str(i) for i in range(0, 5)],
        }

        flight_df = pd.DataFrame.from_dict(flight_deals_dict)



        '''FROM THE CURATED LOWEST DATES, GET THE LOWEST DATES BETWEEN THEM FOR EACH COUNTRY'''

        lowest_details = []
        for i in range(len(flight_df)):
            flight_details = self.flight_data[flight_df.loc[i]['IATA Code']]
            # print(flight_details)

            lowest_price = flight_details[list(flight_details.keys())[0]]['price']
            # print(lowest_price)
            lowest_details.append(flight_details[list(flight_details.keys())[0]])
            for keys in flight_details:
                flight_details[keys]['date'] = keys

                if flight_details[keys]['price'] < lowest_price:
                    lowest_details[len(lowest_details) - 1] = flight_details[keys]
                    lowest_price = flight_details[keys]['price']
                else:
                    continue
            # print(lowest_price)
            #
            # print(lowest_details)
            #
            # print(flight_df)


        '''REPLACE VALUES OF LOWEST PRICE FOR DATE IN THE CREATE DATAFRAME'''
        for j in range(len(flight_df)):
            flight_df.loc[j, 'Lowest Price'] = lowest_details[j]['price']
            flight_df.loc[j, 'Departure Time'] = lowest_details[j]['departure time']
            flight_df.loc[j, 'Duration'] = lowest_details[j]['duration']
            flight_df.loc[j, 'Airline Code'] = lowest_details[j]['airline code']
            flight_df.loc[j, 'Date'] = lowest_details[j]['date']

        print(flight_df)

        return flight_df

    def send_to_sheets(self):

        '''CREATE THE CONNECTION TO GOOGLE SHEETS USING GSPREAD'''
        switch = 0
        email_data = []

        gc = gspread.service_account(filename='insert json file here')
        sh = gc.open("Flight Deals")

        worksheet = sh.get_worksheet(1)

        read_df = pd.DataFrame(worksheet.get_all_records())

        for i in range(len(read_df['Lowest Price'])):
            if self.flight_df['Lowest Price'][i] < read_df['Lowest Price'][i]:
                switch = 1
                email_data.append((self.flight_df['IATA Code'][i], self.flight_df['Lowest Price'][i]))

        if switch == 1:
            nm.NotificationManager(email_data)

        worksheet.update([self.flight_df.columns.values.tolist()] + self.flight_df.values.tolist())


    def create_scatter(self):

        '''CREATE SCATTER PLOT FOR DATA VISUALISATION'''

        scatter_df = self.flight_df[['Date', 'Lowest Price', 'IATA Code']]

        fig, ax = plt.subplots()
        ax.scatter(scatter_df['Date'],scatter_df['Lowest Price'])

        for i, txt in enumerate(scatter_df['IATA Code']):
            ax.annotate(txt, (scatter_df['Date'][i], scatter_df['Lowest Price'][i]))

        plt.show()

