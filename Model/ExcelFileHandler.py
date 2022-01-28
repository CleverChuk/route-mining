#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from typing import IO, Any
from FileHandler import FileHandler
import pandas as pd

from Model.AddressBuilder import AddressBuilder


class ExcelFileHandler(FileHandler):
    """
        A file handler for parsing addresses from excel file
    """
    def __init__(self):
        self.next_handler = None

    def handle(self, filename: str):
        if os.path.splitext(filename)[1] in ["xlsx","xls"]:
            address_df = pd.read_excel(filename)
            addresses = []

            for _, row in address_df.iterrows():
                try:
                    address = AddressBuilder()\
                        .street_number(row["street number"])\
                        .street_name(row["street name"])\
                        .apt_number("apt number")\
                        .city(row["city"])\
                        .state(row["state"])\
                        .zip(row["zip"])\
                        .build()
                    addresses.append(address)

                except KeyError as keyError:
                    print(keyError)

            return addresses
        
        return self.next_handler.handle(filename)
