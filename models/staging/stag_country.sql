{{
    config(
        materialized='table'
    )
}}

with extracted as (
    select distinct
      country_region,
      code3 as country_code,
      iso2 as country_iso2,
      iso3 as country_iso3
    from
      {{ source('csse', 'lookup') }}
),

final as (
    select 
      {{ dbt_utils.generate_surrogate_key(['country_code','country_region']) }} as country_dimkey,
      country_region,
      country_code,
      country_iso2,
      country_iso3
    from
      extracted    
)

select
    *
from
    final