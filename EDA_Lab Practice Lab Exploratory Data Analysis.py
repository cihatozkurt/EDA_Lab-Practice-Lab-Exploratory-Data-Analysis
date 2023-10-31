#!/usr/bin/env python
# coding: utf-8

# <p style="text-align:center">
#     <a href="https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMML0232ENSkillsNetwork837-2023-01-01">
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo"  />
#     </a>
# </p>
# 

# # **Exploratory Data Analysis**
# 

# Estimated time needed: **30** minutes
# 
# Exploratory Data Analysis (EDA) is the crucial process of using summary statistics and graphical representations to perform preliminary investigations on data to uncover patterns, detect anomalies, test hypotheses, and verify assumptions.
# 
# In this notebook, we will learn some interesting and useful data exploration techniques that can be applied to explore any geographical data.
# 

# ## Objectives
# 

# *After completing this lab you will be able to:*
# 
# *   Do Data Wrangling
# *   Do Data Filtering 
# *   Plot with <code>plotly.express</code>
# *   Produce choropleth map
# 

# ***
# 

# ## **Setup**
# 

# For this lab, we will be using the following libraries:
#  - [`pandas`](https://pandas.pydata.org/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMML0232ENSkillsNetwork837-2023-01-01) for managing the data.
#  - [`plotly.express`](https://plotly.com/python/plotly-express/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMML0232ENSkillsNetwork837-2023-01-01) for visualizing the data.
#  - [`json`](https://docs.python.org/3/library/json.html/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMML0232ENSkillsNetwork837-2023-01-01) for reading json file formats.
#  
# 

# ## **Installing Required Libraries**
# 

# The following required modules are pre-installed in the Skills Network Labs environment. However, if you run this notebook commands in a different Jupyter environment (e.g. Watson Studio or Ananconda) you will need to install these libraries by removing the `#` sign before `!mamba` in the code cell below.
# 

# In[1]:


# All Libraries required for this lab are listed below. The libraries pre-installed on Skills Network Labs are commented.
# !mamba install -qy pandas==1.3.4 numpy==1.21.4 seaborn==0.9.0 matplotlib==3.5.0 scikit-learn==0.20.1
# Note: If your environment doesn't support "!mamba install", use "!pip install"


# In[2]:


import pandas as pd
import plotly.express as px
import datetime 
import requests
import json


# ## **Reading and understanding our data**
# 

# The dataset in this lab is <a href="https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMML0232ENSkillsNetwork837-2023-01-01&pid=1810000101">Monthly average retail prices for gasoline and fuel oil, by geography</a>  . It is available through Statistics Canada and includes monthly average gasoline price (Cents per Litre), of major Canadian Cities, starting from 1979 until recent. 
# 

# Another dataset, <a href="https://thomson.carto.com/tables/canada_provinces/public/map?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMML0232ENSkillsNetwork837-2023-01-01">canada_provinces.geojson</a>, contains the mapping information of all Canadian Provinces. It will be used in our analysis to produce a choropleth map. 
# 

# Let's read the data into *pandas* dataframe and look at the first 5 rows using the `head()` method. 
# 

# In[3]:


gasoline = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-ML0232EN-SkillsNetwork/asset/18100001.csv")
gasoline.head()


# Let's find out how many entries there are in our dataset, using `shape` function.
# 

# In[4]:


gasoline.shape


# Using `info` function, we will take a look at our types of data.
# 

# In[5]:


gasoline.info()


# Using `columns` method, we will print all the column names.
# 

# In[6]:


gasoline.columns


# Below, we will check for any missing values.
# 

# In[7]:


gasoline.isnull().sum()


# ## **Data Wrangling** 
# ### Selecting and renaming the columns of interest
# 

# Below, we are filtering our data, by selecting only the relevant columns. Also, we are using the `rename()` method to change the name of the columns.
# 

# In[8]:


data = (gasoline[['REF_DATE','GEO','Type of fuel','VALUE']]).rename(columns={"REF_DATE" : "DATE", "Type of fuel" : "TYPE"})
data.head()


