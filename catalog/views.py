from django.shortcuts import render
from .models import Element
from .molcal import moleCounter, electronegativity, cellParameter, photons, calculator
from .physicsCalc import photon
from django.shortcuts import HttpResponse
from .reductionPotential import ReductionPotential, ReductionPotentialSolution
import os
import openai
from django.template.response import TemplateResponse
from .gptModels import parseUserInfo, parseAdditionalContent
from .gptInterface.gptBuildOutput import buildOutput


#### NOTE: I made a mistake in designing this and as such it is only able to take
# 1 user in the chatbot at a time, this will require fixing later


# this determines if the chatbot is searching for a location or not.
searchForLocation = True

# this allows for continual question to gpt without using too many tokens
result = ""


def index(request):
    """View function for home page of site."""
    """""
    """
    return render(request,'home.html')

def GPTSearch(request):
    global searchForLocation
    global result

    print("SEARCH FOR LOCATION", searchForLocation)
    print("RESULT", result)

    print(request)
    if request.method == "POST":
        patientRequest = request.POST.get("userInput")
        print(result, "THIS IS THE RESULT")
        if searchForLocation:
            result, searchForLocation = parseUserInfo(patientRequest)
            to_return = buildOutput(result)
        else:
            # limited to 4 data entries right now for token count, figure
            # out a better way to do this later
            result=to_return, searchForLocation = parseAdditionalContent(patientRequest,result[:4])
        #print(result, "THIS IS THE RESULT 1")
        return TemplateResponse(request,"GPTHome.html",{"result":to_return})
        #return render(request, "GPTHome.html", result)

    result = request.args.get("result")
    return render(request, "GPTHome.html",result=result)

def GPTDemo(request):
    global searchForLocation
    global result

    searchForLocation = True
    result = ""

    print("DEMO")
    return render(request, "GPTHome.html")
    

def ECellCalculatorPage(request):
    return render(request, "ECellCalculatorPage.html")

def calculateECell(request):
    if request.method == 'POST':
        left = request.POST.get('left',None)
        right = request.POST.get('right',None)

        compound = left + "→" + right
        compound = str(compound).replace(" ", "")
        print(compound, "COMPOUND")
        for i in range(len(ReductionPotentialSolution)):
            print(ReductionPotentialSolution[i])
            if ReductionPotentialSolution[i] == compound:
                return HttpResponse(ReductionPotential[i])
            
        return HttpResponse("No Compound found!")

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
        
def deltaHCalculator(request):
    if request.method == 'POST':
        mass = request.POST.get('mass',None)
        specificHeat = request.POST.get('heat',None)
        deltaT = request.POST.get('deltaT',None)
        try:
            calc = calculator()
            deltaH = calc.deltaHCalculator(mass,specificHeat,deltaT)
            html = ("<H1>DeltaH</H1>" + str(deltaH) + " Joules")
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

