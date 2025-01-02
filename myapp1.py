import streamlit as st
import pandas as pd
from PIL import Image
import joblib

# Charger le modèle, le scaler et la liste des features nécessaires
try:
    model = joblib.load("xgb_best_model.pkl")  # Modèle ML
    scaler = joblib.load("scaler.pkl")  # Scaler pré-entraîné
    selected_features = joblib.load("features_list.pkl")  # Liste des features utilisées lors de l'entraînement
except Exception as e:
    st.error(f"⚠️ Erreur lors du chargement des fichiers nécessaires : {e}")

# Barre latérale avec image et description
try:
    sidebar_image = Image.open("shield.png")  # Remplacez par votre image
    st.sidebar.image(sidebar_image, caption="Sécurité IoT", use_container_width=True)
except Exception:
    st.sidebar.warning("⚠️ Impossible de charger l'image. Assurez-vous que le fichier 'shield.png' existe.")

st.sidebar.write("### Type d'Attaque")
class_mapping = {
    0: "ARP_poisioning",
    1: "DDOS_Slowloris",
    2: "DOS_SYN_Hping",
    3: "Metasploit_Brute_Force_SSH",
    4: "NMAP_FIN_SCAN",
    5: "NMAP_OS_DETECTION",
    6: "NMAP_TCP_scan",
    7: "NMAP_UDP_SCAN",
    8: "NMAP_XMAS_TREE_SCAN",
    9: "Normal"
}
class_mapping_df = pd.DataFrame(list(class_mapping.items()), columns=["Code", "Classe"])
st.sidebar.table(class_mapping_df)

# Titre et description principale
st.title("Système de Détection d'Attaques IoT")
st.write("""
### Bienvenue dans le Système de Détection d'Attaques IoT !
Cet outil prédit le type d'attaque dans un réseau IoT en fonction des caractéristiques du trafic réseau.

#### Étapes d'utilisation :
1. Téléchargez un fichier CSV contenant les features nécessaires.
2. Consultez le type d'attaque dans la barre latérale.
3. Obtenez les prédictions basées sur vos données.
""")

# Charger le fichier CSV
st.header("📂 Charger votre fichier CSV")
uploaded_file = st.file_uploader("Téléchargez votre fichier CSV avec les features requises", type=["csv"])

if uploaded_file:
    try:
        # Charger les données
        input_data = pd.read_csv(uploaded_file)
        st.success("✅ Fichier chargé avec succès ! Voici un aperçu des données :")
        st.write(input_data.head())

        # Vérifier si toutes les colonnes nécessaires sont présentes
        missing_features = [feature for feature in selected_features if feature not in input_data.columns]
        if missing_features:
            st.error(f"⚠️ Les colonnes suivantes manquent dans votre fichier : {missing_features}")
        else:
            # Extraire uniquement les colonnes nécessaires
            input_data = input_data[selected_features]

            # Standardiser les données
            input_data_scaled = scaler.transform(input_data)

            # Vérifier si l'utilisateur souhaite effectuer des prédictions
            if st.button("Prédire"):
                try:
                    predictions = model.predict(input_data_scaled)
                    input_data["Prédictions"] = predictions
                    input_data["Type d'Attaque"] = input_data["Prédictions"].map(class_mapping)

                    st.success("✅ Prédictions réalisées avec succès !")
                    st.write(input_data.head())

                    # Exporter les prédictions en CSV
                    csv = input_data.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="Télécharger les prédictions au format CSV",
                        data=csv,
                        file_name="predictions.csv",
                        mime="text/csv",
                    )
                except Exception as pred_error:
                    st.error(f"⚠️ Une erreur s'est produite lors des prédictions : {pred_error}")
    except Exception as e:
        st.error(f"⚠️ Une erreur s'est produite lors du chargement du fichier : {e}")
else:
    st.warning("⚠️ Veuillez télécharger un fichier CSV pour continuer.")

# Footer
st.markdown("---")
st.markdown("Propulsé par **Streamlit** | Conçu pour l'analyse de sécurité IoT")
