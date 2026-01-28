import requests
import os

# Lista direta dos trimestres mais recentes disponíveis (Exemplo: 2024 e 2023)
LINKS_DIRETOS = [
    "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/3T2024.zip",
    "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/2T2024.zip",
    "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/1T2024.zip"
]

def baixar_fixo():
    print("🚀 Iniciando download dos 3 últimos trimestres...")
    if not os.path.exists('contabeis'):
        os.makedirs('contabeis')
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for url in LINKS_DIRETOS:
        nome_arquivo = url.split('/')[-1]
        print(f"📥 Baixando: {nome_arquivo}...")
        try:
            res = requests.get(url, headers=headers, timeout=20)
            if res.status_code == 200:
                with open(f"contabeis/{nome_arquivo}", 'wb') as f:
                    f.write(res.content)
                print(f"✅ {nome_arquivo} salvo!")
            else:
                print(f"❌ Falha no link {nome_arquivo}: Status {res.status_code}")
        except Exception as e:
            print(f"❌ Erro ao baixar {nome_arquivo}: {e}")

if __name__ == "__main__":
    baixar_fixo()