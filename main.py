# Author: Ignacio-Manuel Atilano
# ID: 010260310

import csv
import datetime
from typing import List, Tuple

import Truck
from HashTable import HashTable
from Package import Package


# CONSTANTS
M_TRUCK_CAPACITY = 16
M_TRUCK_SPEED = 18
M_HUB_ADDRESS = '4001 South 700 East'
M_STARTING_MILEAGE = 0.0
M_STARTING_TIME = 8
M_INITIAL_LOAD = None


def m_load_package_data(filename, hash_table):
    """The m_load_package_data will load in package information for each package opening """
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        for p in package_data:
            pID = int(p[0])
            pAddress = p[1]
            pCity = p[2]
            pState = p[3]
            pZip = p[4]
            pDeadline = p[5]
            pWeight = p[6]
            pStatus = "At Hub"

            # Create package object
            p_obj = Package(pID, pAddress, pCity, pState, pZip, pDeadline, pWeight, pStatus)
            hash_table.m_insert(pID, p_obj)  # insert p_object


def m_extract_address(address):
    """A helper method to obtain the label of the vertex to then reference in the adjacent matrix to determine
    the weighted edge to then be used in the nearest neighbor algorithm"""
    for row in m_address_file:
        if address in row[2]:
            return int(row[0])


def m_distance_between(x_value, y_value):
    """References weighted matrix providing indices for the row and column of the elemnt returning it as a float
    point value."""
    if m_distance_file[x_value][y_value] == '':
        return float(m_distance_file[y_value][x_value])
    else:
        return float(m_distance_file[x_value][y_value])


def m_calculate_distance(address1: str, address2: str) -> float:
    """Calculate the distance between 2 addresses"""
    idx1 = m_extract_address(address1)
    idx2 = m_extract_address(address2)
    return m_distance_between(idx1, idx2)


def m_update_truck_status(truck: Truck, package: Package, distance: float):
    """Update the truck's status after delivering a package"""
    truck.m_packages.append(package.m_ID)
    truck.m_mileage += distance
    truck.m_address = package.m_address
    truck.m_time += datetime.timedelta(hours= distance / truck.m_speed)
    package.m_delivery_time = truck.m_time
    package.m_departure_time = truck.m_departure_time


def m_find_nearest_package(truck: Truck, pending_packages: List[Package]) -> Tuple[Package, float]:
    """Find the nearest package to truck's location."""
    nearest_package = min(pending_packages,
                          key=lambda p: m_calculate_distance(truck.m_address, p.m_address))
    distance = m_calculate_distance(truck.m_address, nearest_package.m_address)
    return nearest_package, distance


def m_deliver_packages(truck: Truck):
    """This method will take a truck object and then sort the packages in the truck object to drop off the packages
    in the most efficient way possible. This method uses a variation of the nearest neighbor algorithm to do so."""

    # load pending packages yet to be delivered
    m_pending_packages = [m_package_hash_table.m_look_up(pID) for pID in truck.m_packages]
    truck.m_packages.clear()  # We want to insert packages according to the most efficient path so clear it

    while m_pending_packages:
        nearest_package, distance = m_find_nearest_package(truck, m_pending_packages)
        m_update_truck_status(truck, nearest_package, distance)
        m_pending_packages.remove(nearest_package)


    # # Determine what packages need to be dropped off so long as the list is not empty in pending packages
    # while len(m_pending_packages) > 0:
    #     next_address = float('inf')  # starting address
    #     next_package: Package = None  # available package object used for later
    #     for package in m_pending_packages:  # go through pending package list
    #         # calculating Euclidean distance is not necessary for this nearest neighbor algorithm since
    #         # the distance_file provides information to make an adjacency matrix
    #         # If (distance = truck.m_address + package.m_address) <= next_address, then execute the code
    #         if m_distance_between(m_extract_address(truck.m_address),
    #                               m_extract_address(package.m_address)) < next_address:
    #             # closer neighbor so reassign next address
    #             next_address = m_distance_between(m_extract_address(truck.m_address),
    #                                               m_extract_address(package.m_address))
    #             next_package = package  # reassign next to equal loop variable
    #
    #     truck.m_packages.append(next_package.m_ID)  # add the closest package
    #     m_pending_packages.remove(next_package)  # remove from pending package since it's in the truck now
    #     truck.m_mileage += next_address  # increment mileage accrued
    #     truck.m_address = next_package.m_address  # update truck's current location, and preps for next iteration
    #     truck.m_time += datetime.timedelta(hours=next_address / 18)  # divide the distance by speed traveled
    #     next_package.m_delivery_time = truck.m_time  # update delivery time
    #     next_package.m_departure_time = truck.m_departure_time  # update departure time


