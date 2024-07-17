class Package:
    def __init__(self, ID, address, city, state, zip, deadline, weight, status):
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
        return (f"{self.m_ID}, {self.m_address}, {self.m_city}, {self.m_state}, {self.m_zip}, {self.m_deadline}, "
                f"{self.m_weight}, Delivery time: {self.m_delivery_time}, Departure time: {self.m_departure_time}, "
                f"{self.m_status}")


    def m_update_status(self, time):
        # print(f'Delivery time: {self.m_delivery_time}\nTime: {time}')
        if self.m_delivery_time < time:
            self.m_status = "Delivered"
        elif self.m_departure_time > time:
            self.m_status = "En route"
        else:
            self.m_status = "At Hub"


