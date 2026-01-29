# Teste Técnico - Estágio Intuitive Care

## 👤 Candidato
- **Nome:** Thays Estefhany Reis França
- [cite_start]**Prazo de Entrega:** 1 semana [cite: 7]

## 🚀 Como Executar o Projeto
1. **Pré-requisitos:** Ter o Python3 instalado.
2. **Instalação:** No terminal do VS Code, execute:
   ```bash
   pip install requests pandas beautifulsoup4
## Notas de Desenvolvimento
O projeto foi desenvolvido e testado utilizando o terminal PowerShell integrado ao VS Code, garantindo a compatibilidade com ambientes Windows conforme os requisitos de execução do teste.
## 📊 Desafio 2 - Transformação e Validação de Dados

Nesta etapa, o objetivo foi consolidar as demonstrações contábeis de três trimestres, validar a integridade dos dados e cruzar as informações com a base cadastral da ANS.

### 🛠️ Decisões Técnicas (Trade-offs)

#### 1. Tratamento de CNPJs Inválidos
- **Decisão**: Optei por filtrar e remover registros com CNPJs que não possuam o formato correto ou falhem no dígito verificador.
- **Prós**: Garante que o cálculo final de despesas por operadora seja 100% confiável.
- **Contras**: Alguns dados reais podem ser perdidos se houver erro de digitação na fonte original da ANS.

#### 2. Estratégia de Join (Enriquecimento)
- **Decisão**: Utilize um `left join` tendo como base o CSV consolidado das demonstrações.
- **Justificativa**: Isso permite manter o histórico financeiro mesmo que uma operadora não seja encontrada no cadastro de "Ativas" (podendo ser uma operadora que encerrou atividades recentemente).

#### 3. Agregação e Cálculo de Despesas (Estatística)
- **Decisão**: Implementei a agregação por `RazaoSocial` e `UF` utilizando o método `.agg()` do Pandas.
- **Destaque**: Além da soma total, incluí o cálculo de **Média** e **Desvio Padrão** por trimestre, conforme sugerido como desafio adicional no teste.
- **Trade-off**: Para a ordenação, utilizei a estratégia de ordenação em memória (QuickSort padrão do Pandas), que é ideal para o volume de dados consolidado após o filtro de despesas.

#### 4. Agregação e Volume de Dados
- **Decisão**: Utilizei a biblioteca **Pandas** com o parâmetro `low_memory=False`.
- **Justificativa**: Dado o volume de milhões de linhas das demonstrações contábeis, o Pandas é eficiente para operações de agrupamento (`groupby`) em memória, garantindo performance na soma das despesas.

### 🚀 Como executar
1. Certifique-se de que os arquivos `.zip` estão na pasta `/contabeis`.
2. Execute o script de transformação:
   ```bash
   python transforma_dados.py
   O arquivo final demonstracoes_consolidadas_enriquecidas.csv será gerado na raiz.

   - **Estabilidade de Conexão:**:"Optei pelo uso de links diretos para os trimestres de 2024 para garantir a estabilidade do download, visto que o servidor FTP da ANS apresenta instabilidades frequentes em buscas dinâmicas."


   - **Nota sobre Enriquecimento de Dados**: Durante o desenvolvimento, o servidor da ANS apresentou erro 404 nos links de dados cadastrais. Para garantir a execução do Desafio 2, utilizei uma amostra local dos dados cadastrais (operadoras_ativas.csv), mantendo a lógica de processamento e join pronta para quando o servidor for restabelecido.

   ## 🗄️ Desafio 3 - Banco de Dados e Análise SQL

Nesta etapa, os dados foram estruturados em um banco de dados relacional para permitir análises complexas e garantir a integridade das informações financeiras.

### 🛠️ Decisões Técnicas (Trade-offs)

1. **Estratégia de Normalização**:
   - **Decisão**: Optei pela **Opção B (Tabelas Normalizadas)**.
   - **Justificativa**: Separei os dados cadastrais (`operadoras`) dos dados financeiros (`despesas_consolidadas`). Isso evita a redundância de dados e segue as melhores práticas de modelagem de dados (KISS).

2. **Tipos de Dados e Precisão**:
   - **Decisão**: Utilização de `DECIMAL(15, 2)` para valores monetários.
   - **Justificativa**: O uso de `DECIMAL` em vez de `FLOAT` é essencial em sistemas de saúde e financeiros para evitar erros de arredondamento e garantir a precisão dos centavos.

3. **Resiliência em Cálculos**:
   - **Decisão**: Uso da função `NULLIF` na Query de crescimento.
   - **Justificativa**: Previne o erro de "divisão por zero" em operadoras que iniciaram o ano com despesa zero, garantindo que o relatório seja gerado sem interrupções.

4. **Performance em Consultas**:
   - **Decisão**: Uso de **CTEs (Common Table Expressions)** para cálculos de média geral.
   - **Justificativa**: Melhora a legibilidade do código e facilita a manutenção, permitindo que o avaliador entenda a lógica de comparação em etapas claras.
