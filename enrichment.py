"""
Enrichissement des données - Analyses avancées
Calculs de métriques RFM, segmentation, tendances
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from data_model import DataModel

class AdvancedAnalytics:
    """Analyses avancées sur les données Northwind"""
    
    def __init__(self, data_model):
        """Initialise avec un modèle de données"""
        self.model = data_model
        self.df = data_model.full_dataset
        self.max_date = self.df['orderDate'].max()
    
    def calculate_rfm(self):
        """
        Calcule les scores RFM (Récence, Fréquence, Montant) par client
        
        Returns:
            DataFrame avec scores RFM et segments
        """
        print("📊 Calcul des scores RFM...")
        
        # Regrouper par client
        rfm = self.df.groupby('customerID').agg({
            'orderDate': lambda x: (self.max_date - x.max()).days,  # Récence
            'orderID': 'nunique',  # Fréquence
            'lineTotal': 'sum'  # Montant
        }).reset_index()
        
        rfm.columns = ['customerID', 'recency', 'frequency', 'monetary']
        
        # Ajouter les informations client
        rfm = rfm.merge(
            self.model.customers[['customerID', 'companyName', 'country']],
            on='customerID',
            how='left'
        )
        
        # Calculer les quartiles pour scoring (1-4)
        rfm['R_score'] = pd.qcut(rfm['recency'], q=4, labels=[4, 3, 2, 1], duplicates='drop')
        rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4], duplicates='drop')
        rfm['M_score'] = pd.qcut(rfm['monetary'].rank(method='first'), q=4, labels=[1, 2, 3, 4], duplicates='drop')
        
        # Score RFM combiné
        rfm['RFM_score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)
        rfm['RFM_total'] = rfm['R_score'].astype(int) + rfm['F_score'].astype(int) + rfm['M_score'].astype(int)
        
        # Segmentation
        def segment_customer(row):
            score = row['RFM_total']
            if score >= 10:
                return 'Champions'
            elif score >= 8:
                return 'Loyal'
            elif score >= 6:
                return 'Potential'
            elif score >= 4:
                return 'At Risk'
            else:
                return 'Lost'
        
        rfm['segment'] = rfm.apply(segment_customer, axis=1)
        
        print(f"   ✅ {len(rfm)} clients analysés")
        return rfm
    
    def analyze_product_performance(self):
        """
        Analyse de performance des produits
        
        Returns:
            DataFrame avec métriques par produit
        """
        print("📦 Analyse de performance produits...")
        
        perf = self.df.groupby(['productID', 'productName', 'categoryName']).agg({
            'lineTotal': ['sum', 'mean', 'count'],
            'quantity': 'sum',
            'discount': 'mean',
            'orderID': 'nunique'
        }).reset_index()
        
        perf.columns = ['productID', 'productName', 'categoryName', 
                        'total_revenue', 'avg_revenue_per_line', 'times_ordered',
                        'total_quantity', 'avg_discount', 'unique_orders']
        
        # Taux de remise moyen
        perf['avg_discount'] = perf['avg_discount'] * 100  # en %
        
        # Contribution au CA total
        total_revenue = perf['total_revenue'].sum()
        perf['revenue_contribution_pct'] = (perf['total_revenue'] / total_revenue * 100).round(2)
        
        # Rang
        perf['revenue_rank'] = perf['total_revenue'].rank(ascending=False, method='min').astype(int)
        
        perf = perf.sort_values('total_revenue', ascending=False)
        
        print(f"   ✅ {len(perf)} produits analysés")
        return perf
    
    def analyze_sales_trends(self):
        """
        Analyse des tendances de ventes
        
        Returns:
            dict avec différentes métriques temporelles
        """
        print("📈 Analyse des tendances...")
        
        df = self.df.copy()
        
        # Ventes par mois
        monthly = df.groupby(df['orderDate'].dt.to_period('M')).agg({
            'lineTotal': 'sum',
            'orderID': 'nunique',
            'quantity': 'sum'
        }).reset_index()
        monthly['orderDate'] = monthly['orderDate'].astype(str)
        monthly.columns = ['month', 'revenue', 'orders', 'quantity']
        
        # Calcul de la croissance mensuelle
        monthly['revenue_growth'] = monthly['revenue'].pct_change() * 100
        
        # Ventes par jour de la semaine
        df['dayofweek'] = df['orderDate'].dt.day_name()
        daily = df.groupby('dayofweek')['lineTotal'].sum().reset_index()
        
        # Réordonner les jours
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily['dayofweek'] = pd.Categorical(daily['dayofweek'], categories=days_order, ordered=True)
        daily = daily.sort_values('dayofweek')
        
        # Ventes par trimestre
        quarterly = df.groupby(df['orderDate'].dt.to_period('Q')).agg({
            'lineTotal': 'sum',
            'orderID': 'nunique'
        }).reset_index()
        quarterly['orderDate'] = quarterly['orderDate'].astype(str)
        quarterly.columns = ['quarter', 'revenue', 'orders']
        
        print(f"   ✅ Tendances calculées")
        
        return {
            'monthly': monthly,
            'daily': daily,
            'quarterly': quarterly
        }
    
    def analyze_cohorts(self):
        """
        Analyse de cohortes basée sur le mois de première commande
        
        Returns:
            DataFrame de rétention par cohorte
        """
        print("👥 Analyse de cohortes...")
        
        df = self.df.copy()
        
        # Identifier la première commande de chaque client
        df['order_month'] = df['orderDate'].dt.to_period('M')
        
        first_orders = df.groupby('customerID')['orderDate'].min().reset_index()
        first_orders['cohort'] = first_orders['orderDate'].dt.to_period('M')
        
        df = df.merge(first_orders[['customerID', 'cohort']], on='customerID', how='left')
        
        # Calculer l'âge de la commande en mois depuis la première commande
        df['order_period'] = (
            (df['order_month'] - df['cohort']).apply(lambda x: x.n)
        )
        
        # Créer la matrice de cohorte
        cohort_data = df.groupby(['cohort', 'order_period'])['customerID'].nunique().reset_index()
        cohort_pivot = cohort_data.pivot_table(
            index='cohort',
            columns='order_period',
            values='customerID'
        )
        
        # Calculer le taux de rétention
        cohort_size = cohort_pivot.iloc[:, 0]
        retention = cohort_pivot.divide(cohort_size, axis=0) * 100
        
        print(f"   ✅ {len(retention)} cohortes analysées")
        
        return retention
    
    def calculate_discount_impact(self):
        """
        Analyse de l'impact des remises sur les ventes
        
        Returns:
            DataFrame avec analyse des remises
        """
        print("💰 Analyse de l'impact des remises...")
        
        df = self.df.copy()
        
        # Créer des catégories de remise
        df['discount_category'] = pd.cut(
            df['discount'],
            bins=[-0.01, 0, 0.05, 0.10, 0.15, 1],
            labels=['No Discount', '1-5%', '6-10%', '11-15%', '>15%']
        )
        
        impact = df.groupby('discount_category').agg({
            'lineTotal': ['sum', 'mean', 'count'],
            'quantity': ['sum', 'mean'],
            'discount': 'mean'
        }).reset_index()
        
        impact.columns = ['discount_category', 'total_revenue', 'avg_order_value', 
                          'order_count', 'total_quantity', 'avg_quantity', 'avg_discount']
        
        impact['avg_discount_pct'] = impact['avg_discount'] * 100
        
        print(f"   ✅ Analyse des remises terminée")
        return impact
    
    def export_enriched_data(self, output_dir='data/enriched'):
        """Exporte toutes les analyses enrichies"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"\n💾 Export des données enrichies vers {output_dir}...")
        
        # RFM
        rfm = self.calculate_rfm()
        rfm.to_csv(output_path / 'rfm_analysis.csv', index=False)
        print(f"   ✅ rfm_analysis.csv")
        
        # Performance produits
        product_perf = self.analyze_product_performance()
        product_perf.to_csv(output_path / 'product_performance.csv', index=False)
        print(f"   ✅ product_performance.csv")
        
        # Tendances
        trends = self.analyze_sales_trends()
        trends['monthly'].to_csv(output_path / 'monthly_trends.csv', index=False)
        trends['daily'].to_csv(output_path / 'daily_trends.csv', index=False)
        trends['quarterly'].to_csv(output_path / 'quarterly_trends.csv', index=False)
        print(f"   ✅ *_trends.csv")
        
        # Impact remises
        discount = self.calculate_discount_impact()
        discount.to_csv(output_path / 'discount_impact.csv', index=False)
        print(f"   ✅ discount_impact.csv")
        
        print("\n✅ Export terminé !")


