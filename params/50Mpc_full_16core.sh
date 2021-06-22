
#######################################################
# Pipeline settings
#######################################################

# APL = Analysis Pipe Line, prefix all env variables so as not to pollute namespace
#       and also have an easy way to grep for the settings in case of issues        

# Stage descriptions:
# 0 : Preps rockstar to be run by creating necessary config files
# 1 : Runs rockstar on an Enzo dataset to generate halo catalogs
# 2 : Extracts useful halo data from halo catalogs and
#     creates a pickle of the resultant object.
# 3 : Runs a specific analysis script in order to create
#     plot-ready data
# 4 : Runs the plot creation script and saves the images
export APL_START_FROM_STAGE=0

# if set to anything but zero, will run from the stage specified by START_FROM_STAGE
# until the end of the pipeline
# if set to 0, will only execute the stage specified by START_FROM_STAGE
export APL_RUN_TO_END=0



#######################################################
# Parallel processing settings
#######################################################
# TODO: Figure out a way to make this play nice with slurm
export APL_NUM_PROCS=16


#######################################################
# Directory settings
#######################################################
export HOME=/mnt/home/llorente # for convenience
export APL_DATA_DIR=${HOME}/comp_structure_research/bigbox_50Mpc/data
export APL_PLOT_DIR=${HOME}/comp_structure_research/bigbox_50Mpc/plots
export APL_ENZO_DIR=${HOME}/cosmo_bigbox/50Mpc_512

#######################################################
# Filename settings
#######################################################
export APL_ENZO_DATA_FNAME=${APL_ENZO_DIR}/RD0135/RD0135 
export APL_HALO_DATA_FNAME=${HOME}/comp_structure_research/bigbox_50Mpc/data/halodata_RD0265.pkl
