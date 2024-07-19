# utils.py
import csv
import logging
from typing import List


class DataManager:
    """Manages data related to the package. It uses a lot of helper methods.

    This class provides methods for loading CSV data, extracting an address which returns a vertex's label or
    ID, a helper method to calculate the distance, then the actual method to calculate the distance.

    Attributes
        m_package_file (List[List[str]]): A list of list containing package data loaded from the corresponding CSV file
        m_distance_file (List[List[str]]): A list of list containing the adjacent matrix for distance calculations
        m_address_file (List[List[str]]): A list of list containing address data used to extract the vertex's label or
            ID
    """
    def __init__(self, package_file: str, distance_file: str, address_file: str):
        """Initializes a DataManager object.

        This constructor loads data from three CSV files.

        :arg
            m_package_file (List[List[str]]): A list of list containing package data loaded from the corresponding
                CSV file 'Package_File.csv'
            m_distance_file (List[List[str]]): A list of list containing the adjacent matrix for distance calculations
                for the corresponding CSV file 'Distance_File.csv'
            m_address_file (List[List[str]]): A list of list containing address data used to extract the vertex's label
                or ID from the corresponding 'Address_File.csv'
        """
        self.m_package_file = self.m_load_csv_file(package_file)
        self.m_distance_file = self.m_load_csv_file(distance_file)
        self.m_address_file = self.m_load_csv_file(address_file)

    @staticmethod
    def m_load_csv_file(filename: str) -> List[List[str]]:
        """
        Loads a CSV file into a lists of lists

        :arg
            filename: The path to the CSV file

        :returns
            A lists of lists where each inner list represents a row from the CSV file.

        :raises
            FileNotFound: When a file is not found
            csv.Error parsing the CSV file sent
            :exception
        """
        try:
            with open(filename, 'r') as file:
                return list(csv.reader(file))
        except FileNotFoundError:
            logging.error(f'File not found {filename}')
            raise
        except csv.Error as e:
            logging.error(f'CSV error in file {filename}: {e}')
            raise
        except Exception as e:
            logging.error(f'Unexpected error when reading {filename}: {e}')

    def m_extract_address(self, address: str) -> int:
        """
        Provided the address, this will extract the label (vertex ID).

        Assuming the 'm_address_file' holds the address data, this method will search for the row where the 'address'
        field matches the provided 'address' argument. If a match is found, this will return the corresponding
        vertex ID.

        :arg
            address (str): The address string to search for

        :return
            int: The vertex ID (label) associated with the address, or it will raise an exception if it's not found.
        :raises
            ValueError: If the address data is not a list of a list OR if the vertex ID cannot be converted to an integer
        """

        if not isinstance(self.m_address_file, list):
            raise ValueError('Address data (m_address_file) must be a list of lists.')
        try:
            for row in self.m_address_file:
                if address in row[2]:
                    return int(row[0])
            raise ValueError(f'Address {address} not found in address data.')
        except (TypeError, ValueError) as e:
            logging.error(f"Error extracting address label for '{address}': {e}")

    def m_distance_between(self, x_value: int, y_value: int) -> float:
        """
        Returns the distance between two locations given their indices in the adjacent matrix.

        This function assumes that the adjacent matrix with weighted edges is stored in the 'm_distance_file' variable.
        Then, it'll look up the x and y value, or the row and column value respectively within the matrix. However, if
        that value is empty, it'll check the mirrored position, (col, row) or (y_value, x_value) respectively, to retrieve
        the distance.

        :arg
            x_value (int): Row index in adjacent matrix
            y_value (int): Column index in adjacent matrix

        :returns
            float: Returns the distance between the two locations OR raises an exception if not found.


        """
        try:
            # check for out of bounds
            if x_value < 0 or x_value >= len(self.m_distance_file):
                logging.error(f'x_value ({x_value}) is out of bounds for the distance matrix')
                raise IndexError(f'x_value ({x_value}) is out bounds for the distance matrix.')
            if y_value < 0 or y_value >= len(self.m_distance_file):
                logging.error(f'y_value ({y_value}) is out of bounds for the distance matrix')
                raise IndexError(f'y_value ({y_value}) is out of bounds for the distance matrix')

            # Access distance value and convert to float
            distance = self.m_distance_file[x_value][y_value]
            if distance == '':
                distance = self.m_distance_file[y_value][x_value]
                if distance == '':
                    logging.error('Distance is not found between locations')
                    raise ValueError('Distance is not found between locations')
            return float(distance)
        except (IndexError, ValueError) as e:
            logging.error(f'Error getting distance between {x_value} and {y_value}: {e}')
            raise

    def m_calculate_distance(self, address1: str, address2: str) -> float:
        """A helper method to calculate the distance between 2 addresses, one that is passed and the second
        referencing the adjacent matrix.

        This function utilizes the 'm_extract_address()' method to obtain the vertex's label, in this case, their ID
        respectively to 'address1' and 'address2'. The distance is determined with the return statement calling
        the 'm_distance_between', functionality is discussed in the respective method.

        :arg
            address1 (str): The first address is a string
            address2 (str): The second address is a string.

        :returns
            float: The distance between the two addresses or raises an exception if an error occurs.

        :raises
            ValueError: If one or both addresses cannot be found in the address CSV file."""
        try:
            # Extract vertex labels for addresses
            idx1 = self.m_extract_address(address1)
            idx2 = self.m_extract_address(address2)
            return self.m_distance_between(idx1, idx2)  # Find distance using m_distance_between() method
        except ValueError as e:
            logging.error(f'Error calculating distance: {e}')
            raise
