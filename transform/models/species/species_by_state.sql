{{
  config(
    materialized='table',
    tags=['species_data', 'threatened', 'endangered', 'extinct', 'by_state']
  )
}}

with src_species as (
    select * from {{ref('threatened_endangered_extinct_species')}}
)

, just_states as (
    select *,
           string_to_array(states_found, ', ') as states
    from src_species
)

, denest as (
    select common_name,
           scientific_name,
           esa_listing_status,
           esa_listing_date,
           unnest(states) as state
    from just_states
)

select * from denest
