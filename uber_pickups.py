import streamlit as st
import pandas as pd
import numpy as np


# Install required packages
subprocess.call(["pip", "install", "kafka-python"])

from kafka import KafkaConsumer


st.title('A Wanted project')

##DATE_COLUMN = 'date/time'
##DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
##         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# Connect to Kafka
cloud_api_key = 'PVOPH4N5P77FTZMI'
cloud_api_secret = 'hYsgWo6H52afMzq1Az3iGn6gC7aD4A/jNU0H//QCtmoz1T3njqg8ZMCKOf960dd+'
bootstrap_servers = 'pkc-7xoy1.eu-central-1.aws.confluent.cloud:9092'

consumer = KafkaConsumer(
    'scored_data',
    group_id='streamlit-group',
    security_protocol='SASL_SSL',
    sasl_mechanism='PLAIN',
    sasl_plain_username=cloud_api_key,
    sasl_plain_password=cloud_api_secret,
    bootstrap_servers=bootstrap_servers,
)


for message in consumer:
    st.write(f"Received: {message.value.decode('utf-8')}")
         
##@st.cache_data
##def load_data(nrows):
##    data = pd.read_csv(DATA_URL, nrows=nrows)
##    lowercase = lambda x: str(x).lower()
##    data.rename(lowercase, axis='columns', inplace=True)
##    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
##    return data

# Create a text element and let the reader know the data is loading.
##data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
##data = load_data(100)
# Notify the reader that the data was successfully loaded.
##data_load_state.text("Done! (using st.cache_data)")
