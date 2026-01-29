-- Query 1: Top 5 crescimento percentual (1T vs 3T)
SELECT 
    t1.cnpj,
    (t3.valor_despesa - t1.valor_despesa) / NULLIF(t1.valor_despesa, 0) * 100 AS crescimento_percentual
FROM despesas_consolidadas t1
JOIN despesas_consolidadas t3 ON t1.cnpj = t3.cnpj
WHERE t1.trimestre = 1 AND t3.trimestre = 3
ORDER BY crescimento_percentual DESC
LIMIT 5;

-- Query 2: Top 5 estados com maiores despesas
SELECT 
    o.uf,
    SUM(d.valor_despesa) AS despesa_total,
    AVG(d.valor_despesa) AS media_por_operadora
FROM despesas_consolidadas d
JOIN operadoras o ON d.cnpj = o.cnpj
GROUP BY o.uf
ORDER BY despesa_total DESC
LIMIT 5;

-- Query 3: Operadoras acima da média em 2 de 3 trimestres
WITH media_geral AS (
    SELECT AVG(valor_despesa) as media FROM despesas_consolidadas
)
SELECT cnpj, COUNT(*) as trimestres_acima_da_media
FROM despesas_consolidadas, media_geral
WHERE valor_despesa > media_geral.media
GROUP BY cnpj
HAVING COUNT(*) >= 2;
