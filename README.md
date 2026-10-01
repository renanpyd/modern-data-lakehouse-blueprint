# Modern Enterprise Data Lakehouse Blueprint

---

## 🇧🇷 Visão Geral do Projeto
Este repositório apresenta um **Blueprint de nível Enterprise** focado no desenho e implementação de uma plataforma moderna de dados baseada em arquiteturas **Data Lakehouse** e **Data Mesh**. O ecossistema demonstra cenários reais de ingestão, transformação distribuída de alta escala e governança corporativa em conformidade rígida com a LGPD/GDPR.

O ecossistema foi estruturado sob três pilares de engenharia avançada:
1. **Processamento Distribuído e Arquitetura Medallion:** Pipelines automatizados em **PySpark** manipulando dados complexos oriundos de sistemas transacionais e organizando-os de forma desacoplada nas camadas **Bronze** (dados brutos), **Silver** (dados limpos, enriquecidos e com versionamento histórico via modelagem Kimball SCD Tipo II) e **Gold** (agregados analíticos prontos para consumo de negócios).
2. **Analytics Engineering & Data Quality Framework:** Camada de modelagem modular utilizando **dbt (Data Build Tool)** integrado a testes rigorosos e automatizados de integridade, consistência e validação de qualidade de dados corporativos a cada estágio de transformação.
3. **Infraestrutura como Código (IaC) e Governança:** Provisionamento completo de ambientes cloud isolados utilizando **Terraform**, aplicando políticas rígidas de menor privilégio (IAM) e segurança na camada de metadados.

---

## 🇺🇸 Project Overview
This repository provides an **Enterprise-grade multi-cloud architectural Blueprint** delivering high-throughput, horizontally scalable data infrastructure models based on modern **Data Lakehouse** and **Data Mesh** paradigms. The project focuses on handling enterprise analytical lifecycle patterns under strict GDPR/LGPD compliance bounds.

The structural matrix centers across three advanced engineering vectors:
1. **Massive Distributed PySpark Pipelines:** Implements transactional source abstractions utilizing Apache Spark execution grids orchestrated over a **Medallion Architecture**. Processes raw streams into **Bronze** (immutable raw ledger), **Silver** (conformed, validated data with historic audit via Kimball SCD Type II modeling), and **Gold** (high-performance analytics marts).
2. **Analytics Engineering & Quality Gates:** Implements advanced semantic abstractions via **dbt (Data Build Tool)** coupled with deterministic data testing validations, automated continuous metadata lineage tracking, and constraint verification layers.
3. **Infrastructure as Code (IaC) & Platform Security:** Multi-cloud infrastructure blueprints provisioned natively through **Terraform** executing least-privilege security matrices (IAM) to protect downstream catalog metadata layers.

---

## 📂 Architecture & Directory Structure / Estrutura de Pastas

*   `terraform/`: Declarative Infrastructure as Code (IaC) provisioning secure cloud components.
*   `src/pipelines/`: Distributed analytical data runtimes built with Python and PySpark (Bronze/Silver/Gold).
*   `dbt_project/`: Modular transformation models, quality constraints, and business marts definition layer.
*   `docs/adr/`: Architecture Decision Records documenting core design patterns choices.
