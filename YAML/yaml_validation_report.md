# YAML validation report

- YAML root: `D:\Repos\METIS_Simulations\YAML`
- Files scanned: **81**
- PyYAML parse failures: **2**
- Static validation failures: **65**
- runSimulationBlock acceptance failures: **15**
- Passed: **14**

A file counts as passing only when it clears all three checks.

## PyYAML parse failures

### `ESO\flatTwilightLM.yaml`

```text
ScannerError: while scanning a simple key
  in "D:\Repos\METIS_Simulations\YAML\ESO\flatTwilightLM.yaml", line 14, column 5
could not find expected ':'
  in "D:\Repos\METIS_Simulations\YAML\ESO\flatTwilightLM.yaml", line 15, column 5
```

### `ESO\flatTwilightN.yaml`

```text
ScannerError: while scanning a simple key
  in "D:\Repos\METIS_Simulations\YAML\ESO\flatTwilightN.yaml", line 14, column 5
could not find expected ':'
  in "D:\Repos\METIS_Simulations\YAML\ESO\flatTwilightN.yaml", line 15, column 5
```

## Static validation issues

From `metis_simulations.runRecipes.validate_recipes` — checks required keys, filter/ND/catg/tech/type/mode allow-lists, and positive `nObs`/`ndit`/`dit`.

### `AIT_Tests\LMS_OPT_01\LMS_OPT_1.yaml`

- Recipe LMS_OPT_1_WCU_OFF has invalid MODE of wcu_lms)
- Recipe LMS_OPT_1_grid_WCU_OFF has invalid MODE of wcu_lms)
- Recipe LMS_OPT_1_WCU_ON has invalid MODE of wcu_lms)
- Recipe LMS_OPT_1_grid_WCU_ON has invalid MODE of wcu_lms)

### `AIT_Tests\LMS_OPT_02\LMS_OPT_2.yaml`

- Recipe LMS_OPT_02_IFU_WCU_OFF_RAW has invalid MODE of wcu_lms)
- Recipe LMS_OPT_02_IFU_DISTORTION_RAW has invalid MODE of wcu_lms)

### `AIT_Tests\LMS_RAD_01\LMS_RAD_01.yaml`

- Recipe LMS_RAD_01_DARK_IFU_RAW_01 has invalid TYPE of DARK)
- Recipe LMS_RAD_01_DARK_IFU_RAW_01 has invalid MODE of wcu_lms)
- Recipe LMS_RAD_01_DARK_IFU_RAW_02 has invalid TYPE of DARK)
- Recipe LMS_RAD_01_DARK_IFU_RAW_02 has invalid MODE of wcu_lms)
- Recipe LMS_RAD_01_DARK_IFU_RAW_03 has invalid TYPE of DARK)
- Recipe LMS_RAD_01_DARK_IFU_RAW_03 has invalid MODE of wcu_lms)
- Recipe LMS_RAD_01_DARK_IFU_RAW_04 has invalid TYPE of DARK)
- Recipe LMS_RAD_01_DARK_IFU_RAW_04 has invalid MODE of wcu_lms)

### `AIT_Tests\LMS_RAD_06\LMS_RAD_06.yaml`

- Recipe DETLIN_IFU_RAW1 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW2 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW3 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW4 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW5 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW6 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW7 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW8 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW9 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW10 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW11 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW12 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW13 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW14 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW15 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW16 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW17 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW18 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW19 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW20 has invalid MODE of wcu_lms)

### `AIT_Tests\LMS_RAD_06\LMS_RAD_06_1.yaml`

- Recipe DETLIN_IFU_RAW1 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW2 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW3 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW4 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW5 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW6 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW7 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW8 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW9 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW10 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW11 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW12 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW13 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW14 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW15 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW16 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW17 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW18 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW19 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW20 has invalid MODE of wcu_lms)

### `AIT_Tests\LMS_RAD_06\LMS_RAD_06_2.yaml`

- Recipe DETLIN_IFU_RAW1 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW2 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW3 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW4 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW5 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW6 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW7 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW8 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW9 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW10 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW11 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW12 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW13 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW14 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW15 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW16 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW17 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW18 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW19 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW20 has invalid MODE of wcu_lms)

### `AIT_Tests\LMS_RAD_06\LMS_RAD_06_3.yaml`

- Recipe DETLIN_IFU_RAW1 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW2 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW3 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW4 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW5 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW6 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW7 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW8 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW9 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW10 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW11 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW12 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW13 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW14 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW15 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW16 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW17 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW18 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW19 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW20 has invalid MODE of wcu_lms)

### `AIT_Tests\LMS_RAD_06\LMS_RAD_06_4.yaml`

- Recipe DETLIN_IFU_RAW1 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW2 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW3 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW4 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW5 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW6 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW7 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW8 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW9 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW10 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW11 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW12 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW13 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW14 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW15 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW16 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW17 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW18 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW19 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW20 has invalid MODE of wcu_lms)

### `AIT_Tests\LMS_RAD_06\LMS_RAD_06_5.yaml`

- Recipe DETLIN_IFU_RAW1 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW2 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW3 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW4 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW5 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW6 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW7 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW8 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW9 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW10 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW11 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW12 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW13 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW14 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW15 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW16 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW17 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW18 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW19 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW20 has invalid MODE of wcu_lms)

### `AIT_Tests\LMS_RAD_06\LMS_RAD_06_6.yaml`

