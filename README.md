# 📊 Dashboard Northwind - Analyse des Ventes

Projet de Data Visualisation avec Dash - Analyse interactive des données de vente Northwind

## 🎯 Objectifs du TP

1. ✅ **Nettoyage des données** : Typage des colonnes, gestion des valeurs NULL, conversion des dates
2. ✅ **Modèle relationnel** : Création des relations entre tables via clés primaires/étrangères
3. ✅ **Visualisation interactive** : Dashboard Dash avec filtres dynamiques
4. ✅ **Enrichissement** : Métriques avancées et optimisations

## 📁 Structure du Projet

```
DataViz/
├── data/                          # Données brutes
│   ├── customers.csv
│   ├── orders.csv
│   ├── order_details.csv
│   ├── products.csv
│   ├── categories.csv
│   └── cleaned/                   # Données nettoyées (généré)
│       ├── customers_clean.csv
│       ├── orders_clean.csv
│       ├── order_details_clean.csv
│       ├── products_clean.csv
│       └── categories_clean.csv
├── data_cleaning.py               # Script de nettoyage
├── data_model.py                  # Modèle de données avec relations
├── app.py                         # Application Dash principale
├── requirements.txt               # Dépendances Python
└── README.md                      # Documentation
```

## 🔑 Clés Primaires et Relations

### Tables et Clés

- **customers.csv** : `customerID` (PK)
- **orders.csv** : `orderID` (PK), `customerID` (FK)
- **products.csv** : `productID` (PK), `categoryID` (FK)
- **categories.csv** : `categoryID` (PK)
- **order_details.csv** : `orderID` (FK) + `productID` (FK) - Table de jointure

### Relations

```
customers (1) ─── (N) orders (1) ─── (N) order_details (N) ─── (1) products (N) ─── (1) categories
```

## 🚀 Installation et Lancement

### Option A : Avec Docker (Recommandé) 🐳

```bash
# Démarrer
docker-compose up -d --build

# Arrêter
docker-compose down
```

Accès : http://localhost:8050

### Option B : Installation Locale

#### 1. Installation des dépendances

```bash
pip install -r requirements.txt
```

#### 2. Nettoyage des données

```bash
python data_cleaning.py
```

Résultat :

- Conversion des dates (format ISO)
- Typage des colonnes numériques
- Remplacement de "NULL" par NaN
- Création du dossier `data/cleaned/`

#### 3. Test du modèle de données

```bash
python data_model.py
```

Affiche :

- KPIs principaux
- Top 5 produits
- Top 5 pays
- Ventes par catégorie

#### 4. Lancement du dashboard

```bash
python app.py
```

Accès : http://127.0.0.1:8050

## 📊 Fonctionnalités du Dashboard

### KPIs Principaux

- 💰 **Chiffre d'Affaires Total** : ~$1.27M
- 📦 **Nombre de Commandes** : 830
- 👥 **Nombre de Clients** : 89
- 💵 **Panier Moyen** : ~$1,525

### Visualisations

1. **Évolution des Ventes** : Graphique en aires montrant l'évolution mensuelle du CA
2. **Ventes par Catégorie** : Pie chart interactif
3. **Top 10 Produits** : Classement des produits les plus vendus
4. **Carte Géographique** : Distribution des ventes par pays
5. **Top Clients** : Classement des meilleurs clients

### Filtres Interactifs

- 📅 **Période** : Sélection de dates de début et fin
- 🌍 **Pays** : Filtrage multi-sélection
- 📂 **Catégories** : Filtrage par catégories de produits

## 🧹 Processus de Nettoyage

### Problèmes traités

1. **Valeurs NULL** : Conversion de "NULL" (texte) → NaN (pandas)
2. **Dates** : Format timestamp → datetime pandas
3. **Types numériques** :
   - `unitPrice`, `freight`, `discount` → float
   - `quantity`, `unitsInStock` → Int64 (nullable integer)
