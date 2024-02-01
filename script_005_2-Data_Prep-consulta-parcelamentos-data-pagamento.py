#!/usr/bin/env python
# coding: utf-8

# ## Divída Ativa
# 
# More background on the project
# 
# ### Data Sources
# - file1 : Description of where this file came from
# 
# ### Changes
# - 12-18-2023 : Started project
import pandas as pd
from pathlib import Path
from datetime import datetime
from config import Config

today = datetime.today()
nome_arquivo = 'consulta-parcelamentos-data-pagamento'
file_directory = Config.DIR_DESTINO / "csv"
summary_file = Path.cwd() / "data" / "processed" / Config.DATA_DOWNLOAD / f"summary_{nome_arquivo}.parquet"


for f in list(file_directory.glob('*.csv'))[:5]:
    print(f.name)

in_files = [f for f in file_directory.glob('*.csv') 
            if f.name.startswith(nome_arquivo)]

dtypes = {
    'Inscrição': 'Int64',
    'Ano': 'Int64',
    'Numero': 'Int64',
    'Pc': 'Int64',
    'Pcs': 'Int64',    
}

dataframe_list = []
for file_ in in_files:
    try:
        dfi = pd.read_csv(file_, skiprows=1, sep=';', encoding='ANSI')
        if dfi.shape[0] > 0:
            contador = 0
            while contador <= 10:
                if 'Inscrição' in dfi.columns:
                    break
                columns = dfi.iloc[0]
                dfi.columns = columns
                dfi = dfi.iloc[1:]
                # print(dfi.columns)
                contador += 1
            dataframe_list.append(dfi)
            
        # print(dfi.columns, file_)

    except Exception  as error:
        print(error)

if dataframe_list:
    print('Qtd dataframes:', len(dataframe_list))
    for dfi in dataframe_list:
        print(dfi.shape)
        
    df = pd.concat(dataframe_list, ignore_index=True)
    print(df.shape)
    df.head()

    # https://stackoverflow.com/questions/30763351/removing-space-in-dataframe-python
    df.columns = [x.strip() for x in df.columns]
    df.columns

    cols_to_rename = {
        'Inscrição': 'Inscricao',
        'Valor Parcelado': 'ValorParcelado',
        'Pcs': 'Parcelamento',
        'Data do acordo': 'DataAcordo',
        'Valor Pago': 'ValorPago',
        'Honorarios': 'Honorarios',
        'Pc': 'Parcela',
        'Data do Pagto': 'DataPagamento',
        'Tipo': 'TipoNum',
        'Tipo.1': 'Tipo',
    }
    df.rename(columns=cols_to_rename, inplace=True)

    # ### Clean Up Data Types
    df['ValorParcelado'] = (df['ValorParcelado'].str.replace('.', '', regex=False)
                                                .str.replace(',', '.', regex=False)
                                                .astype('Float64'))

    df['ValorPago'] = (df['ValorPago'].str.replace('.', '', regex=False)
                                                .str.replace(',', '.', regex=False)
                                                .astype('Float64'))

    df['Honorarios'] = (df['Honorarios'].str.replace('.', '', regex=False)
                                                .str.replace(',', '.', regex=False)
                                                .astype('Float64'))


    def corrige_data(date_str):
        dia, mes, ano = date_str.split('/')
        if dia == '00':
            dia = '01'
        if mes == '00':
            mes = '01'
        return f'{dia}/{mes}/{ano}'


    df['DataAcordo'] = df['DataAcordo'].apply(corrige_data)
    df['DataAcordo'] = pd.to_datetime(df['DataAcordo'], format=f'%d/%m/%Y')
    df['DataPagamento'] = pd.to_datetime(df['DataPagamento'], format=f'%d/%m/%Y')

    # ### Data Manipulation
    for col in df.columns:
        print(f'{col:.<30}:', max([len(str(v)) for v in df[col]]))

    df['IdParcela'] = (
        (df['Ano'].astype(str)) + 
        (df['Numero'].astype(str)).apply(lambda x: f'{x:0>5}') + 
        (df['Parcela'].astype(str)).apply(lambda x: f'{x:0>3}')
    )

    df['IdAcordo'] = (
        (df['Ano'].astype(str)) + 
        (df['Numero'].astype(str)).apply(lambda x: f'{x:0>5}')
    )

    df['IdCadastro'] = (
        (df['TipoNum'].astype(str)).apply(lambda x: f'{x:0>3}') + 
        (df['Inscricao'].astype(str)).apply(lambda x: f'{x:0>12}')
    )

    for col in df.columns:
        print(f'{col:.<30}:', max([len(str(v)) for v in df[col]]))

    for col in df.columns:
        print(f'{col:.<30}:', min([len(str(v)) for v in df[col]]))

    # ### Save output file into processed directory
    df.to_parquet(summary_file)

else:
    print(f'Nenhum dado foi encontrado nos arquivos .csv que iniciam com "{nome_arquivo}"')
