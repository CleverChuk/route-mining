#!/usr/bin/python
#-*- coding: utf-8 -*-

from Handler import Handler

class FileHandler(Handler):
    def __init__(self):
        self.next_handler = None

    def handle(self, file):
        pass

