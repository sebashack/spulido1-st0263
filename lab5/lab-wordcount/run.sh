#!/bin/bash

# HDFS command
INPUT_PATH='/user/hadoop/datasets/gutenberg-small/*.txt'
HADOOP_JAR='/usr/lib/hadoop-mapreduce/hadoop-streaming.jar'
OUT_PATH='/user/hadoop/results/example1'

python wordcount-mr.py -r hadoop hdfs://${INPUT_PATH} --output-dir hdfs://${OUT_PATH} --hadoop-streaming-jar ${HADOOP_JAR}


# S3 command
INPUT_PATH='/st0263spulido1/datasets/gutenberg-small/*.txt'
HADOOP_JAR='/usr/lib/hadoop-mapreduce/hadoop-streaming.jar'
OUT_PATH='/st0263spulido1/wcount2'

python wordcount-mr.py -r hadoop s3:/${INPUT_PATH} --output-dir s3:/${OUT_PATH} --hadoop-streaming-jar ${HADOOP_JAR}
