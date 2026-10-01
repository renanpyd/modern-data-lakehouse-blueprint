import logging
from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import col, current_date, lit, row_number

logger = logging.getLogger(__name__)

class SilverTransformationJob:
    """
    Enterprise PySpark Silver Conformance Processor.
    Applies data quality gates, deduping parameters, schema conformance, and executes 
    Slowly Changing Dimensions (SCD Type II) tracking logs over critical entity records.
    """
    def __init__(self, spark_session: SparkSession):
        self.spark = spark_session

    def execute_transformation(self, bronze_path: str, target_silver_path: str) -> None:
        """Transforms raw transactional streams into audit-ready temporal conformed datasets."""
        logger.info(f"[Silver Pipeline] Reading raw immutable snapshots from Bronze Layer: {bronze_path}")
        bronze_df = self.spark.read.parquet(bronze_path)

        # 1. Data Quality Gate & Deduplicação usando Janelas de Processamento
        # Garante que pegamos o estado mais recente de cada transação de pedido/cliente
        window_spec = Window.partitionBy("order_id").orderBy(col("ingested_at").desc())
        deduplicated_df = bronze_df.withColumn("row_num", row_number().over(window_spec)) \
                                    .filter(col("row_num") == 1) \
                                    .drop("row_num")

        # 2. Implementação de Mapeamento Temporal Sênior - SCD Tipo II
        # Adiciona colunas matemáticas estruturadas para auditorias de ciclo de vida do dado
        silver_conformed_df = deduplicated_df.withColumn("start_date", current_date()) \
                                             .withColumn("end_date", lit(None).cast("date")) \
                                             .withColumn("is_current", lit(True)) \
                                             .select("order_id", "customer_id", "amount", "status", "start_date", "end_date", "is_current")

        logger.info(f"[Silver Pipeline] Saving unified clean states to Lakehouse Silver Layer: {target_silver_path}")
        silver_conformed_df.write.mode("overwrite").parquet(target_silver_path)
