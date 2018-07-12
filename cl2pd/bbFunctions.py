import numpy as np 
import dotdict
dotdict=dotdict.dotdict


def computeBBMatrix(numberOfLRToConsider):
        """
        It returns a beam-beam matrix, that is a representation of the beam-beam encounters scheduled for a filled machine (3564 bunches).
        To obtain the BB encounters scheduled of the bunch N of B1 (for the machine totally full) you have to consider the N-row (e.g., BBMatrix[N,:]).
        To obtain the BB encounters scheduled of the bunch N of B2 (for the machine totally full) you have to consider the N-column (e.g., BBMatrix[:,N]).
                
        The numberOfLRToConsider represents the long-range number at the right and left of each IR (the total number of LR per IR is therefore 2 x numberOfLRToConsider).
        numberOfLRToConsider can be a scalar of an array of 3 scalars (longer arrays will be truncated to the length of 3).
        In case numberOfLRToConsider is as array the first scalar represent the long-range number at the right and left of ATLAS/CMS. 
        The second and third element of the array will be the number of long range encounters (at the right and left) in IR2 and IR8, respectively.
        
        The matrix element has a value 1, 2, 5 and 8 when there is a HO  in IP1, 2, 5 and 8, respectively.
        The matrix element has a value 10, 20, 50 and  80 when there is a LR respectively in IR1, 2, 5 and 8, respectively.
        
        It assumes that the positions of the IPs and the convention of the B1/B2 bunch numbering are such that:
        
        1. B1 Bunch 0 meets B2 Bunch 0 in IP1 and 5.
        2. B1 Bunch 0 meets B2 Bunch 891 in IP2.
        3. B1 Bunch 0 meets B2 Bunch 2670 in IP8.
        4. B2 Bunch 0 meets B1 Bunch 0 in IP1 and 5.
        5. B2 Bunch 0 meets B1 Bunch 2673 in IP2.
        6. B2 Bunch 0 meets B1 Bunch 894 in IP8.

        === EXAMPLE 1 ===
        myMatrix=computeBBMatrix(numberOfLRToConsider=20)
        #in this case the total number of LR will be 160: 40 in IR1/5, 40 in IR2, and 40 in IR8.

        === EXAMPLE 2 ===
        myMatrix=computeBBMatrix(numberOfLRToConsider=[20,15,16])
        #in this case the total number of LR will be 142: 40 in IR1/5, 30 in IR2, and 32 in IR8.
        """ 
        availableBunchSlot=3564
        BBMatrixLHC =np.zeros([availableBunchSlot,availableBunchSlot]);

        if isinstance(numberOfLRToConsider,int):
            numberOfLRToConsiderATLASCMS=numberOfLRToConsider
            numberOfLRToConsiderALICE=numberOfLRToConsider
            numberOfLRToConsiderLHCB=numberOfLRToConsider
        else:
            numberOfLRToConsiderATLASCMS=numberOfLRToConsider[0]
            numberOfLRToConsiderALICE=numberOfLRToConsider[1]
            numberOfLRToConsiderLHCB=numberOfLRToConsider[2]

        # HO in IP1 and IP5
        index=np.arange(availableBunchSlot)
        BBMatrixLHC[index,index]=1

        # BBLR in IP1 and IP5
        for i in range(1,numberOfLRToConsiderATLASCMS+1):
            index=np.arange(availableBunchSlot-i)
            BBMatrixLHC[index,index+i]=10
            BBMatrixLHC[index,index-i]=10
            BBMatrixLHC[index+i,index]=10
            BBMatrixLHC[index-i,index]=10

        # HO in IP2
        IP2slot=availableBunchSlot/4
        index=np.arange(availableBunchSlot-IP2slot)
        BBMatrixLHC[index,index+IP2slot]=2
        index=np.arange(availableBunchSlot-IP2slot,availableBunchSlot)
        BBMatrixLHC[index,index-(availableBunchSlot-IP2slot)]=2

        # BBLR in IP2
        for i in range(1,numberOfLRToConsiderALICE+1):
            index=np.arange(availableBunchSlot-IP2slot-i)
            BBMatrixLHC[index,index+IP2slot+i]=20
            BBMatrixLHC[index+i,index+IP2slot]=20
            BBMatrixLHC[index,index+IP2slot-i]=20
            BBMatrixLHC[index-i,index+IP2slot]=20
            index=np.arange(availableBunchSlot-IP2slot,availableBunchSlot-i)
            BBMatrixLHC[index,index-(availableBunchSlot-IP2slot)+i]=20
            BBMatrixLHC[index+i,index-(availableBunchSlot-IP2slot)]=20
            BBMatrixLHC[index,index-(availableBunchSlot-IP2slot)-i]=20
            BBMatrixLHC[index-i,index-(availableBunchSlot-IP2slot)]=20

        # HO in IP8
        IP8slot=availableBunchSlot/4*3-3 
        index=np.arange(availableBunchSlot-IP8slot)
        BBMatrixLHC[index,index+IP8slot]=8
        index=np.arange(availableBunchSlot-IP8slot,availableBunchSlot)
        BBMatrixLHC[index,index-(availableBunchSlot-IP8slot)]=8

        # BBLR in IP8
        for i in range(1,numberOfLRToConsiderLHCB+1):
            index=np.arange(availableBunchSlot-IP8slot-i)
            BBMatrixLHC[index,index+IP8slot+i]=80
            BBMatrixLHC[index+i,index+IP8slot]=80
            BBMatrixLHC[index,index+IP8slot-i]=80
            BBMatrixLHC[index-i,index+IP8slot]=80
            index=np.arange(availableBunchSlot-IP8slot,availableBunchSlot-i)
            BBMatrixLHC[index,index-(availableBunchSlot-IP8slot)+i]=80
            BBMatrixLHC[index+i,index-(availableBunchSlot-IP8slot)]=80
            BBMatrixLHC[index,index-(availableBunchSlot-IP8slot)-i]=80
            BBMatrixLHC[index-i,index-(availableBunchSlot-IP8slot)]=80

        return BBMatrixLHC;

