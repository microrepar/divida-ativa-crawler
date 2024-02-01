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

# ### File Locations
today = datetime.today()
nome_arquivo = 'parcelamentos-cancelamento-inadimplencia'
file_directory = Config.DIR_DESTINO / "csv"
summary_file = Path.cwd() / "data" / "processed" / Config.DATA_DOWNLOAD / f"summary_{nome_arquivo}.parquet"

in_files = [f for f in file_directory.glob('*.csv') 
            if f.name.startswith(nome_arquivo)]

dtypes = {
    'Inscrição': 'string',
    'Ano': 'Int64',
    'Numero': 'Int64',
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
                contador += 1
            dataframe_list.append(dfi)
            
    except Exception  as error:
        print(error)
    

if dataframe_list:
    print('Qtd dataframes:', len(dataframe_list))
    for dfi in dataframe_list:
        print(dfi.shape)
        
    df = pd.concat(dataframe_list, ignore_index=True)
    print(df.shape)
    df.head()

    # ### Column Cleanup
    # - Remove all leading and trailing spaces
    # - Rename the columns for consistency.
    # https://stackoverflow.com/questions/30763351/removing-space-in-dataframe-python
    df.columns = [x.strip() for x in df.columns]

    cols_to_rename = {
        'Inscrição'       : 'Inscricao',
        'Descrição'       : 'Descricao',
        'Vl Parcelamento' : 'ValorParcelamento',
        'Data do Pagto'   : 'DataPagamento',
    }
    df.rename(columns=cols_to_rename, inplace=True)

    # ### Clean Up Data Types
    df['ValorParcelamento'] = (df['ValorParcelamento'].str.replace('.', '', regex=False)
                                                .str.replace(',', '.', regex=False)
                                                .astype('Float64'))

    df['Vencimento'] = pd.to_datetime(df['Vencimento'], format=f'%d/%m/%Y')

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
        (df['Tipo'].astype(str)).apply(lambda x: f'{x:0>3}') + 
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
