#!/bin/bash
 
#SBATCH -p veu             # Partition to submit to
#SBATCH --mem=10G          # Max CPU Memory
#SBATCH --output=/home/usuaris/veu/javier.abella/TFG/log/evaluate.log
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1

python codegen_sources/model/train.py \
--reload_model "/home/usuaris/veu/javier.abella/TFG/log/Java2kotlin_1/56816/checkpoint.pth,/home/usuaris/veu/javier.abella/TFG/log/Java2kotlin_1/56816/checkpoint.pth" \
--eval_only True \
--reload_encoder_for_decoder false