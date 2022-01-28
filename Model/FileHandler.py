#!/usr/bin/python
#-*- coding: utf-8 -*-


class FileHandler:
    """
        Abstract class for file handler
        This provides extensibility for adding different file type handler
    """
    def __init__(self):
        self.next_handler = None

    def handle(self, filename):
        pass
        
