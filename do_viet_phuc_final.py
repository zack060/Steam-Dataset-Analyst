# -*- coding: utf-8 -*-
"""Do Viet Phuc Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CMW5Kggju4t4Cy-ATbUx5Wr3wVAPhjQg

#IMPORT THE DATASET & INTRODUCTION ABOUT THE DATASET

Introduction about the dataset
"""

from google.colab import drive
drive.mount('/content/drive')

# Import Data
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.preprocessing as sdk
import matplotlib.patches as mpatches

df = pd.read_csv('/content/drive/My Drive/Final Coderschool/steam.csv')
df.info()

pd.set_option('display.max_columns', None)

"""#CLEAN DATA"""

#Create a threshold for selection of 99% of data
threshold = 1

threshold_cumsum = 99

#Convert date to date-time
df["release_date"] = pd.to_datetime(df["release_date"])

"""###CATEGORICAL ANALYSIS

####Clean the CATEGORY DATA
"""

#Count the occurrences of each category
categories = [category for category_list in df['categories'].str.split(';') for category in category_list]

category_counts = pd.Series(categories).value_counts()
category_counts

category_counts.count()

#Total number of all categories combine
total_categories_combined = len(categories)

#Get the percentage of each category
category_counts.reset_index()
category_percentage = (category_counts / total_categories_combined ) * 100

category_percentage

category_percentage_cumsum = category_percentage.cumsum()
category_percentage_cumsum

threshold_percentage_categories_cumsum = category_percentage_cumsum[category_percentage_cumsum < threshold_cumsum ]
threshold_percentage_categories_cumsum

#Group the 1% genre into the "Other" category
other_category_cumsum = category_percentage_cumsum[category_percentage_cumsum > threshold_cumsum]
other_category_cumsum

threshold_percentage_categories_cumsum.count()

"""####Group categories with close similarity with each other into 1 for better observation"""

#Create new columns
df['Online MULTI-PLAYER'] = 0
df['Local MULTI-PLAYER'] = 0
df['Single-Player'] = 0

#Group the categories

#Online Multi-Player
online_conditions = df['categories'].str.contains('Online Multi-Player|Cross-Platform Multiplayer|Online Co-op|MMO', case=False, na=False)
df.loc[online_conditions, 'Online MULTI-PLAYER'] = 1

#Local Multi-Player
local_conditions = df['categories'].str.contains('Shared/Split Screen|Stats|Co-op|Local Multi-Player|Local Co-op', case=False, na=False)
df.loc[local_conditions, 'Local MULTI-PLAYER'] = 1

#Single-player
single_conditions = df['categories'].str.contains('Single-player', case=False, na=False)
df.loc[single_conditions,'Single-Player'] = 1

#Step 3: One-hot encoding with correct column names
df_onehot = pd.get_dummies(df, columns=['Online MULTI-PLAYER', 'Local MULTI-PLAYER','Single-Player']).fillna(0)

df

"""###GENRE ANALYSIS

####GENRES column CLEAN
"""

#Extract & count all the list of genres
genres = [genres for genres_list in df['genres'].str.split(';') for genres in genres_list]

# Convert genres to a pandas Series
genres_series = pd.Series(genres)

genres_counts = genres_series.value_counts()

genres_counts

#Check for any Null OR NaN value
nan_values = genres_series.isna().sum()

null_values = genres_series.isnull().sum()

print(nan_values)

print(null_values)

genres_counts.nunique()

total_genres_combined = len(genres)
total_genres_combined

#Get percentage of each genres
genres_counts.reset_index()
genres_percentage = (genres_counts / total_genres_combined ) * 100
genres_percentage

#Get cumsum of the percentage of each genres
cumulative_percentage = genres_percentage.cumsum()
cumulative_percentage

threshold_percentage_genres_cumsum = cumulative_percentage[cumulative_percentage < threshold_cumsum]
threshold_percentage_genres_cumsum

"""After we get the percentage of each genres as well as the cumsum. We can figure out the most important genres to be included in our selection. In this case, the genres that accounted for 99% of the percentage"""

#Group the 1% genre into the "Other" category
other_genres = cumulative_percentage[cumulative_percentage > threshold_cumsum]
other_genres

#Get the amount of genres needed for the analysis
len(threshold_percentage_genres_cumsum)

"""###Create 3 new columns of Mac, Windows, Linux to better observe game supported platform"""

#See the distribution of OS platform in gaming industry

df["windows"] = df["platforms"].str.contains("windows").astype(int)
df["mac"] = df["platforms"].str.contains("mac").astype(int)
df["linux"] = df["platforms"].str.contains("linux").astype(int)

