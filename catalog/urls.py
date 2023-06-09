from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'), 
    path('GPTDemo/', views.GPTDemo, name="GPTDemoScreen"),
    path('GPTDemo/runGPTParse/', views.GPTSearch, name="GPTDemoScreenParse"),
    path('GPTDemo/runGPTParse/GPTChatScreen/', views.GPTChatScreen, name="GPTChatScreen"),
    path('chemistryCalculator/', views.chemistryCalculator, name = 'calculatorScreen'),
    path('chemistryCalculator/molarmass/', views.molarmass, name = 'molarmass'),
    path('chemistryCalculator/electronegativitycalc/', views.electronegativitycalc, name = 'electronegativitycalc'),
    path('chemistryCalculator/ionicChar/', views.ionicCharacter, name = 'ionicChar'),
    path('chemistryCalculator/millerIndices/', views.millerIndices, name = 'millerIndices'),
    path('chemistryCalculator/d_spacingcalc/', views.d_spacingcalc, name = 'd_spacingcalc'),
    path('chemistryCalculator/unit_cell/', views.unit_cell, name = 'unit_cell'),
    path('chemistryCalculator/xrdCalc/', views.xrdCalc, name = 'xrdCalc'),
    path('chemistryCalculator/deltaH/', views.deltaHCalculator, name = 'xrdCalc'),
    path('chemistryCalculator/ECellCalculatorPage/', views.ECellCalculatorPage, name = 'ECellCalculatorPage'),
    path('chemistryCalculator/ECellCalculatorPage/calculateECell/', views.calculateECell, name = 'calculateECell'),
    path('physicsCalculator/', views.physicsCalculator, name = "physicsCalculator"),
    path('physicsCalculator/photonEnergy/', views.photonEnergy, name = 'photonEnergy'),
    path('physicsCalculator/photonWavelength/', views.photonWavelength, name = 'photonWaveLength'),
    path('personalPage/', views.personalPage, name='personalPage'),
    
]