#!/usr/bin/env python
"""
Parse AIT Performance Test Sequence CSV files into YAML-equivalent
recipe dictionaries for the METIS simulation pipeline.

Reads CSV files in the METIS AIT test sequence format (45 columns,
4 header rows, data from row 5) and produces a dict identical in
structure to yaml.safe_load() output from the existing YAML input files.

Only parameters that are usable in ScopeSim are mapped. See the
"Mapping ICS METIS component names to ScopeSim parameters" google spreadsheet
for the full mapping reference.
"""

import csv
import logging
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)

# DPR.TECH from CSV → DPR.TECH in YAML (comma-separated ESO convention)
TECH_MAP = {
    "IMAGE_LM": "IMAGE,LM",
    "IMAGE_N":  "IMAGE,N",
    "IFU":      "IFU",
    "LSS_LM":   "LSS,LM",
    "LSS_N":    "LSS,N",
    "UNKNOWN":  "IMAGE,LM",  # fallback for darks with unknown tech
}

TYPE_MAP = {
    "DARK":           "DARK",
    "DARK_WCUOFF":    "DARK,WCUOFF",
    "OBJECT":         "OBJECT",
    "FLAT_LAMP":      "FLAT,LAMP",
    "FLAT_TWILIGHT":  "FLAT,TWILIGHT",
    "STD":            "STD",
    "SKY":            "SKY",
    "DETLIN":         "DETLIN",
    "DISTORTION":     "DISTORTION",
    "WAVE":           "WAVE",
    "SLITLOSS":       "SLITLOSS",
    "CHOPHOME":       "CHOPHOME",
    "PUPIL":          "PUPIL",
    "PSF_OFFAXIS":    "PSF,OFFAXIS",
}

FILTER_MAP_LM = {
    "L'":           "Lp",
    "M'":           "Mp",
    "H2Oice":       "H2O-ice",
    "shortL":       "short-L",
    "IB4.05":       "IB_4.05",
    "PAH3.3":       "PAH_3.3",
    "PAH3.3ref":    "PAH_3.3_ref",
    "Br_alpha":     "Br_alpha",
    "Br-alpha":     "Br_alpha",
    "Br_alpharef":  "Br_alpha_ref",
    "Br-alpharef":  "Br_alpha_ref",
    "CO(1-0)/ice":  "CO_1-0_ice",
    "COref":        "CO_ref",
    "HCIL-short":   "HCI_L_short",
    "HCIL-long":    "HCI_L_long",
    # Broadband positions: full_L/full_M don't yet exist in ScopeSim.
    # Lp and Mp are the closest broadband filters.
    "full_L":       "Lp",
    "full_M":       "Mp",
    "OPEN":         "open",
    "DARK":         "closed",
    "DARK-LM":      "closed",
}

FILTER_MAP_N = {
    "N1":             "N1",
    "N2":             "N2",
    "N3":             "N3",
    "PAH8.6":         "PAH_8.6",
    "PAH8.6_ref":     "PAH_8.6_ref",
    "PAH11.25":       "PAH_11.25",
    "PAH11.25_ref":   "PAH_11.25_ref",
    "[NeII]":         "Ne_II",
    "[NeII]_ref":     "Ne_II_ref",
    "[SIV]":          "S_IV",
    "[SIV]_ref":      "S_IV_ref",
    # full_N doesn't exist in ScopeSim; 'open' gives the full N-band passband
    "full_N":         "open",
    "OPEN":           "open",
    "DARK":           "closed",
    "DARK-N":         "closed",
}

ND_MAP = {
    "OPEN":  "open",
    "ND1":   "ND_OD1",
    "ND2":   "ND_OD2",
    "ND3":   "ND_OD3",
    "ND4":   "ND_OD4",
    "ND5":   "ND_OD5",
    "DARK":  "closed",
}

