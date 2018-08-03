import pandas as pd

LHC=pd.DataFrame([['LHC.BOFSU:OFC_ENERGY','Energy','NUMERIC',True,'Beam energy'],
              ['LHC.BCTFR.A6R4.B1:BEAM_INTENSITY','Intensity','NUMERIC',False,'B1 intensity'],
              ['LHC.BCTFR.A6R4.B2:BEAM_INTENSITY','Intensity','NUMERIC',False,'B2 intensity'],
              ['LHC.RUNCONFIG:IP1-XING-V-MURAD','Crossing angle','NUMERIC',True,'Crossing angle IP1 V'],
              ['LHC.RUNCONFIG:IP2-XING-V-MURAD','Crossing angle','NUMERIC',True,'Crossing angle IP2 V'],
              ['LHC.RUNCONFIG:IP5-XING-H-MURAD','Crossing angle','NUMERIC',True,'Crossing angle IP5 H'],
              ['LHC.RUNCONFIG:IP8-XING-H-MURAD','Crossing angle','NUMERIC',True,'Crossing angle IP8 H'],
              ['LHC.BQM.B1:BUNCH_LENGTH_MEAN','Bunch length','NUMERIC',False,'Bunch Length B1'],
              ['LHC.BQM.B2:BUNCH_LENGTH_MEAN','Bunch length','NUMERIC',False,'Bunch Length B2'],
              ['LHC.BQBBQ.CONTINUOUS.B1:TUNE_V', 'Tune','NUMERIC' , False, 'Tune V B1 BBQ'],
              ['LHC.BQBBQ.CONTINUOUS.B2:TUNE_V', 'Tune','NUMERIC', False, 'Tune V B2 BBQ'],
              ['LHC.BQBBQ.CONTINUOUS_HS.B1:TUNE_V', 'Tune','NUMERIC' , False,'Most sensitive tune B1 V'],
              ['LHC.BQBBQ.CONTINUOUS_HS.B2:TUNE_V', 'Tune','NUMERIC', False,'Most sensitive tune B2 V'],
              ['LHC.BQBBQ.CONTINUOUS.B1:TUNE_H', 'Tune','NUMERIC' , False, 'Tune H B1 BBQ'],
              ['LHC.BQBBQ.CONTINUOUS.B2:TUNE_H', 'Tune','NUMERIC', False, 'Tune H B2 BBQ'],
              ['LHC.BQBBQ.CONTINUOUS_HS.B1:TUNE_H', 'Tune','NUMERIC' , False,'Most sensitive tune B1 H'],
              ['LHC.BQBBQ.CONTINUOUS_HS.B2:TUNE_H', 'Tune','NUMERIC', False,'Most sensitive tune B2 H'],

              ['LHC.BQBBQ.CONTINUOUS.B1:FFT_DATA_H', 'Tune FFT','NUMERIC' , False, 'Tune FFT H B1'],
              ['LHC.BQBBQ.CONTINUOUS.B1:FFT_DATA_V', 'Tune FFT','NUMERIC', False, 'Tune FFT V B1'],
              ['LHC.BQBBQ.CONTINUOUS.B2:FFT_DATA_H', 'Tune FFT','NUMERIC' , False,'Tune FFT H B2'],
              ['LHC.BQBBQ.CONTINUOUS.B2:FFT_DATA_V', 'Tune FFT','NUMERIC', False,'Tune FFT V B2'],

              ['LHC.BCTFR.A6R4.B1:BUNCH_INTENSITY', 'Intensity', 'VECTOR NUMERIC', False, 'Main FBCT B1'],
              ['LHC.BCTFR.A6R4.B2:BUNCH_INTENSITY', 'Intensity', 'VECTOR NUMERIC', False, 'Main FBCT B2'],
              ['LHC.BCTFR.B6R4.B1:BUNCH_INTENSITY', 'Intensity', 'VECTOR NUMERIC', False, 'Spare FBCT B1'],
              ['LHC.BCTFR.A6R4.B2:BUNCH_INTENSITY', 'Intensity', 'VECTOR NUMERIC', False, 'Spare FBCT B2'],

              ['LHC.BCTFR.A6R4.B1:BUNCH_FILL_PATTERN', 'Filling Pattern', 'NUMERIC', False, 'Main FBCT B1'],
              ['LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN', 'Filling Pattern', 'NUMERIC', False, 'Main FBCT B2'],
              ['LHC.BCTFR.B6R4.B1:BUNCH_FILL_PATTERN', 'Filling Pattern', 'NUMERIC', False, 'Spare FBCT B1'],
              ['LHC.BCTFR.A6R4.B2:BUNCH_FILL_PATTERN', 'Filling Pattern', 'NUMERIC', False, 'Spare FBCT B2'],

              ['CMS:BUNCH_LUMI_INST', 'Luminosity', 'VECTOR NUMERIC', False, 'CMS bbb luminosity'],
              ['ATLAS:BUNCH_LUMI_INST', 'Luminosity', 'VECTOR NUMERIC', False, 'ATLAS bbb luminosity'],

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

              ['LHC.BLM.LIFETIME:B1_BEAM_LIFETIME', 'Lifetime', 'NUMERIC', False, 'BLM Lifetime B1'],
              ['LHC.BLM.LIFETIME:B1_CALIBRATED_LOSS', 'Losses', 'NUMERIC', False, 'BLM Calibrated losses B1'],
              ['LHC.BLM.LIFETIME:B2_BEAM_LIFETIME', 'Lifetime', 'NUMERIC', False, 'BLM Lifetime B2'],
              ['LHC.BLM.LIFETIME:B2_CALIBRATED_LOSS', 'Losses', 'NUMERIC', False, 'BLM Calibrated losses B2'],
              ['LHC.BLM.LIFETIME:LUMINOSITY_LOSS', 'Losses', 'NUMERIC', False, 'Luminosity Loss (protons)'],

              ['LHC.BOFSU:POSITIONS_H','Horizontal position','VECTOR NUMERIC', False, 'Beams H-position around the machine'],
              ['LHC.BOFSU:POSITIONS_V','Vertical position','VECTOR NUMERIC', False, 'Beams V-position around the machine'],

              ['HX:BETASTAR_IP1','Beta Star','NUMERIC', True, 'Beta Star at IP1'],
              ['HX:BETASTAR_IP2','Beta Star','NUMERIC', True, 'Beta Star at IP2'],
              ['HX:BETASTAR_IP5','Beta Star','NUMERIC', True, 'Beta Star at IP5'],
              ['HX:BETASTAR_IP8','Beta Star','NUMERIC', True, 'Beta Star at IP8'],
              ['RPHH.UA23.RQ5.L2B1:I_MEAS', 'Current', 	'NUMERIC', False	,'RQ5.L2B1 Power Converter Measured Current (A)'],

              ['RPTI.SR8.RBLWH.R8:POL_SWITCH_STATE','Polarity','TEXTUAL', True, 'Polarity of LHCb dipole'],
              ['LHC.BSRT.5R4.B1:BUNCH_EMITTANCE_H',	'Emittance', 'VECTORNUMERIC',	False, 'Bunch by bunch Hor emittance (um)'],
              ['LHC.BSRT.5R4.B1:BUNCH_EMITTANCE_V',	'Emittance', 'VECTORNUMERIC',	False, 'Bunch by bunch Ver emittance (um)'],
              ['LHC.BSRT.5L4.B2:BUNCH_EMITTANCE_H',	'Emittance', 'VECTORNUMERIC',	False, 'Bunch by bunch Hor emittance (um)'],
              ['LHC.BSRT.5L4.B2:BUNCH_EMITTANCE_V',	'Emittance', 'VECTORNUMERIC',	False, 'Bunch by bunch Ver emittance (um)'],

              ['ADTH.SR4.M1.B1:MDSPU_PHASE1', 'ADT Phase', 'NUMERIC', False, 'B1 Horizontal ADT Phase 1 Mon1 (deg)'],
              ['ADTH.SR4.M1.B1:MDSPU_PHASE2', 'ADT Phase', 'NUMERIC', False, 'B1 Horizontal ADT Phase 2 Mon1 (deg)'],
              ['ADTH.SR4.M1.B1:MDSPU_PHASE3', 'ADT Phase', 'NUMERIC', False, 'B1 Horizontal ADT Phase 3 Mon1 (deg)'],
              ['ADTH.SR4.M1.B1:MDSPU_PHASE4', 'ADT Phase', 'NUMERIC', False, 'B1 Horizontal ADT Phase 4 Mon1 (deg)'],

              ['ADTV.SR4.M1.B1:MDSPU_PHASE1', 'ADT Phase', 'NUMERIC', False, 'B1 Vertical ADT Phase 1 Mon1 (deg)'],
              ['ADTV.SR4.M1.B1:MDSPU_PHASE2', 'ADT Phase', 'NUMERIC', False, 'B1 Vertical ADT Phase 2 Mon1 (deg)'],
              ['ADTV.SR4.M1.B1:MDSPU_PHASE3', 'ADT Phase', 'NUMERIC', False, 'B1 Vertical ADT Phase 3 Mon1 (deg)'],
              ['ADTV.SR4.M1.B1:MDSPU_PHASE4', 'ADT Phase', 'NUMERIC', False, 'B1 Vertical ADT Phase 4 Mon1 (deg)'],

              ['ADTH.SR4.M1.B2:MDSPU_PHASE1', 'ADT Phase', 'NUMERIC', False, 'B2 Hozirontal ADT Phase 1 Mon1 (deg)'],
              ['ADTH.SR4.M1.B2:MDSPU_PHASE2', 'ADT Phase', 'NUMERIC', False, 'B2 Hozirontal ADT Phase 2 Mon1 (deg)'],
              ['ADTH.SR4.M1.B2:MDSPU_PHASE3', 'ADT Phase', 'NUMERIC', False, 'B2 Hozirontal ADT Phase 3 Mon1 (deg)'],
              ['ADTH.SR4.M1.B2:MDSPU_PHASE4', 'ADT Phase', 'NUMERIC', False, 'B2 Hozirontal ADT Phase 4 Mon1 (deg)'],

              ['ADTV.SR4.M1.B1:MDSPU_PHASE1', 'ADT Phase', 'NUMERIC', False, 'B2 Vertical ADT Phase 1 Mon1 (deg)'],
              ['ADTV.SR4.M1.B1:MDSPU_PHASE2', 'ADT Phase', 'NUMERIC', False, 'B2 Vertical ADT Phase 2 Mon1 (deg)'],
              ['ADTV.SR4.M1.B1:MDSPU_PHASE3', 'ADT Phase', 'NUMERIC', False, 'B2 Vertical ADT Phase 3 Mon1 (deg)'],
              ['ADTV.SR4.M1.B1:MDSPU_PHASE4', 'ADT Phase', 'NUMERIC', False, 'B2 Vertical ADT Phase 4 Mon1 (deg)'],


              ['ADTH.SR4.B1:TRANSVERSEACTIVITYMAX_HB1', 'ADT Activity', "NUMERIC", False, 'B1 Horizontal ADT Transverse Activity (um)'],
              ['ADTV.SR4.B1:TRANSVERSEACTIVITYMAX_VB1', 'ADT Activity', "NUMERIC", False, 'B1 Vertical ADT Transverse Activity (um)'],
              ['ADTH.SR4.B2:TRANSVERSEACTIVITYMAX_HB2', 'ADT Activity', "NUMERIC", False, 'B2 Horizontal ADT Transverse Activity (um)'],
              ['ADTV.SR4.B2:TRANSVERSEACTIVITYMAX_VB2', 'ADT Activity', "NUMERIC", False, 'B2 Vertical ADT Transverse Activity (um)'],


              ['LHC.BOFSU:DEFLECTIONS_H', 'Orbit', 	'VECTORNUMERIC', False,	'COD deflections in horizontal plane (urad)'],
              ['LHC.BOFSU:DEFLECTIONS_V', 'Orbit', 	'VECTORNUMERIC', False,	'COD deflections in vertical plane (urad)'],

              ['LHC.BPTUH.A4L5.B1:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Upstream Horizontal TCT.A4L5.B1 Calibrated Linearized beam position (mm)'],
              ['LHC.BPTUV.A4L5.B1:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Upstream Vertical TCT.A4L5.B1 Calibrated Linearized beam position (mm)'],
              ['LHC.BPTUH.A4R5.B2:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Upstream Horizontal TCT.A4R5.B2 Calibrated Linearized beam position (mm)'],
              ['LHC.BPTUV.A4R5.B2:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Upstream Vertical TCT.A4R5.B2 Calibrated Linearized beam position (mm)'],

              ['LHC.BPTDH.A4L5.B1:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Downstream Horizontal TCT.A4L5.B1 Calibrated Linearized beam position (mm)'],
              ['LHC.BPTDV.A4L5.B1:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Downstream Vertical TCT.A4L5.B1 Calibrated Linearized beam position (mm)'],
              ['LHC.BPTDH.A4R5.B2:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Downstream Horizontal TCT.A4R5.B2 Calibrated Linearized beam position (mm)'],
              ['LHC.BPTDV.A4R5.B2:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Downstream Vertical TCT.A4R5.B2 Calibrated Linearized beam position (mm)'],



              ['LHC.BPTUH.A4L1.B1:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Upstream Horizontal TCT.A4L1.B1 Calibrated Linearized beam position (mm)'],
              ['LHC.BPTUV.A4L1.B1:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Upstream Vertical TCT.A4L1.B1 Calibrated Linearized beam position (mm)'],
              ['LHC.BPTUH.A4R1.B2:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Upstream Horizontal TCT.A4R1.B2 Calibrated Linearized beam position (mm)'],
              ['LHC.BPTUV.A4R1.B2:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Upstream Vertical TCT.A4R1.B2 Calibrated Linearized beam position (mm)'],

              ['LHC.BPTDH.A4L1.B1:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Downstream Horizontal TCT.A4L1.B1 Calibrated Linearized beam position (mm)'],
              ['LHC.BPTDV.A4L1.B1:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Downstream Vertical TCT.A4L1.B1 Calibrated Linearized beam position (mm)'],
              ['LHC.BPTDH.A4R1.B2:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Downstream Horizontal TCT.A4R1.B2 Calibrated Linearized beam position (mm)'],
              ['LHC.BPTDV.A4R1.B2:CALIBLINEARPOS', 'Orbit', 'NUMERIC', False, 'Downstream Vertical TCT.A4R1.B2 Calibrated Linearized beam position (mm)'],

              ],
                   columns=['Variable','Tag','Type','On change', 'Description'])
