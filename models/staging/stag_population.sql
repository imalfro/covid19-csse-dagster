{{
    config(
        materialized='table'
    )
}}

with extracted as (
    select
      cast("uid" as integer) as unique_id,
      province_state,
      country_region,
      combined_key,
      admin2 as county_administrator,
      code3 as country_code,
      iso2 as country_iso2,
      iso3 as country_iso3,
      cast(regexp_replace("population", '[^0-9]+', '', 'g') as bigint) as "population"
    from
      {{ source('csse', 'lookup') }}
),

final as (
    select
      {{ dbt_utils.generate_surrogate_key(['combined_key']) }} as population_key,
      county_administrator,
      province_state,
      country_region,
      combined_key,
      country_code,
      country_iso2,
      country_iso3,
      "population"
    from
      extracted    
)

select
    *
from
    final