BB_APERTURE_MAP = {
    "CLOSED": 0.0,
    "MASK01": 0.0625,
    "MASK02": 0.125,
    "MASK03": 0.1875,
    "MASK04": 0.25,
    "MASK05": 0.3125,
    "MASK06": 0.375,
    "MASK07": 0.4375,
    "MASK08": 0.5,
    "MASK09": 0.5625,
    "MASK10": 0.625,
    "MASK11": 0.6875,
    "MASK12": 0.75,
    "MASK13": 0.8125,
    "MASK14": 0.875,
    "OPEN":   1.0,
}

FPMASK_MAP = {
    "FLATFIELD":       "open",
    "LM-GRID":         "grid_lm",
    "N-GRID":          "grid_n",
    "LMS-GRID":        "grid_lms",
    "LM-PINHOLE":      "pinhole_lm",
    "N-PINHOLE":       "pinhole_n",
    "ALIGNMENT-MASK":  "open", 
}

SLIT_MAP = {
    "SLIT-A":      "A-19_0",
    "SLIT-B":      "B-28_6",
    "SLIT-C":      "C-38_1",
    "SLIT-D":      "D-57_2",
    "SLIT-E":      "E-114_3",
}

DET_MAP = {
    "IMAGE_LM": ("DET1.DIT", "DET1.NDIT", "SEQ.NEXPO1"),
    "IMAGE_N":  ("DET2.DIT", "DET2.NDIT", "SEQ.NEXPO2"),
    "IFU":      ("DET3.DIT", "DET3.NDIT", "SEQ.NEXPO3"),
    "LSS_LM":   ("DET1.DIT", "DET1.NDIT", "SEQ.NEXPO1"),
    "LSS_N":    ("DET2.DIT", "DET2.NDIT", "SEQ.NEXPO2"),
}

DO_CATG_MAP = {
    ("IMAGE,LM", "DARK"):          "DARK_2RG_RAW",
    ("IMAGE,LM", "OBJECT"):        "LM_IMAGE_SCI_RAW",
    ("IMAGE,LM", "STD"):           "LM_IMAGE_STD_RAW",
    ("IMAGE,LM", "DARK,WCUOFF"):   "LM_WCU_OFF_RAW",
    ("IMAGE,LM", "FLAT,LAMP"):     "LM_FLAT_LAMP_RAW",
    ("IMAGE,LM", "FLAT,TWILIGHT"): "LM_FLAT_TWILIGHT_RAW",
    ("IMAGE,LM", "DETLIN"):        "DETLIN_2RG_RAW",
    ("IMAGE,LM", "DISTORTION"):    "LM_DISTORTION_RAW",
    ("IMAGE,LM", "CHOPHOME"):      "LM_CHOPPERHOME_RAW",
    ("IMAGE,LM", "SLITLOSS"):      "LM_SLITLOSSES_RAW",
    ("IMAGE,LM", "PUPIL"):         "LM_PUPIL_RAW",
    ("IMAGE,N", "DARK"):            "DARK_GEO_RAW",
    ("IMAGE,N", "OBJECT"):          "N_IMAGE_SCI_RAW",
    ("IMAGE,N", "STD"):             "N_IMAGE_STD_RAW",
    ("IMAGE,N", "DARK,WCUOFF"):     "N_WCU_OFF_RAW",
    ("IMAGE,N", "FLAT,LAMP"):       "N_FLAT_LAMP_RAW",
    ("IMAGE,N", "FLAT,TWILIGHT"):   "N_FLAT_TWILIGHT_RAW",
    ("IMAGE,N", "DETLIN"):          "DETLIN_GEO_RAW",
    ("IMAGE,N", "DISTORTION"):      "N_DISTORTION_RAW",
    ("IMAGE,N", "PUPIL"):           "N_PUPIL_RAW",
    # LSS LM
    ("LSS,LM", "DARK"):             "DARK_2RG_RAW",
    ("LSS,LM", "OBJECT"):           "LM_LSS_SCI_RAW",
    ("LSS,LM", "STD"):              "LM_LSS_STD_RAW",
    ("LSS,LM", "DARK,WCUOFF"):      "LM_WCU_OFF_RAW",
    ("LSS,LM", "WAVE"):             "LM_LSS_WAVE_RAW",
    ("LSS,LM", "RSRF"):             "LM_LSS_RSRF_RAW",
    # LSS N
    ("LSS,N", "DARK"):              "DARK_GEO_RAW",
    ("LSS,N", "OBJECT"):            "N_LSS_SCI_RAW",
    ("LSS,N", "STD"):               "N_LSS_STD_RAW",
    ("LSS,N", "DARK,WCUOFF"):       "N_WCU_OFF_RAW",
    ("LSS,N", "RSRF"):              "N_LSS_RSRF_RAW",
    # IFU (LMS)
    ("IFU", "DARK"):                "DARK_IFU_RAW",
    ("IFU", "OBJECT"):              "IFU_SCI_RAW",
    ("IFU", "STD"):                 "IFU_STD_RAW",
    ("IFU", "DARK,WCUOFF"):         "IFU_WCU_OFF_RAW",
    ("IFU", "WAVE"):                "IFU_WAVE_RAW",
    ("IFU", "DISTORTION"):          "IFU_DISTORTION_RAW",
    ("IFU", "RSRF"):                "IFU_RSRF_RAW",
}


