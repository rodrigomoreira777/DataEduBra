WITH
  dicionario_rede AS (
    SELECT
      chave AS chave_rede,
      valor AS descricao_rede
    FROM `basedosdados.br_inep_censo_escolar.dicionario`
    WHERE
      nome_coluna = 'rede'
      AND id_tabela = 'escola'
  ),
  dicionario_tipo_localizacao AS (
    SELECT
      chave AS chave_tipo_localizacao,
      valor AS descricao_tipo_localizacao
    FROM `basedosdados.br_inep_censo_escolar.dicionario`
    WHERE
      nome_coluna = 'tipo_localizacao'
      AND id_tabela = 'escola'
  )
SELECT
    dados.ano AS ano,
    dados.sigla_uf AS sigla_uf,
    dados.id_escola AS id_escola,
    d_rede.descricao_rede AS rede,
    dloc.descricao_tipo_localizacao AS tipo_localizacao,
    dados.internet_aprendizagem AS internet_aprendizagem
FROM `basedosdados.br_inep_censo_escolar.escola` AS dados
LEFT JOIN dicionario_rede d_rede
  ON dados.rede = d_rede.chave_rede
LEFT JOIN dicionario_tipo_localizacao dloc
  ON dados.tipo_localizacao = dloc.chave_tipo_localizacao
WHERE
  dados.ano IS NOT NULL
  AND dados.sigla_uf IS NOT NULL
  AND dados.id_escola IS NOT NULL
  AND dados.tipo_localizacao IS NOT NULL
  AND dados.rede IS NOT NULL
