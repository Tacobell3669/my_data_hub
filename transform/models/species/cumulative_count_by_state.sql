{{
  config(
    materialized='table',
    tags=['species_data', 'cumulative_count', 'by_state']
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
    listing_year,
    state
  from with_year group by state, listing_year
)

, cumulative_count_by_state as (
  select
    state,
    listing_year,
    sum(listing_count) over (partition by state order by listing_year) as cumulative_count
  from state_count_by_year
  order by state, listing_year asc
)

select * from cumulative_count_by_state