def _bunch_BB_pattern(Bunch,BBMatrixLHC):
    '''
    It returns the beam-beam pattern of a bunch of B1 and B2 [adimensional array of integer] in ALICE, ATLAS, CMS, LHCB.
    
    - Bunch [adimensional integer]: the bunch number in B1 and B2 to consider.
    - BBMatrixLHC [adimensional integer matrix]: the beam-beam matrix to consider (see bbFunctions.computeBBMatrix?).
    The returned array is ordered with respect to the positive direction of B1 (clockwise in LHC). 
    WARNING: the bunch number is defined wrt the negative direction of each beam.
    
    Conventions :
    
    ...=>B1 bunch 1 => B1 bunch 0 => |[IP]| <= B2 bunch 0 <= B2 bunch 1 <=...
    
    This means that B1 bunch 0 will meet B2 bunch 1 on the positive side of the IP and B2 bunch 0 will meet B1 bunch 0 on the negative side of IP1 (positive/negative wrt the B1).
    
    '''
    
    #### BEAM 1 ####
    BBVector=BBMatrixLHC[Bunch,:]
    
    numberOfLRToConsider=len(np.where(BBMatrixLHC[Bunch,:]==10)[0])/2
    HO_in_IP=BBVector==1
    LR_in_IP=BBVector==10
    aux=np.where((LR_in_IP) | (HO_in_IP))[0]
    np.where(aux==Bunch)[0]
    B1=np.roll(aux,  numberOfLRToConsider-np.where(aux==np.where(HO_in_IP)[0][0])[0])
    resultsB1=dotdict({'atATLAS':B1,
         'atCMS':B1})
    
    HO_in_IP=BBVector==2
    LR_in_IP=BBVector==20
    numberOfLRToConsider=len(np.where(BBMatrixLHC[Bunch,:]==20)[0])/2
    aux=np.where((LR_in_IP) | (HO_in_IP))[0]
    np.where(aux==Bunch)[0]
    B1=np.roll(aux, numberOfLRToConsider-np.where(aux==np.where(HO_in_IP)[0][0])[0])
    resultsB1.update({'atALICE':B1})
    
    HO_in_IP=BBVector==8
    LR_in_IP=BBVector==80
    numberOfLRToConsider=len(np.where(BBMatrixLHC[Bunch,:]==80)[0])/2
    aux=np.where((LR_in_IP) | (HO_in_IP))[0]
    np.where(aux==Bunch)[0]
    B1=np.roll(aux, numberOfLRToConsider-np.where(aux==np.where(HO_in_IP)[0][0])[0])
    resultsB1.update({'atLHCB':B1})
    
    #### BEAM 2 ####
    BBVector=BBMatrixLHC[:,Bunch]
    numberOfLRToConsider=len(np.where(BBMatrixLHC[Bunch,:]==10)[0])/2
    HO_in_IP=BBVector==1
    LR_in_IP=BBVector==10
    aux=np.where((LR_in_IP) | (HO_in_IP))[0]
    np.where(aux==Bunch)[0]
    B2=np.roll(aux,  numberOfLRToConsider-np.where(aux==np.where(HO_in_IP)[0][0])[0])
    resultsB2=dotdict({'atATLAS':B2[::-1], 
         'atCMS':B2[::-1]}) # To note the inverstion of the direction
   
    HO_in_IP=BBVector==2
    LR_in_IP=BBVector==20
    numberOfLRToConsider=len(np.where(BBMatrixLHC[Bunch,:]==20)[0])/2
    aux=np.where((LR_in_IP) | (HO_in_IP))[0]
    np.where(aux==Bunch)[0]
    B2=np.roll(aux, numberOfLRToConsider-np.where(aux==np.where(HO_in_IP)[0][0])[0])
    resultsB2.update({'atALICE':B2[::-1]})
    
    HO_in_IP=BBVector==8
    LR_in_IP=BBVector==80
    numberOfLRToConsider=len(np.where(BBMatrixLHC[Bunch,:]==80)[0])/2
    aux=np.where((LR_in_IP) | (HO_in_IP))[0]
    np.where(aux==Bunch)[0]
    B2=np.roll(aux, numberOfLRToConsider-np.where(aux==np.where(HO_in_IP)[0][0])[0])
    resultsB2.update({'atLHCB':B2[::-1]})
    # The encounters seen by  B1/2 are in increasing/decreasing order
    return dotdict({'atB1':resultsB1, 'atB2':resultsB2})

