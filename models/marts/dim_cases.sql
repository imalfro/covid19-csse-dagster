{{
    config(
        materialized='table'
    )
}}

with final as (
    select
      case_dimkey,
      case_type
    from {{ ref('int_dim_cases') }}
)

select *
from final