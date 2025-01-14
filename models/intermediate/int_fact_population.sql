{{
    config(
        materialized='table'
    )
}}

with extracted as (
    select
      population_key,
      province_state,
      country_region,
      combined_key,
      country_code,
      country_iso2,
      country_iso3,
      "population"
    from {{ ref('stag_population') }}
),

enriched as (
    select
      e.population_key,
      c.country_dimkey,
      s.states_dimkey,
      "population"
    from extracted e
    join {{ ref('int_dim_country') }} c 
    on e.country_region = c.country_region
    left join {{ ref('int_dim_states') }} s
    on e.combined_key = s.combined_key
)

select *
from enriched