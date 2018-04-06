import pandas as pd

LHC=pd.DataFrame([['LHC.BOFSU:OFC_ENERGY','Energy','NUMERIC',True],
              ['LHC.BCTFR.A6R4.B1:BEAM_INTENSITY','Intensity','NUMERIC',False],
              ['LHC.BCTFR.A6R4.B2:BEAM_INTENSITY','Intensity','NUMERIC',False],
              ['LHC.RUNCONFIG:IP1-XING-V-MURAD','Crossing angle','NUMERIC',True],
              ['LHC.RUNCONFIG:IP2-XING-V-MURAD','Crossing angle','NUMERIC',True],
              ['LHC.RUNCONFIG:IP5-XING-H-MURAD','Crossing angle','NUMERIC',True],
              ['LHC.RUNCONFIG:IP8-XING-H-MURAD','Crossing angle','NUMERIC',True],
              ['LHC.BQM.B1:BUNCH_LENGTH_MEAN','Bunch length','NUMERIC',False],
              ['LHC.BQM.B2:BUNCH_LENGTH_MEAN','Bunch length','NUMERIC',False,'To be done'],\
              ['LHC.BQBBQ.CONTINUOUS.B1:TUNE_V', 'Tune','NUMERIC' , False],
              ['LHC.BQBBQ.CONTINUOUS.B2:TUNE_V', 'Tune','NUMERIC', False],
              ['LHC.BQBBQ.CONTINUOUS_HS.B1:TUNE_V', 'Tune','NUMERIC' , False],
              ['LHC.BQBBQ.CONTINUOUS_HS.B2:TUNE_V', 'Tune','NUMERIC', False],
              ['LHC.BQBBQ.CONTINUOUS.B1:TUNE_H', 'Tune','NUMERIC' , False],
              ['LHC.BQBBQ.CONTINUOUS.B2:TUNE_H', 'Tune','NUMERIC', False],
              ['LHC.BQBBQ.CONTINUOUS_HS.B1:TUNE_H', 'Tune','NUMERIC' , False],
              ['LHC.BQBBQ.CONTINUOUS_HS.B2:TUNE_H', 'Tune','NUMERIC', False],      
                ],           
            columns=['Variable name','TAG','Type','On change', 'Description'])
