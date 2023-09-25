import streamlit as st
import requests
import datetime as dt
import os
import json
from PIL import Image


Image Manipulation
@st.cache_resource
 def load_image(img):
    im =Image.open(os.path.join(img))
    return im
st.image(load_image('/home/ninja/Documents/CES-DS_AnalyseGestionGrandesMassesDonnées/Module14_ProjetPersonnel/Mémoire/Home-Credit_2.png'))
st.write("### You are welcome,","Vous êtes les bienvenus,", "Gern geschehen,", "Sois bienvenidos" )
today = dt.date.today()
now = dt.datetime.now()
current_time = now.time().strftime("%H:%M:%S")
# Afficher la date et l'heure avec une personnalisation de style
st.markdown(f"<div style='font-family: Arial; font-size: 20px; color: green; margin: 0; line-height: 1; font-weight: bold;'>Date: {today}"
            f"<br>Heure: {current_time}</div>", unsafe_allow_html=True)


# st.write(today)
st.header("Dashboard for Customer Advisor")

# url_local= 'http://127.0.0.1:5000/'
url_local= 'https://test-flask1-84968da5768b.herokuapp.com/'

# st.sidebar.header("Query Input")
# ticker = st.sidebar.text_input('Enter your ID', '')
response = requests.get(url_local + '/list_IDs/')
list_id = json.loads(response.content.decode('utf-8')).get("identiy")
# Convertir chaque ID en entier
list_id = [int(x) for x in list_id]
# Trier la liste
list_id = sorted(list_id, reverse=False)
selected_id = st.sidebar.selectbox('Client ID :', list_id)
# st.sidebar.write(selected_id)

url_viability = url_local + 'viability/?id=' + str(selected_id)
response = requests.get(url_viability)
print("response :", response)
# label = json.loads(response.content.decode('utf-8')).get("score")
label = json.loads(response.content).get("score")
print("ID:", selected_id,"label:", label, type(label))
text_viability = 'Félicitation votre crédit est accordé' if label == 0 else 'Nous sommes désolé, le crédit est refusé'
color = 'green' if label == 0 else 'red'
st.markdown(f"<h1 style='text-align: left; color: {color}; font-size: 40px;'>{text_viability}</h1>", unsafe_allow_html=True)
# st.write(text_viability)


n_features = st.sidebar.slider("Sélectionnez le nombre de caractéristiques à afficher", min_value=1, max_value=20, value=5, step=1)

button_global = st.sidebar.button('GET GLOBAL FEATURES')
button_local = st.sidebar.button('GET LOCAL FEATURES')

if button_global:
    url_requete_global = url_local + 'features_importance_global/?n=' + str(n_features)
    response = requests.get(url_requete_global).text
    # st.components.v1.html("<div style='overflow-x: auto; height: 300px;'>" + response + "</div>", height=2000, width= 1000, scrolling=False)
    st.components.v1.html(response, height=1000, width=2500, scrolling=True)
if button_local:
    url_requete_local = url_local + 'lime/?n=' + str(n_features) + '&id=' + str(selected_id)
    response = requests.get(url_requete_local).text
    st.components.v1.html("<div style='overflow-x: auto; height: 300px;'>" + response + "</div>", height=500, width= 1000, scrolling=True)

st.text_area("Info :",'Home-Credit est le fournisseur internationale de crédit à la consommation'
        ' incontournable depuis 25 ans. Nous sommes présent dans sept pays'
        ' (Chine, Inde, Indonésie, ViêtNam, Kazakhstan,'
        ' République Thèque et Slovaquie).')


# streamlit run dashboard.py
