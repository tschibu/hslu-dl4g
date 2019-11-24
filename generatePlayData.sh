#!/bin/bash

CURRENT_DIR=$(pwd)
OUTPUT_DIR_DATA="$CURRENT_DIR/data/play"
OUTPUT_DIR_TEMP="${OUTPUT_DIR_DATA}/temp"

TEMP_TRAIN="$OUTPUT_DIR_TEMP/play_train"
TEMP_TEST="$OUTPUT_DIR_TEMP/play_test"
TEMP_VAL="$OUTPUT_DIR_TEMP/play_val"

JASSKIT_BIN="$CURRENT_DIR/jass-kit/tools"

# cleanup
rm  -rf $OUTPUT_DIR_DATA | true
mkdir -p $OUTPUT_DIR_TEMP $TEMP_TRAIN $TEMP_TEST $TEMP_VAL

# Training data
for file in $(find jass-data/split/train -type f | sort); do
  cat $file >> "${OUTPUT_DIR_TEMP}/play_train.txt"
done

# Test data
for file in $(find jass-data/split/test -type f | sort); do
  cat $file >> "${OUTPUT_DIR_TEMP}/play_test.txt"
done

# Validation set (Do not use this for train / validate your model)
for file in $(find jass-data/split/val -type f | sort); do
  cat $file >> "${OUTPUT_DIR_TEMP}/play_val.txt"
done


# convert to playerround
cd $JASSKIT_BIN
python convert_rounds_to_player_rounds.py --output player_rnd_play_train --output_dir $TEMP_TRAIN $OUTPUT_DIR_TEMP/play_train.txt
python convert_rounds_to_player_rounds.py --output player_rnd_play_test --output_dir $TEMP_TEST $OUTPUT_DIR_TEMP/play_test.txt
python convert_rounds_to_player_rounds.py --output player_rnd_play_val --output_dir $TEMP_VAL $OUTPUT_DIR_TEMP/play_val.txt

# merge playerround to one big file
# Training data
for file in $(find $TEMP_TRAIN -type f | sort); do
  cat $file >> "$OUTPUT_DIR_TEMP/play_train_rounds_merged.txt"
done

# Test data
for file in $(find $TEMP_TEST -type f | sort); do
  cat $file >> "$OUTPUT_DIR_TEMP/play_test_rounds_merged.txt"
done

# Validation set (Do not use this for train / validate your model)
for file in $(find $TEMP_VAL -type f | sort); do
  cat $file >> "$OUTPUT_DIR_TEMP/play_val_rounds_merged.txt"
done

python convert_player_rounds_to_csv.py --output_dir $OUTPUT_DIR_DATA $OUTPUT_DIR_TEMP/play_test_rounds_merged.txt
python convert_player_rounds_to_csv.py --output_dir $OUTPUT_DIR_DATA $OUTPUT_DIR_TEMP/play_val_rounds_merged.txt
python convert_player_rounds_to_csv.py --output_dir $OUTPUT_DIR_DATA $OUTPUT_DIR_TEMP/play_train_rounds_merged.txt