- Recipe DETLIN_IFU_RAW1 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW2 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW3 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW4 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW5 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW6 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW7 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW8 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW9 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW10 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW11 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW12 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW13 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW14 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW15 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW16 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW17 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW18 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW19 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW20 has invalid MODE of wcu_lms)

### `AIT_Tests\LMS_RAD_10\LMS_RAD_10.yaml`

- Recipe LMS_RAD_10_bg_02 has invalid MODE of wcu_lms)

### `AIT_Tests\LSS_RAD_03\LSS_RAD_03_lm.yaml`

- Recipe LM_LSS_SCI_RAW_L has invalid MODE of wcu_lss_l)
- Recipe LM_LSS_SCI_RAW_M has invalid MODE of wcu_lss_m)
- Recipe LM_LSS_SCI_RAW_L_ND has invalid MODE of wcu_lss_l)
- Recipe LM_LSS_SCI_RAW_M_ND has invalid MODE of wcu_lss_m)

### `AIT_Tests\LSS_RAD_03\LSS_RAD_03_n.yaml`

- Recipe LM_LSS_SCI_RAW_N has invalid MODE of wcu_lss_n)

### `AIT_Tests\LSS_RAD_04\LSS_RAD_04_lm.yaml`

- Recipe LM_LSS_SCI_RAW has invalid MODE of wcu_lss_l)

### `AIT_Tests\LSS_RAD_04\LSS_RAD_04_n.yaml`

- Recipe N_LSS_SCI_RAW has invalid MODE of wcu_lss_n)

### `AIT_Tests\LSS_RAD_12\LSS_RAD_12_lm.yaml`

- Recipe L_LSS_SCI_RAW_1 has invalid MODE of wcu_lss_l)
- Recipe L_LSS_SCI_RAW_2 has invalid MODE of wcu_lss_l)
- Recipe L_LSS_SCI_RAW_3 has invalid MODE of wcu_lss_l)
- Recipe L_LSS_SCI_RAW_4 has invalid MODE of wcu_lss_l)
- Recipe L_LSS_SCI_RAW_5 has invalid MODE of wcu_lss_l)
- Recipe L_LSS_SCI_RAW_6 has invalid MODE of wcu_lss_l)
- Recipe L_LSS_SCI_RAW_7 has invalid MODE of wcu_lss_l)
- Recipe L_LSS_SCI_RAW_8 has invalid MODE of wcu_lss_l)
- Recipe L_LSS_SCI_RAW_9 has invalid MODE of wcu_lss_l)
- Recipe L_LSS_SCI_RAW_10 has invalid MODE of wcu_lss_l)
- Recipe L_LSS_SCI_RAW_11 has invalid MODE of wcu_lss_l)
- Recipe M_LSS_SCI_RAW_1 has invalid MODE of wcu_lss_m)
- Recipe M_LSS_SCI_RAW_2 has invalid MODE of wcu_lss_m)
- Recipe M_LSS_SCI_RAW_3 has invalid MODE of wcu_lss_m)
- Recipe M_LSS_SCI_RAW_4 has invalid MODE of wcu_lss_m)

### `AIT_Tests\LSS_RAD_12\LSS_RAD_12_n.yaml`

- Recipe N_LSS_SCI_RAW_1 has invalid MODE of wcu_lss_n)
- Recipe N_LSS_SCI_RAW_2 has invalid MODE of wcu_lss_n)
- Recipe N_LSS_SCI_RAW_3 has invalid MODE of wcu_lss_n)
- Recipe N_LSS_SCI_RAW_4 has invalid MODE of wcu_lss_n)
- Recipe N_LSS_SCI_RAW_5 has invalid MODE of wcu_lss_n)
- Recipe N_LSS_SCI_RAW_6 has invalid MODE of wcu_lss_n)
- Recipe N_LSS_SCI_RAW_7 has invalid MODE of wcu_lss_n)
- Recipe N_LSS_SCI_RAW_8 has invalid MODE of wcu_lss_n)
- Recipe N_LSS_SCI_RAW_9 has invalid MODE of wcu_lss_n)
- Recipe N_LSS_SCI_RAW_10 has invalid MODE of wcu_lss_n)
- Recipe N_LSS_SCI_RAW_11 has invalid MODE of wcu_lss_n)
- Recipe N_LSS_SCI_RAW_12 has invalid MODE of wcu_lss_n)

### `ESO\allRecipes.yaml`

