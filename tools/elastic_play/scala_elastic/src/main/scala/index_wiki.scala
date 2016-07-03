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
        val conf = new SparkConf().setAppName("index_wiki").setMaster("spark://ec2-52-204-191-31.compute-1.amazonaws.com:7077")
        conf.set("es.resource", "wiki_index/article")
        conf.set("es.nodes", "ec2-52-204-244-120.compute-1.amazonaws.com:9200")
        conf.set("es.index.auto.create", "true")
        val sc = new SparkContext(conf)

    /* read xml into a dataframe */
        val sqlContext = new SQLContext(sc)
        val df = sqlContext.read.format("com.databricks.spark.xml").option("rowTag", "page").load("s3a://wiki-xml-dump/sample_dump.xml")
        val map_df = df.select("title", "revision").map(article => Map("title " -> article(0)))

        /** Elastic Search Job Settings     
        val appConfiguration = ConfigFactory.load()
        val index = appConfiguration.getString("wiki_index")
        val topic = appConfiguration.getString("test_topic")
        */

        /**
        val jobConfiguration = new JobConf(sc.SparkContext.hadoopConfiguration)
        jobConfiguration.set("mapred.output.format.class", "org.elasticsearch.hadoop.mr.EsOutputFormat")
        jobConfiguration.setOutputCommitter(classOf[FileOutputCommitter])
        jobConfiguration.set(ConfigurationOptions.ES_RESOURCE, indexWithTopic(index, topic))
        jobConfiguration.set(ConfigurationOptions.ES_NODES, appConfiguration.getString("ec2-52-204-244-120.compute-1.amazonaws.com"))
        FileOutputFormat.setOutputPath(jobConfiguration, new Path(appConfiguration.getString("/home/ubuntu/elasticsearch-2.3.3/config")))
        */

        map_df.saveToEs("wiki_index/article")

        /* saveToEs("test_index") */

        /* val transformed_df = df.select("title", "revision").map(article => ("title: " + article(0) + " body_text: " + article(1))).map(t_a => t_a.slice(0, 2000)) */
        /* val intermediary_df = transformed_df.first() */
        /* val punc_df = transformed_df.map(t_a => t_a.replaceAll("""[\p{Punct}&&[^:]]""", " ")).first() */
        println("########################################")
        println("########################################")
        /* println(map_df) */
        println("########################################")
        println("########################################")

        println("########################################")
        println("########################################")
        /* println(punc_df) */
        println("########################################")
        println("########################################")
}
}