def _clean_value(val):
    """Convert NULL/empty to None, strip whitespace"""
    if val is None:
        return None
    val = val.strip()
    if val == "" or val.upper() == "NULL":
        return None
    return val


def _parse_tech_list(tech_string):
    """Parse DPR.TECH which may be a single value or a bracketed list"""
    if tech_string is None:
        return []
    s = tech_string.strip()
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]
    return [t.strip() for t in s.split(",") if t.strip()]


def _determine_mode(tech, row):
    """Derive ScopeSim mode from CSV tech + instrument state"""
    wcu_active = (row.get("INS.OPTI17.NAME") == "IN")
    prefix = "wcu_" if wcu_active else ""

    if tech == "IMAGE_LM":
        return prefix + "img_lm"
    if tech == "IMAGE_N":
        return prefix + "img_n"
    if tech == "IFU":
        return prefix + "lms"
    if tech == "LSS_LM":
        grism = row.get("INS.OPTI9.NAME")
        if grism == "GRISM-M":
            return prefix + "lss_m"
        return prefix + "lss_l"
    if tech == "LSS_N":
        return prefix + "lss_n"
    if tech == "UNKNOWN":
        if row.get("DET1.DIT") is not None:
            return prefix + "img_lm"
        if row.get("DET2.DIT") is not None:
            return prefix + "img_n"
        if row.get("DET3.DIT") is not None:
            return prefix + "lms"
    raise ValueError(f"Cannot determine mode for tech={tech}")


def _map_filter(mode, row):
    """
    Map the filter name for a given mode from CSV columns.

    For LSS modes, ScopeSim only accepts L_spec/M_spec/N_spec per the
    validFilters configuration in simulationDefinitions.py. The imaging
    filter wheel value from the CSV is NOT used for LSS modes.

    NOTE: If ScopeSim adds support for imaging filters in LSS modes in
    the future, update this function to map INS.OPTI10/13.NAME through
    the filter mapping tables instead of forcing the _spec filters.
    """
    base_mode = mode.replace("wcu_", "")

    if base_mode == "lss_l":
        return "L_spec"
    if base_mode == "lss_m":
        return "M_spec"
    if base_mode == "lss_n":
        return "N_spec"
    if base_mode == "lms":
        return "open"
    if base_mode == "img_lm":
        ics_name = row.get("INS.OPTI10.NAME")
        if ics_name is None:
            return "open"
        mapped = FILTER_MAP_LM.get(ics_name)
        if mapped is None:
            logger.warning("Unmapped LM filter '%s', passing through", ics_name)
            return ics_name
        return mapped
    if base_mode == "img_n":
        ics_name = row.get("INS.OPTI13.NAME")
        if ics_name is None:
            return "open"
        mapped = FILTER_MAP_N.get(ics_name)
        if mapped is None:
            logger.warning("Unmapped N filter '%s', passing through", ics_name)
            return ics_name
        return mapped

    return "open"


