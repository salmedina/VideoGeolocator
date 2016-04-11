#!/usr/bin/env bash
VIDEOS_DIR = ''
KEYFRAMES_DIR = ''
DB_FEATS_DIR = ''
QUERY_FEATS_DIR = ''
QUERY_SCORES = ''
QUERY_RESULTS = ''
TOP_N = 100

# 1. Extract the keyframes from all the videos in video dir
python ./keyframe.py $VIDEOS_DIR $KEYFRAMES_DIR

# 2. Obtain the NetVLAD feature vectors
matlab /r "getFeatVects($KEYFRAMES_DIR, $QUERY_FEATS_DIR)"

# 3. Calculate the similarity scores (Top 100) for each key-frame
python 

# 4. Rank the video according to each key-frame score

# 5. Save results

# 6. Display results at full corpuse level and per video based on keyframes
