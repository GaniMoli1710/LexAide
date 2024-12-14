import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\mailt\OneDrive\Desktop\LexAide\lexaide-f6ed3-firebase-adminsdk-5cwyp-543fe4e7ce.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)