- Recipe PERSISTENCE_MAP_LM has invalid TYPE of PERSISTENCE)
- Recipe PERSISTENCE_MAP_N has invalid TYPE of PERSISTENCE)
- Recipe PERSISTENCE_MAP_IFU has invalid TECH of IFU)
- Recipe PERSISTENCE_MAP_IFU has invalid TYPE of PERSISTENCE)
- Recipe DETLIN_2RG_RAW has invalid MODE of wcu_img_lm)
- Recipe DETLIN_GEO_RAW has invalid MODE of wcu_img_n)
- Recipe LM_LSS_RSRF_RAW has invalid MODE of wcu_lss_l)
- Recipe LM_LSS_RSRF_PINH_RAW has invalid TYPE of FLAT,LAMP,PINH)
- Recipe LM_LSS_RSRF_PINH_RAW has invalid MODE of wcu_lss_l)
- Recipe N_LSS_RSRF_RAW has invalid MODE of wcu_lss_n)
- Recipe N_LSS_RSRF_PINH_RAW has invalid TYPE of FLAT,LAMP,PINH)
- Recipe N_LSS_RSRF_PINH_RAW has invalid MODE of wcu_lss_n)
- Recipe DETLIN_IFU_RAW has invalid TECH of IFU)
- Recipe DETLIN_IFU_RAW has invalid MODE of wcu_lms)
- Recipe IFU_DISTORTION_RAW has invalid TECH of IFU)
- Recipe IFU_WAVE_RAW has invalid TECH of IFU)
- Recipe IFU_SCI_RAW has invalid TECH of IFU)
- Recipe IFU_SCI_SKY_RAW has invalid TECH of IFU)
- Recipe IFU_STD_RAW has invalid TECH of IFU)
- Recipe IFU_STD_SKY_RAW has invalid TECH of IFU)
- Recipe IFU_RSRF_RAW1 has invalid TECH of IFU)
- Recipe IFU_RSRF_RAW1 has invalid TYPE of RSRF)
- Recipe IFU_RSRF_RAW1 has invalid MODE of wcu_lms)
- Recipe IFU_RSRF_RAW2 has invalid TECH of IFU)
- Recipe IFU_RSRF_RAW2 has invalid TYPE of RSRF)
- Recipe IFU_RSRF_RAW2 has invalid MODE of wcu_lms)
- Recipe IFU_WCU_OFF1 has invalid TECH of IFU)
- Recipe IFU_WCU_OFF1 has invalid TYPE of RSRF)
- Recipe IFU_WCU_OFF1 has invalid MODE of wcu_lms)
- Recipe IFU_SKY_RAW1 has invalid TECH of IFU)
- Recipe IFU_OFF_AXIS_PSF_RAW has invalid TECH of IFU)
- Recipe LM_SLITLOSSES_RAW1 Filter value of open not valid for mode lss_l
- Recipe N_LSS_SLITLOSSES_RAW1 Filter value of open not valid for mode lss_n
- Recipe LM_PUPIL_RAW has invalid TECH of PUP,LM)

### `ESO\calib.yaml`

- Recipe LM_PUPIL_RAW has invalid TECH of PUP,LM)
- Recipe IFU_DISTORTION_RAW does not contain required field filter_name for recipe IFU_DISTORTION_RAW

### `ESO\chophomeN.yaml`

- Top-level YAML is not a mapping (got NoneType); expected a dict of named recipes.

### `ESO\darkIFU.yaml`

- Recipe DARK_IFU_RAW has invalid TECH of IFU)
- Recipe DARK_IFU_RAW has invalid TYPE of DARK)
- Recipe DARK_IFU_RAW has invalid MODE of wcu_lms)

### `ESO\darkLM.yaml`

- Recipe DARK_LM_RAW has invalid TYPE of DARK)

### `ESO\darkN.yaml`

- Recipe DARK_N_RAW has invalid TYPE of DARK)

### `ESO\detlinIFU.yaml`

- Recipe DETLIN_IFU_RAW1 has invalid TECH of IFU)
- Recipe DETLIN_IFU_RAW1 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW2 has invalid TECH of IFU)
- Recipe DETLIN_IFU_RAW2 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW3 has invalid TECH of IFU)
- Recipe DETLIN_IFU_RAW3 has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW4 has invalid TECH of IFU)
- Recipe DETLIN_IFU_RAW4 has invalid MODE of wcu_lms)

### `ESO\detlinLM.yaml`

- Recipe DETLIN_2RG_RAW1 has invalid MODE of wcu_img_lm)
- Recipe DETLIN_2RG_RAW2 has invalid MODE of wcu_img_lm)
- Recipe DETLIN_2RG_RAW3 has invalid MODE of wcu_img_lm)
- Recipe DETLIN_2RG_RAW4 has invalid MODE of wcu_img_lm)

### `ESO\detlinN.yaml`

- Recipe DETLIN_GEO_RAW1 has invalid MODE of wcu_img_n)
- Recipe DETLIN_GEO_RAW2 has invalid MODE of wcu_img_n)
- Recipe DETLIN_GEO_RAW3 has invalid MODE of wcu_img_n)
- Recipe DETLIN_GEO_RAW4 has invalid MODE of wcu_img_n)

### `ESO\distortionIFU.yaml`

- Recipe IFU_DISTORTION_RAW has invalid TECH of IFU)
- Recipe IFU_DISTORTION_RAW has invalid MODE of wcu_lms)

### `ESO\distortionLM.yaml`

- Recipe LM_DISTORTION_RAW has invalid MODE of wcu_img_lm)

### `ESO\distortionN.yaml`

- Recipe N_DISTORTION_RAW has invalid MODE of wcu_img_n)

### `ESO\flatLampLM.yaml`

- Recipe WCU_FLAT_LM_RAW does not contain required field nObs for recipe WCU_FLAT_LM_RAW

### `ESO\flatLampLMLp.yaml`

- Recipe WCU_FLAT_LM_RAW1 has invalid MODE of wcu_img_lm)

### `ESO\flatLampN.yaml`

- Recipe WCU_FLAT_N_RAW does not contain required field nObs for recipe WCU_FLAT_N_RAW

### `ESO\flatTwilightLMLp.yaml`

- Recipe LM_FLAT_TWILIGHT_RAW has invalid TYPE of FLAT,TWILIGHT)

### `ESO\ifu-rsrf.yaml`

