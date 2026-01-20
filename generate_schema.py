"""
Génération du schéma relationnel de la base de données Northwind
Crée un diagramme visuel des relations entre les tables
"""

try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
from pathlib import Path

def create_database_schema():
    """Crée le schéma relationnel avec Graphviz"""
    
    # Créer un graphique dirigé
    dot = graphviz.Digraph(
        'Northwind_Schema',
        comment='Schéma Relationnel Northwind',
        format='png',
        engine='dot'
    )
    
    # Configuration globale
    dot.attr(rankdir='LR', bgcolor='#f8f9fa', fontname='Arial')
    dot.attr('node', shape='plaintext', fontname='Arial')
    dot.attr('edge', color='#495057', fontname='Arial', fontsize='10')
    
    # Table CUSTOMERS
    customers_table = '''<
    <TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" BGCOLOR="#e7f3ff">
        <TR><TD COLSPAN="2" BGCOLOR="#0d6efd"><FONT COLOR="white"><B>CUSTOMERS</B></FONT></TD></TR>
        <TR><TD ALIGN="LEFT"><U>customerID</U></TD><TD ALIGN="LEFT">PK</TD></TR>
        <TR><TD ALIGN="LEFT">companyName</TD><TD ALIGN="LEFT">VARCHAR</TD></TR>
        <TR><TD ALIGN="LEFT">contactName</TD><TD ALIGN="LEFT">VARCHAR</TD></TR>
        <TR><TD ALIGN="LEFT">country</TD><TD ALIGN="LEFT">VARCHAR</TD></TR>
        <TR><TD ALIGN="LEFT">city</TD><TD ALIGN="LEFT">VARCHAR</TD></TR>
    </TABLE>>'''
    
    # Table ORDERS
    orders_table = '''<
    <TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" BGCOLOR="#fff3cd">
        <TR><TD COLSPAN="2" BGCOLOR="#ffc107"><FONT COLOR="black"><B>ORDERS</B></FONT></TD></TR>
        <TR><TD ALIGN="LEFT"><U>orderID</U></TD><TD ALIGN="LEFT">PK</TD></TR>
        <TR><TD ALIGN="LEFT"><I>customerID</I></TD><TD ALIGN="LEFT">FK</TD></TR>
        <TR><TD ALIGN="LEFT">employeeID</TD><TD ALIGN="LEFT">INT</TD></TR>
        <TR><TD ALIGN="LEFT">orderDate</TD><TD ALIGN="LEFT">DATE</TD></TR>
        <TR><TD ALIGN="LEFT">shipCountry</TD><TD ALIGN="LEFT">VARCHAR</TD></TR>
    </TABLE>>'''
    
    # Table ORDER_DETAILS
    order_details_table = '''<
    <TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" BGCOLOR="#d1e7dd">
        <TR><TD COLSPAN="2" BGCOLOR="#198754"><FONT COLOR="white"><B>ORDER_DETAILS</B></FONT></TD></TR>
        <TR><TD ALIGN="LEFT"><I>orderID</I></TD><TD ALIGN="LEFT">FK</TD></TR>
        <TR><TD ALIGN="LEFT"><I>productID</I></TD><TD ALIGN="LEFT">FK</TD></TR>
        <TR><TD ALIGN="LEFT">unitPrice</TD><TD ALIGN="LEFT">DECIMAL</TD></TR>
        <TR><TD ALIGN="LEFT">quantity</TD><TD ALIGN="LEFT">INT</TD></TR>
        <TR><TD ALIGN="LEFT">discount</TD><TD ALIGN="LEFT">DECIMAL</TD></TR>
    </TABLE>>'''
    
    # Table PRODUCTS
    products_table = '''<
    <TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" BGCOLOR="#f8d7da">
        <TR><TD COLSPAN="2" BGCOLOR="#dc3545"><FONT COLOR="white"><B>PRODUCTS</B></FONT></TD></TR>
        <TR><TD ALIGN="LEFT"><U>productID</U></TD><TD ALIGN="LEFT">PK</TD></TR>
        <TR><TD ALIGN="LEFT">productName</TD><TD ALIGN="LEFT">VARCHAR</TD></TR>
        <TR><TD ALIGN="LEFT"><I>categoryID</I></TD><TD ALIGN="LEFT">FK</TD></TR>
        <TR><TD ALIGN="LEFT">unitPrice</TD><TD ALIGN="LEFT">DECIMAL</TD></TR>
        <TR><TD ALIGN="LEFT">unitsInStock</TD><TD ALIGN="LEFT">INT</TD></TR>
    </TABLE>>'''
    
    # Table CATEGORIES
    categories_table = '''<
    <TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" BGCOLOR="#e2d9f3">
        <TR><TD COLSPAN="2" BGCOLOR="#6f42c1"><FONT COLOR="white"><B>CATEGORIES</B></FONT></TD></TR>
        <TR><TD ALIGN="LEFT"><U>categoryID</U></TD><TD ALIGN="LEFT">PK</TD></TR>
        <TR><TD ALIGN="LEFT">categoryName</TD><TD ALIGN="LEFT">VARCHAR</TD></TR>
        <TR><TD ALIGN="LEFT">description</TD><TD ALIGN="LEFT">TEXT</TD></TR>
    </TABLE>>'''
    
    # Ajouter les nœuds
    dot.node('customers', customers_table)
    dot.node('orders', orders_table)
    dot.node('order_details', order_details_table)
    dot.node('products', products_table)
    dot.node('categories', categories_table)
    
    # Ajouter les relations
    dot.edge('customers', 'orders', label='1:N', fontsize='12', fontcolor='#0d6efd', color='#0d6efd', penwidth='2')
    dot.edge('orders', 'order_details', label='1:N', fontsize='12', fontcolor='#ffc107', color='#ffc107', penwidth='2')
    dot.edge('products', 'order_details', label='1:N', fontsize='12', fontcolor='#dc3545', color='#dc3545', penwidth='2')
    dot.edge('categories', 'products', label='1:N', fontsize='12', fontcolor='#6f42c1', color='#6f42c1', penwidth='2')
    
    return dot


