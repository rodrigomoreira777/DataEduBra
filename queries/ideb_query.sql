SELECT
    dados.ano AS ano,
    dados.sigla_uf AS sigla_uf,
    dados.id_escola AS id_escola,
    dados.rede AS rede,
    dados.ideb AS ideb
FROM `basedosdados.br_inep_ideb.escola` AS dados
WHERE
    dados.ano >= 2007
    AND dados.ano IS NOT NULL
    AND dados.sigla_uf IS NOT NULL
    AND dados.id_escola IS NOT NULL
    AND dados.rede IS NOT NULL
    AND dados.ideb IS NOT NULL
    AND dados.ideb BETWEEN 0 AND 10
