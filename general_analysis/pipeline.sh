#!/bin/bash 

#####################################################
# Main pipeline script for general analysis
#
# Arguments
# {1} - Parameter file that sets values required for
#       the script to run
#####################################################


#SBATCH -A galaxies
#SBATCH --time=00:30:00             
#SBATCH --nodes=1                 
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=10G            
#SBATCH --job-name gen-analysis-pipeline

export PATH=/mnt/home/llorente/yt-conda/bin:$PATH


MPI_ARGS="--mca orte_base_help_aggregate 0"

# Read in the parameter file (a shell script that just sets values)
source ${1}


srun -n ${NPROC} python ${SQUIRREL} ${ENZO_DATASET} ${HALO_DATASET} -o ${OUTPUT_DIR} > pipeline.out 2>&1

echo "Output directory currently using:" >> pipeline.out
du -h ${OUTPUT_DIR} >> pipeline.out
