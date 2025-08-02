import streamlit as st
import pandas as pd
# Certo:
from st_aggrid import AgGrid, GridOptionsBuilder

df = pd.read_csv('static/data/variants/geral.txt', sep='\t')
st.set_page_config(layout="wide", page_title = "Genes")

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
### Genetic Markers and their relevance to Quilombo populations.
""")

st.markdown("""
#### This application presents a concise overview of selected genes and their health relevance, particularly in the context of **Quilombo communities**, which often retain African ancestral genetic diversity.
---
""")

# Criação da configuração da tabela
gb = GridOptionsBuilder.from_dataframe(df)
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

st.markdown("""

### **Genes and their importance**

**1. G6PD (Glucose-6-Phosphate Dehydrogenase)**  
*Protects red blood cells from oxidative stress.*  
**Relevance**: G6PD deficiency is more common in African populations and affects drug response and infection resistance.

**2. HLA-DRB1**  
*Immune system gene involved in presenting antigens.*  
 **Relevance**: Highly polymorphic; affects autoimmune risk and immune diversity.

**3. HLA-C**  
*Presents antigens to T-cells.*  
**Relevance**: Important for viral immunity and transplantation matching.

**4. LEPR (Leptin Receptor)**  
*Regulates appetite and energy use.*  
**Relevance**: Influences obesity and metabolic health—key in underrepresented populations.

**5. ADRB2 (Beta-2 Adrenergic Receptor)**  
*Mediates stress response.*  
**Relevance**: Variants linked to asthma and blood pressure control.

**6. GNB3 (G Protein Subunit Beta 3)**  
*Signal transduction gene.*  
**Relevance**: Polymorphisms may increase risk of hypertension and obesity.

**7. DBP / GC (Vitamin D Binding Protein)**  
*Transports vitamin D in the bloodstream.*  
**Relevance**: Affects vitamin D bioavailability—often lower in people with darker skin.

**8. NOS3 (Nitric Oxide Synthase 3)**  
*Regulates blood vessel tone.*  
**Relevance**: Associated with cardiovascular health and blood pressure.

**9. IGFBP3 (Insulin-like Growth Factor Binding Protein 3)**  
*Regulates IGF, influencing cell growth and metabolism.*  
**Relevance**: May affect cancer susceptibility and metabolic traits.

**10. CCR5 (Chemokine Receptor 5)**  
*Controls immune cell migration.*  
**Relevance**: Variants influence HIV susceptibility; CCR5-Δ32 is rare in African ancestry.

**11. AR (Androgen Receptor)**  
*Responds to testosterone.*  
**Relevance**: Linked to prostate cancer risk, varies with ancestry.

**12. TCF7L2 (Transcription Factor 7 Like 2)**  
*Regulates insulin secretion.*  
**Relevance**: Strongly associated with type 2 diabetes.

**13. ADIPOR1 (Adiponectin Receptor 1)**  
*Regulates fat metabolism and insulin sensitivity.*  
**Relevance**: Associated with obesity and insulin resistance.

---
""")
