import pandas as pd

votacao_df = pd.read_csv('votacao_secao_2020_RS.csv', delimiter=';', encoding='ISO-8859-1')

colunas_irrelevantes_votacao = [
    'DT_GERACAO', 'HH_GERACAO', 'ANO_ELEICAO', 'CD_TIPO_ELEICAO', 'NM_TIPO_ELEICAO',
    'NR_TURNO', 'CD_ELEICAO', 'DS_ELEICAO', 'DT_ELEICAO', 'TP_ABRANGENCIA',
    'SG_UF', 'SG_UE', 'NM_UE', 'CD_MUNICIPIO', 'NM_MUNICIPIO', 'NR_ZONA', 'NR_SECAO',
    'NR_LOCAL_VOTACAO', 'NM_LOCAL_VOTACAO', 'DS_LOCAL_VOTACAO_ENDERECO'
]
votacao_df = votacao_df.drop(columns=colunas_irrelevantes_votacao, errors='ignore')

votacao_df['QT_VOTOS'] = pd.to_numeric(votacao_df['QT_VOTOS'], errors='coerce')

votacao_df = votacao_df.dropna(subset=['SQ_CANDIDATO', 'QT_VOTOS'])

votos_aggregated = votacao_df.groupby('SQ_CANDIDATO', as_index=False).agg({
    'QT_VOTOS': 'sum',
    'NM_VOTAVEL': 'first'
})

total_instancias = votos_aggregated['QT_VOTOS'].count()
media_votos = votos_aggregated['QT_VOTOS'].mean()
desvio_padrao_votos = votos_aggregated['QT_VOTOS'].std()

print(f"Total de instâncias: {total_instancias}")
print(f"Média (QT_VOTOS): {media_votos:.2f}")
print(f"Desvio padrão (QT_VOTOS): {desvio_padrao_votos:.2f}")
