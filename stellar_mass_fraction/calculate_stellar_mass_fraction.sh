#!/bin/bash

##########################################
# STEP 0
# Decide how much work we need to do
# MODE=1 #Create halo catalog, extract data from catalog, make plots
MODE=2 #Skip the halo catalog creation
#MODE=3 #Skip the halo catalog creation and data extraction (plots only)

# Parallel process settings
NPROCS=4

# File I/O settings
INFILE="$HOME/FOGGIE_analysis/FOGGIE_data/RD0036/RD0036"
OUTFILE="stellar_mass_fraction_z0.3.dat"

##########################################

##########################################
# STEP 1
# First extract the halo catalog from the
# FOGGIE dataset
##########################################
if [ $MODE -lt 2 ]
then
   if [ -d "halo_catalogs" ] 
   then
       rm -r halo_catalogs
   fi

   if [ -d "rockstar_halos" ] 
   then
       rm -r rockstar_halos
   fi

   mpirun -n ${NPROCS} python ../run_rockstar.py $INFILE
fi
##########################################
# STEP 2
# Load the catalog and generate a txt file
# with the relevant data. 
##########################################
if [ $MODE -lt 3 ]
then
   python calculate_stellar_mass_fraction.py $INFILE $OUTFILE
fi
##########################################
# STEP 3
# Plots
##########################################
python plots.py $OUTFILE