# ### Splitting the columns
# 

# The `str.split()` function splits the string records, by a 'comma', with `n=1` slplit, and <code>Expend=True</code> , returns a dataframe. Below, we are splitting 'GEO' into 'City' and 'Province'.
# 

# In[9]:


data[['City', 'Province']] = data['GEO'].str.split(',', n=1, expand=True)


# In[10]:


data.head()


# ### Changing to *datetime* format
# 

# If we scroll up to our `gasoline.info()` section, we can find that  'REF_DATE' is an object type. To be able to filter by day, month, or year, we need to change the format from object type to *datetime*. Pandas function `to_datetime()` transforms to date time format. Also, we need to specify the format of *datetime* that we need. In our case, `format='%b-%y'` means that it will split into the name of a month and year. `str.slice(stop=3)` splits and outputs the first 3 letters of a month. For more information on how to transform to *datetime*, please visit [this](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMML0232ENSkillsNetwork837-2023-01-01) pandas documentation. Also, [this](https://strftime.org/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMML0232ENSkillsNetwork837-2023-01-01) web page contains more information on *datetime* formats.
# 

# In[11]:


data['DATE'] = pd.to_datetime(data['DATE'], format='%b-%y')
data['Month'] = data['DATE'].dt.month_name().str.slice(stop=3)
data['Year'] = data['DATE'].dt.year


# In[12]:


data.head()


# The `describe()` function provides statistical information about the numeric variables. Since we only have the 'VALUE' variable that we want statistical information on, we will filter it by `data.VALUE.describe()` function.
# 

# In[13]:


data.VALUE.describe()
# can also use  data['VALUE'].describe()


# Now, it is useful to know what is inside our categorical variables. We will use `unique().tolist()` functions to print out all of our 'GEO' colunm.
# 

# In[14]:


data.GEO.unique().tolist()
# can also use  data['GEO'].unique().tolist()


# ## Exercise 1
# 

# In this exercise, print out all categories in 'TYPE' column.
# 

# In[15]:


# Enter your code and run the cell
data.TYPE.unique()


# <details>
# <summary><strong>Solution</strong> (Click Here)</summary>
#     &emsp; &emsp; <code>
# data.TYPE.unique().tolist()
# </code>
# </details>
# 

# ## **Data Filtering** 
# 

# This section will introduce you to some of the most common filtering techniques when working with pandas dataframes.
# 

# ### Filtering with logical operators
# 

# We can use the logical operators on column values to filter rows. First, we  specify the name of our data, then, square brackets to select the name of the column, double 'equal' sign, '==' to select the name of a row group, in single or double quotation marks. If we want to exclude some entries (e.g. some locations), we would use the 'equal' and 'exclamation point' signs together, '=!'. We can also use '</>', '<=/>=' signs to select numeric information.
# 
# Let's select the Calgary, Alberta data to see all the information.
# 

# In[16]:


calgary = data[data['GEO'] == 'Calgary, Alberta']
calgary


# Now, let's select 2000 year.
# 

# In[17]:


sel_years = data[data['Year'] ==  2000]
sel_years


# ### Filtering by multiple conditions
# 

# There are many alternative ways to perform filtering in pandas. We can also use '|' ('or') and '&' (and) to select multiple columns and rows. 
# 

# For example, let us select Toronto and Edmonton locations.
# 

# In[18]:


mult_loc = data[(data['GEO'] == "Toronto, Ontario") | (data['GEO'] == "Edmonton, Alberta")]
mult_loc


# Alternatively, we can use `isin` method to select multiple locations.
# 

# In[19]:


cities = ['Calgary', 'Toronto', 'Edmonton']
CTE = data[data.City.isin(cities)]
CTE


# ## Exercise 2 a
# 

# In this exercise, please use the examples shown above, to select the data that shows the price of the 'household heating fuel', in Vancouver, in 1990.
# 

# In[24]:


