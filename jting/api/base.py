# coding: utf-8

class ApiBlueprint(object):
    def __init__(self, name):
        self.name = name
        self.deferred = []