- Recipe IFU_RSRF_RAW1 has invalid TECH of IFU)
- Recipe IFU_RSRF_RAW1 has invalid TYPE of RSRF)
- Recipe IFU_RSRF_RAW1 has invalid MODE of wcu_lms)
- Recipe IFU_RSRF_RAW2 has invalid TECH of IFU)
- Recipe IFU_RSRF_RAW2 has invalid TYPE of RSRF)
- Recipe IFU_RSRF_RAW2 has invalid MODE of wcu_lms)
- Recipe IFU_WCU_OFF1 has invalid TECH of IFU)
- Recipe IFU_WCU_OFF1 has invalid TYPE of RSRF)
- Recipe IFU_WCU_OFF1 has invalid MODE of wcu_lms)
- Recipe IFU_SKY_RAW1 has invalid TECH of IFU)

### `ESO\ifu.yaml`

- Recipe DETLIN_IFU_RAW has invalid TECH of IFU)
- Recipe DETLIN_IFU_RAW has invalid MODE of wcu_lms)
- Recipe IFU_DISTORTION_RAW has invalid TECH of IFU)
- Recipe IFU_DISTORTION_RAW has invalid MODE of wcu_lms)
- Recipe IFU_WAVE_RAW has invalid TECH of IFU)
- Recipe IFU_SCI_RAW has invalid TECH of IFU)
- Recipe IFU_SCI_SKY_RAW has invalid TECH of IFU)
- Recipe IFU_STD_RAW has invalid TECH of IFU)
- Recipe IFU_STD_SKY_RAW has invalid TECH of IFU)
- Recipe IFU_RSRF_RAW1 has invalid TECH of IFU)
- Recipe IFU_RSRF_RAW1 has invalid TYPE of RSRF)
- Recipe IFU_RSRF_RAW1 has invalid MODE of wcu_lms)
- Recipe IFU_RSRF_RAW2 has invalid TECH of IFU)
- Recipe IFU_RSRF_RAW2 has invalid TYPE of RSRF)
- Recipe IFU_RSRF_RAW2 has invalid MODE of wcu_lms)
- Recipe IFU_WCU_OFF1 has invalid TECH of IFU)
- Recipe IFU_WCU_OFF1 has invalid TYPE of RSRF)
- Recipe IFU_WCU_OFF1 has invalid MODE of wcu_lms)
- Recipe IFU_SKY_RAW1 has invalid TECH of IFU)

### `ESO\imgLM.yaml`

- Recipe DETLIN_2RG_RAW has invalid MODE of wcu_img_lm)
- Recipe LM_DISTORTION_RAW has invalid MODE of wcu_img_lm)

### `ESO\imgN.yaml`

- Recipe DETLIN_GEO_RAW has invalid MODE of wcu_img_n)
- Recipe N_DISTORTION_RAW has invalid MODE of wcu_img_n)

### `ESO\lssLM.yaml`

- Recipe LM_LSS_RSRF_RAW has invalid MODE of wcu_lss_l)
- Recipe LM_LSS_RSRF_PINH_RAW has invalid TYPE of FLAT,LAMP,PINH)
- Recipe LM_LSS_RSRF_PINH_RAW has invalid MODE of wcu_lss_l)
- Recipe DETLIN_2RG_RAW has invalid MODE of wcu_img_lm)
- Recipe LM_LSS_WAVE_RAW Filter value of open not valid for mode lss_l

### `ESO\lssN.yaml`

- Recipe N_LSS_RSRF_RAW has invalid MODE of wcu_lss_n)
- Recipe N_LSS_RSRF_PINH_RAW has invalid TYPE of FLAT,LAMP,PINH)
- Recipe N_LSS_RSRF_PINH_RAW has invalid MODE of wcu_lss_n)
- Recipe DETLIN_GEO_RAW has invalid MODE of wcu_img_n)
- Recipe N_LSS_WAVE_RAW Filter value of open not valid for mode lss_n

### `ESO\metis_det_dark.yaml`

- Recipe DARK_LM_RAW has invalid TYPE of DARK)
- Recipe DARK_N_RAW has invalid TYPE of DARK)
- Recipe DARK_IFU_RAW has invalid TECH of IFU)
- Recipe DARK_IFU_RAW has invalid TYPE of DARK)

### `ESO\offAxisIFU.yaml`

- Recipe IFU_OFF_AXIS_PSF_RAW has invalid TECH of IFU)

### `ESO\persistIfu.yaml`

- Recipe PERSISTENCE_MAP_IFU has invalid TECH of IFU)
- Recipe PERSISTENCE_MAP_IFU has invalid TYPE of PERSISTENCE)

### `ESO\persistLM.yaml`

- Recipe PERSISTENCE_MAP_LM has invalid TYPE of PERSISTENCE)

### `ESO\persistN.yaml`

- Recipe PERSISTENCE_MAP_N has invalid TYPE of PERSISTENCE)

### `ESO\pupilLM.yaml`

- Recipe LM_PUPIL_RAW has invalid TECH of PUP,LM)

### `ESO\rsrfIFU.yaml`

- Recipe IFU_RSRF_RAW1 has invalid TECH of IFU)
- Recipe IFU_RSRF_RAW1 has invalid TYPE of RSRF)
- Recipe IFU_RSRF_RAW1 has invalid MODE of wcu_lms)
- Recipe IFU_RSRF_RAW2 has invalid TECH of IFU)
- Recipe IFU_RSRF_RAW2 has invalid TYPE of RSRF)
- Recipe IFU_RSRF_RAW2 has invalid MODE of wcu_lms)

