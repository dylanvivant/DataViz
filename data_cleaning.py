"""
Script de nettoyage et typage des données CSV
Prépare les données pour la visualisation Dash
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Répertoire des données
DATA_DIR = Path("data")
CLEANED_DIR = Path("data/cleaned")
CLEANED_DIR.mkdir(exist_ok=True)


def clean_customers():
    """Nettoie et type le fichier customers.csv"""
    print("🧹 Nettoyage de customers.csv...")
    
    df = pd.read_csv(DATA_DIR / "customers.csv")
    
    # Remplacer 'NULL' par NaN
    df = df.replace('NULL', np.nan)
    
    # Types de colonnes
    df['customerID'] = df['customerID'].astype(str)
    df['companyName'] = df['companyName'].astype(str)
    
    # Sauvegarder
    df.to_csv(CLEANED_DIR / "customers_clean.csv", index=False)
    print(f"   ✅ {len(df)} clients nettoyés")
    return df


def clean_products():
    """Nettoie et type le fichier products.csv"""
    print("🧹 Nettoyage de products.csv...")
    
    df = pd.read_csv(DATA_DIR / "products.csv")
    
    # Remplacer 'NULL' par NaN
    df = df.replace('NULL', np.nan)
    
    # Types de colonnes
    df['productID'] = df['productID'].astype(int)
    df['productName'] = df['productName'].astype(str)
    df['supplierID'] = pd.to_numeric(df['supplierID'], errors='coerce').astype('Int64')
    df['categoryID'] = pd.to_numeric(df['categoryID'], errors='coerce').astype('Int64')
    df['unitPrice'] = pd.to_numeric(df['unitPrice'], errors='coerce')
    df['unitsInStock'] = pd.to_numeric(df['unitsInStock'], errors='coerce').astype('Int64')
    df['unitsOnOrder'] = pd.to_numeric(df['unitsOnOrder'], errors='coerce').astype('Int64')
    df['reorderLevel'] = pd.to_numeric(df['reorderLevel'], errors='coerce').astype('Int64')
    df['discontinued'] = df['discontinued'].astype(int)
    
    # Sauvegarder
    df.to_csv(CLEANED_DIR / "products_clean.csv", index=False)
    print(f"   ✅ {len(df)} produits nettoyés")
    return df


def clean_orders():
    """Nettoie et type le fichier orders.csv"""
    print("🧹 Nettoyage de orders.csv...")
    
    df = pd.read_csv(DATA_DIR / "orders.csv")
    
    # Remplacer 'NULL' par NaN
    df = df.replace('NULL', np.nan)
    
    # Types de colonnes
    df['orderID'] = df['orderID'].astype(int)
    df['customerID'] = df['customerID'].astype(str)
    df['employeeID'] = pd.to_numeric(df['employeeID'], errors='coerce').astype('Int64')
    
    # Conversion des dates
    date_columns = ['orderDate', 'requiredDate', 'shippedDate']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Types numériques
    df['shipVia'] = pd.to_numeric(df['shipVia'], errors='coerce').astype('Int64')
    df['freight'] = pd.to_numeric(df['freight'], errors='coerce')
    
    # Sauvegarder
    df.to_csv(CLEANED_DIR / "orders_clean.csv", index=False)
    print(f"   ✅ {len(df)} commandes nettoyées")
    print(f"   📅 Période : {df['orderDate'].min()} à {df['orderDate'].max()}")
    return df


def clean_order_details():
    """Nettoie et type le fichier order_details.csv"""
    print("🧹 Nettoyage de order_details.csv...")
    
    df = pd.read_csv(DATA_DIR / "order_details.csv")
    
    # Types de colonnes
    df['orderID'] = df['orderID'].astype(int)
    df['productID'] = df['productID'].astype(int)
    df['unitPrice'] = pd.to_numeric(df['unitPrice'], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').astype('Int64')
    df['discount'] = pd.to_numeric(df['discount'], errors='coerce')
    
    # Calculer le montant total par ligne
    df['lineTotal'] = df['unitPrice'] * df['quantity'] * (1 - df['discount'])
    
    # Sauvegarder
    df.to_csv(CLEANED_DIR / "order_details_clean.csv", index=False)
    print(f"   ✅ {len(df)} lignes de détails nettoyées")
    return df


def clean_categories():
    """Nettoie et type le fichier categories.csv"""
    print("🧹 Nettoyage de categories.csv...")
    
    df = pd.read_csv(DATA_DIR / "categories.csv")
    df = df.replace('NULL', np.nan)
    
    df['categoryID'] = df['categoryID'].astype(int)
    df['categoryName'] = df['categoryName'].astype(str)
    
    df.to_csv(CLEANED_DIR / "categories_clean.csv", index=False)
    print(f"   ✅ {len(df)} catégories nettoyées")
    return df


def main():
    """Lance le nettoyage de tous les fichiers"""
    print("\n" + "="*60)
    print("🚀 NETTOYAGE DES DONNÉES - TP DataViz")
    print("="*60 + "\n")
    
    # Nettoyer les fichiers principaux
    customers_df = clean_customers()
    products_df = clean_products()
    orders_df = clean_orders()
    order_details_df = clean_order_details()
    categories_df = clean_categories()
    
    print("\n" + "="*60)
    print("✅ NETTOYAGE TERMINÉ")
    print("="*60)
    print(f"📁 Fichiers nettoyés dans : {CLEANED_DIR}")
    print("\n📊 Résumé :")
    print(f"   - Clients      : {len(customers_df):,}")
    print(f"   - Produits     : {len(products_df):,}")
    print(f"   - Commandes    : {len(orders_df):,}")
    print(f"   - Détails      : {len(order_details_df):,}")
    print(f"   - Catégories   : {len(categories_df):,}")
    print()


if __name__ == "__main__":
    main()
