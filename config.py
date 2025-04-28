import os
APP_METADATA = dict(
    title = "Suivi des Inscriptions",
    team_size = 12,
)

APP_ACCESS_TOKENS = {
    "RESTEMON482": "Reste du Monde",
    "ALGERIE735": "Algérie",
    "MAROC178": "Maroc",
    "CONGOBRA392": "Congo Brazzaville",
    "CONGOKIN931": "Congo Kinshasa",
    "CAMEROUN1313": "Cameroun",
    "COTEIVOIRE452": "Côte D'Ivoire",
    "SENEGAL601": "Sénégal",
    "OUTREMER249": "Outremer",
    "HAITI537": "Haïti",
    "TUNISIE842": "Tunisie",
    "MALI123": "Mali",
    "FRANCE908": "France",
}


TYPEFORM_API_CONFIG = dict(
    API_TOKEN = os.environ.get("TYPEFORM_API_TOKEN"),
    BASE_URL = f"https://api.typeform.com/forms/gAA9HR4K/responses",
)