def create_text_schema():
    """Crée un schéma texte simple"""
    schema = """
╔══════════════════════════════════════════════════════════════════════════╗
║              SCHÉMA RELATIONNEL - BASE DE DONNÉES NORTHWIND              ║
╚══════════════════════════════════════════════════════════════════════════╝

┌─────────────────────┐
│     CUSTOMERS       │
├─────────────────────┤
│ • customerID (PK)   │
│   companyName       │
│   contactName       │
│   country           │
│   city              │
└──────────┬──────────┘
           │ 1:N
           ▼
┌─────────────────────┐
│       ORDERS        │
├─────────────────────┤
│ • orderID (PK)      │
│   customerID (FK) ──┘
│   employeeID        │
│   orderDate         │
│   shipCountry       │
└──────────┬──────────┘
           │ 1:N
           ▼
┌─────────────────────┐         ┌─────────────────────┐
│   ORDER_DETAILS     │    N:1  │      PRODUCTS       │
├─────────────────────┤◄────────┤─────────────────────┤
│   orderID (FK)      │         │ • productID (PK)    │
│   productID (FK)    │─────────┤   productName       │
│   unitPrice         │         │   categoryID (FK) ──┐
│   quantity          │         │   unitPrice         │
│   discount          │         │   unitsInStock      │
└─────────────────────┘         └─────────────────────┘
                                            │ N:1
                                            ▼
                                ┌─────────────────────┐
                                │     CATEGORIES      │
                                ├─────────────────────┤
                                │ • categoryID (PK)   │
                                │   categoryName      │
                                │   description       │
                                └─────────────────────┘

LÉGENDE :
  • PK = Clé Primaire (Primary Key)
  • FK = Clé Étrangère (Foreign Key)
  • 1:N = Relation Un à Plusieurs
  • N:1 = Relation Plusieurs à Un

RELATIONS :
  1. Un CLIENT peut avoir PLUSIEURS COMMANDES
  2. Une COMMANDE peut avoir PLUSIEURS LIGNES DE DÉTAILS
  3. Un PRODUIT peut être dans PLUSIEURS LIGNES DE DÉTAILS
  4. Une CATÉGORIE contient PLUSIEURS PRODUITS
"""
    return schema


def main():
    """Génère les schémas"""
    print("\n" + "="*70)
    print("📊 GÉNÉRATION DU SCHÉMA RELATIONNEL")
    print("="*70 + "\n")
    
    output_dir = Path("schema")
    output_dir.mkdir(exist_ok=True)
    
    # Générer le schéma Graphviz si disponible
    if GRAPHVIZ_AVAILABLE:
        try:
            print("🎨 Génération du schéma graphique...")
            dot = create_database_schema()
            dot.render(output_dir / 'schema_relationnel', cleanup=True)
            print(f"   ✅ {output_dir}/schema_relationnel.png")
        except Exception as e:
            print(f"   ⚠️  Erreur Graphviz : {e}")
    else:
        print("   ⚠️  Graphviz non installé (optionnel)")
        print("   💡 Pour installer : pip install graphviz")
        print("   💡 Et Graphviz : https://graphviz.org/download/")
    
    # Générer le schéma texte
    print("\n📝 Génération du schéma texte...")
    text_schema = create_text_schema()
    with open(output_dir / 'schema_relationnel.txt', 'w', encoding='utf-8') as f:
        f.write(text_schema)
    print(f"   ✅ {output_dir}/schema_relationnel.txt")
    
    # Afficher le schéma texte
    print("\n" + "="*70)
    print(text_schema)
    print("="*70)
    print(f"\n✅ Schémas générés dans le dossier '{output_dir}/'")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
