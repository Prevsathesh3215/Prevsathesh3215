import requests as rq
class FlightData:
    def __init__(self, dates):
        self.__API_KEY = 'insert own api'
        self.__API_SECRET = 'insert secret here'
        self.__access_token = ''
        self.dates = dates
        self.iata = ['PAR', 'FRA', 'HND', 'HKG', 'IST']
        self.info = {}
        self.info_complete = {}
        self.non_stop = 'true'


        self.__access_token = self.get_access_token()

        for iata in self.iata:
            for date in self.dates:
                self.info[date] = self.get_data(date, iata)

            self.info_complete[iata] = self.info
            self.info = {}

    def get_access_token(self):
        params = {
            "grant_type": "client_credentials",
            'client_id': self.__API_KEY,
            'client_secret': self.__API_SECRET,
        }

        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        resp = rq.post(url='https://test.api.amadeus.com/v1/security/oauth2/token', data= params, headers=header)
        return resp.text[286:314]

    def get_data(self, date, iata):

        flight_offer_endpoint = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
        non_stop = 'true'

        body = {
            'originLocationCode': 'KUL',
            'destinationLocationCode': iata,
            'departureDate': date,
            'adults': 1,
            'travelClass': 'ECONOMY',
            'nonStop': non_stop,
            'currencyCode': 'MYR',

        }

        flight_offer_header = {
            'Authorization': f'Bearer {self.__access_token}'
        }

        data = self.obtain_api_data(flight_offer_endpoint, body, flight_offer_header)


        if data['meta']['count'] == 0:
            body['nonStop'] = 'false'
            data = self.obtain_api_data(flight_offer_endpoint, body, flight_offer_header)



        detail = data['data']

        price_list = []
        all_details = []

        for i in detail:
           price_list.append(float(i['price']['total']))
           all_details.append(((i['itineraries'][0]['segments'][0]['departure']['at'][11:], i['itineraries'][0]['segments'][0]['carrierCode'], i['itineraries'][0]['duration'][2:])))

        min_price = min(price_list)
        min_index = price_list.index(min_price)
        min_detail = all_details[min_index]

        return {'price': min_price, 'departure time': min_detail[0], 'duration': min_detail[2], 'airline code': min_detail[1]}


    def obtain_api_data(self,flight_offer_endpoint, body, flight_offer_header):
        flight_offer_resp = rq.get(url=flight_offer_endpoint, params=body, headers=flight_offer_header)
        data = flight_offer_resp.json()
        return data






