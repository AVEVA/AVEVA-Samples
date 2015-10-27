import datetime
import math

class WaveData:
    
    def __init__(self):
        self.__Order = None
        self.__Tau = None
        self.__Radians = None
        self.__Sin = None
        self.__Cos = None
        self.__Tan = None
        self.__Sinh = None
        self.__Cosh = None
        self.__Tanh = None
    
    def getOrder(self):
        return self.__Order

    def setOrder(self, Order):
        self.__Order = Order
    
    Order = property(getOrder, setOrder)
    
    def getTau(self):
        return self.__Tau

    def setTau(self, Tau):
        self.__Tau = Tau
    
    Tau = property(getTau, setTau)

    def getRadians(self):
        return self.__Radians

    def setRadians(self, Radians):
        self.__Radians = Radians
    
    Radians = property(getRadians, setRadians)

    def getSin(self):
        return self.__Sin

    def setSin(self, Sin):
        self.__Sin= Sin
    
    Sin = property(getSin, setSin)

    def getCos(self):
        return self.__Cos

    def setCos(self, Cos):
        self.__Cos = Cos
    
    Cos = property(getCos, setCos)

    def getTan(self):
        return self.__Tan

    def setTan(self, Tan):
        self.__Tan= Tan
    
    Tan = property(getTan, setTan)

    def getSinh(self):
        return self.__Sinh 

    def setSinh(self, Sinh):
        self.__Sinh = Sinh
    
    Sinh = property(getSinh, setSinh)

    def getCosh(self):
        return self.__Cosh

    def setCosh(self, Cosh):
        self.__Cosh = Cosh
    
    Cosh = property(getCosh, setCosh)

    def getTanh(self):
        return self.__Tanh

    def setTanh(self, Tanh):
        self.__Tanh = Tanh
    
    Tanh = property(getTanh, setTanh)    
        
    def toString(self):
        return '\n'.join('Order = {0}'.format(self.__Order),
                         'Radians = {0}'.format(self.__Radians),
                         'Tau = {0}'.format(self.__Tau),
                         'Sine = {0}'.format(self.__Sin),
                         'Cosine = {0}'.format(self.__Sin),
                         'Tangent = {0}'.format(self.__Tan),
                         'Sinh = {0}'.format(self.__Tan),
                         'Cosh = {0}'.format(self.__Cosh),
                         'Tanh = {0}'.format(self.__Tanh))
        
    @staticmethod
    def nextWave(interval, multiplier, order):
        now = datetime.datetime.now()
        totalSecondsDay = (now - now.replace(hour=0, minute=0, second = 0, microsecond = 0)).total_seconds() * 1000
        intervalSeconds = (interval - interval.replace(hour=0, minute=0, second = 0, microsecond = 0)).total_seconds() * 1000
        radians = ((totalSecondsDay % intervalSeconds ) / intervalSeconds) * 2 * math.pi
        
        newWave = WaveData()
        newWave.Order = order
        newWave.Radians = radians
        newWave.Tau = radians / (2 * math.pi)
        newWave.Sin = multiplier * math.sin(radians)
        newWave.Cos = multiplier * math.cos(radians)
        newWave.Tan = multiplier * math.tan(radians)
        newWave.Sinh = multiplier * math.sinh(radians)
        newWave.Cosh = multiplier * math.cosh(radians)
        newWave.Tanh = multiplier * math.tanh(radians)
        
        return newWave