import requests
import pandas as pd
from datetime import datetime

def get_data(config: dict) -> pd.DataFrame:
    """
    Récupère toutes les données de l'API et retourne un DataFrame structuré avec les informations d'intérêt,
    en filtrant pour ne garder que les réponses dont la date est >= aujourd'hui.
    
    Args:
        config (dict): Doit contenir les clés 'API_TOKEN' et 'BASE_URL'.

    Returns:
        pd.DataFrame: Données récupérées sous forme de DataFrame.
    """
    api_token = config["API_TOKEN"]
    base_url = config["BASE_URL"]

    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    params = {
        "page_size": 1000,
        "completed": "true",
    }

    all_items = []
    url = base_url

    update_form_date = datetime(2025,4,28).date()

    while url:
        resp = requests.get(url, headers=headers, params=params, verify=False)
        resp.raise_for_status()
        data = resp.json()

        # Récupérer les items de la réponse
        items = data.get("items", [])

        for item in items:
            # Extraction des éléments d'intérêt
            submitted_at = item.get("submitted_at")
            if submitted_at is None:
                continue  # Ignorer les entrées sans date

            # Convertir submitted_at en objet datetime
            submitted_datetime = datetime.fromisoformat(submitted_at.replace("Z", "+00:00"))
            if submitted_datetime.date() < update_form_date:
                continue  # Ne prendre que les dates récentes pour le nouveau formulaire

            answers = item.get("answers", [])

            print(answers)

            # Initialiser les variables
            nom, prenom, equipe, taille_maillot, nom_maillot, num_maillot, status, email = [None] * 8

            # Extraire les informations des réponses
            for answer in answers:
                field_id = answer.get("field", {}).get("id")

                if field_id == "mJSz2MX7ZzXy":  # Prénom
                    prenom = answer.get("text").lower().capitalize().strip()
                elif field_id == "UEYYQGRjcv1w":  # Nom
                    nom = answer.get("text").lower().capitalize().strip()
                elif field_id == "AiOYe71PFjOI":
                    equipe = answer.get("choice").get("label").strip()
                elif field_id == "9lpvtjHLtrvk":  # Taille du maillot
                    taille_maillot = answer.get("text").upper().strip()
                elif field_id == "HS2DpVA1fH3L":  # Numéro du maillot
                    num_maillot = answer.get("text").strip()
                elif field_id == "Q3HpyFlvtfoy":  # Nom du maillot
                    nom_maillot = answer.get("text").upper().strip()
                elif field_id == "3YFgsyAdsgEH":
                    status = ", ".join(answer.get("choices").get("labels")).strip()
                elif field_id == "1SQ5ILcG7Lj6":
                    provenance = answer.get("text").strip()
                elif field_id == "9YiWRNjOejnT":
                    email = answer.get("email").strip()
                elif field_id == "5s8tbGTjMsOP":
                    phone_number = answer.get("phone_number").strip()

            # Ajouter l'item au tableau de résultats
            all_items.append({
                "Date": submitted_at,
                "Nom": nom,
                "Prenom": prenom,
                "E-mail": email,
                "Tel.": phone_number,
                "Equipe": equipe,
                "Taille du Maillot": taille_maillot,
                "Nom du Maillot": nom_maillot,
                "Numero du Maillot": num_maillot,
                "Status": status,
                "Provenance": provenance,
            })

        # Vérifier si la réponse contient un lien vers la page suivante
        url = data.get("_links", {}).get("next")

    # Convertir la liste de réponses en DataFrame
    df = pd.DataFrame(all_items)

    base_data = pd.read_csv("data/base.csv", sep=";")

    df = pd.concat([base_data, df], ignore_index=True, axis=0)

    df = df.sort_values(by="Date", ascending=False)
    df = df[df["Status"] != "Challenge"]

    return df
