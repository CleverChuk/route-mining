#!/usr/bin/python
#-*- coding: utf-8 -*-


class FileHandler:
    """
        abstract class for file handlers
    """
    def __init__(self):
        self.next_handler = None

    def handle(self, filename):
        pass
        
