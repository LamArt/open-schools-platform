import firebase_admin
from firebase_admin import credentials
from ..env import env

cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": env("FIREBASE_PROJECT_ID", default=""),
        "private_key_id": env("FIREBASE_PRIVATE_KEY_ID", default=""),
        "private_key": env("FIREBASE_PRIVATE_KEY", default="").replace("\\n", "\n"),
        "client_email": env("FIREBASE_CLIENT_EMAIL", default=""),
        "client_id": env("FIREBASE_CLIENT_ID", default=""),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": env("FIREBASE_CLIENT_CERT_URL", default=""),
    }
)

app = firebase_admin.initialize_app(cred)
