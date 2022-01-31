#!/usr/bin/python
#-*- coding: utf-8 -*-

from Handler import Handler

class HandlerChain(Handler):
    def __init__(self):
        self.head = None
        self.tail = None

    def addHandler(self, file_handler):
        pass

