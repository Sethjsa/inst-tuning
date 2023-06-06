#!/bin/bash
#SBATCH --nodes=1                                  # Run on 1 nodes (each node has 48 cores)
#SBATCH --ntasks-per-node=1                        # Run one task
#SBATCH --partition=gengpu                       # Select the correct partition.                              # Run on 1 nodes (each node has 48 cores)
#SBATCH --ntasks-per-node=1                      # Use 8 cores, most of the procesing happens on the GPU
#SBATCH --mem=100GB                                  # Expected ammount CPU RAM needed (Not GPU Memory)
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=6                         # Use 4 cores, most of the procesing happens on the GPU
#SBATCH --time=24:00:00 
#SBATCH --mail-type=BEGIN,END,FAIL                       # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=seth.aycock@city.ac.uk   # Where to send mail

while getopts m:n:t:o: flag
do
    case "${flag}" in
        m) model=${OPTARG};;
        n) ngram=${OPTARG};;
        t) type=${OPTARG};;
        o) output=${OPTARG};;
    esac
done

#Enable modules command
source /opt/flight/etc/setup.sh
flight env activate gridware

#Remove any unwanted modules
module purge

module load libs/nvidia-cuda/11.2.0/bin
module load /users/xbkx052/archive/anaconda3
source /users/xbkx052/archive/anaconda3/etc/profile.d/conda.sh
conda activate nlp

nvidia-smi

GPUS_PER_NODE=1
# Number of GPU workers, for single-worker training, please set to 1
WORKER_CNT=1
export MASTER_PORT=8214
# The rank of this worker, should be in {0, ..., WORKER_CNT-1}, for single-worker training, please set to 0
export RANK=0

# DATA='/users/xbkx052/archive/alpaca-lora/${model}_data_shuf${ngram}_${output}.json

python finetune.py \
    --base_model '/users/xbkx052/archive/llama-7b' \
    --data_path '/users/xbkx052/archive/alpaca-lora/'${model}'_data_'${type}''${ngram}'_'${output}'.json' \
    --output_dir './lora-'${model}'-'${type}''${ngram}'-'${output}'' \
    --enable_lora True \
    --modules_to_save '[q_proj,k_proj,v_proj,o_proj]' \
    --batch_size 48 \
    --micro_batch_size 48 \
    --num_epochs 10 \
    --learning_rate 3e-4 \
    --logging_steps 1 \
    --cutoff_len 512 \
    --evaluation_strategy "no" \
    --lora_r 16 \
    --lora_alpha 16 \
    --lora_dropout 0.05 \
    --lora_target_modules '[q_proj,k_proj,v_proj,o_proj]' \
    --train_on_inputs \
    --group_by_length \
    --use_wanbd \
    --wandb_watch "gradient" \
    --wandb_project "city-nlp" \
    --wandb_log_model "true"