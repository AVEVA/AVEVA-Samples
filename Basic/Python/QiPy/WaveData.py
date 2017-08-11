import datetime
import math
import json
import inspect

class WaveData:
    """Represents a data point to be injected into Qi Service"""
    
    def __init__(self):
        self._order = None
        self._tau = None
        self._radians = None
        self._sin = None
        self._cos = None
        self._tan = None
        self._sinh = None
        self._cosh = None
        self._tanh = None
    
    @property
    def Order(self):
        return self._order
    @Order.setter
    def Order(self, order):
        self._order = order

    @property
    def Tau(self):
        return self._tau
    @Tau.setter
    def Tau(self, tau):
        self._tau = tau
    
    @property
    def Radians(self):
        return self._radians
    @Radians.setter
    def Radians(self, radians):
        self._radians = radians
    
    @property
    def Sin(self):
        return self._sin
    @Sin.setter
    def Sin(self, sin):
        self._sin = sin
    
    @property
    def Cos(self):
        return self._cos
    @Cos.setter
    def Cos(self, cos):
        self._cos = cos

    @property
    def Tan(self):
        return self._tan
    @Tan.setter
    def Tan(self, tan):
        self._tan = tan

    @property
    def Sinh(self):
        return self._sinh
    @Sinh.setter
    def Sinh(self, sinh):
        self._sinh = sinh

    @property
    def Cosh(self):
        return self._cosh
    @Cosh.setter
    def Cosh(self, cosh):
        self._cosh = cosh
    
    @property
    def Tanh(self):
        return self._tanh
    @Tanh.setter
    def Tanh(self, tanh):
        self._tanh = tanh
        
    def isprop(v):
        return isinstance(v, property)

    def toJsonString(self):
        string = ""
        for prop in inspect.getmembers(type(self), lambda v : isinstance(v, property)):
            value = prop[1].fget(self)
            if value is None:
                string += "{name}: , ".format(name = prop[0])
            else:
                string += "{name}: {value}, ".format(name = prop[0], value = value)
        return string

    @staticmethod
    def fromJson(jsonObj):
        if jsonObj is None:
            return None
        wave = WaveData()
        properties = inspect.getmembers(type(wave), lambda v : isinstance(v, property))
        for prop in properties:
            # Pre-Assign the default
            prop[1].fset(wave, 0)

            # If found in JSON object, then set
            if prop[0] in jsonObj:
                value = jsonObj[prop[0]]
                if value is not None:
                    prop[1].fset(wave, value)
        return wave
