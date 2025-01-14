{{
    config(
        materialized='table'
    )
}}

with extracted as (
    select distinct
      case_type
    from {{ ref('int_covid_cases') }}
),

final as (
    select 
      {{ dbt_utils.generate_surrogate_key(['case_type']) }} case_dimkey,
      case_type
    from extracted e
)

select *
from final