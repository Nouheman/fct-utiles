("""
PREMIER DEFI (en deux parties) 
1) Créer une fonction unicite(df,colonne) qui teste sur une colonne d'une DF si les clés sont bien uniques ( ce qui est très important, parce que si une clé identifie deux produits différents, on est mal ) 
2) Créer une fonction info(df,colonne,id) qui affiche la ligne d'un produit ou d'un client en fonction de l'id ( pour explorer la spécificité d'un individu au sens statistique )
@everyone DEUXIEME DEFI ( very important) 
""")
# Fonction de base pour vérifier l'unicité des valeurs dans une colonne d'un DataFrame
import pandas as pd

def unicite(df, colonne):
    """Vérifie si les valeurs d'une colonne sont uniques"""
    return df[colonne].is_unique

def info(df, colonne, id):
    """Affiche la ligne d'un individu spécifique identifié par son ID"""
    return df[df[colonne] == id]


("""
 créer une fonction summarize (df) qui permet d'afficher en 1 seule Dataframe et pour toutes les colonnes :

1) Calcul des statistiques de base, que les variables soient numériques ou non 
2) NAN sur une colonne : OUI ou NON 
3) Calcul du pourcentage de valeurs manquantes 
4) Doublons sur colonne : OUI ou NON 
5) Calcul du pourcentage des doublons 
6) Calcul du nombre de valeurs uniques 
7) Affichage du tableau de corrélation sous forme de Heatmap ( revoir Live Coding 5 : Regression Lineaire Univariée )

Optionnel mais recommandé 
8) Affichage du pairplot si il y a un nombre raisonnable de colonnes dans dans notre DF, sinon, c'est illisible , OU affichage du pairplot par morceaux ( par exemple pas plus de 10x10 graphiques ) 
9) Affichage d'un boxplot d'une colonne ou d'un ensemble de colonnes 
10) Afficher en rouge les cellules ou NaN = OUI , ou pourcentage de NaN > 0 , de même pour les doublons , pour qu'avec un seul coup d'oeil vous sachiez ou vous devez intervenir 
""")

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

def summarize(df, max_cols=10):
    """Génère un résumé complet du dataframe avec visualisations"""
    # Résumé statistique des colonnes
    summary = []
    
    for col in df.columns:
        col_data = {
            'Colonne': col,
            'Type': df[col].dtype,
            'Valeurs uniques': df[col].nunique(),
            'NaN': df[col].isnull().any(),
            'Pourcentage NaN': df[col].isnull().mean() * 100,
            'Doublons': df[col].duplicated().any(),
            'Pourcentage Doublons': df[col].duplicated().mean() * 100,
        }
        
        if pd.api.types.is_numeric_dtype(df[col]):
            col_data.update({
                'Moyenne': df[col].mean(),
                'Médiane': df[col].median(),
                'Écart-type': df[col].std(),
                'Min': df[col].min(),
                'Max': df[col].max(),
                '25%': df[col].quantile(0.25),
                '75%': df[col].quantile(0.75)
            })
        else:
            col_data.update({
                'Valeurs distinctes': df[col].nunique(),
                'Exemples': df[col].unique()[:5]  # Premiers exemples
            })
        
        summary.append(col_data)
    
    summary_df = pd.DataFrame(summary)
    
    # Afficher le résumé statistique
    print("=== RÉSUMÉ DU DATAFRAME ===")
    display(summary_df)
    
    # Afficher la heatmap de corrélation
    print("\n=== HEATMAP DE CORRÉLATION ===")
    plt.figure(figsize=(10, 8))
    numeric_df = df.select_dtypes(include=np.number)
    if not numeric_df.empty:
        corr = numeric_df.corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .5})
        plt.title('Heatmap de corrélation')
        plt.show()
    else:
        print("Aucune colonne numérique pour la corrélation.")
    
    # Afficher le pairplot par morceaux
    print("\n=== PAIRPLOT ===")
    numeric_cols = df.select_dtypes(include=np.number).columns
    
    if len(numeric_cols) > 0:
        # Afficher par groupes de max_cols colonnes
        for i in range(0, len(numeric_cols), max_cols):
            cols_subset = numeric_cols[i:i+max_cols]
            if len(cols_subset) > 1:
                sns.pairplot(df[cols_subset])
                plt.suptitle(f'Pairplot (Colonnes {i+1} à {i+len(cols_subset)})', y=1.02)
                plt.show()
            elif len(cols_subset) == 1:
                print(f"Une seule colonne numérique trouvée ({cols_subset[0]}), pas de pairplot nécessaire.")
    else:
        print("Aucune colonne numérique pour le pairplot.")
    
    # Afficher les boxplots par groupes
    print("\n=== BOXPLOTS ===")
    if len(numeric_cols) > 0:
        # Afficher par groupes de max_cols colonnes
        for i in range(0, len(numeric_cols), max_cols):
            cols_subset = numeric_cols[i:i+max_cols]
            fig, axes = plt.subplots(1, len(cols_subset), figsize=(15, 5))
            
            if len(cols_subset) == 1:
                axes = [axes]
            
            for ax, col in zip(axes, cols_subset):
                sns.boxplot(y=df[col], ax=ax)
                ax.set_title(f'Boxplot de {col}')
            
            plt.tight_layout()
            plt.show()
    else:
        print("Aucune colonne numérique pour les boxplots.")
    
    # Fonction pour colorer les cellules selon les conditions
    def highlight_cells(val):
        color = ''
        if isinstance(val, bool) and val:
            return 'background-color: red'
        elif isinstance(val, float) and val > 0 and ('NaN' in str(val) or 'Doublons' in str(val)):
            return 'background-color: red'
        return ''
    
    # Appliquer le style au résumé
    print("\n=== RÉSUMÉ MIS EN FORME ===")
    styled_summary = summary_df.style.apply(lambda row: [highlight_cells(cell) for cell in row], axis=1)
    display(styled_summary)