def m_get_user_time():
    """Prompt user to ask the status of a package(s) at a particular time."""
    while True:
        user_time = input("Enter time to check the status of a package in HH:MM format: ")
        try:
            (h, m) = user_time.split(':')
            return datetime.timedelta(hours=int(h), minutes=int(m))
        except ValueError:
            print("Invalid time format. Please try again (HH:MM).")  # prompt user to re-enter value correctly


def m_get_package_selection():
    # Ensures we get right data type from user
    while True:
        second_input = input("Enter (1 for 1 package) or (2 for all packages): ")
        if second_input in ("1", "2"):  # We want either 1 or 2
            return int(second_input)
        else:
            print("Invalid selection. Please enter 1 or 2.")  # Reprompt the user to enter a correct value


def main():
    # title
    print("Western Governors University Parcel Service")  # Show delivery service name
    # total miles for all the trucks
    print(f"Total miles: {m_truck1.m_mileage + m_truck2.m_mileage + m_truck3.m_mileage} miles")

    while True:
        text = input("To start please type 's' for start")
        if text == 's':
            try:
                convert_timedelta = m_get_user_time()  # Get time from user
                selection = m_get_package_selection()  # See what option they want displayed

                if selection == 1:
                    try:
                        one_input = input("Enter package ID: ")
                        package = m_package_hash_table.m_look_up(int(one_input))
                        print(str(package))
                        break
                    except ValueError:
                        print('Invalid package ID. Closing program.')
                        exit()
                elif selection == 2:
                    for x in range(1, 41):
                        package = m_package_hash_table.m_look_up(x)
                        package.m_update_status(convert_timedelta)
                        print(str(package))
                    break
                else:
                    exit()
            except ValueError as e:
                print(f'Invalid entry: {e}. Closing program...')
                exit()
        else:
            print("Invalid entry: Closing program...")
            exit()


# Read package information
with open("CSV/Package_File.csv") as package_file:
    m_package_file = csv.reader(package_file)
    m_package_file = list(m_package_file)

# Read distance file
with open("CSV/Distance_File.csv") as distance_file:
    m_distance_file = csv.reader(distance_file)
    m_distance_file = list(m_distance_file)

# Read address file
with open("CSV/Address_File.csv") as address_file:
    m_address_file = csv.reader(address_file)
    m_address_file = list(m_address_file)


m_truck1 = Truck.Truck(M_TRUCK_CAPACITY,
                       M_TRUCK_SPEED,
                       [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40],
                       M_STARTING_MILEAGE,
                       M_HUB_ADDRESS,
                       datetime.timedelta(hours=M_STARTING_TIME),
                       M_INITIAL_LOAD
                       )
m_truck2 = Truck.Truck(M_TRUCK_CAPACITY,
                       M_TRUCK_SPEED,
                       [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39],
                       M_STARTING_MILEAGE,
                       M_HUB_ADDRESS,
                       datetime.timedelta(hours=M_STARTING_TIME),
                       M_INITIAL_LOAD)

m_truck3 = Truck.Truck(M_TRUCK_CAPACITY,
                       M_TRUCK_SPEED,
                       [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33],
                       M_STARTING_MILEAGE,
                       M_HUB_ADDRESS,
                       datetime.timedelta(hours=M_STARTING_TIME),
                       M_INITIAL_LOAD)

m_package_hash_table = HashTable()
m_load_package_data("CSV/Package_File.csv", m_package_hash_table)

m_deliver_packages(m_truck1)
m_deliver_packages(m_truck2)
m_truck3.m_departure_time = min(m_truck1.m_time, m_truck2.m_time)
m_deliver_packages(m_truck3)

if __name__ == "__main__":
    main()
