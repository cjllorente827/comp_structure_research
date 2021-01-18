
NPROCS=2

MPI_ARGS=--mca orte_base_help_aggregate 0 

SQUIRREL=parallel_halo_inspection_proto.py

HOME=/mnt/home/llorente
ENZO_DATASET=${HOME}/cosmo_bigbox/25Mpc_512/RD0265/RD0265
HALO_DATASET=${HOME}/comp_structure_research/bigbox_25Mpc/data/halodata_RD0265.pkl
OUTPUT_DIR=${HOME}/comp_structure_research/bigbox_25Mpc/data

mpirun -np ${NPROCS} ${MPI_ARGS} python ${SQUIRREL} ${ENZO_DATASET} ${HALO_DATASET} ${OUTPUT_DIR}
