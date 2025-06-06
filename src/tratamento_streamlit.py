import os
import io

import streamlit as st #type: ignore
import pandas as pd #type: ignore
import seaborn as sns #type: ignore
import matplotlib.pyplot as plt #type: ignore

# Funções utilitárias (copiadas do seu tratamento.py)
def pega_tamanho_em_mb(caminho: str):
    return os.path.getsize(caminho) / (1024 * 1024)

def selecionar_UG():
    ugs = [
    'SRAC',
    'SRAL',
    'SRAP',
    'SRAM',
    'SRBA',
    'SRCE',
    'CGAD',
    'SRDF',
    'DITEC',
    'DIREN',
    'DTI',
    'SRES',
    'FIG',
    'SRGO',
    'SRMA',
    'SRMT',
    'SRMS',
    'SRMG',
    'SRPA',
    'SRPB',
    'SRPR',
    'SRPE',
    'SRPI',
    'SRRJ',
    'SRRN',
    'SRRS',
    'SRRO',
    'SRRR',
    'SRSC',
    'SRSP',
    'SRSE',
    'SRTO',
    'geral']
    st.session_state['selected_UG'] = st.selectbox("Selecione uma Unidade Gestora:", ugs)

def ler_arquivo_xlsx_com_progresso_streamlit(uploaded_file):
    tamanho_inicial = uploaded_file.size / (1024 * 1024)
    st.session_state['tamanho_inicial'] = tamanho_inicial
    st.write(f"Tamanho do arquivo inicial: {tamanho_inicial:.2f} MB")
    
    # Lê o arquivo Excel
    try:
        df = pd.read_excel(uploaded_file, engine='calamine')
    except Exception as e:
        st.error(f"Ocorreu um erro ao ler o arquivo: {e}")
        return None
    return df

def repor_virgula_por_ponto(valor):
    if isinstance(valor, str):
        novo_valor = valor.replace('.', '').replace(',', '.')
        return novo_valor
    else:
        return valor

# (Cole aqui as funções processa_planilha, salva_estatisticas_levantamento, salva_dataframe, adaptando para uso com Streamlit)

