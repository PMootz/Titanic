import streamlit as st
import pandas as pd
import numpy as np
import dataikuapi
from kafka import KafkaConsumer


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
transported = st.toggle("Transported")
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

total = float(foodCourt+roomService+spa+shoppingMall+vrDeck)
button_clicked  = st.button("Check the survival rate")

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
      "Name": name,
      "Transported": transported
}
st.table(pd.DataFrame(record_to_predict, index=[0]))

client = dataikuapi.APINodeClient("https://api-4034dccc-eaecd172-dku.eu-west-3.app.dataiku.io/", "space_titanic_crounch")
if(button_clicked):
    prediction = client.predict_record("space_titanic_end", record_to_predict)
    if(passenger ==''):
        passenger = "not defined"
    outcome = "Alive"
    if prediction['result']["prediction"] == 'True':
        outcome = "Dead"
    st.text("The passenger " + name + " is " + outcome + " with a probability of "+ str(round(prediction['result']["probas"]['True'],4)*100)+"%")
    st.bar_chart(prediction['result']["probas"])


# Connect to Kafka
cloud_api_key = 'PVOPH4N5P77FTZMI'
cloud_api_secret = 'hYsgWo6H52afMzq1Az3iGn6gC7aD4A/jNU0H//QCtmoz1T3njqg8ZMCKOf960dd+'
bootstrap_servers = 'pkc-7xoy1.eu-central-1.aws.confluent.cloud:9092'

consumer = KafkaConsumer(
    'titanic',
    group_id='streamlit-group',
    security_protocol='SASL_SSL',
    sasl_mechanism='PLAIN',
    sasl_plain_username=cloud_api_key,
    sasl_plain_password=cloud_api_secret,
    bootstrap_servers=bootstrap_servers,
)


for message in consumer:
    st.write(f"Received: {message.value.decode('utf-8')}")
