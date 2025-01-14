{{
    config(
        materialized='table'
    )
}}

with extract_global as (
    select 
      covidcases_us_key as covid_cases_key,
      "date",
      combined_key,
      province_state,
      country_region,
      country_code,
      case_type,
      case_count
    from {{ ref('stag_covid_cases_us') }}
),

extract_us as (
    select 
      covidcases_global_key as covid_cases_key,
      "date",
      case when province_state is not null 
      then concat(province_state,', ',country_region) 
      else country_region end as combined_key,
      province_state,
      country_region,
      null country_code,
      case_type,
      case_count
    from {{ ref('stag_covid_cases_global') }}
),

final as (
    select 
      *
    from extract_global e
    UNION ALL
    select 
      *
    from extract_us e
)

select *
from final