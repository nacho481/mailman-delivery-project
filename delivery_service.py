# delivery_service.py

import logging
import datetime
from typing import List
from Truck import Truck
from Package import Package
from HashTable import HashTable
from utils import DataManager


class DeliveryService:
    def __init__(self, trucks: List[Truck], package_hash_table: HashTable, data_manager: DataManager):
        self.m_trucks = trucks
        self.m_package_hash_table = package_hash_table
        self.m_data_manager = data_manager

    def m_deliver_packages(self):
        self._deliver_packages_for_truck(self.m_trucks[0])
        self._deliver_packages_for_truck(self.m_trucks[1])

        # Set the departure time for the 3rd truck
        self.m_trucks[2].m_departure_time = min(self.m_trucks[0].m_time, self.m_trucks[1].m_time)
        self._deliver_packages_for_truck(self.m_trucks[2])  # deliver packages for 3rd truck

    def _deliver_packages_for_truck(self, truck: Truck):
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
            m_pending_packages = [self.m_package_hash_table.m_look_up(pID) for pID in truck.m_packages]
            truck.m_packages.clear()  # We want to insert packages according to the most efficient path so clear it

            while m_pending_packages:
                nearest_package, distance = self._find_nearest_package(truck, m_pending_packages)
                self._update_truck_status(truck, nearest_package, distance)
                m_pending_packages.remove(nearest_package)
                logging.info(f'Delivered package {nearest_package.m_ID} to {nearest_package.m_address}')

            logging.info(f'Successfully completed delivery for truck')
        except ValueError as e:
            logging.error(f'No pending packages found for the truck: {e}')

    def _find_nearest_package(self, truck: Truck, pending_packages: List[Package]):
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
            # nearest_package = min(pending_packages,
            #                       key=lambda p: self.m_data_manager.m_calculate_distance(truck.m_address, p.m_address))
            # distance = self.m_calculate_distance(truck.m_address, nearest_package.m_address)
            # return nearest_package, distance
            return min(
                ((package, self.m_data_manager.m_calculate_distance(truck.m_address, package.m_address))
                 for package in pending_packages),
                key=lambda x: x[1]  # the shortest distance
            )
        except Exception as e:
            logging.error(f'Error finding nearest package for truck: {e}')
            raise

    def _update_truck_status(self, truck: Truck, package: Package, distance: float):
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
            logging.error(f'Error updating truck status: {e}')
            raise

    def m_get_total_mileage(self):
        return sum(truck.m_mileage for truck in self.m_trucks)