def main():
    """Lance les analyses enrichies"""
    print("\n" + "="*60)
    print("🚀 ANALYSES AVANCÉES - Enrichissement des données")
    print("="*60 + "\n")
    
    # Charger le modèle
    model = DataModel()
    analytics = AdvancedAnalytics(model)
    
    # Analyse RFM
    print("\n" + "-"*60)
    rfm = analytics.calculate_rfm()
    print("\n📊 Distribution des segments RFM:")
    segment_dist = rfm['segment'].value_counts()
    for segment, count in segment_dist.items():
        pct = count / len(rfm) * 100
        print(f"   {segment:15s} : {count:3d} clients ({pct:5.1f}%)")
    
    # Performance produits
    print("\n" + "-"*60)
    product_perf = analytics.analyze_product_performance()
    print(f"\n🏆 Top 5 produits par contribution au CA:")
    for idx, row in product_perf.head(5).iterrows():
        print(f"   {row['productName'][:40]:40s} : {row['revenue_contribution_pct']:5.2f}%")
    
    # Tendances
    print("\n" + "-"*60)
    trends = analytics.analyze_sales_trends()
    print(f"\n📈 Croissance moyenne mensuelle: {trends['monthly']['revenue_growth'].mean():.2f}%")
    
    # Impact remises
    print("\n" + "-"*60)
    discount = analytics.calculate_discount_impact()
    print(f"\n💰 Impact des remises sur le panier moyen:")
    for idx, row in discount.iterrows():
        print(f"   {str(row['discount_category']):12s} : ${row['avg_order_value']:8.2f}")
    
    # Export
    print("\n" + "-"*60)
    analytics.export_enriched_data()
    
    print("\n" + "="*60)
    print("✅ ANALYSES TERMINÉES")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
