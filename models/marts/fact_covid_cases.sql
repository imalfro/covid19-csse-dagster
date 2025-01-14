{{
    config(
        materialized='table'
    )
}}

with final as (
    select 
      e.covid_cases_factkey,
      country_dimkey,
      states_dimkey,
      case_dimkey,
      "date",
      e.case_count
    from {{ ref('int_fact_covid_cases') }} e
)

select *
from final