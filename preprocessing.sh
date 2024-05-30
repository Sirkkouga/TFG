#!/bin/bash

python -m codegen_sources.preprocessing.preprocess \
/home/usuaris/veu/javier.abella/TFG/datasets \
--langs java \
--mode monolingual_functions \
--bpe_mode fast \
--local True \
--train_splits 1
 