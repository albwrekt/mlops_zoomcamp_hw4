#!/usr/bin/env python
# coding: utf-8

# In[14]:


# Import libraries
import pickle
import pandas as pd
import numpy as np
from sys import argv


# In[9]:


# Load in the library
with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


# In[10]:


# Read in the taxi data and generate the unique ID's
categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


# In[20]:


# Read the file
file_year = int(argv[1])
file_month = int(argv[2])
df = read_data(f'./data/yellow_tripdata_{file_year:04d}-{file_month:02d}.parquet')


# In[21]:


# Transform the pandas dataframe to dictionary
dicts = df[categorical].to_dict(orient='records')
# Use dictionary vectorizer to transform the output
X_val = dv.transform(dicts)
# Predict with the newly generated outputs, to the saved model.
y_pred = model.predict(X_val)


# In[22]:


# Calculate the standard deviation of the duration predictions
print(f"Standard Deviation of Predictions: {np.std(y_pred)}")


# In[25]:


# Create the ride ID, needs to be done this way to get the vectorized application of pandas
df['ride_id'] = f'{file_year:04d}/{file_month:02d}_'+df.index.astype('str')


# In[26]:


# Write the ride_id and predictions to a results dataframe
df_results = df.copy()
df_results['duration'] = y_pred
df_results.head()

# print out the mean duration from the numpy array
print(f'Mean of Predictions: {np.mean(y_pred)}')


# In[ ]:


# Save the data back out to parquet
df_results.to_parquet(
    path='output_file.parquet',
    engine='pyarrow',
    compression=None,
    index=False
)

