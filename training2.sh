#!/bin/bash
 
#SBATCH -p veu             # Partition to submit to
#SBATCH --mem=10G          # Max CPU Memory
#SBATCH --output=/home/usuaris/veu/javier.abella/TFG/log/training2.log
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --nodelist=veuc10

export DUMP_PATH="/home/usuaris/veu/javier.abella/TFG/log"
export DATASET_PATH="/home/usuaris/veu/javier.abella/TFG/datacodegz"
export EXP_NAME="Java2kotlin_1"
export LANGUAGES="java,kotlin,bytecode"

python codegen_sources/model/train.py \
--exp_name $EXP_NAME \
--dump_path $DUMP_PATH \
--data_path $DATASET_PATH \
--split_data_accross_gpu local \
--ae_steps 'kotlin,java'  \
--lambda_ae '0:1,30000:0.1,100000:0'  \
--word_shuffle 3  \
--word_dropout '0.1' \
--word_blank '0.3'  \
--encoder_only False \
--n_layers 0  \
--n_layers_encoder 6  \
--n_layers_decoder 6 \
--emb_dim 1024  \
--n_heads 8  \
--lgs 'java-bytecode-kotlin'  \
--max_vocab 64000 \
--gelu_activation false \
--max_len 512 \
--reload_model "/home/usuaris/veu/javier.abella/TFG/log/Java2kotlin_1/56816/checkpoint.pth,/home/usuaris/veu/javier.abella/TFG/log/Java2kotlin_1/56816/checkpoint.pth" \
--reload_encoder_for_decoder true \
--lgs_mapping 'java:java,bytecode:bytecode,kotlin:kotlin' \
--amp 2  \
--fp16 true  \
--tokens_per_batch 3000  \
--group_by_size true \
--max_batch_size 128 \
--epoch_size 50000  \
--max_epoch 10000000  \
--split_data_accross_gpu global \
--optimizer 'adam_inverse_sqrt,warmup_updates=10000,lr=0.0001,weight_decay=0.01' \
--eval_bleu true \
--eval_computation true \
--has_sentence_ids "valid|para,test|para" \
--generate_hypothesis true \
--save_periodic 1 \