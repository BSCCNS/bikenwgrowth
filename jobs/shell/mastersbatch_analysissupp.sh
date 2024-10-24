#!/bin/bash

# Run the largest cities first
sbatch ../schecules/analysissupp_largecity_parsets.job 61
sbatch ../schecules/analysissupp_largecity_parsets.job 60
sbatch ../schecules/analysissupp_largecity_parsets.job 59

# Run medium and small cities next
sbatch ../schecules/analysissupp_mediumcities.job
sbatch ../schecules/analysissupp_smallcities.job