### `ESO\rsrfLSS.yaml`

- Recipe LM_LSS_RSRF_RAW1 has invalid MODE of wcu_lss_l)
- Recipe LM_LSS_RSRF_RAW2 has invalid MODE of wcu_lss_l)

### `ESO\rsrfLSSLM.yaml`

- Recipe LM_LSS_RSRF_RAW1 has invalid MODE of wcu_lss_l)
- Recipe LM_LSS_RSRF_RAW2 has invalid MODE of wcu_lss_l)

### `ESO\rsrfLSSN.yaml`

- Recipe N_LSS_RSRF_RAW1 has invalid MODE of wcu_lss_n)
- Recipe N_LSS_RSRF_RAW2 has invalid MODE of wcu_lss_n)

### `ESO\rsrfPinhIFU.yaml`

- Recipe IFU_RSRF_PINH_RAW1 has invalid TECH of IFU)
- Recipe IFU_RSRF_PINH_RAW1 has invalid TYPE of RSRF)
- Recipe IFU_RSRF_PINH_RAW1 has invalid MODE of wcu_lms)
- Recipe IFU_RSRF_PINH_RAW2 has invalid TECH of IFU)
- Recipe IFU_RSRF_PINH_RAW2 has invalid TYPE of RSRF)
- Recipe IFU_RSRF_PINH_RAW2 has invalid MODE of wcu_lms)

### `ESO\rsrfPinhLSSLM.yaml`

- Recipe LM_LSS_RSRF_PINH_RAW1 has invalid TYPE of FLAT,LAMP,PINH)
- Recipe LM_LSS_RSRF_PINH_RAW1 has invalid MODE of wcu_lss_l)
- Recipe LM_LSS_RSRF_PINH_RAW2 has invalid TYPE of FLAT,LAMP,PINH)
- Recipe LM_LSS_RSRF_PINH_RAW2 has invalid MODE of wcu_lss_l)

### `ESO\rsrfPinhLSSN.yaml`

- Recipe N_LSS_RSRF_PINH_RAW1 has invalid TYPE of FLAT,LAMP,PINH)
- Recipe N_LSS_RSRF_PINH_RAW1 has invalid MODE of wcu_lss_n)
- Recipe N_LSS_RSRF_PINH_RAW2 has invalid TYPE of FLAT,LAMP,PINH)
- Recipe N_LSS_RSRF_PINH_RAW2 has invalid MODE of wcu_lss_n)

### `ESO\scienceIFU.yaml`

- Recipe IFU_SCI_RAW has invalid TECH of IFU)
- Recipe IFU_SCI_SKY_RAW has invalid TECH of IFU)

### `ESO\scienceLSSN.yaml`

- Recipe N_LSS_SCI_RAW Filter value of open not valid for mode lss_n
- Recipe N_LSS_SCI_SKY_RAW Filter value of open not valid for mode lss_n

### `ESO\slitlossLSSLM.yaml`

- Recipe LM_SLITLOSSES_RAW1 Filter value of open not valid for mode lss_l

### `ESO\slitlossLSSN.yaml`

- Recipe N_LSS_SLITLOSSES_RAW1 Filter value of open not valid for mode lss_n

### `ESO\stdIFU.yaml`

- Recipe IFU_STD_RAW has invalid TECH of IFU)
- Recipe IFU_STD_SKY_RAW has invalid TECH of IFU)

### `ESO\stdLSSN.yaml`

- Recipe N_LSS_STD_RAW Filter value of open not valid for mode lss_n
- Recipe N_LSS_STD_SKY_RAW Filter value of open not valid for mode lss_n

### `ESO\testYAML.yaml`

