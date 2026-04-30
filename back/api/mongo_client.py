"""
Client MongoDB — singleton réutilisable dans toutes les vues.
On expose 3 collections : users, analyses, datasets.
"""
from pymongo import MongoClient
from django.conf import settings

_client = None

def get_db():
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGO_URI)
    return _client[settings.MONGO_DB]

def users_col():
    return get_db()['users']

def analyses_col():
    return get_db()['analyses']
