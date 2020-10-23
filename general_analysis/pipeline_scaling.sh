#####################################################
# Scaling test for general analysis pipeline
#####################################################

#!/bin/bash 

#SBATCH -A galaxies
#SBATCH --time=10:00:00             
#SBATCH --nodes=1                 
#SBATCH --ntasks=64                  
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=10G            
#SBATCH --job-name pipeline-scaling-test

NPROCS={1,2,4,8,16,32,64}

HOME="/mnt/home/llorente"

SQUIRREL="${HOME}/comp_structure_research/general_analysis/src/squirrel.py"
ENZO_DATASET="${HOME}/cosmo_bigbox/25Mpc_512/RD0265/RD0265"
HALO_DATASET="${HOME}/comp_structure_research/bigbox_25Mpc/data/halodata_RD0265.pkl"
OUTPUT_DIR="${HOME}/comp_structure_research/bigbox_25Mpc/data"


for n in NPROCS
do
    
    srun -np ${n} python ${SQUIRREL} ${ENZO_DATASET} ${HALO_DATASET} -o ${OUTPUT_DIR} > pipeline_${n}_procs.out
done


