#!/usr/bin/env python
# coding: utf-8

# # Uber Data Analysis

# ![Uber%202.png](attachment:Uber%202.png)

# ![Uber.png](attachment:Uber.png)

# ## Introduction
# Uber is a transportation company with an app that allows passengers to hail a ride and drivers to charge fares, with an estimated price that is dependent on the destination as well as the demand at the time, and get paid.
# More specifically, Uber is a ridesharing company that hires independent contractors as drivers. It's one of many services today that contribute to the sharing economy, supplying a means of connecting existing resources instead of providing the physical resources themselves.
# 
# Uber links passengers with drivers using the Uber app. Generally, the drivers own their own car. The company does also offer rental or lease on cars through third party partners like Hertz, Get Around and Fair. UberFleet is an app for those managing squads of drivers.
# 
# Uber, as a ride-hailing company, relies heavily on data science and analysis to support its day-to-day operations and provide hassle-free rides and deliveries to customers. Data science is a critical component of Uber's operations, and the company invests heavily in its data science and technology capabilities.

# ## Objective
# The objective of this Exploratory Data Analysis is to:
# - break down the data location pockets,
# - identify these pockets based on the demand parameters that show up, then
# - figure out how to position the supply chain in these specific areas

# ## The Key Analysis Components
# - Discovering the locations with the most traffic
# - Uncovering the variance in the Trip Purpose and the effect on the Trip Rate
# - Discovering the weekdays with the most traffic
# - Uncovering the trip rate grouped by Minutes
# - uncovering the Miles travelled under each Trip Purpose grouped by the Trip Category

# ### Environment Setup

# In[1]:


# Import the Library Packages

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# ### Data Exploration

# In[2]:


# Import csv file to read the data 

UberData=pd.read_csv('UberDataset.csv')
UberData


# In[3]:


# Check for the data details

UberData.info()


# In[4]:


# Check for the data Variables

column = UberData.columns
for columns in column:
    print("~",columns)


# In[5]:


# Check for; to familiarize with the Unique values for the trip "CATEGORY"

Data_Conditions= UberData['CATEGORY'].unique()
for CATEGORY in Data_Conditions:
    print("~",CATEGORY)


# In[6]:


# Check for; to familiarize with the Unique values for the trip "PURPOSE"

Data_Conditions= UberData['PURPOSE'].unique()
for PURPOSE in Data_Conditions:
    print("~",PURPOSE)


# In[7]:


# Check for Null values in the data

UberData.isnull().sum()


# ## Data Processing

# In[8]:


# Replace the Null values in "PURPOSE" variable with "Missing"

UberData["PURPOSE"] = UberData["PURPOSE"].fillna("Missing")


# In[9]:


# Check back to comfirm the data status

UberData.isnull().sum()


# In[10]:


# Delete the Null values

UberData.dropna(inplace = True)


# In[11]:


# Check back to comfirm the data status

UberData.isnull().sum()


# In[12]:


# Format the "START_DATE" and "END_DATE" variables as Date/Time value

from dateutil.parser import parse
UberData['START_DATE'] = UberData['START_DATE'].apply(lambda x: parse(x))
UberData["END_DATE"] = UberData["END_DATE"].apply(lambda x: parse(x))


# In[13]:


# Rename specific columns for consistency

UberData.rename(columns={'CATEGORY':'TRIP_CATEGORY', 'START':'START_ADDRESS', 'STOP':'STOP_ADDRESS', 'PURPOSE':'TRIP_PURPOSE'}, inplace=True)
UberData


# ## Eploratory Data Analysis

# ### To discover the areas with the most pickup and destination counts:

# In[14]:


# Extract to analyze the data by the trip (Pickup) "START_ADDRESS" and the "START_DATE"

trip_takeoffs = UberData[['START_ADDRESS', 'START_DATE']]
trip_takeoffs


# In[15]:


# Summarise the start dates from the "trip_takeoffs" extracted data; grouping by the "START_ADDRESS"

takeoff_location = trip_takeoffs.groupby(['START_ADDRESS']).count().sort_values(['START_DATE'], ascending=False)
takeoff_location


# This shows that the Ubers have more customer pickups at Cary area, followed by an Unknown area

# In[16]:


# Extract to analyze the data by the trip (Destination) "STOP_ADDRESS" and the "END_DATE"

trip_stops = UberData[['STOP_ADDRESS', 'END_DATE']]
trip_stops


# In[17]:


# Summarise the start dates from the "trip_stops" extracted data; grouping by the "STOP_ADDRESS"

trip_destination = trip_stops.groupby(['STOP_ADDRESS']).count().sort_values(['END_DATE'], ascending=False)
trip_destination


# The report also shows that Cary has the most trip destination count, then followed by the unknown address

