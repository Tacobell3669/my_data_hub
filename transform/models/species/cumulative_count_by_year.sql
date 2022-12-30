{{
  config(
    materialized='table',
    tags=['species_data', 'cumulative_count', 'by_year']
  )
}}

with src_species_by_state as (
    select * from {{ref('species_by_state')}}
)

, with_year as (
    select *, extract(YEAR from esa_listing_date) as listing_year from src_species_by_state
)

, state_count_by_year as (
  select
    count(*) as listing_count,
    listing_year
  from with_year group by listing_year
)

, cumulative_count_by_year as (
  select
    listing_year,
    sum(listing_count) over (order by listing_year) as cumulative_count
  from state_count_by_year
  order by listing_year asc
)

select * from cumulative_count_by_year