exercise2a = data[(data['TYPE'] == 'Household heating fuel') & (data['Year'] == 1998) & (data['City'] == 'Vancouver')]
exercise2a


# In[25]:


# Enter your code below and run the cell


# <details>
# <summary><strong>Solution</strong> (Click Here)</summary>
#     &emsp; &emsp; <code>
# exercise2a = data[( data['Year'] ==  1990) & (data['TYPE'] == "Household heating fuel") & (data['City']=='Vancouver')]
# exercise2a
# </code>
# </details>
# 

# ## Exercise 2 b
# 

# In this exercise, please select the data that shows the price of the 'household heating fuel', in Vancouver, in the years of 1979 and 2021.
# 

# In[55]:


exercise2b = data[(data['TYPE'] == 'Household heating fuel') & (data['City'] == 'Vancouver') & ((data['Year'] == 1979) | (data['Year'] == 2021))]
exercise2b


# In[ ]:


# Enter your code below and run the cell


# <details>
# <summary><strong>Solution</strong> (Click Here)</summary>
#     &emsp; &emsp; <code>
# exercise2b = data[( data['Year'] <=  1979) | ( data['Year'] ==  2021) & (data['TYPE'] == "Household heating fuel") & (data['City']=='Vancouver')]
# exercise2b
# </code>
# </details>
# 

# <details>
# <summary><strong>Hint</strong> (Click Here)</summary>
#     &emsp; &emsp; <code>
# If we use '&' operator between the two years, it will return an empty data frame. This is because there was no data for the 'household heating fuel, in Vancouver, in 1979. Using 'or' operator is suitable because either one of two years that contains any information on 'household heating fuel' in Vancouver.
# </code>
# </details>
# 

# ### Filtering using `groupby()` method
# 

# The role of `groupby()` is to analyze data by some categories. The simplest call is by a column name. For example, let’s use the 'GEO' column and `ngroups` function to calculate the number of groups (cities, provinces) in 'GEO' column.
# 

# In[56]:


geo = data.groupby('GEO')
geo.ngroups


# Most commonly, we use `groupby()` to split the data into groups,this will apply some function to each of the groups (e.g. mean, median, min, max, count), then combine the results into a data structure. For example, let's select the 'VALUE' column and calculate the mean of the gasoline prices per year. First, we specify the 'Year" column, following by the 'VALUE' column, and the `mean()` function.
# 

# In[57]:


group_year = data.groupby(['Year'])['VALUE'].mean()
group_year


# ## Exercise 3 a
# 

# In the cell below, please use `groupby()` method to group by the maximum value of gasoline prices, for each month. 
# 

# In[ ]:


# Enter your code below and run the cell
exercise3b = data.groupby(['Year', 'City'])['VALUE'].median()


# In[59]:


exercise3b = data.groupby(['Month'])['VALUE'].max()
exercise3b


# <details>
# <summary><strong>Solution</strong> (Click Here)</summary>
#     &emsp; &emsp; <code>
# exercise3a = data.groupby(['Month'])['VALUE'].max()
# </code>
# </details>
# 

# ## Exercise 3 b
# 

# In the cell below, please use `groupby()` method to group by the median value of gasoline prices, for each year and each city. 
# 

# In[62]:


exercise3b = data.groupby(['Year','City'])['VALUE'].median()
exercise3b


# <details>
# <summary><strong>Solution</strong> (Click Here)</summary>
#     &emsp; &emsp; <code>
# exercise3b = data.groupby(['Year', 'City'])['VALUE'].median()
# </code>
# </details>
# 

# <details>
# <summary><strong>Hint</strong> (Click Here)</summary>
#     &emsp; &emsp; <code>
#     
# We can also reset the index of the new data output, by using `reset_index()`, and round up the output values to 2 decimal places.
# 
# exercise3b = data.groupby(['Year', 'City'])['VALUE'].median().reset_index(name ='Value').round(2)
# 
# </code>
# </details>
# 

# ## **Visualizing the data with *pandas* plotly.express** 
# 

