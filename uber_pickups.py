import streamlit as st
import pandas as pd
import dataikuapi
import requests
import json
import os
import base64
import ccloud_lib
from confluent_kafka import Consumer
import time

from kafka import KafkaConsumer
CONF = ccloud_lib.read_ccloud_config("python.config")
TOPIC = "spaceship_titanic_data" 


st.title('A Wanted project')

passenger = st.text_input("Passenger Id")
name = st.text_input("Name Forname")
HomePlanet =st.radio("Home planet", ['Earth','Mars','Europa'])
CryptoSleep = st.toggle("CryoSleep")
cabin = st.text_input("Cabin name")
destination = st.radio("Destination",['TRAPPIST-1e','55 Cancri e','P50 3318.5-22'])
age = float(st.slider("Age",0,400))
vip = st.toggle("VIP")
roomService = st.text_input("room service total amount")
foodCourt = st.text_input("food court total amount")
shoppingMall= st.text_input("shopping mall total amount")
spa = st.text_input("spa total amount")
vrDeck = st.text_input("vr deck total amount")
#transported = st.toggle("Transported")
try:
    roomService= int(roomService)
except ValueError:
   roomService = 0
try:
    foodCourt= int(foodCourt)
except ValueError:
   foodCourt = 0
try:
    shoppingMall= int(shoppingMall)
except ValueError:
   shoppingMall = 0
try:
    spa= int(spa)
except ValueError:
   spa = 0
try:
    vrDeck= int(vrDeck)
except ValueError:
   vrDeck = 0
api_clicked  = st.button("Call the API")
if(api_clicked):
    # Make an API request
    url = "https://api-56ce4d5f-779f448b-dku.eu-west-3.app.dataiku.io/public/api/v1/titanic_passengers/passenger/run"
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        response_data = data.get('response', {})

        # Extracting values with default values if empty or missing
        passenger = response_data.get('PassengerId', 'N/A')
        name = response_data.get('Name', 'Unknown')
        HomePlanet = response_data.get('HomePlanet', 'Earth')
        CryptoSleep = response_data.get('CryoSleep', False)
        cabin = response_data.get('Cabin', 'N/A')
        destination = response_data.get('Destination', 'TRAPPIST-1e')
        age = response_data.get('Age', 20.0)
        vip = response_data.get('VIP', False)  
        roomService = response_data.get('RoomService', 0)  
        try:
            roomService = int(float(roomService))
        except ValueError:
            roomService = 0
        foodCourt = response_data.get('FoodCourt', 0)
        try:
            foodCourt= int(float(foodCourt))
        except ValueError:
            foodCourt = 0
        shoppingMall = response_data.get('ShoppingMall', 0)
        try:
            shoppingMall = int(float(shoppingMall))
        except ValueError:
            shoppingMall = 0
        spa = response_data.get('Spa', 0)
        try:
            spa= int(float(spa))
        except ValueError:
            spa= 0
        vrDeck = response_data.get('VRDeck', 0)
        try:
            vrDeck= int(float(vrDeck))
        except ValueError:
            vrDeck = 0
        #transported = response_data.get('Transported', False)   
    else:
        # Print an error message if the request was not successful
        st.text("Error:", response.status_code)

button_clicked  = st.button("Check the survival rate")


kafkaC=True
kafkaApi =""
kafkaApiS=""
kafkaS=""
# Fetch the base64-encoded secret variable from the environment
encoded_secret_variableD = os.environ.get("DATAIKU_API")
if encoded_secret_variableD:
    decoded_bytes = base64.b64decode(encoded_secret_variableD)
    dataikuApi= decoded_bytes.decode('utf-8')
else:
    dataikuApi ="https://api-4034dccc-eaecd172-dku.eu-west-3.app.dataiku.io/"
    # Decode the base64-encoded secret variable

encoded_secret_variableK = os.environ.get("KAFKA_API")
    # Decode the base64-encoded secret variable
if encoded_secret_variableK:
    decoded_bytes = base64.b64decode(encoded_secret_variableK)
    kafkaApi= decoded_bytes.decode('utf-8')
else:
    kafkaC=False

encoded_secret_variableKS = os.environ.get("KAFKA_API_SECRET")
    # Decode the base64-encoded secret variable
if encoded_secret_variableKS:
    decoded_bytes = base64.b64decode(encoded_secret_variableKS)
    kafkaApiS= decoded_bytes.decode('utf-8')
else:
    kafkaC=False
encoded_secret_variableKSs = os.environ.get("KAFKA_SERVER")
    # Decode the base64-encoded secret variable
