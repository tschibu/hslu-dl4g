#!/bin/bash
#usage: ./generateTrumpData fromScratch #delete old data, generate all the data from scratch
#       ./generateTrumpData #only run filter and generate csv

ARG=$1

MOST_GAMES_PER=0.8
BEST_MEAN_PER=0.2
CURRENT_DIR=$(pwd)
OUTPUT_DIR_DATA="$CURRENT_DIR/data/trump"
OUTPUT_DIR_TEMP="${OUTPUT_DIR_DATA}/temp"

TEMP_TRAIN="$OUTPUT_DIR_TEMP/train"
TEMP_TEST="$OUTPUT_DIR_TEMP/test"
TEMP_VAL="$OUTPUT_DIR_TEMP/val"

TEMP_FILTERED_TRAIN="$OUTPUT_DIR_TEMP/filtered_train"
TEMP_FILTERED_TEST="$OUTPUT_DIR_TEMP/filtered_test"
TEMP_FILTERED_VAL="$OUTPUT_DIR_TEMP/filtered_val"

JASSKIT_BIN="$CURRENT_DIR/jass-kit/tools"

mkdir -p $OUTPUT_DIR_TEMP $TEMP_TRAIN $TEMP_TEST $TEMP_VAL
# filterd dirs
mkdir -p $TEMP_FILTERED_TRAIN $TEMP_FILTERED_TEST $TEMP_FILTERED_VAL

# cleanup - only if fromScratch
if [ "$ARG" == "fromScratch" ] ; then
    rm  -rf $OUTPUT_DIR_DATA | true

    # Training data
    for file in $(find jass-data/split/train -type f | sort); do
      cat $file >> "${OUTPUT_DIR_TEMP}/train.txt"
    done

    # Test data
    for file in $(find jass-data/split/test -type f | sort); do
      cat $file >> "${OUTPUT_DIR_TEMP}/test.txt"
    done

    # Validation set (Do not use this for train / validate your model)
    for file in $(find jass-data/split/val -type f | sort); do
      cat $file >> "${OUTPUT_DIR_TEMP}/val.txt"
    done

    # convert to playerround
    cd $JASSKIT_BIN
    python convert_rounds_to_player_rounds.py --trump --output player_rnd_trump_train --output_dir $TEMP_TRAIN ${OUTPUT_DIR_TEMP}/train.txt
    python convert_rounds_to_player_rounds.py --trump --output player_rnd_trump_test --output_dir $TEMP_TEST ${OUTPUT_DIR_TEMP}/test.txt
    python convert_rounds_to_player_rounds.py --trump --output player_rnd_trump_val --output_dir $TEMP_VAL ${OUTPUT_DIR_TEMP}/val.txt

    # merge playerround to one big file
    # Training data
    for file in $(find $TEMP_TRAIN -type f | sort); do
    cat $file >> "${OUTPUT_DIR_TEMP}/train_rounds_merged.txt"
    done

    # Test data
    for file in $(find $TEMP_TEST -type f | sort); do
    cat $file >> "${OUTPUT_DIR_TEMP}/test_rounds_merged.txt"
    done

    # Validation set (Do not use this for train / validate your model)
    for file in $(find $TEMP_VAL -type f | sort); do
    cat $file >> "${OUTPUT_DIR_TEMP}/val_rounds_merged.txt"
    done
fi

if [ ! -f ${OUTPUT_DIR_TEMP}/train_rounds_merged.txt ]; then
    echo "train_rounds_merged.txt does not exists run ./generateTrumpData.sh fromScratch"
    exit 1
fi
if [ ! -f ${OUTPUT_DIR_TEMP}/test_rounds_merged.txt ]; then
    echo "test_rounds_merged.txt does not exists run ./generateTrumpData.sh fromScratch"
    exit 1
fi
if [ ! -f ${OUTPUT_DIR_TEMP}/val_rounds_merged.txt ]; then
    echo "val_rounds_merged.txt does not exists run ./generateTrumpData.sh fromScratch"
    exit 1
fi


cd $JASSKIT_BIN

# filter the best players form the merged rounds
python filter_player_rounds.py --played_games_most_perc $MOST_GAMES_PER --mean_best_perc $BEST_MEAN_PER --output filtered_trump_train --output_dir $TEMP_FILTERED_TRAIN --stat $CURRENT_DIR/jass-data/stat/player_all_stat.json ${OUTPUT_DIR_TEMP}/train_rounds_merged.txt
python filter_player_rounds.py --played_games_most_perc $MOST_GAMES_PER --mean_best_perc $BEST_MEAN_PER --output filtered_trump_test --output_dir $TEMP_FILTERED_TEST --stat $CURRENT_DIR/jass-data/stat/player_all_stat.json ${OUTPUT_DIR_TEMP}/test_rounds_merged.txt
python filter_player_rounds.py --played_games_most_perc $MOST_GAMES_PER --mean_best_perc $BEST_MEAN_PER --output filtered_trump_val --output_dir $TEMP_FILTERED_VAL --stat $CURRENT_DIR/jass-data/stat/player_all_stat.json ${OUTPUT_DIR_TEMP}/val_rounds_merged.txt

# merge filterd files to one huge file
# Training data
for file in $(find $TEMP_FILTERED_TRAIN -type f | sort); do
  cat $file >> "${OUTPUT_DIR_TEMP}/train_rounds_filtered_merged.txt"
done

# Test data
for file in $(find $TEMP_FILTERED_TEST -type f | sort); do
  cat $file >> "${OUTPUT_DIR_TEMP}/test_rounds_filtered_merged.txt"
done

# Validation set (Do not use this for train / validate your model)
for file in $(find $TEMP_FILTERED_VAL -type f | sort); do
  cat $file >> "${OUTPUT_DIR_TEMP}/val_rounds_filtered_merged.txt"
done

python convert_player_rounds_trump_to_csv.py --output_dir $OUTPUT_DIR_DATA $OUTPUT_DIR_TEMP/train_rounds_filtered_merged.txt
python convert_player_rounds_trump_to_csv.py --output_dir $OUTPUT_DIR_DATA $OUTPUT_DIR_TEMP/test_rounds_filtered_merged.txt
python convert_player_rounds_trump_to_csv.py --output_dir $OUTPUT_DIR_DATA $OUTPUT_DIR_TEMP/val_rounds_filtered_merged.txt
