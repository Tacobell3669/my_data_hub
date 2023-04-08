# How have Endangered and Threatened species grown more numerous in the US?
The following is two things: a test of how well Evidence works as an aid in writing quick and simple data reports, and a showcase of the ability of Meltano to empower a personal data project. I spent the last two days initializing my Meltano project, configuring a data extraction plugin to pull in data from the US Fish and Wildlife Service's Endangered Species Act Database, and writing data transformations and visualizations on top of that. All of this was made insanely easy by Meltano, hence me being able to pull it off with 2-3 hours time a day over two days. Anyways, on to the data!

# Here's how easy it is to display data in Evidence
Write queries using markdown code fences ` ``` `:

```species_in_ga
select
  *
from analytics.cumulative_count_by_state
where state = 'GA'
order by listing_year desc
```

You can see both the SQL and the query results by interacting with the query above.

# Include Values in Text
Return values from queries in text: 

The cumulative total of listed species from GA is <Value data={species_in_ga} column=cumulative_count/>
as of the year: <Value data={species_in_ga} column=listing_year/>.

Sometimes you need something *bigger*: 
<BigValue data={species_in_ga} value=cumulative_count />

# Add Charts & Components
Charts can be included in a single line of code:
<LineChart data={species_in_ga} x=listing_year y=cumulative_count/>

