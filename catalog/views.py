from django.shortcuts import render
from .models import Element
from .molcal import moleCounter, electronegativity, cellParameter, photons
from .physicsCalc import photon
from django.shortcuts import HttpResponse
import os


def index(request):
    """View function for home page of site."""
    """""
    """
    return render(request,'home.html')

def physicsCalculator(request):
    return render(request,"physicsCalculator.html")

def photonEnergy(request):
    if request.method == 'POST':
        wavelength = request.POST.get('textfield', None)
        unit = request.POST.get('length')
        try:
            photonEnergy = photon()
            energyJoules = photonEnergy.calculateEnergy(wavelength, unit)
            energyElectronVolts = photonEnergy.joulesToElectronVolts(energyJoules)
            return HttpResponse(str(energyJoules) + " Joules <br>" + (str(energyElectronVolts) + " ElectronVolts"))
        except Exception as e:
            print(e, "ERROR HERE")
            return HttpResponse("Error")

def photonWavelength(request):
    if request.method == 'POST':
        energy = request.POST.get('textfield', None)
        try:
            photonEnergy = photon()
            wavelength = photonEnergy.calculateWavelength(energy)
            return HttpResponse(str(wavelength) + " nanometers")
        except Exception as e:
            print(e, "ERROR HERE")
            return HttpResponse("Error")
        
def xrdCalc(request):
    """
    calculates wavelength when given d-spacing and theta
    """
    if request.method == 'POST':
        d = request.POST.get('d_spacing', None)
        theta = request.POST.get('theta', None)
        try:
            photonEnergy = photons()
            wavelength = photonEnergy.calcWavelength(d,theta)
            return HttpResponse(str(wavelength) + " picometers")
        except Exception as e:
            print(e, "ERROR HERE")
            return HttpResponse("Error")


def chemistryCalculator(request):
    """
    transfers screen to Calculator screen
    """
    print("calcScreen 1")

    if request.method == 'POST':
        print("Calculator screen 2")
        return render(request, "molcalculation.html")
    return render(request, "molcalculation.html")

def personalPage(request):
    print("Personal Page 1")
    print(os.listdir('catalog/templates/images'))
    return render(request, "personalpage.html")

def displayPicture():
    pass

def molarmass(request):
    """""
    returns the mols of a given compound
    """""

    if request.method == 'POST':
        compound = request.POST.get('textfield',None)
        try:
            molcount = moleCounter(compound)
            moleCounter.parseCompound(molcount)
            mol = moleCounter.calcMolJ(molcount)
            html = ("<H1>Molar Mass</H1>", str(mol) + " g/mol")
            return HttpResponse(html)
        except Exception as e:
            print (e)
            return HttpResponse("Error" + e)
    
    return render(render,'molcalculation.html')

def electronegativitycalc(request):
    """
    returns the electronegativity of a compound
    """
    print("electronegativity")
    if request.method == 'POST':
        compound = request.POST.get('textfield',None)
        try:
            electro = electronegativity(compound)
            elements = electro.parseCompound()
            print(elements)
            if len(elements) > 2:
                negativity = electro.calcElectronegavity(elements[1],elements[2])
            else:
                negativity = electro.calcElectronegavity(elements[1], "He")
            html = ("<H1>ElectroNegativity</H1>", negativity)
            return HttpResponse(html)
        except Exception as e:
            print(e)
            return HttpResponse("Error")

def ionicCharacter(request):
    print("IONIC")
    if request.method == 'POST':
        compound = request.POST.get('textfield',None)

        ionic = electronegativity(compound)
        elements = ionic.parseCompound()
        negativity = ionic.calcElectronegavity(elements[0],elements[1])
        ionicChar = ionic.calcIonicCharacter(negativity)
        html = str(ionicChar) + "%"
        return HttpResponse(html)
    
def millerIndices(request):
    print("MILLER")
    if request.method == 'POST':
        cell_parameter = request.POST.get('cell_parameter')
        d_spacing = request.POST.get('d-spacing')

        print(cell_parameter)
        print(d_spacing)

        miller = cellParameter()
        indices = miller.calcMiller(float(cell_parameter),float(d_spacing))
        html = indices
        return HttpResponse(html)
    
def d_spacingcalc(request):
    print("D_SPACING")
    if request.method == 'POST':
        unit_cell = request.POST.get('unit_cell')
        miller = request.POST.get('miller')
        miller = miller.split(',')

        CeP = cellParameter()
        glasses = CeP.calcD_spacing(unit_cell,miller)
        html = glasses
        return HttpResponse(html)
    
def unit_cell(request):
    print("UNITCELL")
    if request.method == 'POST':
        d_spacing = request.POST.get('d_spacing')
        miller = request.POST.get('miller')
        miller = miller.split(',')

        CeP = cellParameter()
        glasses = CeP.calcUnitCellParameter(d_spacing,miller)
        html = glasses
        return HttpResponse(html)
    else:
        return HttpResponse("ERROR")

