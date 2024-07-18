# Author: Ignacio-Manuel Atilano
# ID: 010260310

import csv
import datetime
import logging


from Truck import Truck
from HashTable import HashTable
from Package import Package
from config import M_TRUCK_CONFIGS, M_PACKAGE_FILE, M_DISTANCE_FILE, M_ADDRESS_FILE
from utils import DataManager
from delivery_service import DeliveryService


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


def m_get_user_time() -> datetime.timedelta:
    """Prompt the user to enter a specific time in HH:MM format to check the status of a package (or packages).

        This function validates the user input to ensure it's in the correct format (HH:MM) then it'll return the
        datetime.timedelta object provided the user's input. The loop will continue to prompt the user until their
        input is valid

    :returns
        datetime.timedelta: A timedelta object representing the user-provided time.

    :raises
        ValueError: If the user enters and invalid format.
    """
    while True:
        user_time = input("Enter time to check the status of a package in HH:MM format: ")
        try:
            (h, m) = map(int, user_time.split(':'))  # specify data type then iterable which is the split string
            # Validate hours and minutes
            if not 0 <= h <= 23 or not 0 <= m <= 59:
                raise ValueError('Invalid time entered. Hours are between 0-23 and minutes between 0-59.')
            return datetime.timedelta(hours=int(h), minutes=int(m))
        except ValueError:
            print("Invalid time format. Please try again (HH:MM).")  # prompt user to re-enter value correctly


def m_get_package_selection():
    """Prompts the user to select whether they want an update on one particular package or an update on
    all the packages. It also validates the user's input.

    :returns
        int: An integer representing the user's selection (1 for one package, 2 for all).
    :raises
        ValueError: If the user enters an invalid input that cannot be converted to an integer."""
    # Ensures we get right data type from user
    while True:
        selection = input("Enter (1 for 1 package) or (2 for all packages): ")
        try:
            if selection in ("1", "2"):  # We want either 1 or 2
                return int(selection)
            else:
                # Reprompt the user to enter a correct value
                raise ValueError("Invalid selection. Please enter 1 or 2.")
        except ValueError as e:
            print(f'Invalid input: {e}. Please enter 1 or 2.')  # More informative error message


def main():
    """Entry point for the Western Governors University Parcel Service program.

    It displays as the program's starting point, showing total miles and a welcoming message. The user will be provided
    options to check the delivery status of 1 or all packages depending on their selection.

    :raises
        ValueError: If invalid user input is encountered during the time conversion or package ID lookup.
    """

    data_manager = DataManager(M_PACKAGE_FILE, M_DISTANCE_FILE, M_ADDRESS_FILE)  # Initialize data manager
    trucks = [Truck(**config) for config in M_TRUCK_CONFIGS]  # initialize trucks
    package_hash_table = HashTable()  # Initialize package hash map
    m_load_package_data(M_PACKAGE_FILE, package_hash_table)  # Load data into hash table
    delivery_service = DeliveryService(trucks, package_hash_table, data_manager)  # Initialize delivery service
    delivery_service.m_deliver_packages()  # Deliver packages

    # title
    print("Western Governors University Parcel Service")  # Show delivery service name
    # total miles for all the trucks
    # print(f"Total miles: {m_truck1.m_mileage + m_truck2.m_mileage + m_truck3.m_mileage} miles")
    # print(f'Total miles: {trucks[0].m_mileage + trucks[1].m_mileage + trucks[2].m_mileage}')
    print(f'Total miles: {delivery_service.m_get_total_mileage():.2f} miles')

    while True:
        text = input("To start please type 's' for start: ")
        if text == 's':
            try:
                convert_timedelta = m_get_user_time()  # Get time from user
                selection = m_get_package_selection()  # See what option they want displayed

                if selection == 1:
                    try:
                        one_input = input("Enter package ID: ")
                        package = package_hash_table.m_look_up(int(one_input))
                        print(str(package))
                        break
                    except ValueError:
                        print('Invalid package ID. Closing program.')
                        exit()
                elif selection == 2:
                    for x in range(1, 41):
                        package = package_hash_table.m_look_up(x)
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


if __name__ == "__main__":
    main()
