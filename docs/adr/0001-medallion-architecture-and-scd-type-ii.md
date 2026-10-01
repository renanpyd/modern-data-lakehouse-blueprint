# ADR 0001: Medallion Architecture and SCD Type II Strategy for Enterprise Data Lakehouse

## Context & Problem Statement
When ingesting enterprise-scale transactional data (e.g., customer profiles, retail orders, CRM data) into an analytical platform, data teams face significant challenges around data quality, consistency, and auditing. Direct queries to transacting systems risk system degradation. 

Furthermore, fields within business objects change dynamically over time (e.g., a customer changes their delivery address). Without a formal strategy to track historical states, old transactions will erroneously map to new customer properties, destroying historical audit integrity, metrics consistency (CAC, LTV), and data compliance tracks (GDPR/LGPD). We need an approach to safeguard raw ingestion layers while delivering high-performance, auditable data marts.

---

## 🇧🇷 Decisão de Arquitetura (Resumo em Português)
**Status:** Approved
**Decisão:** Adotar o padrão de **Arquitetura Medallion** processado de forma distribuída via Apache Spark (PySpark), acoplado ao modelo dimensional **SCD Tipo II (Slowly Changing Dimensions)** na camada Silver.

1. **Camadas Medallion (Desacoplamento Técnico):**
   * **Bronze:** Ingestão bruta e imutável dos dados de origem (ERP, CRM) salvos no formato Delta/Iceberg, preservando o histórico de extração sem transformações.
   * **Silver:** Camada de conformidade e qualidade. É aqui que aplicaremos deduplicação, limpeza de esquemas e a lógica de **SCD Tipo II** (usando colunas de controle como `start_date`, `end_date` e `is_current`) para rastrear cada mudança histórica de atributos de entidades críticas.
   * **Gold:** Modelagem dimensional analítica (tabelas de Fatos e Dimensões seguindo Kimball) consolidada e otimizada para consultas de BI e consumo corporativo.

### Consequências
* **Impacto Positivo:** Rastreabilidade e auditabilidade total do histórico dos dados, isolamento completo entre dados brutos e analíticos, consistência matemática para relatórios de longo prazo (Churn, LTV) e conformidade facilitada com a LGPD.
* **Impacto Negativo:** Aumento no volume de armazenamento de dados devido à persistência de registros históricos e lógica mais elaborada no desenvolvimento dos jobs do Spark.

---

## 🇺🇸 Architectural Decision (English Summary)
**Status:** Approved
**Decision:** Standardize storage layers on the **Medallion Architecture** using distributed Apache Spark (PySpark) engines, implementing **SCD Type II (Slowly Changing Dimensions)** parsing mechanics within the Silver operational layer.

1. **Medallion Layers (Technical Decoupling):**
   * **Bronze:** Immutable raw storage ingestion layer preserving raw application state logs in highly compressed Delta/Iceberg structures.
   * **Silver:** Cleanse, conform, and deduplicate datasets. This layer houses the core **SCD Type II** logic, adding deterministic analytical metadata controls (`start_date`, `end_date`, `is_current`) to capture every mutation event on critical dimension fields without losing baseline transaction states.
   * **Gold:** Production Kimball dimensional marts (Facts and Dimensions) tuned for sub-second business aggregation queries, corporate BI serving, and downstream machine learning usage.

### Consequences
* **Positive Impact:** Full audit capability for any temporal state, reliable computation bounds for strategic historic metrics (LTV, Churn cycles), and structural data security alignment with GDPR/LGPD compliance.
* **Impacto Negativo:** Expanded storage overhead required to retain multi-version records and higher logic complexity inside distributed Spark transformation logic.
