{{
    config(
        materialized='table'
    )
}}

with extracted as (
    select distinct
      cast("uid" as integer) as unique_id,
      combined_key,
      province_state,
      country_region,
      cast(fips as integer) fips,
      admin2 as county_administrator,
      cast(longx as numeric(12,8)) as longx,
      cast(lat as numeric(12,8)) as lat
    from
        {{ source('csse', 'lookup') }}
),

final as (
    select
      {{ dbt_utils.generate_surrogate_key(['combined_key', 'province_state','country_region']) }} as states_dimkey,
      unique_id,
      combined_key,
      province_state,
      country_region,
      fips,
      county_administrator,
      longx,
      lat
    from
        extracted    
)

select
    *
from
    final