# Diffusion-limited-aggregation
This model utilizes a diffusion-limited aggregation process to simulate bacterial growth on a limited nutrient substrate.

#Black and White cluster
-Inital code used to implement DLA into a bacterial growth simulation. All other files were built off this initial code.

#Color Cluster
-Utilized Black and White cluster to simulate DLG from 6 distinct initial seeds. From here, the Center of Mass, and statistics
 code were built as this offered a way to characterize individual clusters within the array, which the initial code did not allow for.

 #Statistics 1
 -Builds off the same methods used in the previous two codes and collects data on the distribution of particles in the array. 
  This model only calculates statistics for an aggregate grown from a single seed.

  #Statistics 2
  -Uses similar methods as Statistics 1, but includes two adjacent seeds from which aggregates are grown.

  #Center of Mass
  -Uses similar methods as previous code, however, the center of mass of each cluster is calculated using particle location information
   stored in the lattice array.
