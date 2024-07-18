# Author: Ignacio-Manuel Atilano
# ID: 010260310

import csv
import datetime
from typing import List, Tuple

import Truck
import logging
from HashTable import HashTable
from Package import Package

# CONSTANTS
M_TRUCK_CAPACITY = 16
M_TRUCK_SPEED = 18
M_HUB_ADDRESS = '4001 South 700 East'
M_STARTING_MILEAGE = 0.0
M_STARTING_TIME = 8
M_INITIAL_LOAD = None


def m_load_csv_file(filename: str) -> List[List[str]]:
    """
    Loads a CSV file into a lists of lists

    :arg
        filename: The path to the CSV file

    :returns
        A lists of lists where each inner list represents a row from the CSV file.

    :raises
        FileNotFound: When a file is not found
        csv.Error parsing the CSV file sent
        :exception
    """
    try:
        with open(filename, 'r') as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        logging.error(f'File not found {filename}')
        raise
    except csv.Error as e:
        logging.error(f'CSV error in file {filename}: {e}')
        raise
    except Exception as e:
        logging.error(f'Unexpected error when reading {filename}: {e}')


def m_load_package_data(filename: str, hash_table: HashTable) -> None:
    """The m_load_package_data will load in package information for each package opening
    :arg
        filename (str): The file being passed
        hash_table (HashTable): The hash table data structure being used

    :returns
        Nothing, just loads data into the truck

    :raises
        FileNotFoundError: If the specified CSV file is not found
        ValueError: If there are errors parsing the CSV data (e.g., invalid data types)

    """
    try:
        with open(filename) as package_info:
            package_data = csv.reader(package_info)
            for p in package_data:
                try:
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
                except (ValueError, TypeError) as e:
                    logging.error(f'Error parsing row in {filename}: {p}. Exception {e}')
    except FileNotFoundError as e:
        logging.error(f'File not found {filename}: Exception {e}')
        raise


def m_extract_address(address: str) -> int:
    """
    Provided the address, this will extract the label (vertex ID).

    Assuming the 'm_address_file' holds the address data, this method will search for the row where the 'address'
    field matches the provided 'address' argument. If a match is found, this will return the corresponding
    vertex ID.

    :arg
        address (str): The address string to search for

    :return
        int: The vertex ID (label) associated with the address, or it will raise an exception if it's not found.
    :raises
        ValueError: If the address data is not a list of a list OR if the vertex ID cannot be converted to an integer
    """

    if not isinstance(m_address_file, list):
        raise ValueError('Address data (m_address_file) must be a list of lists.')
    try:
        for row in m_address_file:
            if address in row[2]:
                return int(row[0])
        raise ValueError(f'Address {address} not found in address data.')
    except (TypeError, ValueError) as e:
        logging.error(f"Error extracting address label for '{address}': {e}")


def m_distance_between(x_value: int, y_value: int) -> float:
    """
    Returns the distance between two locations given their indices in the adjacent matrix.

    This function assumes that the adjacent matrix with weighted edges is stored in the 'm_distance_file' variable.
    Then, it'll look up the x and y value, or the row and column value respectively within the matrix. However, if
    that value is empty, it'll check the mirrored position, (col, row) or (y_value, x_value) respectively, to retrieve
    the distance.

    :arg
        x_value (int): Row index in adjacent matrix
        y_value (int): Column index in adjacent matrix

    :returns
        float: Returns the distance between the two locations OR raises an exception if not found.


    """
    try:
        # check for out of bounds
        if x_value < 0 or x_value >= len(m_distance_file):
            logging.error(f'x_value ({x_value}) is out of bounds for the distance matrix')
            raise IndexError(f'x_value ({x_value}) is out bounds for the distance matrix.')
        if y_value < 0 or y_value >= len(m_distance_file):
            logging.error(f'y_value ({y_value}) is out of bounds for the distance matrix')
            raise IndexError(f'y_value ({y_value}) is out of bounds for the distance matrix')

        # Access distance value and convert to float
        distance = m_distance_file[x_value][y_value]
        if distance == '':
            distance = m_distance_file[y_value][x_value]
            if distance == '':
                logging.error('Distance is not found between locations')
                raise ValueError('Distance is not found between locations')
        return float(distance)
    except (IndexError, ValueError) as e:
        logging.error(f'Error getting distance between {x_value} and {y_value}: {e}')
        raise