- Recipe DARK_LM_RAW has invalid TYPE of DARK)
- Recipe DARK_N_RAW has invalid TYPE of DARK)
- Recipe DETLIN_2RG_RAW1 has invalid MODE of wcu_img_lm)
- Recipe DETLIN_GEO_RAW1 has invalid MODE of wcu_img_n)
- Recipe LM_DISTORTION_RAW has invalid MODE of wcu_img_lm)
- Recipe N_DISTORTION_RAW has invalid MODE of wcu_img_n)
- Recipe WCU_FLAT_LM_RAW has invalid MODE of wcu_img_lm)
- Recipe WCU_FLAT_N_RAW has invalid MODE of wcu_img_n)
- Recipe LM_FLAT_TWILIGHT_RAW has invalid TYPE of FLAT,TWILIGHT)
- Recipe N_FLAT_TWILIGHT_RAW has invalid TYPE of FLAT,TWILIGHT)
- Recipe PERSISTENCE_MAP_LM has invalid TYPE of PERSISTENCE)
- Recipe PERSISTENCE_MAP_N has invalid TYPE of PERSISTENCE)
- Recipe LM_PUPIL_RAW has invalid TECH of PUP,LM)
- Recipe IFU_WCU_OFF_RAW has invalid TECH of IFU)
- Recipe IFU_WCU_OFF_RAW has invalid TYPE of DARK,WCU_OFF)
- Recipe IFU_WCU_OFF_RAW has invalid MODE of wcu_lms)
- Recipe LM_WCU_OFF_RAW has invalid TYPE of DARK,WCU_OFF)
- Recipe LM_WCU_OFF_RAW has invalid MODE of wcu_img_lm)
- Recipe N_WCU_OFF_RAW has invalid TYPE of DARK,WCU_OFF)
- Recipe N_WCU_OFF_RAW has invalid MODE of wcu_img_n)
- Recipe DARK_IFU_RAW has invalid TECH of IFU)
- Recipe DARK_IFU_RAW has invalid TYPE of DARK)
- Recipe DARK_IFU_RAW has invalid MODE of wcu_lms)
- Recipe DETLIN_IFU_RAW1 has invalid TECH of IFU)
- Recipe DETLIN_IFU_RAW1 has invalid MODE of wcu_lms)
- Recipe IFU_DISTORTION_RAW has invalid TECH of IFU)
- Recipe IFU_DISTORTION_RAW has invalid MODE of wcu_lms)
- Recipe IFU_OFF_AXIS_PSF_RAW has invalid TECH of IFU)
- Recipe PERSISTENCE_MAP_IFU has invalid TECH of IFU)
- Recipe PERSISTENCE_MAP_IFU has invalid TYPE of PERSISTENCE)
- Recipe IFU_RSRF_RAW1 has invalid TECH of IFU)
- Recipe IFU_RSRF_RAW1 has invalid TYPE of RSRF)
- Recipe IFU_RSRF_RAW1 has invalid MODE of wcu_lms)
- Recipe IFU_RSRF_PINH_RAW1 has invalid TECH of IFU)
- Recipe IFU_RSRF_PINH_RAW1 has invalid TYPE of RSRF)
- Recipe IFU_RSRF_PINH_RAW1 has invalid MODE of wcu_lms)
- Recipe IFU_SCI_RAW has invalid TECH of IFU)
- Recipe IFU_SCI_SKY_RAW has invalid TECH of IFU)
- Recipe IFU_STD_RAW has invalid TECH of IFU)
- Recipe IFU_STD_SKY_RAW has invalid TECH of IFU)
- Recipe IFU_WAVE_RAW ND Filter value of ND-2.8 not valid
- Recipe IFU_WAVE_RAW has invalid TECH of IFU)
- Recipe IFU_WAVE_RAW has invalid MODE of wcu_lms)
- Recipe LM_LSS_RSRF_RAW1 has invalid MODE of wcu_lss_l)
- Recipe N_LSS_RSRF_RAW1 has invalid MODE of wcu_lss_n)
- Recipe LM_LSS_RSRF_PINH_RAW1 has invalid TYPE of FLAT,LAMP,PINH)
- Recipe LM_LSS_RSRF_PINH_RAW1 has invalid MODE of wcu_lss_l)
- Recipe N_LSS_RSRF_PINH_RAW1 has invalid TYPE of FLAT,LAMP,PINH)
- Recipe N_LSS_RSRF_PINH_RAW1 has invalid MODE of wcu_lss_n)
- Recipe LM_LSS_WAVE_RAW has invalid MODE of wcu_lss_l)
- Recipe N_LSS_WAVE_RAW has invalid MODE of wcu_lss_n)

### `ESO\wavecalIFU.yaml`

- Recipe IFU_WAVE_RAW ND Filter value of ND-2.8 not valid
- Recipe IFU_WAVE_RAW has invalid TECH of IFU)
- Recipe IFU_WAVE_RAW has invalid MODE of wcu_lms)

### `ESO\wavecalLSSLM.yaml`

- Recipe LM_LSS_WAVE_RAW has invalid MODE of wcu_lss_l)

### `ESO\wavecalLSSN.yaml`

- Recipe N_LSS_WAVE_RAW has invalid MODE of wcu_lss_n)

### `ESO\wcuOffIFU.yaml`

- Recipe IFU_WCU_OFF_RAW does not contain required field properties for recipe IFU_WCU_OFF_RAW

### `ESO\wcuOffLM.yaml`

- Recipe LM_WCU_OFF_RAW does not contain required field properties for recipe LM_WCU_OFF_RAW

### `ESO\wcuOffN.yaml`

- Recipe N_WCU_OFF_RAW does not contain required field properties for recipe N_WCU_OFF_RAW

## runSimulationBlock acceptance failures

### `ESO\allRecipes.yaml`

**Top-level error:**

```text
KeyError: 'ndfilter_name'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
    rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
  File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 38, in runSimulationBlock
    simulationSet.runSimulations()
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 184, in runSimulations
    self._run(self.allrcps)
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 384, in _run
    recipeDark["properties"]["ndfilter_name"] = recipe["properties"]["ndfilter_name"]
                                               ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
KeyError: 'ndfilter_name'
```

**Failing YAML entries:**

- `PERSISTENCE_MAP_LM`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `PERSISTENCE_MAP_N`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `PERSISTENCE_MAP_IFU`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `DETLIN_2RG_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_DISTORTION_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_IMAGE_SCI_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_IMAGE_SCI_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_IMAGE_STD_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_IMAGE_STD_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `DETLIN_GEO_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_DISTORTION_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_IMAGE_SCI_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_IMAGE_SCI_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_IMAGE_STD_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_IMAGE_STD_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_LSS_RSRF_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_LSS_RSRF_PINH_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_LSS_WAVE_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_LSS_SCI_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_LSS_SCI_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_LSS_STD_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_LSS_STD_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_LSS_RSRF_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_LSS_RSRF_PINH_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_LSS_WAVE_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_LSS_SCI_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_LSS_SCI_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_LSS_STD_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_LSS_STD_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `DETLIN_IFU_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_DISTORTION_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_WAVE_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_SCI_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_SCI_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_STD_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_STD_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_SKY_RAW1`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_OFF_AXIS_PSF_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_OFF_AXIS_PSF_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_OFF_AXIS_PSF_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_IMAGE_SCI_CORONAGRAPH_RAW1`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_IMAGE_SCI_CORONAGRAPH_RAW2`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_IMAGE_SCI_CORONAGRAPH_RAW3`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_IMAGE_SCI_CORONAGRAPH_RAW4`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_SCI_CORONAGRAPH_RAW1`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_SCI_CORONAGRAPH_RAW2`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_SLITLOSSES_RAW1`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_LSS_SLITLOSSES_RAW1`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_CHOPHOME_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_PUPIL_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_PUPIL_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

