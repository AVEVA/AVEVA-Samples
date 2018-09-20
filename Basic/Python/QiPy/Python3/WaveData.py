import datetime
import math
import json
import inspect

class WaveData:
    """Represents a data point to be injected into Sds Service"""
    
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

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        dictionary = { }
        for prop in inspect.getmembers(type(self), lambda v : isinstance(v, property)):
            if hasattr(self, prop[0]):
                dictionary[prop[0]] = prop[1].fget(self)

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return WaveData.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        wave = WaveData()

        if len(content) == 0:
            return wave

        for prop in inspect.getmembers(type(wave), lambda v : isinstance(v, property)):
            # Pre-Assign the default
            prop[1].fset(wave, 0)

            # If found in JSON object, then set
            if prop[0] in content:
                value = content[prop[0]]
                if value is not None:
                    prop[1].fset(wave, value)

        return wave



class WaveDataInteger:
    """Represents a data point to be injected into Sds Service"""
    
    def __init__(self):
        self._OrderTarget = None
        self._SinInt = None
        self._CosInt = None
        self._TanInt = None
   
    @property
    def OrderTarget(self):
        return self._OrderTarget
    @OrderTarget.setter
    def OrderTarget(self, OrderTarget):
        self._OrderTarget = OrderTarget
    
    @property
    def SinInt(self):
        return self._SinInt
    @SinInt.setter
    def SinInt(self, SinInt):
        self._SinInt = SinInt
    
    @property
    def CosInt(self):
        return self._CosInt
    @CosInt.setter
    def CosInt(self, CosInt):
        self._CosInt = CosInt

    @property
    def TanInt(self):
        return self._TanInt
    @TanInt.setter
    def TanInt(self, TanInt):
        self._TanInt = TanInt
        
    def isprop(v):
        return isinstance(v, property)

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        dictionary = { }
        for prop in inspect.getmembers(type(self), lambda v : isinstance(v, property)):
            if hasattr(self, prop[0]):
                dictionary[prop[0]] = prop[1].fget(self)

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return WaveDataInteger.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        wave = WaveDataInteger()

        if len(content) == 0:
            return wave

        for prop in inspect.getmembers(type(wave), lambda v : isinstance(v, property)):
            # Pre-Assign the default
            prop[1].fset(wave, 0)

            # If found in JSON object, then set
            if prop[0] in content:
                value = content[prop[0]]
                if value is not None:
                    prop[1].fset(wave, value)
        return wave


class WaveDataTarget:
    """Represents a data point to be injected into Sds Service"""
    
    def __init__(self):
        self._OrderTarget = None
        self._TauTarget = None
        self._RadiansTarget = None
        self._SinTarget = None
        self._CosTarget = None
        self._TanTarget = None
        self._SinhTarget = None
        self._CoshTarget = None
        self._TanhTarget = None
    
    @property
    def OrderTarget(self):
        return self._OrderTarget
    @OrderTarget.setter
    def OrderTarget(self, OrderTarget):
        self._OrderTarget = OrderTarget

    @property
    def TauTarget(self):
        return self._TauTarget
    @TauTarget.setter
    def TauTarget(self, TauTarget):
        self._TauTarget = TauTarget
    
    @property
    def RadiansTarget(self):
        return self._RadiansTarget
    @RadiansTarget.setter
    def RadiansTarget(self, RadiansTarget):
        self._RadiansTarget = RadiansTarget
    
    @property
    def SinTarget(self):
        return self._SinTarget
    @SinTarget.setter
    def SinTarget(self, SinTarget):
        self._SinTarget = SinTarget
    
    @property
    def CosTarget(self):
        return self._CosTarget
    @CosTarget.setter
    def CosTarget(self, CosTarget):
        self._CosTarget = CosTarget

    @property
    def TanTarget(self):
        return self._TanTarget
    @TanTarget.setter
    def TanTarget(self, TanTarget):
        self._TanTarget = TanTarget

    @property
    def SinhTarget(self):
        return self._SinhTarget
    @SinhTarget.setter
    def SinhTarget(self, SinhTarget):
        self._SinhTarget = SinhTarget

    @property
    def CoshTarget(self):
        return self._CoshTarget
    @CoshTarget.setter
    def CoshTarget(self, CoshTarget):
        self._CoshTarget = CoshTarget
    
    @property
    def TanhTarget(self):
        return self._TanhTarget
    @TanhTarget.setter
    def TanhTarget(self, TanhTarget):
        self._TanhTarget = TanhTarget
        
    def isprop(v):
        return isinstance(v, property)

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        dictionary = { }
        for prop in inspect.getmembers(type(self), lambda v : isinstance(v, property)):
            if hasattr(self, prop[0]):
                dictionary[prop[0]] = prop[1].fget(self)

        return dictionary

    @staticmethod
    def fromJson(jsonObj):
        return WaveDataTarget.fromDictionary(jsonObj)

    @staticmethod
    def fromDictionary(content):
        wave = WaveDataTarget()

        if len(content) == 0:
            return wave

        for prop in inspect.getmembers(type(wave), lambda v : isinstance(v, property)):
            # Pre-Assign the default
            prop[1].fset(wave, 0)

            # If found in JSON object, then set
            if prop[0] in content:
                value = content[prop[0]]
                if value is not None:
                    prop[1].fset(wave, value)

        return wave
