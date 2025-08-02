import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network

st.title("Rede Direcionada de TFs e Tecidos")

# Upload do arquivo tabular
uploaded_file = st.file_uploader("Faça o upload do arquivo CSV", type=["csv", "txt"])

if uploaded_file:
    # Carregar o arquivo em um DataFrame
    df = pd.read_csv(uploaded_file, delimiter="\t")
    st.dataframe(df)

    # Criar o grafo direcionado
    G = nx.DiGraph()

    # Adicionar nós e arestas ao grafo
    for _, row in df.iterrows():
        tissue = row[0]  # Tissue
        tf = row[2]  # TF
        expression = row[5]  # Valor categórico "Up" ou "Down"
        color = "#66c2a5" if expression == "Up" else "#fc8d62"
        G.add_node(tf, color=color)
        G.add_node(tissue, color="#8da0cb", title="Tecido")
        G.add_edge(tf, tissue, color=color)

    G1 = Network(height='1000px', width='1000px', notebook=False, cdn_resources="local")
    G1.from_nx(G)
    G1.save_graph('graph.html')
    with open('graph.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=800, width=800)