#Get the popularity of each platform
platform_popularity = df[["windows", "mac", "linux"]].sum()
platform_popularity

"""##Owner data clean"""

#Split the "owner" column into lower and upper limits
df[['Owner_Lower', 'Owner_Upper']] = df['owners'].str.split('-', expand=True).astype(float)

#Calculate "Owner_Mean" for later usage in chart drawing & Encoding for Machine-Learning
df['Owner_Mean'] = (df['Owner_Upper'] + df['Owner_Lower'])/2

df

"""###Label-Encoding "Owner" for Machine-Learning"""

from sklearn.preprocessing import LabelEncoder
df['Owner_encoded'] = LabelEncoder().fit_transform(df['Owner_Mean'])

df[['owners', 'Owner_encoded']].drop_duplicates().sort_values(by=['Owner_encoded'])

print(df[['owners', 'Owner_encoded']].sort_values(by=['Owner_encoded']))

"""##Percentage of free game"""

#Identify FREE game

#Define a function to differentiate FREE & Non-free game
def categorize_price(price):
    if price == 0:
        return 0
    else:
        return 1

df['prize_category'] = df['price'].apply(categorize_price)
df

percentage_free_game = (df['prize_category'] == 0).mean() * 100
print(percentage_free_game)

"""##SORT GAME BY Required_Age

###See how much error is present within the "Required_age" column
"""

#Calculate the proportion of rows where 'required_Age' is equal to 0
proportion = (df['required_age'] == 0).mean() * 100
proportion
#~98% of the column is 0 => 98% of game has 0 required age

"""##Find how many of the games are there have English"""

english_percentages = df['english'].value_counts(normalize=True) * 100
english_percentages

"""#EDA

##Trend-Analysis : Gaming category & Trend by year

###Amount games get released by each year
"""

#Filter for the year 2019
df_2019 = df[df['release_date'].dt.year == 2019]

#Extract year and month only
unique_months_2019 = df_2019['release_date'].dt.month.unique()

# Sort the array of unique months
unique_months_2019.sort()

print(unique_months_2019)

#Select only the year within the "release_date" column
df['release_year'] = df["release_date"].dt.year

#Group by 'release_year' and count the number of games released each year
games_by_year = df['release_year'].value_counts().sort_index()

#Plotting the line chart
plt.figure(figsize=(10, 6))
plt.plot(games_by_year.index, games_by_year.values, marker='o', linestyle='-', color='b')
plt.title('Number of game released by year from 2003 to mid-2019')
plt.xlabel('Year')
plt.ylabel('Number of game released')
plt.grid(True)
plt.show()

games_by_year

# Calculate the growth rate for each year
games_by_year_growth = games_by_year.pct_change() * 100

# Calculate the average growth rate
average_growth_rate = games_by_year_growth.mean()

games_by_year_growth

average_growth_rate

"""###Amount games get released by each Month"""

#Select only the month within the "release_date" column
df['release_month'] = df["release_date"].dt.month

#Group by 'release_month' and calculate the total number of games released and the count of months
monthly_counts = df.groupby('release_month').size()
months_count = len(monthly_counts)

#Calculate the average number of games released for each month
avg_games_by_month = monthly_counts / months_count

#Plotting the line char
plt.figure(figsize=(10, 6))
plt.plot(avg_games_by_month.index, avg_games_by_month.values, marker='o', linestyle='-', color='b')
plt.title('Average number of game released each month')
plt.xlabel('Month')
plt.ylabel('Average number of game released')
plt.grid(True)
plt.show()


avg_games_by_month

"""###Distribution of games by platform"""

Platforms_count = df[df["platforms"].str.contains("windows")]['platforms'].value_counts()
Platforms_count

# Calculate the percentage of each platform
platforms_percentage = (Platforms_count / df.shape[0]) * 100

platforms_percentage

from matplotlib_venn import venn3

#Calculate the sizes of different intersections and individual sets
windows_size = (df["platforms"] == 'windows').sum()
mac_size = (df["platforms"] == 'mac').sum()
linux_size = (df["platforms"] == 'linux').sum()
windows_mac_size = (df["platforms"] == 'windows;mac').sum()
windows_linux_size = (df["platforms"] == 'windows;linux').sum()
mac_linux_size = (df["platforms"] == 'mac;linux').sum()
windows_mac_linux_size = (df["platforms"] == 'windows;mac;linux').sum()

# Create a Venn diagram
venn3(subsets=(windows_size, mac_size, windows_mac_size, linux_size, windows_linux_size, mac_linux_size, windows_mac_linux_size),
      set_labels=('Windows', 'Mac', 'Linux'))