def m_calculate_distance(address1: str, address2: str) -> float:
    """A helper method to calculate the distance between 2 addresses, one that is passed and the second
    referencing the adjacent matrix.

    This function utilizes the 'm_extract_address()' method to obtain the vertex's label, in this case, their ID
    respectively to 'address1' and 'address2'. The distance is determined with the return statement calling
    the 'm_distance_between', functionality is discussed in the respective method.

    :arg
        address1 (str): The first address is a string
        address2 (str): The second address is a string.

    :returns
        float: The distance between the two addresses or raises an exception if an error occurs.

    :raises
        ValueError: If one or both addresses cannot be found in the address CSV file."""
    try:
        # Extract vertex labels for addresses
        idx1 = m_extract_address(address1)
        idx2 = m_extract_address(address2)
        return m_distance_between(idx1, idx2)  # Find distance using m_distance_between() method
    except ValueError as e:
        logging.error(f'Error calculating distance: {e}')
        raise


def m_update_truck_status(truck: Truck, package: Package, distance: float):
    """Update the truck's status after delivering a package by updating the package's attributes in the truck and the
    truck itself. This function updates the truck's package list, total mileage, current address, travel time by
    dividing distance by its speed, and updates the package's delivery and departure time.

    :arg
        truck (Truck): The truck object whose status needs to be updated.
        package (Package): The package object represents the package being delivered.
        distance (float): The distance the truck driver traveled to deliver the package.

    :raises
        ValueError: If the distance is negative or zero"""

    # Attempt to update status information
    try:
        truck.m_packages.append(package.m_ID)
        truck.m_mileage += distance
        truck.m_address = package.m_address
        truck.m_time += datetime.timedelta(hours=distance / truck.m_speed)
        package.m_delivery_time = truck.m_time
        package.m_departure_time = truck.m_departure_time
    except (AttributeError, IndexError) as e:
        logging.error(f'Error updating truck {truck.m_ID} status: {e}')
        raise


def m_find_nearest_package(truck: Truck, pending_packages: List[Package]) -> Tuple[Package, float]:
    """Find the nearest package in the list of packages relative to the truck's location.

    The function uses the m_calculate_distance() method used to find the distance between the truck's current
    address (truck.m_address) and each pending package's stored in (pending_packages). The min function is used
    with a custom key to find the package with minimum distance.

    :arg
        truck (Truck): The truck object used to deliver the nearest package
        pending_packages (List[Package]): A list of package objects representing packages pending to be delivered.

    :returns
        Tuple[Package, float]: A tuple containing the nearest package and the corresponding distance.

    :raises
        ValueError: If there are no pending packages in the provided list"""

    if not pending_packages:
        logging.error('No pending packages to search for the nearest one.')
        raise ValueError('No pending packages available for delivery')

    try:
        # Find nearest package using distance calculation and min function
        nearest_package = min(pending_packages,
                              key=lambda p: m_calculate_distance(truck.m_address, p.m_address))
        distance = m_calculate_distance(truck.m_address, nearest_package.m_address)
        return nearest_package, distance
    except Exception as e:
        logging.error(f'Error finding nearest package for truck {truck.m_ID}: {e}')
        raise


def m_deliver_packages(truck: Truck) -> None:
    """Delivers all pending packages using the Nearest Neighbor Algorithm.

    This function uses an iterative approach to find the nearest undelivered package with respect to the truck's
    current location. In addition, it will update the truck's status such as its mileage, address, delivery and
     departure times, along with the package's deliver information. Then the packages are delivered optimizing the
     truck's delivery route.

     :arg
        truck (Truck): The truck object with packages to be delivered

    :raises
        ValueError: If there are no pending packages in the truck. """

    try:
        # load pending packages yet to be delivered
        logging.info(f'Starting delivery for the truck')
        m_pending_packages = [m_package_hash_table.m_look_up(pID) for pID in truck.m_packages]
        truck.m_packages.clear()  # We want to insert packages according to the most efficient path so clear it

        while m_pending_packages:
            nearest_package, distance = m_find_nearest_package(truck, m_pending_packages)
            m_update_truck_status(truck, nearest_package, distance)
            m_pending_packages.remove(nearest_package)
            logging.info(f'Delivered package {nearest_package.m_ID} to {nearest_package.m_address}')

        logging.info(f'Successfully completed delivery for truck')
    except ValueError as e:
        logging.error(f'No pending packages found for the truck: {e}')


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


logging.basicConfig(filename='app.log', level=logging.DEBUG)  # configure for error tracking

m_package_file = m_load_csv_file('CSV/Package_File.csv')  # Load package file information
m_distance_file = m_load_csv_file('CSV/Distance_File.csv')  # Load distance information
m_address_file = m_load_csv_file('CSV/Address_File.csv')  # Load address information


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
