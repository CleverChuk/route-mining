#!/usr/bin/python
#-*- coding: utf-8 -*-


import os
import pandas as pd

from lib.model import AddressBuilder

class FileHandler:
    """
        Abstract class for file handler
        This provides extensibility for adding different file type handler
    """
    def __init__(self):
        self.next_handler = None

    def handle(self, filename):
        pass
        
class ExcelFileHandler(FileHandler):
    """
        A file handler for parsing addresses from excel file
    """
    def __init__(self):
        self.next_handler = None

    def handle(self, filename: str):
        file_extension = os.path.splitext(filename)[1]        
        if file_extension in [".xlsx",".xls"]:
            address_df = pd.read_excel(filename)
            address_df["apt number"] = address_df["apt number"].fillna(0)
            addresses = []

            for _, row in address_df.iterrows():
                try:
                    address = AddressBuilder()\
                        .street_number(row["street number"])\
                        .street_name(row["street name"])\
                        .apt_number(row["apt number"])\
                        .city(row["city"])\
                        .state(row["state"])\
                        .zip(row["zip"])\
                        .build()
                    addresses.append(address)

                except KeyError as keyError:
                    print(keyError)

            return addresses
        
        return self.next_handler.handle(filename)



class FileHandlerChain(FileHandler):
    """
        Handler chain that  prepares and starts execution of the file handlers.
        The order in which the handlers added doesn't matter since execution terminates
        with one successful handling otherwise it falls of the tail of the chain
    """
    
    def __init__(self):
        self.head = None
        self.next_handler = None

    def addHandler(self, file_handler):
        if not self.head:
            self.head = self.next_handler = file_handler
        else:
            self.next_handler.next_handler = file_handler
            self.next_handler = file_handler

    def handle(self, filename):
        head = self.head
        try:
            return head.handle(filename)

        except Exception as e:
            print(e)
            return f"No handler found for {filename}"

        
