"""
Génération du jeu de données synthétique réaliste pour le projet :
"Gestion intelligente du trafic routier à Ziguinchor"
Groupe 1 - UASZ (Licence 3 Informatique)
"""

import numpy as np
import pandas as pd

# Fixer la graine aléatoire pour la reproductibilité scientifique
np.random.seed(42)

# Définition des axes stratégiques de Ziguinchor et leurs distances moyennes
axes_config = {
    "Pont Emile Badiane": {"distance_km": 3.5, "vitesse_max": 50, "sensibilite_pointe": 1.4},
    "Rond-point Aline Sitoe Diatta - Marche Saint-Maur": {"distance_km": 2.0, "vitesse_max": 35, "sensibilite_pointe": 1.6},
    "Boulevard des 54 metres - Escale": {"distance_km": 2.8, "vitesse_max": 45, "sensibilite_pointe": 1.2},
    "Axe Universite Assane Seck (Nema / Belfort)": {"distance_km": 4.2, "vitesse_max": 45, "sensibilite_pointe": 1.5},
    "Carrefour Tilene - Gare Routiere": {"distance_km": 3.0, "vitesse_max": 38, "sensibilite_pointe": 1.5}
}

jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
etats_route = ["Bon", "Moyen", "Degrade"]
meteos = ["Ensoleille", "Pluvieux"]

n_samples = 2500
records = []

axes_list = list(axes_config.keys())

for _ in range(n_samples):
    axe = np.random.choice(axes_list)
    conf = axes_config[axe]
    distance = conf["distance_km"]
    vitesse_max = conf["vitesse_max"]
    
    jour = np.random.choice(jours_semaine)
    est_weekend = 1 if jour in ["Samedi", "Dimanche"] else 0
    
    # Heure tirée de façon réaliste (plus d'activités entre 6h et 22h)
    if np.random.rand() < 0.85:
        heure = np.random.randint(6, 22)
    else:
        heure = np.random.choice([22, 23, 0, 1, 2, 3, 4, 5])
        
    # Heures de pointe à Ziguinchor : 7h-9h (écoles, bureaux), 13h-14h (déjeuner), 17h-19h (sortie bureaux/marché)
    if not est_weekend and heure in [7, 8, 12, 13, 17, 18, 19]:
        est_heure_pointe = 1
    elif est_weekend and heure in [11, 12, 18, 19]:
        est_heure_pointe = 1
    else:
        est_heure_pointe = 0
        
    etat_route = np.random.choice(etats_route, p=[0.45, 0.35, 0.20])
    # Climat Casamance : hivernage / forte pluie ponctuelle
    meteo = np.random.choice(meteos, p=[0.78, 0.22])
    travaux = np.random.choice([0, 1], p=[0.88, 0.12])
    
    # Volume de véhicules estimé par heure
    base_vehicules = 180 if est_heure_pointe else 70
    if est_weekend:
        base_vehicules *= 0.8
    if axe == "Rond-point Aline Sitoe Diatta - Marche Saint-Maur":
        base_vehicules *= 1.3
    nb_vehicules = int(np.clip(np.random.normal(base_vehicules, 25), 20, 450))
    
    # Calcul de la vitesse réelle impactée par les conditions
    ralentissement = 1.0
    if est_heure_pointe:
        ralentissement *= (1.0 + conf["sensibilite_pointe"] * 0.45)
    if etat_route == "Moyen":
        ralentissement *= 1.15
    elif etat_route == "Degrade":
        ralentissement *= 1.35
    if meteo == "Pluvieux":
        ralentissement *= 1.30
    if travaux == 1:
        ralentissement *= 1.40
        
    vitesse_effective = max(8.0, vitesse_max / ralentissement + np.random.normal(0, 2))
    
    # Temps de trajet en minutes = (distance / vitesse) * 60 + aléa
    temps_min = (distance / vitesse_effective) * 60 + np.random.normal(0, 0.8)
    temps_min = round(max(3.0, temps_min), 1)
    
    # Catégorisation pour la classification (Niveau de congestion)
    if vitesse_effective >= 32.0:
        congestion = "Fluide"
    elif vitesse_effective >= 18.0:
        congestion = "Modere"
    else:
        congestion = "Embouteille"
        
    records.append({
        "axe_routier": axe,
        "distance_km": distance,
        "heure": heure,
        "jour_semaine": jour,
        "est_weekend": est_weekend,
        "est_heure_pointe": est_heure_pointe,
        "etat_route": etat_route,
        "meteo": meteo,
        "travaux_en_cours": travaux,
        "nb_vehicules_estime": nb_vehicules,
        "temps_trajet_min": temps_min,
        "niveau_congestion": congestion
    })

df = pd.DataFrame(records)
csv_path = r"c:\LICENCE INFOMATIQUE\mon_Semestre_6\innovation\trafic_ziguinchor.csv"
df.to_csv(csv_path, index=False, encoding="utf-8")
print(f"Jeu de donnees genere avec succes : {len(df)} lignes !")
print(df.head(5))
print("\nRepartition de la variable cible de Classification (niveau_congestion) :")
print(df["niveau_congestion"].value_counts())
print("\nResume statistique de la variable cible de Regression (temps_trajet_min) :")
print(df["temps_trajet_min"].describe())
