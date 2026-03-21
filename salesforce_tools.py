from simple_salesforce import Salesforce
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def conectar_salesforce():
    """Conecta ao Salesforce apenas com login e senha via OAuth2."""
    try:
        # Opção 1 — login direto sem token (mais simples)
        sf = Salesforce(
            username=os.getenv("SF_USERNAME"),
            password=os.getenv("SF_PASSWORD"),
            security_token="",  # deixa vazio
            domain=os.getenv("SF_DOMAIN", "login"),
            version="58.0"
        )
        return sf

    except Exception:
        # Opção 2 — via OAuth2 com client credentials
        url = f"https://{os.getenv('SF_DOMAIN', 'login')}.salesforce.com/services/oauth2/token"
        payload = {
            "grant_type": "password",
            "client_id": os.getenv("SF_CLIENT_ID", ""),
            "client_secret": os.getenv("SF_CLIENT_SECRET", ""),
            "username": os.getenv("SF_USERNAME"),
            "password": os.getenv("SF_PASSWORD")
        }
        r = requests.post(url, data=payload)
        token = r.json().get("access_token")
        instance = r.json().get("instance_url")

        sf = Salesforce(
            instance_url=instance,
            session_id=token
        )
        return sf