# The *plotly.express* library (usually imported as px) contains functions that can create entire figures at once. *plotly.express* is a built-in part of the *plotly* library, and makes creation of most common figures very easy. For more information on *plotly.express*, please refer to [this](https://plotly.com/python/plotly-express/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMML0232ENSkillsNetwork837-2023-01-01) documentation.
# 

# Here, we will plot the prices of gasoline in all cities during 1979 - 2021.
# 

# In[66]:


price_bycity = data.groupby(['Year', 'GEO'])['VALUE'].mean().reset_index(name ='Value').round(2)
price_bycity


# In[67]:


fig = px.line(price_bycity
                   ,x='Year', y = "Value", 
                   color = "GEO", color_discrete_sequence=px.colors.qualitative.Light24)
fig.update_traces(mode='markers+lines')
fig.update_layout(
    title="Gasoline Price Trend per City",
    xaxis_title="Year",
    yaxis_title="Annual Average Price, Cents per Litre")
fig.show()


# Here, we will plot the average monthly prices of gasoline in Toronto for the year of 2021.
# 

# In[68]:


mon_trend = data[(data['Year'] ==  2021) & (data['GEO'] == "Toronto, Ontario")]
group_month = mon_trend.groupby(['Month'])['VALUE'].mean().reset_index().sort_values(by="VALUE")


# In[69]:


fig = px.line(group_month,
                   x='Month', y = "VALUE")
fig.update_traces(mode='markers+lines')
fig.update_layout(
    title="Toronto Average Monthly Gasoline Price in 2021",
    xaxis_title="Month",
    yaxis_title="Monthly Price, Cents per Litre")
fig.show()


# ## Exercise 4
# 

# In the cell below, use *plotly.express* or other libraries, to plot the annual average gasoline price, per year, per gasoline type.
# 

# In[81]:


gas_type = data.groupby(['Year','TYPE'])['VALUE'].mean().reset_index(name='Price').round(2)
gas_type


# In[94]:


fig = px.line(gas_type, x='Year', y='Price',color = 'TYPE')
fig.update_traces(mode='markers+lines')
fig.update_layout(title = 'annual average gasoline price')
fig.show()


# <details>
# <summary><strong>Solution</strong> (Click Here)</summary>
#     &emsp; &emsp; <code>
# type_gas = data.groupby(['Year', 'TYPE'])['VALUE'].mean().reset_index(name ='Type').round(2)
# fig = px.line(type_gas,
#                    x='Year', y = "Type", 
#                    color = "TYPE", color_discrete_sequence=px.colors.qualitative.Light24)
# fig.update_traces(mode='markers+lines')
# fig.update_layout(
#     title="Fuel Type Price Trend",
#     xaxis_title="Year",
#     yaxis_title="Annual Average Price, Cents per Litre")
# fig.show()
# 
# </code>
# </details>
# 

# In[99]:


type_gas = data.groupby(['Year', 'TYPE'])['VALUE'].mean().reset_index(name ='Type').round(2)
fig = px.line(type_gas,
                   x='Year', y = "Type", 
                   color = "TYPE", color_discrete_sequence=px.colors.qualitative.Light24)
fig.update_traces(mode='markers+lines')
fig.update_layout(
    title="Fuel Type Price Trend",
    xaxis_title="Year",
    yaxis_title="Annual Average Price, Cents per Litre")
fig.show()


# We can also use the animated time frame to show the trend of gasoline prices over time.
# 

# In[95]:


bycity = data.groupby(['Year', 'City'])['VALUE'].mean().reset_index(name ='Value').round(2)
bycity.head()


# In[96]:


fig = px.bar(bycity,  
            x='City', y = "Value", animation_frame="Year")
fig.update_layout(
    title="Time Lapse of Average Price of Gasoline, by Province",
    xaxis_title="Year",
    yaxis_title="Average Price of Gasoline, Cents per Litre")

fig.show()
 


# Another way to display the distribution of average gasoline prices in Canadian Provinces is by plotting a map. We will use 2021 year to display the average gasoline price in all Canadian Provinces.
# First, we select the year.
# 

