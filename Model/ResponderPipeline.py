#!/usr/bin/python
#-*- coding: utf-8 -*-

from Responder import Responder

class ResponderPipeline(Responder):
    def __init__(self):
        self.head = None
        self.tail = None

    def add_first(self, responder):
        pass

    def add_last(self, responder):
        pass

    def respond(self, addresses):
        pass

