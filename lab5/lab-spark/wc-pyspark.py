from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("WordCount").getOrCreate()
sc = spark.sparkContext

files_rdd_s3 = sc.textFile("s3://st0263spulido1/datasets/gutenberg-small/*.txt")
files_rdd_hdfs = sc.textFile("hdfs:///user/hadoop/datasets/gutenberg-small/*.txt")

wc_unsort_s3 = files_rdd_s3.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
wc_unsort_hdfs = files_rdd_hdfs.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

wc_s3 = wc_unsort_s3.sortBy(lambda a: -a[1])
wc_hdfs = wc_unsort_hdfs.sortBy(lambda a: -a[1])

wc_hdfs.coalesce(1).saveAsTextFile("hdfs:///user/hadoop/results-wc-spark/wordcount1.one")
wc_s3.coalesce(1).saveAsTextFile("s3://st0263spulido1/wordcount2.two")
