import numpy as np 

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
        
        It assumes that the positions of the IPs and the convention of the B1/B2 bunch numbering is such that.
        1. B1 Bunch 0 meets B2 Bunch 0 in IP1 and 5.
        2. B1 Bunch 0 meets B2 Bunch 891 in IP2.
        2. B1 Bunch 0 meets B2 Bunch 2670 in IP8.

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
