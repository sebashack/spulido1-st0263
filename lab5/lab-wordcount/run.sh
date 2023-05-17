#!/bin/bash

INPUT_PATH='/user/hadoop/datasets/gutenberg-small/*.txt'
HADOOP_JAR='/usr/lib/hadoop-mapreduce/hadoop-streaming.jar'
OUT_PATH='/user/hadoop/results/example1'

python wordcount-mr.py -r hadoop hdfs://${INPUT_PATH} --output-dir hdfs://${OUT_PATH} --hadoop-streaming-jar ${HADOOP_JAR}
