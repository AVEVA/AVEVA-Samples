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
    
    @property
    def Order(self):
        return self.__order
    @Order.setter
    def Order(self, order):
        self.__order = order

    @property
    def Tau(self):
        return self.__tau
    @Tau.setter
    def Tau(self, tau):
        self.__tau = tau
    
    @property
    def Radians(self):
        return self.__radians
    @Radians.setter
    def Radians(self, radians):
        self.__radians = radians
    
    @property
    def Sin(self):
        return self.__sin
    @Sin.setter
    def Sin(self, sin):
        self.__sin = sin
    
    @property
    def Cos(self):
        return self.__cos
    @Cos.setter
    def Cos(self, cos):
        self.__cos = cos

    @property
    def Tan(self):
        return self.__tan
    @Tan.setter
    def Tan(self, tan):
        self.__tan = tan

    @property
    def Sinh(self):
        return self.__sinh
    @Sinh.setter
    def Sinh(self, sinh):
        self.__sinh = sinh

    @property
    def Cosh(self):
        return self.__cosh
    @Cosh.setter
    def Cosh(self, cosh):
        self.__cosh = cosh
    
    @property
    def Tanh(self):
        return self.__tanh
    @Tanh.setter
    def Tanh(self, tanh):
        self.__tanh = tanh
        
    def toString(self):
        return '\n'.join('Order = {0}'.format(self.Order),
                         'Radians = {0}'.format(self.Radians),
                         'Tau = {0}'.format(self.Tau),
                         'Sine = {0}'.format(self.Sin),
                         'Cosine = {0}'.format(self.Sin),
                         'Tangent = {0}'.format(self.Tan),
                         'Sinh = {0}'.format(self.Tan),
                         'Cosh = {0}'.format(self.Cosh),
                         'Tanh = {0}'.format(self.Tanh))
        
