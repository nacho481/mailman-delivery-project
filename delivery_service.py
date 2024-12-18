# delivery_service.py

import datetime
import logging
from typing import List, Tuple

from HashTable import HashTable
from Package import Package
from Truck import Truck
from utils import DataManager
from config import M_HUB_ADDRESS


class DeliveryService:
    def __init__(self, trucks: List[Truck], package_hash_table: HashTable, data_manager: DataManager) -> None:
        """
        Initializes the DeliveryService object.

        :arg
            trucks (List[Truck]): A list of truck objects representing the delivery vehicles
            package_hash_table (HashTable): A HashTable used for efficient lookup by ID
            data_manager (DataManager): A DataManager object is used for loading and distance calculations

        :raises
            :TypeError
                - If any of the arguments are not of the expected types (List[Truck], HashTable, DataManager).
        """
        if not isinstance(trucks, list) or not all(isinstance(truck, Truck) for truck in trucks):
            raise TypeError('Trucks arguments must be a list of truck objects')

        self.m_trucks = trucks
        self.m_package_hash_table = package_hash_table
        self.m_data_manager = data_manager

    def update_package_9_address(self, current_time: datetime.timedelta) -> None:
        """Updates the address of package 9 if the current time is after the update time.

        This method checks if the current time has reached or passed the time when package 9's
        address should be updated. If so, it updates the package's address, city, state, and zip code.
        It also resets the package status to "At Hub" for redelivery.

        :arg
            current_time (datetime.timedelta): The current time in the simulation
        """
        package_9: Package = self.m_package_hash_table.m_look_up(9)
        package_9.update_address("410 S State St", "Salt Lake City", "UT", "84111", current_time)
        package_9.m_status = "At Hub"  # Reset status for redelivery
        logging.info(f'Updated address at package #9 at {current_time}')

    def _handle_package_9_update(self):
        """
        Handles the update and redelivery process for package 9.

        This private method manages the special case of package 9, which requires an address update
        and redelivery. It updates the package's address at a specific time, adjusts the truck's time
        if necessary, and initiates the redelivery process.
        """
        package_9: Package = self.m_package_hash_table.m_look_up(9)
        update_time = datetime.timedelta(hours=10, minutes=20)

        if self.m_trucks[2].m_time < update_time:
            self.m_trucks[2].m_time = update_time

        self.update_package_9_address(update_time)
        self._redeliver_package_9()

    def _redeliver_package_9(self):
        """
        Manages the redelivery process for package 9 after its address update.

        This method simulates the process of the truck returning to the hub, picking up package 9 from the incorrect
        address, then drops it off to the updated address. It updates the truck's (status, time, mileage, current
        address) and the package's information (departure time, delivery time, and status) respectively.
        """
        package_9: Package = self.m_package_hash_table.m_look_up(9)  # look up hashitem
        truck = self.m_trucks[2]  # reuse truck 3

        # Calculate time to return to hub
        distance_to_hub = self.m_data_manager.m_calculate_distance(truck.m_address, M_HUB_ADDRESS)
        time_to_hub = datetime.timedelta(hours=distance_to_hub / truck.m_speed)

        # Update truck status
        truck.m_time += time_to_hub
        truck.m_mileage += distance_to_hub
        truck.m_address = M_HUB_ADDRESS

        # Redeliver package 9
        distance_to_new_address = self.m_data_manager.m_calculate_distance(truck.m_address, package_9.m_address)
        time_to_new_address = datetime.timedelta(hours=distance_to_new_address / truck.m_speed)

        # Update truck and package status
        truck.m_time += time_to_new_address
        truck.m_mileage += distance_to_new_address
        truck.m_address = package_9.m_address
        package_9.m_departure_time = truck.m_time - time_to_new_address
        package_9.m_delivery_time = truck.m_time
        package_9.m_status = "Delivered"

        logging.info(f'Redelivered package 9 to correct address at {truck.m_time}')

    def m_deliver_packages(self) -> None:
        """
        Delivers all pending packages using the Nearest Neighbor Algorithm for each truck.
        This function iterates through the list of trucks calling the "_deliver_packages_for_truck() method' for each
        truck, keeping in mind that there are only 2 drives and 3 trucks, and optimizes a solution for that predicament.

        :raises
            IndexError:
                - If the list of trucks is empty
        """
        logging.info(f'Starting delivery for all trucks')

        if not self.m_trucks:
            logging.error('No trucks found for delivery. Please ensure trucks are available.')
            raise IndexError('No trucks available for delivery')

        self._deliver_packages_for_truck(self.m_trucks[0])
        self._deliver_packages_for_truck(self.m_trucks[1])

        # Set the departure time for the 3rd truck
        self.m_trucks[2].m_departure_time = min(self.m_trucks[0].m_time, self.m_trucks[1].m_time)
        self._deliver_packages_for_truck(self.m_trucks[2])  # deliver packages for 3rd truck
        self._handle_package_9_update()

        logging.info(f'Completed delivery for all trucks')

    def _deliver_packages_for_truck(self, truck: Truck) -> None:
        """Delivers all pending packages using the Nearest Neighbor Algorithm.

        This function uses an iterative approach to find the nearest undelivered package with respect to the truck's
        current location. In addition, it will update the truck's status such as its mileage, address, delivery and
         departure times, along with the package's deliver information. Then the packages are delivered optimizing the
         truck's delivery route.

         :arg
            truck (Truck): The truck object with packages to be delivered

        :raises
            ValueError: If there are no pending packages in the truck.

        Algorithm:
            1. Create a list of pending packages from the truck's package IDs.
            2. Clear the truck's current package list.
            3. While there are pending packages.
                a. Find the nearest undelivered package
                b. Add the package to the truck's delivery list
                c. Update the truck's mileage, address and time
                d. Update package's delivery and departure time.

        Note: This function assumes the global m_package_hash_table is available
            """

        try:
            # load pending packages yet to be delivered
            logging.info(f'Starting delivery for the truck')
            m_pending_packages: List[Package] = [self.m_package_hash_table.m_look_up(pID) for pID in truck.m_packages]
            # Assign truck number in list
            for pID in m_pending_packages:
                pID.m_truck = truck.m_truck_number
            truck.m_packages.clear()  # We want to insert packages according to the most efficient path so clear it

            last_delivery_time = truck.m_departure_time

            while m_pending_packages:
                self.update_package_9_address(truck.m_time)
                nearest_package, distance = self._find_nearest_package(truck, m_pending_packages)
                nearest_package.m_departure_time = last_delivery_time
                self._update_truck_status(truck, nearest_package, distance)
                last_delivery_time = nearest_package.m_delivery_time
                m_pending_packages.remove(nearest_package)

                logging.info(f'Delivered package {nearest_package.m_ID} to {nearest_package.m_address}')

            logging.info(f'Successfully completed delivery for truck')
        except ValueError as e:
            logging.error(f'No pending packages found for the truck: {e}')

    def _find_nearest_package(self, truck: Truck, pending_packages: List[Package]) -> Tuple[Package, float]:
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
            return min(
                ((package, self.m_data_manager.m_calculate_distance(truck.m_address, package.m_address))
                 for package in pending_packages),
                key=lambda x: x[1]  # the shortest distance
            )
        except Exception as e:
            logging.error(f'Error finding nearest package for truck: {e}')
            raise

    def _update_truck_status(self, truck: Truck, package: Package, distance: float) -> None:
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

            # Set the original times if they haven't been set
            if package.m_original_delivery_time is None and package.m_ID == 9:
                package.m_original_delivery_time = truck.m_time
            if package.m_original_departure_time is None and package.m_ID == 9:
                package.m_original_departure_time = truck.m_departure_time

            package.m_delivery_time = truck.m_time
        except (AttributeError, IndexError) as e:
            logging.error(f'Error updating truck status: {e}')
            raise

    def m_get_total_mileage(self) -> float:
        """Calculates the total mileage driven by all trucks.

        This function will iterate through the list of trucks incrementing their mileage attributes summing it.

        :returns
            float: The total mileage driven by all trucks combined."""
        return sum(truck.m_mileage for truck in self.m_trucks)

    def m_get_completion_time(self):
        """Returns latest deliver indicating the completion time and all deliveries have been made.

        :return: The time when all deliveries are completed.
        :rtype: datetime.timedelta"""
        return max(truck.m_time for truck in self.m_trucks)
