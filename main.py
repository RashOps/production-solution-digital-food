"""
Launch the food script with Streamlit UI
"""
import streamlit as st
import pandas as pd
from food import Food

# Configuration de la page
st.set_page_config(page_title="Food Characteristics Retriever", page_icon="🍎", layout="wide")

# Sidebar pour options supplémentaires
with st.sidebar:
    st.header("Options")
    if st.button("Effacer l'historique"):
        st.session_state.history = []
        st.rerun()
    st.markdown("---")
    st.markdown("**Historique des recherches :**")
    if "history" not in st.session_state:
        st.session_state.history = []
    for item in st.session_state.history[-5:]:  # Afficher les 5 dernières
        st.write(f"- {item}")

# Titre principal avec icône
st.title("🍎 Food Characteristics Retriever")
st.subheader("Récupérez les caractéristiques nutritionnelles : Calories, Protéines, Glucides, Lipides")

# Section de recherche
st.markdown("### 🔍 Recherche d'aliment")
col_input, col_button = st.columns([3, 1])

with col_input:
    aliment = st.text_input("Entrez le nom d'un aliment", value="pomme", placeholder="Ex: pomme, banane...")

with col_button:
    button = st.button("Rechercher", type="primary", use_container_width=True)

# Validation d'entrée
if button and not aliment.strip():
    st.error("Veuillez entrer un nom d'aliment valide.")
    st.stop()

# Section d'affichage des infos
st.markdown("---")
st.markdown("## 📊 Informations nutritionnelles")

# Valeurs par défaut
calories, proteins, carbs, fat, is_fat = 0.0, 0.0, 0.0, 0.0, False
food_name = ""

# Récupération des données avec spinner
if button and aliment.strip():
    with st.spinner("Recherche en cours..."):
        try:
            food = Food()
            food.retrieve_food_infos(str(aliment))
            calories = food.get_calories()
            proteins = food.get_proteins()
            carbs = food.get_carbs()
            fat = food.get_fat()
            is_fat = food.is_fat()
            food_name = aliment

            # Ajouter à l'historique
            if aliment not in st.session_state.history:
                st.session_state.history.append(aliment)

            st.success(f"Données récupérées pour '{aliment}' !")
        except ValueError as e:
            st.error(f"Erreur : {str(e)}")
        except Exception as e:
            st.error(f"Erreur inattendue : {e}")

# Affichage des métriques
if food_name:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Calories", f"{calories} Kcal", delta=None)
    with col2:
        st.metric("Protéines", f"{proteins} g", delta=None)
    with col3:
        st.metric("Glucides", f"{carbs} g", delta=None)
    with col4:
        st.metric("Lipides", f"{fat} g", delta=None)

    # Indicateur gras/non gras
    if is_fat:
        st.warning("⚠️ Aliment considéré comme gras (lipides > 20g)")
    else:
        st.info("✅ Aliment non gras")

    # Graphique en barres
    st.markdown("### 📈 Répartition nutritionnelle")
    data = {"Nutriment": ["Protéines", "Glucides", "Lipides"], "Quantité (g)": [proteins, carbs, fat]}
    df = pd.DataFrame(data)
    st.bar_chart(df.set_index("Nutriment"))

    # Bouton d'export
    if st.button("Exporter en CSV"):
        csv_data = f"name,calories,fat,carbs,proteins\n{food_name},{calories},{fat},{carbs},{proteins}"
        st.download_button("Télécharger CSV", csv_data, file_name=f"{food_name}.csv", mime="text/csv")
else:
    st.info("Entrez un aliment et cliquez sur 'Rechercher' pour afficher les informations.")
