import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, timestamp_millis
from pyspark.sql.types import (
    BooleanType,
    DoubleType,
    LongType,
    StringType,
    StructField,
    StructType,
)

# Define schema for Binance aggregate trade events
trade_schema = StructType(
    [
        StructField("e", StringType()),  # event type ("aggTrade")
        StructField("E", LongType()),  # event time (UNIX ms)  <-- Long
        StructField("s", StringType()),  # symbol ("BTCUSDT")
        StructField("a", LongType()),  # aggregate trade ID    <-- Long
        StructField("p", StringType()),  # price (string)
        StructField("q", StringType()),  # quantity (string)
        StructField("f", LongType()),  # first trade ID        <-- Long
        StructField("l", LongType()),  # last trade ID         <-- Long
        StructField("T", LongType()),  # trade time (UNIX ms)  <-- Long
        StructField("m", BooleanType()),  # is buyer the maker    <-- Boolean
    ]
)

# Create SparkSession (Spark Master will be provided by container or use local if standalone)
spark = SparkSession.builder.appName("CryptoTradeStreaming").getOrCreate()

kafka_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

# Read from Kafka topic as streaming DataFrame
df_kafka = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", kafka_servers)
    .option("subscribe", "crypto_trades")
    .option("startingOffsets", "latest")
    .option("failOnDataLoss", "false")
    .load()
)
# The incoming data is in the "value" field as bytes. Convert to JSON string and parse.
df_strings = df_kafka.selectExpr("CAST(value AS STRING) as json_str")

# Parse JSON and select only needed columns with clean types
df_raw = df_strings.select(from_json(col("json_str"), trade_schema).alias("trade"))
df_clean = df_raw.select(
    timestamp_millis(col("trade.T")).alias("timestamp"),
    col("trade.s").alias("symbol"),
    col("trade.p").cast(DoubleType()).alias("price"),
    col("trade.q").cast(DoubleType()).alias("quantity"),
    col("trade.m").alias("is_buyer_maker"),
    col("trade.a").alias("trade_id"),
    col("trade.T").alias("trade_time_ms"),
)

# ES configuration
es_host = os.getenv("ES_HOST", "es")
es_port = os.getenv("ES_PORT", "9200")
es_user = os.getenv("ES_USER", "elastic")
es_pass = os.getenv("ES_PASS", os.getenv("ELASTIC_PASSWORD"))


def write_to_es(batch_df, batch_id):
    batch_df.write.format("org.elasticsearch.spark.sql").option(
        "es.nodes", es_host
    ).option("es.port", es_port).option("es.nodes.wan.only", "true").option(
        "es.resource", "crypto-trades-v2"
    ).option(
        "es.index.auto.create", "true"
    ).option(
        "es.net.http.auth.user", es_user
    ).option(
        "es.net.http.auth.pass", es_pass
    ).mode(
        "append"
    ).save()


query = (
    df_clean.writeStream.foreachBatch(write_to_es)
    .option("checkpointLocation", "/tmp/spark_checkpoints/crypto_trades")
    .start()
)

query.awaitTermination()