### `ESO\calib.yaml`

**Top-level error:**

```text
KeyError: 'ndfilter_name'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
    rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
  File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 49, in runSimulationBlock
    simulationSet.calculateCalibs()
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 439, in calculateCalibs
    flatParms.append((props['filter_name'],props['ndfilter_name'],props['tech']))
                                           ~~~~~^^^^^^^^^^^^^^^^^
KeyError: 'ndfilter_name'
```

**Failing YAML entries:**

- `LM_SLITLOSSES_RAW1`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_LSS_SLITLOSSES_RAW1`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_CHOPHOME_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_PUPIL_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_PUPIL_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_DISTORTION_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_DISTORTION_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_DISTORTION_RAW`

  ```text
  KeyError: 'filter_name'
  ```

### `ESO\chophomeN.yaml`

**Top-level error:**

```text
AttributeError: 'NoneType' object has no attribute 'keys'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
    rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
  File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 35, in runSimulationBlock
    simulationSet.getStartDate()
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 165, in getStartDate
    recipe =  self.allrcps[list(self.allrcps.keys())[0]]
                                ^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'keys'
```

**Failing YAML entries:**

- `<file>`

  ```text
  Top-level YAML is not a mapping (got NoneType); runSimulationBlock expects a dict of named recipes. Outer error: AttributeError: 'NoneType' object has no attribute 'keys'
  Traceback (most recent call last):
    File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
      rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
    File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 35, in runSimulationBlock
      simulationSet.getStartDate()
    File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 165, in getStartDate
      recipe =  self.allrcps[list(self.allrcps.keys())[0]]
                                  ^^^^^^^^^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'keys'
  ```

### `ESO\flatLampLM.yaml`

**Top-level error:**

```text
KeyError: 'nObs'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
    rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
  File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 38, in runSimulationBlock
    simulationSet.runSimulations()
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 184, in runSimulations
    self._run(self.allrcps)
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 344, in _run
    nObs = recipe["properties"]["nObs"]
           ~~~~~~~~~~~~~~~~~~~~^^^^^^^^
KeyError: 'nObs'
```

**Failing YAML entries:**

- `WCU_FLAT_LM_RAW`

  ```text
  KeyError: 'nObs'
  ```

### `ESO\flatLampN.yaml`

**Top-level error:**

```text
KeyError: 'nObs'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
    rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
  File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 38, in runSimulationBlock
    simulationSet.runSimulations()
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 184, in runSimulations
    self._run(self.allrcps)
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 344, in _run
    nObs = recipe["properties"]["nObs"]
           ~~~~~~~~~~~~~~~~~~~~^^^^^^^^
KeyError: 'nObs'
```

**Failing YAML entries:**

- `WCU_FLAT_N_RAW`

  ```text
  KeyError: 'nObs'
  ```

### `ESO\ifu-rsrf.yaml`

**Top-level error:**

```text
KeyError: 'ndfilter_name'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
    rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
  File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 49, in runSimulationBlock
    simulationSet.calculateCalibs()
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 439, in calculateCalibs
    flatParms.append((props['filter_name'],props['ndfilter_name'],props['tech']))
                                           ~~~~~^^^^^^^^^^^^^^^^^
KeyError: 'ndfilter_name'
```

**Failing YAML entries:**

- `IFU_SKY_RAW1`

  ```text
  KeyError: 'ndfilter_name'
  ```

### `ESO\ifu.yaml`

**Top-level error:**

```text
KeyError: 'ndfilter_name'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
    rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
  File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 38, in runSimulationBlock
    simulationSet.runSimulations()
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 184, in runSimulations
    self._run(self.allrcps)
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 384, in _run
    recipeDark["properties"]["ndfilter_name"] = recipe["properties"]["ndfilter_name"]
                                               ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
KeyError: 'ndfilter_name'
```

**Failing YAML entries:**

- `DETLIN_IFU_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_DISTORTION_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_WAVE_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_SCI_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_SCI_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_STD_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_STD_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `IFU_SKY_RAW1`

  ```text
  KeyError: 'ndfilter_name'
  ```

### `ESO\imgLM.yaml`

**Top-level error:**

```text
KeyError: 'ndfilter_name'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
    rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
  File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 38, in runSimulationBlock
    simulationSet.runSimulations()
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 184, in runSimulations
    self._run(self.allrcps)
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 384, in _run
    recipeDark["properties"]["ndfilter_name"] = recipe["properties"]["ndfilter_name"]
                                               ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
KeyError: 'ndfilter_name'
```

**Failing YAML entries:**

- `DETLIN_2RG_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_DISTORTION_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_IMAGE_SCI_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_IMAGE_SCI_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_IMAGE_STD_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_IMAGE_STD_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

