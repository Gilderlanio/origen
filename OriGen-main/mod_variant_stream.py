import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import os
import plotly.express as px

st.set_page_config(layout="wide", page_title = "Variants")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp {
        background-color: whitesmoke;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# Define o caminho da pasta onde os arquivos CSV estão armazenados
folder_path = "static/data/variants"

st.markdown("""
### Painel of genetic markers, functional prediction, and allele frequency.

""")

if folder_path and os.path.isdir(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    if csv_files:
        dataframes = {}
        for file in csv_files:
            gene = file.split('_')[0]
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(file_path, sep=',')
                dataframes[gene] = df
            except Exception as e:
                st.error(f"Erro ao ler {file}: {e}")
        if dataframes:
            selected_file = st.selectbox('Selecione um arquivo para visualizar:', list(dataframes.keys()))
            st.write(f"### Gene: {selected_file}")

            df = dataframes[selected_file]
            # Colunas básicas
            colunas_base = [
                'gnomAD ID', 'Source',
                # Informações genômicas
                'Transcript', 'Protein Consequence', 'VEP Annotation',
                # Informações clínicas
                'ClinVar Germline Classification'
            ]

            # Populações e colunas associadas
            populacoes = {
                'African/African American': {
                    'count': 'Allele Count African/African American',
                    'number': 'Allele Number African/African American',
                    'freq_col': 'Freq(AAA)'
                },
                'Admixed American': {
                    'count': 'Allele Count Admixed American',
                    'number': 'Allele Number Admixed American',
                    'freq_col': 'Freq(AMR)'
                },
                'European': {
                    'count': 'Allele Count European (non-Finnish)',
                    'number': 'Allele Number European (non-Finnish)',
                    'freq_col': 'Freq(EUR)'
                }
            }

            # Adiciona colunas disponíveis
            colunas_validas = colunas_base.copy()
            for pop, campos in populacoes.items():
                if campos['count'] in df.columns and campos['number'] in df.columns:
                    colunas_validas.extend([
                        campos['count'], campos['number']
                    ])

            # Remove colunas duplicadas
            colunas_validas = list(dict.fromkeys(colunas_validas))

            # Filtra o DataFrame
            df_filtered = df[colunas_validas].copy()

            # Calcular as frequências específicas
            for pop, campos in populacoes.items():
                count_col = campos['count']
                number_col = campos['number']
                freq_col = campos['freq_col']
                if count_col in df.columns and number_col in df.columns:
                    df_filtered[freq_col] = df[count_col] / df[number_col]

            gb = GridOptionsBuilder.from_dataframe(df_filtered)
            gb.configure_side_bar()  # adiciona barra lateral
            gb.configure_grid_options(enableRangeSelection=True,  # permite seleção de intervalo
                                      domLayout='normal',
                                      suppressRowClickSelection=False)
            grid_options = gb.build()
            AgGrid(df_filtered,
                   gridOptions=grid_options,
                   enable_enterprise_modules=True,
                   theme='material')
    else:
        st.warning("Nenhum arquivo CSV encontrado na pasta especificada.")
else:
    if folder_path:
        st.error("Caminho inválido. Por favor, insira um caminho válido.")


col1, col2, col3 = st.columns(3)

with col1:
    frequencias = df_filtered['Source'].value_counts().reset_index()
    frequencias.columns = ['Source', 'Frequency']
    fig = px.bar(frequencias, x='Source', y='Frequency', color='Source')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, theme='streamlit')

with col2:
    frequencias = df_filtered['ClinVar Germline Classification'].value_counts().reset_index()
    frequencias.columns = ['ClinVar', 'Frequency']
    fig = px.bar(frequencias, x='ClinVar', y='Frequency', color='ClinVar')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, theme='streamlit')

with col3:
    frequencias = df_filtered['VEP Annotation'].value_counts().reset_index()
    frequencias.columns = ['VEP', 'Frequency']
    fig = px.bar(frequencias, x='VEP', y='Frequency', color='VEP')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, theme="streamlit")

col4, col5, col6 = st.columns(3)

with col4:
    fig = px.histogram(df_filtered, x="Freq(AAA)", nbins=100, title='Frequency in African/Afro-American')
    st.plotly_chart(fig, theme=None)
with col5:
    fig = px.histogram(df_filtered, x="Freq(AMR)", nbins=100, title='Frequency in Admixed Americans')
    st.plotly_chart(fig, theme='streamlit')
with col6:
    fig = px.histogram(df_filtered, x="Freq(EUR)", nbins=100, title='Frequency in Europeans')
    st.plotly_chart(fig, theme='streamlit')