{{ config(materialized='view') }}

with source_silver_data as (
    -- Simula a leitura da tabela conformada gerada pelo Spark na camada Silver
    select * 
    from {{ source('lakehouse_silver', 'silver_conformed_orders') }}
)

select
    order_id as transaction_id,
    customer_id as account_holder_id,
    amount as transactional_value_usd,
    status as order_execution_status,
    start_date as row_valid_from,
    is_current as is_active_record
from source_silver_data
where is_current = true
