with base as (
  select 
    date_part('year', "date") as year,
    dc2.country_region,
    sum(
      case when dc.case_type = 'confirmed' then case_count else 0 end
    ) as confirmed_case_count,
    sum(
      case when dc.case_type = 'deaths' then case_count else 0 end
    ) as death_case_count,
    sum(
      case when dc.case_type = 'recovered' then case_count else 0 end
    ) as recovered_case_count
  from {{ ref('fact_covid_cases' )}} fc
  left join {{ ref('dim_cases' )}} dc
  on fc.case_dimkey = dc.case_dimkey
  left join  {{ ref('dim_country' )}} dc2
  on fc.country_dimkey = dc2.country_dimkey 
  group by 1,2
),

sorted as (
  select 
    "year",
    country_region,
    confirmed_case_count,
    death_case_count,
    recovered_case_count,
    row_number() over(partition by country_region order by confirmed_case_count desc) rn,
    row_number() over(partition by country_region order by death_case_count desc) rn_death,
    row_number() over(partition by country_region order by recovered_case_count desc) rn_recovery
  from base
),

--biggest year cases in country
peak_cases as (
  select *
  from sorted
  where rn = 1
),

--sentiment increase/decrease confirmed
sentiment_confirmed as (
  select 
    s1."year",
    s1.country_region,
    case when s2.rn > s1.rn then 'increasing from last year'
    when s2.rn is null then 'first year reported cases'
    else 'decreasing' end as sentiment
  from sorted s1
  left join sorted s2
  on s2."year" = s1."year" - 1
  and s1.country_region = s2.country_region
),

--sentiment increase/decrease death and recovery
sentiment_death_recovery as (
  select 
    s1."year",
    s1.country_region,
    case when s2.rn_death > s1.rn_death then 'increasing from last year'
    when s2.rn_death is null then 'first year reported cases'
    else 'decreasing' end as sentiment_death,
    case when s2.rn_recovery > s1.rn_recovery then 'increasing from last year'
    when s2.rn_recovery is null then 'first year reported cases'
    else 'decreasing' end as sentiment_recovery
  from sorted s1
  left join sorted s2
  on s2."year" = s1."year" - 1
  and s1.country_region = s2.country_region
)

--change from {table} to whichever cte part to analyze
select *
from sentiment_death_recovery