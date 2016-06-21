import pandas as pd
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from get_first_link import Article

"""
process xml dump using Article class using Spark cluster
"""



if __name__ == "__main__":
    # block transfer overcomes known error with netty network handler
    conf = SparkConf().setAppName("build fln").set("spark.shuffle.blockTransferService", "nio") 

    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    # load data into Spark DataFrame (runtime < 1min)
    sample_xml = "s3a://wiki-xml-dump/sample_dump.xml"
    full_xml = "s3a://wiki-xml-dump/enwiki-20160407.xml"

    df = sqlContext.read.format('com.databricks.spark.xml').options(rowTag='page').load(full_xml)

    fln_pandas_df = pd.DataFrame(df.select("title", "revision").map(lambda s: (s[0],Article(s[1].text[0]).first_link)).collect())

    fln_pandas_df.columns = [':START_ID(Article)', ':END_ID(Article)']
    fln_pandas_df.to_csv('fln.csv', encoding='utf-8', index=False)

"""
To Submit Spark Job:
spark-submit 
--packages com.databricks:spark-xml_2.10:0.3.3 
--master spark://master-node-dns:7077  
--executor-memory 6400M --driver-memory 6400M 
Knowledge_search/create_fln.py
"""
