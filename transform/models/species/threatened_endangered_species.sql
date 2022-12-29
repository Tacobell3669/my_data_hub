{{
  config(
    materialized='table',
    tags=['species_data', 'threatened', 'endangered']
  )
}}

with dated as (
    select * from fws_species_data
    where "ESA Listing Date" != ''
)

, threatened_endangered as (
    select "Common Name",
           "Scientific Name",
           "ESA Listing Status",
           "ESA Listing Date"::date,
           "Current Range Combined States" as states_found
    from dated where "ESA Listing Status" = 'Threatened' or "ESA Listing Status" = 'Endangered'
)

select * from threatened_endangered
