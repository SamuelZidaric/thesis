#!/bin/bash
#SBATCH --job-name=convert_btf_to_avi
#SBATCH --time=0-01:00:00
#SBATCH --output=logs/btf2avi_job-%J/btf2avi_RUNME-%J.log
#SBATCH --mem=10G

# Count the number of sub-folders in the main directory that end with "_sam"
NUMDIRS=$(ls -d *_sam | wc -l)

# Adjust for zero-based indexing
ZBNUMDIRS=$(($NUMDIRS - 1))

# Log the number of jobs to be created
echo "${NUMDIRS} jobs have been created"

# Check if there are sub-folders to process
if [ $ZBNUMDIRS -ge 0 ]; then
  # Log the zero-based number of jobs
  echo "Submitting $ZBNUMDIRS jobs"
  
  # Submit an array job for each sub-folder
  sbatch --array=0-$ZBNUMDIRS /scratch/neurobiology/zimmer/zidaric/code/converters/btf2avi/btf_2_avi_behavior_folder_improved.sh
else
  # Log a message if there are no sub-folders to process
  echo "No jobs to submit, as there are no directories ending with _sam."
fi
