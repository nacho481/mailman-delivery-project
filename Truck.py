# Truck.py
class Truck:
    """
    Holds information for the truck class representing attributes and methods to maintain the truck object.

    Attributes:
        m_capacity (int): The number of packages that can be held
        m_speed (int): The speed of the truck (which is a constant, you can see the value in config.py).
        m_packages (list[Package]): A list of Package objects assigned to the truck.
        m_mileage (float): The total mileage accumulated by the truck.
        m_address (str): The starting address of the truck.
        m_departure_time (str): The scheduled departure time for the truck.
        m_time (str): The current time of the truck (used for tracking deliveries).
        m_load (object): Keeps track if the truck is loaded or not, will be utilized in future iteration.

    """
    def __init__(self, capacity, speed, packages, mileage, address, depart_time, load, truck_number):
        """
        Initializes the Truck class for you

        :arg
            capacity (int): The number of packages that can be held
            speed (int): The speed of the truck (which is a constant, you can see the value in config.py).
            packages (list[Package]): A list of Package objects assigned to the truck.
            mileage (float): The total mileage accumulated by the truck.
            address (str): The starting address of the truck.
            departure_time (str): The scheduled departure time for the truck.
            time (str): The current time of the truck (used for tracking deliveries).
            load (object): Keeps track if the truck is loaded or not, will be utilized in future iteration.
        """
        self.m_capacity = capacity
        self.m_speed = speed
        self.m_packages = packages
        self.m_mileage = mileage
        self.m_address = address
        self.m_departure_time = depart_time
        self.m_time = depart_time
        self.m_load = load
        self.m_truck_number = truck_number

    def __str__(self):
        """Returns a string representation of the truck object.

        :returns
            all the attributes minus one that the truck object contains."""
        return (f"{self.m_capacity}, {self.m_speed}, {self.m_load}, {self.m_packages}, {self.m_mileage}, "
                f"{self.m_address}, {self.m_departure_time}")
