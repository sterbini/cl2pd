'''This module gives a set of static method to compute the kinematic quantities of a particle. 
All the methods are static and have as predefined restEnergy_GeV and elementaryCharge argument the proton's ones.
'''
import numpy as np
restEnergyProton_GeV=0.93827231
elementaryChargeProton=1.
speedOfLight_m_s=299792458. 
mu0_H_m=4.*np.pi*1e-7
epsilon0_F_m= 8.854187817e-12
elementaryChargeProton_C=1.6021766209e-19

def setRelativisticGamma(relativisticGamma, restEnergy_GeV=restEnergyProton_GeV, elementaryCharge=elementaryChargeProton):
    """See signature."""
    if restEnergy_GeV<=0:
        print('Error: restEnergy_GeV should be greater than 0.')
        return;
    if elementaryCharge==0:
        print('Warning: elementaryCharge is set to zero, magneticRigidity_Tm is not undetermined.')  
    if elementaryCharge<0:
        print('Warning: elementaryCharge will be considered positive.')
        elementaryCharge=-elementaryCharge
    if relativisticGamma>=1:
        totalEnergy_GeV=restEnergy_GeV*relativisticGamma
        relativisticBeta=np.sqrt(1.-relativisticGamma**-2)
        relativisticBetaGamma=relativisticGamma*relativisticBeta
        pc_GeV=restEnergy_GeV*np.sqrt(relativisticGamma**2-1)
        kinetikEnergy_GeV=totalEnergy_GeV-restEnergy_GeV
        if elementaryCharge==0:
            magneticRigidity_Tm=np.nan
        else:
            magneticRigidity_Tm=1.E9/speedOfLight_m_s*pc_GeV/elementaryCharge
        return {'totalEnergy_GeV': totalEnergy_GeV,
                'kinetikEnergy_GeV':kinetikEnergy_GeV,
                'pc_GeV':pc_GeV,
                'restEnergy_GeV':restEnergy_GeV,
                'relativisticBeta': relativisticBeta,
                'relativisticBetaGamma': relativisticBetaGamma, 
                'relativisticGamma': relativisticGamma,
                'elementaryCharge':elementaryCharge,
                'magneticRigidity_Tm':magneticRigidity_Tm}
    else:
        print('Error: RelativisticGamma has to be equal or larger than 1.')

def setRelativisticBeta(relativisticBeta, restEnergy_GeV=restEnergyProton_GeV, elementaryCharge=elementaryChargeProton):
    """See signature."""
    if restEnergy_GeV<=0:
        print('Error: restEnergy_GeV should be greater than 0.')
        return;
    if elementaryCharge==0:
        print('Warning: elementaryCharge is set to zero, magneticRigidity_Tm is not undetermined.')  
    if elementaryCharge<0:
        print('Warning: elementaryCharge will be considered positive.')
        elementaryCharge=-elementaryCharge
    if (relativisticBeta>0) & (relativisticBeta<1):
        relativisticGamma=(1.-relativisticBeta**2)**(-.5)
        totalEnergy_GeV=restEnergy_GeV*relativisticGamma
        relativisticBeta=relativisticBeta
        relativisticBetaGamma=relativisticGamma*relativisticBeta
        pc_GeV=restEnergy_GeV*np.sqrt(relativisticGamma**2-1)
        kinetikEnergy_GeV=totalEnergy_GeV-restEnergy_GeV
        if elementaryCharge==0:
            magneticRigidity_Tm=np.nan
        else:
            magneticRigidity_Tm=1.E9/speedOfLight_m_s*pc_GeV/elementaryCharge
        return {'totalEnergy_GeV': totalEnergy_GeV,
                'kinetikEnergy_GeV':kinetikEnergy_GeV,
                'pc_GeV':pc_GeV,
                'restEnergy_GeV':restEnergy_GeV,
                'relativisticBeta': relativisticBeta,
                'relativisticBetaGamma': relativisticBetaGamma, 
                'relativisticGamma': relativisticGamma,
                'elementaryCharge':elementaryCharge,
                'magneticRigidity_Tm':magneticRigidity_Tm}
    else:
        print('Error: relativisticBeta has to be larger than 0 and smaller that 1.')


