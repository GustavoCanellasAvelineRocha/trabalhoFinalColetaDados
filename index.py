import pandas as pd
import matplotlib.pyplot as plt

bens_df = pd.read_csv('bem_candidato_2020_RS.csv', delimiter=';', encoding='ISO-8859-1')
votacao_df = pd.read_csv('votacao_secao_2020_RS.csv', delimiter=';', encoding='ISO-8859-1')

colunas_irrelevantes_bens = [
    'DT_GERACAO', 'HH_GERACAO', 'ANO_ELEICAO', 'CD_TIPO_ELEICAO', 'NM_TIPO_ELEICAO',
    'CD_ELEICAO', 'DS_ELEICAO', 'DT_ELEICAO', 'SG_UF', 'SG_UE', 'NM_UE',
    'NR_ORDEM_BEM_CANDIDATO', 'CD_TIPO_BEM_CANDIDATO', 'DS_TIPO_BEM_CANDIDATO',
    'DS_BEM_CANDIDATO', 'DT_ULT_ATUAL_BEM_CANDIDATO', 'HH_ULT_ATUAL_BEM_CANDIDATO'
]
bens_df = bens_df.drop(columns=colunas_irrelevantes_bens, errors='ignore')

colunas_irrelevantes_votacao = [
    'DT_GERACAO', 'HH_GERACAO', 'ANO_ELEICAO', 'CD_TIPO_ELEICAO', 'NM_TIPO_ELEICAO',
    'NR_TURNO', 'CD_ELEICAO', 'DS_ELEICAO', 'DT_ELEICAO', 'TP_ABRANGENCIA',
    'SG_UF', 'SG_UE', 'NM_UE', 'CD_MUNICIPIO', 'NM_MUNICIPIO', 'NR_ZONA', 'NR_SECAO',
    'CD_CARGO', 'NR_LOCAL_VOTACAO', 'NM_LOCAL_VOTACAO', 'DS_LOCAL_VOTACAO_ENDERECO'
]
votacao_df = votacao_df.drop(columns=colunas_irrelevantes_votacao, errors='ignore')

bens_df['VR_BEM_CANDIDATO'] = pd.to_numeric(bens_df['VR_BEM_CANDIDATO'].str.replace(',', '.'), errors='coerce') * 1_000_000  # Ajuste para reais
votacao_df['QT_VOTOS'] = pd.to_numeric(votacao_df['QT_VOTOS'], errors='coerce')

bens_df = bens_df.dropna(subset=['SQ_CANDIDATO', 'VR_BEM_CANDIDATO'])
votacao_df = votacao_df.dropna(subset=['SQ_CANDIDATO', 'QT_VOTOS', 'NM_VOTAVEL', 'DS_CARGO'])

votacao_df = votacao_df[~votacao_df['NM_VOTAVEL'].str.startswith(('Partido', 'VOTO'))]

bens_aggregated = bens_df.groupby('SQ_CANDIDATO', as_index=False)['VR_BEM_CANDIDATO'].sum()
votos_aggregated = votacao_df.groupby(['SQ_CANDIDATO', 'DS_CARGO'], as_index=False).agg({
    'QT_VOTOS': 'sum',
    'NM_VOTAVEL': 'first'
})

merged_df = pd.merge(bens_aggregated, votos_aggregated, on='SQ_CANDIDATO', how='inner')

prefeitos_df = merged_df[merged_df['DS_CARGO'] == 'Prefeito']
vereadores_df = merged_df[merged_df['DS_CARGO'] == 'Vereador']

prefeito_maior_votos = prefeitos_df.nlargest(1, 'QT_VOTOS')
prefeito_maior_bens = prefeitos_df.nlargest(1, 'VR_BEM_CANDIDATO')

vereador_maior_votos = vereadores_df.nlargest(1, 'QT_VOTOS')
vereador_maior_bens = vereadores_df.nlargest(1, 'VR_BEM_CANDIDATO')

def formatar_resultado(candidato, cargo, descricao):
    return f"""
    {descricao}:
    - Nome: {candidato['NM_VOTAVEL']}
    - SQ_CANDIDATO: {candidato['SQ_CANDIDATO']}
    - Bens Declarados: R$ {candidato['VR_BEM_CANDIDATO'] / 1_000_000:,.2f} milhões
    - Votos Recebidos: {candidato['QT_VOTOS']:,}
    """

print(formatar_resultado(prefeito_maior_votos.iloc[0], "Prefeito", "Prefeito com maior número de votos"))
print(formatar_resultado(prefeito_maior_bens.iloc[0], "Prefeito", "Prefeito com maior valor de bens declarados"))
print(formatar_resultado(vereador_maior_votos.iloc[0], "Vereador", "Vereador com maior número de votos"))
print(formatar_resultado(vereador_maior_bens.iloc[0], "Vereador", "Vereador com maior valor de bens declarados"))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.scatter(prefeitos_df['VR_BEM_CANDIDATO'], prefeitos_df['QT_VOTOS'], color='blue', label='Prefeitos')
ax1.scatter(prefeito_maior_votos['VR_BEM_CANDIDATO'], prefeito_maior_votos['QT_VOTOS'], color='red', label='Prefeito com Maior Votos', s=100, edgecolors='black')
ax1.scatter(prefeito_maior_bens['VR_BEM_CANDIDATO'], prefeito_maior_bens['QT_VOTOS'], color='green', label='Prefeito com Maior Bens', s=100, edgecolors='black')
ax1.set_title('Prefeitos: Bens vs Votos')
ax1.set_xlabel('Valor dos Bens Declarados (Milhões de R$)')
ax1.set_ylabel('Total de Votos Recebidos')
ax1.legend()

ax2.scatter(vereadores_df['VR_BEM_CANDIDATO'], vereadores_df['QT_VOTOS'], color='orange', label='Vereadores')
ax2.scatter(vereador_maior_votos['VR_BEM_CANDIDATO'], vereador_maior_votos['QT_VOTOS'], color='red', label='Vereador com Maior Votos', s=100, edgecolors='black')
ax2.scatter(vereador_maior_bens['VR_BEM_CANDIDATO'], vereador_maior_bens['QT_VOTOS'], color='green', label='Vereador com Maior Bens', s=100, edgecolors='black')
ax2.set_title('Vereadores: Bens vs Votos')
ax2.set_xlabel('Valor dos Bens Declarados (Milhões de R$)')
ax2.set_ylabel('Total de Votos Recebidos')
ax2.legend()

plt.tight_layout()
plt.show()

file_path = 'dataset_final.csv'
merged_df.to_csv(file_path, index=False)
