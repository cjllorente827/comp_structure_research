
#######################################################
# Pipeline settings
#######################################################

# Stage descriptions:
# 0 : Preps rockstar to be run by creating necessary config files
# 1 : Runs rockstar on an Enzo dataset to generate halo catalogs
# 2 : Extracts useful halo data from halo catalogs and
#     creates a pickle of the resultant object.
# 3 : Runs a specific analysis script in order to create
#     plot-ready data
# 4 : Runs the plot creation script and saves the images
export START_FROM_STAGE=0

# if set to anything but zero, will run from the stage specified by START_FROM_STAGE
# until the end of the pipeline
# if set to 0, will only execute the stage specified by START_FROM_STAGE
export RUN_TO_END=0



#######################################################
# Parallel processing settings
#######################################################
# TODO: Figure out a way to make this play nice with slurm
export NPROCS=16


#######################################################
# Directory settings
#######################################################
export HOME=/mnt/home/llorente # for convenience
export DATA_DIR=${HOME}/comp_structure_research/bigbox_50Mpc/data
export PLOT_DIR=${HOME}/comp_structure_research/bigbox_50Mpc/plots
export ENZO_DIR=${HOME}/cosmo_bigbox/50Mpc_512

#######################################################
# Filename settings
#######################################################
export ENZO_DATA_FNAME=${ENZO_DIR}/RD0135/RD0135 
export HALO_DATA_FNAME=${HOME}/comp_structure_research/bigbox_50Mpc/data/halodata_RD0265.pkl
