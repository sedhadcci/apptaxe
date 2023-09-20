import io
import streamlit as st
import pandas as pd

# Chargement du fichier de base depuis GitHub
@st.cache_data
def load_base_data():
    base_url = "https://github.com/sedhadcci/Applisteprefectorale/raw/main/ListeprefectoralBASE.xlsx"
    return pd.read_excel(base_url, header=None)

# Fonction pour effectuer la correspondance
def perform_lookup(input_codes, base_df):
    filter_condition = base_df.iloc[:, 0].isin(input_codes)
    result_df = base_df[filter_condition]
    return result_df

# Interface Streamlit
st.title("Application pour correspondance de CODE")

uploaded_file = st.file_uploader("Choisissez un fichier Excel avec les codes", type=["xlsx"])

if uploaded_file:
    input_df = pd.read_excel(uploaded_file)
    input_codes = input_df.iloc[:, 0].dropna().tolist()
    
    base_df = load_base_data()
    base_df.dropna(subset=[0], inplace=True)

    # Spécifiez les colonnes à utiliser
    base_columns = [0, 4, 5, 8, 18, 11, 13, 14, 21, 16]

    # Filtrer les colonnes
    base_df_filtered = base_df.iloc[:, base_columns]

    # Renommer les colonnes
    base_df_filtered.columns = ['CODE', 'SIRET PREF', 'RAISON SOCIALE', 'UAI 1', 'UAI 2', 'Adresse', 'Code postal', 'Ville', 'LIBELLE FORMATION', 'ADRESSE MAIL']

    # Effectuer la correspondance
    result_df = perform_lookup(input_codes, base_df_filtered)

    # Afficher le résultat
    st.write(result_df)

    # Option pour télécharger le fichier résultant
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        result_df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    st.download_button(
        "Télécharger le fichier Excel après correspondance",
        data=output.read(),
        file_name="resultat_correspondance.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
