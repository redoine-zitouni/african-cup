# app.py

import streamlit as st
import pandas as pd
from auth import authenticate_token
from data import get_data
from config import TYPEFORM_API_CONFIG, APP_METADATA

# --- Début de l'interface Streamlit ---

st.set_page_config(page_title=APP_METADATA.get("title"), layout="wide")  # Changement ici

# Créer des colonnes pour centrer le contenu
left, center, right = st.columns([1, 3, 1])

with center:
    # Titre principal centré
    st.markdown(
        "<h1 style='text-align: center;'>Tournoi de l'Unité Africaine du Blanc Mesnil</h1>",
        unsafe_allow_html=True
    )

    # Sous-titre centré venant des métadonnées
    st.markdown(
        f"<h2 style='text-align: center;'>{APP_METADATA.get('title')}</h2>",
        unsafe_allow_html=True
    )

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

    # Input token centré
    token = st.text_input("🔒 Entrez votre token d'accès", type="password")

    if token:
        equipe = authenticate_token(token)
        if equipe:

            # Gestion du cas "All" avec sélection d'équipe
            if equipe == "All":
                st.success(f"Bienvenue, cher administrateur 👋")
                
                equipes_disponibles = df["Equipe"].dropna().unique()
                equipe_selectionnee = st.selectbox("Choisissez une équipe à visualiser :", sorted(equipes_disponibles))
                participants = df[df["Equipe"] == equipe_selectionnee]
                equipe_affichee = equipe_selectionnee
            else:
                st.success(f"Bienvenue, référent de **{equipe}** 👋")
                participants = df[df["Equipe"] == equipe]
                equipe_affichee = equipe

            participants = participants.reset_index(drop=True)

            # Jauge d'inscription
            nb_inscrits = len(participants)
            team_size = APP_METADATA.get("team_size")
            st.metric(label="Inscriptions", value=f"{nb_inscrits} / {team_size}")

            # Tableau des participants, centré
            if not participants.empty:
                st.subheader(f"👥 Liste des Participants - Équipe {equipe_affichee}")
                st.dataframe(participants, use_container_width=True, hide_index=True)
            else:
                st.info("Aucun participant inscrit pour l'instant.")
        else:
            st.error("❌ Token invalide. Vérifiez votre saisie.")
    else:
        st.info("Veuillez entrer votre token pour accéder au suivi des inscriptions.")