def _map_nd_filter(mode, row):
    """Map ND filter from CSV. Returns (nd_filter_name, is_dark_override)"""
    base_mode = mode.replace("wcu_", "")

    if base_mode in ("img_lm", "lss_l", "lss_m"):
        ics_name = row.get("INS.OPTI11.NAME")
    elif base_mode in ("img_n", "lss_n"):
        ics_name = row.get("INS.OPTI14.NAME")
    else:
        return "open", False

    if ics_name is None:
        return "open", False

    mapped = ND_MAP.get(ics_name, "open")
    is_dark = (ics_name == "DARK")
    return mapped, is_dark


def _map_slit(row):
    """Map CFO FP2 slit wheel to ScopeSim slit name, None if no slit"""
    fp2 = row.get("INS.OPTI3.NAME")
    if fp2 is None:
        return None
    return SLIT_MAP.get(fp2)


def _build_wcu(row):
    """Build WCU config dict if WCU periscopic arm is IN, else None"""
    if row.get("INS.OPTI17.NAME") != "IN":
        return None

    aperture_name = row.get("INS.OPTI19.NAME")
    bb_aperture = BB_APERTURE_MAP.get(aperture_name, 0.0) if aperture_name else 0.0

    fpmask_name = row.get("INS.OPTI20.NAME")
    current_fpmask = FPMASK_MAP.get(fpmask_name, "open") if fpmask_name else "open"

    bb_temp_str = row.get("SEQ.WCU_BB_TEMP")
    if bb_temp_str is not None and bb_temp_str != "0":
        try:
            bb_temp = int(float(bb_temp_str))
        except (ValueError, TypeError):
            bb_temp = 300
    else:
        bb_temp = 300

    return {
        "current_lamp": "bb",
        "current_fpmask": current_fpmask,
        "bb_aperture": bb_aperture,
        "bb_temp": bb_temp,
        "is_temp": 300,
        "wcu_temp": 300,
    }


def _build_do_catg(tech_dpr, type_dpr):
    """Look up do.catg from DRLD Table 6, falls back to generic construction"""
    key = (tech_dpr, type_dpr)
    if key in DO_CATG_MAP:
        return DO_CATG_MAP[key]

    # Fallback: construct from components
    band_map = {
        "IMAGE,LM": "LM", "IMAGE,N": "N", "IFU": "IFU",
        "LSS,LM": "LM_LSS", "LSS,N": "N_LSS",
    }
    band = band_map.get(tech_dpr, tech_dpr.replace(",", "_"))
    type_clean = type_dpr.replace(",", "_")
    fallback = f"{band}_{type_clean}_RAW"
    logger.warning("No DRLD do.catg for (%s, %s), using fallback: %s",
                   tech_dpr, type_dpr, fallback)
    return fallback


def _map_type(type_str):
    """Map CSV DPR.TYPE to YAML convention (underscore → comma)"""
    if type_str is None:
        return "OBJECT"
    # If it already has commas, pass through
    if "," in type_str:
        return type_str
    return TYPE_MAP.get(type_str, type_str)


def _map_tech(tech):
    """Map a single CSV tech string to DPR.TECH YAML convention"""
    return TECH_MAP.get(tech, tech)


def _get_detector_params(tech, row):
    """Get (dit, ndit, nObs) for the detector corresponding to this tech"""
    det_keys = DET_MAP.get(tech)
    if det_keys is None:
        return None

    dit_key, ndit_key, nexpo_key = det_keys
    dit_str = row.get(dit_key)
    ndit_str = row.get(ndit_key)

    if dit_str is None:
        return None

    try:
        dit = float(dit_str)
    except (ValueError, TypeError):
        return None

    try:
        ndit = int(float(ndit_str)) if ndit_str is not None else 1
    except (ValueError, TypeError):
        ndit = 1

    nexpo_str = row.get(nexpo_key)
    try:
        nObs = int(float(nexpo_str)) if nexpo_str is not None else 1
    except (ValueError, TypeError):
        nObs = 1

    return dit, ndit, nObs


