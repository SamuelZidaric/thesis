#!/bin/bash
#SBATCH --job-name=convert_btf_to_avi
#SBATCH --cpus-per-task=1
#SBATCH --mem=1GB
#SBATCH --time=0-01:00:00
#SBATCH --output=logs/btf2avi_job-%J/btf2avi_folder-%J.log

# Activate the conda environment
source /apps/conda/miniconda3/bin/activate HR_tracker_v2

# Full path to the Python script to run
command="/scratch/neurobiology/zimmer/zidaric/code/converters/btf2avi/btf_2_avi_behavior_improved.py"

# List directories in the current directory
DIRS=("$PWD/"*/)

echo "Converting behavior .btf folders to .avi"

# Navigate to the directory specified by the SLURM_ARRAY_TASK_ID
cd ${DIRS[SLURM_ARRAY_TASK_ID]}

# Run the Python script, passing the current directory as an argument
python $command --path $PWD
