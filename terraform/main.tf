provider "aws" {
  region = var.aws_region
}

# Configuração do Bucket centralizado do Data Lakehouse
resource "aws_s3_bucket" "lakehouse_bucket" {
  bucket        = "enterprise-modern-lakehouse-${var.environment}"
  force_destroy = true

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = "ModernDataLakehouse"
  }
}

# Habilita o versionamento de objetos para segurança operacional de metadados
resource "aws_s3_bucket_versioning" "lakehouse_versioning" {
  bucket = aws_s3_bucket.lakehouse_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Bloqueia qualquer acesso público acidental, garantindo conformidade regulatória
resource "aws_s3_bucket_public_access_block" "lakehouse_public_block" {
  bucket = aws_s3_bucket.lakehouse_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Estruturação programática das três camadas lógicas lidas pelo Spark
resource "aws_s3_object" "bronze_folder" {
  bucket = aws_s3_bucket.lakehouse_bucket.id
  key    = "bronze/"
}

resource "aws_s3_object" "silver_folder" {
  bucket = aws_s3_bucket.lakehouse_bucket.id
  key    = "silver/"
}

resource "aws_s3_object" "gold_folder" {
  bucket = aws_s3_bucket.lakehouse_bucket.id
  key    = "gold/"
}
