import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('flights.csv')
print(df.head(10))

# Print information about the dataframe.
print(df.info())

# Check for null values in the dataframe.
print(df.isnull().sum())

print(df.describe())
print(df.describe().round(2)) # To get it out of scientific notation.

# Note that the describe() method only returns summary statistics for numerical columns.
# Even with numerical columns, interpretation is key here. Some of these statistics don't 
# really make sense given the nature of the data.
# How might we start to get a sense for our categorical data? Such as the names of airports and cities?
# One way is to use the value_counts() method to get a count of the unique values in a column.
print(df['Origin'].value_counts())

# We can also use the unique() and nunique() methods to get the unique values and the number of unique values respectively.
print(df['Origin'].unique())
print(df['Origin'].nunique())

# FILTERING DATA

# Scenario 1: Extract records for flights in the year 2000
df['Year'] = df['Fly Date'].astype(str).str.slice(0, 4).astype(int) # Adding a new column 'Year' to the dataframe.
flights_in_2000 = df[df['Year'] == 2000]

print(flights_in_2000.head(3))

# Scenario 2: Find flights that do not include 'LAX' as an origin
non_lax_flights = df[~df['Origin'].isin(['LAX'])]
print(non_lax_flights.head(3))
# Check that LAX is not in the list of origins.
print(non_lax_flights['Origin'].unique())

# Scenario 3: Filter data to include only flights with more than 100 passengers and less than 1000 miles in distance
flights_by_passenger_and_distance = df[(df['Passengers'] > 100) & (df['Distance'] < 1000)]
print(flights_by_passenger_and_distance.head(3))

# Scenario 4: Filter for flights to or from either 'New York' or 'Los Angeles' using string methods
popular_city_flights = df[df['Origin City'].str.contains('New York|Los Angeles') | 
                           df['Destination City'].str.contains('New York|Los Angeles')]
print(popular_city_flights.head(3))

# Scenario 5: Use the query method to filter flights where the number of seats is greater than the number of passengers
underbooked_flights = df.query('Seats > Passengers')
print(underbooked_flights.head(3))

# Scenario 6: Select flights that have an origin population of over 1 million people
large_origin_population_flights = df[df['Origin Population'] > 1_000_000]
print(large_origin_population_flights.head(3))

# Scenario 7: Find flights that are short-haul (distance less than 500 miles) and very busy (more than 10 flights)
short_haul_busy_flights = df[(df['Distance'] < 500) & (df['Flights'] > 10)]
print(short_haul_busy_flights.head(3))

#3. GROUPING DATA AND AGGREGATING RESULTS

# Scenario 1: Group by Origin and Destination to identify busiest routes.
busiest_routes = df.groupby(['Origin', 'Destination']).agg({'Passengers': 'sum'}).reset_index()
busiest_routes = busiest_routes.sort_values(by='Passengers', ascending=False)  # Sorting to find the busiest routes

# Scenario 2: Group by Fly Date to see the monthly trend of flights.
df['YearMonth'] = pd.to_datetime(df['Fly Date'], format='%Y%m').dt.to_period('M')
monthly_trends = df.groupby('YearMonth').agg({'Flights': 'sum'}).reset_index()
monthly_trends = monthly_trends.sort_values(by='YearMonth')  # Sorting to see the trend over time

# Scenario 3: Calculate total passengers and flights for each route.
route_summary = df.groupby(['Origin', 'Destination']).agg({'Passengers': 'sum', 'Flights': 'sum'}).reset_index()
route_summary = route_summary.sort_values(by=['Passengers', 'Flights'], ascending=[False, False])

# Scenario 4: Group by Origin to Identify Top Departure Airports
departure_traffic = df.groupby('Origin').agg({'Flights': 'sum'}).reset_index()
departure_traffic = departure_traffic.sort_values(by='Flights', ascending=False)

# Scenario 5: Group by Destination City to Explore Inbound Passenger Volumes
inbound_passengers = df.groupby('Destination City').agg({'Passengers': 'sum'}).reset_index()
inbound_passengers = inbound_passengers.sort_values(by='Passengers', ascending=False)

# Scenario 6: Group by Distance to Analyze Flight Volume by Distance Traveled
distance_bins = pd.cut(df['Distance'], bins=[0, 500, 1000, 2000, 3000, 4000, df['Distance'].max()])
distance_grouping = df.groupby(distance_bins).agg({'Flights': 'count', 'Passengers': 'sum'}).reset_index()
distance_grouping = distance_grouping.sort_values(by='Distance')

# 4. VISUALIZING DATA
# BAR CHARTS
# Set a style for the plots
plt.style.use('ggplot')
# Increase default figure and font sizes for easier viewing
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 14

# 1. Bar Chart for Top 10 Busiest Airports
# Aggregating data to find the busiest airports by summing up the number of flights that originate from each airport
# Note: This considers only outgoing flights. You could also include incoming flights or use passengers for a different measure.
busiest_airports = df.groupby('Origin').agg({'Flights': 'sum'}).nlargest(10, 'Flights')
# Plotting the result
busiest_airports.plot(kind='bar', legend=False)
plt.title('Top 10 Busiest Airports by Number of Outgoing Flights')
plt.xlabel('Airport')
plt.ylabel('Number of Outgoing Flights')
plt.xticks(rotation=45)  # Rotate x-axis labels to show them more clearly
plt.tight_layout()  # Adjust layout to fit everything nicely
plt.show()

