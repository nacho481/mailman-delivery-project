import logging


class HashItem:
    """
    Represents a key-value pair within a hash table.

    Attributes:
        key (object): Unique identifier for data
        value (object): Data associated with the key

    """

    def __init__(self, key, value):
        """
        Initializes a hash item

        :arg
            key (object): Unique identifier for data
            value (object): Data associated with key
        """
        self.key = key
        self.value = value
        logging.debug(f'Created HashItem: key={key}, value={value}')


class HashTable:
    """
    A hash table implementation for efficient key-value lookup.

    This class uses hash functions with empty buckets to store key-value pairs. This class provides a method for
    inserting, searching and deleting.

    :arg
        m_capacity (int): Indicates number of buckets
        m_buckets (List[HashItem]): A list containing a hashtable where each entry can be a HashItem.
        m_counter (int): The number of elements present within the hash table
    """
    def __init__(self, capacity=40):
        """
        Initializes a HashTable object.

        :arg
            capacity (int, optional): The initial capacity for the hash table

        :raises
            ValueError:
                - If the initial capacity is less than or equal to 0

        """

        if capacity <= 0:
            raise ValueError('Hash table capacity must be a positive integer.')

        self.m_capacity = capacity
        self.m_buckets = [None for i in range(capacity)]
        self.m_counter = 0

    def m_insert(self, key, item):
        """
        Inserts a key-value pair into the hash table.

        This method will create a HashItem object then it will calculate a hash for the key value to place into the
        hash table's bucket. If the bucket it hashes, then it will use linear probing to find an empty bucket to insert
        the HashItem object into.

        :arg
            key (object): The unique identifier for the data
            item (object): Data associated with the key.

        Raises:
            RuntimeError:
                - If the hash table is full (load factor exceeds a threshold)
        """

        if self.m_counter > self.m_capacity:  # Check to see if counter is greater than capacity
            raise RuntimeError('Hashtable is full. Consider increase capacity.')

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
        """Looks up a value associated with a given key in the hashtable.

        This method calculates a hash value of the key to return the value or will opt to use linear probing to find
        the bucket with the key to return the corresponding value in the HashItem object.

        :arg
            key (object): The unique identifier in the hashtable stored in a HashItem.

        :returns
            object: The value associated with the key, or None if the key is not found."""
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
        """Deletes a key-value pair from the hash table.

        This method calculates the hash value then will use linear probing if the bucket with the same key is not found
        initially, then once the proper bucket is found, it will be marked empty and the counter will decrement by 1.

        :arg
            key (object): The unique identifier for the data to be deleted"""
        h = hash(key) % self.m_capacity  # Find hash value
        while self.m_buckets[h] is not None:  # Run if it is not empty
            if self.m_buckets[h].key is key:  # When key is found
                self.m_buckets[h] = None  # Mark the bucket as empty
                self.m_counter -= 1  # Decrement the counter
                break  # Break out of function
            h = (h + 1) % self.m_capacity  # probe through list if needed
        # loop will exit if not found
