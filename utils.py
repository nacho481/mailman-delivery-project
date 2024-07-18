# utils.py
import csv
import logging
from typing import List


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


