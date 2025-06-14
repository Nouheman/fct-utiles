import pandas as pd
from df_analyzer import unicite, info, summarize

# Charger un jeu de données d'exemple (Iris)
try:
    df = pd.read_csv('iris.csv')
except FileNotFoundError:
    print("⚠️ Fichier 'iris.csv' non trouvé. Téléchargez-le avec :")
    print("curl -O https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv")
    exit()

# Ajouter une colonne ID unique pour tester la fonction 'unicite'
df['ID'] = range(1, len(df)+1)

# 1. Tester la fonction 'unicite'
print("\n=== TEST unicite() ===")
print("Colonne 'ID' unique ?", unicite(df, 'ID'))  # Devrait retourner True
print("Colonne 'species' unique ?", unicite(df, 'species'))  # Devrait retourner False

# 2. Tester la fonction 'info'
print("\n=== TEST info() ===")
print("Informations sur l'ID=50 :")
print(info(df, 'ID', 50))  # Affiche la 50e fleur

# 3. Tester la fonction 'summarize'
print("\n=== TEST summarize() ===")
summarize(df)