### `ESO\imgN.yaml`

**Top-level error:**

```text
KeyError: 'ndfilter_name'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
    rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
  File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 38, in runSimulationBlock
    simulationSet.runSimulations()
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 184, in runSimulations
    self._run(self.allrcps)
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 384, in _run
    recipeDark["properties"]["ndfilter_name"] = recipe["properties"]["ndfilter_name"]
                                               ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
KeyError: 'ndfilter_name'
```

**Failing YAML entries:**

- `DETLIN_GEO_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_DISTORTION_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_IMAGE_SCI_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_IMAGE_SCI_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_IMAGE_STD_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_IMAGE_STD_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

### `ESO\lssLM.yaml`

**Top-level error:**

```text
KeyError: 'ndfilter_name'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
    rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
  File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 38, in runSimulationBlock
    simulationSet.runSimulations()
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 184, in runSimulations
    self._run(self.allrcps)
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 384, in _run
    recipeDark["properties"]["ndfilter_name"] = recipe["properties"]["ndfilter_name"]
                                               ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
KeyError: 'ndfilter_name'
```

**Failing YAML entries:**

- `LM_LSS_RSRF_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_LSS_RSRF_PINH_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `DETLIN_2RG_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_LSS_WAVE_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_LSS_SCI_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_LSS_SCI_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_LSS_STD_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `LM_LSS_STD_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

### `ESO\lssN.yaml`

**Top-level error:**

```text
KeyError: 'ndfilter_name'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
    rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
  File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 38, in runSimulationBlock
    simulationSet.runSimulations()
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 184, in runSimulations
    self._run(self.allrcps)
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 384, in _run
    recipeDark["properties"]["ndfilter_name"] = recipe["properties"]["ndfilter_name"]
                                               ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
KeyError: 'ndfilter_name'
```

**Failing YAML entries:**

- `N_LSS_RSRF_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_LSS_RSRF_PINH_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `DETLIN_GEO_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_LSS_WAVE_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_LSS_SCI_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_LSS_SCI_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_LSS_STD_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `N_LSS_STD_SKY_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

### `ESO\metis_det_dark.yaml`

**Top-level error:**

```text
KeyError: 'ndfilter_name'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
    rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
  File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 49, in runSimulationBlock
    simulationSet.calculateCalibs()
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 439, in calculateCalibs
    flatParms.append((props['filter_name'],props['ndfilter_name'],props['tech']))
                                           ~~~~~^^^^^^^^^^^^^^^^^
KeyError: 'ndfilter_name'
```

**Failing YAML entries:**

- `DARK_LM_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `DARK_N_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

- `DARK_IFU_RAW`

  ```text
  KeyError: 'ndfilter_name'
  ```

### `ESO\wcuOffIFU.yaml`

**Top-level error:**

```text
KeyError: 'properties'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
    rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
  File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 38, in runSimulationBlock
    simulationSet.runSimulations()
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 184, in runSimulations
    self._run(self.allrcps)
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 338, in _run
    recipe["properties"]["dit"] = float(recipe["properties"]["dit"])
                                        ~~~~~~^^^^^^^^^^^^^^
KeyError: 'properties'
```

**Failing YAML entries:**

- `IFU_WCU_OFF_RAW`

  ```text
  KeyError: 'properties'
  ```

### `ESO\wcuOffLM.yaml`

**Top-level error:**

```text
KeyError: 'properties'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
    rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
  File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 38, in runSimulationBlock
    simulationSet.runSimulations()
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 184, in runSimulations
    self._run(self.allrcps)
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 338, in _run
    recipe["properties"]["dit"] = float(recipe["properties"]["dit"])
                                        ~~~~~~^^^^^^^^^^^^^^
KeyError: 'properties'
```

**Failing YAML entries:**

- `LM_WCU_OFF_RAW`

  ```text
  KeyError: 'properties'
  ```

### `ESO\wcuOffN.yaml`

**Top-level error:**

```text
KeyError: 'properties'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 103, in _try_run
    rs.runSimulationBlock([str(yaml_path)], params, ["-t"])
  File "D:\Repos\METIS_Simulations\metis_simulations\runSimulationBlock.py", line 38, in runSimulationBlock
    simulationSet.runSimulations()
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 184, in runSimulations
    self._run(self.allrcps)
  File "D:\Repos\METIS_Simulations\metis_simulations\setupSimulations.py", line 338, in _run
    recipe["properties"]["dit"] = float(recipe["properties"]["dit"])
                                        ~~~~~~^^^^^^^^^^^^^^
KeyError: 'properties'
```

**Failing YAML entries:**

- `N_WCU_OFF_RAW`

  ```text
  KeyError: 'properties'
  ```

## Passing files

- `ESO\chophomeLM.yaml`
- `ESO\hciAppLM.yaml`
- `ESO\hciRavcIfu.yaml`
- `ESO\hciRavcLM.yaml`
- `ESO\offAxisLM.yaml`
- `ESO\offAxisN.yaml`
- `ESO\pupilN.yaml`
- `ESO\scienceLM.yaml`
- `ESO\scienceLMLp.yaml`
- `ESO\scienceLSSLM.yaml`
- `ESO\scienceN.yaml`
- `ESO\stdLM.yaml`
- `ESO\stdLSSLM.yaml`
- `ESO\stdN.yaml`
