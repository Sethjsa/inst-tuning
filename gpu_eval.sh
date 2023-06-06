#!/bin/bash
#SBATCH --nodes=1                                  # Run on 1 nodes (each node has 48 cores)
#SBATCH --ntasks-per-node=1                        # Run one task
#SBATCH --partition=gengpu                       # Select the correct partition.                              # Run on 1 nodes (each node has 48 cores)
#SBATCH --ntasks-per-node=1                      # Use 8 cores, most of the procesing happens on the GPU
#SBATCH --mem=47GB                                  # Expected ammount CPU RAM needed (Not GPU Memory)
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=6                          # Use 4 cores, most of the procesing happens on the GPU
#SBATCH --time=64:00:00 
#SBATCH --mail-type=BEGIN,END,FAIL                       # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=seth.aycock@city.ac.uk   # Where to send mail

while getopts m:n:t:o:1:2:3:4: flag
do
    case "${flag}" in
        m) model=${OPTARG};;
        n) ngram=${OPTARG};;
        t) type=${OPTARG};;
        o) output=${OPTARG};;
        1) zero=${OPTARG};;
        2) five=${OPTARG};;
        3) ten=${OPTARG};;
        4) twenfive=${OPTARG};;
        
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

# ,peft=/users/xbkx052/archive/alpaca-lora/lora-${model}${type}${ngram}${output}

if [[ -n "${zero}" ]];
    then 
        python /users/xbkx052/archive/eval/harness/lm-evaluation-harness/main.py \
            --model hf-causal-experimental \
            --model_args pretrained=/users/xbkx052/archive/llama-7b,load_in_8bit=True,dtype="float16",peft=/users/xbkx052/archive/alpaca-lora/lora-${model}${type}${ngram}${output} \
            --batch_size 16 \
            --device cuda:0 \
            --remove_pc 20 \
            --num_fewshot 0 \
            --tasks hellaswag,boolq,piqa,openbookqa,arc_easy,arc_challenge,cb,wic,wsc,race,record,xnli_en,qnli
fi

# ,truthfulqa_mc,crows_pairs_eng*
# winogrande,xwinograd_en,multirc,

if [[ -n "${five}" ]];
    then 
        python /users/xbkx052/archive/eval/harness/lm-evaluation-harness/main.py \
            --model hf-causal-experimental \
            --model_args pretrained=/users/xbkx052/archive/llama-7b,load_in_8bit=True,dtype="float16",peft=/users/xbkx052/archive/alpaca-lora/lora-${model}${type}${ngram}${output} \
            --batch_size 2 \
            --device cuda:0 \
            --remove_pc 20 \
            --num_fewshot 5 \
            --tasks hendrycksTest*
fi

if [[ -n "${ten}" ]];
    then 
        python /users/xbkx052/archive/eval/harness/lm-evaluation-harness/main.py \
            --model hf-causal-experimental \
            --model_args pretrained=/users/xbkx052/archive/llama-7b,load_in_8bit=True,dtype="float16",peft=/users/xbkx052/archive/alpaca-lora/lora-${model}${type}${ngram}${output} \
            --batch_size 16 \
            --device cuda:0 \
            --remove_pc 20 \
            --num_fewshot 10 \
            --tasks hellaswag
fi

if [[ -n "${twenfive}" ]];
    then 
        python /users/xbkx052/archive/eval/harness/lm-evaluation-harness/main.py \
            --model hf-causal-experimental \
            --model_args pretrained=/users/xbkx052/archive/llama-7b,load_in_8bit=True,dtype="float16",peft=/users/xbkx052/archive/alpaca-lora/lora-${model}${type}${ngram}${output} \
            --batch_size 16 \
            --device cuda:0 \
            --remove_pc 20 \
            --num_fewshot 25 \
            --tasks arc_*
fi


# hellaswag,boolq,piqa,openbookqa,arc_easy,arc_challenge,lambada_standard,winogrande,cb,wic,wsc,race,multirc,record,xnli_en,qnli,truthfulqa_mc,crows_pairs_eng*,xwinograd_en

# dtype="float16",load_in_8bit=True,
# ,load_in_8bit=True,peft=/users/xbkx052/archive/alpaca-lora/lora-dolly-n-i-o-n-i-o


# python /users/xbkx052/archive/eval/harness/lm-evaluation-harness/main.py \
#     --model hf-causal-experimental \
#     --model_args pretrained=facebook/opt-125m \
#     --batch_size 16 \
#     --remove_pc 20 \
#     --remove_few \
#     --device cuda:0 \
#     --limit 2 \
#     --num_fewshot 2 \
#     --tasks hellaswag,boolq,piqa,openbookqa,arc_easy,arc_challenge,cb,wic,wsc,race,multirc,record,xnli_en,qnli,truthfulqa_mc,crows_pairs_eng*,xwinograd_en