def processa_planilha(df):    
    st.write(f'Quantidade de linhas: {df.shape[0]}')
    st.write(f'Quantidade inicial de colunas: {df.shape[1]}')
    st.write(f'Lista de colunas iniciais: {df.columns.tolist()}')
    
 
    #checar se colunas de números de série existem na planilha
    cols_to_check = ['imei','n de serie', 'numero de serie',
                'numero de serie.1', 'numero de serie  ',
                 'num serie', 'placa', 'placa  ', 'placa vinculada',
                 'placa oficial', 'placa ','numero de serie.2',
                 'n  serie', ' placa ',  ' serie', 'serie',
                  'n  serie.1', 'numero de serie.3','numero serie']
    existing_serie_cols = [col for col in cols_to_check if col in df.columns]
    
    #checar se colunas de modelo existem na planilha
    cols_to_check = ['modelo', 'modelo  ', 'modelo    ', 
                     'modelo1', 'modelo.1', 'modelo ']
    existing_modelo_cols = [col for col in cols_to_check if col in df.columns]
    
    # checar se colunas de marca existem na planilha
    cols_to_check = ['marca','marca.1', 'marca1']
    existing_marca_cols = [col for col in cols_to_check if col in df.columns]
    
    #checar se colunas de tombo antigo existem na planilha
    cols_to_check = ['tombo antigo', 'tombo antigo.1']
    existing_tombo_antigo_cols = [col for col in cols_to_check if col in df.columns]
    
    # checar se colunas de especificações na planilha
    cols_to_check = ['observacao bloqueio', 'matriz', 'qtd de rodas',
                'acabamento da estrutura', 'altura', 'ano de fabricacao',
                'ano do modelo', 'aplicacao', 'bordas', 'calibre', 'calibre  ',
                'carga', 'data de validade', 'destino', 'genero', 'largura',
                'lote  numeros e letras sem espacos e caracteres especiais ',
                'material', 'material do assento e encosto',
                'material revestimento assento e encosto',
                'memoria de armazenamento', 'necessita ser substituido', 'nivel de protecao',
                'numero de chassis', 'numero de raias',
                    'num serie  chassis',
                'ostensivo', 'profundidade', 'qtd de gavetas',
                'qtd de passageiros', 'qtd de portas', 'renavam',
                'sentido das raias', 'servidor responsavel', 'tamanho  novo ',
                'tipo de veiculo', 'alcance',
                'ano de fabricacao.1', 'aplicacao.1', 'blindagem', 'calibre.1',
                'capacidade', 'capacidade de tiros', 'combustivel',
                'compartimento cela', 'contraste', 'cor', 'cor predominante',
                'dimensao', 'espaco disco rigido', 'faixa de operacao',
                'frequencia', 'heavy duty', 'impedancia', 'interface',
                'largura de leitura', 'material.1', 'material da estrutura',
                'meio de aquisicao', 'numero de portas',
                'padrao de leitura', 'peso',
                'polegadas', 'potencia', 'potencia  cv ', 'qtd de canais',
                'qtd de nivel', 'qtd memoria ram', 'resolucao', 'revestimento',
                'tamanho da tela', 'taxa de transferencia', 'tensao',
                'tensao de alimentacao', 'tipo', 'tipo de identificacao',
                'tipo de propriedade', 'velocidade de varredura', 'voltagem',
                'zoom otico', 'nivel de protecao da placa', 'tipo do monitor',
                'carga.1',	'classe',	'portas',	'tanque',	'velocidade',
                'volume', 'bitola do pneu', 'numero do registro', 'qtde de canais',
                'nome da embarcacao', 'numero de registro','tipo de veiculo.1',
                'descritor especial','temporario','referencia do cartucho',
                'versao', 'aplicacao.2','material de fabricacao',
                 'peso.1', 'potencia.1', 'tamanho da maleta',
                 'velocidade de impressao', 'voltagem.1']
    existing_especificacoes_cols = [col for col in cols_to_check if col in df.columns]
    
    # criar coluna de serie que compilará os demais números de série
    df['serie_total'] = None
    df['modelo_total'] = None
    df['especificacoes'] = None
    df['tombo_antigo'] = None
    df['marca_total'] = None

    #lista_colunas_exibir = ['denominacao','serie_total', 'modelo_total', 'tombo_antigo', 'marca_total', 'especificacoes']

    #define as funções
    def create_especificacoes(row):
        especificacoes = {}
        for col in existing_especificacoes_cols:
            if col in row and not pd.isna(row[col]):
                especificacoes[col] = row[col]
        return especificacoes

    def compile_series(row, existing_serie_cols):
        lista_numero_series = []
        for col in existing_serie_cols:
            value = row[col]
            if not pd.isna(value) and value not in [" ","", ".", "..."]:
                lista_numero_series.append(str(value).strip())

        lista_numero_series = list(set(lista_numero_series))
        return ', '.join(lista_numero_series)

    def compile_modelo(row, existing_modelo_cols):
        lista_modelo = []
        for col in existing_modelo_cols:
            value = row[col]
            if not pd.isna(value) and value not in [" ","", ".", "..."]:
                lista_modelo.append(str(value).strip())

        lista_modelo = list(set(lista_modelo))
        return ', '.join(lista_modelo)

    def compile_marca(row, existing_marca_cols):
        lista_marca = []
        for col in existing_marca_cols:
            value = row[col]
            if not pd.isna(value) and value not in [" ","", ".", "..."]:
                lista_marca.append(str(value).strip())

        lista_marca = list(set(lista_marca))
        return ', '.join(lista_marca)

    def compile_tombo_antigo(row, existing_tombo_antigo_cols):
        lista_tombo_antigo = []
        for col in existing_tombo_antigo_cols:
            value = row[col]
            if not pd.isna(value) and value not in [" ","", ".", "..."]:
                for char in str(value):
                    value = str(value).lstrip('P')
                    value = str(value).lstrip('S')
                    value = str(value).lstrip('0')
                lista_tombo_antigo.append(str(value).strip())

        lista_tombo_antigo = list(set(lista_tombo_antigo))
        return ', '.join(lista_tombo_antigo)

    #chamar as funções
    df['especificacoes'] = df.apply(create_especificacoes, axis=1)
    df['serie_total'] = df.apply(compile_series, axis=1, args=(existing_serie_cols,))
    df['modelo_total'] = df.apply(compile_modelo, axis=1, args=(existing_modelo_cols,))
    df['marca_total'] = df.apply(compile_marca, axis=1, args=(existing_marca_cols,))
    df['tombo_antigo'] = df[existing_tombo_antigo_cols].apply(compile_tombo_antigo, axis=1, args=(existing_tombo_antigo_cols,))

    #exclui as colunas compiladas
    df.drop(columns=existing_tombo_antigo_cols, inplace=True)
    df.drop(columns=existing_modelo_cols, inplace=True)
    df.drop(columns=existing_serie_cols, inplace=True)
    df.drop(columns=existing_marca_cols, inplace=True)
    df.drop(columns=existing_especificacoes_cols, inplace=True)

    # dividir a célula e retornar a última parte após '-' para retitrar a sigla
    df['sigla'] = df['unidade responsavel material'].apply(lambda x: x.split('-')[-1].strip())

    
    #trazer o tombo novo para a 1ª coluna (para o PROCV do excel)
    df = df.reindex(columns=['num tombamento'] + [col for col in df.columns if col != 'num tombamento'])
    
    #configura índice
    df.set_index('num tombamento', inplace=True, drop=False)
    df.index.name = 'index'    
    if 'num tombamento.1' in df.columns:
        #renomeia a coluna 'num tombamento.1' para 'num_tombamento'
        df.rename(columns={'num tombamento.1': 'num_tombamento'}, inplace=True)

    #transformar colunas em astype(str)
    colunas_astype = ['denominacao', 'especificacoes', 'marca_total', 'modelo_total', 'serie_total']
    df[colunas_astype] = df[colunas_astype].astype(str)
    
    #Preencher campos vazios das colunas
    df['localidade'] = df['localidade'].fillna('Sem localidade') #TypeError: sequence item 0: expected str instance, float found
    df['ultimo levantamento'] = df['ultimo levantamento'].fillna("0000 / 2010")
    df['modelo_total'] = df['modelo_total'].fillna('Sem modelo')
    df['serie_total'] = df['serie_total'].replace('', 'Sem serial cadastrado')
    df['acautelado para'] = df['acautelado para'].replace('','Sem acautelamento')
    
    #Remover coluinas com nome 'Unnamed'
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    
    
    #trnasforma valores numéricos em float -> '.' => ''' e ',' => '.'
    colunas_valores = ['valor', 'valor entrada', 'valor acumulado', 'valor depreciacao acumulada']
    for col in colunas_valores:
        df[col] = df[col].apply(lambda x: repor_virgula_por_ponto(x))
    
    st.write(f"Quantidade de colunas após processamento: {df.shape[1]}")
    st.write(f"Lista de colunas após processamento: {df.columns.tolist()}")

    if df.shape[1] > 45:
        st.error("O DataFrame resultante tem mais de 45 colunas. Solicite a correção do código.")
        #informa colunas não esperadas
        colunas_nao_esperadas = df.columns.difference(['num tombamento', 'unidade responsavel material', 
                                                       'codigo', 'grupo de material', 'codigo material', 
                                                       'subgrupo de material', 'acautelado para', 'matricula detentor', 
                                                       'validado eletron', 'data assinatura', 'lotacao detentor', 
                                                       'data acautelamento', 'data cadastro', 'denominacao', 
                                                       'especificacao', 'observacao', 'anulado', 'estado bem', 
                                                       'status', 'bem terceiros', 'data balanco', 'data inicio uso', 
                                                       'ano balanco', 'garantia', 'data fabricacao', 'data validade', 
                                                       'localidade', 'ultimo levantamento', 'unidade tombamento', 
                                                       'valor', 'valor entrada', 'valor acumulado', 'depreciavel', 
                                                       'valor depreciacao acumulada', 'data ultimo ajuste', 'vida util',
                                                         'vida util base depreciacao', 'data ultimo ajuste depreciacao', 
                                                         'tipo bloqueio', 'serie_total', 'modelo_total', 'especificacoes', 
                                                         'tombo_antigo', 'marca_total', 'sigla'])
        st.write("Colunas não esperadas:")
        st.write(colunas_nao_esperadas.tolist())

    return df


