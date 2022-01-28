#!/usr/bin/python
#-*- coding: utf-8 -*-

from FileHandler import FileHandler

class HandlerChain(FileHandler):
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
            return f"No handler found for {filename}"

        

