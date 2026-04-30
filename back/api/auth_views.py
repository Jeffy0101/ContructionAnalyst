"""
Vues d'authentification :
- POST /api/auth/register : créer un compte
- POST /api/auth/login    : se connecter, retourne un token JWT
- GET  /api/auth/me       : infos utilisateur courant (vérifie le token)
"""
import jwt
import bcrypt
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .mongo_client import users_col


def make_token(user_id, email):
    """Génère un JWT valable 7 jours."""
    payload = {
        'sub': str(user_id),
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')


def decode_token(token):
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
    except Exception:
        return None


def get_user_from_request(request):
    """Helper : récupère l'user depuis le header Authorization."""
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    payload = decode_token(auth[7:])
    if not payload:
        return None
    user = users_col().find_one({'email': payload['email']})
    return user


@api_view(['POST'])
def register(request):
    email = request.data.get('email', '').lower().strip()
    password = request.data.get('password', '')
    name = request.data.get('name', '').strip()

    if not email or not password or not name:
        return Response({'error': 'Champs requis manquants'}, status=400)
    if len(password) < 6:
        return Response({'error': 'Mot de passe trop court (min 6)'}, status=400)
    if users_col().find_one({'email': email}):
        return Response({'error': 'Email déjà utilisé'}, status=400)

    # Hash bcrypt sécurisé
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    result = users_col().insert_one({
        'email': email, 'password': hashed, 'name': name,
        'created_at': datetime.datetime.utcnow(),
    })
    token = make_token(result.inserted_id, email)
    return Response({'token': token, 'user': {'email': email, 'name': name}})


@api_view(['POST'])
def login(request):
    email = request.data.get('email', '').lower().strip()
    password = request.data.get('password', '')

    user = users_col().find_one({'email': email})
    if not user or not bcrypt.checkpw(password.encode(), user['password'].encode()):
        return Response({'error': 'Identifiants invalides'}, status=401)

    token = make_token(user['_id'], email)
    return Response({'token': token, 'user': {'email': email, 'name': user['name']}})


@api_view(['GET'])
def me(request):
    user = get_user_from_request(request)
    if not user:
        return Response({'error': 'Non authentifié'}, status=401)
    return Response({'email': user['email'], 'name': user['name']})
