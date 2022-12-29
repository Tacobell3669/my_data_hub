# Welcome to Evidence! 👋
Build a polished business intelligence system using only SQL & Markdown.

# Write Markdown
Evidence creates pages from markdown files. The file for this page is:

`[my-project]/pages/index.md`.

👉 Open this file, change some text and save it to see this page update instantly.

# Connect to a Database
👉 Connect to a database in the **Settings** menu. For this tutorial, choose a **SQLite** database and enter the filename `needful_things`. 

![Connecting a database](connect-db.gif)

# Run SQL
Write queries using markdown code fences ` ``` `:

```species_in_ga
select
  count(*) as listing_count,
  sum(count(*)) over (order by esa_listing_date) cum_total,
  esa_listing_date
from analytics.species_by_state
-- where state = 'GA'
group by esa_listing_date
order by esa_listing_date desc
```

You can see both the SQL and the query results by interacting with the query above.

👉 Edit the above query to just display Georgia data by adding:

`where state = 'GA'`

# Include Values in Text
Return values from queries in text: 

The cumulative total of listed species from GA is <Value data={species_in_ga} column=cum_total/>
as of the date: <Value data={species_in_ga} column=esa_listing_date/>.

Sometimes you need something *bigger*: 
<BigValue data={species_in_ga} value=cum_total />

# Add Charts & Components
Charts can be included in a single line of code:
<LineChart data={species_in_ga} x=esa_listing_date y=cum_total/>

# Use More Powerful Features ⚡
Evidence supports using logic & loops to determine what text and data is displayed.

<BigLink href="/powerful-features">Using Logic & Loops &rarr;</BigLink>
