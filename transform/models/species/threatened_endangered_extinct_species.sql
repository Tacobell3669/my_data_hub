{{
  config(
    materialized='table',
    tags=['species_data', 'threatened', 'endangered', 'extinct']
  )
}}

with dated as (
    select * from {{source('public', 'fws_species_data')}}
    where "ESA Listing Date" != ''
)

, threatened_endangered_extinct as (
    select "Common Name" as common_name,
           "Scientific Name" as scientific_name,
           "ESA Listing Status" as esa_listing_status,
           "ESA Listing Date"::date as esa_listing_date,
           "Current Range Combined States" as states_found
    from dated where "ESA Listing Status" = 'Threatened' or
                     "ESA Listing Status" = 'Endangered' or
                     "ESA Listing Status" = 'Extinction'
)

select * from threatened_endangered_extinct
