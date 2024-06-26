#!/bin/bash
 
#SBATCH -p veu             # Partition to submit to
#SBATCH --mem=10G          # Max CPU Memory
#SBATCH --output=/home/usuaris/veu/javier.abella/TFG/log/trainingbackup.log
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
 
export DUMP_PATH="/home/usuaris/veu/javier.abella/TFG/log"
export DATASET_PATH="/home/usuaris/veu/javier.abella/TFG/datacodegz"
export EXP_NAME="Java2kotlin_4"
export LANGUAGES="java,kotlin,bytecode"
 
python codegen_sources/model/train.py \
--dump_path $DUMP_PATH \
--data_path $DATASET_PATH \
--exp_name $EXP_NAME \
--lgs 'java-kotlin-bytecode' \
--mlm_steps 'java,kotlin,bytecode' \
--word_pred '0.15' \
--word_mask_keep_rand '0.8,0.1,0.1' \
--encoder_only false \
--n_layers 0 \
--n_layers_decoder 6 \
--n_layers_encoder 6 \
--emb_dim 1024 \
--bptt 256 \
--n_heads 8 \
--max_vocab 64000 \
--dropout '0.1' \
--optimizer 'adam_inverse_sqrt,warmup_updates=10000,lr=0.003,weight_decay=0.01' \
--max_len 2000 \
--max_batch_size 128 \
--tokens_per_batch 2000 \
--clip_grad_norm 1 \
--epoch_size 100000 \
--max_epoch 10000000 \
--batch_size 16 \
--amp 2 \
--fp16 true \
--stopping_criterion '_valid_mlm_ppl,50' \
--validation_metrics '_valid_mlm_ppl' \
--eval_st false