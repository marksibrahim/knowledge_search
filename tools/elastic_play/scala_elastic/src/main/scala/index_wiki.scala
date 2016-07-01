package my_wiki

import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.SQLContext._
import org.elasticsearch.spark.sql._
import org.apache.spark._



object WikiIndex {
    def main(args: Array[String]): Unit = {
    /* initialize a spark context */
        val conf = new SparkConf().setAppName("Load cached model")
        val sc = new SparkContext(conf)

        val sqlContext = new SQLContext(sc)
        val df = sqlContext.read.format("com.databricks.spark.xml").option("rowTag", "page").load("s3a://wiki-xml-dump/sample_dump.xml")
}}