# 2. Bar Chart for Top 10 Busiest Routes
busiest_routes = df.groupby(['Origin', 'Destination']).agg({'Flights': 'sum'}).nlargest(10, 'Flights')
busiest_routes.plot(kind='bar', legend=False, color='darkblue')
plt.title('Top 10 Busiest Routes by Number of Flights')
plt.xlabel('Route')
plt.ylabel('Number of Flights')
plt.xticks(rotation=45)  # Rotate x-axis labels to show them more clearly
plt.tight_layout()  # Adjust layout to fit everything nicely
plt.show()

# 3. Bar chart showing the top 10 routes by passenger numbers.
busiest_routes_by_passengers = df.groupby(['Origin', 'Destination']).agg({'Passengers': 'sum'}).nlargest(10, 'Passengers')
busiest_routes_by_passengers.plot(kind='bar', legend=False)
plt.title('Top 10 Busiest Routes by Number of Passengers')
plt.xlabel('Route')
plt.ylabel('Number of Passengers')
plt.xticks(rotation=45)  # Rotate x-axis labels to show them more clearly
plt.tight_layout()  # Adjust layout to fit everything nicely
plt.show()

# LINE PLOTS
df['Year'] = df['Year'].astype(str) # Converting 'Year' to string to avoid floating point years in the plot
year_groups = df.groupby('Year')
year_groups.agg({'Flights': 'sum'}).plot(kind='line', legend=False)
plt.title('Total Number of Flights per Year')
plt.xlabel('Year')
plt.ylabel('Number of Flights')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# But notice that the years are being displayed as floating points. Not what we want.
# We can fix this by converting the 'Year' column to a string before grouping. (See above)
# Now let's see the same data but for number of passengers.
year_groups.agg({'Passengers': 'sum'}).plot(kind='line', legend=False)
plt.title('Total Number of Passengers per Year')
plt.xlabel('Year')
plt.ylabel('Number of Passengers')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# We can also plot mutliple lines on the same plot.
year_groups.agg({'Flights': 'sum', 'Passengers': 'sum'}).plot(kind='line')
plt.title('Total Number of Flights and Passengers per Year')
plt.xlabel('Year')
plt.ylabel('Number of Flights/Passengers')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# PIE CHARTS
# Create a pie chart that shows the distribution of flights by distance buckets.
# First we need to create the distance buckets
distance_bins = pd.cut(df['Distance'], bins=[0, 500, 1000, 2000, 3000, 4000, df['Distance'].max()])
# Then, we group by the distance bins and aggregate by the number of flights
distance_groups = df.groupby(distance_bins).agg({'Flights': 'count'})
# Finally, we can make our pie chart.
distance_groups.plot(kind='pie', y='Flights', legend=False)
plt.title('Distribution of Flights by Distance')
plt.tight_layout()
plt.show()

# The aesthetics aren't the best, but it gets the job done.
# Create a pie chart that shows the distribution of passengers by route (in the top 50 routes by passenger numbers).
# First let's prepare the data. We need to find the top 50 routes by passsenger numbers.
# We can do this by grouping by origin and destination, aggregating by passengers, and then sorting.
top_50_routes = df.groupby(['Origin', 'Destination']).agg({'Passengers': 'sum'}).nlargest(50, 'Passengers')

# Then we can create our pie chart
top_50_routes.plot(kind='pie', y='Passengers', legend=False)
plt.title('Distribution of Passengers by Route')
plt.tight_layout()
plt.show()
# Finally, let's create a pie chart to show the distribution of flights by month.
# First we need to extract months from the 'Fly Date' column.
df['Month'] = df['Fly Date'].astype(str).str.slice(4, 6).astype(int)
# Then we can group by month and aggregate by the number of flights.
month_groups = df.groupby('Month').agg({'Flights': 'count'})
# And finally, we can create our pie chart.
month_groups.plot(kind='pie', y='Flights', legend=False)
plt.title('Distribution of Flights by Month')
plt.tight_layout()
plt.show()

# SCATTER PLOTS
# Scatter plots are useful for visualizing the relationship between two numerical variables.
# They can help us identify correlations and outliers in our data.
# Let's make a scatter plot of routes by distance and number of passengers.
# First, we need to group by origin and destination and aggregate by distance and passengers.
route_groups = df.groupby(['Origin', 'Destination']).agg({'Distance': 'mean', 'Passengers': 'sum'})
# Then we can create our scatter plot.
route_groups.plot(kind='scatter', x='Distance', y='Passengers')
plt.title('Number of Passengers by Distance')
plt.xlabel('Distance')
plt.ylabel('Number of Passengers')
plt.tight_layout()
plt.show()

# HISTOGRAMS
# We can get another perspective on this distribution of distances by plotting a histogram.
# Histograms are useful for visualizing the distribution of a single numerical variable.
# They can help us identify outliers and understand the shape of the data.
# Let's plot a histogram of the distribution of distances.
df['Distance'].plot(kind='hist')
plt.title('Distribution of Distances')
plt.xlabel('Distance')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Correlating city populations with flights and passengers
df['Total City Population'] = df['Origin Population'] + df['Destination Population']
city_populations = df.groupby(['Origin', 'Destination', 'Year']).agg({'Passengers': 'sum', 'Total City Population': 'sum'}).reset_index().sort_values(by='Year')
# Now we can plot the relationship between city population and number of passengers.
city_populations.plot(kind='scatter', x='Total City Population', y='Passengers')
plt.title('Number of Passengers by Total City Population')
plt.xlabel('Total City Population')
plt.ylabel('Number of Passengers')
plt.tight_layout()
plt.show()
