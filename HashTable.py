

class HashItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    def __init__(self, capacity = 40):
        self.m_capacity = capacity
        self.m_buckets =[None for i in range(capacity)]
        self.m_counter = 0

    def m_insert(self, key, item):
        item = HashItem(key, item)
        h = hash(key) % self.m_capacity

        while self.m_buckets[h] is not None:
            if self.m_buckets[h].key is key:  # Do not allow duplicate values
                break
            h = (h + 1) % self.m_capacity  # probe through the table

        # This means we found an open bucket that has not been assigned a value
        if self.m_buckets[h] is None:
            self.m_counter += 1
        self.m_buckets[h] = item  # insert hash item after incrementing the counter

    def m_look_up(self, key):
        h = hash(key) % self.m_capacity
        while self.m_buckets[h] is not None:
            try:
                if self.m_buckets[h].key is key:  # we found our value
                    return self.m_buckets[h].value  # return our value
            except AttributeError:  # ignore if bucket is empty
                pass
            h = (h + 1) % self.m_capacity
        return None  # if not found return none

    def m_delete(self, key):
        h = hash(key) % self.m_capacity
        while self.m_buckets[h] is not None:
            if self.m_buckets[h].key is key:
                self.m_buckets[h] = None  # Mark the bucket as empty
                self.m_counter -= 1  # Decrement the counter
                break
            h = (h + 1) % self.m_capacity  # probe through list if needed
        # loop will exit if not found

    def __setitem__(self, key, value):
        self.m_insert(key, value)

    def __getitem__(self, key):
        return self.m_look_up(key)


    # def __str__(self):
    #     result = ""
    #     for x in range(self.m_capacity):
    #         if self.m_buckets[x] is not None:
    #             result += f"Bucket {x}: (Key - {self.m_buckets[x].key}) - (Value - {self.m_buckets[x].value})\n"
    #     return result
    #
    #


# method stub