# In[102]:


one_year = data[data['Year'] == 2021]
one_year.head()


# Then, we group by the 'Province' and the 'mean' values of gasoline prices per each province. We also need to index each province with province id. 
# 

# In[103]:


geodata =  one_year.groupby('Province')['VALUE'].mean().reset_index(name ='Average Gasoline Price').round(2)

provinces={' Newfoundland and Labrador':5,
 ' Prince Edward Island':8,
 ' Nova Scotia':2,
 ' New Brunswick':7,
 ' Quebec':1,
 ' Ontario':11,
 ' Ontario part, Ontario/Quebec':12,
 ' Manitoba':10,
 ' Saskatchewan':3,
 ' Alberta':4,
 ' British Columbia':6,
 ' Yukon':9,
 ' Northwest Territories':13
}
geodata['ProvinceID']=geodata['Province'].map(provinces)
display(geodata)


# Here, we are linking each province by its specified 'provinceID' with another dataset, ‘canada_provinces.geojson’, containing all the mapping information for plotting our provinces.
# 
# First, we need to download the Canadian Provinces dataset from IBM cloud storage, using the `requests.get()` function.
# 

# In[104]:


geo = requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-ML0232EN-SkillsNetwork/asset/canada_provinces.geojson")


# Next, we will load the file as a string, using `json.loads()` function.
# 

# In[105]:


mp = json.loads(geo.text)
    
fig = px.choropleth(geodata,
                    locations="ProvinceID",
                    geojson=mp,
                    featureidkey="properties.cartodb_id",
                    color="Average Gasoline Price",
                    color_continuous_scale=px.colors.diverging.Tropic,
                    scope='north america',
                    title='<b>Average Gasoline Price </b>',                
                    hover_name='Province',
                    hover_data={
                        'Average Gasoline Price' : True,
                        'ProvinceID' : False
                    },
                     
                    locationmode='geojson-id',
                    )
fig.update_layout(
    showlegend=True,
    legend_title_text='<b>Average Gasoline Price</b>',
    font={"size": 16, "color": "#808080", "family" : "calibri"},
    margin={"r":0,"t":40,"l":0,"b":0},
    legend=dict(orientation='v'),
    geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#e0fffe')
)

#Show Canada only 
fig.update_geos(showcountries=False, showcoastlines=False,
                showland=False, fitbounds="locations",
                subunitcolor='white')
fig.show()


# ## Exercise 5
# 

# In this exercise, experiment with different color scales to make the visualization easier to read. Some suggestions are provided in the "Hint" section. Simply copy the above code and replace 'px.colors.diverging.Tropic', with any other color scales. For example, the sequential color scales are appropriate for most continuous data, but in some cases it can be helpful to use a diverging or cyclical color scale. Diverging color scales are appropriate for the continuous data that has a natural midpoint. For more information on *plotly* colors, please visit [this plotly documentation](https://plotly.com/python/builtin-colorscales/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMML0232ENSkillsNetwork837-2023-01-01) web page.
# 

# In[ ]:


# Enter your code and run the cell


# <details>
# <summary><strong>Hint</strong> (Click Here)</summary>
#     &emsp; &emsp; <code>
#     px.colors.diverging.Tropic
#     px.colors.diverging.Temps
#     px.colors.sequential.Greens
#     px.colors.sequential.Reds
# 
# </code>
# </details>
# 

# # Congratulations! - You have completed the lab
# 

# ## Author
# 

# [Svitlana Kramar](https://www.linkedin.com/in/svitlana-kramar/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMML0232ENSkillsNetwork837-2023-01-01)
# 

# ## Change Log
# 

# | Date (YYYY-MM-DD) | Version | Changed By | Change Description      |
# | ----------------- | ------- | ---------- | ----------------------- |
# | 2022-01-18        | 0.1     |Svitlana K. | Added Introduction      |
# 
# 

# Copyright © 2020 IBM Corporation. All rights reserved.
# 
