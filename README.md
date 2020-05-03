# Research Notes

<!-- <img src="https://render.githubusercontent.com/render/math?math=f =\frac{\displaystyle M_*}{\displaystyle \frac{\Omega_b}{\Omega_m}M_{vir}}"> -->

## TODO:
1) Create weighted projections of halo density that inform us as to what we're seeing in the simulations. Do so in a way that allows easy modification (CLI arguments) for creating more kinds of plots.
   - No weight
   - Density Weighted
   - Temperature weighted
   - Metallicity weighted
   - Bulk Velocity weighted
   - Velocity Dispersion weighted
   - Surface Brightness weighted
   - Star Particle Overlay
   - Density,Temperature,CellMass phase diagram
 
 2) Automate and optimize (parallelize?) plot creation for small simulation dataset
 
 3) Get rockstar running independent of yt
 
 4) Automate full pipeline that:
   - Runs rockstar on a simulation dataset to create halo catalogs
   - Runs script on halo catalogs to extract relevant data to smaller text files that can more easily/quickly be read by plotting scripts
   - Creates plots and saves their images. 
   
## Misc ideas for workflow development:
   - Use an environment variable (RUN_TESTS=0,1) or CLI argument to run scripts using test data with assertions or to accept a production dataset as an input value
   




