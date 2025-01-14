{{
    config(
        materialized='table'
    )
}}

with final as (
    select 
      population_key,
      country_dimkey,
      states_dimkey,
      "population"
    from {{ ref('int_fact_population') }} 
)

select *
from final