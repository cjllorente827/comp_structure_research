#!/bin/bash -login

#####################################################
# Scaling test for general analysis pipeline
#####################################################


#SBATCH -A galaxies
#SBATCH --time=3:30:00             
#SBATCH --nodes=1                 
#SBATCH --ntasks=128 
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=10G            
#SBATCH --job-name pipeline-scaling-test

# Read in the parameter file (a shell script that just sets values)
source ${1}

for n in 1 2 4 8 16 32 64 
do
    
    #srun -n ${n} python ${SQUIRREL} ${ENZO_DATASET} ${HALO_DATASET} -o ${OUTPUT_DIR} > pipeline_${n}_procs.out 2>&1

    #TODO: See if this works the same way with srun
    mpirun -n ${n} -map-by l3cache --bind-to core python ${SQUIRREL} ${ENZO_DATASET} ${HALO_DATASET} -o ${OUTPUT_DIR} > pipeline_${n}_procs.out 2>&1
done

