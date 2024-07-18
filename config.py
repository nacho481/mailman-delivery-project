# config.py

import datetime

# Constants
M_TRUCK_CAPACITY = 16
M_TRUCK_SPEED = 18
M_HUB_ADDRESS = '4001 South 700 East'
M_STARTING_MILEAGE = 0.0
M_STARTING_TIME = 8
M_INITIAL_LOAD = None

# File paths
M_PACKAGE_FILE = 'CSV/Package_File.csv'
M_DISTANCE_FILE = 'CSV/Distance_File.csv'
M_ADDRESS_FILE = 'CSV/Address_File.csv'

# Truck configurations
M_TRUCK_CONFIGS = [
    {
        "capacity": M_TRUCK_CAPACITY,
        "speed": M_TRUCK_SPEED,
        "packages": [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40],
        "mileage": M_STARTING_MILEAGE,
        "address": M_HUB_ADDRESS,
        "depart_time": datetime.timedelta(hours=M_STARTING_TIME),
        "load": M_INITIAL_LOAD
    },
    {
        "capacity": M_TRUCK_CAPACITY,
        "speed": M_TRUCK_SPEED,
        "packages": [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39],
        "mileage": M_STARTING_MILEAGE,
        "address": M_HUB_ADDRESS,
        "depart_time": datetime.timedelta(hours=M_STARTING_TIME),
        "load": M_INITIAL_LOAD
    },
    {
        "capacity": M_TRUCK_CAPACITY,
        "speed": M_TRUCK_SPEED,
        "packages": [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33],
        "mileage": M_STARTING_MILEAGE,
        "address": M_HUB_ADDRESS,
        "depart_time": datetime.timedelta(hours=M_STARTING_TIME),
        "load": M_INITIAL_LOAD
    }
]