def setTotalEnergy_GeV(totalEnergy_GeV, restEnergy_GeV=restEnergyProton_GeV, elementaryCharge=elementaryChargeProton):
    """See signature."""
    if restEnergy_GeV<=0:
        print('Error: restEnergy_GeV should be greater than 0.')
        return;
    if elementaryCharge==0:
        print('Warning: elementaryCharge is set to zero, magneticRigidity_Tm is not undetermined.')  
    if elementaryCharge<0:
        print('Warning: elementaryCharge will be considered positive.')
        elementaryCharge=-elementaryCharge
    if (totalEnergy_GeV>=restEnergy_GeV):
        relativisticGamma=totalEnergy_GeV/restEnergy_GeV
        totalEnergy_GeV=totalEnergy_GeV
        relativisticBeta=np.sqrt(1.-relativisticGamma**-2)
        relativisticBetaGamma=relativisticGamma*relativisticBeta
        pc_GeV=restEnergy_GeV*np.sqrt(relativisticGamma**2-1)
        kinetikEnergy_GeV=totalEnergy_GeV-restEnergy_GeV
        if elementaryCharge==0:
            magneticRigidity_Tm=np.nan
        else:
            magneticRigidity_Tm=1.E9/speedOfLight_m_s*pc_GeV/elementaryCharge
        return {'totalEnergy_GeV': totalEnergy_GeV,
                'kinetikEnergy_GeV':kinetikEnergy_GeV,
                'pc_GeV':pc_GeV,
                'restEnergy_GeV':restEnergy_GeV,
                'relativisticBeta': relativisticBeta,
                'relativisticBetaGamma': relativisticBetaGamma, 
                'relativisticGamma': relativisticGamma,
                'elementaryCharge':elementaryCharge,
                'magneticRigidity_Tm':magneticRigidity_Tm}
    else:
        print('Error: totalEnergy should be equal or larger than restEnergy_GeV.')

def setPc_GeV(pc_GeV, restEnergy_GeV=restEnergyProton_GeV, elementaryCharge=elementaryChargeProton):
    """See signature."""
    if restEnergy_GeV<=0:
        print('Error: restEnergy_GeV should be greater than 0.')
        return;
    if elementaryCharge==0:
        print('Warning: elementaryCharge is set to zero, magneticRigidity_Tm is not undetermined.')  
    if elementaryCharge<0:
        print('Warning: elementaryCharge will be considered positive.')
        elementaryCharge=-elementaryCharge
    if (pc_GeV>=0):
        relativisticGamma=(1+(pc_GeV/restEnergy_GeV)**2)**.5
        totalEnergy_GeV=restEnergy_GeV*relativisticGamma
        relativisticBeta=np.sqrt(1.-relativisticGamma**-2)
        relativisticBetaGamma=relativisticGamma*relativisticBeta
        pc_GeV=pc_GeV
        kinetikEnergy_GeV=totalEnergy_GeV-restEnergy_GeV
        if elementaryCharge==0:
            magneticRigidity_Tm=np.nan
        else:
            magneticRigidity_Tm=1.E9/speedOfLight_m_s*pc_GeV/elementaryCharge
        return {'totalEnergy_GeV': totalEnergy_GeV,
                'kinetikEnergy_GeV':kinetikEnergy_GeV,
                'pc_GeV':pc_GeV,
                'restEnergy_GeV':restEnergy_GeV,
                'relativisticBeta': relativisticBeta,
                'relativisticBetaGamma': relativisticBetaGamma, 
                'relativisticGamma': relativisticGamma,
                'elementaryCharge':elementaryCharge,
                'magneticRigidity_Tm':magneticRigidity_Tm}
    else:
        print('Error: pc_GeV should be equal or larger than 0.')

def setMagneticRigidity_Tm(magneticRigidity_Tm, restEnergy_GeV=restEnergyProton_GeV, elementaryCharge=elementaryChargeProton):
    """See signature."""
    if restEnergy_GeV<=0:
        print('Error: restEnergy_GeV should be greater than 0.')
        return;
    if magneticRigidity_Tm<0:
        print('Warning: magneticRigidity_Tm will be considered positive.')
        magneticRigidity_Tm=-magneticRigidity_Tm      
    if elementaryCharge<0:
        print('Warning: elementaryCharge will be considered positive.')
        elementaryCharge=-elementaryCharge

    if (magneticRigidity_Tm!=0) or ( elementaryCharge!=0):
        pc_GeV=magneticRigidity_Tm/1.E9*elementaryCharge*speedOfLight_m_s
        relativisticGamma=(1+(pc_GeV/restEnergy_GeV)**2)**.5
        totalEnergy_GeV=restEnergy_GeV*relativisticGamma
        relativisticBeta=np.sqrt(1.-relativisticGamma**-2)
        relativisticBetaGamma=relativisticGamma*relativisticBeta
        kinetikEnergy_GeV=totalEnergy_GeV-restEnergy_GeV
        return {'totalEnergy_GeV': totalEnergy_GeV,
                'kinetikEnergy_GeV':kinetikEnergy_GeV,
                'pc_GeV':pc_GeV,
                'restEnergy_GeV':restEnergy_GeV,
                'relativisticBeta': relativisticBeta,
                'relativisticBetaGamma': relativisticBetaGamma, 
                'relativisticGamma': relativisticGamma,
                'elementaryCharge':elementaryCharge,
                'magneticRigidity_Tm':magneticRigidity_Tm}
    else:
         print('Error: elementaryCharge and magneticRigidity_Tm are equal to 0, so the problem cannot be inverted.')  