# ### Analyze to uncover the rate of trips by "TRIP_CATEGORY"

# In[18]:


# Present the data in a chart

sns.countplot(x='TRIP_CATEGORY', data=UberData)
plt.show()


# The report shows that the Business trip category has the major bookings for the year as against the Personal trips

# ### Analyze to uncover the variance in the trip purpose and how they affect the trip rate

# In[19]:


# Analyze to uncover the variance in the trip purpose and how they affect the trip rate

trip_purpose=sns.countplot(x='TRIP_PURPOSE', data=UberData,)
trip_purpose.set_xticklabels(trip_purpose.get_xticklabels(), rotation=90)
plt.show()


# The report shows that the unstated (Missing) trip purpose has the more value counts, followed by the Meal/Entertaiment and Meeting trip purposes

# ### To discover the days of the week with the higher traffic:

# In[20]:


# Extract the weekdays from the "START_DATE" pickups 

weekdays=UberData['START_DATE'].dt.strftime('%A')
weekdays


# In[21]:


# Plot a chart to present the traffic summary for each each day of week

plt.figure(figsize=(10, 5))
fig=sns.countplot(x=weekdays)
plt.title("Rate of Ride per Day of the Week")
plt.xticks(rotation=45)


# The report showws that the weekend (Friday) trips has more value counts, followed by that of Monday and Tuesday.
# This implies that there was more traffic at the beginning of every week and during the weekeend.

# ### Analyze to discover the rate of trips by Minutes

# In[22]:


# Create a new column by Calculating each trip duration by examining the time between the "START_DATE" and "END_DATE"

UberData['TRIP_DURATION(Minutes)']=(UberData['END_DATE'] - UberData['START_DATE']).dt.total_seconds() / 60


# In[23]:


# Check back to comfirm the data status

UberData.head()


# In[24]:


# Plot the chart to present the data

plt.figure(figsize=(12, 5))
sns.histplot(UberData['TRIP_DURATION(Minutes)'])
plt.xlabel('Trip Duration (Minutes)')
plt.ylabel('Trip Count (Frequency)')
plt.title('Rate of Trip by Duration (Minutes)')
plt.show()


# The report shows that the trips are only frequent within the range of 50 minutes, while most of the traffic occur within the average minutes.

# ### Analyze to uncover the Miles travelled under each Trip Purpose grouped by the Trip Category

# In[25]:


# Plot the chart to present the data

plt.figure(figsize=(11, 5))
sns.barplot(x= UberData["TRIP_PURPOSE"], y= UberData['MILES'],hue = UberData["TRIP_CATEGORY"])
plt.title("Miles Travelled Per Trip Purpose Compared by the Trip Category")
plt.xticks(rotation=90)


# - The report shows that customers travel more miles by "Commute" as the trip purpose, yet for a "Personal" trip category, While "Business" Category dominated the other Trip Purposes.
# - Interestingly, the "Missing" (unstated) Trip Purpose shared connection with both the "Business" and "Personal" Trip Categories, which implies that the unstated Trip Purpose value is mostly due to Business or Personal reasons.

# ## Conclusion
# The Key Analytic Metrics so far reveals the anticipating demand patterns, and placing driver partners across those hubs with the aim to plug in the demand, lower Estimated Time Arrival (ETAs) and increase overall efficiency.

# ## Implication
# The Uber Data Analysis uses Uber historical data as a benchmark and predicts future action by identifying pockets within the city that witness extremely high demand within a specified range of time.

# ## Limitation
# While Uber generally increases the convenience and efficiency of ridesharing using its app, there are ways in which this method of offering and getting rides can create new challenges for passengers and drivers alike.
# 
# Primarily, passengers need access to an app-capable device and an internet connection in order to hail an uber. Passengers cannot hail an uber directly from the street. Not having a smartphone or computer prevents someone from using Uber to hail themselves a ride.  
# 
# In addition, although Uber drivers must pass a background check to become a driver, it's not perfect, and Uber does not independently test driver skills in the hiring process. This results in inconsistencies in driver quality, which leads to customer complaints and potentially a damaged reputation for Uber.
# 
# Because the company manages employment and facilitates rides remotely, it's nearly impossible for the company to adequately handle incidents over such a large breadth of contexts and interactions. This is problematic for both riders and drivers.
# 
# Uber's dynamic pricing model can also cause difficulty for the drivers who rely on Uber as their primary source of income, because fares can change quickly, and changes are difficult to predict.

# ## Further Research
# As the goal is to drive efficiency across all areas of business, an A/B testing would be necessary to find the most optimized and effective communications that had to be dispatched to driver-partners to address their issues, and convert drivers to become loyal Uber partners by incentivizing. Also to make the process for a driver-partner signing up on our platform easy and scalable, so that they can reach out for specific issues, such as using the app.

# In[ ]:




