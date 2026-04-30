"""
Moteur ML — calcule le risque d'un terrain à partir des variables collectées.

Techniques implémentées (programme EC2 INF232) :
  1. Régression linéaire SIMPLE  : risque vs pente
  2. Régression linéaire MULTIPLE : risque vs toutes variables
  3. Réduction de dimensionnalité : ACP (PCA) + variance expliquée
  4. Classification SUPERVISÉE   : RandomForest (faible/moyen/élevé)
  5. Classification NON-SUPERVISÉE : KMeans (3 clusters de terrains)

On génère un dataset synthétique réaliste de 500 terrains au démarrage,
puis on entraîne tous les modèles. Les nouveaux terrains soumis sont
prédits par les modèles entraînés.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score


# ============================================================
# 1. GÉNÉRATION DU DATASET SYNTHÉTIQUE
# ============================================================
# Variables collectées (3 catégories : géotech / hydro / urbanisme)
FEATURES = [
    # Géotechnique
    'capacite_portante',     # kPa  (50 → 500)
    'pente',                 # %    (0 → 45)
    'zone_sismique',         # 1→5
    'profondeur_nappe',      # m    (0 → 30)
    'type_sol_score',        # 1=argile mou … 5=roche
    # Hydrologie & climat
    'pluviometrie_annuelle', # mm   (300 → 3000)
    'distance_cours_eau',    # m    (0 → 5000)
    'risque_inondation',     # 0→10
    'qualite_drainage',      # 1→5
    # Environnement & urbanisme
    'distance_route',        # m
    'densite_urbaine',       # hab/km²
    'distance_industrie',    # m
    'couverture_vegetale',   # %
    'altitude',              # m
    'exposition_vent',       # 1→5
]


def generer_dataset(n=500, seed=42):
    """Crée un dataset réaliste avec une cible 'risque' calculée logiquement."""
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        'capacite_portante':     rng.uniform(50, 500, n),
        'pente':                 rng.uniform(0, 45, n),
        'zone_sismique':         rng.integers(1, 6, n),
        'profondeur_nappe':      rng.uniform(0, 30, n),
        'type_sol_score':        rng.integers(1, 6, n),
        'pluviometrie_annuelle': rng.uniform(300, 3000, n),
        'distance_cours_eau':    rng.uniform(0, 5000, n),
        'risque_inondation':     rng.uniform(0, 10, n),
        'qualite_drainage':      rng.integers(1, 6, n),
        'distance_route':        rng.uniform(0, 5000, n),
        'densite_urbaine':       rng.uniform(0, 10000, n),
        'distance_industrie':    rng.uniform(0, 10000, n),
        'couverture_vegetale':   rng.uniform(0, 100, n),
        'altitude':              rng.uniform(0, 3000, n),
        'exposition_vent':       rng.integers(1, 6, n),
    })

    # Cible CONTINUE : score de risque 0–100 (formule pondérée logique)
    risque = (
        + 0.20 * df['pente'] * 1.5
        + 0.18 * df['zone_sismique'] * 8
        + 0.15 * df['risque_inondation'] * 4
        - 0.12 * (df['capacite_portante'] / 5)
        - 0.10 * (df['profondeur_nappe'])
        + 0.10 * (10 - df['qualite_drainage']) * 3
        - 0.05 * (df['distance_cours_eau'] / 200)
        + 0.05 * (5 - df['type_sol_score']) * 4
        + rng.normal(0, 5, n)  # bruit
    )
    df['risque'] = np.clip(risque, 0, 100)

    # Cible CATÉGORIELLE pour la classification supervisée
    df['classe_risque'] = pd.cut(
        df['risque'], bins=[-1, 33, 66, 101],
        labels=['Faible', 'Moyen', 'Élevé']
    ).astype(str)
    return df


# ============================================================
# 2. CLASSE MOTEUR — entraîne tous les modèles une fois
# ============================================================
class MLEngine:
    def __init__(self):
        self.df = generer_dataset()
        self.scaler = StandardScaler()
        X = self.df[FEATURES].values
        y_reg = self.df['risque'].values
        y_clf = self.df['classe_risque'].values

        X_scaled = self.scaler.fit_transform(X)

        # 1. Régression simple : risque ~ pente
        self.lr_simple = LinearRegression().fit(
            self.df[['pente']].values, y_reg
        )

        # 2. Régression multiple : risque ~ toutes variables
        self.lr_multi = LinearRegression().fit(X_scaled, y_reg)

        # 3. ACP — réduction à 2 composantes pour visualisation
        self.pca = PCA(n_components=2).fit(X_scaled)

        # 4. Classification supervisée
        self.rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_scaled, y_clf)

        # 5. Clustering non-supervisé
        self.kmeans = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X_scaled)

        # Métriques
        self.metrics = {
            'r2_simple': float(r2_score(y_reg, self.lr_simple.predict(self.df[['pente']].values))),
            'r2_multiple': float(r2_score(y_reg, self.lr_multi.predict(X_scaled))),
            'rmse_multiple': float(np.sqrt(mean_squared_error(y_reg, self.lr_multi.predict(X_scaled)))),
            'accuracy_rf': float(accuracy_score(y_clf, self.rf.predict(X_scaled))),
            'pca_variance': self.pca.explained_variance_ratio_.tolist(),
        }

    def predire(self, donnees: dict):
        """Prend les variables d'un terrain → retourne analyse complète."""
        x = np.array([[donnees[f] for f in FEATURES]])
        x_scaled = self.scaler.transform(x)

        risque_score = float(self.lr_multi.predict(x_scaled)[0])
        risque_score = max(0, min(100, risque_score))
        classe = str(self.rf.predict(x_scaled)[0])
        proba = self.rf.predict_proba(x_scaled)[0]
        cluster = int(self.kmeans.predict(x_scaled)[0])
        coords_pca = self.pca.transform(x_scaled)[0].tolist()

        # Importance des variables (pour graphique)
        importances = dict(zip(FEATURES, self.rf.feature_importances_.tolist()))

        # Recommandation textuelle
        if risque_score < 33:
            verdict = "Terrain ADÉQUAT pour construction. Peu de précautions nécessaires."
        elif risque_score < 66:
            verdict = "Terrain CONSTRUCTIBLE SOUS CONDITIONS. Études complémentaires recommandées."
        else:
            verdict = "Terrain À RISQUE ÉLEVÉ. Construction déconseillée ou nécessite mesures lourdes."

        # Projection 5 ans (analyse future simple : si pluies augmentent / urbanisation…)
        risque_5ans = min(100, risque_score * 1.08)  # +8% scénario tendanciel
        risque_10ans = min(100, risque_score * 1.15)

        return {
            'risque_score': round(risque_score, 2),
            'classe': classe,
            'probabilites': {
                'Faible': float(proba[list(self.rf.classes_).index('Faible')]) if 'Faible' in self.rf.classes_ else 0,
                'Moyen': float(proba[list(self.rf.classes_).index('Moyen')]) if 'Moyen' in self.rf.classes_ else 0,
                'Élevé': float(proba[list(self.rf.classes_).index('Élevé')]) if 'Élevé' in self.rf.classes_ else 0,
            },
            'cluster': cluster,
            'coords_pca': coords_pca,
            'importances': importances,
            'verdict': verdict,
            'projection': {
                'actuel': round(risque_score, 2),
                'risque_5ans': round(risque_5ans, 2),
                'risque_10ans': round(risque_10ans, 2),
            },
            'metrics_modeles': self.metrics,
        }

    def get_dataset_sample(self, n=100):
        """Retourne un échantillon du dataset pour les graphiques côté Streamlit."""
        sample = self.df.sample(min(n, len(self.df)), random_state=1)
        # Ajoute coords PCA et clusters pour viz
        X_scaled = self.scaler.transform(sample[FEATURES].values)
        coords = self.pca.transform(X_scaled)
        sample = sample.copy()
        sample['pca1'] = coords[:, 0]
        sample['pca2'] = coords[:, 1]
        sample['cluster'] = self.kmeans.predict(X_scaled)
        return sample.to_dict(orient='records')


# Singleton global — entraîné une seule fois au démarrage
ENGINE = MLEngine()
