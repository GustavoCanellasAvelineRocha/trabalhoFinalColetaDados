import pandas as pd

df_bem_candidato = pd.read_csv("bem_candidato_2020_RS.csv", delimiter=';', encoding='ISO-8859-1')

df_bem_candidato.columns = df_bem_candidato.columns.str.strip()

if 'VR_BEM_CANDIDATO' not in df_bem_candidato.columns:
    print("Coluna 'VR_BEM_CANDIDATO' não encontrada!")
else:
    df_bem_candidato['VR_BEM_CANDIDATO'] = pd.to_numeric(df_bem_candidato['VR_BEM_CANDIDATO'].str.replace(",", "."), errors='coerce')

    df_bem_candidato = df_bem_candidato.dropna(subset=['SQ_CANDIDATO', 'VR_BEM_CANDIDATO'])

    total_instancias = df_bem_candidato.shape[0]
    media_valor = df_bem_candidato['VR_BEM_CANDIDATO'].mean()
    desvio_padrao_valor = df_bem_candidato['VR_BEM_CANDIDATO'].std()

    print("bem_candidato_2020_RS")
    print("Total de instâncias:", total_instancias)
    print("Campo escolhido para análise: VR_BEM_CANDIDATO")
    print("Média:", media_valor)
    print("Desvio Padrão:", desvio_padrao_valor)
