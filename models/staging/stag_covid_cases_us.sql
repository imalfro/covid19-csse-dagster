{{
    config(
        materialized='table'
    )
}}

with extracted as (
    select
      TO_DATE("date", 'MM/DD/YY') as "date",
      cast("uid" as integer) as unique_id,
      combined_key,
      province_state,
      country_region,
      code3 as country_code,
      case_type,
      cast(regexp_replace(cases, '[^0-9]+', '', 'g')  as integer) as case_count
    from
        {{ source('csse', 'timeseries_us') }}
),

enriched as (
    select
      {{ dbt_utils.generate_surrogate_key(['combined_key','date','case_type']) }} as covidcases_us_key,
      "date",
      combined_key,
      province_state,
      country_region,
      country_code,
      case_type,
      case_count
    from
        extracted    
),

dedup as (
    select
      covidcases_us_key,
      "date",
      combined_key,
      province_state,
      country_region,
      country_code,
      case_type,
      case_count,
      row_number() over(partition by covidcases_us_key order by case_count desc) rn
    from
        enriched    
),

final as (
    select
      covidcases_us_key,
      "date",
      combined_key,
      province_state,
      country_region,
      country_code,
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