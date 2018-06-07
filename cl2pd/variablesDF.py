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
              ['LHC.BQBBQ.CONTINUOUS_HS.B1:TUNE_V', 'Tune','NUMERIC' , False,'Most sensitive tune'],
              ['LHC.BQBBQ.CONTINUOUS_HS.B2:TUNE_V', 'Tune','NUMERIC', False,'Most sensitive tune'],
              ['LHC.BQBBQ.CONTINUOUS.B1:TUNE_H', 'Tune','NUMERIC' , False],
              ['LHC.BQBBQ.CONTINUOUS.B2:TUNE_H', 'Tune','NUMERIC', False],
              ['LHC.BQBBQ.CONTINUOUS_HS.B1:TUNE_H', 'Tune','NUMERIC' , False,'Most sensitive tune'],
              ['LHC.BQBBQ.CONTINUOUS_HS.B2:TUNE_H', 'Tune','NUMERIC', False,'Most sensitive tune'],
                    
              ['RPMC.UL14.RBBCW.L1B2:I_MEAS','Wire L1 B2','NUMERIC', True,'Wire current'],
              ['RPMC.UL16.RBBCW.R1B2:I_MEAS','Wire R1 B2','NUMERIC', True,'Wire current'],
              ['RPMC.USC55.RBBCW.L5B2:I_MEAS','Wire L5 B2','NUMERIC', True,'Wire current'],
              ['RPMC.UL557.RBBCW.R5B2:I_MEAS','Wire R5 B2','NUMERIC', True,'Wire current'],
                    
              ['TCTPV_4R1_B2_TTLU.POSST','Wire R1 B2','NUMERIC', True,'Wire-collimator temperature'],
              ['TCTPV_4R1_B2_TTLD.POSST','Wire R1 B2','NUMERIC', True,'Wire-collimator temperature'],
              ['TCTPV_4R1_B2_TTRU.POSST','Wire R1 B2','NUMERIC', True,'Wire-collimator temperature'],
              ['TCTPV_4R1_B2_TTRD.POSST','Wire R1 B2','NUMERIC', True,'Wire-collimator temperature'],
                    
              ['TCLVW_A5L1_B2_TTLU.POSST','Wire L1 B2','NUMERIC', True,'Wire-collimator temperature'],
              ['TCLVW_A5L1_B2_TTLD.POSST','Wire L1 B2','NUMERIC', True,'Wire-collimator temperature'],
              ['TCLVW_A5L1_B2_TTRU.POSST','Wire L1 B2','NUMERIC', True,'Wire-collimator temperature'],
              ['TCLVW_A5L1_B2_TTRD.POSST','Wire L1 B2','NUMERIC', True,'Wire-collimator temperature'],
                    
              ['TCTPH_4R5_B2_TTLU.POSST','Wire R5 B2','NUMERIC', True,'Wire-collimator temperature'],
              ['TCTPH_4R5_B2_TTLD.POSST','Wire R5 B2','NUMERIC', True,'Wire-collimator temperature'],
              ['TCTPH_4R5_B2_TTRU.POSST','Wire R5 B2','NUMERIC', True,'Wire-collimator temperature'],
              ['TCTPH_4R5_B2_TTRD.POSST','Wire R5 B2','NUMERIC', True,'Wire-collimator temperature'],
                    
              ['TCL_4L5_B2_TTLU.POSST','Wire L5 B2','NUMERIC', True,'Wire-collimator temperature'],
              ['TCL_4L5_B2_TTLD.POSST','Wire L5 B2','NUMERIC', True,'Wire-collimator temperature'],
              ['TCL_4L5_B2_TTRU.POSST','Wire L5 B2','NUMERIC', True,'Wire-collimator temperature'],
              ['TCL_4L5_B2_TTRD.POSST','Wire L5 B2','NUMERIC', True,'Wire-collimator temperature'],
                    
              ['TCTPV.4R1.B2:MEAS_MOTOR_LD','Wire R1 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCTPV.4R1.B2:MEAS_MOTOR_LU','Wire R1 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCTPV.4R1.B2:MEAS_MOTOR_RD','Wire R1 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCTPV.4R1.B2:MEAS_MOTOR_RU','Wire R1 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCTPV.4R1.B2:MEAS_V_MOTOR_POS','Wire R1 B2','NUMERIC', False,'Wire-collimator motor'],
                    
              ['TCLVW.A5L1.B2:MEAS_MOTOR_LD','Wire L1 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCLVW.A5L1.B2:MEAS_MOTOR_LU','Wire L1 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCLVW.A5L1.B2:MEAS_MOTOR_RD','Wire L1 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCLVW.A5L1.B2:MEAS_MOTOR_RU','Wire L1 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCLVW.A5L1.B2:MEAS_V_MOTOR_POS','Wire L1 B2','NUMERIC', False,'Wire-collimator motor'],
            
              ['TCTPH.4R5.B2:MEAS_MOTOR_LD','Wire R5 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCTPH.4R5.B2:MEAS_MOTOR_LU','Wire R5 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCTPH.4R5.B2:MEAS_MOTOR_RD','Wire R5 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCTPH.4R5.B2:MEAS_MOTOR_RU','Wire R5 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCTPH.4R5.B2:MEAS_V_MOTOR_POS','Wire R5 B2','NUMERIC', False,'Wire-collimator motor'],
                    
              ['TCL.4L5.B2:MEAS_MOTOR_LD','Wire L5 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCL.4L5.B2:MEAS_MOTOR_LU','Wire L5 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCL.4L5.B2:MEAS_MOTOR_RD','Wire L5 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCL.4L5.B2:MEAS_MOTOR_RU','Wire L5 B2','NUMERIC', False,'Wire-collimator motor'],
              ['TCL.4L5.B2:MEAS_V_MOTOR_POS','Wire L5 B2','NUMERIC', False,'Wire-collimator motor'],  
                    
              ['TCLVW.A5L1.B2:MEAS_LVDT_GD','Wire L1 B2','NUMERIC', False,'Wire-collimator LVDT gap'],
              ['TCLVW.A5L1.B2:MEAS_LVDT_GU','Wire L1 B2','NUMERIC', False,'Wire-collimator LVDT gap'],
              ['TCLVW.A5L1.B2:MEAS_LVDT_LD','Wire L1 B2','NUMERIC', False,'Wire-collimator LVDT'],
              ['TCLVW.A5L1.B2:MEAS_LVDT_LU','Wire L1 B2','NUMERIC', False,'Wire-collimator LVDT'],
              ['TCLVW.A5L1.B2:MEAS_LVDT_RD','Wire L1 B2','NUMERIC', False,'Wire-collimator LVDT'],  
              ['TCLVW.A5L1.B2:MEAS_LVDT_RU','Wire L1 B2','NUMERIC', False,'Wire-collimator LVDT'],
              ['TCLVW.A5L1.B2:MEAS_V_LVDT_POS','Wire L1 B2','NUMERIC', False,'Wire-collimator LVDT Vertical'],  


              ['TCTPV.4R1.B2:MEAS_LVDT_GD','Wire R1 B2','NUMERIC', False,'Wire-collimator LVDT gap'],
              ['TCTPV.4R1.B2:MEAS_LVDT_GU','Wire R1 B2','NUMERIC', False,'Wire-collimator LVDT gap'],
              ['TCTPV.4R1.B2:MEAS_LVDT_LD','Wire R1 B2','NUMERIC', False,'Wire-collimator LVDT'],
              ['TCTPV.4R1.B2:MEAS_LVDT_LU','Wire R1 B2','NUMERIC', False,'Wire-collimator LVDT'],
              ['TCTPV.4R1.B2:MEAS_LVDT_RD','Wire R1 B2','NUMERIC', False,'Wire-collimator LVDT'],  
              ['TCTPV.4R1.B2:MEAS_LVDT_RU','Wire R1 B2','NUMERIC', False,'Wire-collimator LVDT'],  
              ['TCTPV.4R1.B2:MEAS_V_LVDT_POS','Wire R1 B2','NUMERIC', False,'Wire-collimator LVDT Vertical'],  

                    
              ['TCL.4L5.B2:MEAS_LVDT_GD','Wire L5 B2','NUMERIC', False,'Wire-collimator LVDT gap'],
              ['TCL.4L5.B2:MEAS_LVDT_GU','Wire L5 B2','NUMERIC', False,'Wire-collimator LVDT gap'],
              ['TCL.4L5.B2:MEAS_LVDT_LD','Wire L5 B2','NUMERIC', False,'Wire-collimator LVDT'],
              ['TCL.4L5.B2:MEAS_LVDT_LU','Wire L5 B2','NUMERIC', False,'Wire-collimator LVDT'],
              ['TCL.4L5.B2:MEAS_LVDT_RD','Wire L5 B2','NUMERIC', False,'Wire-collimator LVDT'],  
              ['TCL.4L5.B2:MEAS_LVDT_RU','Wire L5 B2','NUMERIC', False,'Wire-collimator LVDT'],
              ['TCL.4L5.B2:MEAS_V_LVDT_POS','Wire L5 B2','NUMERIC', False,'Wire-collimator LVDT Vertical'],  


              ['TCTPH.4R5.B2:MEAS_LVDT_GD','Wire R5 B2','NUMERIC', False,'Wire-collimator LVDT gap'],
              ['TCTPH.4R5.B2:MEAS_LVDT_GU','Wire R5 B2','NUMERIC', False,'Wire-collimator LVDT gap'],
              ['TCTPH.4R5.B2:MEAS_LVDT_LD','Wire R5 B2','NUMERIC', False,'Wire-collimator LVDT'],
              ['TCTPH.4R5.B2:MEAS_LVDT_LU','Wire R5 B2','NUMERIC', False,'Wire-collimator LVDT'],
              ['TCTPH.4R5.B2:MEAS_LVDT_RD','Wire R5 B2','NUMERIC', False,'Wire-collimator LVDT'],  
              ['TCTPH.4R5.B2:MEAS_LVDT_RU','Wire R5 B2','NUMERIC', False,'Wire-collimator LVDT'],  
              ['TCTPH.4R5.B2:MEAS_V_LVDT_POS','Wire R5 B2','NUMERIC', False,'Wire-collimator LVDT Vertical'],  
              
              ['LHC.BOFSU:POSITIONS_H','Horizontal position','VECTOR NUMERIC', False, 'Beams H-position around the machine'],
              ['LHC.BOFSU:POSITIONS_V','Vertical position','VECTOR NUMERIC', False, 'Beams V-position around the machine']
      
              ],
                   columns=['Variable','Tag','Type','On change', 'Description'])
