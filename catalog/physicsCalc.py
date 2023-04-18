from decimal import Decimal

class photon():
    def __init__(self):
        self.planck = 6.626*(10**-34) # J*S
        self.lightSpeed = 299792458 # m/s
        self.conversions = {"meters":1, "millimeters":1000, "micrometers":1000000,
                            "nanometers":1*10**9, "angstroms":1*10**10}
        
    def exponentConversion(self,value):
        return 10*value
    
    def findExponentValue(self,toCheck):
        for i in range(len(toCheck)):
            if toCheck[i] == 'e':
                return (toCheck[:i],toCheck[i+1:]) # val 2 is exponent value
        return False
        

    def calculateEnergy(self, wavelength, unit):
        # wavelength is in meters
        # retuns energy in joules
        return Decimal((Decimal(self.planck * self.lightSpeed)/Decimal(wavelength)) * Decimal(self.conversions.get(unit)))
    
    def joulesToElectronVolts(self, num):
        return Decimal(Decimal(num)*Decimal(6.2442*(10**18)))
    
    def electronVoltsToJoules(self, num):
        return Decimal(Decimal(num)*Decimal(1.602*(10**-19)))
    
    def calculateWavelength(self,energy):
        value = self.findExponentValue(energy)
        if value == False:
            return ((self.planck*self.lightSpeed)/float(energy))
        exponentValue = self.exponentConversion(value[1])
        return (float(value[0]) * float(exponentValue))