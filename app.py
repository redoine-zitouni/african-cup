# app.py

import streamlit as st
import pandas as pd
from auth import authenticate_token
from data import get_data
from config import TYPEFORM_API_CONFIG, APP_METADATA

# --- Début de l'interface Streamlit ---

st.set_page_config(page_title=APP_METADATA.get("title"), layout="centered")

st.markdown("# Coupe d'Afrique des Nations à Le Blanc Mesnil")

# Sous-titre venant des métadonnées
st.markdown(f"## {APP_METADATA.get('title')}")

# Petite citation centrée
st.markdown(
    """
    <p style='text-align: center; font-style: italic; color: gray;'>
    "pour nous, par nous"
    </p>
    """,
    unsafe_allow_html=True
)

# Appliquer le style custom Apple-like
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Chargement des données ---

df = get_data(config=TYPEFORM_API_CONFIG)

# Retour Tilia
st.link_button("Le Tilia", "https://letilia.org/actus/")

# Input token
token = st.text_input("🔒 Entrez votre token d'accès", type="password")

if token:
    equipe = authenticate_token(token)
    if equipe:
        st.success(f"Bienvenue, référent de **{equipe}** 👋")

        # Filtrer les participants de cette équipe
        if equipe == "All":
            participants = df.copy()
        else:
            participants = df[df["Equipe"] == equipe]

        # Jauge d'inscription
        nb_inscrits = len(participants)
        if equipe == "All":
            st.metric(label="Inscriptions", value=f"{nb_inscrits} Joueurs")
        else:
            st.metric(label="Inscriptions", value=f"{nb_inscrits} / {team_size}")

        # Tableau des participants
        if not participants.empty:
            st.subheader("👥 Liste des Participants")
            st.dataframe(
                participants,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Aucun participant inscrit pour l'instant.")
    else:
        st.error("❌ Token invalide. Vérifiez votre saisie.")
else:
    st.info("Veuillez entrer votre token pour accéder au suivi des inscriptions.")
