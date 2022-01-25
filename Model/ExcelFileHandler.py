#!/usr/bin/python
#-*- coding: utf-8 -*-

from FileHandler import FileHandler

class ExcelFileHandler(FileHandler):
    def __init__(self):
        self.next_handler = None

    def handle(self, file):
        pass

