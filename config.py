# config.py

import datetime

# Constants
TRUCK_CAPACITY = 16
TRUCK_SPEED = 18
HUB_ADDRESS = '4001 South 700 East'
STARTING_MILEAGE = 0.0
STARTING_TIME = 8
INITIAL_LOAD = None

# File paths
PACKAGE_FILE = 'CSV/Package_File.csv'
DISTANCE_FILE = 'CSV/Distance_File.csv'
ADDRESS_FILE = 'CSV/Address_File.csv'

# Truck configurations
TRUCK_CONFIGS = [
    {
        "capacity": TRUCK_CAPACITY,
        "speed": TRUCK_SPEED,
        "packages": [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40],
        "starting_mileage": STARTING_MILEAGE,
        "address": HUB_ADDRESS,
        "departure_time": datetime.timedelta(hours=STARTING_TIME),
        "initial_load": INITIAL_LOAD
    },
    {
        "capacity": TRUCK_CAPACITY,
        "speed": TRUCK_SPEED,
        "packages": [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39],
        "starting_mileage": STARTING_MILEAGE,
        "address": HUB_ADDRESS,
        "departure_time": datetime.timedelta(hours=STARTING_TIME),
        "initial_load": INITIAL_LOAD
    },
    {
        "capacity": TRUCK_CAPACITY,
        "speed": TRUCK_SPEED,
        "packages": [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33],
        "starting_mileage": STARTING_MILEAGE,
        "address": HUB_ADDRESS,
        "departure_time": datetime.timedelta(hours=STARTING_TIME),
        "initial_load": INITIAL_LOAD
    }
]