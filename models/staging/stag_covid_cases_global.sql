{{
    config(
        materialized='table'
    )
}}

with extracted as (
    select
      TO_DATE("date", 'MM/DD/YY') as "date",
      province_state,
      country_region,
      case_type,
      cast(regexp_replace(cases, '[^0-9]+', '', 'g')  as integer) as case_count
    from
        {{ source('csse', 'timeseries_global') }}
),

enriched as (
    select
      {{ dbt_utils.generate_surrogate_key(['date','province_state','country_region','case_type']) }} as covidcases_global_key,
      "date",
      province_state,
      country_region,
      case_type,
      case_count
    from
        extracted    
),

dedup as (
    select
      covidcases_global_key,
      "date",
      province_state,
      country_region,
      case_type,
      case_count,
      row_number() over(partition by covidcases_global_key order by case_count desc) rn
    from
        enriched    
),

final as (
    select
      covidcases_global_key,
      "date",
      province_state,
      country_region,
      case_type,
      case_count
    from
        dedup    
    where rn = 1
)

select
    *
from
    final