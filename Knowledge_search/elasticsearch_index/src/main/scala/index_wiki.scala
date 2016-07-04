package my_wiki

import org.apache.spark._
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.SQLContext._
import org.elasticsearch.spark._
import org.elasticsearch.spark.sql._
import org.elasticsearch.spark.rdd.EsSpark
import org.elasticsearch.hadoop.cfg.ConfigurationOptions
import org.apache.hadoop.fs.Path
import org.apache.hadoop.mapred.{FileOutputCommitter, FileOutputFormat, JobConf}
import com.typesafe.config.ConfigFactory
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.{Future, _}
import scala.concurrent.duration._


object WikiIndex {
    def main(args: Array[String]): Unit = {
        /* initialize a spark context */
        val conf = new SparkConf().setAppName("index_wiki").setMaster("spark://" + sys.env("master_node_dns") + ":7077")
        conf.set("es.resource", "wiki_index/article")
        conf.set("es.nodes", sys.env("elasticsearch_node_dns") + ":9200")
        conf.set("es.index.auto.create", "true")
        val sc = new SparkContext(conf)

        /* read xml into a dataframe */
        val sqlContext = new SQLContext(sc)
        val df = sqlContext.read.format("com.databricks.spark.xml").option("rowTag", "page").load("s3a://wiki-xml-dump/enwiki-20160407.xml")

        val index_rdd = df.select("title", "revision").map(article => Map("title" -> article(0), "body_text" -> article(1).toString.slice(0, 2000).replaceAll("[^A-Za-z0-9]", " ")))

        /* write to elastic search */
        index_rdd.saveToEs("wiki_index/article") 
    }
}

