#!/bin/bash

# Run the largest cities first
sbatch ../schecules/export_largecity_parsets.job 61
sbatch ../schecules/export_largecity_parsets.job 60
sbatch ../schecules/export_largecity_parsets.job 59

# Run medium and small cities next
sbatch export_smallcities.job