def BBEncounterSchedule(B1_fillingScheme,B2_fillingScheme,BBMatrixLHC):
    """
    It returns a dictionary structure with the BB encounters of B1 and B2 taking into account the filling schemes.
    - B1_fillingScheme [adimensional integer array]: the B1 filling scheme.
    - B2_fillingScheme [adimensional integer array]: the B2 filling scheme.
    The dictionary structure has the following hierarchy:
    - BEAM >> BUNCH >> EXPERIMENT >> ENCOUNTERS
    - BEAM >> BUNCH >> EXPERIMENT >> POSITIONS
    All the positions are referred to the positive direction of B1 (clockwise in LHC).
    WARNING: the bunch number is defined wrt the negative direction of each beam.
    
    === EXAMPLE 1 ===
    from cl2pd import bbFunctions
    from cl2pd import importData
   
    np=importData.np  
    BBMatrixLHC=bbFunctions.computeBBMatrix(numberOfLRToConsider=25)
    B1_bunches=np.array([0,1,2])
    B2_bunches=np.array([0,1,2])
    results=beam_BB_pattern(B1_bunches, B2_bunches, BBMatrixLHC)
    """
    experiments=['atALICE','atATLAS','atCMS','atLHCB']

    #B1
    B1_BB_pattern=dotdict()
    for i in B1_fillingScheme:
        bunch_aux=dotdict()
        for j in experiments:
            results=_bunch_BB_pattern(i,BBMatrixLHC)
            B2=results['atB1'][j]
            aux=B2[np.in1d(B2,B2_fillingScheme)]
            myPosition=np.arange(-(len(B2)-1)/2,(len(B2)-1)/2+1)
            bunch_aux.update({j: {'atEncounters' : aux,'atPositions':myPosition[np.in1d(B2,B2_fillingScheme)]}})
            B1_BB_pattern.update({'at'+format(i,'04d'):bunch_aux})

    #B2
    B2_BB_pattern=dotdict()
    for i in B2_fillingScheme:
        bunch_aux=dotdict()
        for j in experiments:
            results=_bunch_BB_pattern(i,BBMatrixLHC)
            B1=results['atB2'][j]
            aux=B1[np.in1d(B1,B1_fillingScheme)]
            myPosition=np.arange(-(len(B1)-1)/2,(len(B1)-1)/2+1)
            bunch_aux.update({j: {'atEncounters' : aux,'atPositions':myPosition[np.in1d(B1,B1_fillingScheme)]}})
            B2_BB_pattern.update({'at'+format(i,'04d'):bunch_aux})

    beam_BB_pattern=dotdict({'atB1':B1_BB_pattern,'atB2':B2_BB_pattern})
    return beam_BB_pattern
