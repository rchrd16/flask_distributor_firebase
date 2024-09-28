import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("ladju_distributor.json")
firebase_admin.initialize_app(cred)

# Firestore database instance
db = firestore.client()
