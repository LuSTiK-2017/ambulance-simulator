from src.model.iterator import *


class Car:
    iterator = Iterator()

    def __init__(self):
        super().__init__()

        self.__id = next(self.iterator)
        self.__status = True

    @property
    def id(self):
        return self.__id

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status
