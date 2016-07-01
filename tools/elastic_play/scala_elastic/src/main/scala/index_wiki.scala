package my_wiki

import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.SQLContext._

object WikiIndex {
    def main(args: Array[String]): Unit = {
        val sqlContext = new SQLContext(sc)
        val df = sqlContext.read.format("com.databricks.spark.xml").option("rowTag", "page").load("s3a://wiki-xml-dump/sample_dump.xml")
}}