# Show the plot
plt.show()

"""###Distribution of all categories after accounted for categories with close similarity to each other

####Pie chart
"""

threshold_cumsum = 99

#Count the occurrences of each category of TOP DEVELOPER
categories_market = [category for category_list in df['categories'].str.split(';') for category in category_list]

#Count all the categories of TOP DEVELOPER
category_counts_market = pd.Series(categories_market).value_counts()

#Get the TOTAL NUMBER of all categories of TOP DEVELOPER
total_categories_combined_market = len(categories_market)

category_counts_market.reset_index()

#get percentage of each categories
category_percentage_market = (category_counts_market / total_categories_combined_market ) * 100

#get cumsum
category_percentage_market_cumsum = category_percentage_market.cumsum()

# Get the categories that are within the thresholds
threshold_categories_market = category_counts_market[category_percentage_market_cumsum < threshold_cumsum]
other_category_market = category_counts_market[category_percentage_market_cumsum > threshold_cumsum]


#Single-player
single_conditions_topDev = df['categories'].str.contains('Single-player', case=False, na=False)

#Multi-player in general
multi_player_general_topDev = df['categories'].str.contains('Multi-player|Shared/Split Screen|Stats|Co-op|Local Multi-Player|Local Co-op|Steam Leaderboards|Online Multi-Player|Stats|Cross-Platform Multiplayer|Online Co-op|MMO', case=False, na=False)

# Calculate the lengths of the conditions
single_topDev = df[single_conditions_topDev].shape[0]
multi_player_general_topDev = df[multi_player_general_topDev].shape[0]

# Define the categories to filter out
filter_categories = ['Steam Leaderboards', 'Online Multi-Player', 'Stats', 'Cross-Platform Multiplayer', 'Online Co-op', 'MMO', 'Shared/Split Screen', 'Co-op', 'Local Multi-Player', 'Local Co-op', 'Single-player', 'Multi-player']

# Filter out the categories from threshold_percentage_categories_cumsum
filtered_threshold_percentage_categories_cumsum_topDev = threshold_categories_market[~threshold_categories_market.index.isin(filter_categories)]

# Create a new DataFrame
market_pie = pd.DataFrame({'count': [single_topDev, multi_player_general_topDev] + list(filtered_threshold_percentage_categories_cumsum_topDev.values)},
                      index=['Single-Player','Multi-player in general'] + list(filtered_threshold_percentage_categories_cumsum_topDev.index))


# Get the categories that are in 'other'
other_categories = other_category_market.index

# Convert categories_topDev to a pandas Series
categories_market_series = pd.Series(categories_market)

# Get the counts of these categories
other_counts = categories_market_series.isin(other_categories).value_counts()

# Sum the counts
other_sum = other_counts[True]

# Add a new row 'OTHER' to df_pie
market_pie.loc['OTHER', 'count'] = other_sum

# Calculate the percentage of each category
market_pie['percentage'] = (market_pie['count'] / market_pie['count'].sum()) * 100

# Sort df_pie by 'percentage' in ascending order
market_pie = market_pie.sort_values('percentage')

# Create the pie chart
plt.figure(figsize=(20, 10))
plt.pie(market_pie['percentage'], labels=market_pie.index, autopct='%2.1f%%', textprops={'fontsize': 10}, counterclock=False)
plt.title('Pie Chart')
plt.show()

category_counts_market

market_pie

"""####Venn Chart"""

#Overlapping of Single-player & Multi-player game - Local Multiplayer & Online Multiplayer
from matplotlib_venn import venn3

# Conditions
online_conditions_market = df['categories'].str.contains('Steam Leaderboards|Online Multi-Player|Stats|Cross-Platform Multiplayer|Online Co-op|MMO', case=False, na=False)
local_conditions_market = df['categories'].str.contains('Shared/Split Screen|Stats|Co-op|Local Multi-Player|Local Co-op', case=False, na=False)
single_conditions_market = df['categories'].str.contains('Single-player', case=False, na=False)

# Calculate the sizes of the regions
single_market =  df[single_conditions_market].shape[0]
online_market = df[online_conditions_market].shape[0]
local_market = df[local_conditions_market].shape[0]

# Calculate the intersections
single_online = (single_conditions_market & online_conditions_market).sum()
single_local = (single_conditions_market & local_conditions_market).sum()
online_local = (online_conditions_market & local_conditions_market).sum()
single_online_local = (single_conditions_market & online_conditions_market & local_conditions_market).sum()

