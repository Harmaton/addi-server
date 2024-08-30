import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseService:
    @staticmethod
    def initialize():
        cred = credentials.Certificate("path/to/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        return firestore.client()

    @staticmethod
    def save_data(collection, data):
        db = FirebaseService.initialize()
        db.collection(collection).add(data)