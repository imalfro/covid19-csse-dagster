{{
    config(
        materialized='table'
    )
}}

with extracted as (
    select
      states_dimkey,
      unique_id,
      combined_key,
      province_state,
      country_region,
      fips,
      county_administrator,
      longx,
      lat
    from {{ ref('int_dim_states') }}
)

select *
from extracted