# Create the Venn diagram
venn3(subsets=(single_market, online_market, single_online, local_market, single_local, online_local, single_online_local),
      set_labels=('Single-player', 'Online Multiplayer', 'Local Multiplayer'))

plt.show()

"""From the Venn diagram, we can conclude that MULTIPLAYER game can either has Single, Online, Local Multiplayer OR only has Local & Online Multiplayer

###ANALYZE the distribution of GENRES

####Pie chart genres distribution
"""

other_genres_index = other_genres.index

#Create a new DataFrame for combined counts
genres_counts_combined = genres_counts.copy()

#Assign the sum of genres that are in other_genres_index into a new "Other" category
genres_counts_combined.loc["OTHER"] = genres_counts_combined.loc[other_genres_index].sum()

#Drop genres that are now part of "OTHER" category
genres_counts_combined = genres_counts_combined.drop(other_genres_index)

# Set the figure size
plt.figure(figsize=(15, 10))

#Create a pie chart with automatic labels
plt.pie(genres_counts_combined, labels=genres_counts_combined.index, autopct='%0.1f%%')

#Display the pie chart
plt.show()

genres_counts_combined.sum()

"""####Stacked Bar Chart genres trend over the year"""

#Specifying the color for the bar chart
custom_colors = sns.color_palette('husl', 15)

#Calculate the total count of all genres
count_genres = genres_counts.sum()

#Filter out genres above the threshold
filtered_genres = genres_counts[genres_counts / count_genres * 100 >= threshold].index

#Filter the DataFrame to include only the desired genres
df_filtered = df[df['genres'].isin(filtered_genres)]

# Add a filter for the release year
df_filtered = df_filtered[df_filtered['release_year'] >= 2006]

#Group by release_date and genres to get counts
genres_counts_over_time = df_filtered.groupby(['release_year', 'genres']).size().unstack()

genres_counts_over_time.plot.bar(stacked=True, color=custom_colors, figsize=(10, 7))

