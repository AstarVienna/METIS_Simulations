#!/bin/bash

cat YAML/persist.yaml > YAML/allRecipes.yaml
cat YAML/wcu.yaml >> YAML/allRecipes.yaml
cat YAML/img.yaml >> YAML/allRecipes.yaml
cat YAML/lss.yaml >> YAML/allRecipes.yaml
cat YAML/ifu.yaml >> YAML/allRecipes.yaml
cat YAML/hci.yaml >> YAML/allRecipes.yaml

python/run_recipes.py --inputYAML=YAML/allRecipes.yaml --outputDir outputSmall/ --doCalib=1 --sequence=1 --doStatic --small 

