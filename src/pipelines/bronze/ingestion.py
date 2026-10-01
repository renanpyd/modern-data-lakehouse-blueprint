import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name

logger = logging.getLogger(__name__)

class BronzeIngestionJob:
    """
    Enterprise PySpark Bronze Ingestion Processor.
    Executes raw, immutable ingestion routines from transactional systems (ERP/CRM)
    and persists them inside the data lakehouse warehouse layer adding systemic audit tracks.
    """
    def __init__(self, spark_session: SparkSession):
        self.spark = spark_session

    def execute_ingestion(self, source_path: str, target_bronze_path: str) -> None:
        """Reads landing raw source files and writes them down into immutable Bronze Delta/Parquet formats."""
        logger.info(f"[Bronze Pipeline] Extracting batch raw files from landing zone: {source_path}")
        
        # Ingestão de dados transacionais brutos simulando registros de vendas
        raw_df = self.spark.read.format("json").load(source_path)
        
        # Enriquecimento técnico para governança e auditoria operacional (linhagem de dados)
        bronze_df = raw_df.withColumn("ingested_at", current_timestamp()) \
                           .withColumn("source_file_name", input_file_name())
        
        logger.info(f"[Bronze Pipeline] Persisting state to distributed Lakehouse Bronze layer: {target_bronze_path}")
        # Gravação distribuída imutável usando partição temporal técnica
        bronze_df.write.mode("append").partitionBy("ingested_at").parquet(target_bronze_path)
