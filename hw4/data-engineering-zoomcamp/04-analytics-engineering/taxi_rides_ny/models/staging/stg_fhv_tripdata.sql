{{ config(materialized='view') }}

select
    dispatching_base_num,
    pickup_datetime,
    dropoff_datetime,
    pulocationid,
    dolocationid,
    sr_flag
from {{ source('raw', 'fhv_tripdata') }}