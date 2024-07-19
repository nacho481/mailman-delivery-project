import logging


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

    def __str__(self):
        """Returns a string representation of the package's details

        :returns
            str: A formatted string containing package information."""
        return (f"{self.m_ID}, {self.m_address}, {self.m_city}, {self.m_state}, {self.m_zip}, {self.m_deadline}, "
                f"{self.m_weight}, Delivery time: {self.m_delivery_time}, Departure time: {self.m_departure_time}, "
                f"{self.m_status}")

    def m_update_status(self, time):
        """
        Updates the package status based on the current time with respect to the delivery time or departure time,
        depending on which one is available.

        :arg
            time (datetime.timedelta): The current time for comparison
        """
        # print(f'Delivery time: {self.m_delivery_time}\nTime: {time}')
        if self.m_delivery_time < time:
            self.m_status = "Delivered"
            logging.info(f'Package {self.m_ID} status updated to Delivered.')
        elif self.m_departure_time > time:
            self.m_status = "En route"
            logging.info(f'Package {self.m_ID} status updated to En route.')
        else:
            self.m_status = "At Hub"
            logging.info(f'Package {self.m_ID} status updated to At hub .')


