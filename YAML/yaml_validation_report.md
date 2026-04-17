# YAML validation report

- YAML root: `D:\Repos\METIS_Simulations\YAML`
- Files scanned: **81**
- PyYAML parse failures: **2**
- runSimulationBlock acceptance failures: **15**
- Passed: **64**

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

## runSimulationBlock acceptance failures

### `ESO\allRecipes.yaml`

**Top-level error:**

```text
KeyError: 'ndfilter_name'
Traceback (most recent call last):
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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
    File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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
  File "D:\Repos\METIS_Simulations\YAML\validate_yamls.py", line 97, in _try_run
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

- `AIT_Tests\LMS_OPT_01\LMS_OPT_1.yaml`
- `AIT_Tests\LMS_OPT_02\LMS_OPT_2.yaml`
- `AIT_Tests\LMS_RAD_01\LMS_RAD_01.yaml`
- `AIT_Tests\LMS_RAD_06\LMS_RAD_06.yaml`
- `AIT_Tests\LMS_RAD_06\LMS_RAD_06_1.yaml`
- `AIT_Tests\LMS_RAD_06\LMS_RAD_06_2.yaml`
- `AIT_Tests\LMS_RAD_06\LMS_RAD_06_3.yaml`
- `AIT_Tests\LMS_RAD_06\LMS_RAD_06_4.yaml`
- `AIT_Tests\LMS_RAD_06\LMS_RAD_06_5.yaml`
- `AIT_Tests\LMS_RAD_06\LMS_RAD_06_6.yaml`
- `AIT_Tests\LMS_RAD_10\LMS_RAD_10.yaml`
- `AIT_Tests\LSS_RAD_03\LSS_RAD_03_lm.yaml`
- `AIT_Tests\LSS_RAD_03\LSS_RAD_03_n.yaml`
- `AIT_Tests\LSS_RAD_04\LSS_RAD_04_lm.yaml`
- `AIT_Tests\LSS_RAD_04\LSS_RAD_04_n.yaml`
- `AIT_Tests\LSS_RAD_12\LSS_RAD_12_lm.yaml`
- `AIT_Tests\LSS_RAD_12\LSS_RAD_12_n.yaml`
- `ESO\chophomeLM.yaml`
- `ESO\darkIFU.yaml`
- `ESO\darkLM.yaml`
- `ESO\darkN.yaml`
- `ESO\detlinIFU.yaml`
- `ESO\detlinLM.yaml`
- `ESO\detlinN.yaml`
- `ESO\distortionIFU.yaml`
- `ESO\distortionLM.yaml`
- `ESO\distortionN.yaml`
- `ESO\flatLampLMLp.yaml`
- `ESO\flatTwilightLMLp.yaml`
- `ESO\hciAppLM.yaml`
- `ESO\hciRavcIfu.yaml`
- `ESO\hciRavcLM.yaml`
- `ESO\offAxisIFU.yaml`
- `ESO\offAxisLM.yaml`
- `ESO\offAxisN.yaml`
- `ESO\persistIfu.yaml`
- `ESO\persistLM.yaml`
- `ESO\persistN.yaml`
- `ESO\pupilLM.yaml`
- `ESO\pupilN.yaml`
- `ESO\rsrfIFU.yaml`
- `ESO\rsrfLSS.yaml`
- `ESO\rsrfLSSLM.yaml`
- `ESO\rsrfLSSN.yaml`
- `ESO\rsrfPinhIFU.yaml`
- `ESO\rsrfPinhLSSLM.yaml`
- `ESO\rsrfPinhLSSN.yaml`
- `ESO\scienceIFU.yaml`
- `ESO\scienceLM.yaml`
- `ESO\scienceLMLp.yaml`
- `ESO\scienceLSSLM.yaml`
- `ESO\scienceLSSN.yaml`
- `ESO\scienceN.yaml`
- `ESO\slitlossLSSLM.yaml`
- `ESO\slitlossLSSN.yaml`
- `ESO\stdIFU.yaml`
- `ESO\stdLM.yaml`
- `ESO\stdLSSLM.yaml`
- `ESO\stdLSSN.yaml`
- `ESO\stdN.yaml`
- `ESO\testYAML.yaml`
- `ESO\wavecalIFU.yaml`
- `ESO\wavecalLSSLM.yaml`
- `ESO\wavecalLSSN.yaml`
