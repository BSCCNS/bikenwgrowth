#!/bin/bash

# Run the largest cities first
sbatch ../schecules/analysis_largecity_parsets.job 61
sbatch ../schecules/analysis_largecity_parsets.job 60
sbatch ../schecules/analysis_largecity_parsets.job 59

# Run medium and small cities next
sbatch ../schecules/analysis_mediumcities.job
sbatch ../schecules/analysis_smallcities.job