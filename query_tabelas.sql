-- Criação da tabela de Operadoras (Dados Cadastrais)
CREATE TABLE operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY,
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    modalidade VARCHAR(100),
    uf CHAR(2)
);

-- Tabela de Despesas (Consolidado)
CREATE TABLE despesas_consolidadas (
    id SERIAL PRIMARY KEY,
    cnpj VARCHAR(20),
    trimestre INTEGER,
    ano INTEGER,
    valor_despesa DECIMAL(15, 2)
);
