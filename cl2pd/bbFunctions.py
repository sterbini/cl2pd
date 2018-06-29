import numpy as np 

def computeBBMatrix(numberOfLRToConsider=20):
        """
        It returns a beam-beam matrix. 
        To obtain the BB pattern of the bunch N of B1 you have to consider the N-row (e.g., BBMatrix[N,:]).
        
        The matrix will have a value 1,2,5,8 when there is a HO respectively in IP1,2,5,8.
        The matrix will have a value 10,20,50,80 when there is a LR respectively in IP1,2,5,8.
        
        It assumes that the positions of the IPs and the convention of the B1/B2 bunch numbering is such that.
        1. B1 Bunch 0 meets B2 Bunch 0 in IP1 and 5.
        2. B1 Bunch 0 meets B2 Bunch 891 in IP2.
        2. B1 Bunch 0 meets B2 Bunch 2670 in IP8.

        Example:
        myMatrix=computeBBMatrix(numberOfLRToConsider=20)
        """ 
        availableBunchSlot=3564
        BBMatrixLHC =np.zeros([availableBunchSlot,availableBunchSlot]);

        #numberOfLRToConsider=20;

        # HO in IP1 and IP5
        index=np.arange(availableBunchSlot)
        BBMatrixLHC[index,index]=1

        # BBLR in IP1 and IP5
        for i in range(1,numberOfLRToConsider+1):
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
        for i in range(1,numberOfLRToConsider+1):
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
        for i in range(1,numberOfLRToConsider+1):
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