def loadCSV(filepath, write_yaml=False):
    """
    Parse an AIT Performance Test Sequence CSV file into a dict of recipe
    blocks compatible with the YAML input format used by setupSimulations.

    If write_yaml is True, also writes the parsed recipes to a .yaml file
    next to the CSV for inspection.
    """
    filepath = Path(filepath)
    allrcps = {}

    with filepath.open(encoding="utf-8") as f:
        reader = csv.reader(f)

        column_ids = next(reader)
        _components = next(reader)
        _descriptions = next(reader)
        _data_types = next(reader)

        column_ids = [c.strip() for c in column_ids]

        for raw_row in reader:
            row = {}
            for i, col_id in enumerate(column_ids):
                val = raw_row[i] if i < len(raw_row) else None
                row[col_id] = _clean_value(val)

            test_id = row.get("test_ID")
            step = row.get("step_number")
            template_name = row.get("templateName")

            tech_str = row.get("DPR.TECH")
            if tech_str is None:
                logger.info("Skipping row %s/%s: no DPR.TECH", test_id, step)
                continue

            techs = _parse_tech_list(tech_str)

            for tech in techs:
                det_params = _get_detector_params(tech, row)
                if det_params is None:
                    # For UNKNOWN tech, try all detectors
                    if tech == "UNKNOWN":
                        for fallback_tech in ["IMAGE_LM", "IMAGE_N", "IFU"]:
                            det_params = _get_detector_params(fallback_tech, row)
                            if det_params is not None:
                                tech = fallback_tech
                                break
                    if det_params is None:
                        logger.info("Skipping %s/%s tech=%s: no detector data",
                                    test_id, step, tech)
                        continue

                dit, ndit, nObs = det_params

                try:
                    mode = _determine_mode(tech, row)
                except ValueError as e:
                    logger.warning("Skipping %s/%s: %s", test_id, step, e)
                    continue

                tech_dpr = _map_tech(tech)
                type_dpr = _map_type(row.get("DPR.TYPE"))
                catg = row.get("DPR.CATG", "CALIB")

                filter_name = _map_filter(mode, row)

                # ND filter (may override filter_name for darks)
                nd_filter_name, is_nd_dark = _map_nd_filter(mode, row)
                if is_nd_dark:
                    filter_name = "closed"

                do_catg = _build_do_catg(tech_dpr, type_dpr)

                # Properties
                properties = {
                    "dit": dit,
                    "ndit": ndit,
                    "filter_name": filter_name,
                    "nd_filter_name": nd_filter_name if not is_nd_dark else "open",
                    "catg": catg,
                    "tech": tech_dpr,
                    "type": type_dpr,
                    "nObs": nObs,
                    "tplname": template_name if template_name else "",
                }

                slit = _map_slit(row)
                if slit is not None:
                    properties["slit"] = slit

                # Source — always empty_sky for AIT test sequences
                source = {"name": "empty_sky", "kwargs": {}}

                # WCU
                wcu = _build_wcu(row)

                # Block name
                tech_suffix = tech.replace(",", "_")
                block_name = f"{test_id}_{step}_{tech_suffix}"

                # Handle duplicate block names
                if block_name in allrcps:
                    counter = 2
                    while f"{block_name}_{counter}" in allrcps:
                        counter += 1
                    block_name = f"{block_name}_{counter}"

                allrcps[block_name] = {
                    "do.catg": do_catg,
                    "mode": mode,
                    "source": source,
                    "properties": properties,
                    "wcu": wcu,
                }

    logger.info("Loaded %d recipe blocks from %s", len(allrcps), filepath)
    print(f"Loaded {len(allrcps)} recipe blocks from CSV: {filepath}")

    if write_yaml:
        yaml_path = filepath.with_suffix(".yaml")
        with yaml_path.open("w", encoding="utf-8") as yf:
            yaml.dump(allrcps, yf, default_flow_style=False, sort_keys=False)
        print(f"YAML written to: {yaml_path}")

    return allrcps
