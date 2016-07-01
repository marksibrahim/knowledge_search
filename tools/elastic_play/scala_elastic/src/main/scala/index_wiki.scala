package my_wiki

import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.SQLContext._
import org.elasticsearch.spark.sql._
import org.apache.spark._

object WikiIndex {
    def main(args: Array[String]): Unit = {
    /* initialize a spark context */
        val conf = new SparkConf().setAppName("Oleg")
        val sc = new SparkContext(conf)

    /* read xml into a dataframe */
        val sqlContext = new SQLContext(sc)
        val df = sqlContext.read.format("com.databricks.spark.xml").option("rowTag", "page").load("s3a://wiki-xml-dump/sample_dump.xml")
        val transformed_df = df.select("title", "revision").map(article => "title: " + t(0)).first().foreach(println)


}}
