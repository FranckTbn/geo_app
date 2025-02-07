import streamlit as st
import requests
import time

# ---------------------------- 🎨 STYLE ----------------------------
st.set_page_config(
    page_title="Analyse d'Adresse",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        h1, h2, h3, h4, h5, h6 {
            color: #00796b; 
            font-family: 'Georgia', serif;
        }
        .stTextInput, .stButton>button {
            border-radius: 8px;
        }
        .stButton>button {
            background-color: #0288d1 !important;
            color: white !important;
            font-size: 16px !important;
            padding: 10px 20px !important;
            transition: 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #004d40 !important;
        }
        .main { background-color: #f5f7fa; }
        .footer { text-align: center; font-size: 12px; color: grey; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------- 🏠 INTERFACE ----------------------------
st.markdown('<h1 style="text-align: center;">🗺️ Analyse d\'Adresse avec FastAPI</h1>', unsafe_allow_html=True)
st.write("Entrez une adresse et obtenez ses composants (numéro, rue, code postal, ville) en quelques secondes !")

# Champ de saisie de l'adresse avec mémoire
adresse = st.text_input("📌 **Adresse complète :**", placeholder="Ex : 12 rue de la paix, 75002 Paris", key="adresse_input")

# Stocker l'état de la requête dans session_state
if "analyse_effectuee" not in st.session_state:
    st.session_state.analyse_effectuee = False

# Bouton pour analyser l'adresse
if st.button("🔍 Analyser l'adresse", key="analyser"):
    if adresse.strip():
        st.session_state.analyse_effectuee = True  # Marquer que la requête est lancée
        st.session_state.result = None  # Réinitialiser l'ancien résultat

# Exécuter la requête seulement si une analyse est demandée
if st.session_state.analyse_effectuee:
    with st.spinner("🔄 Analyse en cours..."):
        url = "http://127.0.0.1:8000/parse-address/"
        data = {"adresse": adresse}

        try:
            response = requests.post(url, json=data)
            time.sleep(1)  # Simuler un léger délai pour l'effet
            if response.status_code == 200:
                st.session_state.result = response.json()
                st.success("✅ Adresse analysée avec succès !")
            else:
                st.error("❌ Erreur lors de l'analyse. Vérifiez que l'API est bien lancée.")
        except requests.exceptions.ConnectionError:
            st.error("🚨 Impossible de se connecter à l'API. Vérifiez qu'elle est en cours d'exécution.")

    # Réinitialisation automatique pour une nouvelle entrée
    st.session_state.analyse_effectuee = False

# Affichage du résultat stocké
if "result" in st.session_state and st.session_state.result:
    st.json(st.session_state.result)

# Footer
st.markdown('<p class="footer">Développé avec ❤️ par <b>TBN</b></p>', unsafe_allow_html=True)

# streamlit run app.py