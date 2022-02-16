#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from typing import List
import pandas as pd

from lib.address import Address, AddressBuilder
from lib.file_io import default_file_io_factory


class FileHandler:
    """
        Abstract class for file handler
        This provides extensibility for adding different file type handler
    """

    def __init__(self):
        self.next_handler: FileHandler = None

    def handle(self, filename: str) -> List[Address]:
        raise NotImplementedError


class ExcelFileHandler(FileHandler):
    """
        A file handler for parsing addresses from excel file
    """

    def __init__(self):
        super().__init__()

    def handle(self, filename: str) -> List[Address]:
        """
            Create a list of Address from excel file
        """
        from flask import current_app
        file_io = default_file_io_factory.create(current_app.env)
        file_extension = os.path.splitext(filename)[1]

        if file_extension in [".xlsx", ".xls"]:
            address_df = pd.read_excel(file_io.read(filename))
            address_df["apt_number"] = address_df["apt_number"].fillna("")
            addresses = []

            for _, row in address_df.iterrows():
                try:
                    address = AddressBuilder()\
                        .street_number(row["street_number"])\
                        .street_name(row["street_name"])\
                        .apt_number(row["apt_number"])\
                        .city(row["city"])\
                        .state(row["state"])\
                        .zip(row["zip"])\
                        .build()
                    addresses.append(address)

                except KeyError as keyError:
                    print(keyError)
                    raise keyError

            return addresses

        return self.next_handler.handle(filename)


class FileHandlerChain(FileHandler):
    """
        Handler chain that prepares and starts the execution of file handlers.
        The order in which the handlers are added doesn't matter since execution terminates
        with one successful handling otherwise it falls of the tail of the chain
    """

    def __init__(self):
        self.head = None
        self.next_handler = None

    def add_handler(self, file_handler: FileHandler) -> None:
        """
            Add a filehandler to the tail of the chain
        """
        if not self.head:
            self.head = self.next_handler = file_handler
        else:
            self.next_handler.next_handler = file_handler
            self.next_handler = file_handler

    def handle(self, filename: str) -> List[Address]:
        """
            Executes the handler chain
        """
        head = self.head
        try:
            return (None, head.handle(filename))

        except Exception as e:
            return (e, f"No handler found for {filename}")
