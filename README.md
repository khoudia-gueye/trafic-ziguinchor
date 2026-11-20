# Projet : Gestion Intelligente du Trafic Routier à Ziguinchor

**Université Assane Seck de Ziguinchor (UASZ)**  
**Module :** Innovations Technologiques en Intelligence Artificielle  
**Enseignant :** Dr. Ousseynou Mbaye  
**Groupe 1 :**
* Mame Khoudia Gueye
* Baye Samba Ndiaye
* Fatma Dioum
* Ousmane Kane
* Bassirou Yate

---

## 📁 Contenu des Livrables

Conformément aux exigences officielles du module (Page 8) :

1. **Fiche Problème :** `GRP1.odt`  
   Description complète du problème de circulation à Ziguinchor, des usagers ciblés et de la valeur ajoutée de l'IA.

2. **Jeu de données :** `trafic_ziguinchor.csv`  
   Dataset de 2 500 observations modélisant la circulation sur 5 axes stratégiques de Ziguinchor (Pont Émile Badiane, Marché Saint-Maur, campus UASZ, Boulevard 54m, Tilène).

3. **Notebook Commenté & Modèles Évalués :** `Projet_Trafic_Ziguinchor_Groupe1.ipynb`  
   * **Volet 1 - Régression Linéaire Multiple :** Prédiction du temps de trajet en minutes ($R^2 = 78,2\%$, $RMSE = 1,22\text{ min}$).
   * **Volet 2 - Classification Logistique :** Détection du niveau de congestion ($Accuracy = 90,0\%$, matrice de confusion).

4. **Modèles Enregistrés :**  
   * `modele_regression_trafic.joblib`
   * `modele_classification_trafic.joblib`
   * `colonnes_modele.joblib`

5. **Mini-application Prototype :** `app_trafic_ziguinchor.py`  
   Application web interactive développée avec Streamlit (diagnostic en temps réel, carte interactive de Ziguinchor, recommandations).

6. **Diaporama de Présentation :** `Presentation_Groupe1.pptx`  
   Support pour le pitch final.

---

## 🚀 Instructions d'Exécution

### 1. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 2. Lancement du Notebook Jupyter
```bash
python -m notebook
```
Puis ouvrir `Projet_Trafic_Ziguinchor_Groupe1.ipynb`.

### 3. Lancement de l'Application Streamlit
```bash
streamlit run app_trafic_ziguinchor.py
```
L'application s'ouvre automatiquement dans le navigateur sur `http://localhost:8501`.
