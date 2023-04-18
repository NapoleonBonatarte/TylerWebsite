
import json
import math

class moleCounter():
    def __init__(self,compound):
        f = open("chem\catalog\elements.json")
 
        self.elementList = json.load(f)

        self.compound = compound
        self.elements = []

    def parseCompound(self):
        previous = 0
        compnum = ""
        for i in range(len(self.compound)):
            if self.compound[i].isupper():
                self.elements.append(self.compound[previous:i])
                previous = i
            if self.compound[i].isnumeric():
                n = 0
                while (i+n) < len(self.compound) and self.compound[i + n].isnumeric():
                    n+=1
                compnum = int(self.compound[i:i+n])
                for j in range(int(compnum)):
                    self.elements.append(self.compound[previous:i])
        self.elements.append(self.compound[previous:])
        self.elements = self.elements[1:]
        #print(self.elements)

    def calcMolJ(self):
        print("MOLCOUNT")
        molcount = 0

        # change this to a set at some point, it is very slow (O(n^2))

        # iterate thru given compound
        for i in self.elements:
            # iterate thru all elements of periodic table
            for j in self.elementList:
                if i == j["symbol"]:
                    molcount += j["atomic weight"]
        return molcount
        

    def checkIfElement(self, checkelement):
        for i in self.elementList:
            if checkelement == i["symbol"]:
                return True
        return False




class electronegativity():
    def __init__(self,compound):
        f = open("chem\catalog\elements.json")
 
        self.elementList = json.load(f)
        self.compound = compound
        self.elements = []

    def parseCompound(self):
        upperlist = []
        finalcompound = ''
        for i in self.compound:
            if i.isupper():
                finalcompound += "#" + i
            finalcompound += i

        print(self.compound)
        print(upperlist)
        self.elements = self.compound.split("#",1)
        print(finalcompound)
        return finalcompound

    
    def calcElectronegavity(self,comp1,comp2):
        electro1 = 0
        electro2 = 0
        electronegativity = 0
        for i in self.elementList:
            if comp1 == i["symbol"]:
                electro1 = i["electronegativity"]
                #print(electro1)
            if comp2 == i["symbol"]:
                electro2 = i["electronegativity"]
                #print(electro2)

        electronegativity = round(abs(electro1 - electro2),5)
        return electronegativity

    def calcIonicCharacter(self,electronegativity):
        ionicChar = {
            0.1:0.5,0.2:1,0.3:2,0.4:4,0.5:6,0.6:9,0.7:12,0.8:15
            ,0.9:19,1:22,1.1:26,1.2:30,1.3:34,1.4:39,1.5:43,1.6:47,1.7:51,1.8:55,1.9:59,2:63,2.1:67,
            2.2:70,2.3:74,2.4:76,2.5:79,2.6:82,2.7:84,2.8:86,2.9:88,3:89,3.1:91,3.2:92
        }
        #print(electronegativity, "VALUE")
        try:
            return ionicChar[round(electronegativity,1)]
        except:
            if electronegativity > 3.2:
                return 95
            if electronegativity < .1:
                return 0
    
class cellParameter():
    def __init__(self):
        self.d_spacing = 0
        self.unit_cell_parameter = 0
        self.miller = (0,0,0)

    
    def calcUnitCellParameter(self,d_spacing,miller):
        print("DOING CALCULATIONS")
        return float(d_spacing) * math.sqrt(int(miller[0])^2 + int(miller[1])^2 + int(miller[2])^2)
    
    def calcD_spacing(self,unitCell,miller):
        print(miller)
        return (float(unitCell)/math.sqrt(int(miller[0])^2 + int(miller[1])^2 + int(miller[2])^2))
    
    def calcMiller(self,unitCell,d_spacing):
        # this needs brute forcing as far as I know, so python
        # is not a very good language for this, as such there
        # is a limiter, rewrite in Java or C++ later

        tempval = 0
        hkl = 0
        possibleMillerValues = []
        print(unitCell)
        print(d_spacing)
        # finds total hkl value
        for i in range(100):
            tempval = unitCell/math.sqrt(i+1)
            print(tempval)
            if (abs(tempval - d_spacing) < 0.1):
                hkl = i+1
                break
        

        h = 0
        k = 0
        l = 0
        # O(n^3) implementation, change this later
        for h in range(50):
            for k in range(50):
                for l in range(50):
                    if ((h^2) + (k^2) + (l^2)) == hkl:
                        # I don't know why but not putting the squares in this somehow multiplies
                        # all values by 3, and since I have no idea why that is I am just doing this
                        # it is very computationally intensive so change later
                        possibleMillerValues.append(((h^2),(k^2),(l^2)))
        
        return possibleMillerValues
    
class photons():
    def __init__(self):
        self.speedLight = 299792458
        self.planck = 6.6260715 * 10^-34

    def calcEnergy(self,wavelength):
        # wavelength in meters
        num = self.speedLight * self.planck
        energy = num/wavelength
        return energy
    




        
        


#c = cellParameter()
#print(c.calcUnitCellParameter(2.89,(0,1,1)))
#print(c.calcD_spacing(4.087,(0,1,1)))
#print(c.calcMiller(4.860,2.806))



#a = moleCounter("C2H2Cl2O2")
#b = electronegativity()


#a.parseCompound()
#print(a.calcMolJ())
#print(b.calcElectronegavity("Na","Cl"))
#print(b.calcIonicCharacter(b.calcElectronegavity("Na","Cl")))

