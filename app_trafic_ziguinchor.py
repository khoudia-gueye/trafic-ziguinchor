"""
=============================================================================
ZIG-RIDE IA • MOBILITÉ URBAINE ZIGUINCHOR
Design : Style "Yango / Uber" (Application VTC & Mobilité Urbaine)
=============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="ZIG-RIDE • Mobilité Ziguinchor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Chargement des ressources ML
DOSSIER = os.path.dirname(os.path.abspath(__file__))
PATH_REG = os.path.join(DOSSIER, "modele_regression_trafic.joblib")
PATH_CLF = os.path.join(DOSSIER, "modele_classification_trafic.joblib")
PATH_COLS = os.path.join(DOSSIER, "colonnes_modele.joblib")
PATH_CSV = os.path.join(DOSSIER, "trafic_ziguinchor.csv")

@st.cache_resource
def charger_ressources():
    df = pd.read_csv(PATH_CSV) if os.path.exists(PATH_CSV) else None
    m_reg = joblib.load(PATH_REG) if os.path.exists(PATH_REG) else None
    m_clf = joblib.load(PATH_CLF) if os.path.exists(PATH_CLF) else None
    cols = joblib.load(PATH_COLS) if os.path.exists(PATH_COLS) else None
    return df, m_reg, m_clf, cols

df_global, modele_reg, modele_clf, colonnes_modele = charger_ressources()

# Points d'intérêt et coordonnées réelles à Ziguinchor
lieux_ziguinchor = {
    "Rond-point Aline Sitoé Diatta (Marché Saint-Maur)": {
        "lat": 12.5820, "lon": -16.2745, "secteur": "Centre-ville commercial"
    },
    "Pont Émile Badiane (Entrée Nord)": {
        "lat": 12.5895, "lon": -16.2714, "secteur": "Franchissement fleuve Casamance"
    },
    "Campus Université (Néma / Belfort)": {
        "lat": 12.5650, "lon": -16.2820, "secteur": "Zone universitaire"
    },
    "Boulevard des 54 mètres (Escale)": {
        "lat": 12.5855, "lon": -16.2700, "secteur": "Cité administrative & Port"
    },
    "Gare Routière de Tilène": {
        "lat": 12.5760, "lon": -16.2650, "secteur": "Pôle transports interurbains"
    },
    "Hôpital Silence (Boucotte)": {
        "lat": 12.5710, "lon": -16.2730, "secteur": "Quartier résidentiel & Santé"
    }
}

# Style CSS : reproduction de l'expérience mobile Yango / Uber
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Outfit:wght@600;700;800;900&display=swap');
    
    html, body, [class*="css"], .stApp {
        background-color: #f1f3f5 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #111827 !important;
    }
    
    /* Masquer la sidebar par défaut */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    .main .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1320px !important;
    }
    
    /* Top Bar Yango / Uber */
    .yango-topbar {
        background: #111827;
        color: #ffffff;
        border-radius: 20px;
        padding: 16px 26px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    }
    .yango-logo {
        font-family: 'Outfit', sans-serif;
        font-size: 24px;
        font-weight: 900;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .yango-badge {
        background: #ef4444;
        color: #ffffff;
        font-size: 11px;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 980px;
        letter-spacing: 0.5px;
    }
    
    /* Panneau de Commande (Booking Card) */
    .booking-card {
        background: #ffffff;
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        border: 1px solid #e5e7eb;
    }
    .booking-title {
        font-size: 18px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 16px;
    }
    
    /* Input Points A et B */
    .route-input-group {
        position: relative;
        padding-left: 28px;
        margin-bottom: 18px;
    }
    .route-input-group::before {
        content: '';
        position: absolute;
        left: 8px;
        top: 22px;
        bottom: 22px;
        width: 2px;
        background: #d1d5db;
    }
    .dot-a {
        position: absolute;
        left: 4px;
        top: 10px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
    }
    .dot-b {
        position: absolute;
        left: 4px;
        bottom: 10px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #ef4444;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2);
    }
    
    /* Options de Véhicules VTC */
    .ride-option {
        background: #ffffff;
        border: 2px solid #e5e7eb;
        border-radius: 18px;
        padding: 16px 20px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    .ride-option:hover {
        border-color: #111827;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    }
    .ride-option.selected {
        border-color: #111827;
        background: #f9fafb;
    }
    
    /* Bouton principal géant Yango */
    div.stButton > button:first-child {
        background: #111827 !important;
        color: #ffffff !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 17px !important;
        font-weight: 800 !important;
        border-radius: 16px !important;
        padding: 16px 28px !important;
        border: none !important;
        width: 100% !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:first-child:hover {
        background: #000000 !important;
        transform: scale(1.01) !important;
    }
    
    /* Cartes de résultats */
    .result-banner {
        background: #ffffff;
        border-radius: 20px;
        padding: 22px 26px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Barre de navigation supérieure Yango Style
st.markdown("""
<div class="yango-topbar">
    <div class="yango-logo">
        <span>🚗</span> ZIG-RIDE <span class="yango-badge">IA EN DIRECT</span>
    </div>
    <div style="font-size: 13px; font-weight: 600; color: #9ca3af;">
        Ziguinchor · Mobilité Intelligente & VTC
    </div>
