# auth.py

from config import APP_ACCESS_TOKENS

def authenticate_token(token: str) -> str:
    """
    Retourne le nom de l'équipe associée à un token, sinon None.
    """
    return APP_ACCESS_TOKENS.get(token)
