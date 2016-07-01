import org.apache.spark.sql.SQLContext

val sqlContext = new SQLContext(sc)
val df = sqlContext.read.format("com.databricks.spark.xml").option("rowTag", "page").load("s3a://wiki-xml-dump/sample_dump.xml") 


