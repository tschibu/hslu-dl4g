#!/bin/bash
#usage: ./showDataStats
#

echo "Trump Data Stats:"
train_count=$(ls data/trump/train*.csv | wc -l)
test_count=$(ls data/trump/test*.csv | wc -l)
val_count=$(ls data/trump/val*.csv | wc -l)
echo "  Train Count : $train_count"
echo "  Test Count  : $test_count"
echo "  Val Count   : $val_count"
