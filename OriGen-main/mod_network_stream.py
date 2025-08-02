import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import networkx as nx
from pyvis.network import Network
import tempfile, os

from st_aggrid import AgGrid

st.set_page_config(layout="wide", page_title="Regulatory")
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

st.markdown("""
### miRNA-gene network
""")


dataframes = {}
target_df = None
# Define o caminho da pasta onde os arquivos CSV estão armazenados
folder_path = "static/data/mirnas"
if folder_path and os.path.isdir(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    if csv_files:
        for file in csv_files:
            gene = file.split('.')[0]
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(file_path, sep=";")
                dataframes[gene] = df
            except Exception as e:
                st.error(f"Erro ao ler {file}: {e}")

col1, col2 = st.columns(2)

with col1:
    selected_file = st.selectbox('Selecione um arquivo para visualizar:', list(dataframes.keys()))
    st.write(f"### Gene: {selected_file}")
    target_df = dataframes[selected_file]
    # Criação da configuração da tabela
    gb = GridOptionsBuilder.from_dataframe(target_df)
    gb.configure_side_bar()  # adiciona barra lateral
    gb.configure_grid_options(enableRangeSelection=True,  # permite seleção de intervalo
                              domLayout='normal',
                              suppressRowClickSelection=False)
    grid_options = gb.build()
    AgGrid(df,
           gridOptions=grid_options,
           enable_enterprise_modules=True,
           theme='material',
           fit_columns_on_grid_load=True)

with col2:
    net = nx.from_pandas_edgelist(target_df, source='miRNA', target='Gene', edge_attr=['Weight'])
    G1 = Network(directed=False, height='550px', width='100%', notebook=False, cdn_resources="local")
    G1.from_nx(net)
    G1.save_graph('graph.html')
    with open('graph.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=550)
