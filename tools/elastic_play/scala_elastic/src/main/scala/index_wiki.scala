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
        val map_df = df.select("title", "revision").map(article => Map("title " -> article(0),  " body_text " -> article(1))).first()
        val transformed_df = df.select("title", "revision").map(article => ("title: " + article(0) + " body_text: " + article(1))).map(t_a => t_a.slice(0, 2000))
        val intermediary_df = transformed_df.first()
        val punc_df = transformed_df.map(t_a => t_a.replaceAll("""[\p{Punct}&&[^:]]""", " ")).first()
        println("########################################")
        println("########################################")
        println(map_df)
        println("########################################")
        println("########################################")

        println("########################################")
        println("########################################")
        println(punc_df)
        println("########################################")
        println("########################################")
}
}
