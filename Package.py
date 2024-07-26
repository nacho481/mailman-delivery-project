# Package.py
import logging
import datetime

class Package:
    """
        Represents a package with its details and delivery status.

        Attributes:
            m_ID (object): The unique identifier of the package.
            m_address (str): The delivery address of the package.
            m_city (str): The city where the package will be delivered.
            m_state (str): The state where the package will be delivered.
            m_zip (str): The zip code of the delivery location.
            m_deadline (str): The deadline for delivery.
            m_weight (str): The weight of the package.
            m_status (str): The current status of the package (e.g., "En route", "Delivered").
            m_departure_time (datetime.datetime): The time the package departed from the hub. (Optional)
            m_delivery_time (datetime.datetime): The time the package was delivered. (Optional)
        """
    def __init__(self, ID, address, city, state, zip, deadline, weight, status):
        """
        Initializes a Package object.

        :arg
            m_ID (str): The unique identifier of the package.
            m_address (str): The delivery address of the package.
            m_city (str): The city where the package will be delivered.
            m_state (str): The state where the package will be delivered.
            m_zip (str): The zip code of the delivery location.
            m_deadline (datetime.date): The deadline for delivery.
            m_weight (float): The weight of the package.
            m_status (str): The current status of the package (e.g., "En route", "Delivered").
            m_departure_time (datetime.datetime): The time the package departed from the hub. (Optional)
            m_delivery_time (datetime.datetime): The time the package was delivered. (Optional)
    """
        self.m_ID = ID
        self.m_address = address
        self.m_city = city
        self.m_state = state
        self.m_zip = zip
        self.m_deadline = deadline
        self.m_weight = weight
        self.m_status = status
        self.m_departure_time = None
        self.m_delivery_time = None

        # in preparation for package 9
        self.m_original_address = address
        self.m_original_city = city
        self.m_original_state = state
        self.m_original_zip = zip
        self.m_address_update_time = None
        self.m_original_departure_time = None
        self.m_original_delivery_time = None
        self.m_truck = None  # Keep track of which truck it is on

    def __str__(self):
        """Returns a string representation of the package's details

        :returns
            str: A formatted string containing package information."""
        return self.m_get_status_string(None)
        # return (f"{self.m_ID}, {self.m_address}, {self.m_city}, {self.m_state}, {self.m_zip}, {self.m_deadline}, "
        #         f"{self.m_weight}, Delivery time: {self.m_delivery_time}, Departure time: {self.m_departure_time}, "
        #         f"{self.m_status}")

    def m_get_status_string(self, current_time: datetime.timedelta):
        address = self.m_address
        city = self.m_city
        state = self.m_state
        intermediate_zip = self.m_zip
        delivery_time = self.m_delivery_time
        departure_time = self.m_departure_time

        if self.m_address_update_time and current_time:
            if current_time < self.m_address_update_time:
                address = self.m_original_address
                city = self.m_original_city
                state = self.m_original_state
                intermediate_zip = self.m_original_zip
                delivery_time = self.m_original_delivery_time
                departure_time = self.m_original_departure_time

        truck_info = f'on Truck #{self.m_truck}' if self.m_truck else 'not assigned'
        return (f"{self.m_ID}, {address}, {city}, {state}, {intermediate_zip}, "
                f"{self.m_deadline}, {self.m_weight}, Delivery time: {delivery_time}, "
                f"Departure time: {departure_time}, {self.m_status}, {truck_info}")

    def m_update_status(self, time):
        """
        Updates the package status based on the current time with respect to the delivery time or departure time,
        depending on which one is available.

        :arg
            time (datetime.timedelta): The current time for comparison
        """

        if self.m_ID == 9 and self.m_address_update_time:
            if self.m_address_update_time <= time < self.m_departure_time:
                self.m_status = 'En route'  # Say it's in route when it's on its way to pick up the package
                return  # exit function

        delivery_time = self.m_original_delivery_time if (
                    self.m_address_update_time and time < self.m_address_update_time) else self.m_delivery_time
        departure_time = self.m_original_departure_time if (
                    self.m_address_update_time and time < self.m_address_update_time) else self.m_departure_time

        if delivery_time and time >= delivery_time:
            self.m_status = "Delivered"
            logging.info(f'Package {self.m_ID} status updated to Delivered.')
        elif departure_time and time >= departure_time:
            self.m_status = "En route"
            logging.info(f'Package {self.m_ID} status updated to En route.')
        else:
            self.m_status = "At Hub"
            logging.info(f'Package {self.m_ID} status updated to At hub .')

    def update_address(self, new_address, new_city, new_state, new_zip, update_time):
        self.m_address = new_address
        self.m_city = new_city
        self.m_state = new_state
        self.m_zip = new_zip
        self.m_address_update_time = update_time