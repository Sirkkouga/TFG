#!/bin/bash

#SBATCH -p veu             # Partition to submit to
#SBATCH --mem=10G      # Max CPU Memory
#SBATCH --output=log/preprocessingbytecode.log  # ir_functions

python -m codegen_sources.preprocessing.preprocess \
/home/usuaris/veu/javier.abella/TFG/datasetbytecodeIR \
--langs bytecode \
--mode ir_full_files \
--bpe_mode fast \
--local True \
--train_splits 1 \
--ncodes 500 \
--percent_test_valid 20