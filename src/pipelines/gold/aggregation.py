import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count

logger = logging.getLogger(__name__)

class GoldAggregationJob:
    """
    Enterprise PySpark Gold Presentation Processor.
    Aggregates conformed structural Silver tables into business-level multidimensional data marts 
    optimized for sub-second analytical reporting queries and financial metrics verification.
    """
    def __init__(self, spark_session: SparkSession):
        self.spark = spark_session

    def execute_aggregation(self, silver_path: str, target_gold_path: str) -> None:
        """Aggregates corporate metrics compiling multi-million records down to highly dense facts dashboards."""
        logger.info(f"[Gold Pipeline] Ingesting conformed dimensional tables from Silver Layer: {silver_path}")
        silver_df = self.spark.read.parquet(silver_path).filter(col("is_current") == True)

        # Agregação Analítica Corporativa de Alto Nível (KPIs de Receita por Cliente)
        gold_business_mart_df = silver_df.groupBy("customer_id") \
                                          .agg(sum("amount").alias("total_revenue_spent"),
                                               count("order_id").alias("total_orders_placed")) \
                                          .withColumn("clv_tier", col("total_revenue_spent") * col("total_orders_placed")) # Customer Lifetime Value Proxy

        logger.info(f"[Gold Pipeline] Committing presentation marts to Lakehouse Gold Layer: {target_gold_path}")
        gold_business_mart_df.write.mode("overwrite").parquet(target_gold_path)
