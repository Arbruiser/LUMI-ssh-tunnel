#!/bin/bash
#SBATCH -A project_XXXXXXXXX
#SBATCH -p dev-g
#SBATCH --time 2:00:00
#SBATCH --tasks-per-node 1
#SBATCH --cpus-per-task=7
#SBATCH --gpus-per-node 1
#SBATCH --nodes 1
#SBATCH --mem 60G

# We use the PyTorch container provided by the LUMI AI Factory Services, which contains vLLM.
export CONTAINER_IMAGE=/appl/local/laifs/containers/lumi-multitorch-latest.sif
module use /appl/local/laifs/modules
module load lumi-aif-singularity-bindings

# Where to store the huge models. Point this to your project's scratch directory.
export HF_HOME=/scratch/$SLURM_JOB_ACCOUNT/hf-cache/

# Torch compilation currently fails in the container, so we disable it here.
export TORCH_COMPILE_DISABLE=1

# Make sure vLLM only sees available GPU(s)
export HIP_VISIBLE_DEVICES=$ROCR_VISIBLE_DEVICES

# Generate the API key
export API_KEY=$(openssl rand -hex 16)

echo "================================================================="
echo "🔑 YOUR SUPER SECRET API KEY FOR THIS SESSION IS:"
echo $API_KEY
echo "================================================================="

# Start vLLM
srun singularity exec $CONTAINER_IMAGE ./run-vllm-process.sh Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8 \
 --api-key $API_KEY \
 --enable-auto-tool-choice \
 --tool-call-parser qwen3_coder