plt.legend(title='genres', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xlabel("release_year")

# Calculate the total count of genres for each release year
total_counts_per_year = genres_counts_over_time.sum(axis=1)

#Normalize the data then convert to percentage
genres_percentage_over_time = genres_counts_over_time.divide(total_counts_per_year, axis=0) * 100

# Plot the bar chart
genres_percentage_over_time.plot.bar(stacked=True, color=custom_colors)

plt.legend(title='Genres', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xlabel("Release Year")
plt.ylabel("Percentage")
plt.title("Normalized Genres Distribution Over Time")

"""###Line chart to analyze price trend over years"""

# get the AVERAGE PRICE by year
average_price_by_year = df.groupby('release_year')['price'].mean()

average_price_by_year.plot(figsize=(10, 7))
plt.title('Average price by year')
plt.xlabel('Year')
plt.ylabel('Price')
plt.grid(True)
plt.show()

average_price_by_year

average_price = df['price'].mean()
average_price_by_year

# Get the MEDIAN PRICE by year
median_price_by_year = df.groupby('release_year')['price'].median()

median_price_by_year.plot(figsize=(10, 7))
plt.title('Median price by year')
plt.xlabel('Year')
plt.ylabel('Price')
plt.grid(True)
plt.show()

"""###Positive rating trend"""

df["positive_negative_ratio"] = df["positive_ratings"] / ( df["negative_ratings"] + df["positive_ratings"] ) * 100

positive_ratio_yearly = df.groupby('release_year')['positive_negative_ratio'].mean()

positive_ratio_yearly.plot(figsize=(10,7))
plt.title('Positive-Negative rating ratio by Year')
plt.xlabel('Year')
plt.ylabel('Positive-Negative rating ratio')
plt.grid(True)
plt.show()

"""##ANALYZE THE DATA ABOUT THE TOP DEVELOPER

#####Find top 3 developer in term of 'Positive rating' by year & compared them with the rest
"""

#Group by 'year' and 'developer', calculate sum of 'positive_ratings'
grouped = df.groupby(['release_year', 'developer'])['positive_ratings'].sum().reset_index()

#For each year, select top 3 developers based on 'positive_ratings'
top_developers = grouped.groupby('release_year').apply(lambda x: x.nlargest(3, 'positive_ratings')).reset_index(drop=True)

#Create a list of top developers with year
top_developers_list = top_developers[['release_year', 'developer']].values.tolist()

#If developer-year pair is not in top developers list, replace it with 'other'
grouped['developer'] = grouped.apply(lambda row: row['developer'] if [row['release_year'], row['developer']] in top_developers_list else 'other', axis=1)

#calculate the sum of positive rating by 'year' & 'developer' of grouped & then reshape the dataframe from Long > Wide format with 'year' as index
grouped_data = grouped.groupby(['release_year', 'developer'])['positive_ratings'].sum().unstack()

# Normalize the data to create a 100% stacked bar chart
grouped_data = grouped_data.div(grouped_data.sum(axis=1), axis=0)

# Manually create a list of colors
colorss=[
    'black','dimgray','lightgray','rosybrown','lightcoral','brown','red','salmon','darkorange',
    'darkgoldenrod','gold','darkkhaki','yellow','darkolivegreen','greenyellow','palegreen',
    'darkgreen','turquoise','cyan','deepskyblue','steelblue','blue','magenta','deeppink',
    'lightpink','navy','darkviolet','mediumslateblue','sandybrown','darkslategray','azure',
    'violet','maroon','navajowhite','whitesmoke','mediumvioletred','thistle','royalblue',
    'mistyrose','darkturquoise','purple','y','aquamarine','mediumpurple','darkcyan','paleturquoise',
]

grouped_data.plot(kind='bar', stacked=True, color=colorss, figsize=(10,5))
plt.title('Positive Ratings by Year for Top Developers and Others')
plt.xlabel('Year')
plt.ylabel('Positive Ratings')
plt.legend(title='Developer', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
plt.show()

"""#####Find top 3 developer in term of 'Owner' by year using Owner_Mean"""

# Group by 'year' and 'developer', calculate sum of 'Owner_encode'
grouped_owner = df.groupby(['release_year', 'developer'])['Owner_Mean'].mean().reset_index()

# For each year, select top 3 developers based on 'Owner_encode'
top_developers_owner = grouped_owner.groupby('release_year').apply(lambda x: x.nlargest(3, 'Owner_Mean')).reset_index(drop=True)

# Create a list of top developers with year
top_developers_list_owner = top_developers_owner[['release_year', 'developer']].values.tolist()

# If developer-year pair is not in top developers list, replace it with 'other'
grouped_owner['developer'] = grouped_owner.apply(lambda row: row['developer'] if [row['release_year'], row['developer']] in top_developers_list else 'other', axis=1)

grouped_data_Owner = grouped_owner.groupby(['release_year', 'developer'])['Owner_Mean'].sum().unstack()

# Normalize the data to create a 100% stacked bar chart
grouped_data_Owner = grouped_data_Owner.div(grouped_data_Owner.sum(axis=1), axis=0)

# Manually create a list of colors
colorss=[
    'black','dimgray','lightgray','rosybrown','lightcoral','brown','red','salmon','darkorange',
    'darkgoldenrod','gold','darkkhaki','yellow','darkolivegreen','greenyellow','palegreen',
    'darkgreen','turquoise','cyan','deepskyblue','steelblue','blue','magenta','deeppink',
    'lightpink','navy','darkviolet','mediumslateblue','sandybrown','darkslategray','azure',
    'violet','maroon','navajowhite','whitesmoke','mediumvioletred','thistle','royalblue',
    'mistyrose','darkturquoise','purple','y','aquamarine','mediumpurple','darkcyan','paleturquoise',
]


grouped_data_Owner.plot(kind='bar', stacked=True, color=colorss, figsize=(10,5))
plt.title('Owner Count by Year for Top 3 Developers and Others')
plt.xlabel('release_year')
plt.ylabel('Owner Count')
plt.legend(title='Developer', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
plt.show()

"""######Find the difference between "Top 3 developer in positive rating yearly" & "top 3 developer in owner count yearly"
"""

#Convert the columns to sets
grouped_data_columns = set(grouped_data.columns)
grouped_data_Owner_columns = set(grouped_data_Owner.columns)

#Find the difference
difference = grouped_data_columns.difference(grouped_data_Owner_columns)

difference

#There is no difference between the 2 chart

"""####Price trend of TOP DEVELOPER

#####Get the trend of price of top 3 Developers yearly
"""

#Create a new dataframe based on 'df' BUT ONLY INCLUDE EVERYTHING ASSOCIATED with the top developers
include_top_dev = df[df['developer'].isin(top_developers['developer'])]

#Create a color dictionary
unique_developers = include_top_dev['developer'].unique()
colors = {developer: color for developer, color in zip(unique_developers, colorss)}

#Create a bar chart
bar = include_top_dev.plot(kind='bar', x='name', y='price', color=include_top_dev['developer'].map(colors), figsize=(30,5))

#Set x-axis label
bar.set_xlabel("Game Name")

#Change the font size of the x-axis labels
bar.tick_params(axis='x')

#Set y-axis label
bar.set_ylabel("Price")

#Create legend
patches = [mpatches.Patch(color=color, label=developer) for developer, color in colors.items()]
bar.legend(handles=patches,title='Developer', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.show()

#Average price
include_top_dev['price'].mean()

"""#####Price category of game made by top 3 developer"""

#Getting the percentage of free game made by the top 3 developer yearly in term of "positive_rating"
free_games = include_top_dev[include_top_dev['prize_category'] == 0]

#Getting the TOTAL AMOUNT OF FREE GAME made by the top 3 developer yearly in term of "positive_rating"
free_game_TopDev_counts = len(free_games)

#Getting the TOTAL AMOUNT OF GAME made by the top 3 developer yearly in term of "positive_rating"
total_games_topDev = len(include_top_dev)

#Calculate the percentage of free games
free_game_percentage = (free_game_TopDev_counts / total_games_topDev) * 100

#Create each categorical price percentage
game_TopDev_10 = include_top_dev[include_top_dev['price'] <= 10]['price'].count()

game_TopDev_20 = include_top_dev[(include_top_dev['price'] > 10) & (include_top_dev['price'] <= 20)]['price'].count()

game_TopDev_30 = include_top_dev[(include_top_dev['price'] > 20) & (include_top_dev['price'] <= 30)]['price'].count()

game_TopDev_40 = include_top_dev[(include_top_dev['price'] > 30) & (include_top_dev['price'] <= 40)]['price'].count()

game_TopDev_50 = include_top_dev[(include_top_dev['price'] >= 50) & (include_top_dev['price'] <= 50)]['price'].count()

#Calculate the percentages
free = ( free_game_TopDev_counts / total_games_topDev ) * 100
percent_game_10_topDev = (game_TopDev_10 / total_games_topDev) * 100
percent_game_20_topDev = (game_TopDev_20 / total_games_topDev) * 100
percent_game_30_topDev = (game_TopDev_30 / total_games_topDev) * 100
percent_game_40_topDev = (game_TopDev_40 / total_games_topDev) * 100
percent_game_50_topDev = (game_TopDev_50 / total_games_topDev) * 100

#Create a list of the percentages
percentages = [free, percent_game_10_topDev, percent_game_20_topDev, percent_game_30_topDev, percent_game_40_topDev, percent_game_50_topDev]

#Create a list of the price ranges
price_ranges = ['free','<=10', '<=20', '<=30', '<=40','<=50']

#Create the bar chart
plt.bar(price_ranges, percentages)

#Add a title and labels
plt.title('Percentage of games made by top 3 Developer of all years by positive rating in each price range', fontsize=9)
plt.xlabel('Price Range', fontsize=9)
plt.ylabel('Percentage of Games', fontsize=9)

#Display the chart
plt.show()

"""####Price category by percentage of the entire market"""

#Sort out free game of the dataset
free_games_market = df[df['prize_category'] == 0]

#Find the total number of free game of the dataset
free_game_counts_market = len(free_games_market)

#Find the total amount of games
total_games = len(df)

#Create each categorical price percentage
game_market_10 = df[df['price'] <= 10]['price'].count()

game_market_20 = df[(df['price'] > 10) & (df['price'] <= 20)]['price'].count()

game_market_30 = df[(df['price'] > 20) & (df['price'] <= 30)]['price'].count()

game_market_40 = df[(df['price'] > 30) & (df['price'] <= 40)]['price'].count()

game_market_50 = df[(df['price'] >= 50) & (df['price'] <= 50)]['price'].count()

# Calculate the percentages
free = ( free_game_counts_market / total_games ) * 100
percent_cost10 = (game_market_10 / total_games) * 100
percent_cost20 = (game_market_20 / total_games) * 100
percen_cost30 = (game_market_30 / total_games) * 100
percent_cost40 = (game_market_40 / total_games) * 100
percent_cost50 = (game_market_50 / total_games) * 100

# Create a list of the percentages
percentages = [free, percent_cost10, percent_cost20, percen_cost30, percent_cost40, percent_cost50]

# Create a list of the price ranges
price_ranges = ['free','<=10', '<=20', '<=30', '<=40','<=50']

# Create the bar chart
plt.bar(price_ranges, percentages)

# Add a title and labels
plt.title('Percentage of ALL Games in Each Price Range',fontsize=9)
plt.xlabel('Price Range', fontsize=9)
plt.ylabel('Percentage of Games', fontsize=9)

# Display the chart
plt.show()

"""####Pie chart Genre distribution of top developer"""

#Create a threshold to filter out game that are within the 1% ( >99% of cumsum )
threshold_cumsum = 99

#Extract the genres of the game made by topDev
genres_topDev = [genres for genres_list in include_top_dev['genres'].str.split(';') for genres in genres_list]

#Convert to series for count
genres_series_topDev = pd.Series(genres_topDev)

#Count the number for each genres
genres_counts_topDev = genres_series_topDev.value_counts()

#Count the total number of all genres combined
total_genres_topDev_combined = len(genres_topDev)

#Get the percentage
genres_percentage_topDev = (genres_counts_topDev / total_genres_topDev_combined ) * 100

#Get the cumsum percentage
genres_percentage_topDev_cumsum = genres_percentage_topDev.cumsum()

#Create a new variable that only has the genres that are within the 99%
genres_counts_topDev_combined = genres_percentage_topDev_cumsum[genres_percentage_topDev_cumsum < threshold_cumsum]

#Get a new variable that has the genres are within the 1%
other_genres_TopDev = genres_percentage_topDev_cumsum[genres_percentage_topDev_cumsum > threshold_cumsum]

other_genres_TopDev_index = other_genres_TopDev.index

#copy genres from "genres_counts_topDev" to get ALL THE GENRES
genres_counts_topDev_combined = genres_counts_topDev.copy()

#Count the total number of genres that are matched with "other_genres_TopDev_index"
genres_counts_topDev_combined.loc["OTHER"] = genres_counts_topDev_combined.loc[other_genres_TopDev_index].sum()

#Drop genres that are now part of "OTHER" category
genres_counts_topDev_combined = genres_counts_topDev_combined.drop(other_genres_TopDev_index)

# Set the figure size
plt.figure(figsize=(15, 10))

#Create a pie chart with automatic labels
plt.pie(genres_counts_topDev_combined, labels=genres_counts_topDev_combined.index, autopct='%1.1f%%')

#Display the pie chart
plt.show()

other_genres_TopDev

"""####Pie chart Categorical distribution of top developer"""

threshold_cumsum = 99

#Count the occurrences of each category of TOP DEVELOPER
categories_topDev = [category for category_list in include_top_dev['categories'].str.split(';') for category in category_list]

#Count all the categories of TOP DEVELOPER
category_counts_topDev = pd.Series(categories_topDev).value_counts()

#Get the TOTAL NUMBER of all categories of TOP DEVELOPER
total_categories_combined_topDev = len(categories_topDev)

category_counts_topDev.reset_index()

#get percentage of each categories
category_percentage_topDev = (category_counts_topDev / total_categories_combined_topDev ) * 100

#get cumsum
category_percentage_topDev_cumsum = category_percentage_topDev.cumsum()


#Get the categories that are within the threshold of cumsum
threshold_category_topDev = category_counts_topDev[category_percentage_topDev_cumsum < threshold_cumsum]
other_category_topDev = category_counts_topDev[category_percentage_topDev_cumsum > threshold_cumsum]


#Single-player
single_conditions_topDev = include_top_dev['categories'].str.contains('Single-player', case=False, na=False)

#Multi-player in general
multi_player_general_topDev = include_top_dev['categories'].str.contains('Multi-player|Shared/Split Screen|Stats|Co-op|Local Multi-Player|Local Co-op|Steam Leaderboards|Online Multi-Player|Stats|Cross-Platform Multiplayer|Online Co-op|MMO', case=False, na=False)

# Calculate the lengths of the conditions
single_topDev = include_top_dev[single_conditions_topDev].shape[0]
multi_player_general_topDev = include_top_dev[multi_player_general_topDev].shape[0]

# Define the categories to filter out
filter_categories = ['Steam Leaderboards', 'Online Multi-Player', 'Stats', 'Cross-Platform Multiplayer', 'Online Co-op', 'MMO', 'Shared/Split Screen', 'Co-op', 'Local Multi-Player', 'Local Co-op', 'Single-player', 'Multi-player']

# Filter out the categories from threshold_percentage_categories_cumsum
filtered_threshold_percentage_categories_cumsum_topDev = threshold_category_topDev[~threshold_category_topDev.index.isin(filter_categories)]

# Create a new DataFrame
topDev_pie = pd.DataFrame({'count': [single_topDev, multi_player_general_topDev] + list(filtered_threshold_percentage_categories_cumsum_topDev.values)},
                      index=['Single-Player','Multi-player in general'] + list(filtered_threshold_percentage_categories_cumsum_topDev.index))


# Get the categories that are in 'other'
other_categories = other_category_topDev.index

# Convert categories_topDev to a pandas Series
categories_topDev_series = pd.Series(categories_topDev)

# Get the counts of these categories
other_counts = categories_topDev_series.isin(other_categories).value_counts()

# Sum the counts
other_sum = other_counts[True]

# Add a new row 'OTHER' to df_pie
topDev_pie.loc['OTHER', 'count'] = other_sum

# Recalculate the percentages
topDev_pie['percentage'] = (topDev_pie['count'] / topDev_pie['count'].sum()) * 100

# Sort df_pie by 'percentage' in ascending order
topDev_pie = topDev_pie.sort_values('percentage')

# Create the pie chart
plt.figure(figsize=(20, 8))
plt.pie(topDev_pie['percentage'], labels=topDev_pie.index, autopct='%2.1f%%', textprops={'fontsize': 8}, counterclock=False)
plt.title('Pie Chart')
plt.show()

other_category_topDev = category_percentage_topDev_cumsum[category_percentage_topDev_cumsum > threshold_cumsum]
other_category_topDev

topDev_pie

category_counts_topDev

"""####Venn chart of platform distribution of the top developer"""

platform_count_topDev = include_top_dev[include_top_dev['platforms'].str.contains('windows')]['platforms'].value_counts()

platform_percentage_topDev = ( platform_count_topDev / include_top_dev.shape[0]) * 100

platform_percentage_topDev

from matplotlib_venn import venn3

#Calculate the sizes of different intersections and individual sets
windows_size_topDev = (include_top_dev["platforms"] == 'windows').sum()
mac_size_topDev = (include_top_dev["platforms"] == 'mac').sum()
linux_size_topDev = (include_top_dev["platforms"] == 'linux').sum()
windows_mac_size_topDev = (include_top_dev["platforms"] == 'windows;mac').sum()
windows_linux_size_topDev = (include_top_dev["platforms"] == 'windows;linux').sum()
mac_linux_size_topDev = (include_top_dev["platforms"] == 'mac;linux').sum()
windows_mac_linux_size_topDev = (include_top_dev["platforms"] == 'windows;mac;linux').sum()

# Create a Venn diagram
venn3(subsets=(windows_size_topDev, mac_size_topDev, windows_mac_size_topDev, linux_size_topDev, windows_linux_size_topDev, mac_linux_size_topDev, windows_mac_linux_size_topDev),
      set_labels=('Windows', 'Mac', 'Linux'))

# Show the plot
plt.show()

"""###Machine-Learning"""

#One-hot encoding the 'genres' and 'categories' columns for Machine-Learning
categories_encoded = pd.get_dummies(df['categories'].str.split(';').apply(pd.Series).stack()).groupby(level=0).sum()

genres_encoded = pd.get_dummies(df['genres'].str.split(';').apply(pd.Series).stack()).sum(level=0)

#Combining them into df dataframe
df = pd.concat([df,categories_encoded, genres_encoded], axis = 1)

import statsmodels.api as sm

#Single-player
single_conditions_market = df['categories'].str.contains('Single-player', case=False, na=False)

#Multi-player in general
multi_player_general_market = df['categories'].str.contains('MMO|Multi-player|Shared/Split Screen|Stats|Co-op|Local Multi-Player|Local Co-op|Steam Leaderboards|Online Multi-Player|Stats|Cross-Platform Multiplayer|Online Co-op|MMO', case=False, na=False)

#CONVERT 'Window', 'Mac' and 'Linux' to BINARY
df["windows"] = df["platforms"].str.contains("windows").astype(float)
df["mac"] = df["platforms"].str.contains("mac").astype(float)
df["linux"] = df["platforms"].str.contains("linux").astype(float)

#CONVERT Online, Local, Single-player to BINARY
df['Multiplayer'] = multi_player_general_market.astype(float)
df['single_player'] = single_conditions_market.astype(float)

x = sm.add_constant(df[['Indie', 'Action', 'Casual', 'Adventure',
                        'Strategy','Simulation','RPG','Early Access',
                        'Free to Play','linux','mac',
                        'single_player','Multiplayer','release_year','price','windows',
                        'Steam Achievements', 'Steam Trading Cards', 'Steam Cloud',
              'Full controller support', 'Partial Controller Support',
              'Steam Leaderboards', 'Stats' , 'Includes level editor', 'Steam Workshop', 'Captions available', 'In-App Purchases', 'VR Support', 'Valve Anti-Cheat enabled'
                        ]].astype(float))

e = df['Owner_encoded']

#OLS model
OLS_m = sm.OLS(e, x).fit()

print(OLS_m.summary())

"""#####Heat-map"""

correlation_matrix = x.corr()

plt.figure(figsize=(20, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')