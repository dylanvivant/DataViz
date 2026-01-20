"""
Modèle de données - Création des relations entre tables
Prépare les DataFrames pour les visualisations Dash
"""

import pandas as pd
import numpy as np
from pathlib import Path

CLEANED_DIR = Path("data/cleaned")


class DataModel:
    """Classe pour gérer le modèle de données avec relations"""
    
    def __init__(self):
        """Charge les données nettoyées"""
        print("📂 Chargement des données nettoyées...")
        
        self.customers = pd.read_csv(CLEANED_DIR / "customers_clean.csv")
        self.products = pd.read_csv(CLEANED_DIR / "products_clean.csv")
        self.categories = pd.read_csv(CLEANED_DIR / "categories_clean.csv")
        self.orders = pd.read_csv(CLEANED_DIR / "orders_clean.csv", parse_dates=['orderDate', 'requiredDate', 'shippedDate'])
        self.order_details = pd.read_csv(CLEANED_DIR / "order_details_clean.csv")
        
        print(f"   ✅ Données chargées")
        
        # Créer les vues enrichies
        self._create_views()
    
    def _create_views(self):
        """Crée des vues enrichies avec jointures"""
        print("\n🔗 Création des vues avec relations...")
        
        # Vue complète : order_details + products + categories
        self.order_details_enriched = self.order_details.merge(
            self.products[['productID', 'productName', 'categoryID', 'supplierID']],
            on='productID',
            how='left'
        ).merge(
            self.categories[['categoryID', 'categoryName']],
            on='categoryID',
            how='left'
        )
        print(f"   ✅ order_details_enriched créé ({len(self.order_details_enriched)} lignes)")
        
        # Vue commandes complètes : orders + customers
        self.orders_enriched = self.orders.merge(
            self.customers[['customerID', 'companyName', 'country', 'city', 'region']],
            on='customerID',
            how='left'
        )
        print(f"   ✅ orders_enriched créé ({len(self.orders_enriched)} lignes)")
        
        # Vue complète : tout ensemble
        # order_details -> products -> categories + orders -> customers
        self.full_dataset = self.order_details_enriched.merge(
            self.orders_enriched,
            on='orderID',
            how='left'
        )
        print(f"   ✅ full_dataset créé ({len(self.full_dataset)} lignes)")
        
    def get_sales_by_period(self, period='M'):
        """
        Retourne les ventes groupées par période
        
        Args:
            period: 'D' (jour), 'W' (semaine), 'M' (mois), 'Y' (année)
        """
        df = self.full_dataset.copy()
        df['period'] = df['orderDate'].dt.to_period(period)
        
        sales = df.groupby('period').agg({
            'lineTotal': 'sum',
            'orderID': 'nunique',
            'quantity': 'sum'
        }).reset_index()
        
        sales.columns = ['period', 'revenue', 'orders_count', 'items_sold']
        sales['period'] = sales['period'].astype(str)
        
        return sales
    
    def get_top_products(self, top_n=10):
        """Retourne les N produits les plus vendus"""
        top = self.full_dataset.groupby('productName').agg({
            'lineTotal': 'sum',
            'quantity': 'sum'
        }).reset_index().sort_values('lineTotal', ascending=False).head(top_n)
        
        top.columns = ['productName', 'revenue', 'quantity_sold']
        return top
    
    def get_sales_by_country(self):
        """Retourne les ventes par pays"""
        sales = self.full_dataset.groupby('country').agg({
            'lineTotal': 'sum',
            'orderID': 'nunique',
            'customerID': 'nunique'
        }).reset_index().sort_values('lineTotal', ascending=False)
        
        sales.columns = ['country', 'revenue', 'orders_count', 'customers_count']
        return sales
    
    def get_sales_by_category(self):
        """Retourne les ventes par catégorie"""
        sales = self.full_dataset.groupby('categoryName').agg({
            'lineTotal': 'sum',
            'quantity': 'sum'
        }).reset_index().sort_values('lineTotal', ascending=False)
        
        sales.columns = ['categoryName', 'revenue', 'quantity_sold']
        return sales
    
    def get_customer_stats(self):
        """Retourne les statistiques par client"""
        stats = self.full_dataset.groupby(['customerID', 'companyName', 'country']).agg({
            'lineTotal': 'sum',
            'orderID': 'nunique',
            'quantity': 'sum'
        }).reset_index().sort_values('lineTotal', ascending=False)
        
        stats.columns = ['customerID', 'companyName', 'country', 'revenue', 'orders_count', 'items_purchased']
        stats['avg_order_value'] = stats['revenue'] / stats['orders_count']
        
        return stats
    
    def get_kpi_summary(self):
        """Retourne les KPIs principaux"""
        total_revenue = self.full_dataset['lineTotal'].sum()
        total_orders = self.full_dataset['orderID'].nunique()
        total_customers = self.full_dataset['customerID'].nunique()
        avg_order_value = total_revenue / total_orders
        
        return {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'total_customers': total_customers,
            'avg_order_value': avg_order_value,
            'total_products': len(self.products),
            'active_products': self.full_dataset['productID'].nunique()
        }
    
    def get_filtered_data(self, start_date=None, end_date=None, countries=None, categories=None):
        """
        Retourne les données filtrées selon les critères
        
        Args:
            start_date: date de début (str ou datetime)
            end_date: date de fin (str ou datetime)
            countries: liste de pays
            categories: liste de catégories
        """
        df = self.full_dataset.copy()
        
        if start_date:
            df = df[df['orderDate'] >= pd.to_datetime(start_date)]
        
        if end_date:
            df = df[df['orderDate'] <= pd.to_datetime(end_date)]
        
        if countries:
            df = df[df['country'].isin(countries)]
        
        if categories:
            df = df[df['categoryName'].isin(categories)]
        
        return df


def main():
    """Teste le modèle de données"""
    print("\n" + "="*60)
    print("🚀 TEST DU MODÈLE DE DONNÉES")
    print("="*60 + "\n")
    
    # Initialiser le modèle
    model = DataModel()
    
    # Afficher les KPIs
    print("\n📊 KPIs Principaux:")
    kpis = model.get_kpi_summary()
    print(f"   💰 Chiffre d'affaires total : ${kpis['total_revenue']:,.2f}")
    print(f"   📦 Nombre de commandes     : {kpis['total_orders']:,}")
    print(f"   👥 Nombre de clients       : {kpis['total_customers']:,}")
    print(f"   💵 Panier moyen            : ${kpis['avg_order_value']:,.2f}")
    print(f"   🏷️  Produits au catalogue   : {kpis['total_products']:,}")
    print(f"   ✅ Produits vendus         : {kpis['active_products']:,}")
    
    # Top 5 produits
    print("\n🏆 Top 5 Produits:")
    top_products = model.get_top_products(5)
    for idx, row in top_products.iterrows():
        print(f"   {idx+1}. {row['productName'][:40]:40s} - ${row['revenue']:,.2f}")
    
    # Top 5 pays
    print("\n🌍 Top 5 Pays:")
    top_countries = model.get_sales_by_country().head(5)
    for idx, row in top_countries.iterrows():
        print(f"   {idx+1}. {row['country']:20s} - ${row['revenue']:,.2f}")
    
    # Ventes par catégorie
    print("\n📂 Ventes par Catégorie:")
    sales_cat = model.get_sales_by_category()
    for idx, row in sales_cat.iterrows():
        print(f"   - {row['categoryName']:20s} - ${row['revenue']:,.2f}")
    
    print("\n" + "="*60)
    print("✅ MODÈLE DE DONNÉES PRÊT")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