</div>
""", unsafe_allow_html=True)

# Disposition en 2 colonnes style Yango :
# Gauche (Panneau de commande VTC 38%) | Droite (Carte & Télémétrie 62%)
col_vtc, col_carte = st.columns([1.15, 1.85], gap="large")

# =============================================================================
# COLONNE GAUCHE : COMMANDE & PARAMÈTRES (STYLE YANGO)
# =============================================================================
with col_vtc:
    st.markdown('<div class="booking-card">', unsafe_allow_html=True)
    st.markdown('<div class="booking-title">Où allez-vous ?</div>', unsafe_allow_html=True)
    
    lieux_cles = list(lieux_ziguinchor.keys())
    
    # Sélecteurs de points A et B avec indicateurs colorés
    st.markdown('<div class="route-input-group">', unsafe_allow_html=True)
    st.markdown('<div class="dot-a"></div>', unsafe_allow_html=True)
    point_depart = st.selectbox("Point de départ (A)", lieux_cles, index=0)
    st.markdown('<div class="dot-b"></div>', unsafe_allow_html=True)
    point_arrivee = st.selectbox("Destination (B)", lieux_cles, index=1)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Calcul de distance approximative entre les points
    coord_a = lieux_ziguinchor[point_depart]
    coord_b = lieux_ziguinchor[point_arrivee]
    
    # Distance géodésique euclidienne approximée en km
    d_lat = (coord_b["lat"] - coord_a["lat"]) * 111.0
    d_lon = (coord_b["lon"] - coord_a["lon"]) * 108.0
    distance_estimee = round(max(1.5, np.sqrt(d_lat**2 + d_lon**2) * 1.3), 1)
    
    st.markdown("---")
    st.markdown("**Conditions du trajet :**")
    
    c_h, c_j = st.columns(2)
    with c_h:
        heure_depart = st.selectbox("Heure", [f"{h}h00" for h in range(24)], index=8)
        heure_num = int(heure_depart.replace("h00", ""))
    with c_j:
        jour_course = st.selectbox("Jour", ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])
        
    c_met, c_cha = st.columns(2)
    with c_met:
        meteo_course = st.selectbox("Météo", ["Ensoleillé", "Pluie (Hivernage)"])
    with c_cha:
        etat_course = st.selectbox("État chaussée", ["Bon", "Moyen", "Dégradé"])
        
    travaux_flag = st.checkbox("🚧 Travaux ou ralentissements signalés", value=False)
    
    btn_simuler = st.button("CALCULER L'ITINÉRAIRE")
    st.markdown('</div>', unsafe_allow_html=True)

# Déduction Machine Learning
est_weekend = 1 if jour_course in ["Samedi", "Dimanche"] else 0
if not est_weekend and heure_num in [7, 8, 12, 13, 17, 18, 19]:
    est_heure_pointe = 1
elif est_weekend and heure_num in [11, 12, 18, 19]:
    est_heure_pointe = 1
else:
    est_heure_pointe = 0

base_veh = 220 if est_heure_pointe else 70
if est_weekend:
    base_veh = int(base_veh * 0.8)

# Détection de l'axe principal concerné
if "Badiane" in point_depart or "Badiane" in point_arrivee:
    axe_modele = "Pont Emile Badiane"
elif "Aline" in point_depart or "Aline" in point_arrivee:
    axe_modele = "Rond-point Aline Sitoe Diatta - Marche Saint-Maur"
elif "Universit" in point_depart or "Universit" in point_arrivee:
    axe_modele = "Axe Universite Assane Seck (Nema / Belfort)"
elif "Boulevard" in point_depart or "Boulevard" in point_arrivee:
    axe_modele = "Boulevard des 54 metres - Escale"
else:
    axe_modele = "Carrefour Tilene - Gare Routiere"

meteo_val = "Pluvieux" if "Pluie" in meteo_course else "Ensoleille"
etat_val = "Degrade" if "Dégradé" in etat_course else etat_course

if modele_reg is not None and modele_clf is not None and colonnes_modele is not None:
    dict_x = {
        "axe_routier": [axe_modele],
        "distance_km": [distance_estimee],
        "heure": [heure_num],
        "jour_semaine": [jour_course],
        "est_weekend": [est_weekend],
        "est_heure_pointe": [est_heure_pointe],
        "etat_route": [etat_val],
        "meteo": [meteo_val],
        "travaux_en_cours": [1 if travaux_flag else 0],
        "nb_vehicules_estime": [base_veh]
    }
    df_x = pd.get_dummies(pd.DataFrame(dict_x)).reindex(columns=colonnes_modele, fill_value=0)
    temps_trajet = round(max(3.0, float(modele_reg.predict(df_x)[0])), 1)
    statut_congestion = str(modele_clf.predict(df_x)[0])
    vitesse_moyenne = round((distance_estimee / (temps_trajet / 60.0)), 1)
else:
    temps_trajet = 7.5
    statut_congestion = "Modere"
    vitesse_moyenne = 26.0

# Estimation des tarifs en Francs CFA (Ziguinchor)
tarif_taxi = int(500 + (distance_estimee * 150) + (temps_trajet * 30))
tarif_jakarta = int(300 + (distance_estimee * 100) + (temps_trajet * 15))
tarif_confort = int(tarif_taxi * 1.5)

# Temps pour la moto Jakarta (se faufile plus vite dans les bouchons !)
temps_jakarta = round(max(2.5, temps_trajet * 0.75 if statut_congestion != "Fluide" else temps_trajet * 0.9), 1)

# =============================================================================
# COLONNE DROITE : CARTE & ESTIMATIONS YANGO
# =============================================================================
with col_carte:
    # 1. Carte interactive du trajet
    st.markdown('<div class="result-banner">', unsafe_allow_html=True)
    
    c_info_a, c_info_b = st.columns(2)
    with c_info_a:
        st.markdown(f"**🟢 Départ :** {point_depart}")
    with c_info_b:
        st.markdown(f"**🔴 Arrivée :** {point_arrivee}")
        
    df_pts = pd.DataFrame([
        {"Lieu": point_depart, "latitude": coord_a["lat"], "longitude": coord_a["lon"]},
        {"Lieu": point_arrivee, "latitude": coord_b["lat"], "longitude": coord_b["lon"]}
    ])
    st.map(df_pts, latitude="latitude", longitude="longitude", size=45, zoom=12)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. Diagnostic IA du trafic
    st.markdown('<div class="result-banner">', unsafe_allow_html=True)
    
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        st.metric("📏 Distance", f"{distance_estimee} km")
    with col_t2:
        st.metric("⏱️ Temps Estimé (IA)", f"{temps_trajet} min", delta="Heure de pointe" if est_heure_pointe else "Fluide")
    with col_t3:
        badge_style = {
            "Fluide": ("🟢 Fluide", "#10b981", "Voie dégagée"),
            "Modere": ("🟠 Ralenti", "#f59e0b", "Ralentissements"),
            "Embouteille": ("🔴 Bouché", "#ef4444", "Embouteillage")
        }.get(statut_congestion, ("🟠 Modéré", "#f59e0b", "Normal"))
        st.metric("🚦 État du Trafic", badge_style[0], badge_style[2])
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. Grille de Choix des Véhicules (Style Yango / Uber)
    st.markdown("##### Choisissez votre moyen de transport :")
    
    v1, v2, v3 = st.columns(3)
    
    with v1:
        st.markdown(f"""
        <div class="ride-option selected">
            <div>
                <div style="font-size: 26px;">🚕</div>
                <div style="font-weight: 800; font-size: 16px; margin-top: 4px;">Taxi Clando</div>
                <div style="font-size: 13px; color: #6b7280;">~{temps_trajet} min</div>
            </div>
            <div style="text-align: right;">
                <div style="font-weight: 900; font-size: 18px; color: #111827;">{tarif_taxi} F</div>
                <div style="font-size: 11px; color: #10b981; font-weight: 700;">Le plus prisé</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with v2:
        st.markdown(f"""
        <div class="ride-option">
            <div>
                <div style="font-size: 26px;">🏍️</div>
                <div style="font-weight: 800; font-size: 16px; margin-top: 4px;">Moto Jakarta</div>
                <div style="font-size: 13px; color: #10b981; font-weight: 700;">~{temps_jakarta} min (Rapide)</div>
            </div>
            <div style="text-align: right;">
                <div style="font-weight: 900; font-size: 18px; color: #111827;">{tarif_jakarta} F</div>
                <div style="font-size: 11px; color: #6b7280;">Économique</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with v3:
        st.markdown(f"""
        <div class="ride-option">
            <div>
                <div style="font-size: 26px;">🚘</div>
                <div style="font-weight: 800; font-size: 16px; margin-top: 4px;">Taxi Privé</div>
                <div style="font-size: 13px; color: #6b7280;">~{temps_trajet} min</div>
            </div>
            <div style="text-align: right;">
                <div style="font-weight: 900; font-size: 18px; color: #111827;">{tarif_confort} F</div>
                <div style="font-size: 11px; color: #6b7280;">Climatisé</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # Conseil et itinéraire de contournement
    if statut_congestion == "Embouteille":
        st.warning(f"⚠️ **Forte affluence sur l'axe {axe_modele} !** Les motos Jakarta circulent beaucoup plus rapidement lors des congestions.")
    elif "Pluie" in meteo_course:
        st.info("🌧️ **Alerte Hivernage :** Les pluies en Casamance ralentissent la circulation de 25%. Conduisez prudemment.")