4. **Calculs dérivés** :
   - `lineTotal = unitPrice × quantity × (1 - discount)`

### Exemple de code

```python
# Conversion des dates
df['orderDate'] = pd.to_datetime(df['orderDate'], errors='coerce')

# Types numériques nullable
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').astype('Int64')

# Remplacement NULL
df = df.replace('NULL', np.nan)
```

## 🔗 Modèle de Données

### Classes principales

- **DataModel** : Classe principale gérant les données
  - `orders_enriched` : Orders + Customers
  - `order_details_enriched` : Order Details + Products + Categories
  - `full_dataset` : Jointure complète de toutes les tables

### Méthodes utiles

```python
model = DataModel()

# KPIs
kpis = model.get_kpi_summary()

# Top produits
top_products = model.get_top_products(10)

# Ventes par pays
sales_country = model.get_sales_by_country()

# Données filtrées
filtered = model.get_filtered_data(
    start_date='1997-01-01',
    countries=['France', 'Germany']
)
```

## 📈 Statistiques Clés

### Top 5 Produits

1. Côte de Blaye : $141,396
2. Thüringer Rostbratwurst : $80,368
3. Raclette Courdavault : $71,155
4. Tarte au sucre : $47,234
5. Camembert Pierrot : $46,825

### Top 5 Pays

1. USA : $245,584
2. Germany : $230,284
3. Austria : $128,003
4. Brazil : $106,925
5. France : $81,358

### Répartition par Catégorie

1. Beverages : $267,868 (21%)
2. Dairy Products : $234,507 (19%)
3. Confections : $167,357 (13%)
4. Meat/Poultry : $163,022 (13%)
5. Seafood : $131,261 (10%)

## 🎨 Technologies Utilisées

- **Dash 2.18.2** : Framework web pour dashboards interactifs
- **Plotly 5.24.1** : Graphiques interactifs (inclus avec Dash)
- **Pandas 2.2.3** : Manipulation et analyse de données
- **NumPy 1.26.4** : Calculs numériques
- **Dash Bootstrap Components 1.6.0** : Composants UI Bootstrap

## 💡 Pistes d'Enrichissement

### Analyses Avancées

- [ ] Analyse RFM (Récence, Fréquence, Montant)
- [ ] Segmentation clients (K-means clustering)
- [ ] Prévisions de ventes (séries temporelles)
- [ ] Analyse de panier (association rules)
- [ ] Taux de rétention clients

### Visualisations Supplémentaires

- [ ] Heatmap des ventes par jour de la semaine
- [ ] Analyse des délais de livraison
- [ ] Performance par employé
- [ ] Analyse des remises (impact sur CA)
- [ ] Tableau de bord temps réel

### Optimisations

- [ ] Cache des données avec `@cache`
- [ ] Pagination des tableaux
- [ ] Export PDF/Excel des rapports
- [ ] Mode responsive mobile
- [ ] Thèmes dark/light

## 📝 Notes de Développement

### Callbacks Dash

- Tous les graphiques sont mis à jour via un seul callback pour optimiser les performances
- Les filtres déclenchent automatiquement le recalcul
- Format des dates : DD/MM/YYYY pour l'interface FR

### Performance

- Données chargées une seule fois au démarrage
- Filtrage côté serveur (pandas)
- ~2155 lignes dans le dataset complet

## 🐛 Dépannage

### Erreur d'import Dash

```bash
pip install --upgrade dash dash-bootstrap-components
```

### Problème de dates

Vérifiez le format dans les CSV (ISO 8601 recommandé)

### Port 8050 déjà utilisé

Modifiez dans `app.py` :

```python
app.run_server(debug=True, port=8051)
```

## 📚 Ressources

- [Documentation Dash](https://dash.plotly.com/)
- [Plotly Graph Reference](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)

---

**Auteur** : TP DataViz  
**Date** : Janvier 2026  
**Version** : 1.0
