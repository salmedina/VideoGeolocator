#!/usr/bin/env bash

RESULT_DIR=/home/yingkaig/VideoGeolocator/VideoProcessing/netvlad
FOLDER_NAME=output_*
OUTPUT_DIR=output

python combine_batch_mat.py $RESULT_DIR $FOLDER_NAME $OUTPUT_DIR
