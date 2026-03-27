
temp=$METIS_ODIR
echo "$temp"
export METIS_ODIR="Small/"

python simulationBlocks/imgLM.py --small
python simulationBlocks/imgN.py --small
python simulationBlocks/lssLM.py --small
python simulationBlocks/lssN.py --small
python simulationBlocks/ifu.py --small
python simulationBlocks/calib.py --small
python simulationBlocks/hciRavcLM.py --small
python simulationBlocks/hciAppLm.py --small
python simulationBlocks/hciRavcIfu.py --small

export METIS_ODIR="Temp/"

