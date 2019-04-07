import random
from peewee import *
from datetime import date
from datetime import time


db_arrival = SqliteDatabase('avia_schedule_arrival.db')
db_departure = SqliteDatabase('avia_schedule_departure.db')
db_user_data_input = SqliteDatabase('data_user.db')
db_avia_places = SqliteDatabase('avia_places.db')


class AviaSchleduleArrival(Model):
    airport = CharField()
    flight = CharField()
    time = TimeField()
    date = DateField()
    departure = CharField()
    arrival = CharField()
    is_relative = BooleanField()

    class Meta:
        database = db_arrival  # модель будет использовать базу данных 'avia_schedule_arrival.db'


class AviaSchleduleDeparture(Model):
    airport = CharField()
    flight = CharField()
    time = TimeField()
    date = DateField()
    departure = CharField()
    arrival = CharField()
    is_relative = BooleanField()

    class Meta:
        database = db_departure  # модель будет использовать базу данных 'avia_schedule_departure.db'


class UserData(Model):
    data = CharField()

    class Meta:
        database = db_user_data_input  # модель будет использовать базу данных 'avia_schedule_departure.db'


class AviaPlace(Model):
    literal_avia = CharField()
    num_avia = CharField()
    data_avia = CharField()

    class Meta:
        database = db_avia_places  # модель будет использовать базу данных 'avia_schedule_departure.db'

#Person.create_table()
# a-b, A-B - '1-9' (4 nums)
# ab-1234
if __name__ == '__main__':
    AviaSchleduleArrival.create_table()
    AviaSchleduleDeparture.create_table()
    UserData.create_table()
    AviaPlace().create_table()

    literals = 'qwertyuiopasdfghjklzxcvbnm'
    nums = '1234567890'
    flight_generated_arrival = [
        ''.join([random.choice(list(literals.upper())) for i in range(2)]),
        ''.join([random.choice(list(nums)) for j in range(4)])
    ]
    airport_arrival = 'Pulkovo Airport'
    time_arrival = '20:04'
    date_arrival = '2019-04-06'
    departure_arrival = 'Saint-Petersburg'
    arrival_arr = 'Los Angeles'
    status_arrival = True,  # reformat
    type_arrival = ''   # reformat

    user_data_arrival = AviaSchleduleArrival.create(airport=airport_arrival,
                                                    flight='-'.join(flight_generated_arrival),
                                                    time=time_arrival,
                                                    date=date_arrival,
                                                    departure=departure_arrival,
                                                    arrival=arrival_arr,
                                                    status=status_arrival,
                                                    type=type_arrival,
                                                    is_relative=True)

    flight_generated_departure = [
        ''.join([random.choice(list(literals.upper())) for i in range(2)]),
        ''.join([random.choice(list(nums)) for j in range(4)])
    ]
    airport_departure = 'LA Airport'
    time_departure = '20:04'
    date_departure = '2019-04-06'
    departure_departure = 'Los Angeles'
    arrival_departure = 'Saint-Petersburg'
    status_departure = True,  # reformat
    type_departure = ''   # reformat

    user_data_departure = AviaSchleduleDeparture.create(airport=airport_departure,
                                                        flight='-'.join(flight_generated_departure),
                                                        time=time_departure,
                                                        date=date_departure,
                                                        departure=departure_departure,
                                                        arrival=arrival_departure,
                                                        status=status_departure,
                                                        type=type_departure,
                                                        is_relative=True)

    data_usr = 'Maxim, 89258329337'

    user_data_input = UserData.create(data=data_usr,
                                      is_relative=True)

    for data_arrival in AviaSchleduleArrival.select():
        print(data_arrival.airport, data_arrival.flight, data_arrival.date,
              data_arrival.departure, data_arrival.arrival)

    for data_departure in AviaSchleduleDeparture.select():
        print(data_departure.airport, data_departure.flight, data_departure.date,
              data_departure.departure, data_departure.arrival)

    for data_user in UserData.select():
        print(data_user.date, data_user.name, data_user.telephone)

