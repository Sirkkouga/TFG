#!/bin/bash

#SBATCH -p veu             # Partition to submit to
#SBATCH --mem=10G      # Max CPU Memory
#SBATCH --output=log/preprocessingbytecode.log

export BPE_PATH="/home/usuaris/veu/javier.abella/TFG/datacode"

python -m codegen_sources.preprocessing.preprocess \
/home/usuaris/veu/javier.abella/TFG/datacodegz \
--langs java kotlin bytecode \
--mode ir_full_files \
--local True \
--bpe_mode fast \
--fastbpe_code_path $BPE_PATH \
--train_splits 1