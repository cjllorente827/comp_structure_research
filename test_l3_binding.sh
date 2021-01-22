#!/bin/bash -login

#####################################################
# See how l3 cache binding works on the AMD nodes
#####################################################


#SBATCH -A galaxies
#SBATCH --time=00:10:00             
#SBATCH --nodes=1                 
#SBATCH --ntasks=128 
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=10G            
#SBATCH --job-name cache-binding-test

for n in 1 2 4 8 16 32 64 
do
    
    #TODO: See if this works the same way with srun
    mpirun -n ${n} -map-by l3cache --bind-to core --report-bindings echo "..." > binding_${n}_procs.out 2>&1
done
