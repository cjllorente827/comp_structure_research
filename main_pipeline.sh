#######################################################
# Main Analysis Pipeline Script
#
# This script controls the analysis flow from the top
# by managing arguments/input and passing necessary
# information down to the specific analysis scripts
# in their respective directories. 
#######################################################

source $1

#######################################################
# Module settings
#######################################################
module purge
module load GNU/6.4.0-2.28
module load OpenMPI/2.1.2
module load HDF5/1.10.1

#######################################################
# Function definitions
#######################################################

function prep_rockstar {
 echo nothing
}

function run_rockstar {
    [ ! -d rockstar_halos ] && mkdir rockstar_halos
    [ -f rockstar_halos/auto-rockstar.cfg ] && rm -v rockstar_halos/auto-rockstar.cfg
    if [ -f rockstar_halos/restart.cfg ]; then
	cfg=rockstar_halos/restart.cfg
	for i in `seq 0 100`; do
	    newc=`echo $i | gawk '{printf "client%3.3d.out", $1}'`
	    news=`echo $i | gawk '{printf "server%3.3d.out", $1}'`
	    if [ ! -f $newc ]; then
		cp -v client.out $newc
		cp -v server.out $news
		break
	    fi
	done
    else
	cfg=rockstar.cfg
	[ -f client.out ] && rm -v client*.out
	[ -f server.out ] && rm -v server*.out
    fi

    #TODO: Something to look into here
    #  This script creates a rockstar server in the background and then a number of client rockstar
    #  processes equal to the number of tasks given to the slurm script. This could cause an issue
    #  if the server process is competing with one (or more) of the client processes for processor
    #  time. Check to see if this is the case and modify the script if it is
    
    ./rockstar-galaxies -c $cfg >& server.out&
    while [ ! -e rockstar_halos/auto-rockstar.cfg ]; do
	sleep 1
    done
    mpirun --mca btl ^tcp --oversubscribe -n $NPROCS ./rockstar-galaxies -c rockstar_halos/auto-rockstar.cfg >& client.out

}

# Ensure directories exist
[ ! -d ${DATA_DIR} ] && mkdir ${DATA_DIR}
[ ! -d ${PLOT_DIR} ] && mkdir ${PLOT_DIR}

if [ "${START_FROM_STAGE}" -lt 1 ]
then
    cd ${DATA_DIR}
    python ${HOME}/comp_structure_research/src/prep_rockstar.py

    [ ${RUN_TO_END} -eq 0 ] && exit 0
fi

if [ "${START_FROM_STAGE}" -lt 2 ]
then
    echo 'run_rockstar()'

    [ ${RUN_TO_END} -eq 0 ] && exit 0
fi

if [ "${START_FROM_STAGE}" -lt 3 ]
then
    echo 'extract_halo_data()'

    [ ${RUN_TO_END} -eq 0 ] && exit 0
fi

if [ "${START_FROM_STAGE}" -lt 4 ]
then
    echo 'run_analysis()'

    [ ${RUN_TO_END} -eq 0 ] && exit 0
fi

if [ "${START_FROM_STAGE}" -lt 5 ]
then
    echo 'make_plots()'

    [ ${RUN_TO_END} -eq 0 ] && exit 0
fi



# MPI_ARGS=--mca orte_base_help_aggregate 0 

# mpirun -np ${NPROCS} ${MPI_ARGS} python ${SQUIRREL} ${ENZO_DATASET} ${HALO_DATASET} ${OUTPUT_DIR}

