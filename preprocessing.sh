#!/bin/bash

python -m codegen_sources.preprocessing.preprocess \
datasets \
--langs java kotlin bytecode \
--mode monolingual_functions \
--bpe_mode fast \
--local True \
--train_splits 1
