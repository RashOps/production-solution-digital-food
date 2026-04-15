"""
Launch the food script with Streamlit UI
"""
import streamlit as st
from food import Food

# Title
st.title("Food Characteristics retriever")
st.subheader("Retrieve any food characteristics : Calorie, Fat, Carbs, Proteins")

# Search line
aliment_col, button_aliment_col = st.columns(2)

# Aliment
aliment = st.text_input("Entrez le nom d'un aliment", value="pomme")
button = st.button(label="Recherche", key="food-retrieve", type="primary")
st.space("xsmall")

# Foods infos
st.markdown("## ---------------------- Food infos ----------------------", text_alignment="center")


# Valeurs par défaut
calories, proteins, carbs, fat, is_fat = 73.0, 0.4, 17.0, 0.4, False

# Aliment retrieval 
if button:                          
    try:
        food = Food()
        food.retrieve_food_infos(str(aliment))
        calories = food.get_calories()
        proteins = food.get_proteins()
        carbs    = food.get_carbs()
        fat      = food.get_fat()
        is_fat   = food.is_fat()
    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Erreur inattendue : {e}")


# Sections
col_1, col_2 = st.columns(2, vertical_alignment="bottom", border=True) 
col_3, col_4 = st.columns(2, vertical_alignment="bottom", border=True) 

# Sections badges
with col_1:
    st.badge("Calories", color="orange")
    st.metric(label="Kcal", value=calories)

with col_2:
    st.badge("Proteins", color="gray")
    st.metric(label="grammes", value=proteins)

with col_3:
    st.badge("Carbs", color="violet")
    st.metric(label="grammes", value=carbs)

with col_4:
    st.badge("Fat", color="yellow")
    st.metric(label="grammes", value=fat)

if not is_fat:
    st.info("Aliment non gras", icon="🆗")
else:
    st.warning("Aliment gras", icon="🚨")
    