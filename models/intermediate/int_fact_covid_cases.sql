{{
    config(
        materialized='table'
    )
}}

with extracted as (
    select 
      e.covid_cases_key as covid_cases_factkey,
      e.province_state,
      e.combined_key,
      e.country_region,
      e.country_code,
      e."date",
      e.case_type,
      e.case_count
    from {{ ref('int_covid_cases') }} e
),

final as (
    select 
      e.covid_cases_factkey,
      c.country_dimkey,
      s.states_dimkey,
      {{ dbt_utils.generate_surrogate_key(['case_type']) }} case_dimkey,
      "date",
      e.case_count
    from extracted e
    join {{ ref('int_dim_country') }} c 
    on e.country_region = c.country_region
    left join {{ ref('int_dim_states') }} s
    on e.combined_key = s.combined_key
)

select *
from final