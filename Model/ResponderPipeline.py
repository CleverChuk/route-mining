#!/usr/bin/python
#-*- coding: utf-8 -*-

from collections import deque
from Responder import Responder

class ResponderPipeline(Responder):
    """
        
    """
    def __init__(self):
        self.responders = deque()

    def add_first(self, responder):
        self.responders.appendleft(responder)

    def add_last(self, responder):
        self.responders.append(responder)

    def respond(self, addresses):
        for responder in self.responders:
            response = responder.respond(addresses)
        
        return response

