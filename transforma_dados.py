import pandas as pd
import zipfile
import os
import requests

def processar_desafio_2():
    print("🚀 Iniciando Desafio 2...")
    
    # 1. Carregamento do Cadastro (Ignorando download devido ao Erro 404 da ANS)
    caminho_csv = 'operadoras_ativas.csv'
    
    if os.path.exists(caminho_csv):
        df_ativas = pd.read_csv(caminho_csv, sep=';', encoding='latin-1')
        # Normaliza colunas para evitar o KeyError
        df_ativas.columns = df_ativas.columns.str.strip().str.upper()
        df_ativas['CNPJ'] = df_ativas['CNPJ'].astype(str).str.replace(r'\D', '', regex=True)
        print("✅ Cadastro de operadoras carregado localmente.")
    else:
        print("❌ Erro: Crie o arquivo operadoras_ativas.csv manualmente primeiro.")
        return

    # PADRONIZAÇÃO TOTAL: Remove espaços e coloca tudo em MAIÚSCULO
    df_ativas.columns = df_ativas.columns.str.strip().str.upper()
    
    # Se ele não achar 'CNPJ', ele vai procurar a coluna que começa com 'CNPJ'
    if 'CNPJ' not in df_ativas.columns:
        possiveis = [c for c in df_ativas.columns if 'CNPJ' in c]
        if possiveis:
            df_ativas.rename(columns={possiveis[0]: 'CNPJ'}, inplace=True)

    # Limpa a coluna CNPJ apenas se ela existir para evitar o erro KeyError
    if 'CNPJ' in df_ativas.columns:
        df_ativas['CNPJ'] = df_ativas['CNPJ'].astype(str).str.replace(r'\D', '', regex=True)
    else:
        print("⚠️ Aviso: Coluna CNPJ não encontrada no cadastro. Verifique o arquivo operadoras_ativas.csv")
    
    print(f"📋 Colunas encontradas no cadastro: {list(df_ativas.columns)}")

    # VERIFICAÇÃO DE SEGURANÇA: Se não achar 'CNPJ', tenta achar qualquer coluna que contenha 'CNPJ'
    if 'CNPJ' not in df_ativas.columns:
        colunas_cnpj = [c for c in df_ativas.columns if 'CNPJ' in c]
        if colunas_cnpj:
            df_ativas.rename(columns={colunas_cnpj[0]: 'CNPJ'}, inplace=True)
            print(f"✅ Coluna {colunas_cnpj[0]} renomeada para CNPJ")

    # Agora sim limpa o CNPJ
    df_ativas['CNPJ'] = df_ativas['CNPJ'].astype(str).str.replace(r'\D', '', regex=True)

    # 2. Consolidação dos Trimestres
    pasta = 'contabeis'
    arquivos_zip = [f for f in os.listdir(pasta) if f.endswith('.zip')]
    lista_dfs = []

    for z_name in arquivos_zip:
        print(f"📖 Lendo {z_name}...")
        with zipfile.ZipFile(os.path.join(pasta, z_name), 'r') as z:
            csv_interno = z.namelist()[0]
            with z.open(csv_interno) as f:
                df = pd.read_csv(f, sep=';', encoding='latin-1', low_memory=False)
                df.columns = df.columns.str.strip().str.upper()
                
                # Tratamento preventivo de colunas nos trimestres
                if 'CNPJ' not in df.columns:
                    col_cnpj_alt = [c for c in df.columns if 'CNPJ' in c]
                    if col_cnpj_alt: df.rename(columns={col_cnpj_alt[0]: 'CNPJ'}, inplace=True)

                if 'CNPJ' in df.columns:
                    df['CNPJ'] = df['CNPJ'].astype(str).str.replace(r'\D', '', regex=True)
                
                if 'VL_SALDO_FINAL' in df.columns:
                    df['VL_SALDO_FINAL'] = pd.to_numeric(df['VL_SALDO_FINAL'].astype(str).str.replace(',', '.'), errors='coerce')
                
                lista_dfs.append(df)

    df_consolidado = pd.concat(lista_dfs, ignore_index=True)

    # 3. Validação e Filtros
    print("🛡️ Validando dados...")
    df_consolidado = df_consolidado.dropna(subset=['RAZAO_SOCIAL'])
    df_consolidado = df_consolidado[df_consolidado['VL_SALDO_FINAL'] > 0]
    
    # 4. Join
    print("🔗 Realizando Join...")
    # Verifica se as colunas do join existem antes de tentar
    cols_para_join = ['CNPJ', 'REGISTRO_ANS', 'MODALIDADE', 'UF']
    cols_existentes = [c for c in cols_para_join if c in df_ativas.columns]
    
    df_final = pd.merge(df_consolidado, df_ativas[cols_existentes], on='CNPJ', how='left')

    # 5. Agregação Final
    print("📊 Gerando análise estatística...")
    agrupado = df_final.groupby(['RAZAO_SOCIAL', 'UF'])['VL_SALDO_FINAL'].agg(['sum', 'mean', 'std']).reset_index()
    agrupado.columns = ['RazaoSocial', 'UF', 'Total_Despesas', 'Media_Trimestral', 'Desvio_Padrao']
    
    df_final.to_csv('demonstracoes_consolidadas_enriquecidas.csv', index=False, sep=';', encoding='latin-1')
    agrupado.to_csv('analise_despesas_operadoras.csv', index=False, sep=';', encoding='latin-1')
    
    print("✅ Sucesso! Desafio 2 concluído.")

if __name__ == "__main__":
    processar_desafio_2()