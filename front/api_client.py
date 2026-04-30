"""Client HTTP minimal pour parler au backend Django."""
import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv('API_URL', 'https://contructionanalyst.onrender.com')


def _headers():
    token = st.session_state.get('token')
    return {'Authorization': f'Bearer {token}'} if token else {}


def register(email, password, name):
    return requests.post(f'{API_URL}/api/auth/register', json={
        'email': email, 'password': password, 'name': name
    }).json()

def login(email, password):
    return requests.post(f'{API_URL}/api/auth/login', json={
        'email': email, 'password': password
    }).json()

def get_features():
    return requests.get(f'{API_URL}/api/features').json()['features']

def analyser(nom_terrain, localisation, donnees):
    return requests.post(f'{API_URL}/api/analyser', json={
        'nom_terrain': nom_terrain, 'localisation': localisation, 'donnees': donnees
    }, headers=_headers()).json()

def historique():
    return requests.get(f'{API_URL}/api/historique', headers=_headers()).json()

def dataset():
    return requests.get(f'{API_URL}/api/dataset').json()
