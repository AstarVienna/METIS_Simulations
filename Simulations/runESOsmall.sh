#!/bin/bash

cat YAML/persist.yaml > YAML/allRecipes.yaml
cat YAML/imgLM.yaml >> YAML/allRecipes.yaml
cat YAML/imgN.yaml >> YAML/allRecipes.yaml
cat YAML/lssLM.yaml >> YAML/allRecipes.yaml
cat YAML/lssN.yaml >> YAML/allRecipes.yaml
cat YAML/ifu.yaml >> YAML/allRecipes.yaml
cat YAML/hci.yaml >> YAML/allRecipes.yaml
cat YAML/calib.yaml >> YAML/allRecipes.yaml

python/run_recipes.py --inputYAML=YAML/allRecipes.yaml --outputDir outputSmall/ --doCalib=1 --sequence=1 --doStatic --nCores=8 --small

