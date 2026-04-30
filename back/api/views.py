from django.shortcuts import render

# Create your views here.
"""
Vues API — endpoints d'analyse :
  POST /api/analyser    : nouvelle analyse de terrain
  GET  /api/historique  : analyses de l'utilisateur connecté
  GET  /api/dataset     : échantillon pour graphiques globaux
  GET  /api/features    : liste des variables attendues
"""
import datetime
from bson import ObjectId
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .ml_engine import ENGINE, FEATURES
from .auth_views import get_user_from_request
from .mongo_client import analyses_col


@api_view(['GET'])
def features(request):
    return Response({'features': FEATURES})


@api_view(['POST'])
def analyser(request):
    user = get_user_from_request(request)
    if not user:
        return Response({'error': 'Non authentifié'}, status=401)

    donnees = request.data.get('donnees', {})
    nom_terrain = request.data.get('nom_terrain', 'Terrain sans nom')
    localisation = request.data.get('localisation', '')

    # Validation : toutes les features doivent être présentes
    manquantes = [f for f in FEATURES if f not in donnees]
    if manquantes:
        return Response({'error': f'Variables manquantes : {manquantes}'}, status=400)

    try:
        resultat = ENGINE.predire(donnees)
    except Exception as e:
        return Response({'error': f'Erreur ML : {e}'}, status=500)

    # Sauvegarde MongoDB
    doc = {
        'user_email': user['email'],
        'nom_terrain': nom_terrain,
        'localisation': localisation,
        'donnees': donnees,
        'resultat': resultat,
        'date': datetime.datetime.utcnow(),
    }
    inserted = analyses_col().insert_one(doc)
    resultat['analyse_id'] = str(inserted.inserted_id)
    return Response(resultat)


@api_view(['GET'])
def historique(request):
    user = get_user_from_request(request)
    if not user:
        return Response({'error': 'Non authentifié'}, status=401)

    docs = list(analyses_col().find(
        {'user_email': user['email']}
    ).sort('date', -1).limit(50))

    for d in docs:
        d['_id'] = str(d['_id'])
        d['date'] = d['date'].isoformat()
    return Response({'analyses': docs})


@api_view(['GET'])
def dataset(request):
    return Response({
        'sample': ENGINE.get_dataset_sample(200),
        'metrics': ENGINE.metrics,
    })
