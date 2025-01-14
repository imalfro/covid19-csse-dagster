{{
    config(
        materialized='table'
    )
}}

with extracted as (
    select
      country_dimkey,
      country_region,
      country_code,
      country_iso2,
      country_iso3
    from {{ ref('stag_country') }}
)

select *
from extracted