def salva_dataframe(df_processado):
    # salva o DataFrame processado em diferentes formatos
    df_processado.to_csv('data_bronze/lista_bens-processado.csv')
    df_processado.to_json('data_bronze/lista_bens-processado.json', orient='records', lines=True)
    df_processado.to_excel('data_bronze/lista_bens-processado.xlsx', engine='openpyxl', index=False)
    
    st.divider()
    st.subheader("Download dos arquivos processados")
    col1, col2, col3 = st.columns(3)
    col1.download_button(
        label=f"xlsx processado \n {pega_tamanho_em_mb('data_bronze/lista_bens-processado.xlsx'):.2f} MB",
        data=open('data_bronze/lista_bens-processado.xlsx', 'rb'),
        file_name='lista_bens-processado.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    #informar variação percentual do tamanho do arquivo
    col1.write(f'Variação percentual do tamanho do arquivo: {((pega_tamanho_em_mb('data_bronze/lista_bens-processado.xlsx') - st.session_state['tamanho_inicial']) / st.session_state['tamanho_inicial']) * 100:.2f}%')

    col3.download_button(
        label=f"CSV processado \n {pega_tamanho_em_mb('data_bronze/lista_bens-processado.csv'):.2f} MB",
        data=open('data_bronze/lista_bens-processado.csv', 'rb'),
        file_name='lista_bens-processado.csv',
        mime='text/csv'
    )
    #informar variação percentual do tamanho do arquivo
    col3.write(f'Variação percentual do tamanho do arquivo: {((pega_tamanho_em_mb('data_bronze/lista_bens-processado.csv') - st.session_state['tamanho_inicial']) / st.session_state['tamanho_inicial']) * 100:.2f}%')

    col2.download_button(
        label=f"JSON processado \n {pega_tamanho_em_mb('data_bronze/lista_bens-processado.json'):.2f} MB",
        data=open('data_bronze/lista_bens-processado.json', 'rb'),
        file_name='lista_bens-processado.json',
        mime='application/json'
    )
    #informar variação percentual do tamanho do arquivo
    col2.write(f'Variação percentual do tamanho do arquivo: {((pega_tamanho_em_mb('data_bronze/lista_bens-processado.json') - st.session_state['tamanho_inicial']) / st.session_state['tamanho_inicial']) * 100:.2f}%')
    st.divider()

def apresenta_graficos(base_elog : pd.DataFrame):
    st.header("Análise estatística")
    bens_ativos = base_elog[base_elog.status.isin(['EFETIVADO','ACAUTELADO',
                                                   'BEM NÃO LOCALIZADO', 'EM PROCESSO DE ALIENAÇÃO', 
                                                   'PENDENTE DE DISTRIBUIÇÃO PARA USO'])]

    bens_ativos['ano_levantamento'] = bens_ativos['ultimo levantamento'].apply(lambda x: str(x).split('/')[1] if isinstance(x, str) and '/' in x else '2010')
    
    
    # Gráfico de barras da quantidade de bens por estado do bem
    st.subheader("Distribuição percentual dos bens por estado do bem")
    df_estado_bem = bens_ativos['estado bem'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 8))
    df_estado_bem.plot.pie(
        ax=ax,
        autopct='%1.1f%%',
        startangle=90,
        legend=False,
        ylabel=''  # Remove o label do eixo y
    )
    ax.set_title('Distribuição percentual dos bens por estado do bem')
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    st.image(buf, caption='Gráfico de pizza: bens por estado do bem', use_container_width=True)
    plt.close(fig)


    # HISTOGRAMA DE ÚLTIMO ANO DE LEVANTAMENTO
    st.subheader(f"Distribuição de bens por último ano de inventário da {st.session_state['selected_UG']}")
    histograma_levantamento = bens_ativos['ano_levantamento'].value_counts().sort_index()
    with sns.axes_style('whitegrid'):
        fig, ax = plt.subplots(figsize=(10, 6))
        grafico = histograma_levantamento.plot(
            kind='bar',
            title=f'Quantidade de bens ativos pelo último ano de inventário ({st.session_state["selected_UG"]})',
            ax=ax
        )
        ax.set_xlabel('Ano do último levantamento')
        ax.set_ylabel('Quantidade de bens ativos')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

        # colocar valores nas barras
        for i, v in enumerate(histograma_levantamento):
            ax.text(i, v, str(v), ha='center', va='bottom')

        plt.tight_layout()

        # Salvar como imagem em memória
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)

        # Mostrar no Streamlit
        st.image(buf, caption='Histograma de bens por último ano de inventário', use_container_width=True)

        plt.close(fig)
    
    
    # -- GRÁFICO ANO DE INVENTÁRIO POR SETOR
    contagem = bens_ativos.groupby(['sigla', 'ano_levantamento']).size().unstack()

    # calcular soma da quantidade de bens ativos de cada linha
    contagem['soma'] = contagem.sum(axis=1).fillna(0).astype(int)
    
    # calcular percentual de 'ano levantamento' = 2024 em relação ao total
    contagem['percentual'] = contagem.iloc[:, -2]/contagem['soma']
    contagem['percentual'] = contagem['percentual'].mul(100).round(1).fillna(0)

    #transformar em string

    contagem['soma'] = contagem['soma'].astype(str)
    contagem['percentual'] = contagem['percentual'].astype(str)

    contagem['sigla'] = contagem.index.get_level_values('sigla')
    contagem['sigla'] = contagem['sigla'] + ' (' + contagem['soma'].astype(str) + ' / ' + contagem['percentual'].astype(str) + '%)'
    contagem = contagem.drop(columns=['percentual'])

    #somar os valores de todas colunas de cada linhas, exceto coluna sigla
    colunas_numericas = contagem.select_dtypes(include=['float64', 'int64']).columns

    contagem['total'] = contagem[colunas_numericas].sum(axis=1)

    #ordenar por total
    contagem = contagem.sort_values(by='total', ascending=False)
    contagem = contagem.drop(columns=['total'])

    #plotar com plotly

    # Plotar o gráfico de barras empilhadas
    fig, ax = plt.subplots(figsize=(20, 15))
    contagem.plot(
        kind='barh',
        x='sigla',
        stacked=True,
        title=f'Bens ativos por setor e ano do último levantamento na {st.session_state["selected_UG"]} (Quantidade total de bens / percentual inventariado)',
        colormap='RdBu',
        ax=ax
    )
    ax.set_ylabel('Setor (% levantado)')
    ax.set_xlabel('Quantidade de bens ativos')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    plt.tight_layout()

    # Salvar como imagem em memória
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    # Mostrar no Streamlit
    st.image(buf, caption='Gráfico de bens ativos por setor e ano', use_container_width=True)

    plt.close(fig)  # Fecha a figura para liberar memória

    # -- GRÁFICO DE ÚLTIMO ANO DE LEVANTAMENTO POR GRUPO DE MATERIAL
    st.subheader("Quantidade de bens por grupo de material (cores por ano de levantamento)")
    if 'grupo de material' in bens_ativos.columns and 'ano_levantamento' in bens_ativos.columns:
        # Cria tabela dinâmica: linhas=grupo, colunas=ano, valores=contagem
        pivot = bens_ativos.pivot_table(
            index='grupo de material',
            columns='ano_levantamento',
            values='num tombamento',  # ou qualquer coluna, pois é só para contar
            aggfunc='count',
            fill_value=0
        )
        # Ordena pelo total de bens
        pivot['total'] = pivot.sum(axis=1)
        pivot = pivot.sort_values('total', ascending=False).drop(columns='total')

        # Plota gráfico de barras horizontais empilhadas
        fig, ax = plt.subplots(figsize=(14, max(6, len(pivot) * 0.4)))
        pivot.plot(
            kind='barh',
            stacked=True,
            ax=ax,
            colormap='RdBu'
        )
        ax.set_xlabel('Quantidade de bens')
        ax.set_ylabel('Grupo de material')
        ax.set_title('Quantidade de bens por grupo de material (cores por ano de levantamento)')
        plt.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        st.image(buf, caption='Bens por grupo de material e ano de levantamento', use_container_width=True)
        plt.close(fig)
    else:
        st.warning("Colunas 'grupo de material' ou 'ano_levantamento' não encontradas.")

# ------------------- STREAMLIT APP -------------------
if __name__ == "__main__":
    if not os.path.exists('data_bronze'):
        os.makedirs('data_bronze')
    
    st.title("Processamento de Listagem geral de bens do eLog")

    uploaded_file = st.file_uploader("Selecione o arquivo Excel para processar", type=["xlsx"])

    if uploaded_file is not None:
        st.info("Lendo arquivo Excel...")
        selecionar_UG()
        df_lista_materiais = ler_arquivo_xlsx_com_progresso_streamlit(uploaded_file)
        if df_lista_materiais is not None:
            st.success("Arquivo lido com sucesso!")
            st.subheader('Processando dados...')
            df_processado = processa_planilha(df_lista_materiais)
            st.success("Planilha processada!")
            st.info("Gerando planilha processada...")
            salva_dataframe(df_processado)
            st.success("Processamento concluído!")
            apresenta_graficos(df_processado)
            
    else:
        st.warning("Faça upload de um arquivo Excel para começar.")