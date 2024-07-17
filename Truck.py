class Truck:
    def __init__(self, capacity, speed, packages, mileage, address, depart_time, load):
        self.m_capacity = capacity
        self.m_speed = speed
        self.m_packages = packages
        self.m_mileage = mileage
        self.m_address = address
        self.m_departure_time = depart_time
        self.m_time = depart_time
        self.m_load = load

    def __str__(self):
        return (f"{self.m_capacity}, {self.m_speed}, {self.m_load}, {self.m_packages}, {self.m_mileage}, "
                f"{self.m_address}, {self.m_departure_time}")
