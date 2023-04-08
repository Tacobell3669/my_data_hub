import json
import geojson
import plotly.express as px
import plotly.offline as po
import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd
import itertools

load_dotenv()

# Open the US states JSON file
with open("../../data/us-states.json", "r") as f:
  us_states = json.load(f)

# Create a GeoJSON object
geojson_us_states = geojson.FeatureCollection(us_states)

warehouse_url = os.environ["WAREHOUSE_URL"]
conn = psycopg2.connect(warehouse_url)
cur = conn.cursor()

# Execute a SQL query to retrieve the data
cur.execute("select state, cumulative_count, listing_year from \
            analytics.cumulative_count_by_state order by listing_year;")

counts_over_time = cur.fetchall()
counts_over_time_df = pd.DataFrame(counts_over_time, columns=['state', 'species_listing_count', 'listing_year'])

state_codes = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MP': 'Norther Mariana Islands',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'PW': 'Palau',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VI': 'Virgin Islands',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
}

# Map the two-character codes to the full names of the states
counts_over_time_df['state_code'] = counts_over_time_df['state']

# Transform the count data into a format that can be used by Chloropleth
counts_over_time_df['species_listing_count'] = counts_over_time_df['species_listing_count'].astype(float)
counts_over_time_df['listing_year'] = counts_over_time_df['listing_year'].astype(str)
counts_over_time_df.drop('state', axis=1, inplace=True)

# Create full data set of all states and all years
years = pd.date_range(start='1967', end='2023', freq='Y')
years = years.strftime('%Y')
state_codes = counts_over_time_df['state_code'].unique()
combinations = list(itertools.product(state_codes, years))

# Combine existing DataFrame with the combined list of state codes and years
df_new = pd.DataFrame(combinations, columns=['state_code', 'listing_year'])
df_new = pd.merge(df_new, counts_over_time_df, how='outer', left_on=['state_code', 'listing_year'],
right_on=['state_code', 'listing_year'])
df_new['species_listing_count'] = df_new.groupby(['state_code'])['species_listing_count'].fillna(method='ffill')

# Create an animated Chloropleth map using Plotly and the dataframe we made
over_time_fig = px.choropleth(df_new, geojson=geojson_us_states, locations='state_code',
                    locationmode="USA-states", color='species_listing_count', title='State Species Listing Counts - 2020',
                    color_continuous_scale='Viridis_r', scope='usa', range_color=(0,500), labels={'species_listing_count':'# of species listed'},
                    animation_frame='listing_year')

# Write the Choropleth map to an HTML file to be used in the data report
po.plot(over_time_fig, filename='species_map.html')