if encoded_secret_variableKSs:
    decoded_bytes = base64.b64decode(encoded_secret_variableKSs)
    kafkaS= decoded_bytes.decode('utf-8')
else:
    kafkaC=False


# Connect to Kafka
CLUSTER_API_KEY = kafkaApi
CLUSTER_API_SECRET = kafkaApiS
bootstrap_servers = kafkaS
if kafkaC:
    consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(CONF)
    consumer_conf['group.id'] = 'python-group-1'
    consumer_conf['auto.offset.reset'] = 'earliest' # This means that you will consume latest messages that your script haven't consumed yet!
    consumer = Consumer(consumer_conf)
    st.write("Data from Kafka")
    # Subscribe to topic
    consumer.subscribe([TOPIC])
    try:
        while True:
            msg = consumer.poll(5.0) # Search for all non-consumed events. It times out after 5 second
            if msg is None:
                print("Waiting for message or event/error in poll()")
                continue
            elif msg.error():
                st.write('error: {}'.format(msg.error()))
            else:
                # Check for Kafka message
                record_key = msg.key()
                record_value = msg.value()
                data = json.loads(record_value)
                newdata = True
                passenger = data.get('PassengerId', 'N/A')
                name = data.get('Name', 'Unknown')
                HomePlanet = data.get('HomePlanet', 'Earth')
                CryptoSleep = data.get('CryoSleep', False)
                cabin = data.get('Cabin', 'N/A')
                destination = data.get('Destination', 'TRAPPIST-1e')
                age = data.get('Age', 20.0)
                vip = data.get('VIP', False)  
                roomService = data.get('RoomService', 0)  
                time.sleep(10) # Wait 10  second
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
else:
    CLUSTER_API_KEY  = 'PVOPH4N5P77FTZMI'
    CLUSTER_API_SECRET = 'hYsgWo6H52afMzq1Az3iGn6gC7aD4A/jNU0H//QCtmoz1T3njqg8ZMCKOf960dd+'
    consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(CONF)
    consumer_conf['group.id'] = 'python-group-1'
    consumer_conf['auto.offset.reset'] = 'earliest' # This means that you will consume latest messages that your script haven't consumed yet!
    consumer = Consumer(consumer_conf)
    st.write("Data from Kafka")
    # Subscribe to topic
    consumer.subscribe([TOPIC])
    try:
        while True:
            msg = consumer.poll(5.0) # Search for all non-consumed events. It times out after 5 second
            if msg is None:
                print("Waiting for message or event/error in poll()")
                continue
            elif msg.error():
                st.write('error: {}'.format(msg.error()))
            else:
                # Check for Kafka message
                record_key = msg.key()
                record_value = msg.value()
                data = json.loads(record_value)
                st.write(data)
                newdata = True
                passenger = data.get('PassengerId', 'N/A')
                name = data.get('Name', 'Unknown')
                HomePlanet = data.get('HomePlanet', 'Earth')
                CryptoSleep = data.get('CryoSleep', False)
                cabin = data.get('Cabin', 'N/A')
                destination = data.get('Destination', 'TRAPPIST-1e')
                age = data.get('Age', 20.0)
                vip = data.get('VIP', False)  
                roomService = data.get('RoomService', 0)  
                time.sleep(10) # Wait 10  second
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
    
    
if(passenger==''):
    passenger = 'N/A'
if(name==''):
    name='Unknow'
if(cabin ==''):
    cabin='N/A'

record_to_predict = {
      "PassengerId": passenger,
      "HomePlanet": HomePlanet,
      "CryoSleep": CryptoSleep,
      "Cabin": cabin,
      "Destination": destination,
      "Age": age,
      "VIP": vip,
      "new_RoomService": roomService,
      "new_FoodCourt": foodCourt,
      "new_ShoppingMall": shoppingMall,
      "new_Spa": spa,
      "new_VRDeck": vrDeck,
      "Total": total,
      "Name": name
}
total = float(foodCourt+roomService+spa+shoppingMall+vrDeck)

client = dataikuapi.APINodeClient(dataikuApi,"space_titanic_crounch")
if(button_clicked or api_clicked or newdata):
    st.table(pd.DataFrame(record_to_predict, index=[0]))
    prediction = client.predict_record("space_titanic_end", record_to_predict)
    if(passenger =='N/A'):
        passenger = "not defined"
    outcome = "Dead"
    if prediction['result']["prediction"] == 'True':
        outcome = "Alive"
    st.text("The passenger " + name + " is " + outcome + " with a probability of "+ str(round(prediction['result']["probas"][prediction['result']["prediction"]],4)*100)+"%")
    st.bar_chart(prediction['result']["probas"])
    api_clicked = False
    newdata=False
  
