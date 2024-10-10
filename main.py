import datetime as dt
import flight_data as fd
import data_manager as dm

today = dt.datetime.now()
dates = [dt.datetime.strftime(today, '%Y-%m-%d')]

for i in range(1, 3):
    date_next = today.date() + dt.timedelta(days=i)
    dates.append(dt.datetime.strftime(date_next, '%Y-%m-%d'))

flight_obj = fd.FlightData(dates)
flight_data = flight_obj.info_complete
dm.DataManager(flight_data)

