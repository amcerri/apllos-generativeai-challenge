# Batch Query Results

## Summary

- **Generated:** 2025-10-03 16:42:49
- **Total Queries:** 20
- **Successful:** 20
- **Failed:** 0

<a id="table-of-contents"></a>
## 📋 Table of Contents

1. [Qual é a receita média por pedido nos últimos 6 meses, segme...](#query-1) - `analytics`
2. [Identifique os top 10 produtos que geram maior margem de con...](#query-2) - `analytics`
3. [Qual é a correlação entre valor do frete e taxa de cancelame...](#query-3) - `analytics`
4. [Compare a performance de receita entre diferentes métodos de...](#query-4) - `analytics`
5. [Qual é o perfil demográfico dos clientes com maior valor de ...](#query-5) - `analytics`
6. [Identifique padrões sazonais de compra por categoria de prod...](#query-6) - `analytics`
7. [Qual é a distribuição de clientes por frequência de compra e...](#query-7) - `analytics`
8. [Analise o comportamento de recompra: quantos clientes fizera...](#query-8) - `analytics`
9. [Qual é o tempo médio entre aprovação do pagamento e entrega,...](#query-9) - `analytics`
10. [Identifique gargalos operacionais analisando pedidos com mai...](#query-10) - `analytics`
11. [Qual é a taxa de pedidos entregues no prazo estimado, segmen...](#query-11) - `analytics`
12. [Compare a eficiência logística entre diferentes faixas de CE...](#query-12) - `analytics`
13. [Quais categorias de produtos têm maior crescimento de vendas...](#query-13) - `analytics`
14. [Identifique produtos com alta demanda mas baixa satisfação d...](#query-14) - `analytics`
15. [Qual é a penetração de cada categoria de produto por estado ...](#query-15) - `analytics`
16. [Analise a concentração de vendas: quantos vendedores represe...](#query-16) - `analytics`
17. [Calcule o churn rate de clientes por coorte de primeira comp...](#query-17) - `analytics`
18. [Qual é o impacto do número de parcelas no valor médio do ped...](#query-18) - `analytics`
19. [Identifique oportunidades de cross-selling analisando produt...](#query-19) - `analytics`
20. [Qual é a elasticidade-preço da demanda para as principais ca...](#query-20) - `knowledge`

---

## Results

<a id="query-1"></a>
### Query 1

#### 📝 Input

- **Query:** Qual é a receita média por pedido nos últimos 6 meses, segmentada por estado do cliente?

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.9
- **Reason:** average revenue per order by customer state over recent 6 months
- **Thread ID:** `e1aab6d2-194e-4228-9634-38a629f1e38c`

#### 💬 Response

```
Não foram encontrados pedidos nos últimos 6 meses, portanto não é possível calcular a receita média por pedido segmentada por estado.
```

#### 📊 Metadata

- **sql:** SELECT c.customer_state AS state, AVG(oi.price + oi.freight_value) AS avg_revenue FROM analytics.orders o JOIN analytics.customers c ON o.customer_id = c.customer_id JOIN analytics.order_items oi ON o.order_id = oi.order_id WHERE o.order_purchase_timestamp >= CURRENT_DATE - INTERVAL '6 months' GROUP BY state ORDER BY state
- **row_count:** 0
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-2"></a>
### Query 2

#### 📝 Input

- **Query:** Identifique os top 10 produtos que geram maior margem de contribuição considerando preço e frete

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.9
- **Reason:** top-N products by contribution margin using price and freight
- **Thread ID:** `a0abd978-be37-44de-a1d6-0212849b137d`

#### 💬 Response

```
Top 10 produtos por margem de contribuição:
  1. Produto ID bb50f2e236e5eea0100680137654686c: R$ 67.606,10
  2. Produto ID d1c427060a0f73f6b889a5c7c61f2ac4: R$ 60.976,03
  3. Produto ID 6cdd53843498f92890544667809f1595: R$ 59.093,99
  4. Produto ID 99a4788cb24856965c36a24e339b6058: R$ 51.071,60
  5. Produto ID d6160fb7873f184099d9bc95e30376af: R$ 50.326,18
  6. Produto ID 3dd2a17168ec895c781a9191c1e95ad7: R$ 48.212,22
  7. Produto ID aca2eb7d00ea1a7b8ebd4e68314663af: R$ 44.820,76
  8. Produto ID 5f504b3a1c75b73d6151be81eb05bdc9: R$ 41.725,81
  9. Produto ID 25c38557cf793876c5abdd5931f922db: R$ 40.311,95
  10. Produto ID 53b36df67ebb7c41585e8d54d6772e08: R$ 39.957,93
```

#### 📊 Metadata

- **sql:** SELECT oi.product_id, SUM(oi.price + oi.freight_value) AS total_contribution FROM analytics.order_items oi GROUP BY oi.product_id ORDER BY total_contribution DESC LIMIT 10
- **row_count:** 10
- **limit_applied:** True

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-3"></a>
### Query 3

#### 📝 Input

- **Query:** Qual é a correlação entre valor do frete e taxa de cancelamento de pedidos por região?

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.9
- **Reason:** correlation analysis between freight value and cancellation rate by region
- **Thread ID:** `e0f3ad12-6f03-4145-b1e1-98b478228d2c`

#### 💬 Response

```
Análise da correlação entre valor do frete e taxa de cancelamento de pedidos por região:
  AC: Frete R$ 40,07, Taxa de Cancelamento: 0,00%
  AL: Frete R$ 35,84, Taxa de Cancelamento: 0,00%
  AM: Frete R$ 33,21, Taxa de Cancelamento: 0,00%
  AP: Frete R$ 34,01, Taxa de Cancelamento: 0,00%
  BA: Frete R$ 26,36, Taxa de Cancelamento: 0,37%
  CE: Frete R$ 32,71, Taxa de Cancelamento: 0,27%
  DF: Frete R$ 21,04, Taxa de Cancelamento: 0,37%
  ES: Frete R$ 22,06, Taxa de Cancelamento: 0,35%
  GO: Frete R$ 22,77, Taxa de Cancelamento: 0,43%
  MA: Frete R$ 38,26, Taxa de Cancelamento: 0,49%
  MG: Frete R$ 20,63, Taxa de Cancelamento: 0,43%
  MS: Frete R$ 23,37, Taxa de Cancelamento: 0,12%
  MT: Frete R$ 28,17, Taxa de Cancelamento: 0,09%
  PA: Frete R$ 35,83, Taxa de Cancelamento: 0,09%
  PB: Frete R$ 42,72, Taxa de Cancelamento: 0,33%
  PE: Frete R$ 32,92, Taxa de Cancelamento: 0,28%
  PI: Frete R$ 39,15, Taxa de Cancelamento: 0,55%
  PR: Frete R$ 20,53, Taxa de Cancelamento: 0,37%
  RJ: Frete R$ 20,96, Taxa de Cancelamento: 0,47%
  RN: Frete R$ 35,65, Taxa de Cancelamento: 0,00%
  RO: Frete R$ 41,07, Taxa de Cancelamento: 0,36%
  RR: Frete R$ 42,98, Taxa de Cancelamento: 1,92%
  RS: Frete R$ 21,74, Taxa de Cancelamento: 0,37%
  SC: Frete R$ 21,47, Taxa de Cancelamento: 0,36%
  SE: Frete R$ 36,65, Taxa de Cancelamento: 0,00%
  SP: Frete R$ 15,15, Taxa de Cancelamento: 0,62%
  TO: Frete R$ 37,25, Taxa de Cancelamento: 0,32%

Total: 27 estados analisados.
```

#### 📊 Metadata

- **sql:** SELECT c.customer_state AS state, AVG(oi.freight_value) AS avg_freight, COUNT(CASE WHEN o.order_status LIKE '%cancel%' THEN 1 END) * 1.0 / COUNT(*) AS cancellation_rate FROM analytics.orders o JOIN analytics.customers c ON o.customer_id = c.customer_id JOIN analytics.order_items oi ON o.order_id = oi.order_id GROUP BY state ORDER BY state
- **row_count:** 27
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-4"></a>
### Query 4

#### 📝 Input

- **Query:** Compare a performance de receita entre diferentes métodos de pagamento nos últimos 12 meses

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.9
- **Reason:** revenue comparison by payment method over time
- **Thread ID:** `37d5e0ab-58cf-4b44-abe5-ed0d46f54adf`

#### 💬 Response

```
Não foram encontrados pedidos nos últimos 12 meses, portanto não é possível comparar a performance de receita entre os métodos de pagamento.
```

#### 📊 Metadata

- **sql:** SELECT op.payment_type, SUM(oi.price + oi.freight_value) AS revenue FROM analytics.orders o JOIN analytics.order_items oi ON o.order_id = oi.order_id JOIN analytics.order_payments op ON o.order_id = op.order_id WHERE o.order_purchase_timestamp >= CURRENT_DATE - INTERVAL '12 months' GROUP BY op.payment_type ORDER BY revenue DESC
- **row_count:** 0
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-5"></a>
### Query 5

#### 📝 Input

- **Query:** Qual é o perfil demográfico dos clientes com maior valor de pedido médio?

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.8
- **Reason:** demographic analysis with average order value
- **Thread ID:** `db202565-9ed2-4ea7-9c66-172874e76c0d`

#### 💬 Response

```
O perfil demográfico dos clientes com maior valor de pedido médio é o seguinte:

PB: R$ 248,33 (média)
AC: R$ 234,29 (média)
RO: R$ 233,20 (média)
AP: R$ 232,33 (média)
AL: R$ 227,08 (média)
RR: R$ 218,80 (média)
PA: R$ 215,92 (média)
SE: R$ 208,44 (média)
PI: R$ 207,11 (média)
TO: R$ 204,27 (média)
CE: R$ 199,90 (média)
MA: R$ 198,86 (média)
RN: R$ 196,78 (média)
MT: R$ 195,23 (média)
PE: R$ 187,99 (média)
MS: R$ 186,87 (média)
AM: R$ 181,60 (média)
BA: R$ 170,82 (média)
SC: R$ 165,98 (média)
GO: R$ 165,76 (média)
DF: R$ 161,13 (média)
RJ: R$ 158,53 (média)
RS: R$ 157,18 (média)
ES: R$ 154,71 (média)
MG: R$ 154,71 (média)
PR: R$ 154,15 (média)
SP: R$ 137,50 (média)

Total: 27 estados analisados.
```

#### 📊 Metadata

- **sql:** SELECT c.customer_state, AVG(op.payment_value) AS average_order_value FROM analytics.customers c JOIN analytics.orders o ON c.customer_id = o.customer_id JOIN analytics.order_payments op ON o.order_id = op.order_id GROUP BY c.customer_state ORDER BY average_order_value DESC
- **row_count:** 27
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-6"></a>
### Query 6

#### 📝 Input

- **Query:** Identifique padrões sazonais de compra por categoria de produto ao longo do ano

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.85
- **Reason:** seasonal purchase patterns by product category over time
- **Thread ID:** `a2b76c95-212d-444c-9ea6-58aaac0d5e62`

#### 💬 Response

```
Análise dos padrões sazonais de compra por categoria de produto ao longo do ano revela variações significativas nas compras. Abaixo estão alguns dos dados coletados, mostrando a quantidade de compras por categoria em meses específicos:

Setembro de 2016:
  beleza_saude: 3
  moveis_decoracao: 2
  telefonia: 1

Outubro de 2016:
  alimentos: 1
  audio: 2
  automotivo: 12
  bebes: 14
  beleza_saude: 48
  brinquedos: 27
  cama_mesa_banho: 8
  climatizacao: 10
  consoles_games: 10
  cool_stuff: 8
  eletronicos: 2
  esporte_lazer: 19
  fashion_bolsas_e_acessorios: 9
  fashion_calcados: 1
  fashion_roupa_feminina: 1
  fashion_roupa_masculina: 1
  ferramentas_jardim: 5
  fraldas_higiene: 1
  industria_comercio_e_negocios: 4
  informatica_acessorios: 21
  livros_interesse_geral: 1
  livros_tecnicos: 1
  market_place: 13
  moveis_decoracao: 67
  moveis_escritorio: 6
  perfumaria: 33
  pet_shop: 4
  relogios_presentes: 5
  telefonia: 10
  telefonia_fixa: 5
  utilidades_domesticas: 12

Janeiro de 2017:
  agro_industria_e_comercio: 3
  alimentos: 2
  automotivo: 34
  bebes: 41
  beleza_saude: 85
  brinquedos: 43
  cama_mesa_banho: 48
  casa_conforto_2: 2
  climatizacao: 4
  consoles_games: 23
  construcao_ferramentas_construcao: 1
  cool_stuff: 40
  dvds_blu_ray: 2
  eletrodomesticos_2: 8

Esses dados indicam que categorias como 'beleza_saude' e 'bebes' têm um desempenho forte em meses específicos, enquanto outras categorias como 'moveis_decoracao' mostram picos de vendas em outubro. Essa análise pode ajudar a direcionar campanhas de marketing e estoques conforme as tendências sazonais.

Dados por categoria:
beleza_saude: period: 2016-09-01 00:00:00, purchase_count: 3
moveis_decoracao: period: 2016-09-01 00:00:00, purchase_count: 2
telefonia: period: 2016-09-01 00:00:00, purchase_count: 1
alimentos: period: 2016-10-01 00:00:00, purchase_count: 1
audio: period: 2016-10-01 00:00:00, purchase_count: 2
automotivo: period: 2016-10-01 00:00:00, purchase_count: 12
bebes: period: 2016-10-01 00:00:00, purchase_count: 14
beleza_saude: period: 2016-10-01 00:00:00, purchase_count: 48
brinquedos: period: 2016-10-01 00:00:00, purchase_count: 27
cama_mesa_banho: period: 2016-10-01 00:00:00, purchase_count: 8
climatizacao: period: 2016-10-01 00:00:00, purchase_count: 10
consoles_games: period: 2016-10-01 00:00:00, purchase_count: 10
cool_stuff: period: 2016-10-01 00:00:00, purchase_count: 8
eletronicos: period: 2016-10-01 00:00:00, purchase_count: 2
esporte_lazer: period: 2016-10-01 00:00:00, purchase_count: 19
fashion_bolsas_e_acessorios: period: 2016-10-01 00:00:00, purchase_count: 9
fashion_calcados: period: 2016-10-01 00:00:00, purchase_count: 1
fashion_roupa_feminina: period: 2016-10-01 00:00:00, purchase_count: 1
fashion_roupa_masculina: period: 2016-10-01 00:00:00, purchase_count: 1
ferramentas_jardim: period: 2016-10-01 00:00:00, purchase_count: 5
fraldas_higiene: period: 2016-10-01 00:00:00, purchase_count: 1
industria_comercio_e_negocios: period: 2016-10-01 00:00:00, purchase_count: 4
informatica_acessorios: period: 2016-10-01 00:00:00, purchase_count: 21
livros_interesse_geral: period: 2016-10-01 00:00:00, purchase_count: 1
livros_tecnicos: period: 2016-10-01 00:00:00, purchase_count: 1
market_place: period: 2016-10-01 00:00:00, purchase_count: 13
moveis_decoracao: period: 2016-10-01 00:00:00, purchase_count: 67
moveis_escritorio: period: 2016-10-01 00:00:00, purchase_count: 6
perfumaria: period: 2016-10-01 00:00:00, purchase_count: 33
pet_shop: period: 2016-10-01 00:00:00, purchase_count: 4
relogios_presentes: period: 2016-10-01 00:00:00, purchase_count: 5
telefonia: period: 2016-10-01 00:00:00, purchase_count: 10
telefonia_fixa: period: 2016-10-01 00:00:00, purchase_count: 5
utilidades_domesticas: period: 2016-10-01 00:00:00, purchase_count: 12
fashion_bolsas_e_acessorios: period: 2016-12-01 00:00:00, purchase_count: 1
agro_industria_e_comercio: period: 2017-01-01 00:00:00, purchase_count: 3
alimentos: period: 2017-01-01 00:00:00, purchase_count: 2
automotivo: period: 2017-01-01 00:00:00, purchase_count: 34
bebes: period: 2017-01-01 00:00:00, purchase_count: 41
beleza_saude: period: 2017-01-01 00:00:00, purchase_count: 85
brinquedos: period: 2017-01-01 00:00:00, purchase_count: 43
cama_mesa_banho: period: 2017-01-01 00:00:00, purchase_count: 48
casa_conforto_2: period: 2017-01-01 00:00:00, purchase_count: 2
climatizacao: period: 2017-01-01 00:00:00, purchase_count: 4
consoles_games: period: 2017-01-01 00:00:00, purchase_count: 23
construcao_ferramentas_construcao: period: 2017-01-01 00:00:00, purchase_count: 1
cool_stuff: period: 2017-01-01 00:00:00, purchase_count: 40
dvds_blu_ray: period: 2017-01-01 00:00:00, purchase_count: 2
eletrodomesticos_2: period: 2017-01-01 00:00:00, purchase_count: 8
eletronicos: period: 2017-01-01 00:00:00, purchase_count: 11
eletroportateis: period: 2017-01-01 00:00:00, purchase_count: 6
esporte_lazer: period: 2017-01-01 00:00:00, purchase_count: 80
fashion_bolsas_e_acessorios: period: 2017-01-01 00:00:00, purchase_count: 35
fashion_calcados: period: 2017-01-01 00:00:00, purchase_count: 1
fashion_roupa_feminina: period: 2017-01-01 00:00:00, purchase_count: 2
fashion_roupa_masculina: period: 2017-01-01 00:00:00, purchase_count: 1
fashion_underwear_e_moda_praia: period: 2017-01-01 00:00:00, purchase_count: 2
ferramentas_jardim: period: 2017-01-01 00:00:00, purchase_count: 58
informatica_acessorios: period: 2017-01-01 00:00:00, purchase_count: 31
instrumentos_musicais: period: 2017-01-01 00:00:00, purchase_count: 1
livros_interesse_geral: period: 2017-01-01 00:00:00, purchase_count: 2
malas_acessorios: period: 2017-01-01 00:00:00, purchase_count: 5
market_place: period: 2017-01-01 00:00:00, purchase_count: 6
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2017-01-01 00:00:00, purchase_count: 1
moveis_decoracao: period: 2017-01-01 00:00:00, purchase_count: 182
moveis_escritorio: period: 2017-01-01 00:00:00, purchase_count: 10
moveis_quarto: period: 2017-01-01 00:00:00, purchase_count: 8
moveis_sala: period: 2017-01-01 00:00:00, purchase_count: 10
musica: period: 2017-01-01 00:00:00, purchase_count: 2
papelaria: period: 2017-01-01 00:00:00, purchase_count: 14
pcs: period: 2017-01-01 00:00:00, purchase_count: 1
perfumaria: period: 2017-01-01 00:00:00, purchase_count: 34
pet_shop: period: 2017-01-01 00:00:00, purchase_count: 15
relogios_presentes: period: 2017-01-01 00:00:00, purchase_count: 11
seguros_e_servicos: period: 2017-01-01 00:00:00, purchase_count: 1
telefonia: period: 2017-01-01 00:00:00, purchase_count: 26
telefonia_fixa: period: 2017-01-01 00:00:00, purchase_count: 22
utilidades_domesticas: period: 2017-01-01 00:00:00, purchase_count: 28
agro_industria_e_comercio: period: 2017-02-01 00:00:00, purchase_count: 7
alimentos: period: 2017-02-01 00:00:00, purchase_count: 9
audio: period: 2017-02-01 00:00:00, purchase_count: 5
automotivo: period: 2017-02-01 00:00:00, purchase_count: 86
bebes: period: 2017-02-01 00:00:00, purchase_count: 34
beleza_saude: period: 2017-02-01 00:00:00, purchase_count: 166
brinquedos: period: 2017-02-01 00:00:00, purchase_count: 67
cama_mesa_banho: period: 2017-02-01 00:00:00, purchase_count: 165
casa_conforto: period: 2017-02-01 00:00:00, purchase_count: 3
casa_construcao: period: 2017-02-01 00:00:00, purchase_count: 4
cine_foto: period: 2017-02-01 00:00:00, purchase_count: 1
climatizacao: period: 2017-02-01 00:00:00, purchase_count: 12
consoles_games: period: 2017-02-01 00:00:00, purchase_count: 18
construcao_ferramentas_construcao: period: 2017-02-01 00:00:00, purchase_count: 3
construcao_ferramentas_jardim: period: 2017-02-01 00:00:00, purchase_count: 2
construcao_ferramentas_seguranca: period: 2017-02-01 00:00:00, purchase_count: 1
cool_stuff: period: 2017-02-01 00:00:00, purchase_count: 70
dvds_blu_ray: period: 2017-02-01 00:00:00, purchase_count: 1
eletrodomesticos: period: 2017-02-01 00:00:00, purchase_count: 7
eletrodomesticos_2: period: 2017-02-01 00:00:00, purchase_count: 1
eletronicos: period: 2017-02-01 00:00:00, purchase_count: 19
eletroportateis: period: 2017-02-01 00:00:00, purchase_count: 28
esporte_lazer: period: 2017-02-01 00:00:00, purchase_count: 156
fashion_bolsas_e_acessorios: period: 2017-02-01 00:00:00, purchase_count: 39
fashion_calcados: period: 2017-02-01 00:00:00, purchase_count: 3
fashion_roupa_feminina: period: 2017-02-01 00:00:00, purchase_count: 4
fashion_roupa_masculina: period: 2017-02-01 00:00:00, purchase_count: 7
fashion_underwear_e_moda_praia: period: 2017-02-01 00:00:00, purchase_count: 8
ferramentas_jardim: period: 2017-02-01 00:00:00, purchase_count: 72
industria_comercio_e_negocios: period: 2017-02-01 00:00:00, purchase_count: 1
informatica_acessorios: period: 2017-02-01 00:00:00, purchase_count: 106
instrumentos_musicais: period: 2017-02-01 00:00:00, purchase_count: 9
livros_importados: period: 2017-02-01 00:00:00, purchase_count: 1
livros_interesse_geral: period: 2017-02-01 00:00:00, purchase_count: 8
livros_tecnicos: period: 2017-02-01 00:00:00, purchase_count: 1
malas_acessorios: period: 2017-02-01 00:00:00, purchase_count: 21
market_place: period: 2017-02-01 00:00:00, purchase_count: 22
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2017-02-01 00:00:00, purchase_count: 2
moveis_decoracao: period: 2017-02-01 00:00:00, purchase_count: 266
moveis_escritorio: period: 2017-02-01 00:00:00, purchase_count: 63
moveis_quarto: period: 2017-02-01 00:00:00, purchase_count: 1
moveis_sala: period: 2017-02-01 00:00:00, purchase_count: 24
papelaria: period: 2017-02-01 00:00:00, purchase_count: 19
pcs: period: 2017-02-01 00:00:00, purchase_count: 1
perfumaria: period: 2017-02-01 00:00:00, purchase_count: 51
pet_shop: period: 2017-02-01 00:00:00, purchase_count: 40
relogios_presentes: period: 2017-02-01 00:00:00, purchase_count: 37
tablets_impressao_imagem: period: 2017-02-01 00:00:00, purchase_count: 8
telefonia: period: 2017-02-01 00:00:00, purchase_count: 111
telefonia_fixa: period: 2017-02-01 00:00:00, purchase_count: 22
utilidades_domesticas: period: 2017-02-01 00:00:00, purchase_count: 81
agro_industria_e_comercio: period: 2017-03-01 00:00:00, purchase_count: 2
alimentos: period: 2017-03-01 00:00:00, purchase_count: 24
alimentos_bebidas: period: 2017-03-01 00:00:00, purchase_count: 5
artes: period: 2017-03-01 00:00:00, purchase_count: 5
audio: period: 2017-03-01 00:00:00, purchase_count: 14
automotivo: period: 2017-03-01 00:00:00, purchase_count: 87
bebes: period: 2017-03-01 00:00:00, purchase_count: 44
bebidas: period: 2017-03-01 00:00:00, purchase_count: 5
beleza_saude: period: 2017-03-01 00:00:00, purchase_count: 211
brinquedos: period: 2017-03-01 00:00:00, purchase_count: 103
cama_mesa_banho: period: 2017-03-01 00:00:00, purchase_count: 289
casa_conforto: period: 2017-03-01 00:00:00, purchase_count: 13
casa_conforto_2: period: 2017-03-01 00:00:00, purchase_count: 3
casa_construcao: period: 2017-03-01 00:00:00, purchase_count: 10
climatizacao: period: 2017-03-01 00:00:00, purchase_count: 17
consoles_games: period: 2017-03-01 00:00:00, purchase_count: 50
construcao_ferramentas_construcao: period: 2017-03-01 00:00:00, purchase_count: 4
construcao_ferramentas_seguranca: period: 2017-03-01 00:00:00, purchase_count: 2
cool_stuff: period: 2017-03-01 00:00:00, purchase_count: 123
dvds_blu_ray: period: 2017-03-01 00:00:00, purchase_count: 5
eletrodomesticos: period: 2017-03-01 00:00:00, purchase_count: 10
eletrodomesticos_2: period: 2017-03-01 00:00:00, purchase_count: 2
eletronicos: period: 2017-03-01 00:00:00, purchase_count: 37
eletroportateis: period: 2017-03-01 00:00:00, purchase_count: 31
esporte_lazer: period: 2017-03-01 00:00:00, purchase_count: 199
fashion_bolsas_e_acessorios: period: 2017-03-01 00:00:00, purchase_count: 68
fashion_calcados: period: 2017-03-01 00:00:00, purchase_count: 14
fashion_esporte: period: 2017-03-01 00:00:00, purchase_count: 1
fashion_roupa_feminina: period: 2017-03-01 00:00:00, purchase_count: 1
fashion_roupa_masculina: period: 2017-03-01 00:00:00, purchase_count: 9
fashion_underwear_e_moda_praia: period: 2017-03-01 00:00:00, purchase_count: 6
ferramentas_jardim: period: 2017-03-01 00:00:00, purchase_count: 150
industria_comercio_e_negocios: period: 2017-03-01 00:00:00, purchase_count: 2
informatica_acessorios: period: 2017-03-01 00:00:00, purchase_count: 174
instrumentos_musicais: period: 2017-03-01 00:00:00, purchase_count: 10
livros_interesse_geral: period: 2017-03-01 00:00:00, purchase_count: 25
livros_tecnicos: period: 2017-03-01 00:00:00, purchase_count: 2
malas_acessorios: period: 2017-03-01 00:00:00, purchase_count: 38
market_place: period: 2017-03-01 00:00:00, purchase_count: 17
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2017-03-01 00:00:00, purchase_count: 3
moveis_decoracao: period: 2017-03-01 00:00:00, purchase_count: 328
moveis_escritorio: period: 2017-03-01 00:00:00, purchase_count: 78
moveis_sala: period: 2017-03-01 00:00:00, purchase_count: 24
musica: period: 2017-03-01 00:00:00, purchase_count: 1
papelaria: period: 2017-03-01 00:00:00, purchase_count: 56
perfumaria: period: 2017-03-01 00:00:00, purchase_count: 106
pet_shop: period: 2017-03-01 00:00:00, purchase_count: 45
relogios_presentes: period: 2017-03-01 00:00:00, purchase_count: 81
sinalizacao_e_seguranca: period: 2017-03-01 00:00:00, purchase_count: 1
tablets_impressao_imagem: period: 2017-03-01 00:00:00, purchase_count: 5
telefonia: period: 2017-03-01 00:00:00, purchase_count: 172
telefonia_fixa: period: 2017-03-01 00:00:00, purchase_count: 21
utilidades_domesticas: period: 2017-03-01 00:00:00, purchase_count: 204
alimentos: period: 2017-04-01 00:00:00, purchase_count: 8
alimentos_bebidas: period: 2017-04-01 00:00:00, purchase_count: 3
artes: period: 2017-04-01 00:00:00, purchase_count: 1
artigos_de_natal: period: 2017-04-01 00:00:00, purchase_count: 1
audio: period: 2017-04-01 00:00:00, purchase_count: 11
automotivo: period: 2017-04-01 00:00:00, purchase_count: 88
bebes: period: 2017-04-01 00:00:00, purchase_count: 51
bebidas: period: 2017-04-01 00:00:00, purchase_count: 7
beleza_saude: period: 2017-04-01 00:00:00, purchase_count: 189
brinquedos: period: 2017-04-01 00:00:00, purchase_count: 113
cama_mesa_banho: period: 2017-04-01 00:00:00, purchase_count: 274
casa_conforto: period: 2017-04-01 00:00:00, purchase_count: 17
casa_conforto_2: period: 2017-04-01 00:00:00, purchase_count: 1
casa_construcao: period: 2017-04-01 00:00:00, purchase_count: 5
cine_foto: period: 2017-04-01 00:00:00, purchase_count: 2
climatizacao: period: 2017-04-01 00:00:00, purchase_count: 16
consoles_games: period: 2017-04-01 00:00:00, purchase_count: 17
construcao_ferramentas_ferramentas: period: 2017-04-01 00:00:00, purchase_count: 1
construcao_ferramentas_jardim: period: 2017-04-01 00:00:00, purchase_count: 8
cool_stuff: period: 2017-04-01 00:00:00, purchase_count: 121
dvds_blu_ray: period: 2017-04-01 00:00:00, purchase_count: 2
eletrodomesticos: period: 2017-04-01 00:00:00, purchase_count: 10
eletrodomesticos_2: period: 2017-04-01 00:00:00, purchase_count: 2
eletronicos: period: 2017-04-01 00:00:00, purchase_count: 48
eletroportateis: period: 2017-04-01 00:00:00, purchase_count: 21
esporte_lazer: period: 2017-04-01 00:00:00, purchase_count: 218
fashion_bolsas_e_acessorios: period: 2017-04-01 00:00:00, purchase_count: 50
fashion_calcados: period: 2017-04-01 00:00:00, purchase_count: 23
fashion_esporte: period: 2017-04-01 00:00:00, purchase_count: 4
fashion_roupa_feminina: period: 2017-04-01 00:00:00, purchase_count: 1
fashion_roupa_masculina: period: 2017-04-01 00:00:00, purchase_count: 7
fashion_underwear_e_moda_praia: period: 2017-04-01 00:00:00, purchase_count: 4
ferramentas_jardim: period: 2017-04-01 00:00:00, purchase_count: 119
informatica_acessorios: period: 2017-04-01 00:00:00, purchase_count: 136
instrumentos_musicais: period: 2017-04-01 00:00:00, purchase_count: 16
la_cuisine: period: 2017-04-01 00:00:00, purchase_count: 1
livros_importados: period: 2017-04-01 00:00:00, purchase_count: 1
livros_interesse_geral: period: 2017-04-01 00:00:00, purchase_count: 12
livros_tecnicos: period: 2017-04-01 00:00:00, purchase_count: 1
malas_acessorios: period: 2017-04-01 00:00:00, purchase_count: 49
market_place: period: 2017-04-01 00:00:00, purchase_count: 20
moveis_colchao_e_estofado: period: 2017-04-01 00:00:00, purchase_count: 1
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2017-04-01 00:00:00, purchase_count: 9
moveis_decoracao: period: 2017-04-01 00:00:00, purchase_count: 203
moveis_escritorio: period: 2017-04-01 00:00:00, purchase_count: 58
moveis_quarto: period: 2017-04-01 00:00:00, purchase_count: 5
moveis_sala: period: 2017-04-01 00:00:00, purchase_count: 12
musica: period: 2017-04-01 00:00:00, purchase_count: 2
papelaria: period: 2017-04-01 00:00:00, purchase_count: 36
pc_gamer: period: 2017-04-01 00:00:00, purchase_count: 2
perfumaria: period: 2017-04-01 00:00:00, purchase_count: 105
pet_shop: period: 2017-04-01 00:00:00, purchase_count: 51
relogios_presentes: period: 2017-04-01 00:00:00, purchase_count: 97
sinalizacao_e_seguranca: period: 2017-04-01 00:00:00, purchase_count: 3
tablets_impressao_imagem: period: 2017-04-01 00:00:00, purchase_count: 11
telefonia: period: 2017-04-01 00:00:00, purchase_count: 145
telefonia_fixa: period: 2017-04-01 00:00:00, purchase_count: 11
utilidades_domesticas: period: 2017-04-01 00:00:00, purchase_count: 183
agro_industria_e_comercio: period: 2017-05-01 00:00:00, purchase_count: 4
alimentos: period: 2017-05-01 00:00:00, purchase_count: 3
alimentos_bebidas: period: 2017-05-01 00:00:00, purchase_count: 17
artes: period: 2017-05-01 00:00:00, purchase_count: 8
artes_e_artesanato: period: 2017-05-01 00:00:00, purchase_count: 1
audio: period: 2017-05-01 00:00:00, purchase_count: 17
automotivo: period: 2017-05-01 00:00:00, purchase_count: 125
bebes: period: 2017-05-01 00:00:00, purchase_count: 108
bebidas: period: 2017-05-01 00:00:00, purchase_count: 1
beleza_saude: period: 2017-05-01 00:00:00, purchase_count: 290
brinquedos: period: 2017-05-01 00:00:00, purchase_count: 200
cama_mesa_banho: period: 2017-05-01 00:00:00, purchase_count: 369
casa_conforto: period: 2017-05-01 00:00:00, purchase_count: 37
casa_construcao: period: 2017-05-01 00:00:00, purchase_count: 7
cine_foto: period: 2017-05-01 00:00:00, purchase_count: 1
climatizacao: period: 2017-05-01 00:00:00, purchase_count: 8
consoles_games: period: 2017-05-01 00:00:00, purchase_count: 29
construcao_ferramentas_construcao: period: 2017-05-01 00:00:00, purchase_count: 1
construcao_ferramentas_ferramentas: period: 2017-05-01 00:00:00, purchase_count: 2
construcao_ferramentas_jardim: period: 2017-05-01 00:00:00, purchase_count: 8
cool_stuff: period: 2017-05-01 00:00:00, purchase_count: 247
dvds_blu_ray: period: 2017-05-01 00:00:00, purchase_count: 4
eletrodomesticos: period: 2017-05-01 00:00:00, purchase_count: 28
eletrodomesticos_2: period: 2017-05-01 00:00:00, purchase_count: 9
eletronicos: period: 2017-05-01 00:00:00, purchase_count: 68
eletroportateis: period: 2017-05-01 00:00:00, purchase_count: 18
esporte_lazer: period: 2017-05-01 00:00:00, purchase_count: 316
fashion_bolsas_e_acessorios: period: 2017-05-01 00:00:00, purchase_count: 110
fashion_calcados: period: 2017-05-01 00:00:00, purchase_count: 22
fashion_esporte: period: 2017-05-01 00:00:00, purchase_count: 3
fashion_roupa_feminina: period: 2017-05-01 00:00:00, purchase_count: 5
fashion_roupa_infanto_juvenil: period: 2017-05-01 00:00:00, purchase_count: 1
fashion_roupa_masculina: period: 2017-05-01 00:00:00, purchase_count: 4
fashion_underwear_e_moda_praia: period: 2017-05-01 00:00:00, purchase_count: 7
ferramentas_jardim: period: 2017-05-01 00:00:00, purchase_count: 141
industria_comercio_e_negocios: period: 2017-05-01 00:00:00, purchase_count: 2
informatica_acessorios: period: 2017-05-01 00:00:00, purchase_count: 320
instrumentos_musicais: period: 2017-05-01 00:00:00, purchase_count: 21
la_cuisine: period: 2017-05-01 00:00:00, purchase_count: 1
livros_interesse_geral: period: 2017-05-01 00:00:00, purchase_count: 20
livros_tecnicos: period: 2017-05-01 00:00:00, purchase_count: 3
malas_acessorios: period: 2017-05-01 00:00:00, purchase_count: 70
market_place: period: 2017-05-01 00:00:00, purchase_count: 22
moveis_colchao_e_estofado: period: 2017-05-01 00:00:00, purchase_count: 3
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2017-05-01 00:00:00, purchase_count: 9
moveis_decoracao: period: 2017-05-01 00:00:00, purchase_count: 279
moveis_escritorio: period: 2017-05-01 00:00:00, purchase_count: 56
moveis_quarto: period: 2017-05-01 00:00:00, purchase_count: 9
moveis_sala: period: 2017-05-01 00:00:00, purchase_count: 34
papelaria: period: 2017-05-01 00:00:00, purchase_count: 66
pc_gamer: period: 2017-05-01 00:00:00, purchase_count: 1
perfumaria: period: 2017-05-01 00:00:00, purchase_count: 145
pet_shop: period: 2017-05-01 00:00:00, purchase_count: 73
relogios_presentes: period: 2017-05-01 00:00:00, purchase_count: 135
sinalizacao_e_seguranca: period: 2017-05-01 00:00:00, purchase_count: 4
tablets_impressao_imagem: period: 2017-05-01 00:00:00, purchase_count: 7
telefonia: period: 2017-05-01 00:00:00, purchase_count: 224
telefonia_fixa: period: 2017-05-01 00:00:00, purchase_count: 10
utilidades_domesticas: period: 2017-05-01 00:00:00, purchase_count: 307
agro_industria_e_comercio: period: 2017-06-01 00:00:00, purchase_count: 1
alimentos: period: 2017-06-01 00:00:00, purchase_count: 1
alimentos_bebidas: period: 2017-06-01 00:00:00, purchase_count: 2
artes: period: 2017-06-01 00:00:00, purchase_count: 10
artigos_de_natal: period: 2017-06-01 00:00:00, purchase_count: 3
audio: period: 2017-06-01 00:00:00, purchase_count: 11
automotivo: period: 2017-06-01 00:00:00, purchase_count: 112
bebes: period: 2017-06-01 00:00:00, purchase_count: 78
bebidas: period: 2017-06-01 00:00:00, purchase_count: 1
beleza_saude: period: 2017-06-01 00:00:00, purchase_count: 260
brinquedos: period: 2017-06-01 00:00:00, purchase_count: 158
cama_mesa_banho: period: 2017-06-01 00:00:00, purchase_count: 382
casa_conforto: period: 2017-06-01 00:00:00, purchase_count: 18
casa_conforto_2: period: 2017-06-01 00:00:00, purchase_count: 1
casa_construcao: period: 2017-06-01 00:00:00, purchase_count: 8
cine_foto: period: 2017-06-01 00:00:00, purchase_count: 1
climatizacao: period: 2017-06-01 00:00:00, purchase_count: 11
consoles_games: period: 2017-06-01 00:00:00, purchase_count: 30
construcao_ferramentas_construcao: period: 2017-06-01 00:00:00, purchase_count: 8
construcao_ferramentas_jardim: period: 2017-06-01 00:00:00, purchase_count: 4
cool_stuff: period: 2017-06-01 00:00:00, purchase_count: 201
dvds_blu_ray: period: 2017-06-01 00:00:00, purchase_count: 4
eletrodomesticos: period: 2017-06-01 00:00:00, purchase_count: 43
eletrodomesticos_2: period: 2017-06-01 00:00:00, purchase_count: 6
eletronicos: period: 2017-06-01 00:00:00, purchase_count: 42
eletroportateis: period: 2017-06-01 00:00:00, purchase_count: 23
esporte_lazer: period: 2017-06-01 00:00:00, purchase_count: 277
fashion_bolsas_e_acessorios: period: 2017-06-01 00:00:00, purchase_count: 83
fashion_calcados: period: 2017-06-01 00:00:00, purchase_count: 20
fashion_esporte: period: 2017-06-01 00:00:00, purchase_count: 6
fashion_roupa_feminina: period: 2017-06-01 00:00:00, purchase_count: 3
fashion_roupa_infanto_juvenil: period: 2017-06-01 00:00:00, purchase_count: 1
fashion_roupa_masculina: period: 2017-06-01 00:00:00, purchase_count: 10
fashion_underwear_e_moda_praia: period: 2017-06-01 00:00:00, purchase_count: 1
ferramentas_jardim: period: 2017-06-01 00:00:00, purchase_count: 114
industria_comercio_e_negocios: period: 2017-06-01 00:00:00, purchase_count: 2
informatica_acessorios: period: 2017-06-01 00:00:00, purchase_count: 261
instrumentos_musicais: period: 2017-06-01 00:00:00, purchase_count: 20
livros_importados: period: 2017-06-01 00:00:00, purchase_count: 2
livros_interesse_geral: period: 2017-06-01 00:00:00, purchase_count: 21
livros_tecnicos: period: 2017-06-01 00:00:00, purchase_count: 2
malas_acessorios: period: 2017-06-01 00:00:00, purchase_count: 61
market_place: period: 2017-06-01 00:00:00, purchase_count: 16
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2017-06-01 00:00:00, purchase_count: 4
moveis_decoracao: period: 2017-06-01 00:00:00, purchase_count: 233
moveis_escritorio: period: 2017-06-01 00:00:00, purchase_count: 50
moveis_quarto: period: 2017-06-01 00:00:00, purchase_count: 2
moveis_sala: period: 2017-06-01 00:00:00, purchase_count: 15
musica: period: 2017-06-01 00:00:00, purchase_count: 4
papelaria: period: 2017-06-01 00:00:00, purchase_count: 38
pc_gamer: period: 2017-06-01 00:00:00, purchase_count: 1
perfumaria: period: 2017-06-01 00:00:00, purchase_count: 154
pet_shop: period: 2017-06-01 00:00:00, purchase_count: 64
portateis_casa_forno_e_cafe: period: 2017-06-01 00:00:00, purchase_count: 1
relogios_presentes: period: 2017-06-01 00:00:00, purchase_count: 124
sinalizacao_e_seguranca: period: 2017-06-01 00:00:00, purchase_count: 2
tablets_impressao_imagem: period: 2017-06-01 00:00:00, purchase_count: 6
telefonia: period: 2017-06-01 00:00:00, purchase_count: 160
telefonia_fixa: period: 2017-06-01 00:00:00, purchase_count: 12
utilidades_domesticas: period: 2017-06-01 00:00:00, purchase_count: 331
agro_industria_e_comercio: period: 2017-07-01 00:00:00, purchase_count: 1
alimentos: period: 2017-07-01 00:00:00, purchase_count: 7
alimentos_bebidas: period: 2017-07-01 00:00:00, purchase_count: 8
artes: period: 2017-07-01 00:00:00, purchase_count: 3
artes_e_artesanato: period: 2017-07-01 00:00:00, purchase_count: 1
artigos_de_festas: period: 2017-07-01 00:00:00, purchase_count: 1
artigos_de_natal: period: 2017-07-01 00:00:00, purchase_count: 2
audio: period: 2017-07-01 00:00:00, purchase_count: 7
automotivo: period: 2017-07-01 00:00:00, purchase_count: 117
bebes: period: 2017-07-01 00:00:00, purchase_count: 129
bebidas: period: 2017-07-01 00:00:00, purchase_count: 3
beleza_saude: period: 2017-07-01 00:00:00, purchase_count: 316
brinquedos: period: 2017-07-01 00:00:00, purchase_count: 207
cama_mesa_banho: period: 2017-07-01 00:00:00, purchase_count: 579
casa_conforto: period: 2017-07-01 00:00:00, purchase_count: 43
casa_conforto_2: period: 2017-07-01 00:00:00, purchase_count: 1
casa_construcao: period: 2017-07-01 00:00:00, purchase_count: 2
cds_dvds_musicais: period: 2017-07-01 00:00:00, purchase_count: 5
climatizacao: period: 2017-07-01 00:00:00, purchase_count: 5
consoles_games: period: 2017-07-01 00:00:00, purchase_count: 48
construcao_ferramentas_construcao: period: 2017-07-01 00:00:00, purchase_count: 6
construcao_ferramentas_iluminacao: period: 2017-07-01 00:00:00, purchase_count: 1
construcao_ferramentas_jardim: period: 2017-07-01 00:00:00, purchase_count: 8
cool_stuff: period: 2017-07-01 00:00:00, purchase_count: 230
dvds_blu_ray: period: 2017-07-01 00:00:00, purchase_count: 4
eletrodomesticos: period: 2017-07-01 00:00:00, purchase_count: 37
eletrodomesticos_2: period: 2017-07-01 00:00:00, purchase_count: 7
eletronicos: period: 2017-07-01 00:00:00, purchase_count: 97
eletroportateis: period: 2017-07-01 00:00:00, purchase_count: 34
esporte_lazer: period: 2017-07-01 00:00:00, purchase_count: 387
fashion_bolsas_e_acessorios: period: 2017-07-01 00:00:00, purchase_count: 88
fashion_calcados: period: 2017-07-01 00:00:00, purchase_count: 20
fashion_esporte: period: 2017-07-01 00:00:00, purchase_count: 1
fashion_roupa_feminina: period: 2017-07-01 00:00:00, purchase_count: 4
fashion_roupa_masculina: period: 2017-07-01 00:00:00, purchase_count: 9
fashion_underwear_e_moda_praia: period: 2017-07-01 00:00:00, purchase_count: 3
ferramentas_jardim: period: 2017-07-01 00:00:00, purchase_count: 190
industria_comercio_e_negocios: period: 2017-07-01 00:00:00, purchase_count: 2
informatica_acessorios: period: 2017-07-01 00:00:00, purchase_count: 326
instrumentos_musicais: period: 2017-07-01 00:00:00, purchase_count: 32
la_cuisine: period: 2017-07-01 00:00:00, purchase_count: 4
livros_interesse_geral: period: 2017-07-01 00:00:00, purchase_count: 13
livros_tecnicos: period: 2017-07-01 00:00:00, purchase_count: 2
malas_acessorios: period: 2017-07-01 00:00:00, purchase_count: 74
market_place: period: 2017-07-01 00:00:00, purchase_count: 13
moveis_colchao_e_estofado: period: 2017-07-01 00:00:00, purchase_count: 1
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2017-07-01 00:00:00, purchase_count: 11
moveis_decoracao: period: 2017-07-01 00:00:00, purchase_count: 320
moveis_escritorio: period: 2017-07-01 00:00:00, purchase_count: 115
moveis_quarto: period: 2017-07-01 00:00:00, purchase_count: 5
moveis_sala: period: 2017-07-01 00:00:00, purchase_count: 31
musica: period: 2017-07-01 00:00:00, purchase_count: 1
papelaria: period: 2017-07-01 00:00:00, purchase_count: 80
perfumaria: period: 2017-07-01 00:00:00, purchase_count: 126
pet_shop: period: 2017-07-01 00:00:00, purchase_count: 86
relogios_presentes: period: 2017-07-01 00:00:00, purchase_count: 168
sinalizacao_e_seguranca: period: 2017-07-01 00:00:00, purchase_count: 6
tablets_impressao_imagem: period: 2017-07-01 00:00:00, purchase_count: 2
telefonia: period: 2017-07-01 00:00:00, purchase_count: 144
telefonia_fixa: period: 2017-07-01 00:00:00, purchase_count: 9
utilidades_domesticas: period: 2017-07-01 00:00:00, purchase_count: 276
agro_industria_e_comercio: period: 2017-08-01 00:00:00, purchase_count: 4
alimentos: period: 2017-08-01 00:00:00, purchase_count: 8
alimentos_bebidas: period: 2017-08-01 00:00:00, purchase_count: 15
artes: period: 2017-08-01 00:00:00, purchase_count: 4
artigos_de_natal: period: 2017-08-01 00:00:00, purchase_count: 1
audio: period: 2017-08-01 00:00:00, purchase_count: 7
automotivo: period: 2017-08-01 00:00:00, purchase_count: 166
bebes: period: 2017-08-01 00:00:00, purchase_count: 132
bebidas: period: 2017-08-01 00:00:00, purchase_count: 2
beleza_saude: period: 2017-08-01 00:00:00, purchase_count: 360
brinquedos: period: 2017-08-01 00:00:00, purchase_count: 184
cama_mesa_banho: period: 2017-08-01 00:00:00, purchase_count: 512
casa_conforto: period: 2017-08-01 00:00:00, purchase_count: 28
casa_conforto_2: period: 2017-08-01 00:00:00, purchase_count: 3
casa_construcao: period: 2017-08-01 00:00:00, purchase_count: 1
cds_dvds_musicais: period: 2017-08-01 00:00:00, purchase_count: 3
climatizacao: period: 2017-08-01 00:00:00, purchase_count: 15
consoles_games: period: 2017-08-01 00:00:00, purchase_count: 90
construcao_ferramentas_construcao: period: 2017-08-01 00:00:00, purchase_count: 7
construcao_ferramentas_iluminacao: period: 2017-08-01 00:00:00, purchase_count: 2
construcao_ferramentas_jardim: period: 2017-08-01 00:00:00, purchase_count: 10
construcao_ferramentas_seguranca: period: 2017-08-01 00:00:00, purchase_count: 1
cool_stuff: period: 2017-08-01 00:00:00, purchase_count: 264
dvds_blu_ray: period: 2017-08-01 00:00:00, purchase_count: 6
eletrodomesticos: period: 2017-08-01 00:00:00, purchase_count: 49
eletrodomesticos_2: period: 2017-08-01 00:00:00, purchase_count: 17
eletronicos: period: 2017-08-01 00:00:00, purchase_count: 56
eletroportateis: period: 2017-08-01 00:00:00, purchase_count: 36
esporte_lazer: period: 2017-08-01 00:00:00, purchase_count: 425
fashion_bolsas_e_acessorios: period: 2017-08-01 00:00:00, purchase_count: 99
fashion_calcados: period: 2017-08-01 00:00:00, purchase_count: 22
fashion_esporte: period: 2017-08-01 00:00:00, purchase_count: 2
fashion_roupa_feminina: period: 2017-08-01 00:00:00, purchase_count: 4
fashion_roupa_infanto_juvenil: period: 2017-08-01 00:00:00, purchase_count: 1
fashion_roupa_masculina: period: 2017-08-01 00:00:00, purchase_count: 15
fashion_underwear_e_moda_praia: period: 2017-08-01 00:00:00, purchase_count: 13
ferramentas_jardim: period: 2017-08-01 00:00:00, purchase_count: 238
industria_comercio_e_negocios: period: 2017-08-01 00:00:00, purchase_count: 3
informatica_acessorios: period: 2017-08-01 00:00:00, purchase_count: 350
instrumentos_musicais: period: 2017-08-01 00:00:00, purchase_count: 27
la_cuisine: period: 2017-08-01 00:00:00, purchase_count: 2
livros_importados: period: 2017-08-01 00:00:00, purchase_count: 1
livros_interesse_geral: period: 2017-08-01 00:00:00, purchase_count: 29
livros_tecnicos: period: 2017-08-01 00:00:00, purchase_count: 9
malas_acessorios: period: 2017-08-01 00:00:00, purchase_count: 63
market_place: period: 2017-08-01 00:00:00, purchase_count: 23
moveis_colchao_e_estofado: period: 2017-08-01 00:00:00, purchase_count: 2
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2017-08-01 00:00:00, purchase_count: 7
moveis_decoracao: period: 2017-08-01 00:00:00, purchase_count: 436
moveis_escritorio: period: 2017-08-01 00:00:00, purchase_count: 58
moveis_quarto: period: 2017-08-01 00:00:00, purchase_count: 3
moveis_sala: period: 2017-08-01 00:00:00, purchase_count: 23
papelaria: period: 2017-08-01 00:00:00, purchase_count: 80
pcs: period: 2017-08-01 00:00:00, purchase_count: 29
perfumaria: period: 2017-08-01 00:00:00, purchase_count: 128
pet_shop: period: 2017-08-01 00:00:00, purchase_count: 90
portateis_casa_forno_e_cafe: period: 2017-08-01 00:00:00, purchase_count: 2
relogios_presentes: period: 2017-08-01 00:00:00, purchase_count: 212
sinalizacao_e_seguranca: period: 2017-08-01 00:00:00, purchase_count: 4
tablets_impressao_imagem: period: 2017-08-01 00:00:00, purchase_count: 6
telefonia: period: 2017-08-01 00:00:00, purchase_count: 136
telefonia_fixa: period: 2017-08-01 00:00:00, purchase_count: 20
utilidades_domesticas: period: 2017-08-01 00:00:00, purchase_count: 288
agro_industria_e_comercio: period: 2017-09-01 00:00:00, purchase_count: 4
alimentos: period: 2017-09-01 00:00:00, purchase_count: 17
alimentos_bebidas: period: 2017-09-01 00:00:00, purchase_count: 9
artes: period: 2017-09-01 00:00:00, purchase_count: 3
artigos_de_festas: period: 2017-09-01 00:00:00, purchase_count: 2
artigos_de_natal: period: 2017-09-01 00:00:00, purchase_count: 4
audio: period: 2017-09-01 00:00:00, purchase_count: 10
automotivo: period: 2017-09-01 00:00:00, purchase_count: 108
bebes: period: 2017-09-01 00:00:00, purchase_count: 174
bebidas: period: 2017-09-01 00:00:00, purchase_count: 8
beleza_saude: period: 2017-09-01 00:00:00, purchase_count: 380
brinquedos: period: 2017-09-01 00:00:00, purchase_count: 297
cama_mesa_banho: period: 2017-09-01 00:00:00, purchase_count: 533
casa_conforto: period: 2017-09-01 00:00:00, purchase_count: 33
casa_conforto_2: period: 2017-09-01 00:00:00, purchase_count: 1
casa_construcao: period: 2017-09-01 00:00:00, purchase_count: 11
cine_foto: period: 2017-09-01 00:00:00, purchase_count: 1
climatizacao: period: 2017-09-01 00:00:00, purchase_count: 8
consoles_games: period: 2017-09-01 00:00:00, purchase_count: 66
construcao_ferramentas_construcao: period: 2017-09-01 00:00:00, purchase_count: 11
construcao_ferramentas_ferramentas: period: 2017-09-01 00:00:00, purchase_count: 3
construcao_ferramentas_iluminacao: period: 2017-09-01 00:00:00, purchase_count: 1
construcao_ferramentas_jardim: period: 2017-09-01 00:00:00, purchase_count: 6
construcao_ferramentas_seguranca: period: 2017-09-01 00:00:00, purchase_count: 5
cool_stuff: period: 2017-09-01 00:00:00, purchase_count: 207
dvds_blu_ray: period: 2017-09-01 00:00:00, purchase_count: 2
eletrodomesticos: period: 2017-09-01 00:00:00, purchase_count: 10
eletrodomesticos_2: period: 2017-09-01 00:00:00, purchase_count: 6
eletronicos: period: 2017-09-01 00:00:00, purchase_count: 67
eletroportateis: period: 2017-09-01 00:00:00, purchase_count: 33
esporte_lazer: period: 2017-09-01 00:00:00, purchase_count: 461
fashion_bolsas_e_acessorios: period: 2017-09-01 00:00:00, purchase_count: 124
fashion_calcados: period: 2017-09-01 00:00:00, purchase_count: 14
fashion_esporte: period: 2017-09-01 00:00:00, purchase_count: 5
fashion_roupa_feminina: period: 2017-09-01 00:00:00, purchase_count: 4
fashion_roupa_infanto_juvenil: period: 2017-09-01 00:00:00, purchase_count: 1
fashion_roupa_masculina: period: 2017-09-01 00:00:00, purchase_count: 16
fashion_underwear_e_moda_praia: period: 2017-09-01 00:00:00, purchase_count: 18
ferramentas_jardim: period: 2017-09-01 00:00:00, purchase_count: 225
industria_comercio_e_negocios: period: 2017-09-01 00:00:00, purchase_count: 2
informatica_acessorios: period: 2017-09-01 00:00:00, purchase_count: 253
instrumentos_musicais: period: 2017-09-01 00:00:00, purchase_count: 28
livros_importados: period: 2017-09-01 00:00:00, purchase_count: 4
livros_interesse_geral: period: 2017-09-01 00:00:00, purchase_count: 15
livros_tecnicos: period: 2017-09-01 00:00:00, purchase_count: 8
malas_acessorios: period: 2017-09-01 00:00:00, purchase_count: 42
market_place: period: 2017-09-01 00:00:00, purchase_count: 11
moveis_colchao_e_estofado: period: 2017-09-01 00:00:00, purchase_count: 1
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2017-09-01 00:00:00, purchase_count: 5
moveis_decoracao: period: 2017-09-01 00:00:00, purchase_count: 348
moveis_escritorio: period: 2017-09-01 00:00:00, purchase_count: 61
moveis_quarto: period: 2017-09-01 00:00:00, purchase_count: 4
moveis_sala: period: 2017-09-01 00:00:00, purchase_count: 11
papelaria: period: 2017-09-01 00:00:00, purchase_count: 77
pcs: period: 2017-09-01 00:00:00, purchase_count: 41
perfumaria: period: 2017-09-01 00:00:00, purchase_count: 160
pet_shop: period: 2017-09-01 00:00:00, purchase_count: 71
portateis_casa_forno_e_cafe: period: 2017-09-01 00:00:00, purchase_count: 1
relogios_presentes: period: 2017-09-01 00:00:00, purchase_count: 268
seguros_e_servicos: period: 2017-09-01 00:00:00, purchase_count: 1
sinalizacao_e_seguranca: period: 2017-09-01 00:00:00, purchase_count: 9
tablets_impressao_imagem: period: 2017-09-01 00:00:00, purchase_count: 3
telefonia: period: 2017-09-01 00:00:00, purchase_count: 177
telefonia_fixa: period: 2017-09-01 00:00:00, purchase_count: 13
utilidades_domesticas: period: 2017-09-01 00:00:00, purchase_count: 255
agro_industria_e_comercio: period: 2017-10-01 00:00:00, purchase_count: 5
alimentos: period: 2017-10-01 00:00:00, purchase_count: 17
alimentos_bebidas: period: 2017-10-01 00:00:00, purchase_count: 17
artes: period: 2017-10-01 00:00:00, purchase_count: 3
artigos_de_festas: period: 2017-10-01 00:00:00, purchase_count: 2
artigos_de_natal: period: 2017-10-01 00:00:00, purchase_count: 12
audio: period: 2017-10-01 00:00:00, purchase_count: 32
automotivo: period: 2017-10-01 00:00:00, purchase_count: 150
bebes: period: 2017-10-01 00:00:00, purchase_count: 138
bebidas: period: 2017-10-01 00:00:00, purchase_count: 12
beleza_saude: period: 2017-10-01 00:00:00, purchase_count: 361
brinquedos: period: 2017-10-01 00:00:00, purchase_count: 290
cama_mesa_banho: period: 2017-10-01 00:00:00, purchase_count: 545
casa_conforto: period: 2017-10-01 00:00:00, purchase_count: 27
casa_conforto_2: period: 2017-10-01 00:00:00, purchase_count: 5
casa_construcao: period: 2017-10-01 00:00:00, purchase_count: 18
cds_dvds_musicais: period: 2017-10-01 00:00:00, purchase_count: 1
cine_foto: period: 2017-10-01 00:00:00, purchase_count: 1
climatizacao: period: 2017-10-01 00:00:00, purchase_count: 12
consoles_games: period: 2017-10-01 00:00:00, purchase_count: 109
construcao_ferramentas_construcao: period: 2017-10-01 00:00:00, purchase_count: 19
construcao_ferramentas_ferramentas: period: 2017-10-01 00:00:00, purchase_count: 5
construcao_ferramentas_iluminacao: period: 2017-10-01 00:00:00, purchase_count: 2
construcao_ferramentas_jardim: period: 2017-10-01 00:00:00, purchase_count: 9
construcao_ferramentas_seguranca: period: 2017-10-01 00:00:00, purchase_count: 12
cool_stuff: period: 2017-10-01 00:00:00, purchase_count: 258
dvds_blu_ray: period: 2017-10-01 00:00:00, purchase_count: 5
eletrodomesticos: period: 2017-10-01 00:00:00, purchase_count: 8
eletrodomesticos_2: period: 2017-10-01 00:00:00, purchase_count: 10
eletronicos: period: 2017-10-01 00:00:00, purchase_count: 63
eletroportateis: period: 2017-10-01 00:00:00, purchase_count: 32
esporte_lazer: period: 2017-10-01 00:00:00, purchase_count: 471
fashion_bolsas_e_acessorios: period: 2017-10-01 00:00:00, purchase_count: 110
fashion_calcados: period: 2017-10-01 00:00:00, purchase_count: 18
fashion_esporte: period: 2017-10-01 00:00:00, purchase_count: 1
fashion_roupa_infanto_juvenil: period: 2017-10-01 00:00:00, purchase_count: 1
fashion_roupa_masculina: period: 2017-10-01 00:00:00, purchase_count: 11
fashion_underwear_e_moda_praia: period: 2017-10-01 00:00:00, purchase_count: 3
ferramentas_jardim: period: 2017-10-01 00:00:00, purchase_count: 281
industria_comercio_e_negocios: period: 2017-10-01 00:00:00, purchase_count: 5
informatica_acessorios: period: 2017-10-01 00:00:00, purchase_count: 322
instrumentos_musicais: period: 2017-10-01 00:00:00, purchase_count: 27
la_cuisine: period: 2017-10-01 00:00:00, purchase_count: 1
livros_interesse_geral: period: 2017-10-01 00:00:00, purchase_count: 11
livros_tecnicos: period: 2017-10-01 00:00:00, purchase_count: 6
malas_acessorios: period: 2017-10-01 00:00:00, purchase_count: 56
market_place: period: 2017-10-01 00:00:00, purchase_count: 11
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2017-10-01 00:00:00, purchase_count: 16
moveis_decoracao: period: 2017-10-01 00:00:00, purchase_count: 379
moveis_escritorio: period: 2017-10-01 00:00:00, purchase_count: 102
moveis_quarto: period: 2017-10-01 00:00:00, purchase_count: 4
moveis_sala: period: 2017-10-01 00:00:00, purchase_count: 19
musica: period: 2017-10-01 00:00:00, purchase_count: 1
papelaria: period: 2017-10-01 00:00:00, purchase_count: 101
pcs: period: 2017-10-01 00:00:00, purchase_count: 27
perfumaria: period: 2017-10-01 00:00:00, purchase_count: 189
pet_shop: period: 2017-10-01 00:00:00, purchase_count: 76
relogios_presentes: period: 2017-10-01 00:00:00, purchase_count: 314
sinalizacao_e_seguranca: period: 2017-10-01 00:00:00, purchase_count: 10
tablets_impressao_imagem: period: 2017-10-01 00:00:00, purchase_count: 1
telefonia: period: 2017-10-01 00:00:00, purchase_count: 253
telefonia_fixa: period: 2017-10-01 00:00:00, purchase_count: 7
utilidades_domesticas: period: 2017-10-01 00:00:00, purchase_count: 235
agro_industria_e_comercio: period: 2017-11-01 00:00:00, purchase_count: 19
alimentos: period: 2017-11-01 00:00:00, purchase_count: 17
alimentos_bebidas: period: 2017-11-01 00:00:00, purchase_count: 33
artes: period: 2017-11-01 00:00:00, purchase_count: 1
artigos_de_festas: period: 2017-11-01 00:00:00, purchase_count: 4
artigos_de_natal: period: 2017-11-01 00:00:00, purchase_count: 24
audio: period: 2017-11-01 00:00:00, purchase_count: 36
automotivo: period: 2017-11-01 00:00:00, purchase_count: 263
bebes: period: 2017-11-01 00:00:00, purchase_count: 203
bebidas: period: 2017-11-01 00:00:00, purchase_count: 19
beleza_saude: period: 2017-11-01 00:00:00, purchase_count: 584
brinquedos: period: 2017-11-01 00:00:00, purchase_count: 495
cama_mesa_banho: period: 2017-11-01 00:00:00, purchase_count: 975
casa_conforto: period: 2017-11-01 00:00:00, purchase_count: 45
casa_conforto_2: period: 2017-11-01 00:00:00, purchase_count: 3
casa_construcao: period: 2017-11-01 00:00:00, purchase_count: 38
cds_dvds_musicais: period: 2017-11-01 00:00:00, purchase_count: 3
cine_foto: period: 2017-11-01 00:00:00, purchase_count: 1
climatizacao: period: 2017-11-01 00:00:00, purchase_count: 19
consoles_games: period: 2017-11-01 00:00:00, purchase_count: 134
construcao_ferramentas_construcao: period: 2017-11-01 00:00:00, purchase_count: 47
construcao_ferramentas_ferramentas: period: 2017-11-01 00:00:00, purchase_count: 5
construcao_ferramentas_iluminacao: period: 2017-11-01 00:00:00, purchase_count: 10
construcao_ferramentas_jardim: period: 2017-11-01 00:00:00, purchase_count: 17
construcao_ferramentas_seguranca: period: 2017-11-01 00:00:00, purchase_count: 15
cool_stuff: period: 2017-11-01 00:00:00, purchase_count: 302
dvds_blu_ray: period: 2017-11-01 00:00:00, purchase_count: 3
eletrodomesticos: period: 2017-11-01 00:00:00, purchase_count: 25
eletrodomesticos_2: period: 2017-11-01 00:00:00, purchase_count: 13
eletronicos: period: 2017-11-01 00:00:00, purchase_count: 184
eletroportateis: period: 2017-11-01 00:00:00, purchase_count: 31
esporte_lazer: period: 2017-11-01 00:00:00, purchase_count: 612
fashion_bolsas_e_acessorios: period: 2017-11-01 00:00:00, purchase_count: 200
fashion_calcados: period: 2017-11-01 00:00:00, purchase_count: 20
fashion_esporte: period: 2017-11-01 00:00:00, purchase_count: 1
fashion_roupa_feminina: period: 2017-11-01 00:00:00, purchase_count: 3
fashion_roupa_masculina: period: 2017-11-01 00:00:00, purchase_count: 12
fashion_underwear_e_moda_praia: period: 2017-11-01 00:00:00, purchase_count: 10
ferramentas_jardim: period: 2017-11-01 00:00:00, purchase_count: 550
flores: period: 2017-11-01 00:00:00, purchase_count: 6
industria_comercio_e_negocios: period: 2017-11-01 00:00:00, purchase_count: 7
informatica_acessorios: period: 2017-11-01 00:00:00, purchase_count: 532
instrumentos_musicais: period: 2017-11-01 00:00:00, purchase_count: 49
la_cuisine: period: 2017-11-01 00:00:00, purchase_count: 1
livros_importados: period: 2017-11-01 00:00:00, purchase_count: 4
livros_interesse_geral: period: 2017-11-01 00:00:00, purchase_count: 38
livros_tecnicos: period: 2017-11-01 00:00:00, purchase_count: 6
malas_acessorios: period: 2017-11-01 00:00:00, purchase_count: 72
market_place: period: 2017-11-01 00:00:00, purchase_count: 16
moveis_colchao_e_estofado: period: 2017-11-01 00:00:00, purchase_count: 2
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2017-11-01 00:00:00, purchase_count: 33
moveis_decoracao: period: 2017-11-01 00:00:00, purchase_count: 783
moveis_escritorio: period: 2017-11-01 00:00:00, purchase_count: 102
moveis_quarto: period: 2017-11-01 00:00:00, purchase_count: 3
moveis_sala: period: 2017-11-01 00:00:00, purchase_count: 39
papelaria: period: 2017-11-01 00:00:00, purchase_count: 166
pcs: period: 2017-11-01 00:00:00, purchase_count: 7
perfumaria: period: 2017-11-01 00:00:00, purchase_count: 311
pet_shop: period: 2017-11-01 00:00:00, purchase_count: 99
relogios_presentes: period: 2017-11-01 00:00:00, purchase_count: 469
sinalizacao_e_seguranca: period: 2017-11-01 00:00:00, purchase_count: 5
tablets_impressao_imagem: period: 2017-11-01 00:00:00, purchase_count: 6
telefonia: period: 2017-11-01 00:00:00, purchase_count: 383
telefonia_fixa: period: 2017-11-01 00:00:00, purchase_count: 5
utilidades_domesticas: period: 2017-11-01 00:00:00, purchase_count: 423
agro_industria_e_comercio: period: 2017-12-01 00:00:00, purchase_count: 11
alimentos: period: 2017-12-01 00:00:00, purchase_count: 14
alimentos_bebidas: period: 2017-12-01 00:00:00, purchase_count: 22
artes: period: 2017-12-01 00:00:00, purchase_count: 3
artigos_de_festas: period: 2017-12-01 00:00:00, purchase_count: 2
artigos_de_natal: period: 2017-12-01 00:00:00, purchase_count: 16
audio: period: 2017-12-01 00:00:00, purchase_count: 17
automotivo: period: 2017-12-01 00:00:00, purchase_count: 268
bebes: period: 2017-12-01 00:00:00, purchase_count: 143
bebidas: period: 2017-12-01 00:00:00, purchase_count: 34
beleza_saude: period: 2017-12-01 00:00:00, purchase_count: 466
brinquedos: period: 2017-12-01 00:00:00, purchase_count: 445
cama_mesa_banho: period: 2017-12-01 00:00:00, purchase_count: 552
casa_conforto: period: 2017-12-01 00:00:00, purchase_count: 14
casa_construcao: period: 2017-12-01 00:00:00, purchase_count: 39
cds_dvds_musicais: period: 2017-12-01 00:00:00, purchase_count: 1
climatizacao: period: 2017-12-01 00:00:00, purchase_count: 3
consoles_games: period: 2017-12-01 00:00:00, purchase_count: 93
construcao_ferramentas_construcao: period: 2017-12-01 00:00:00, purchase_count: 27
construcao_ferramentas_ferramentas: period: 2017-12-01 00:00:00, purchase_count: 6
construcao_ferramentas_iluminacao: period: 2017-12-01 00:00:00, purchase_count: 2
construcao_ferramentas_jardim: period: 2017-12-01 00:00:00, purchase_count: 6
construcao_ferramentas_seguranca: period: 2017-12-01 00:00:00, purchase_count: 7
cool_stuff: period: 2017-12-01 00:00:00, purchase_count: 252
dvds_blu_ray: period: 2017-12-01 00:00:00, purchase_count: 1
eletrodomesticos: period: 2017-12-01 00:00:00, purchase_count: 16
eletrodomesticos_2: period: 2017-12-01 00:00:00, purchase_count: 8
eletronicos: period: 2017-12-01 00:00:00, purchase_count: 210
eletroportateis: period: 2017-12-01 00:00:00, purchase_count: 29
esporte_lazer: period: 2017-12-01 00:00:00, purchase_count: 493
fashion_bolsas_e_acessorios: period: 2017-12-01 00:00:00, purchase_count: 135
fashion_calcados: period: 2017-12-01 00:00:00, purchase_count: 13
fashion_esporte: period: 2017-12-01 00:00:00, purchase_count: 1
fashion_roupa_masculina: period: 2017-12-01 00:00:00, purchase_count: 4
fashion_underwear_e_moda_praia: period: 2017-12-01 00:00:00, purchase_count: 13
ferramentas_jardim: period: 2017-12-01 00:00:00, purchase_count: 325
flores: period: 2017-12-01 00:00:00, purchase_count: 2
fraldas_higiene: period: 2017-12-01 00:00:00, purchase_count: 2
industria_comercio_e_negocios: period: 2017-12-01 00:00:00, purchase_count: 9
informatica_acessorios: period: 2017-12-01 00:00:00, purchase_count: 287
instrumentos_musicais: period: 2017-12-01 00:00:00, purchase_count: 42
livros_importados: period: 2017-12-01 00:00:00, purchase_count: 3
livros_interesse_geral: period: 2017-12-01 00:00:00, purchase_count: 42
livros_tecnicos: period: 2017-12-01 00:00:00, purchase_count: 4
malas_acessorios: period: 2017-12-01 00:00:00, purchase_count: 47
market_place: period: 2017-12-01 00:00:00, purchase_count: 14
moveis_colchao_e_estofado: period: 2017-12-01 00:00:00, purchase_count: 8
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2017-12-01 00:00:00, purchase_count: 20
moveis_decoracao: period: 2017-12-01 00:00:00, purchase_count: 390
moveis_escritorio: period: 2017-12-01 00:00:00, purchase_count: 49
moveis_quarto: period: 2017-12-01 00:00:00, purchase_count: 1
moveis_sala: period: 2017-12-01 00:00:00, purchase_count: 20
papelaria: period: 2017-12-01 00:00:00, purchase_count: 251
pcs: period: 2017-12-01 00:00:00, purchase_count: 23
perfumaria: period: 2017-12-01 00:00:00, purchase_count: 241
pet_shop: period: 2017-12-01 00:00:00, purchase_count: 74
relogios_presentes: period: 2017-12-01 00:00:00, purchase_count: 367
sinalizacao_e_seguranca: period: 2017-12-01 00:00:00, purchase_count: 2
tablets_impressao_imagem: period: 2017-12-01 00:00:00, purchase_count: 6
telefonia: period: 2017-12-01 00:00:00, purchase_count: 267
telefonia_fixa: period: 2017-12-01 00:00:00, purchase_count: 5
utilidades_domesticas: period: 2017-12-01 00:00:00, purchase_count: 295
agro_industria_e_comercio: period: 2018-01-01 00:00:00, purchase_count: 18
alimentos: period: 2018-01-01 00:00:00, purchase_count: 20
alimentos_bebidas: period: 2018-01-01 00:00:00, purchase_count: 11
artes: period: 2018-01-01 00:00:00, purchase_count: 19
artigos_de_festas: period: 2018-01-01 00:00:00, purchase_count: 2
artigos_de_natal: period: 2018-01-01 00:00:00, purchase_count: 10
audio: period: 2018-01-01 00:00:00, purchase_count: 26
automotivo: period: 2018-01-01 00:00:00, purchase_count: 268
bebes: period: 2018-01-01 00:00:00, purchase_count: 223
bebidas: period: 2018-01-01 00:00:00, purchase_count: 52
beleza_saude: period: 2018-01-01 00:00:00, purchase_count: 628
brinquedos: period: 2018-01-01 00:00:00, purchase_count: 165
cama_mesa_banho: period: 2018-01-01 00:00:00, purchase_count: 848
casa_conforto: period: 2018-01-01 00:00:00, purchase_count: 18
casa_construcao: period: 2018-01-01 00:00:00, purchase_count: 42
cine_foto: period: 2018-01-01 00:00:00, purchase_count: 2
climatizacao: period: 2018-01-01 00:00:00, purchase_count: 29
consoles_games: period: 2018-01-01 00:00:00, purchase_count: 54
construcao_ferramentas_construcao: period: 2018-01-01 00:00:00, purchase_count: 48
construcao_ferramentas_ferramentas: period: 2018-01-01 00:00:00, purchase_count: 8
construcao_ferramentas_iluminacao: period: 2018-01-01 00:00:00, purchase_count: 7
construcao_ferramentas_jardim: period: 2018-01-01 00:00:00, purchase_count: 24
construcao_ferramentas_seguranca: period: 2018-01-01 00:00:00, purchase_count: 11
cool_stuff: period: 2018-01-01 00:00:00, purchase_count: 300
dvds_blu_ray: period: 2018-01-01 00:00:00, purchase_count: 2
eletrodomesticos: period: 2018-01-01 00:00:00, purchase_count: 28
eletrodomesticos_2: period: 2018-01-01 00:00:00, purchase_count: 13
eletronicos: period: 2018-01-01 00:00:00, purchase_count: 351
eletroportateis: period: 2018-01-01 00:00:00, purchase_count: 55
esporte_lazer: period: 2018-01-01 00:00:00, purchase_count: 654
fashion_bolsas_e_acessorios: period: 2018-01-01 00:00:00, purchase_count: 125
fashion_calcados: period: 2018-01-01 00:00:00, purchase_count: 9
fashion_esporte: period: 2018-01-01 00:00:00, purchase_count: 2
fashion_roupa_feminina: period: 2018-01-01 00:00:00, purchase_count: 3
fashion_roupa_masculina: period: 2018-01-01 00:00:00, purchase_count: 6
fashion_underwear_e_moda_praia: period: 2018-01-01 00:00:00, purchase_count: 8
ferramentas_jardim: period: 2018-01-01 00:00:00, purchase_count: 240
flores: period: 2018-01-01 00:00:00, purchase_count: 10
fraldas_higiene: period: 2018-01-01 00:00:00, purchase_count: 5
industria_comercio_e_negocios: period: 2018-01-01 00:00:00, purchase_count: 19
informatica_acessorios: period: 2018-01-01 00:00:00, purchase_count: 707
instrumentos_musicais: period: 2018-01-01 00:00:00, purchase_count: 53
la_cuisine: period: 2018-01-01 00:00:00, purchase_count: 1
livros_importados: period: 2018-01-01 00:00:00, purchase_count: 6
livros_interesse_geral: period: 2018-01-01 00:00:00, purchase_count: 45
livros_tecnicos: period: 2018-01-01 00:00:00, purchase_count: 17
malas_acessorios: period: 2018-01-01 00:00:00, purchase_count: 128
market_place: period: 2018-01-01 00:00:00, purchase_count: 14
moveis_colchao_e_estofado: period: 2018-01-01 00:00:00, purchase_count: 9
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2018-01-01 00:00:00, purchase_count: 21
moveis_decoracao: period: 2018-01-01 00:00:00, purchase_count: 612
moveis_escritorio: period: 2018-01-01 00:00:00, purchase_count: 145
moveis_quarto: period: 2018-01-01 00:00:00, purchase_count: 5
moveis_sala: period: 2018-01-01 00:00:00, purchase_count: 22
musica: period: 2018-01-01 00:00:00, purchase_count: 1
papelaria: period: 2018-01-01 00:00:00, purchase_count: 397
pcs: period: 2018-01-01 00:00:00, purchase_count: 12
perfumaria: period: 2018-01-01 00:00:00, purchase_count: 229
pet_shop: period: 2018-01-01 00:00:00, purchase_count: 90
portateis_casa_forno_e_cafe: period: 2018-01-01 00:00:00, purchase_count: 1
relogios_presentes: period: 2018-01-01 00:00:00, purchase_count: 370
sinalizacao_e_seguranca: period: 2018-01-01 00:00:00, purchase_count: 8
tablets_impressao_imagem: period: 2018-01-01 00:00:00, purchase_count: 3
telefonia: period: 2018-01-01 00:00:00, purchase_count: 372
telefonia_fixa: period: 2018-01-01 00:00:00, purchase_count: 10
utilidades_domesticas: period: 2018-01-01 00:00:00, purchase_count: 359
agro_industria_e_comercio: period: 2018-02-01 00:00:00, purchase_count: 27
alimentos: period: 2018-02-01 00:00:00, purchase_count: 39
alimentos_bebidas: period: 2018-02-01 00:00:00, purchase_count: 24
artes: period: 2018-02-01 00:00:00, purchase_count: 13
artigos_de_natal: period: 2018-02-01 00:00:00, purchase_count: 24
audio: period: 2018-02-01 00:00:00, purchase_count: 15
automotivo: period: 2018-02-01 00:00:00, purchase_count: 319
bebes: period: 2018-02-01 00:00:00, purchase_count: 176
bebidas: period: 2018-02-01 00:00:00, purchase_count: 32
beleza_saude: period: 2018-02-01 00:00:00, purchase_count: 668
brinquedos: period: 2018-02-01 00:00:00, purchase_count: 146
cama_mesa_banho: period: 2018-02-01 00:00:00, purchase_count: 690
casa_conforto: period: 2018-02-01 00:00:00, purchase_count: 21
casa_conforto_2: period: 2018-02-01 00:00:00, purchase_count: 3
casa_construcao: period: 2018-02-01 00:00:00, purchase_count: 39
cine_foto: period: 2018-02-01 00:00:00, purchase_count: 2
climatizacao: period: 2018-02-01 00:00:00, purchase_count: 12
consoles_games: period: 2018-02-01 00:00:00, purchase_count: 52
construcao_ferramentas_construcao: period: 2018-02-01 00:00:00, purchase_count: 69
construcao_ferramentas_ferramentas: period: 2018-02-01 00:00:00, purchase_count: 12
construcao_ferramentas_iluminacao: period: 2018-02-01 00:00:00, purchase_count: 17
construcao_ferramentas_jardim: period: 2018-02-01 00:00:00, purchase_count: 20
construcao_ferramentas_seguranca: period: 2018-02-01 00:00:00, purchase_count: 8
cool_stuff: period: 2018-02-01 00:00:00, purchase_count: 187
dvds_blu_ray: period: 2018-02-01 00:00:00, purchase_count: 1
eletrodomesticos: period: 2018-02-01 00:00:00, purchase_count: 49
eletrodomesticos_2: period: 2018-02-01 00:00:00, purchase_count: 21
eletronicos: period: 2018-02-01 00:00:00, purchase_count: 332
eletroportateis: period: 2018-02-01 00:00:00, purchase_count: 32
esporte_lazer: period: 2018-02-01 00:00:00, purchase_count: 651
fashion_bolsas_e_acessorios: period: 2018-02-01 00:00:00, purchase_count: 107
fashion_calcados: period: 2018-02-01 00:00:00, purchase_count: 11
fashion_roupa_feminina: period: 2018-02-01 00:00:00, purchase_count: 1
fashion_roupa_masculina: period: 2018-02-01 00:00:00, purchase_count: 3
fashion_underwear_e_moda_praia: period: 2018-02-01 00:00:00, purchase_count: 7
ferramentas_jardim: period: 2018-02-01 00:00:00, purchase_count: 296
flores: period: 2018-02-01 00:00:00, purchase_count: 4
fraldas_higiene: period: 2018-02-01 00:00:00, purchase_count: 4
industria_comercio_e_negocios: period: 2018-02-01 00:00:00, purchase_count: 37
informatica_acessorios: period: 2018-02-01 00:00:00, purchase_count: 981
instrumentos_musicais: period: 2018-02-01 00:00:00, purchase_count: 44
livros_importados: period: 2018-02-01 00:00:00, purchase_count: 3
livros_interesse_geral: period: 2018-02-01 00:00:00, purchase_count: 29
livros_tecnicos: period: 2018-02-01 00:00:00, purchase_count: 26
malas_acessorios: period: 2018-02-01 00:00:00, purchase_count: 47
market_place: period: 2018-02-01 00:00:00, purchase_count: 28
moveis_colchao_e_estofado: period: 2018-02-01 00:00:00, purchase_count: 6
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2018-02-01 00:00:00, purchase_count: 20
moveis_decoracao: period: 2018-02-01 00:00:00, purchase_count: 434
moveis_escritorio: period: 2018-02-01 00:00:00, purchase_count: 109
moveis_quarto: period: 2018-02-01 00:00:00, purchase_count: 8
moveis_sala: period: 2018-02-01 00:00:00, purchase_count: 26
musica: period: 2018-02-01 00:00:00, purchase_count: 2
papelaria: period: 2018-02-01 00:00:00, purchase_count: 159
pc_gamer: period: 2018-02-01 00:00:00, purchase_count: 1
perfumaria: period: 2018-02-01 00:00:00, purchase_count: 215
pet_shop: period: 2018-02-01 00:00:00, purchase_count: 102
portateis_casa_forno_e_cafe: period: 2018-02-01 00:00:00, purchase_count: 5
relogios_presentes: period: 2018-02-01 00:00:00, purchase_count: 337
sinalizacao_e_seguranca: period: 2018-02-01 00:00:00, purchase_count: 15
tablets_impressao_imagem: period: 2018-02-01 00:00:00, purchase_count: 13
telefonia: period: 2018-02-01 00:00:00, purchase_count: 359
telefonia_fixa: period: 2018-02-01 00:00:00, purchase_count: 12
utilidades_domesticas: period: 2018-02-01 00:00:00, purchase_count: 400
agro_industria_e_comercio: period: 2018-03-01 00:00:00, purchase_count: 28
alimentos: period: 2018-03-01 00:00:00, purchase_count: 35
alimentos_bebidas: period: 2018-03-01 00:00:00, purchase_count: 19
artes: period: 2018-03-01 00:00:00, purchase_count: 7
artigos_de_festas: period: 2018-03-01 00:00:00, purchase_count: 6
artigos_de_natal: period: 2018-03-01 00:00:00, purchase_count: 12
audio: period: 2018-03-01 00:00:00, purchase_count: 34
automotivo: period: 2018-03-01 00:00:00, purchase_count: 344
bebes: period: 2018-03-01 00:00:00, purchase_count: 224
bebidas: period: 2018-03-01 00:00:00, purchase_count: 21
beleza_saude: period: 2018-03-01 00:00:00, purchase_count: 673
brinquedos: period: 2018-03-01 00:00:00, purchase_count: 234
cama_mesa_banho: period: 2018-03-01 00:00:00, purchase_count: 798
casa_conforto: period: 2018-03-01 00:00:00, purchase_count: 21
casa_conforto_2: period: 2018-03-01 00:00:00, purchase_count: 1
casa_construcao: period: 2018-03-01 00:00:00, purchase_count: 44
cine_foto: period: 2018-03-01 00:00:00, purchase_count: 7
climatizacao: period: 2018-03-01 00:00:00, purchase_count: 25
consoles_games: period: 2018-03-01 00:00:00, purchase_count: 58
construcao_ferramentas_construcao: period: 2018-03-01 00:00:00, purchase_count: 71
construcao_ferramentas_ferramentas: period: 2018-03-01 00:00:00, purchase_count: 9
construcao_ferramentas_iluminacao: period: 2018-03-01 00:00:00, purchase_count: 13
construcao_ferramentas_jardim: period: 2018-03-01 00:00:00, purchase_count: 23
construcao_ferramentas_seguranca: period: 2018-03-01 00:00:00, purchase_count: 22
cool_stuff: period: 2018-03-01 00:00:00, purchase_count: 256
dvds_blu_ray: period: 2018-03-01 00:00:00, purchase_count: 2
eletrodomesticos: period: 2018-03-01 00:00:00, purchase_count: 70
eletrodomesticos_2: period: 2018-03-01 00:00:00, purchase_count: 12
eletronicos: period: 2018-03-01 00:00:00, purchase_count: 261
eletroportateis: period: 2018-03-01 00:00:00, purchase_count: 37
esporte_lazer: period: 2018-03-01 00:00:00, purchase_count: 761
fashion_bolsas_e_acessorios: period: 2018-03-01 00:00:00, purchase_count: 139
fashion_calcados: period: 2018-03-01 00:00:00, purchase_count: 12
fashion_esporte: period: 2018-03-01 00:00:00, purchase_count: 1
fashion_roupa_feminina: period: 2018-03-01 00:00:00, purchase_count: 4
fashion_roupa_infanto_juvenil: period: 2018-03-01 00:00:00, purchase_count: 2
fashion_underwear_e_moda_praia: period: 2018-03-01 00:00:00, purchase_count: 5
ferramentas_jardim: period: 2018-03-01 00:00:00, purchase_count: 262
flores: period: 2018-03-01 00:00:00, purchase_count: 3
fraldas_higiene: period: 2018-03-01 00:00:00, purchase_count: 6
industria_comercio_e_negocios: period: 2018-03-01 00:00:00, purchase_count: 29
informatica_acessorios: period: 2018-03-01 00:00:00, purchase_count: 758
instrumentos_musicais: period: 2018-03-01 00:00:00, purchase_count: 55
la_cuisine: period: 2018-03-01 00:00:00, purchase_count: 1
livros_importados: period: 2018-03-01 00:00:00, purchase_count: 3
livros_interesse_geral: period: 2018-03-01 00:00:00, purchase_count: 39
livros_tecnicos: period: 2018-03-01 00:00:00, purchase_count: 17
malas_acessorios: period: 2018-03-01 00:00:00, purchase_count: 57
market_place: period: 2018-03-01 00:00:00, purchase_count: 17
moveis_colchao_e_estofado: period: 2018-03-01 00:00:00, purchase_count: 4
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2018-03-01 00:00:00, purchase_count: 12
moveis_decoracao: period: 2018-03-01 00:00:00, purchase_count: 595
moveis_escritorio: period: 2018-03-01 00:00:00, purchase_count: 202
moveis_quarto: period: 2018-03-01 00:00:00, purchase_count: 6
moveis_sala: period: 2018-03-01 00:00:00, purchase_count: 19
musica: period: 2018-03-01 00:00:00, purchase_count: 2
papelaria: period: 2018-03-01 00:00:00, purchase_count: 164
perfumaria: period: 2018-03-01 00:00:00, purchase_count: 202
pet_shop: period: 2018-03-01 00:00:00, purchase_count: 124
portateis_casa_forno_e_cafe: period: 2018-03-01 00:00:00, purchase_count: 7
relogios_presentes: period: 2018-03-01 00:00:00, purchase_count: 430
sinalizacao_e_seguranca: period: 2018-03-01 00:00:00, purchase_count: 9
tablets_impressao_imagem: period: 2018-03-01 00:00:00, purchase_count: 3
telefonia: period: 2018-03-01 00:00:00, purchase_count: 344
telefonia_fixa: period: 2018-03-01 00:00:00, purchase_count: 14
utilidades_domesticas: period: 2018-03-01 00:00:00, purchase_count: 407
agro_industria_e_comercio: period: 2018-04-01 00:00:00, purchase_count: 12
alimentos: period: 2018-04-01 00:00:00, purchase_count: 40
alimentos_bebidas: period: 2018-04-01 00:00:00, purchase_count: 18
artes: period: 2018-04-01 00:00:00, purchase_count: 26
artes_e_artesanato: period: 2018-04-01 00:00:00, purchase_count: 1
artigos_de_festas: period: 2018-04-01 00:00:00, purchase_count: 2
artigos_de_natal: period: 2018-04-01 00:00:00, purchase_count: 12
audio: period: 2018-04-01 00:00:00, purchase_count: 31
automotivo: period: 2018-04-01 00:00:00, purchase_count: 356
bebes: period: 2018-04-01 00:00:00, purchase_count: 244
bebidas: period: 2018-04-01 00:00:00, purchase_count: 54
beleza_saude: period: 2018-04-01 00:00:00, purchase_count: 694
brinquedos: period: 2018-04-01 00:00:00, purchase_count: 205
cama_mesa_banho: period: 2018-04-01 00:00:00, purchase_count: 746
casa_conforto: period: 2018-04-01 00:00:00, purchase_count: 18
casa_conforto_2: period: 2018-04-01 00:00:00, purchase_count: 1
casa_construcao: period: 2018-04-01 00:00:00, purchase_count: 76
cds_dvds_musicais: period: 2018-04-01 00:00:00, purchase_count: 1
cine_foto: period: 2018-04-01 00:00:00, purchase_count: 5
climatizacao: period: 2018-04-01 00:00:00, purchase_count: 23
consoles_games: period: 2018-04-01 00:00:00, purchase_count: 48
construcao_ferramentas_construcao: period: 2018-04-01 00:00:00, purchase_count: 92
construcao_ferramentas_ferramentas: period: 2018-04-01 00:00:00, purchase_count: 17
construcao_ferramentas_iluminacao: period: 2018-04-01 00:00:00, purchase_count: 47
construcao_ferramentas_jardim: period: 2018-04-01 00:00:00, purchase_count: 18
construcao_ferramentas_seguranca: period: 2018-04-01 00:00:00, purchase_count: 24
cool_stuff: period: 2018-04-01 00:00:00, purchase_count: 207
dvds_blu_ray: period: 2018-04-01 00:00:00, purchase_count: 5
eletrodomesticos: period: 2018-04-01 00:00:00, purchase_count: 106
eletrodomesticos_2: period: 2018-04-01 00:00:00, purchase_count: 23
eletronicos: period: 2018-04-01 00:00:00, purchase_count: 214
eletroportateis: period: 2018-04-01 00:00:00, purchase_count: 67
esporte_lazer: period: 2018-04-01 00:00:00, purchase_count: 600
fashion_bolsas_e_acessorios: period: 2018-04-01 00:00:00, purchase_count: 107
fashion_calcados: period: 2018-04-01 00:00:00, purchase_count: 11
fashion_esporte: period: 2018-04-01 00:00:00, purchase_count: 1
fashion_roupa_feminina: period: 2018-04-01 00:00:00, purchase_count: 5
fashion_roupa_masculina: period: 2018-04-01 00:00:00, purchase_count: 1
fashion_underwear_e_moda_praia: period: 2018-04-01 00:00:00, purchase_count: 6
ferramentas_jardim: period: 2018-04-01 00:00:00, purchase_count: 288
flores: period: 2018-04-01 00:00:00, purchase_count: 3
fraldas_higiene: period: 2018-04-01 00:00:00, purchase_count: 4
industria_comercio_e_negocios: period: 2018-04-01 00:00:00, purchase_count: 53
informatica_acessorios: period: 2018-04-01 00:00:00, purchase_count: 544
instrumentos_musicais: period: 2018-04-01 00:00:00, purchase_count: 60
la_cuisine: period: 2018-04-01 00:00:00, purchase_count: 2
livros_importados: period: 2018-04-01 00:00:00, purchase_count: 4
livros_interesse_geral: period: 2018-04-01 00:00:00, purchase_count: 50
livros_tecnicos: period: 2018-04-01 00:00:00, purchase_count: 23
malas_acessorios: period: 2018-04-01 00:00:00, purchase_count: 57
market_place: period: 2018-04-01 00:00:00, purchase_count: 15
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2018-04-01 00:00:00, purchase_count: 20
moveis_decoracao: period: 2018-04-01 00:00:00, purchase_count: 594
moveis_escritorio: period: 2018-04-01 00:00:00, purchase_count: 133
moveis_quarto: period: 2018-04-01 00:00:00, purchase_count: 8
moveis_sala: period: 2018-04-01 00:00:00, purchase_count: 34
musica: period: 2018-04-01 00:00:00, purchase_count: 5
papelaria: period: 2018-04-01 00:00:00, purchase_count: 155
pcs: period: 2018-04-01 00:00:00, purchase_count: 15
perfumaria: period: 2018-04-01 00:00:00, purchase_count: 175
pet_shop: period: 2018-04-01 00:00:00, purchase_count: 170
portateis_casa_forno_e_cafe: period: 2018-04-01 00:00:00, purchase_count: 15
relogios_presentes: period: 2018-04-01 00:00:00, purchase_count: 505
sinalizacao_e_seguranca: period: 2018-04-01 00:00:00, purchase_count: 36
tablets_impressao_imagem: period: 2018-04-01 00:00:00, purchase_count: 1
telefonia: period: 2018-04-01 00:00:00, purchase_count: 284
telefonia_fixa: period: 2018-04-01 00:00:00, purchase_count: 11
utilidades_domesticas: period: 2018-04-01 00:00:00, purchase_count: 471
agro_industria_e_comercio: period: 2018-05-01 00:00:00, purchase_count: 8
alimentos: period: 2018-05-01 00:00:00, purchase_count: 44
alimentos_bebidas: period: 2018-05-01 00:00:00, purchase_count: 25
artes: period: 2018-05-01 00:00:00, purchase_count: 36
artes_e_artesanato: period: 2018-05-01 00:00:00, purchase_count: 1
artigos_de_festas: period: 2018-05-01 00:00:00, purchase_count: 4
artigos_de_natal: period: 2018-05-01 00:00:00, purchase_count: 6
audio: period: 2018-05-01 00:00:00, purchase_count: 21
automotivo: period: 2018-05-01 00:00:00, purchase_count: 311
bebes: period: 2018-05-01 00:00:00, purchase_count: 245
bebidas: period: 2018-05-01 00:00:00, purchase_count: 48
beleza_saude: period: 2018-05-01 00:00:00, purchase_count: 770
brinquedos: period: 2018-05-01 00:00:00, purchase_count: 221
cama_mesa_banho: period: 2018-05-01 00:00:00, purchase_count: 747
casa_conforto: period: 2018-05-01 00:00:00, purchase_count: 22
casa_construcao: period: 2018-05-01 00:00:00, purchase_count: 79
cine_foto: period: 2018-05-01 00:00:00, purchase_count: 18
climatizacao: period: 2018-05-01 00:00:00, purchase_count: 15
consoles_games: period: 2018-05-01 00:00:00, purchase_count: 54
construcao_ferramentas_construcao: period: 2018-05-01 00:00:00, purchase_count: 125
construcao_ferramentas_ferramentas: period: 2018-05-01 00:00:00, purchase_count: 5
construcao_ferramentas_iluminacao: period: 2018-05-01 00:00:00, purchase_count: 41
construcao_ferramentas_jardim: period: 2018-05-01 00:00:00, purchase_count: 16
construcao_ferramentas_seguranca: period: 2018-05-01 00:00:00, purchase_count: 29
cool_stuff: period: 2018-05-01 00:00:00, purchase_count: 176
dvds_blu_ray: period: 2018-05-01 00:00:00, purchase_count: 7
eletrodomesticos: period: 2018-05-01 00:00:00, purchase_count: 64
eletrodomesticos_2: period: 2018-05-01 00:00:00, purchase_count: 23
eletronicos: period: 2018-05-01 00:00:00, purchase_count: 235
eletroportateis: period: 2018-05-01 00:00:00, purchase_count: 48
esporte_lazer: period: 2018-05-01 00:00:00, purchase_count: 492
fashion_bolsas_e_acessorios: period: 2018-05-01 00:00:00, purchase_count: 111
fashion_calcados: period: 2018-05-01 00:00:00, purchase_count: 10
fashion_roupa_masculina: period: 2018-05-01 00:00:00, purchase_count: 1
fashion_underwear_e_moda_praia: period: 2018-05-01 00:00:00, purchase_count: 6
ferramentas_jardim: period: 2018-05-01 00:00:00, purchase_count: 291
flores: period: 2018-05-01 00:00:00, purchase_count: 1
fraldas_higiene: period: 2018-05-01 00:00:00, purchase_count: 3
industria_comercio_e_negocios: period: 2018-05-01 00:00:00, purchase_count: 41
informatica_acessorios: period: 2018-05-01 00:00:00, purchase_count: 464
instrumentos_musicais: period: 2018-05-01 00:00:00, purchase_count: 61
livros_importados: period: 2018-05-01 00:00:00, purchase_count: 10
livros_interesse_geral: period: 2018-05-01 00:00:00, purchase_count: 53
livros_tecnicos: period: 2018-05-01 00:00:00, purchase_count: 56
malas_acessorios: period: 2018-05-01 00:00:00, purchase_count: 49
market_place: period: 2018-05-01 00:00:00, purchase_count: 14
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2018-05-01 00:00:00, purchase_count: 13
moveis_decoracao: period: 2018-05-01 00:00:00, purchase_count: 605
moveis_escritorio: period: 2018-05-01 00:00:00, purchase_count: 105
moveis_quarto: period: 2018-05-01 00:00:00, purchase_count: 6
moveis_sala: period: 2018-05-01 00:00:00, purchase_count: 16
musica: period: 2018-05-01 00:00:00, purchase_count: 5
papelaria: period: 2018-05-01 00:00:00, purchase_count: 130
pcs: period: 2018-05-01 00:00:00, purchase_count: 14
perfumaria: period: 2018-05-01 00:00:00, purchase_count: 198
pet_shop: period: 2018-05-01 00:00:00, purchase_count: 136
portateis_casa_forno_e_cafe: period: 2018-05-01 00:00:00, purchase_count: 9
portateis_cozinha_e_preparadores_de_alimentos: period: 2018-05-01 00:00:00, purchase_count: 2
relogios_presentes: period: 2018-05-01 00:00:00, purchase_count: 636
sinalizacao_e_seguranca: period: 2018-05-01 00:00:00, purchase_count: 7
tablets_impressao_imagem: period: 2018-05-01 00:00:00, purchase_count: 1
telefonia: period: 2018-05-01 00:00:00, purchase_count: 256
telefonia_fixa: period: 2018-05-01 00:00:00, purchase_count: 17
utilidades_domesticas: period: 2018-05-01 00:00:00, purchase_count: 619
agro_industria_e_comercio: period: 2018-06-01 00:00:00, purchase_count: 10
alimentos: period: 2018-06-01 00:00:00, purchase_count: 24
alimentos_bebidas: period: 2018-06-01 00:00:00, purchase_count: 11
artes: period: 2018-06-01 00:00:00, purchase_count: 28
artigos_de_festas: period: 2018-06-01 00:00:00, purchase_count: 2
artigos_de_natal: period: 2018-06-01 00:00:00, purchase_count: 7
audio: period: 2018-06-01 00:00:00, purchase_count: 20
automotivo: period: 2018-06-01 00:00:00, purchase_count: 300
bebes: period: 2018-06-01 00:00:00, purchase_count: 225
bebidas: period: 2018-06-01 00:00:00, purchase_count: 33
beleza_saude: period: 2018-06-01 00:00:00, purchase_count: 885
brinquedos: period: 2018-06-01 00:00:00, purchase_count: 191
cama_mesa_banho: period: 2018-06-01 00:00:00, purchase_count: 773
casa_conforto: period: 2018-06-01 00:00:00, purchase_count: 16
casa_conforto_2: period: 2018-06-01 00:00:00, purchase_count: 2
casa_construcao: period: 2018-06-01 00:00:00, purchase_count: 71
cine_foto: period: 2018-06-01 00:00:00, purchase_count: 13
climatizacao: period: 2018-06-01 00:00:00, purchase_count: 15
consoles_games: period: 2018-06-01 00:00:00, purchase_count: 43
construcao_ferramentas_construcao: period: 2018-06-01 00:00:00, purchase_count: 113
construcao_ferramentas_ferramentas: period: 2018-06-01 00:00:00, purchase_count: 4
construcao_ferramentas_iluminacao: period: 2018-06-01 00:00:00, purchase_count: 44
construcao_ferramentas_jardim: period: 2018-06-01 00:00:00, purchase_count: 11
construcao_ferramentas_seguranca: period: 2018-06-01 00:00:00, purchase_count: 16
cool_stuff: period: 2018-06-01 00:00:00, purchase_count: 103
dvds_blu_ray: period: 2018-06-01 00:00:00, purchase_count: 6
eletrodomesticos: period: 2018-06-01 00:00:00, purchase_count: 67
eletrodomesticos_2: period: 2018-06-01 00:00:00, purchase_count: 19
eletronicos: period: 2018-06-01 00:00:00, purchase_count: 191
eletroportateis: period: 2018-06-01 00:00:00, purchase_count: 50
esporte_lazer: period: 2018-06-01 00:00:00, purchase_count: 426
fashion_bolsas_e_acessorios: period: 2018-06-01 00:00:00, purchase_count: 87
fashion_calcados: period: 2018-06-01 00:00:00, purchase_count: 10
fashion_roupa_infanto_juvenil: period: 2018-06-01 00:00:00, purchase_count: 1
fashion_roupa_masculina: period: 2018-06-01 00:00:00, purchase_count: 7
fashion_underwear_e_moda_praia: period: 2018-06-01 00:00:00, purchase_count: 7
ferramentas_jardim: period: 2018-06-01 00:00:00, purchase_count: 185
flores: period: 2018-06-01 00:00:00, purchase_count: 2
fraldas_higiene: period: 2018-06-01 00:00:00, purchase_count: 7
industria_comercio_e_negocios: period: 2018-06-01 00:00:00, purchase_count: 26
informatica_acessorios: period: 2018-06-01 00:00:00, purchase_count: 408
instrumentos_musicais: period: 2018-06-01 00:00:00, purchase_count: 47
livros_importados: period: 2018-06-01 00:00:00, purchase_count: 9
livros_interesse_geral: period: 2018-06-01 00:00:00, purchase_count: 39
livros_tecnicos: period: 2018-06-01 00:00:00, purchase_count: 26
malas_acessorios: period: 2018-06-01 00:00:00, purchase_count: 36
market_place: period: 2018-06-01 00:00:00, purchase_count: 7
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2018-06-01 00:00:00, purchase_count: 30
moveis_decoracao: period: 2018-06-01 00:00:00, purchase_count: 405
moveis_escritorio: period: 2018-06-01 00:00:00, purchase_count: 77
moveis_quarto: period: 2018-06-01 00:00:00, purchase_count: 9
moveis_sala: period: 2018-06-01 00:00:00, purchase_count: 29
musica: period: 2018-06-01 00:00:00, purchase_count: 3
papelaria: period: 2018-06-01 00:00:00, purchase_count: 167
pcs: period: 2018-06-01 00:00:00, purchase_count: 13
perfumaria: period: 2018-06-01 00:00:00, purchase_count: 189
pet_shop: period: 2018-06-01 00:00:00, purchase_count: 178
portateis_casa_forno_e_cafe: period: 2018-06-01 00:00:00, purchase_count: 3
relogios_presentes: period: 2018-06-01 00:00:00, purchase_count: 481
sinalizacao_e_seguranca: period: 2018-06-01 00:00:00, purchase_count: 27
tablets_impressao_imagem: period: 2018-06-01 00:00:00, purchase_count: 1
telefonia: period: 2018-06-01 00:00:00, purchase_count: 219
telefonia_fixa: period: 2018-06-01 00:00:00, purchase_count: 17
utilidades_domesticas: period: 2018-06-01 00:00:00, purchase_count: 584
agro_industria_e_comercio: period: 2018-07-01 00:00:00, purchase_count: 30
alimentos: period: 2018-07-01 00:00:00, purchase_count: 64
alimentos_bebidas: period: 2018-07-01 00:00:00, purchase_count: 18
artes: period: 2018-07-01 00:00:00, purchase_count: 21
artes_e_artesanato: period: 2018-07-01 00:00:00, purchase_count: 11
artigos_de_festas: period: 2018-07-01 00:00:00, purchase_count: 2
artigos_de_natal: period: 2018-07-01 00:00:00, purchase_count: 8
audio: period: 2018-07-01 00:00:00, purchase_count: 22
automotivo: period: 2018-07-01 00:00:00, purchase_count: 344
bebes: period: 2018-07-01 00:00:00, purchase_count: 222
bebidas: period: 2018-07-01 00:00:00, purchase_count: 17
beleza_saude: period: 2018-07-01 00:00:00, purchase_count: 784
brinquedos: period: 2018-07-01 00:00:00, purchase_count: 156
cama_mesa_banho: period: 2018-07-01 00:00:00, purchase_count: 624
casa_conforto: period: 2018-07-01 00:00:00, purchase_count: 24
casa_conforto_2: period: 2018-07-01 00:00:00, purchase_count: 3
casa_construcao: period: 2018-07-01 00:00:00, purchase_count: 61
cine_foto: period: 2018-07-01 00:00:00, purchase_count: 7
climatizacao: period: 2018-07-01 00:00:00, purchase_count: 17
consoles_games: period: 2018-07-01 00:00:00, purchase_count: 49
construcao_ferramentas_construcao: period: 2018-07-01 00:00:00, purchase_count: 115
construcao_ferramentas_ferramentas: period: 2018-07-01 00:00:00, purchase_count: 12
construcao_ferramentas_iluminacao: period: 2018-07-01 00:00:00, purchase_count: 55
construcao_ferramentas_jardim: period: 2018-07-01 00:00:00, purchase_count: 25
construcao_ferramentas_seguranca: period: 2018-07-01 00:00:00, purchase_count: 15
cool_stuff: period: 2018-07-01 00:00:00, purchase_count: 121
dvds_blu_ray: period: 2018-07-01 00:00:00, purchase_count: 1
eletrodomesticos: period: 2018-07-01 00:00:00, purchase_count: 79
eletrodomesticos_2: period: 2018-07-01 00:00:00, purchase_count: 23
eletronicos: period: 2018-07-01 00:00:00, purchase_count: 159
eletroportateis: period: 2018-07-01 00:00:00, purchase_count: 43
esporte_lazer: period: 2018-07-01 00:00:00, purchase_count: 468
fashion_bolsas_e_acessorios: period: 2018-07-01 00:00:00, purchase_count: 77
fashion_calcados: period: 2018-07-01 00:00:00, purchase_count: 5
fashion_roupa_masculina: period: 2018-07-01 00:00:00, purchase_count: 5
fashion_underwear_e_moda_praia: period: 2018-07-01 00:00:00, purchase_count: 2
ferramentas_jardim: period: 2018-07-01 00:00:00, purchase_count: 179
flores: period: 2018-07-01 00:00:00, purchase_count: 2
fraldas_higiene: period: 2018-07-01 00:00:00, purchase_count: 4
industria_comercio_e_negocios: period: 2018-07-01 00:00:00, purchase_count: 14
informatica_acessorios: period: 2018-07-01 00:00:00, purchase_count: 427
instrumentos_musicais: period: 2018-07-01 00:00:00, purchase_count: 37
livros_importados: period: 2018-07-01 00:00:00, purchase_count: 8
livros_interesse_geral: period: 2018-07-01 00:00:00, purchase_count: 25
livros_tecnicos: period: 2018-07-01 00:00:00, purchase_count: 28
malas_acessorios: period: 2018-07-01 00:00:00, purchase_count: 54
market_place: period: 2018-07-01 00:00:00, purchase_count: 4
moveis_colchao_e_estofado: period: 2018-07-01 00:00:00, purchase_count: 1
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2018-07-01 00:00:00, purchase_count: 23
moveis_decoracao: period: 2018-07-01 00:00:00, purchase_count: 440
moveis_escritorio: period: 2018-07-01 00:00:00, purchase_count: 82
moveis_quarto: period: 2018-07-01 00:00:00, purchase_count: 10
moveis_sala: period: 2018-07-01 00:00:00, purchase_count: 55
musica: period: 2018-07-01 00:00:00, purchase_count: 3
papelaria: period: 2018-07-01 00:00:00, purchase_count: 191
pc_gamer: period: 2018-07-01 00:00:00, purchase_count: 3
pcs: period: 2018-07-01 00:00:00, purchase_count: 8
perfumaria: period: 2018-07-01 00:00:00, purchase_count: 205
pet_shop: period: 2018-07-01 00:00:00, purchase_count: 160
portateis_casa_forno_e_cafe: period: 2018-07-01 00:00:00, purchase_count: 15
portateis_cozinha_e_preparadores_de_alimentos: period: 2018-07-01 00:00:00, purchase_count: 8
relogios_presentes: period: 2018-07-01 00:00:00, purchase_count: 528
sinalizacao_e_seguranca: period: 2018-07-01 00:00:00, purchase_count: 29
telefonia: period: 2018-07-01 00:00:00, purchase_count: 225
telefonia_fixa: period: 2018-07-01 00:00:00, purchase_count: 11
utilidades_domesticas: period: 2018-07-01 00:00:00, purchase_count: 577
agro_industria_e_comercio: period: 2018-08-01 00:00:00, purchase_count: 18
alimentos: period: 2018-08-01 00:00:00, purchase_count: 116
alimentos_bebidas: period: 2018-08-01 00:00:00, purchase_count: 21
artes: period: 2018-08-01 00:00:00, purchase_count: 18
artes_e_artesanato: period: 2018-08-01 00:00:00, purchase_count: 9
artigos_de_festas: period: 2018-08-01 00:00:00, purchase_count: 14
artigos_de_natal: period: 2018-08-01 00:00:00, purchase_count: 11
audio: period: 2018-08-01 00:00:00, purchase_count: 26
automotivo: period: 2018-08-01 00:00:00, purchase_count: 377
bebes: period: 2018-08-01 00:00:00, purchase_count: 217
bebidas: period: 2018-08-01 00:00:00, purchase_count: 30
beleza_saude: period: 2018-08-01 00:00:00, purchase_count: 849
brinquedos: period: 2018-08-01 00:00:00, purchase_count: 170
cama_mesa_banho: period: 2018-08-01 00:00:00, purchase_count: 658
casa_conforto: period: 2018-08-01 00:00:00, purchase_count: 16
casa_construcao: period: 2018-08-01 00:00:00, purchase_count: 49
cine_foto: period: 2018-08-01 00:00:00, purchase_count: 10
climatizacao: period: 2018-08-01 00:00:00, purchase_count: 21
consoles_games: period: 2018-08-01 00:00:00, purchase_count: 62
construcao_ferramentas_construcao: period: 2018-08-01 00:00:00, purchase_count: 162
construcao_ferramentas_ferramentas: period: 2018-08-01 00:00:00, purchase_count: 14
construcao_ferramentas_iluminacao: period: 2018-08-01 00:00:00, purchase_count: 62
construcao_ferramentas_jardim: period: 2018-08-01 00:00:00, purchase_count: 23
construcao_ferramentas_seguranca: period: 2018-08-01 00:00:00, purchase_count: 26
cool_stuff: period: 2018-08-01 00:00:00, purchase_count: 123
dvds_blu_ray: period: 2018-08-01 00:00:00, purchase_count: 1
eletrodomesticos: period: 2018-08-01 00:00:00, purchase_count: 65
eletrodomesticos_2: period: 2018-08-01 00:00:00, purchase_count: 15
eletronicos: period: 2018-08-01 00:00:00, purchase_count: 120
eletroportateis: period: 2018-08-01 00:00:00, purchase_count: 25
esporte_lazer: period: 2018-08-01 00:00:00, purchase_count: 475
fashion_bolsas_e_acessorios: period: 2018-08-01 00:00:00, purchase_count: 127
fashion_calcados: period: 2018-08-01 00:00:00, purchase_count: 3
fashion_esporte: period: 2018-08-01 00:00:00, purchase_count: 1
fashion_roupa_feminina: period: 2018-08-01 00:00:00, purchase_count: 3
fashion_roupa_masculina: period: 2018-08-01 00:00:00, purchase_count: 3
fashion_underwear_e_moda_praia: period: 2018-08-01 00:00:00, purchase_count: 2
ferramentas_jardim: period: 2018-08-01 00:00:00, purchase_count: 138
fraldas_higiene: period: 2018-08-01 00:00:00, purchase_count: 3
industria_comercio_e_negocios: period: 2018-08-01 00:00:00, purchase_count: 10
informatica_acessorios: period: 2018-08-01 00:00:00, purchase_count: 419
instrumentos_musicais: period: 2018-08-01 00:00:00, purchase_count: 41
livros_importados: period: 2018-08-01 00:00:00, purchase_count: 1
livros_interesse_geral: period: 2018-08-01 00:00:00, purchase_count: 36
livros_tecnicos: period: 2018-08-01 00:00:00, purchase_count: 29
malas_acessorios: period: 2018-08-01 00:00:00, purchase_count: 66
market_place: period: 2018-08-01 00:00:00, purchase_count: 8
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2018-08-01 00:00:00, purchase_count: 21
moveis_decoracao: period: 2018-08-01 00:00:00, purchase_count: 433
moveis_escritorio: period: 2018-08-01 00:00:00, purchase_count: 30
moveis_quarto: period: 2018-08-01 00:00:00, purchase_count: 12
moveis_sala: period: 2018-08-01 00:00:00, purchase_count: 40
musica: period: 2018-08-01 00:00:00, purchase_count: 6
papelaria: period: 2018-08-01 00:00:00, purchase_count: 170
pc_gamer: period: 2018-08-01 00:00:00, purchase_count: 1
pcs: period: 2018-08-01 00:00:00, purchase_count: 12
perfumaria: period: 2018-08-01 00:00:00, purchase_count: 223
pet_shop: period: 2018-08-01 00:00:00, purchase_count: 199
portateis_casa_forno_e_cafe: period: 2018-08-01 00:00:00, purchase_count: 17
portateis_cozinha_e_preparadores_de_alimentos: period: 2018-08-01 00:00:00, purchase_count: 5
relogios_presentes: period: 2018-08-01 00:00:00, purchase_count: 416
sinalizacao_e_seguranca: period: 2018-08-01 00:00:00, purchase_count: 22
telefonia: period: 2018-08-01 00:00:00, purchase_count: 277
telefonia_fixa: period: 2018-08-01 00:00:00, purchase_count: 10
utilidades_domesticas: period: 2018-08-01 00:00:00, purchase_count: 629
moveis_cozinha_area_de_servico_jantar_e_jardim: period: 2018-09-01 00:00:00, purchase_count: 1
```

#### 📊 Metadata

- **sql:** SELECT date_trunc('month', o.order_purchase_timestamp) AS period, p.product_category_name AS category, COUNT(*) AS purchase_count FROM analytics.orders o JOIN analytics.order_items oi ON o.order_id = oi.order_id JOIN analytics.products p ON oi.product_id = p.product_id GROUP BY period, category ORDER BY period, category
- **row_count:** 1283
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-7"></a>
### Query 7

#### 📝 Input

- **Query:** Qual é a distribuição de clientes por frequência de compra e como isso varia por estado?

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.85
- **Reason:** customer distribution by purchase frequency and state
- **Thread ID:** `1bcda9a5-5b6a-464f-b451-fbdb57d01e7b`

#### 💬 Response

```
Distribuição de clientes por estado e frequência de compra:
  SP: 41.746
  RJ: 12.852
  MG: 11.635
  RS: 5.466
  PR: 5.045
  SC: 3.637
  BA: 3.380
  DF: 2.140
  ES: 2.033
  GO: 2.020
  PE: 1.652
  CE: 1.336
  PA: 975
  MT: 907
  MA: 747
  MS: 715
  PB: 536
  PI: 495
  RN: 485
  AL: 413
  SE: 350
  TO: 280
  RO: 253
  AM: 148
  AC: 81
  AP: 68
  RR: 46

Total: 99.441 clientes em 27 estados.
```

#### 📊 Metadata

- **sql:** SELECT c.customer_state, COUNT(DISTINCT o.customer_id) AS customer_count, COUNT(o.order_id) AS purchase_frequency FROM analytics.customers c JOIN analytics.orders o ON c.customer_id = o.customer_id GROUP BY c.customer_state ORDER BY customer_count DESC
- **row_count:** 27
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-8"></a>
### Query 8

#### 📝 Input

- **Query:** Analise o comportamento de recompra: quantos clientes fizeram mais de 3 pedidos?

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.9
- **Reason:** count customers with more than 3 orders
- **Thread ID:** `0afb2218-6e63-4fad-8f0b-bfc6d2145b7b`

#### 💬 Response

```
Nenhum cliente fez mais de 3 pedidos. Isso pode indicar uma oportunidade para melhorar a fidelização e incentivar a recompra entre os clientes.
```

#### 📊 Metadata

- **sql:** SELECT COUNT(DISTINCT o.customer_id) AS customer_count FROM analytics.orders o GROUP BY o.customer_id HAVING COUNT(o.order_id) > 3
- **row_count:** 0
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-9"></a>
### Query 9

#### 📝 Input

- **Query:** Qual é o tempo médio entre aprovação do pagamento e entrega, por transportadora?

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.9
- **Reason:** average time difference grouped by carrier
- **Thread ID:** `7c8c31cb-cf3f-4e84-ab57-3e28c1cc6aa4`

#### 💬 Response

```
Análise do tempo médio entre aprovação do pagamento e entrega por transportadora:

0015a82c2db000af6aaaf3ae2ecb0532: 245,70 horas (média)
001cca7ae9ae17fb1caed9dfb1094831: 303,43 horas (média)
001e6ad469a905060d959994f1b41e4f: dados não disponíveis
002100f778ceb8431b7a1020ff7ab48f: 365,88 horas (média)
003554e2dce176b5555353e4f3555ac8: 111,21 horas (média)
004c9cd9d87a3c30c522c48c4fc07416: 338,37 horas (média)
00720abe85ba0859807595bbf045a33b: 200,14 horas (média)
00ab3eff1b5192e5f1a63bcecfee11c8: 217,26 horas (média)
00d8b143d12632bad99c0ad66ad52825: 173,39 horas (média)
00ee68308b45bc5e2660cd833c3f81cc: 207,05 horas (média)
00fc707aaaad2d31347cf883cd2dfe10: 368,73 horas (média)
010543a62bd80aa422851e79a3bc7540: 206,02 horas (média)
010da0602d7774602cd1b3f5fb7b709e: 602,77 horas (média)
011b0eaba87386a2ae96a7d32bb531d1: 584,31 horas (média)
01266d4c46afa519678d16a8b683d325: 131,85 horas (média)
013900e863eace745d3ec7614cab5b1a: 272,24 horas (média)
014c0679dd340a0e338872e7ec85666a: 450,29 horas (média)
014d9a685fd57276679edd00e07089e5: 207,13 horas (média)
0176f73cc1195f367f7b32db1e5b3aa8: 311,72 horas (média)
01bcc9d254a0143f0ce9791b960b2a47: 293,97 horas (média)
01c97ebb5cdac52891c0ed1c37ba0012: 297,55 horas (média)
01cf7e3d21494c41fb86034f2e714fa1: 267,50 horas (média)
01ed254b9ff8407dfb9d99ba1e17d923: 145,89 horas (média)
01fd077212124329bac32490e8ef80d9: 183,22 horas (média)
01fdefa7697d26ad920e9e0346d4bd1b: 249,23 horas (média)
0241d4d5d36f10f80c644447315af0bd: 251,94 horas (média)
0249d282d911d23cb8b869ab49c99f53: 238,46 horas (média)
024b564ae893ce8e9bfa02c10a401ece: 407,83 horas (média)
028872bfa080090a9d0abd4f1af168f8: 395,31 horas (média)
02a2272692e13558373c66db98f05e2e: dados não disponíveis
02b72cdeb9cfcc429f1af6f4e3f3b737: 282,74 horas (média)
02c988090b766852e088c69d7fb3b551: 189,14 horas (média)
02d35243ea2e497335cd0f076b45675d: 606,80 horas (média)
02dcd3e8e25bee036e32512bcf175493: 394,59 horas (média)
02ecc2a19303f05e59ce133fd923fff7: 244,95 horas (média)
02f5837340d7eb4f653d676c7256523a: 223,74 horas (média)
02f623a8eb246f3c5f7c2f96462654e6: 193,29 horas (média)
0307f7565ff85b299b6e5ef162b1b1a9: 362,56 horas (média)
0336182e1b3e92f029d5354832045fdf: 292,64 horas (média)
034b9387752bfa309f350a70cd45ffa3: 186,76 horas (média)
038b75b729c8a9a04b0d07cba7eabe86: 465,57 horas (média)
039b29ff3b3473435d0cd59040575de9: 215,33 horas (média)
039e6ad9dae79614493083e241147386: 338,99 horas (média)
03a2a6dcbe45d639c4dc2a0d24769c40: 243,63 horas (média)
03bd479e1d9484cdb14104d3023f7321: 483,07 horas (média)
0417b067eeab773d2f7061a726dc477f: 409,69 horas (média)
042573af89b6d931f672efaf789d8358: 473,66 horas (média)
04308b1ee57b6625f47df1d56f00eedf: 439,95 horas (média)
0432ead42b6c8a0bdf68154add917fdf: 204,62 horas (média)
044668ccd5316b12a7cf0d54a156e3e9: 172,43 horas (média)

Dados completos:
1. seller_id: 0015a82c2db000af6aaaf3ae2ecb0532, avg_hours: 245.7035185185185185
2. seller_id: 001cca7ae9ae17fb1caed9dfb1094831, avg_hours: 303.4328786799620133
3. seller_id: 001e6ad469a905060d959994f1b41e4f
4. seller_id: 002100f778ceb8431b7a1020ff7ab48f, avg_hours: 365.8767129629629630
5. seller_id: 003554e2dce176b5555353e4f3555ac8, avg_hours: 111.2127777777777778
6. seller_id: 004c9cd9d87a3c30c522c48c4fc07416, avg_hours: 338.3661377245508982
7. seller_id: 00720abe85ba0859807595bbf045a33b, avg_hours: 200.1439850427350427
8. seller_id: 00ab3eff1b5192e5f1a63bcecfee11c8, avg_hours: 217.2597222222222222
9. seller_id: 00d8b143d12632bad99c0ad66ad52825, avg_hours: 173.3886111111111111
10. seller_id: 00ee68308b45bc5e2660cd833c3f81cc, avg_hours: 207.0462742248062016
11. seller_id: 00fc707aaaad2d31347cf883cd2dfe10, avg_hours: 368.7300164609053498
12. seller_id: 010543a62bd80aa422851e79a3bc7540, avg_hours: 206.0247222222222223
13. seller_id: 010da0602d7774602cd1b3f5fb7b709e, avg_hours: 602.7688888888888889
14. seller_id: 011b0eaba87386a2ae96a7d32bb531d1, avg_hours: 584.3086111111111111
15. seller_id: 01266d4c46afa519678d16a8b683d325, avg_hours: 131.8483333333333334
16. seller_id: 013900e863eace745d3ec7614cab5b1a, avg_hours: 272.2403418803418803
17. seller_id: 014c0679dd340a0e338872e7ec85666a, avg_hours: 450.2917222222222222
18. seller_id: 014d9a685fd57276679edd00e07089e5, avg_hours: 207.1342592592592593
19. seller_id: 0176f73cc1195f367f7b32db1e5b3aa8, avg_hours: 311.7228947368421053
20. seller_id: 01bcc9d254a0143f0ce9791b960b2a47, avg_hours: 293.9747222222222222
21. seller_id: 01c97ebb5cdac52891c0ed1c37ba0012, avg_hours: 297.5459953703703704
22. seller_id: 01cf7e3d21494c41fb86034f2e714fa1, avg_hours: 267.5010256410256410
23. seller_id: 01ed254b9ff8407dfb9d99ba1e17d923, avg_hours: 145.8891111111111111
24. seller_id: 01fd077212124329bac32490e8ef80d9, avg_hours: 183.2237250712250712
25. seller_id: 01fdefa7697d26ad920e9e0346d4bd1b, avg_hours: 249.2319444444444444
26. seller_id: 0241d4d5d36f10f80c644447315af0bd, avg_hours: 251.9448419150858175
27. seller_id: 0249d282d911d23cb8b869ab49c99f53, avg_hours: 238.4577777777777778
28. seller_id: 024b564ae893ce8e9bfa02c10a401ece, avg_hours: 407.8298611111111112
29. seller_id: 028872bfa080090a9d0abd4f1af168f8, avg_hours: 395.3100000000000000
30. seller_id: 02a2272692e13558373c66db98f05e2e
31. seller_id: 02b72cdeb9cfcc429f1af6f4e3f3b737, avg_hours: 282.7427777777777778
32. seller_id: 02c988090b766852e088c69d7fb3b551, avg_hours: 189.1380381944444445
33. seller_id: 02d35243ea2e497335cd0f076b45675d, avg_hours: 606.8016319444444444
34. seller_id: 02dcd3e8e25bee036e32512bcf175493, avg_hours: 394.5882222222222222
35. seller_id: 02ecc2a19303f05e59ce133fd923fff7, avg_hours: 244.9455208333333333
36. seller_id: 02f5837340d7eb4f653d676c7256523a, avg_hours: 223.7388518518518518
37. seller_id: 02f623a8eb246f3c5f7c2f96462654e6, avg_hours: 193.2888005050505051
38. seller_id: 0307f7565ff85b299b6e5ef162b1b1a9, avg_hours: 362.5606944444444444
39. seller_id: 0336182e1b3e92f029d5354832045fdf, avg_hours: 292.6375000000000000
40. seller_id: 034b9387752bfa309f350a70cd45ffa3, avg_hours: 186.7550000000000000
41. seller_id: 038b75b729c8a9a04b0d07cba7eabe86, avg_hours: 465.5693055555555556
42. seller_id: 039b29ff3b3473435d0cd59040575de9, avg_hours: 215.3301234567901235
43. seller_id: 039e6ad9dae79614493083e241147386, avg_hours: 338.9950000000000000
44. seller_id: 03a2a6dcbe45d639c4dc2a0d24769c40, avg_hours: 243.6301543209876543
45. seller_id: 03bd479e1d9484cdb14104d3023f7321, avg_hours: 483.0729629629629629
46. seller_id: 0417b067eeab773d2f7061a726dc477f, avg_hours: 409.6879059829059829
47. seller_id: 042573af89b6d931f672efaf789d8358, avg_hours: 473.6569444444444444
48. seller_id: 04308b1ee57b6625f47df1d56f00eedf, avg_hours: 439.9487560386473430
49. seller_id: 0432ead42b6c8a0bdf68154add917fdf, avg_hours: 204.6234323116219668
50. seller_id: 044668ccd5316b12a7cf0d54a156e3e9, avg_hours: 172.4265277777777778
51. seller_id: 04843805947f0fc584fc1969b6e50fe7, avg_hours: 360.6372222222222222
52. seller_id: 048c2757535328e0d7dac690ad3c0aae, avg_hours: 433.1792611111111111
53. seller_id: 04aa0a1c5ce6b222003403a3e11c3cc0, avg_hours: 377.5431699346405229
54. seller_id: 04aba03279157f6d4e0fe8ccaf21963c, avg_hours: 269.8082592592592592
55. seller_id: 04e38a233f726ef161074ab1c9b0399a, avg_hours: 266.8444212962962963
56. seller_id: 04ee0ec01589969663ba5967c0e0bdc0, avg_hours: 73.2605555555555556
57. seller_id: 04fdea0c111866e6cf812f1570d6b5bd, avg_hours: 427.6733333333333333
58. seller_id: 0509040ea3fe50071181bbc359eb7738, avg_hours: 264.1225607638888889
59. seller_id: 052577151711aec5c744fe12e66db3e1, avg_hours: 336.2858333333333333
60. seller_id: 054694fa03fe82cec4b7551487331d74, avg_hours: 702.3197089947089947
61. seller_id: 056b4ada5bbc2c50cc7842547dda6b51, avg_hours: 294.8489957264957265
62. seller_id: 0570350b23eda5444f8d1d9544932058, avg_hours: 114.2463888888888889
63. seller_id: 05730013efda596306417c3b09302475, avg_hours: 214.0394444444444445
64. seller_id: 058cb5aeb36d7c0fcae20fc85d5e0a59, avg_hours: 217.4321064814814815
65. seller_id: 058fd0aa2bfdb2274e05e1ae971dabb6, avg_hours: 237.4790476190476190
66. seller_id: 05a48cc8859962767935ab9087417fbb, avg_hours: 269.6586111111111111
67. seller_id: 05a940b4ecae36cadfd8e93bd9c43257, avg_hours: 336.0685493827160494
68. seller_id: 05aebce0b5c8f0d41b29b686f2d05fd3, avg_hours: 96.3837500000000000
69. seller_id: 05ca864204d09595ae591b93ea9cf93d, avg_hours: 105.7641666666666667
70. seller_id: 05d2173d43ea568aa0540eba70d2ca76, avg_hours: 336.9842129629629630
71. seller_id: 05e107217c7266362fd44b75b2cd4cc4, avg_hours: 148.4208680555555556
72. seller_id: 05f51e13da97139648b8125c31e5f51b, avg_hours: 290.6162175925925926
73. seller_id: 05feb94f19d094d4b0f9281f0b1d4c99, avg_hours: 364.7933796296296296
74. seller_id: 05ff92fedb5be47920fea08e501238b9, avg_hours: 284.7244722222222222
75. seller_id: 062c325cd6a2b87845fab56b4ec2eeae, avg_hours: 128.4554166666666667
76. seller_id: 062ce95fa2ad4dfaedfc79260130565f, avg_hours: 309.0029990583804143
77. seller_id: 06532f10282704ef4c69168b914b77be, avg_hours: 390.8267013888888889
78. seller_id: 06579cb253ecd5a3a12a9e6eb6bf8f47, avg_hours: 256.0653015873015873
79. seller_id: 066a6914e1ebf3ea95a216c73a986b91, avg_hours: 335.2001929012345679
80. seller_id: 0691148aee60ca47977c187804f935ae, avg_hours: 302.8120440251572327
81. seller_id: 0692610d8abe24f287e9fae90ea0bbee, avg_hours: 153.8983333333333334
82. seller_id: 06a2c3af7b3aee5d69171b0e14f0ee87, avg_hours: 415.6880762852404643
83. seller_id: 06bb3a2fe5e7b7a845b13e8fb91bd944, avg_hours: 205.4654012345679013
84. seller_id: 06df0c10d34e459d9672bc77388742eb, avg_hours: 229.8965092592592593
85. seller_id: 06e5eefc71ec47ae763c5c6f8db7064f, avg_hours: 252.6895310633213859
86. seller_id: 07017df32dc5f2f1d2801e579548d620, avg_hours: 231.9234567901234568
87. seller_id: 070d165398b553f3b4b851c216b8a358, avg_hours: 253.4982163742690059
88. seller_id: 0725b8c0f3f906e58f70cbe76b7c748c, avg_hours: 265.2099922839506173
89. seller_id: 0743a0239d764b9a0f959a57d07e36ab, avg_hours: 128.0185416666666667
90. seller_id: 0747d5bb69f0586cc869d8af4c50f93e, avg_hours: 332.0189102564102564
91. seller_id: 0761743cbffb25d7148189e9f1a5f03a, avg_hours: 318.9855952380952381
92. seller_id: 077c5fae4bea9500e3737b16f71b9d3a, avg_hours: 181.9348148148148148
93. seller_id: 0791d9fc1e30678ecf03d3e55fa108d3, avg_hours: 146.3302525252525252
94. seller_id: 079d295dcbf06ee8bb1b65ba964eb2b6, avg_hours: 160.2581388888888889
95. seller_id: 07a9bc7f61396b658ddf3ac534efe44c, avg_hours: 143.6991666666666667
96. seller_id: 07bf9669d84d1f11be443a9dd938f698, avg_hours: 200.0261111111111111
97. seller_id: 07d75e33f2750d97d467fb57e4dfdd8a, avg_hours: 261.3073611111111111
98. seller_id: 07de60b03d150fb3ea09eab5da5e4c8b, avg_hours: 320.1829012345679012
99. seller_id: 07e8e8fc5222bb358e6f259da3197074, avg_hours: 206.7315277777777778
100. seller_id: 080102cd0a76b09e0dcf55fcacc60e05, avg_hours: 222.0578472222222222
101. seller_id: 080199a181c46c657dc5aa235411be3b, avg_hours: 188.7687583668005355
102. seller_id: 08061dc0fc165ed41288cc7acde738ee, avg_hours: 451.9199305555555556
103. seller_id: 08084d990eb3f53af056ccbc1730c8a7, avg_hours: 200.5814814814814815
104. seller_id: 081acf3de680d554796c9cf041be7bc2, avg_hours: 322.6151041666666667
105. seller_id: 082e0bf4cb865a6533b1e8e498cc0255, avg_hours: 299.7258574879227053
106. seller_id: 085f6f7e049c996695fb2074fe38d45e, avg_hours: 241.8532291666666667
107. seller_id: 08633c14ef2db992c11f840f04fad4cd, avg_hours: 232.87589060710194730619
108. seller_id: 0873d9f8f36123f8d910f4760e788cfb, avg_hours: 310.9672222222222223
109. seller_id: 0885aaf116795758dfeb5f1032487bcd, avg_hours: 128.8029980842911877
110. seller_id: 0887a9f087bcd5d9f6642b52f897fc6c, avg_hours: 335.9271296296296296
111. seller_id: 08ad4ac1388e4420ca531c3edfc46198, avg_hours: 129.1365079365079365
112. seller_id: 08cdbae123ff67ca4e36d9d641ce0119, avg_hours: 683.4473148148148148
113. seller_id: 08d0949a9a17c027262db1f3c450c26c, avg_hours: 339.7577546296296296
114. seller_id: 08d1c9478fb0d7d7fcac9c0da4e82fc7, avg_hours: 238.1363888888888889
115. seller_id: 08d2d642cf72b622b14dde1d2f5eb2f5, avg_hours: 351.5879583333333333
116. seller_id: 08f5819815f3d06545011850bd70f0a8, avg_hours: 197.2743518518518519
117. seller_id: 091065b789659bc3cd9af9cb3a6253ff, avg_hours: 250.7723611111111111
118. seller_id: 0936e1837d0c79253456bbb2ffaaef10, avg_hours: 425.7905555555555556
119. seller_id: 093805f8f2aeb63881444571e1f48f30, avg_hours: 176.9709053497942387
120. seller_id: 094ced053e257ae8cae57205592d6712, avg_hours: 278.5957309941520468
121. seller_id: 0951a6e282947e09cd47969f4ed0b47f, avg_hours: 109.6053571428571429
122. seller_id: 09883d9ab71c8fe8a9bfc7fc3075b07e, avg_hours: 330.4626388888888889
123. seller_id: 099095b050cfe8eb1ddff5317587e96e, avg_hours: 246.7846198830409357
124. seller_id: 09bad886111255c5b5030314fc7f1a4a, avg_hours: 134.5623888888888889
125. seller_id: 09f952a5f58d2285b0372551ae8f9b01, avg_hours: 300.3108829365079365
126. seller_id: 0a198e95d32b1be2da9424c962a6ebfa, avg_hours: 384.6905555555555556
127. seller_id: 0a82f5fb06a4fe4ac2cf7cb412ec71b8, avg_hours: 126.2805555555555556
128. seller_id: 0a85ebe4e328db81ac9109781205e2f7, avg_hours: 113.2320370370370370
129. seller_id: 0aa124728afc1131dff5655f4c6f487b
130. seller_id: 0aa2205ca24f113f4658a5c536667426, avg_hours: 152.1801767676767677
131. seller_id: 0ac4201fda2c68ebc0e47cb9423cf3c9, avg_hours: 287.1682341269841270
132. seller_id: 0ad80de75c811326389cfb1daba7d45e, avg_hours: 196.6498148148148149
133. seller_id: 0adac9fbd9a2b63cccaac4f8756c1ca8, avg_hours: 293.9898320895522388
134. seller_id: 0ade5cc4a305ed7093a23f68ca47519c, avg_hours: 152.7563888888888889
135. seller_id: 0aea4c6ae1505b3228ddf3dd7822ee5b, avg_hours: 429.0213888888888889
136. seller_id: 0af2ab31141893d26aca5a404a537dab, avg_hours: 137.4702777777777778
137. seller_id: 0af977692321d895349eded183341d28, avg_hours: 60.4434722222222223
138. seller_id: 0afccdb8a34ee5c79f7c06faf2b4d56e, avg_hours: 312.9850578703703704
139. seller_id: 0b09101900100c0e9d312861fad5a1b9, avg_hours: 444.3833333333333333
140. seller_id: 0b0ddbc7b9d9584f442c7ac92b0ff6c9, avg_hours: 278.3297222222222222
141. seller_id: 0b18d63d0cd1d723567903fd34a07df2, avg_hours: 156.5602976190476190
142. seller_id: 0b1ca3ef18a63d7eb0c8897fa0849c08, avg_hours: 135.0244444444444444
143. seller_id: 0b35c634521043bf4b47e21547b99ab5, avg_hours: 408.7575505050505050
144. seller_id: 0b36063d5818f81ccb94b54adfaebbf5, avg_hours: 348.2402777777777778
145. seller_id: 0b3f27369a4d8df98f7eb91077e438ac, avg_hours: 171.6906944444444445
146. seller_id: 0b46f784306be7200ca1700aa55d819f, avg_hours: 77.8477777777777778
147. seller_id: 0b64bcdb0784abc139af04077d49a20e, avg_hours: 203.6672222222222222
148. seller_id: 0b90b6df587eb83608a64ea8b390cf07, avg_hours: 335.7393633705475811
149. seller_id: 0bae85eb84b9fb3bd773911e89288d54, avg_hours: 238.9620804597701149
150. seller_id: 0bb27263628258b8111a0262769fa9db, avg_hours: 1000.1594444444444444
151. seller_id: 0bb738e4d789e63e2267697c42d35a2d, avg_hours: 277.3658812260536398
152. seller_id: 0be8ff43f22e456b4e0371b2245e4d01, avg_hours: 241.2912650793650794
153. seller_id: 0bebbb2cea103a4a020c95d43fd7d754, avg_hours: 140.4312037037037037
154. seller_id: 0bf0150d5b9d60d9cd2906003332f085, avg_hours: 329.2390412186379928
155. seller_id: 0bfd0b434243adc5c2e1aa6baf19c6aa, avg_hours: 200.8070370370370370
156. seller_id: 0c7533c71df861ec58ad7ff999ed0e8d, avg_hours: 247.8339611872146119
157. seller_id: 0c7f30ae9b147eca07affbef92832a6a, avg_hours: 202.9863333333333333
158. seller_id: 0c8380b62e38e8a1e6adbeba7eb9688c, avg_hours: 294.4473037716615698
159. seller_id: 0cab2da43793a6f3c5ed8514c5f54627, avg_hours: 111.8296296296296297
160. seller_id: 0cbcee27c791afa0cdcb08587a2013a8, avg_hours: 314.6032152777777778
161. seller_id: 0d33a55da925bbf1ff02af5f6059fc7f, avg_hours: 204.1329629629629629
162. seller_id: 0d4c8269e7f0401201794deef160edd6, avg_hours: 444.8982638888888889
163. seller_id: 0d83f8e03188682112cc0d93523705cc, avg_hours: 588.3505555555555556
164. seller_id: 0d85bbda9889ce1f7e63778d24f346eb, avg_hours: 428.2687739463601533
165. seller_id: 0daf5180aa44356f60f8effa533b55a2, avg_hours: 170.1165277777777778
166. seller_id: 0db783cfcd3b73998abc6e10e59a102f, avg_hours: 267.2157201646090535
167. seller_id: 0dd184061fb0eaa7ca37932c68ab91c5, avg_hours: 262.0342012089810017
168. seller_id: 0ddefe3c7a032b91f4e25b9c3a08fca1, avg_hours: 198.5910277777777778
169. seller_id: 0df3984f9dfb3d49ac6366acbd3bbb85, avg_hours: 221.7362247474747475
170. seller_id: 0dfbed20065e425d2eaefb101f9816c0, avg_hours: 517.3276851851851852
171. seller_id: 0e44d110fa6a54e121cb2c095a77762f, avg_hours: 265.6349074074074074
172. seller_id: 0e72c1a751b496722a6cb1f10653b62a, avg_hours: 163.4890740740740741
173. seller_id: 0e982cff76cc0579f632cea8a0e38c9d, avg_hours: 188.9116666666666667
174. seller_id: 0ea22c1cfbdc755f86b9b54b39c16043, avg_hours: 252.4846278825995807
175. seller_id: 0eaa7e33d73809f1f925f7d07c506cbd, avg_hours: 133.5977592592592593
176. seller_id: 0ebd97a106433a45a4aebe57c1799778, avg_hours: 212.0294357638888889
177. seller_id: 0ec28cec4046a4a199b6de9b4c891d97, avg_hours: 196.7540972222222223
178. seller_id: 0ed6ce5d87fd9c69eaacaeb778d67235, avg_hours: 376.2427910052910053
179. seller_id: 0ee4fb99ac55ffbbc98795aa01b7f8fa, avg_hours: 164.9891666666666667
180. seller_id: 0ef83d7d83ed97cd2a0049ac8be5f88a, avg_hours: 224.8909949494949495
181. seller_id: 0f0c984a4a955310903b6b6008660bad, avg_hours: 339.3657638888888889
182. seller_id: 0f519b0d2e5eb2227c93dd25038bfc01, avg_hours: 294.1808333333333333
183. seller_id: 0f7eea709efdf942b5f95c7516dbacd7, avg_hours: 192.7490740740740741
184. seller_id: 0f80a40c312b2472dca482cf50f5186f, avg_hours: 127.5755555555555556
185. seller_id: 0f94588695d71662beec8d883ffacf09, avg_hours: 357.1494444444444444
186. seller_id: 0fe2d9733ed841eb064503920015a8c0, avg_hours: 207.7178703703703704
187. seller_id: 0ff83046c3fa22efee8ecf291888b191, avg_hours: 288.9163888888888889
188. seller_id: 0ffa40d54288e4f3499b8780dd0f144f, avg_hours: 311.9970555555555556
189. seller_id: 10076e5788b8ee532724bcd460baf762, avg_hours: 231.1702136752136752
190. seller_id: 10089e9f2fd0c668a8fd4e52e1698888, avg_hours: 183.0876851851851852
191. seller_id: 101921376b577a4540dc30e9009133ca
192. seller_id: 101a3a003516bc11253298b2fad3cb65, avg_hours: 155.4387962962962963
193. seller_id: 1025f0e2d44d7041d6cf58b6550e0bfa, avg_hours: 276.7722701486697966
194. seller_id: 10264f60a8f0a4d2f30810f5c661c673, avg_hours: 95.2138194444444445
195. seller_id: 1099a00e0ee3a50935e6c2447ca090c5, avg_hours: 360.7331481481481482
196. seller_id: 10cdd491d1dbea8fb4ead97b19c334ce, avg_hours: 169.9114814814814815
197. seller_id: 10ff823eda2b032e2c93d17a7d294736, avg_hours: 229.5679166666666667
198. seller_id: 112453736dbe3889cfb74e1aaa0ba0c1, avg_hours: 319.1639682539682540
199. seller_id: 1127b7f2594683f2510f1c2c834a486b, avg_hours: 234.8394661458333333
200. seller_id: 11305281b50fff20ae8bb473f8e11876, avg_hours: 324.2958541666666667
201. seller_id: 113e3a788b935f48aad63e1c41dac1bd, avg_hours: 278.6861342592592593
202. seller_id: 116ccb1a1604bc88e4d234a8c23f33de, avg_hours: 200.4662480974124810
203. seller_id: 11742f81550ac064cc9a40f67151d9ad, avg_hours: 206.2426388888888889
204. seller_id: 117cfc326c6d50da67ca858ff5c0c852, avg_hours: 140.5807777777777778
205. seller_id: 11938fcc75f6902fea1d0a6f72b54a57, avg_hours: 536.4520833333333334
206. seller_id: 119c7f1a00ef43fad0e57604e76a747c, avg_hours: 143.0980555555555556
207. seller_id: 119d1aef1b4144adba89163f6cd9f5d4, avg_hours: 106.8197222222222222
208. seller_id: 11bfa66332777660bd0640ee84d47006, avg_hours: 375.4165550108932462
209. seller_id: 11d4c477d09821164bca4f70a2eae031, avg_hours: 160.7828472222222222
210. seller_id: 11eac105f3f90a9b87b19c89d91e24f3, avg_hours: 213.9973333333333333
211. seller_id: 11fb6f6d341adbe19e81733701704635, avg_hours: 119.0286111111111111
212. seller_id: 120476eb7a04c149d14772edaf5d9bf2, avg_hours: 145.6917592592592592
213. seller_id: 1284de4ae8aa26997e748c851557cf0e, avg_hours: 441.2443518518518518
214. seller_id: 128639473a139ac0f3e5f5ade55873a5, avg_hours: 336.1392679502607300
215. seller_id: 128f9bfbe4c7d5185033914b1de3d39a, avg_hours: 289.3512962962962963
216. seller_id: 12a8eb0f8d1cd3270695bf2a99f55966, avg_hours: 503.2481944444444445
217. seller_id: 12b9676b00f60f3b700e83af21824c0e, avg_hours: 349.2166541353383459
218. seller_id: 12c2ed9cded6138cf0c75f525f565fc7, avg_hours: 293.5540972222222222
219. seller_id: 13074f016982ff2bd6c58ced8682f000, avg_hours: 343.6541071428571429
220. seller_id: 131fcb0a0c9a47bba4474aacff0f14b7, avg_hours: 102.9706944444444444
221. seller_id: 1336efc61c316ddf92c899eb817f7cae, avg_hours: 273.1685490196078431
222. seller_id: 134285d1f41da5c13a756ee8142c8a4e, avg_hours: 205.1708333333333333
223. seller_id: 134a288e7de827ec5ec62e3ec9c3a295, avg_hours: 203.3181790123456790
224. seller_id: 134b867a0f7f8bbe6abf10f91874891e, avg_hours: 300.2241666666666667
225. seller_id: 13511db12ac61e2f89c53b72a944a60b, avg_hours: 212.2535648148148148
226. seller_id: 1352e06ae67b410cdae0b2a22361167b, avg_hours: 823.1886111111111111
227. seller_id: 1354d51653f645349064725ed204e85e, avg_hours: 206.8995833333333333
228. seller_id: 138dbe45fc62f1e244378131a6801526, avg_hours: 139.2402873563218391
229. seller_id: 139157dd4daa45c25b0807ffff348363, avg_hours: 28.8819444444444444
230. seller_id: 13c2ed7698b3ca92dad49e849219da59, avg_hours: 274.4949691358024691
231. seller_id: 13d058e4eeac2ce8217660b2f8a05812, avg_hours: 263.5278535353535354
232. seller_id: 13d95f0f6f73943d4ceffad0fc2cd32c, avg_hours: 512.2658333333333333
233. seller_id: 13dd308f81fea30cc670c656b2b46cc3, avg_hours: 86.9807407407407408
234. seller_id: 13e85aac53340018b40c2af68001b7e0, avg_hours: 364.8894444444444444
235. seller_id: 13f57c12a00ed4610db646b913a7f5c6, avg_hours: 292.7365811965811966
236. seller_id: 13fa2a6c6b9d0f43cb588d7c82117a12, avg_hours: 481.4100555555555556
237. seller_id: 141440cad9341e553f8401c574a2aa38, avg_hours: 160.5950925925925926
238. seller_id: 1430239a858e7682bbc43b20758af153, avg_hours: 171.2768939393939394
239. seller_id: 1444c08e64d55fb3c25f0f09c07ffcf2, avg_hours: 225.6144444444444444
240. seller_id: 1464afc72f696af775557a821c2e253f, avg_hours: 253.8513888888888889
241. seller_id: 14a08204d03bb6b6bde8029f801ae0eb, avg_hours: 197.0664619883040936
242. seller_id: 14d7985702e72162bbf13b6beb74ab2b, avg_hours: 252.0014839181286550
243. seller_id: 14ee35374a7876217954b5fa08e50463, avg_hours: 409.3964351851851852
244. seller_id: 14f2b3587172b9db894c9bad8dab520b, avg_hours: 336.5111111111111111
245. seller_id: 152ee17e4c8aaf53dac99f3462e4999b, avg_hours: 236.3347222222222222
246. seller_id: 154bdf805377afea75a3bd158e9eab10, avg_hours: 528.5458333333333333
247. seller_id: 1554a68530182680ad5c8b042c3ab563, avg_hours: 328.9573397836038285
248. seller_id: 157c3e4b42f81ac4a44e8b1ca2fe9876, avg_hours: 230.9412544802867384
249. seller_id: 1588ac4010787100dddef64568f0ae35, avg_hours: 411.9836111111111111
250. seller_id: 15aac934c58d886785ac1b17953ea898, avg_hours: 360.3609722222222222
251. seller_id: 15ac3c501e2599e4917316fde5c5669a
252. seller_id: 15aec03fe4cf30dfa574cf550f5ff5ff
253. seller_id: 15b3b1b81484422eb41df68ac87f1f50, avg_hours: 347.9133333333333333
254. seller_id: 15cd6eefe58588619aaed41dfa6621b1, avg_hours: 341.3681018518518518
255. seller_id: 15ead3a5037a918ddb520dfe39a3d2b9, avg_hours: 430.6892063492063492
256. seller_id: 15fa791d5e017f66402dc28c44480657, avg_hours: 274.3948958333333334
257. seller_id: 160851d3ece7aa1a510f8d1a4bb8a8af, avg_hours: 103.4959722222222223
258. seller_id: 16090f2ca825584b5a147ab24aa30c86, avg_hours: 208.00320333880678708147
259. seller_id: 160e4f13fd3a64b1b86807be88b5ffb0, avg_hours: 342.5820138888888889
260. seller_id: 164a5a8794e6d42e14f55e447b12a3bc, avg_hours: 321.1261111111111111
261. seller_id: 165b1235e9e9942cb5fae67103576fb0, avg_hours: 164.5250347222222222
262. seller_id: 165fc07beebdcb6190fba8a06db2a449, avg_hours: 309.6742230902777778
263. seller_id: 1660ad786c27fd935378b6192a90b417, avg_hours: 207.9869230769230769
264. seller_id: 166e8f1381e09651983c38b1f6f91c11, avg_hours: 341.0809722222222222
265. seller_id: 167fd940acebc789debd6eb418c46e38, avg_hours: 356.9128888888888889
266. seller_id: 1690cada046eb7e92c12f98b1f8a8167, avg_hours: 156.9455000000000000
267. seller_id: 16bdc8cefd0e32a6f0824d296c5ad14a, avg_hours: 221.3836111111111111
268. seller_id: 1703bc09972dab9782e7a9194943b69f, avg_hours: 290.6188888888888889
269. seller_id: 1710c3aaa9c6b44ec3883ee0fe300e21, avg_hours: 145.1068055555555556
270. seller_id: 17306570e772e7718c92a562d33f5f1d, avg_hours: 327.1562407407407407
271. seller_id: 173d56ffbd4c56cb80fc3615487d712b, avg_hours: 162.0293055555555556
272. seller_id: 1746c1ae87ac63d530c7c943d0ac42e2, avg_hours: 552.3925000000000000
273. seller_id: 1771297ac436903d1dd6b0e9279aa505, avg_hours: 221.3452314814814815
274. seller_id: 1782ce2db72c3dda627d5e7c898104e1, avg_hours: 647.6746388888888889
275. seller_id: 17908cf9b444ee34047cadd5c0f4a516, avg_hours: 429.4551262626262626
276. seller_id: 17998cf586426bf0f2c3726cb0a4b211, avg_hours: 181.8870833333333334
277. seller_id: 179d859f51292aac5c10806a356f7af9, avg_hours: 189.4634795321637427
278. seller_id: 17a053fcb14bd219540cbde0df490be0, avg_hours: 271.3136655405405405
279. seller_id: 17adeba047385fb0c67d8e90b4296d21
280. seller_id: 17ca9b9e9b9ef8fdb529001b49ebb50f, avg_hours: 179.7867100694444444
281. seller_id: 17e34d8224d27a541263c4c64b11a56b, avg_hours: 329.9825288461538462
282. seller_id: 17eea220a40cc0d2c0c5346379682398, avg_hours: 592.0948148148148148
283. seller_id: 17f51e7198701186712e53a39c564617, avg_hours: 533.9122495446265938
284. seller_id: 180c3376aff0e43dd5788709df48a843, avg_hours: 379.8933888888888889
285. seller_id: 1835b56ce799e6a4dc4eddc053f04066, avg_hours: 297.0578367614438395
286. seller_id: 1838dd9b8977065acf51d95e0053ea7a, avg_hours: 290.9801153846153846
287. seller_id: 184725737946a1a938bbbd1a9e978103, avg_hours: 205.5933333333333334
288. seller_id: 184a67a8f9f63234d3a92340bbdb727f, avg_hours: 369.7663611111111111
289. seller_id: 186cdd1b2df32caa72cfb410bba768d3, avg_hours: 210.7689814814814815
290. seller_id: 189ca3538ce9f920cacf0f982cbe223b, avg_hours: 60.0945555555555555
291. seller_id: 18a349e75d307f4b4cc646a691ed4216, avg_hours: 251.7475412326388889
292. seller_id: 18e694e0e48ed6f7aa3f24aade5fd697, avg_hours: 135.7310457516339869
293. seller_id: 1900267e848ceeba8fa32d80c1a5f5a8, avg_hours: 297.7802283832589760
294. seller_id: 191d55f7edb8524d525ed01b20fe32e8, avg_hours: 540.3865740740740741
295. seller_id: 1927cdb9fa74f5270097f6250e8e8f34, avg_hours: 194.9691666666666667
296. seller_id: 19484c79cef6c062cb177aa4ef2fcc3c, avg_hours: 501.2286111111111111
297. seller_id: 1961c3e1272bfeceb05d0b78b5bbfdaf, avg_hours: 112.0482407407407407
298. seller_id: 1967a9e2ad6f51802b093147d861df58
299. seller_id: 1976a05ecf2996d6ffb7b5430e635fe7, avg_hours: 390.2183950617283951
300. seller_id: 1987cd4be10fe09ee50454f9c354d1c6, avg_hours: 374.5474305555555556
301. seller_id: 198c7ea11960a9844b544d9bcdca860c, avg_hours: 337.4934000000000000
302. seller_id: 1992f8fb6b19fcccd97ca819811e7267
303. seller_id: 1996942dc085d7773ba77a529b163cd0, avg_hours: 280.1456790123456790
304. seller_id: 19a7c9f66ffa6452ff4b4c0cca71da27, avg_hours: 604.2425000000000000
305. seller_id: 19d62d484cba71963c93f0f00ab42013, avg_hours: 333.6736111111111111
306. seller_id: 19e0f40a907ec568c34bfac15de4f4a1, avg_hours: 131.9838194444444445
307. seller_id: 1a3df491d1c4f1589fc2b934ada68bf2, avg_hours: 351.1349561403508772
308. seller_id: 1a6245add4353f18ed55138808906979
309. seller_id: 1a8e2d9c38b84a9702ac7922924b0573, avg_hours: 374.0011111111111111
310. seller_id: 1a932caad4f9d804097d7f8e615baed1, avg_hours: 204.8792962962962963
311. seller_id: 1acde099eb406aa220b1169b188b42da, avg_hours: 289.2311111111111111
312. seller_id: 1b0b0f4f95e962d6f32fe90c759d0479, avg_hours: 226.7213888888888889
313. seller_id: 1b1ae47a313a825a7ccceb8e2e30fa9d, avg_hours: 251.1311666666666667
314. seller_id: 1b45169b635ef59425637e9a33eb5fb3, avg_hours: 183.2649652777777778
315. seller_id: 1b4b28463457a256e9a784ebe2a8f630, avg_hours: 304.4672222222222222
316. seller_id: 1b4c3a6f53068f0b6944d2d005c9fc89, avg_hours: 331.0853743961352657
317. seller_id: 1b61fb1f0f2185d89e9a126c498e9cc7, avg_hours: 272.4455555555555556
318. seller_id: 1b65c144b17e607c0f37f10bb7dfec8d, avg_hours: 178.7028888888888889
319. seller_id: 1b7e5006cb25dd23ce8686691013b121, avg_hours: 365.4910858585858586
320. seller_id: 1b8356dabde1d35e17cef975c3f82730, avg_hours: 238.0941712962962963
321. seller_id: 1b8b75e227c9a9c100d0c210fb6176ce, avg_hours: 349.2107592592592593
322. seller_id: 1b938a7ec6ac5061a66a3766e0e75f90, avg_hours: 259.7381541218637993
323. seller_id: 1bb2bdb95f4841f1bba2c0d2cd83d3c9, avg_hours: 283.7217737617135208
324. seller_id: 1bb3812d5f0747a3ab7348f199001a10, avg_hours: 290.0538580246913580
325. seller_id: 1bc2e21de46adfea6b98cc96b00f3b40, avg_hours: 378.7603888888888889
326. seller_id: 1c129092bf23f28a5930387c980c0dfc, avg_hours: 270.7642897006595637
327. seller_id: 1c40343cc5d18c2d8248ac2f3366de34, avg_hours: 171.3571969696969697
328. seller_id: 1c56ffe0e9dea2657fc6e95b53f40b13, avg_hours: 146.2761111111111111
329. seller_id: 1c5e4e49b9079480255b49d50aac1aa9, avg_hours: 205.3790046296296296
330. seller_id: 1c68394e931a64f90ea236c5ea590300, avg_hours: 367.3613515269655620
331. seller_id: 1c742ac33582852aaf3bcfbf5893abcf, avg_hours: 134.2102777777777778
332. seller_id: 1c83418358f249c9d6affa52d579db0e, avg_hours: 244.3625000000000000
333. seller_id: 1ca4bdb0cd7fc48e949bac066188ed26, avg_hours: 342.9528703703703704
334. seller_id: 1ca7077d890b907f89be8c954a02686a, avg_hours: 353.6405096237970254
335. seller_id: 1caf283236cd69af44cbc09a0a1e7d32, avg_hours: 326.4363963963963964
336. seller_id: 1cbcd2ee0afb3fc09963b87eb65e7e4f, avg_hours: 87.2813888888888889
337. seller_id: 1cbd32d00d01bb8087a5eb088612fd9c, avg_hours: 284.4420370370370371
338. seller_id: 1cbd50a8c52e6cf8e315c5709fab386f, avg_hours: 425.8676543209876543
339. seller_id: 1cbdc7cf130a41fd13a3c2a7d2fcfda7, avg_hours: 166.2777777777777778
340. seller_id: 1cd9e0cc1839d55516843def5600816d, avg_hours: 169.4629444444444444
341. seller_id: 1ce3ae5a399804d1a87e706f8a813c3e, avg_hours: 314.3386111111111111
342. seller_id: 1d0646a72178a6fb37ee8082140e06ec, avg_hours: 183.4126388888888889
343. seller_id: 1d0997ff06b524ce9289ffd75114ecd3, avg_hours: 406.7425925925925926
344. seller_id: 1d139e3a3b14025640d8df1b230aace0, avg_hours: 183.5018055555555556
345. seller_id: 1d1bbb8ac1581824986f582583fff01d, avg_hours: 219.6539583333333333
346. seller_id: 1d2732ef8321502ee8488e8bed1ab8cd, avg_hours: 249.9100555555555556
347. seller_id: 1d29dfba02015238dfbe2449a5eaa361, avg_hours: 344.6255555555555556
348. seller_id: 1d4587203296c8f4ad134dc286fa6db0, avg_hours: 214.5049254742547426
349. seller_id: 1d503743d2526f03f0c2c89540ee008c, avg_hours: 211.6528267973856209
350. seller_id: 1d8dbc4f32378d715c717c1c1fc57bae, avg_hours: 366.8536912943871707
351. seller_id: 1d953075c2f0dd990bacf27b83b330f1, avg_hours: 174.5416666666666667
352. seller_id: 1da366cade6d8276e7d8beea7af5d4bf, avg_hours: 406.0551793981481481
353. seller_id: 1da3aeb70d7989d1e6d9b0e887f97c23, avg_hours: 191.6628600823045267
354. seller_id: 1dc2de47ee26a0a5b12dc14fd6dc0dea, avg_hours: 341.3507818930041152
355. seller_id: 1dcfa3835714681d4ba4a93bc1e0fd41, avg_hours: 367.8315277777777778
356. seller_id: 1dd33b8119b3cb1056ed5dc88cd0aaf4, avg_hours: 249.0760763888888889
357. seller_id: 1de62b6f2fd96227629786db492433db, avg_hours: 197.3416666666666667
358. seller_id: 1dfe5347016252a7884b694d4f10f5c4, avg_hours: 458.5568803418803419
359. seller_id: 1e26c56af8d48424e1df0140a2401f83, avg_hours: 125.6479166666666667
360. seller_id: 1e47d8b6546eb3a77b1acddcc9406242, avg_hours: 851.6841666666666667
361. seller_id: 1e47defeeadeca0e9a18fa5a9311e735, avg_hours: 288.1275925925925926
362. seller_id: 1e483cc5c76fef08d3ca05f9a8af7d01, avg_hours: 182.2295555555555555
363. seller_id: 1e8b33f18b4f7598d87f5cbee2282cc2, avg_hours: 178.0993405275779376
364. seller_id: 1e8c6a4c538f286aee9573239740a4b4, avg_hours: 174.9901666666666667
365. seller_id: 1e9d5a33694bddb76316fd1f54734d20, avg_hours: 293.8477777777777778
366. seller_id: 1eade46fba20122dc4aefb379f8c636b, avg_hours: 279.1164074074074074
367. seller_id: 1f1bb1f0859883505541bdd6606193e5, avg_hours: 335.7756800766283525
368. seller_id: 1f2eebc0e970fd3c463e4f5d9652687a, avg_hours: 273.5186111111111111
369. seller_id: 1f50f920176fa81dab994f9023523100, avg_hours: 360.3495273739471559
370. seller_id: 1f7dfad2cb384ea4d2d7e1ffbd78c407, avg_hours: 152.3963888888888889
371. seller_id: 1f7fd2a6fcd5a6fa5d8a4dabc72aaae0, avg_hours: 167.4889814814814815
372. seller_id: 1f867308a0ce13133a4e639ff4de0c02, avg_hours: 244.0155769230769231
373. seller_id: 1f9ab4708f3056ede07124aad39a2554, avg_hours: 338.4229076479076479
374. seller_id: 1fa2d3def6adfa70e58c276bb64fe5bb, avg_hours: 149.7897222222222222
375. seller_id: 1fbe10c70e30765ed1de86d9f7e98409, avg_hours: 178.9646759259259259
376. seller_id: 1fdc574883ef3b33ad41562d93f3a74a, avg_hours: 259.7586882716049383
377. seller_id: 1fddcb7b326905d3ad5efe82187db347
378. seller_id: 1fe5540d7c1c37a595fefbacd5570d9e, avg_hours: 282.8592777777777778
379. seller_id: 1fe61aa5494bd3ae92a2c13e067c810f, avg_hours: 191.4219444444444444
380. seller_id: 2009a095de2a2a41626f6c6d7722678d, avg_hours: 223.9169212962962963
381. seller_id: 2039c5e51785b5dde7cf93ccb3b7be2c, avg_hours: 198.2219444444444444
382. seller_id: 204b4e07bddef3c9b317f70189135b22, avg_hours: 244.2655555555555556
383. seller_id: 2059c39f76271d4ca3f15b5ffaccc8b8, avg_hours: 220.4860185185185185
384. seller_id: 20611af7866c6068fd5ae1f9dbe15c92, avg_hours: 195.1009722222222222
385. seller_id: 2063dd1b9f568df1c16741ea7d3e6adb, avg_hours: 303.3890740740740741
386. seller_id: 2075d8cd4dd63ff12df0749a5866bb06, avg_hours: 104.2437962962962963
387. seller_id: 2078fe5066350e7d220c0ad3a3bbc6c1
388. seller_id: 2089a6d640999f9b9141ac719b2af596, avg_hours: 455.4879132791327913
389. seller_id: 20a7efa9721046319bdde5d60b6b5365, avg_hours: 354.2225462962962963
390. seller_id: 20a8b0dc55da94fe74d112082427c84f, avg_hours: 194.4000000000000000
391. seller_id: 20b54c376b794ed028df09a3cd88e8dc, avg_hours: 503.7339682539682540
392. seller_id: 20cb7c2fde3e5bf10f0bbe7394e1c6a9, avg_hours: 280.7076444444444444
393. seller_id: 20d53aad4fe5ee93a64f8839609d3586, avg_hours: 942.3819444444444444
394. seller_id: 20d83f3ef0e6925fd74bfd59170babf7, avg_hours: 192.0021039094650206
395. seller_id: 20f0aeea30bc3b8c4420be8ced4226c0, avg_hours: 1073.0450000000000000
396. seller_id: 20fd2d2080ed85fa67fad3fcbb2c1813
397. seller_id: 2138ccb85b11a4ec1e37afbd1c8eda1f, avg_hours: 258.7749065234685760
398. seller_id: 213b25e6f54661939f11710a6fddb871, avg_hours: 355.0345453216374269
399. seller_id: 213fafb0ca06fb3d5886579c2565791b, avg_hours: 87.2622222222222222
400. seller_id: 2156f2671501a81034d7d07f217609d0, avg_hours: 350.7192460317460317
401. seller_id: 217f005bb37ff3aeef5b2ae1788e75ba, avg_hours: 346.7498611111111111
402. seller_id: 218d46b86c1881d022bce9c68a7d4b15, avg_hours: 322.7141964285714286
403. seller_id: 218f991754f360af9c2daa5e0b8e990c, avg_hours: 312.4161437908496732
404. seller_id: 2199e7fe213c16213bf5d6a7eadc9a5d, avg_hours: 254.8900555555555556
405. seller_id: 21c62b998a043ebe31161d38f84929fc, avg_hours: 318.9025000000000000
406. seller_id: 21d59342ba150175ca2aa4f8faddeca6, avg_hours: 204.6711111111111111
407. seller_id: 21e83881401b92b49fb09a16d3852291, avg_hours: 252.1547008547008547
408. seller_id: 2235cf78d3e2073a88146a9cb60f0dd0, avg_hours: 326.8536111111111111
409. seller_id: 226b05fe067266c59c15dae208213d06, avg_hours: 228.6600757575757576
410. seller_id: 228e4c1a0be164f613d41c24345f9d2c, avg_hours: 262.0533333333333333
411. seller_id: 229c3efbfb0ea2058de4ccdfbc3d784a, avg_hours: 251.1152413793103448
412. seller_id: 22a23e5ac7061fc538cc2a019afaaf16, avg_hours: 264.5341666666666667
413. seller_id: 22c32ec35d0116ef02c281798a25bf8b, avg_hours: 225.5543981481481482
414. seller_id: 2305ab43e846518f58dd9d59f3f54e96, avg_hours: 282.3337037037037037
415. seller_id: 232a6014e7b10cba61c6c2b2ea6bb4b0, avg_hours: 318.3209365079365079
416. seller_id: 23613d49c3ac2bd302259e55c06c050c, avg_hours: 320.9726265822784810
417. seller_id: 236585a4ddb5fea9fa40233e2249ed91, avg_hours: 302.3849747474747475
418. seller_id: 2379bdc3888025689a9deb7b141507d5, avg_hours: 437.2416049382716049
419. seller_id: 238fac594e170b59c6d228f5a4f4f1d9, avg_hours: 292.3669259259259259
420. seller_id: 23a0ffca143a15b9b5bbdb7d552f626a, avg_hours: 260.6789236111111111
421. seller_id: 23c38debaffe4a25a30fdbd9b586a13f, avg_hours: 267.3170048309178744
422. seller_id: 23ca5f678e0b3ea6c630b30fa8bf51ea, avg_hours: 179.9380555555555556
423. seller_id: 23d7c96d4a1160db1c726b248601b25a, avg_hours: 312.6094925213675214
424. seller_id: 23ff42c4bf1f8f16cddb19d8b972974a, avg_hours: 296.2442592592592593
425. seller_id: 240b9776d844d37535668549a396af32, avg_hours: 262.2412063492063492
426. seller_id: 244b04680fdbded0acf5aebd9c92b44a, avg_hours: 912.0395833333333333
427. seller_id: 244c2f1bff6afe1f2eaf9bfe9b2aed38, avg_hours: 357.2401234567901235
428. seller_id: 247587846358bb1d2e4c6522020b36fe, avg_hours: 115.0000000000000000
429. seller_id: 2493dc3f20131696a0ecdb9948051a8d, avg_hours: 204.6061805555555556
430. seller_id: 249f0e9905a6e06ad6c6bea7547ab9f6, avg_hours: 147.0704629629629630
431. seller_id: 24a6daf925d9d591870a66660416de31, avg_hours: 319.8979166666666667
432. seller_id: 24c1de8d9551c0b4fbc53317d53efda8, avg_hours: 273.7005555555555556
433. seller_id: 2528513dd95219a6013d4d05176e391a, avg_hours: 239.6105840026773762
434. seller_id: 2528744c5ef5d955adc318720a94d2e7, avg_hours: 219.0623333333333333
435. seller_id: 252e76235acb79183cfca6e34f13337d, avg_hours: 316.8715277777777778
436. seller_id: 253c025bab43881055aeecde5e2d8b77, avg_hours: 390.3251388888888889
437. seller_id: 253f95b3a0e6983ae18aed49fbc2b845, avg_hours: 214.4469444444444444
438. seller_id: 257e61d3251fb5efb9daadddbc2cf7ca, avg_hours: 181.7263888888888889
439. seller_id: 258447aad3f7b01e2643c89f64dc5647, avg_hours: 190.5308333333333333
440. seller_id: 259f7b5e6e482c230e5bfaa670b6bb8f, avg_hours: 196.1045799039780521
441. seller_id: 25be943a321c8938947bdaabca979a90, avg_hours: 76.5939814814814815
442. seller_id: 25c5c91f63607446a97b143d2d535d31, avg_hours: 317.1694005847953216
443. seller_id: 25cf099de44674fde97473224f9d59ab, avg_hours: 216.3140555555555556
444. seller_id: 25debeafbce801fdd479539350185eee, avg_hours: 352.6579166666666667
445. seller_id: 25e47381a6c510ddeb36084e33b89f0c, avg_hours: 223.7278758169934641
446. seller_id: 25e6ffe976bd75618accfe16cefcbd0d, avg_hours: 228.2791666666666667
447. seller_id: 262237171f48e85819065498cac80d7b, avg_hours: 190.0421388888888889
448. seller_id: 2646baaf662d4d92ac48f047e35db92d, avg_hours: 124.4282716049382716
449. seller_id: 26562f211dd1364af2a8596dc945e8ae, avg_hours: 53.7633333333333333
450. seller_id: 265fdc289dffa9f1ad801c74f7d0de47, avg_hours: 176.4222222222222222
451. seller_id: 26785a546900236d66f2e4197c211158, avg_hours: 132.5782037037037037
452. seller_id: 269c5fc9fcadee614364c3620c30a1f9, avg_hours: 109.6980555555555555
453. seller_id: 269cff2d3c8d205c11f37a52402ea93b, avg_hours: 170.5246111111111111
454. seller_id: 26af45f5dfd967225a832838aa4e24a3, avg_hours: 212.5850757575757576
455. seller_id: 26b482dccfa29bd2e40703ba45523702, avg_hours: 81.3419444444444444
456. seller_id: 26bad72add1f86e08a776ce4ffdaf1ca, avg_hours: 253.4175000000000000
457. seller_id: 26d6bbee02420494d471c9f6436929c0, avg_hours: 176.2364316239316239
458. seller_id: 26d8a1c7c75d513045798992ead43aa2, avg_hours: 294.5005169753086420
459. seller_id: 26e13b6ff5b641b329e5524241ee2c93, avg_hours: 159.1150694444444444
460. seller_id: 26e2c91ef821e1ff8985f408788fe35b, avg_hours: 588.3783928571428571
461. seller_id: 26e2e5033827d2ba53929f43e03d8ffe, avg_hours: 126.2313888888888889
462. seller_id: 26f6b7ab07be3e9e69ce82a6552efc19, avg_hours: 245.3679166666666667
463. seller_id: 270297ead4c65a6cd2593960d2af6b21, avg_hours: 342.0440643274853801
464. seller_id: 270572bb714b00531be85e16e1550f26, avg_hours: 265.2225000000000000
465. seller_id: 2709af9587499e95e803a6498a5a56e9, avg_hours: 288.2672403381642512
466. seller_id: 270d3ef21830ad0ecf3a6c53d08a533a, avg_hours: 269.5330228758169935
467. seller_id: 271b8923c6a549e02d3c9fd1f8c0422b, avg_hours: 308.3286111111111111
468. seller_id: 271c58a1d139c45eaf3316107c6d3a3b, avg_hours: 305.5750205761316872
469. seller_id: 272f092de69afedd4d2969440b37f18f, avg_hours: 220.6462820512820513
470. seller_id: 2745f798279e0ed033addcc1474776d7, avg_hours: 305.9960590277777778
471. seller_id: 276677b5d08786d5dce7c2149dcce48b, avg_hours: 248.7590308641975309
472. seller_id: 278b6e0b20c4f61fefaa0577943d7a35
473. seller_id: 27a56ff04b34c2ba34ce6ba4d3b9d616, avg_hours: 300.2643055555555556
474. seller_id: 282c7480173bb9c01dd41cc739fec010, avg_hours: 295.9092013888888889
475. seller_id: 282f23a9769b2690c5dda22e316f9941, avg_hours: 258.0596355759429154
476. seller_id: 28405831a29823802aa22c084cfd0649, avg_hours: 170.0947222222222222
477. seller_id: 28872dc528e978a639754bc8c2ce5a4c, avg_hours: 96.5591666666666667
478. seller_id: 289cdb325fb7e7f891c38608bf9e0962, avg_hours: 149.0191288888888889
479. seller_id: 28a26ebce31d5918b181ede016fd693b, avg_hours: 265.4613888888888889
480. seller_id: 28c7d8743fbc8679f484868cc0fcaefb, avg_hours: 324.1021296296296296
481. seller_id: 28d162ab86bb49d719c32f0ee6186eaa, avg_hours: 393.0822222222222222
482. seller_id: 28ea411b354f14b1a494be4e79f0ce02, avg_hours: 213.4663888888888889
483. seller_id: 28f10b1c5e5abb9d4857745bede6147c, avg_hours: 175.7384821428571429
484. seller_id: 28fb0829fd777877cdc350d25cb5bd5b, avg_hours: 337.7498611111111111
485. seller_id: 293dee954235e4e4e43f129313625ebe, avg_hours: 329.7767708333333334
486. seller_id: 2953ce3a88f5e3c3b696d77fc9e4c8eb, avg_hours: 184.4479814814814815
487. seller_id: 296729ffb9b684050dd24836dac4494a, avg_hours: 158.0550000000000000
488. seller_id: 297d5eccd19fa9a83b2630071ff105e4, avg_hours: 148.6204166666666667
489. seller_id: 299c89a525fee36c567f4fe72f038100, avg_hours: 223.5186111111111111
490. seller_id: 29c322e3f09f886f8bacbe91dfbd979e, avg_hours: 129.5080555555555556
491. seller_id: 29e6e05b65f93bc224c644319dc52ecf, avg_hours: 165.7959027777777778
492. seller_id: 29fe9f200d3fa0c668d2aa1ec7e08dfb, avg_hours: 257.7861111111111111
493. seller_id: 2a1348e9addc1af5aaa619b1a3679d6b, avg_hours: 645.3683823529411765
494. seller_id: 2a167ca73899c85001a837d8fb4962f6, avg_hours: 177.3787037037037037
495. seller_id: 2a261b5b644fa05f4f2700eb93544f2c, avg_hours: 334.5855284552845529
496. seller_id: 2a50b7ee5aebecc6fd0ff9784a4747d6, avg_hours: 953.4758333333333333
497. seller_id: 2a5b78b41cd05baeac8df54c6606b92c, avg_hours: 215.9374305555555556
498. seller_id: 2a61c271b1ac763450d846849783e922, avg_hours: 466.4272101449275362
499. seller_id: 2a6fbeaa7ab9e5d59a35841a8da71ce4, avg_hours: 342.8607685185185185
500. seller_id: 2a73cba571d90c694b7caca072ccf6ce, avg_hours: 494.8061111111111111
501. seller_id: 2a7c6c0b0d5efde2bf75ec1e1cec2d41, avg_hours: 236.5400925925925926
502. seller_id: 2a7dc43cecabf23403078e2188437d1d, avg_hours: 301.6736111111111111
503. seller_id: 2a84855fd20af891be03bc5924d2b453, avg_hours: 195.3378022361984626
504. seller_id: 2aa3443d7bf9d9bb11133f420d75e083, avg_hours: 249.7006111111111111
505. seller_id: 2aafae69bf4c41fbd94053d9413e87ee, avg_hours: 196.1275000000000000
506. seller_id: 2addf05f476d0637864454e93ba673d5, avg_hours: 245.0999305555555556
507. seller_id: 2b03ac196f5ed62ac483960fe0fa3b65, avg_hours: 306.9323015873015873
508. seller_id: 2b1a40c1daabc6ca280c4b815c101841, avg_hours: 324.2462710437710438
509. seller_id: 2b2fed75b8e5ea3a052fc4c0825da485, avg_hours: 93.3460416666666667
510. seller_id: 2b3b9ce054da76a7428df143a567b156, avg_hours: 158.5059259259259259
511. seller_id: 2b3e4a2a3ea8e01938cabda2a3e5cc79, avg_hours: 192.2656172839506173
512. seller_id: 2b402d5dc42554061f8ea98d1916f148, avg_hours: 143.7883333333333333
513. seller_id: 2b5ed0c9139dae8883a200dfcb272ece, avg_hours: 395.0967361111111111
514. seller_id: 2ba91c7ad80ff88b23b7db823b43c233, avg_hours: 441.1811574074074074
515. seller_id: 2bd05d410a8fd26dc4184a15f4f2f588, avg_hours: 213.2256746031746032
516. seller_id: 2bdb95a56a36ebbc6640337ac5eac174, avg_hours: 61.8908333333333333
517. seller_id: 2be17df1c49978426251562096c3cc09, avg_hours: 288.5206250000000000
518. seller_id: 2bf28e311bba65237358230cabac3f15, avg_hours: 254.7890277777777778
519. seller_id: 2bf6a2c1e71bbd29a4ad64e6d3c3629f, avg_hours: 306.2128673835125448
520. seller_id: 2c00c85d30361cd2ced2969cffbbffa3, avg_hours: 44.5825000000000000
521. seller_id: 2c2c9832d1bb38c5b0034a3b47d313ee, avg_hours: 290.0588888888888889
522. seller_id: 2c3d56f92f360fb89d849b84e8f50eae, avg_hours: 319.0681746031746032
523. seller_id: 2c43fb513632d29b3b58df74816f1b06, avg_hours: 105.3942592592592593
524. seller_id: 2c4c47cb51acd5ea5db5e0ae0e26542a, avg_hours: 244.8505555555555555
525. seller_id: 2c538755f1ca9540af144f266e70df6c, avg_hours: 157.1469444444444444
526. seller_id: 2c54051840f19eca309a5423cf22df36, avg_hours: 214.0747222222222223
527. seller_id: 2c9005d8043aff18b8557ffb7b13cda4, avg_hours: 167.6013888888888889
528. seller_id: 2c9e548be18521d1c43cde1c582c6de8, avg_hours: 319.8457716049382716
529. seller_id: 2cb4700db635baa1c0d4f90ed27b6669, avg_hours: 395.6012500000000000
530. seller_id: 2cb6eb1b7185064167657fa09f541105, avg_hours: 194.3107142857142857
531. seller_id: 2cb98e27ce1c18abdb42209b34c382a7, avg_hours: 457.1052777777777778
532. seller_id: 2d20f1cd18725c91147da0791d498022, avg_hours: 238.5883333333333333
533. seller_id: 2d22fc3089eb907b29ebff50581fb472, avg_hours: 230.2257407407407407
534. seller_id: 2d2322d842118867781fc737e96d59a1, avg_hours: 146.7249444444444445
535. seller_id: 2d2c62bef4c8ba0dd74e0e228e808539, avg_hours: 244.9789930555555556
536. seller_id: 2d34636518ba88f5349b732fcf8ba2e4, avg_hours: 253.1536111111111111
537. seller_id: 2d378dbb39815785238c0139c7647fb7, avg_hours: 404.9147222222222223
538. seller_id: 2d42ebcda99fd55f6f4bc2f1ca035d50, avg_hours: 224.9672727272727273
539. seller_id: 2d50d6282f8aa2257819a77bfaa0efe0, avg_hours: 319.0627777777777778
540. seller_id: 2d518637f53161b973e01f56ea4bb88e, avg_hours: 312.3086111111111111
541. seller_id: 2d8cfba3fcd3170555941605edaa196a, avg_hours: 118.8855555555555556
542. seller_id: 2d9e8987a2ea5cf88dce330249043ff1, avg_hours: 213.1050000000000000
543. seller_id: 2dcf93836ae3ce0d7c93e2f10876467a, avg_hours: 148.2187731481481481
544. seller_id: 2dd1fb6f0e42a2243b8a01e40cd41216, avg_hours: 361.1969444444444445
545. seller_id: 2dee2ce60de9709b1a24083217181a1f, avg_hours: 336.1009949494949495
546. seller_id: 2e0dba2da448400b1c11d7b4b22f32a4, avg_hours: 190.5541025641025641
547. seller_id: 2e13c71026e1a39ba5cc1b86dcb679aa, avg_hours: 240.5969246031746032
548. seller_id: 2e1a7d075abe038c1b2743005fe42ff1, avg_hours: 350.2698484848484849
549. seller_id: 2e1c9f22be269ef4643f826c9e650a52, avg_hours: 226.5610512308715902
550. seller_id: 2e2f44824ab87a0cb961f68bf4073e7f, avg_hours: 232.9608333333333333
551. seller_id: 2e3be8a987a30d7544dbbda6861cc14e, avg_hours: 327.4000925925925926
552. seller_id: 2e7ea2aafec5835e781b21d6d1faf1f1, avg_hours: 169.2344444444444444
553. seller_id: 2e90cb1677d35cfe24eef47d441b7c87, avg_hours: 281.5346046228710462
554. seller_id: 2ea0861cc19e94cad86438c984c52da4, avg_hours: 118.4531018518518518
555. seller_id: 2eb70248d66e0e3ef83659f71b244378, avg_hours: 422.3510208685843204
556. seller_id: 2ec6e37d992a95eaddb3369dcbcc76d9, avg_hours: 226.2172222222222223
557. seller_id: 2ee0a0689f2f6a72f35a7cb6033f6e7e, avg_hours: 204.4405555555555556
558. seller_id: 2eeb6531ee027a48d401e72bebdd87d3, avg_hours: 276.6912962962962963
559. seller_id: 2ef086a599b597572aca4433b7ed6b3d, avg_hours: 269.3925000000000000
560. seller_id: 2f09f7d37a97956d11cc1a7cadd5262b, avg_hours: 304.2242013888888889
561. seller_id: 2f1e7b90e01d9f086cbcb301c0c3d406, avg_hours: 170.5152777777777778
562. seller_id: 2f3d8b4c9e2ee165075331fea3f3095a, avg_hours: 295.6600000000000000
563. seller_id: 2f4b0d3b9634b647d4edee577d7ebb7e, avg_hours: 148.1593181818181818
564. seller_id: 2f4b9d112bfa44a214bc6cef085d17c8, avg_hours: 333.4056481481481482
565. seller_id: 2f73e04d12cdf0c945ded66bb3fcf6c7, avg_hours: 317.1714814814814815
566. seller_id: 2f74af7a0ee5636f12c2336f9fffed47, avg_hours: 228.1103846153846154
567. seller_id: 2f9b7ce230a057a98a9f5df5893ee36c, avg_hours: 230.9863888888888889
568. seller_id: 2fa13c8bd5705d279f7ed5cc9ec61c68, avg_hours: 122.6258333333333334
569. seller_id: 2fb25ab44bdbeae6a4d816e0d0c9d500, avg_hours: 195.9323888888888889
570. seller_id: 2fdde51ad3e12f297da656d4fbd5d0b5, avg_hours: 358.3418209876543210
571. seller_id: 2ff6b7bff164ef05590a52734e1296da, avg_hours: 276.4287301587301587
572. seller_id: 2ff97219cb8622eaf3cd89b7d9c09824, avg_hours: 197.74711879432624113487
573. seller_id: 3076499bbc033a927bf4a8a41bcf7fd4, avg_hours: 158.3408333333333333
574. seller_id: 3078096983cf766a32a06257648502d1, avg_hours: 281.8651411657559198
575. seller_id: 30829ded4523ab9224b93bc49a62c95f, avg_hours: 241.5558781362007169
576. seller_id: 3092c0b297aacfb4bb6e056ebe13b9b8, avg_hours: 319.9733823529411765
577. seller_id: 30a2f535bb48308f991d0b9ad4a8c4bb, avg_hours: 192.0340229885057471
578. seller_id: 30a81d8cf85fb2ada1b1b094c9583a95, avg_hours: 87.6618888888888889
579. seller_id: 30c7f28fd3a5897b2c82d152bb760c17, avg_hours: 482.8353703703703704
580. seller_id: 312ba1d77e9c332ef21f9598b7f64cd7, avg_hours: 610.1862301587301587
581. seller_id: 31344c16881c08a8a72c6d2eb29918c1, avg_hours: 365.6355357142857143
582. seller_id: 31561f325664a8a7aba4c8d0c3a9b3db, avg_hours: 167.4184137426900585
583. seller_id: 318f287a62ab7ac10b703ac37435a231, avg_hours: 286.1676639344262295
584. seller_id: 31ae0774c17fabd06ff707cc5bde005f, avg_hours: 264.3691161616161616
585. seller_id: 31be790e64fc99f8ff48ec2bd18a3104, avg_hours: 146.9385185185185186
586. seller_id: 31da954dc0855f2495c6310f70a2f931, avg_hours: 184.4973240740740741
587. seller_id: 31e60bf8d103ce47932a85f5562deb16, avg_hours: 346.7519444444444444
588. seller_id: 31eec405c9bb71dec8e2629a92e764fa, avg_hours: 187.9957222222222222
589. seller_id: 323ce52b5b81df2cd804b017b7f09aa7, avg_hours: 404.7683524904214559
590. seller_id: 324583d68897f5ddbaf38f6248322176, avg_hours: 599.6485185185185185
591. seller_id: 325f3178fb58e2a9778334621eecdbf9, avg_hours: 140.3183152173913044
592. seller_id: 327b89b872c14d1c0be7235ef4871685, avg_hours: 1148.1287962962962963
593. seller_id: 3289d8c3eef4873f91ce0b1343c0dd58, avg_hours: 331.4000000000000000
594. seller_id: 328acb143b4a73aad6bee8e734f5d20d, avg_hours: 288.5911111111111111
595. seller_id: 3296662b1331dea51e744505065ae889, avg_hours: 81.1488888888888889
596. seller_id: 32b8764b4ef628b53608fc34011fcc13, avg_hours: 255.9235672514619883
597. seller_id: 32e5635e63cb374eb63afdd242fb6134, avg_hours: 111.4102777777777778
598. seller_id: 32f1bb9dfa65bc7df5c0d9d95a616be4, avg_hours: 137.5242777777777778
599. seller_id: 32f83ffe11cd40f7adcf4eef171f52d9, avg_hours: 215.3797222222222222
600. seller_id: 32fdd5d44ecb43dfd6a24b9369eca144, avg_hours: 367.7415972222222222
601. seller_id: 3338e7a0710a195872be80e0d2423867
602. seller_id: 333c4210e76a1aa2ab817b99437e3ff1, avg_hours: 171.6383333333333334
603. seller_id: 3340ef1913fb70d28420f6ceb685c339, avg_hours: 363.9309722222222222
604. seller_id: 334cab711dee080b079fa5779b584783, avg_hours: 142.0951495726495727
605. seller_id: 33576ec5412fb5905d876f12f33bfde6, avg_hours: 342.0668402777777778
606. seller_id: 3361277dc30b7cccdb0c286b24219756, avg_hours: 323.8433862433862434
607. seller_id: 3364a91ec4d56c98e44174de954b94f6, avg_hours: 351.6302777777777778
608. seller_id: 33a17d60c64393351ebf1ef860f4e0f2, avg_hours: 246.4833451536643026
609. seller_id: 33a6f4b1e7cdc205511e76ba1b6e0186, avg_hours: 198.49762345679012346102
610. seller_id: 33ab10be054370c254ddfcf0a6253422, avg_hours: 138.7818055555555556
611. seller_id: 33ac3e28642ab8bda860a2f693000e78, avg_hours: 203.6011269841269841
612. seller_id: 33c51922b6e3c16b24a8f28e5833c99d, avg_hours: 346.4316388888888889
613. seller_id: 33cbbec1e7e1044aaf11d152172c776f, avg_hours: 186.1122569444444444
614. seller_id: 33cbda8716511e27e556dff9d8418bf2, avg_hours: 312.0509722222222222
615. seller_id: 33d677f27a69b84051204ee4ae76eaca, avg_hours: 213.3432500000000000
616. seller_id: 33dd941c27854f7625b968cc6195a552, avg_hours: 275.7106666666666667
617. seller_id: 33fd411ed63a7c2f9005e3f065d9f85d, avg_hours: 156.5708333333333333
618. seller_id: 34056b8b55c1775a22af2331670a799c, avg_hours: 297.4363600288600289
619. seller_id: 340636a908b13bbe0f4fb63fbe1d0c03, avg_hours: 168.8413888888888889
620. seller_id: 343e716476e3748b069f980efbaa294e, avg_hours: 370.4561956521739130
621. seller_id: 3442033154be05bac582e173ef54fd12, avg_hours: 93.5066666666666667
622. seller_id: 344223b2a90784f64136a8a5da012e7f, avg_hours: 782.8280555555555556
623. seller_id: 3442f8959a84dea7ee197c632cb2df15, avg_hours: 311.9475925925925926
624. seller_id: 34675b28b826facfde119785bf287dc1, avg_hours: 142.1916666666666667
625. seller_id: 3481aa57cd91f9f9d3fa1fa12d9a3bf7, avg_hours: 225.3837268518518519
626. seller_id: 3492e68f37fd1df87f4f2f2ea247f445, avg_hours: 224.5057407407407407
627. seller_id: 34a557286ead8fe75c989e0afcf7d98c, avg_hours: 187.1853472222222222
628. seller_id: 34aefe746cd81b7f3b23253ea28bef39
629. seller_id: 34d1ca11b242c0fee2c834ae8d788566, avg_hours: 302.2923780487804878
630. seller_id: 34f563c82a85b99ae9e6d60db5fc2e28, avg_hours: 246.1401041666666667
631. seller_id: 3504c0cb71d7fa48d967e0e4c94d59d9, avg_hours: 170.4462106918238994
632. seller_id: 35281d148dcf7134bae913c57db4e6da, avg_hours: 126.4075000000000000
633. seller_id: 353e21e8bf8de2722b4fae1636664b76, avg_hours: 204.4697222222222222
634. seller_id: 35857757f553273b1056c1cabdace7fb, avg_hours: 436.7758796296296296
635. seller_id: 3586b8580d9c917874e053a1bb37b5ff, avg_hours: 318.2569702842377261
636. seller_id: 35b96509602ec4b7da831b5cd73ff2c2, avg_hours: 206.9281944444444445
637. seller_id: 35ef5aa32949680f627efec3c23e705c, avg_hours: 272.2348888888888889
638. seller_id: 35fb511489d9ee3ee27a76debce9df06, avg_hours: 400.7421825396825397
639. seller_id: 3606774ec64634822d78dc2db6d37045, avg_hours: 339.4741666666666667
640. seller_id: 365e445f796710c3431557e85caa25db, avg_hours: 233.1326111111111111
641. seller_id: 365e4bce19bda0082c3d15d83fdb8bcd, avg_hours: 274.4153174603174603
642. seller_id: 36890be00bbfc1cdb9a4a38a6af05a69, avg_hours: 214.0157264957264957
643. seller_id: 36a968b544695394e4e9d7572688598f, avg_hours: 246.0461663105413105
644. seller_id: 36f98ad67cc981f50ce8aed093d5783c, avg_hours: 138.2483333333333334
645. seller_id: 37303482a42fb700d8d127e70a9cd6c8, avg_hours: 48.9433333333333333
646. seller_id: 373ee4a3a775a733770ca3f790b8b9ac, avg_hours: 223.8983459595959596
647. seller_id: 37515688008a7a40ac93e3b2e4ab203f, avg_hours: 349.1994525801952580
648. seller_id: 376a891762bbdecbc02b4b6adec3fdda, avg_hours: 278.2671886973180077
649. seller_id: 376d67b61dce0c990155286e7ae486a4, avg_hours: 343.8836111111111111
650. seller_id: 3771c85bac139d2344864ede5d9341e3, avg_hours: 296.8300092592592593
651. seller_id: 377bc18334c78dd2f1535ef22a3ad225, avg_hours: 237.1086111111111111
652. seller_id: 3785b653b1b82de85ab47dd139938091, avg_hours: 251.5316203703703703
653. seller_id: 37be5a7c751166fbc5f8ccba4119e043, avg_hours: 246.2221093125499600
654. seller_id: 37ceb404da208418c9032f0674e57804
655. seller_id: 37dd29b36c458d82f74a953c40c43645, avg_hours: 448.8197569444444444
656. seller_id: 38102b031c2a15e54623d711bfc753d3, avg_hours: 499.7631666666666667
657. seller_id: 381c83fdca332ea6afd896da20bf6e4a, avg_hours: 298.1597584541062802
658. seller_id: 3820c6537b3853be1a0687d5a60807ec
659. seller_id: 382229d1e840115ffe3dbf5ff460e417, avg_hours: 207.1303472222222222
660. seller_id: 385799a1cddbd26dfeb9157356a42282, avg_hours: 147.1912500000000000
661. seller_id: 38874e327ce94d11390b96eb42d61928, avg_hours: 476.6521296296296296
662. seller_id: 389e45560e33d2d0747f949dcddbc08e, avg_hours: 94.5927777777777778
663. seller_id: 38af8acfd46ac4a7bf754e8ca6736664, avg_hours: 138.6767222222222222
664. seller_id: 38e679b9e0064cd94c6f035707344dae, avg_hours: 255.1208730158730159
665. seller_id: 38e6dada03429a47197d5d584d793b41, avg_hours: 294.9327777777777778
666. seller_id: 38f276ca6e7cc95a6d1bb55ac9e5550f, avg_hours: 124.6391666666666667
667. seller_id: 3903c788ded8dc03b5ebab37a2f3e9a1, avg_hours: 217.2281666666666667
668. seller_id: 391bbd13b6452244774beff1824006ed, avg_hours: 1045.4022222222222222
669. seller_id: 391fc6631aebcf3004804e51b40bcf1e, avg_hours: 333.2811097337006428
670. seller_id: 392353362d22cc2c236e1ee81ff19890, avg_hours: 186.7595277777777778
671. seller_id: 392e0502231ae2f8b29994ef6398cd77, avg_hours: 418.9200490196078431
672. seller_id: 392f7f2c797e4dc077e4311bde2ab8ce, avg_hours: 111.8825000000000000
673. seller_id: 3935fe5fe0f82787a9dcb8deb62be09d, avg_hours: 258.8860294117647059
674. seller_id: 3968920b9aa752ab98f7d5888c9252f2, avg_hours: 197.7800833333333333
675. seller_id: 3969863bb8af7f72580b3b1ffd3a17b3, avg_hours: 232.6540811965811966
676. seller_id: 397c4d0c005b6f41f90098ac724e28cb, avg_hours: 371.3787222222222222
677. seller_id: 3985a3c45be355a4c57fde108bfabd1c, avg_hours: 247.4798263888888889
678. seller_id: 3986c0b54f6b748b75e7bd4e092aa3e5, avg_hours: 146.7091666666666667
679. seller_id: 398cb257329ef7af7f1943a8974a3cbc, avg_hours: 164.8147222222222222
680. seller_id: 39a5005f2605cbdb4f9ac14485cabfd1, avg_hours: 215.5763541666666667
681. seller_id: 39c763cca83e654764b7a4a650fb9b7c, avg_hours: 316.6566161616161616
682. seller_id: 39d54ff918774174706fb065d7f9dc07, avg_hours: 358.8728819444444444
683. seller_id: 39d61be7a92eb77b7da367bd4845bc0e, avg_hours: 243.5073809523809524
684. seller_id: 39f776d2974049026ff531fc42ef2a3e, avg_hours: 363.0765972222222222
685. seller_id: 3a1a1fec38dd360f15fc912e821e169d, avg_hours: 336.3015740740740741
686. seller_id: 3a3c180dd702a725bd0ba4117689239e, avg_hours: 331.5452777777777778
687. seller_id: 3a3e46d10f74d8a6ca76e2b538f106a0, avg_hours: 380.4577222222222222
688. seller_id: 3a4127e1ba7208ea37044c5092aae170, avg_hours: 268.3599444444444444
689. seller_id: 3a490ba60afa30ece0e7d50cfe74a4f0, avg_hours: 285.7894791666666667
690. seller_id: 3a52d63a8f9daf5a28f3626d7eb9bd28, avg_hours: 151.9416666666666667
691. seller_id: 3a734b715d333a2588a3d54a0c9b8746, avg_hours: 266.6237433862433862
692. seller_id: 3a79f35a2344ede41af21267f61d5ec6, avg_hours: 305.9911111111111111
693. seller_id: 3aa3c89ae3cd482385568be76120f63c, avg_hours: 231.6025000000000000
694. seller_id: 3ab971ce71839580d2ae5b4e40fe8044, avg_hours: 151.7631231231231231
695. seller_id: 3ac588cd562971392504a9e17130c40b, avg_hours: 169.7736111111111111
696. seller_id: 3ade81dab5a172b88e1871c28ae05260, avg_hours: 322.7101574074074074
697. seller_id: 3afc536624bc2e65bddfb5db33cc01f3, avg_hours: 223.1795833333333333
698. seller_id: 3b15288545f8928d3e65a8f949a28291, avg_hours: 336.2621516007532957
699. seller_id: 3b18f9856c6eb2413eafedb58e9eecd9, avg_hours: 175.1358333333333333
700. seller_id: 3b872fd4747f01cc56206f2934198618, avg_hours: 331.4322942386831276
701. seller_id: 3bb32fedaa74e4ad20f4ce067733bd31, avg_hours: 139.8813888888888889
702. seller_id: 3bb548e3cb7f70f28e3f11ee9dce0e59, avg_hours: 243.5349685534591195
703. seller_id: 3bdff180c7e1f6551a643b99c265a120, avg_hours: 237.2824185823754789
704. seller_id: 3be5841cdcc46de4ed3f9116f104b2c5, avg_hours: 161.0306250000000000
705. seller_id: 3be634553519fb6536a03e1358e9fdc7, avg_hours: 229.3634444444444444
706. seller_id: 3bfad056cf05c00dabe2f895925d83b1
707. seller_id: 3bfba5a77604f6dfae7e6dd7aaf65821, avg_hours: 212.8034027777777778
708. seller_id: 3c010235b7345c92f125d14ee232a76b, avg_hours: 250.0539074074074074
709. seller_id: 3c03b12bab54d8b37d79d914bfdb1aa0, avg_hours: 322.8736950904392765
710. seller_id: 3c3017960b2dbd72711a61f0400aab8f, avg_hours: 290.3447222222222222
711. seller_id: 3c487ae8f8d7542beff5788e2e0aea83, avg_hours: 311.3281060606060606
712. seller_id: 3c4e0452bff7a2a788179488d3d77032, avg_hours: 317.6040509259259259
713. seller_id: 3c7c4a49ec3c6550809089c6a2ca9370, avg_hours: 218.3556575246132208
714. seller_id: 3c88ed2e76a2247933a15daa7161eb1c, avg_hours: 477.3472222222222222
715. seller_id: 3ca08eeb8d5595949fed424bd3677742, avg_hours: 238.6216452991452991
716. seller_id: 3cfa1358a6caa965278721344c8d76f2, avg_hours: 139.0635000000000000
717. seller_id: 3d01d1c414c44b5943a09619ff3853cb, avg_hours: 306.3153472222222222
718. seller_id: 3d0cd21d41671c46f82cd11176bf7277, avg_hours: 305.9342929292929293
719. seller_id: 3d2400ac620cffa23ac81bd192f7f555, avg_hours: 176.2277777777777778
720. seller_id: 3d2531eccfbde1d7c8db7a3a12fb267a, avg_hours: 221.3937500000000000
721. seller_id: 3d290fe363c60a77498c1126fd3fb8d3, avg_hours: 167.1114814814814815
722. seller_id: 3d39fbf22a665714baf62fae36029e23, avg_hours: 204.2793055555555556
723. seller_id: 3d3ccf2b2f8134b10dce9dd446f0e075, avg_hours: 386.1997222222222222
724. seller_id: 3d4824f20035949c710eaf111f869d39, avg_hours: 215.1905864197530864
725. seller_id: 3d49bfdd1b43a7fe169b3740067acc61, avg_hours: 165.0737962962962963
726. seller_id: 3d4b1ae7539303b5704493798893e82c, avg_hours: 263.8568209876543210
727. seller_id: 3d5d0dc7073a299e31fa718ce1bc00b6, avg_hours: 187.0288510101010101
728. seller_id: 3d621842b2ed28e2b474132480edac3c, avg_hours: 229.4858333333333333
729. seller_id: 3d62f86afa7c73be2628a3be1423f5a0, avg_hours: 395.0894444444444445
730. seller_id: 3d68c634a99a1ba46dbca3967a69c623, avg_hours: 209.6923611111111111
731. seller_id: 3d700782d7818f2c1e0d7a9e9d75fc00, avg_hours: 609.3013888888888889
732. seller_id: 3d871de0142ce09b7081e2b9d1733cb1, avg_hours: 313.2147971313488555
733. seller_id: 3d8fa2f5b647373c8620330c4e077a9f, avg_hours: 216.6512588652482270
734. seller_id: 3da38366e7bd9baf6369071f782ecdf0, avg_hours: 1267.3491666666666667
735. seller_id: 3db66a856d18a9cba7c9241fc5221c50, avg_hours: 368.5371678121420389
736. seller_id: 3dbbce181edfaa4a597ec858c382d2ec, avg_hours: 330.8464166666666667
737. seller_id: 3dc69bf2c42f0568a5c4791ec3fd3745, avg_hours: 630.2900000000000000
738. seller_id: 3ded4e2d5f135cb103e5949d7263d2dd, avg_hours: 107.2766666666666667
739. seller_id: 3df020b72d3d44b3af9d110fa3940b65, avg_hours: 299.6248954895489549
740. seller_id: 3dfd3dc96f7f8598eca74e9ac8a2fa31, avg_hours: 293.1181481481481482
741. seller_id: 3e35a8bb43569389d3cebef0ce820f69, avg_hours: 189.6350000000000000
742. seller_id: 3e46a38ee171c503c3b4a3f23fe3bf0c, avg_hours: 100.1044444444444444
743. seller_id: 3e51f9cbe317bc3a88f2c76583811ee4, avg_hours: 212.7772222222222222
744. seller_id: 3e8bd881d92466e63ba9e3e809cd3c50, avg_hours: 344.7186419753086420
745. seller_id: 3ea00e1dea2b0659dbaf654735929220, avg_hours: 250.5424603174603175
746. seller_id: 3ea08c48e851106d2f584349daba335f, avg_hours: 143.7977777777777778
747. seller_id: 3ef37b7ca6dd2b80bd8af81a62504996, avg_hours: 302.3719444444444445
748. seller_id: 3f0e48d209018b466fcd3bb4ccfeb520, avg_hours: 230.1070000000000000
749. seller_id: 3f2af2670e104d1bcb54022274daeac5, avg_hours: 450.3826190476190476
750. seller_id: 3f3486b61f45078d4f31ee5e43d8c5bb, avg_hours: 322.5907478632478633
751. seller_id: 3f8034bfc6b8b4135534975d49f04c63, avg_hours: 246.9622420634920635
752. seller_id: 3f8247d0f772ffa58560e5c682521ad5
753. seller_id: 3f84fefc07dc159b268d4a77d3e8c425, avg_hours: 191.0251851851851852
754. seller_id: 3f995f07c49d0d55a99d5c54957f7d81, avg_hours: 220.3438307493540052
755. seller_id: 3f9be91358837bff69df67edfa3e42e8, avg_hours: 232.7150000000000000
756. seller_id: 3f9c56764fabca627406093dcb3ef0b4, avg_hours: 192.1831349206349206
757. seller_id: 3fac58ce0ad699020c7944d53c41329c, avg_hours: 95.6318055555555556
758. seller_id: 3fadb4cba4c35bce6a7eaf9872d5623a, avg_hours: 168.9351111111111111
759. seller_id: 3faf68a3b0af94b10bac70d86077be49, avg_hours: 382.6020634920634921
760. seller_id: 3fd1e727ba94cfe122d165e176ce7967, avg_hours: 368.5853317901234568
761. seller_id: 3fe7120d6257285ac6a3ce7cb071ccec, avg_hours: 229.5200000000000000
762. seller_id: 3febca52652e7209509ccfe61cbde40e
763. seller_id: 3fefda3299e6dfaea3466ef346a3571a, avg_hours: 134.8744444444444444
764. seller_id: 4003520d80d0bad1d5623f7aa3c63cda, avg_hours: 409.6633333333333333
765. seller_id: 400f221ab83037c0ea78f1267da9624d
766. seller_id: 402916f742e5c740cc751493d9cf5053, avg_hours: 147.6617777777777778
767. seller_id: 403aa86912527d730337ffcb0fb096ab, avg_hours: 247.0844191919191919
768. seller_id: 4049512728d969bec69f84088b012416, avg_hours: 256.1139814814814815
769. seller_id: 404e1ba01358af4cd63f679b2c4d1fa1, avg_hours: 184.5383101851851852
770. seller_id: 40536e7ca18e1bce252828e5876466cc
771. seller_id: 406740ee611378a662d274c7d8c43c4a, avg_hours: 364.0938333333333333
772. seller_id: 406822777a0b9eb5c50e442dd4cd3ec5, avg_hours: 320.0955797101449275
773. seller_id: 4091f77d8c768fc3e81c20761471761d, avg_hours: 420.1323263888888889
774. seller_id: 40d54b51e962dbe09cabbcfd33298dee, avg_hours: 162.1283154121863799
775. seller_id: 40db9e9aa57f7bb151bcda6b0f9bdbb7, avg_hours: 335.0005324074074074
776. seller_id: 40ec8ab6cdafbcc4f544da38c67da39a, avg_hours: 157.6822222222222222
777. seller_id: 411f3b52d857390502ee4e4d5ceabc2d, avg_hours: 187.2609629629629630
778. seller_id: 4125d9385a25e82d2f72d3a0fd55bc3f, avg_hours: 215.5055555555555556
779. seller_id: 412a4720f3e9431b4afa1476a1acddbe, avg_hours: 236.3365151515151515
780. seller_id: 4170f6a9367e6b5d6401d03ce6d54569, avg_hours: 496.8070000000000000
781. seller_id: 417a1e6c7321084d2a0ae0d023cfad93, avg_hours: 143.7394444444444444
782. seller_id: 41958cbd3335433c8740300e8cd600d5, avg_hours: 115.7116666666666667
783. seller_id: 41ab63a91b8b264e8c8780368bf1dd5b, avg_hours: 411.8138888888888889
784. seller_id: 41b14765bd56c8ad10971074380f9c0c, avg_hours: 161.7994444444444445
785. seller_id: 41b39e28db005d9731d9d485a83b4c38, avg_hours: 290.1618921275535625
786. seller_id: 41b86b552e54e3a7009596125aa8b167, avg_hours: 371.5510858585858586
787. seller_id: 41c2bad7229b0c25e6becf179ebf63ff, avg_hours: 97.6299758454106280
788. seller_id: 41c9d3997dd3c072c31139dc5bb5761f, avg_hours: 513.8848148148148148
789. seller_id: 41da412d33e8da4f22baf55cb1bde82c, avg_hours: 209.5659523809523809
790. seller_id: 41e0fa5761c886a630994a55c12087e7, avg_hours: 229.56250000000000000667
791. seller_id: 4200ddf1967c5e41e48db62bc6d4b5ac, avg_hours: 202.0602116402116402
792. seller_id: 4221a7df464f1fe2955934e30ff3a5a1, avg_hours: 387.0853333333333333
793. seller_id: 422be4cc81a457fdb46f47edeb968ae5, avg_hours: 435.0397222222222222
794. seller_id: 427165bf50f8ca07efc7bdc2bfcf1688, avg_hours: 922.1403333333333333
795. seller_id: 42b6488f5b8246d9141712abd4b1b693, avg_hours: 189.2551388888888889
796. seller_id: 42b729f859728f5079499127a9c2ef37, avg_hours: 179.0698897370653096
797. seller_id: 42bde9fef835393bb8a8849cb6b7f245, avg_hours: 231.5415099715099715
798. seller_id: 42d4b7e70819438f5ada61c965e92d7e, avg_hours: 526.1683333333333333
799. seller_id: 42ef3192a9ff87a22d1867b74b3ee205, avg_hours: 212.5847222222222222
800. seller_id: 42fa4ee7240e9b8eb4576358ec142ba7, avg_hours: 159.8953661616161616
801. seller_id: 42fb44130ac3134cde8e35cf8ec7df25, avg_hours: 141.5995833333333333
802. seller_id: 430315b7bb4b6e4b3c978f9dfa9b0558, avg_hours: 336.6275972222222222
803. seller_id: 4305fe92735c8a43d154ff6dd2b8d927, avg_hours: 263.0720906432748538
804. seller_id: 431050a06a317f2b38168dec3dcd2b46, avg_hours: 211.3684166666666667
805. seller_id: 431af27f296bc6519d890aa5a05fdb11, avg_hours: 397.7222267025089606
806. seller_id: 4324dd16853115efb0fd9d0d131ba6f4, avg_hours: 286.1495370370370371
807. seller_id: 432c37c9dfba871172ec162e20118b8c, avg_hours: 362.1559595959595960
808. seller_id: 432c67955c0acd1fd6b0b5d678766a71, avg_hours: 96.0008333333333333
809. seller_id: 43402bdf22aa2310e8f99e2f94f78628, avg_hours: 370.6935000000000000
810. seller_id: 4342d4b2ba6b161468c63a7e7cfce593, avg_hours: 375.7140277777777778
811. seller_id: 436bf27f2f18474fc6047702e9f8a866, avg_hours: 459.8591666666666667
812. seller_id: 4371b634e0efc0e22b09b52907d9d469, avg_hours: 249.2274774774774775
813. seller_id: 43753b27d77860f1654aa72e251a7878, avg_hours: 589.1347222222222222
814. seller_id: 4391ea5c5990502176a1dcda44a2373d, avg_hours: 225.0519444444444444
815. seller_id: 439a47cc365d6e3bd526812ea9de3c29, avg_hours: 195.0673717948717949
816. seller_id: 43a1d4bab73b816e44ef4e4facd9f9b5, avg_hours: 235.5861111111111111
817. seller_id: 43a5d4a57af536fddc96d08be3afdfcb, avg_hours: 283.2575000000000000
818. seller_id: 43b2c864251aa0ce4030c746984e088a, avg_hours: 134.4031944444444445
819. seller_id: 43f8c9950d11ecd03a0304a49e010da6, avg_hours: 263.5395325203252033
820. seller_id: 44073f8b7e41514de3b7815dd0237f4f, avg_hours: 305.8204139072847682
821. seller_id: 440dd6ab244315c632130ecfb63827b1, avg_hours: 390.8213405797101449
822. seller_id: 443d880f15cbd3572885e1d44bf2c478, avg_hours: 297.4466666666666667
823. seller_id: 4450bd8327d471c4a11a83d1445b1b62, avg_hours: 175.1425000000000000
824. seller_id: 446cc09cdbb130904da114e807dbec40, avg_hours: 89.6058333333333333
825. seller_id: 44717f64ec2a457979cf83c429077666, avg_hours: 105.1848148148148148
826. seller_id: 447d377bdb757058acb569025ee18a93, avg_hours: 431.1758333333333333
827. seller_id: 44ed138eca6214d572ce1d813fb0049b, avg_hours: 205.6674074074074074
828. seller_id: 44f091b5abab8018f682fce8124b85e5, avg_hours: 351.6611111111111111
829. seller_id: 45213867cefbf2cd4c6177e10216a951, avg_hours: 343.1648015873015873
830. seller_id: 4559697a8f7e637227c2eeaed843baff, avg_hours: 301.7886538461538462
831. seller_id: 455befea1bb853c75ccbca94cff26e5c, avg_hours: 255.9808333333333333
832. seller_id: 455c5640e8c5bd1b2ee85c0158f85727, avg_hours: 341.4989236111111111
833. seller_id: 455f46ef09a9e45667e2981df84b5cc2, avg_hours: 311.4058333333333333
834. seller_id: 457fe919b032a3f7dadba6fb92cf7855, avg_hours: 142.5411805555555555
835. seller_id: 458c6fa920810ce2492da71bc26d9eec, avg_hours: 609.2861111111111111
836. seller_id: 458d868c9642f55f18f04e951a3fdde6, avg_hours: 422.4102777777777778
837. seller_id: 45a3d05fb00435e52a28859dd03703b3, avg_hours: 604.3805555555555556
838. seller_id: 45ba18c210d42734ec52c0c1c574e9ee, avg_hours: 149.1296198830409357
839. seller_id: 45c20d94d9171b0bcfab3c955e47d67b, avg_hours: 344.6977777777777778
840. seller_id: 45d33f715e24d15a6ccf5c17b3a23e3c, avg_hours: 264.1054549808429119
841. seller_id: 461ff5303b6c9c1a4a07f40c5aece516, avg_hours: 150.2474074074074074
842. seller_id: 466222e777149751370e7e98fb623b0c, avg_hours: 163.7225000000000000
843. seller_id: 4677a5437afda5fa7140b927b07be1cc, avg_hours: 288.8734595959595960
844. seller_id: 46dc3b2cc0980fb8ec44634e21d2718e, avg_hours: 276.0659467769296014
845. seller_id: 46ef1a25845fc051c2998d878354810c, avg_hours: 404.0463888888888889
846. seller_id: 4736e9d642ef4257cd7622516931eb51, avg_hours: 101.6241527777777778
847. seller_id: 47648caee88ccfe951fbb27fbf7b4cbe, avg_hours: 321.6624074074074074
848. seller_id: 478bfe564db21eeb44386606aa30b650, avg_hours: 335.1687962962962963
849. seller_id: 47efca563408aae19bb7206c2d969ea9, avg_hours: 324.6327777777777778
850. seller_id: 47f55702f598c7c6cc8458b0fbc1c49a, avg_hours: 414.7136111111111111
851. seller_id: 48162d548f5b1b11b9d29d1e01f75a61, avg_hours: 256.2619444444444444
852. seller_id: 4830e40640734fc1c52cd21127c341d4, avg_hours: 231.5535600104821803
853. seller_id: 48328ec9a579151d9cc6a86d4a59336c, avg_hours: 509.2302777777777778
854. seller_id: 483ca627d131e18f988349b1655c0acd, avg_hours: 322.0216666666666667
855. seller_id: 48436dade18ac8b2bce089ec2a041202, avg_hours: 331.7585619803476946
856. seller_id: 485452467ff670447e84a8370c3fc898, avg_hours: 340.9579629629629630
857. seller_id: 4867209cb29b56b92893d7bde3ce8012, avg_hours: 245.2650000000000000
858. seller_id: 4869f7a5dfa277a7dca6462dcf3b52b2, avg_hours: 350.3239626887340302
859. seller_id: 48985c61529077fa4f1e38bcff0f2ed3, avg_hours: 245.9295238095238095
860. seller_id: 48b6c3f4c6a93171da04b75313f2130f, avg_hours: 578.8138888888888889
861. seller_id: 48bad451945f5227341793478d6353ea, avg_hours: 525.6347222222222222
862. seller_id: 48e5ee06fb2dc74df1c711a9b6dfac2a, avg_hours: 269.4758333333333333
863. seller_id: 48e954b2da4f6a750c844173b347ed40, avg_hours: 191.6143055555555555
864. seller_id: 48efc9d94a9834137efd9ea76b065a38, avg_hours: 228.3149264705882353
865. seller_id: 48fb026ed7455a42f5d3e9390ed5088e, avg_hours: 277.9260802469135803
866. seller_id: 49067458c68f7701fd334ce326accbe0, avg_hours: 280.9198198198198198
867. seller_id: 4917cee8d902e13428c3ec4b1ca6f315, avg_hours: 426.2629390681003584
868. seller_id: 491a5ada3aa1678414e990262c4bbdc1, avg_hours: 156.1416666666666667
869. seller_id: 49383af7ab774e4e8f3000f49c83dc4b, avg_hours: 184.3314814814814815
870. seller_id: 4965a7002cca77301c82d3f91b82e1a9, avg_hours: 69.2547222222222222
871. seller_id: 497709c2976a8fa308730a2dec5b0726, avg_hours: 142.5305555555555556
872. seller_id: 4978a02ea9c8be7a9b5480680f40334e, avg_hours: 113.89589181286549707836
873. seller_id: 499185655c29ecfdbfe776ef7cf875b5, avg_hours: 266.6447222222222222
874. seller_id: 4992e76a42cb3aad7a7047e0d3d7e729, avg_hours: 182.9063698630136986
875. seller_id: 499ec63c58e51296c9cf57edcfe1c8a8, avg_hours: 124.9248888888888889
876. seller_id: 49cdc90518a4f82676b38b3c1aa43ff6, avg_hours: 130.3388888888888889
877. seller_id: 49e7217cfe4e427191c378ec626d8737, avg_hours: 382.1375427350427350
878. seller_id: 49f8d2ea7b718d0ce587d34207caf2b4, avg_hours: 163.8005555555555556
879. seller_id: 4a1917ef994878940e1fb03eeb787ad7, avg_hours: 224.8314814814814815
880. seller_id: 4a1f694197d05fe70026b016a7316b41, avg_hours: 259.4832487922705314
881. seller_id: 4a23adac87cf538689fa600d976f78b2, avg_hours: 205.0656481481481482
882. seller_id: 4a3ca9315b744ce9f8e9374361493884, avg_hours: 336.0589632860156205
883. seller_id: 4a3ccda38b2129705f3fb522db62ca31, avg_hours: 314.1460882800608828
884. seller_id: 4a5b36211b1f51bf7eaa5c10a57fa483, avg_hours: 96.6866666666666667
885. seller_id: 4a82168aaef173cbb6e46ae88728f919, avg_hours: 157.6240972222222222
886. seller_id: 4a82c4af97ffc0fb2dc26bfdc03b1842, avg_hours: 293.4272222222222222
887. seller_id: 4aba391bc3b88717ce08eb11e44937b2, avg_hours: 389.1588789682539683
888. seller_id: 4aba6a02a788d3ec81c03137144d9a80, avg_hours: 316.9761111111111111
889. seller_id: 4b0fdb526525f9890eb145bf1534640e, avg_hours: 207.9628055555555556
890. seller_id: 4b1eaadf791bdbbad8c4a35b65236d52, avg_hours: 540.8370555555555555
891. seller_id: 4b39558c138930b9e5489c93b6df5fe3, avg_hours: 293.2698888888888889
892. seller_id: 4b5f66b7adcf57f1ecc0d3c07dd6b177, avg_hours: 314.7314035087719298
893. seller_id: 4b90495391ac0bd181a80a459df1e718, avg_hours: 267.4216666666666667
894. seller_id: 4b9750c8ad28220fe6702d4ecb7c898f, avg_hours: 218.4060444947209653
895. seller_id: 4b98b0428fc1932cc2514ef9ce2505e6, avg_hours: 541.5223611111111111
896. seller_id: 4ba52dfeba874da5b9ee7b17c7494f04, avg_hours: 246.3801262626262626
897. seller_id: 4bc3d93e4a5f88a598d3d8ce4ae510b3
898. seller_id: 4bcec44888b30ba9001234c534716d3f, avg_hours: 219.5132222222222222
899. seller_id: 4bde6149c15cf7e177b36fa060dd6de8, avg_hours: 254.2676388888888889
900. seller_id: 4be2e7f96b4fd749d52dff41f80e39dd
901. seller_id: 4be6b962d83299498bae2190f95d6566, avg_hours: 175.2953240740740741
902. seller_id: 4be9ae93c4fc0f41713d71a4194ee1b3, avg_hours: 265.9852777777777778
903. seller_id: 4bf2f4ee540798a61f9636d12cd9cc80, avg_hours: 322.2595462962962963
904. seller_id: 4bf658053d453036c70976bccb2c31b2, avg_hours: 582.7516666666666667
905. seller_id: 4bfc7a4a1cf8d4d2121c27422d9e50b5, avg_hours: 180.5037638888888889
906. seller_id: 4c03b9dd4c11ee2cb35c96c49efc9420, avg_hours: 245.5211631944444444
907. seller_id: 4c18691b6037662be2df78a765d98ab5, avg_hours: 208.3264220563847429
908. seller_id: 4c1c7281388a33dd06daac44f9fadbd1, avg_hours: 202.8947222222222222
909. seller_id: 4c2b230173bb36f9b240f2b8ac11786e, avg_hours: 294.8173291221250405
910. seller_id: 4c498c7345e89aebad651544829beca0, avg_hours: 248.1499645390070922
911. seller_id: 4c4d546adf3c3868fe19c9ec6e9ffda9, avg_hours: 161.4702777777777778
912. seller_id: 4c60877808f4318ef1107fbeb8f89afa, avg_hours: 360.4127777777777778
913. seller_id: 4c61e37f664c3c88aff092aa5ac779d7, avg_hours: 388.3595138888888889
914. seller_id: 4c8545742faaf58fafd5fd14d25d75cf, avg_hours: 238.9294444444444444
915. seller_id: 4c8b8048e33af2bf94f2eb547746a916, avg_hours: 451.6704106280193237
916. seller_id: 4cc43a222a0f94910728b62b97a8c5f8, avg_hours: 339.1605555555555556
917. seller_id: 4cc4fd4fdd406a85bbdc1f824b731bd7, avg_hours: 198.9744444444444444
918. seller_id: 4ce6e5f6c52515177e18c1c9361d8677
919. seller_id: 4ce8b55b4bfa4659184e7becc1fba3f2, avg_hours: 283.5648611111111111
920. seller_id: 4cf490a58259286ada5ba8525ba9e84a, avg_hours: 577.9511507936507936
921. seller_id: 4d0041cdbe51b4617d95c70b19decc74, avg_hours: 170.7099652777777778
922. seller_id: 4d232b78ab7ef10393dc3807d827bc0d, avg_hours: 134.2551111111111111
923. seller_id: 4d600e08ecbe08258c79e536c5a42fee, avg_hours: 304.3363492063492064
924. seller_id: 4d6d651bd7684af3fffabd5f08d12e5a, avg_hours: 304.7925799771493859
925. seller_id: 4d6fb82c629c7a5028bfd973c07b05e0
926. seller_id: 4d8809767a5bafe22909c77951fb6b41
927. seller_id: 4d9fea3499bdc22aa4da4e339365f215, avg_hours: 291.8575000000000000
928. seller_id: 4da0e408c99d2fdc2126dc9fce518060, avg_hours: 213.1250360082304527
929. seller_id: 4dab98ca6cd6d3df586203cefd28a042, avg_hours: 669.7655555555555556
930. seller_id: 4dbd95a08b31ede5c82d3f861cb1ce1a, avg_hours: 295.8416666666666667
931. seller_id: 4dc2e811a1760953cb7c6a590b498943, avg_hours: 159.8313888888888889
932. seller_id: 4dc646b9b9e8e411ef48ba000ea3ac6f, avg_hours: 254.5771111111111111
933. seller_id: 4ddeb3e828550cddc8d45c8bc36ab2d1, avg_hours: 188.8783333333333333
934. seller_id: 4de6e4ba574aa9dfdc824bc44dc47fdd, avg_hours: 216.7467460317460318
935. seller_id: 4deebb3199eeafb282ae33229144f94b, avg_hours: 272.2057777777777778
936. seller_id: 4e06067cc08b3f41d837768d392c3ee3, avg_hours: 218.5448309178743961
937. seller_id: 4e0d109ccfba9a1151c103049880c857, avg_hours: 461.1966666666666667
938. seller_id: 4e17c65a516f69d023a2ae78b84f28d6, avg_hours: 346.7716291291291291
939. seller_id: 4e2627090e6e5b9fabba883a37897683, avg_hours: 94.7388888888888889
940. seller_id: 4e326052e5dbba8adcd512f3450a307e, avg_hours: 459.8235648148148148
941. seller_id: 4e42581f08e8cfc7c090f930bac4552a, avg_hours: 1048.9605555555555556
942. seller_id: 4e480be820e37de1444325ff358c9296, avg_hours: 290.4447222222222222
943. seller_id: 4e5725ba188db8252977a4f0227bd462, avg_hours: 490.3324537037037037
944. seller_id: 4e6015589b781adaa5ce7f1892d06bb1, avg_hours: 139.6693518518518519
945. seller_id: 4e7c18b98d84e05cbae3ff0ff03846c2, avg_hours: 279.1493773946360153
946. seller_id: 4e85b538b0dad58852641540686d0e14, avg_hours: 407.0166666666666667
947. seller_id: 4e8dacf3d38f281ae26c3e0321d92d88, avg_hours: 318.6563888888888889
948. seller_id: 4e922959ae960d389249c378d1c939f5, avg_hours: 340.6029060787244644
949. seller_id: 4e92348462c75b6c842b994ce84a0ed4, avg_hours: 193.8566666666666667
950. seller_id: 4ea2f12dbe91deeacd2c1e74f069a6e6, avg_hours: 184.5106944444444445
951. seller_id: 4eb61f060e7dcc1d5a80d806c35cc541, avg_hours: 145.4934027777777778
952. seller_id: 4ebdc7e6cd6102a022dadc49156d4ea8, avg_hours: 237.0044097222222222
953. seller_id: 4eeb99008a0f59d2c7759c59f9a346eb, avg_hours: 167.7898611111111111
954. seller_id: 4ef4c39cf3c24f326434cf0b2e48046a, avg_hours: 315.4527777777777778
955. seller_id: 4f0d637c1197fd65405ebd755ac9f86b, avg_hours: 112.9045833333333334
956. seller_id: 4f1f1c8666cdb6442f775c4e8caed465, avg_hours: 478.8856944444444445
957. seller_id: 4f40d2ed38d1cc945364a7cd202a82c7
958. seller_id: 4fae87d32467e18eb46e4a76a0a0b9ce, avg_hours: 162.9644444444444444
959. seller_id: 4fb41dff7c50136976d1a5cf004a42e2, avg_hours: 1594.4085185185185185
960. seller_id: 4fe2f67634d00c021aa01f96b6f2d68e, avg_hours: 251.5677777777777778
961. seller_id: 5011f0d93373a4c5753adf58ca77af8d, avg_hours: 349.4108333333333333
962. seller_id: 503c1de08ae81a2d86f17951b204db55, avg_hours: 312.8630176767676768
963. seller_id: 5058e8c1e82653974541e83690655b4a, avg_hours: 617.7570310245310245
964. seller_id: 5075aaa8404020ae6aa8bf4792099b41, avg_hours: 293.3759259259259259
965. seller_id: 50770d25768b0486d89be26afca3108f, avg_hours: 288.8858333333333333
966. seller_id: 508808d438fe2ff972ed13bb8f4a82e2, avg_hours: 108.1995000000000000
967. seller_id: 50a7e551a7b3f8d37cd6e32d8bfbe5ea, avg_hours: 301.8297222222222222
968. seller_id: 50bf89f1349bc0409a268c3a49678009, avg_hours: 206.1366666666666667
969. seller_id: 50c361bcf670d16f6df4d52de3dff924
970. seller_id: 50c9975695009e5e6473912e83a6d1da, avg_hours: 354.9342687908496732
971. seller_id: 51209b446b2073894bdc0face6c73ffc, avg_hours: 238.6869444444444445
972. seller_id: 512d298ac2a96d1931b6bd30aa21f61d, avg_hours: 225.2581712962962963
973. seller_id: 513a54369b6a8a6602fcb0e129c6d78d, avg_hours: 85.2830555555555556
974. seller_id: 5145090ab595c0d0b8557199f5701fbf, avg_hours: 344.4011805555555556
975. seller_id: 5151aea44289d6c6b090ee31c2132508, avg_hours: 411.9643253968253968
976. seller_id: 515d781150feed28a6ac091bb0e3cb8c, avg_hours: 222.6370370370370370
977. seller_id: 5160d23075764e18e07c1f4a87fad743, avg_hours: 217.0964839181286550
978. seller_id: 516e7738bd8f735ac19a010ee5450d8d, avg_hours: 201.9715108401084011
979. seller_id: 51702dc2a3e106c76dbff722b5bf0726, avg_hours: 330.8770436507936508
980. seller_id: 5194c22ed1f616ec0c0f33c571542879, avg_hours: 239.9781250000000000
981. seller_id: 519a7aa428f18d125a283cf8c014fdd6, avg_hours: 179.3162962962962963
982. seller_id: 51a04a8a6bdcb23deccc82b0b80742cf, avg_hours: 847.3688888888888889
983. seller_id: 51e0557bc7b86de13e946c60ee91ce39, avg_hours: 250.2963888888888889
984. seller_id: 51e4e89242cbb846c2deff3dc015650e, avg_hours: 215.8949131944444444
985. seller_id: 51ed72984a04e5dd35c2b27e77179038, avg_hours: 384.1171825396825397
986. seller_id: 51f108f62cb87d61918159902c8f8583, avg_hours: 133.8884259259259259
987. seller_id: 5206cc4bc2297c833e6061c49bf9c43f
988. seller_id: 52092ddbd3a58c450a4459bf051b2287, avg_hours: 309.0619907407407408
989. seller_id: 520b493b57809f446cb0a233bb3e25c7, avg_hours: 166.6279109589041096
990. seller_id: 522620dcb18a6b31cd7bdf73665113a9, avg_hours: 357.4319303995006242
991. seller_id: 5236605f4d4b0b3e4df85b850393fca0, avg_hours: 245.1672777777777778
992. seller_id: 52454f90d4c30c016768db02f88c1a74, avg_hours: 286.4395555555555556
993. seller_id: 52562a9f449c3dc3d53f5f5b9ed74903, avg_hours: 310.8161507936507936
994. seller_id: 525e75a6fb1454a2325ab1734bcec221, avg_hours: 148.5965277777777778
995. seller_id: 5275ca25d0358ca73864e0ae41be1320, avg_hours: 165.7265972222222223
996. seller_id: 527801b552d0077ffd170872eb49683b, avg_hours: 300.5825090579710145
997. seller_id: 52831e5990d0771cb4951d6f12928167, avg_hours: 110.4930555555555556
998. seller_id: 528bcf6680c36dddf07620bd35b33a6f, avg_hours: 480.2869444444444445
999. seller_id: 528ce32f560edd11add4169f6a5b65be, avg_hours: 228.6055555555555556
1000. seller_id: 52956b80ae65fda598f06f6b9943e7a9, avg_hours: 614.3455555555555556
1001. seller_id: 52a50b42accf164f9f019941e5759d9b, avg_hours: 124.9234722222222222
1002. seller_id: 52a52b9f656520e99716f5bc40f661c8, avg_hours: 251.9504513888888889
1003. seller_id: 52ac6f920b7280e4c6d30dd94de6259b, avg_hours: 265.1537698412698413
1004. seller_id: 52b53f7061969fe471d119b6195da864, avg_hours: 42.9958333333333333
1005. seller_id: 52bb00821bcdd358a5a5a27e1f6be5a1, avg_hours: 359.9776388888888889
1006. seller_id: 52d76513f0c4d97f3b99570e2c94ee31, avg_hours: 278.5669543650793651
1007. seller_id: 52f0fe436a347ddad7ed5f9aa4e27eaa, avg_hours: 324.0795767195767196
1008. seller_id: 52f6f9f13ba19504c02781132a049e75, avg_hours: 324.2444444444444444
1009. seller_id: 52f976b17ea7f2f087f56dcc419328f6, avg_hours: 236.6693518518518519
1010. seller_id: 52f9db5cfb423382a2fa5c9e39303202, avg_hours: 218.9134974747474747
1011. seller_id: 5305693ffae2d3463377b1f6fe67b15a, avg_hours: 320.7122222222222222
1012. seller_id: 53088c75f948b48a7ece173ac17f0c12, avg_hours: 262.9017592592592592
1013. seller_id: 530ec6109d11eaaf87999465c6afee01, avg_hours: 245.9744251925192519
1014. seller_id: 53243585a1d6dc2643021fd1853d8905, avg_hours: 309.0656680555555556
1015. seller_id: 53336f97ddbe53e2a617d07b17447b95, avg_hours: 442.1722222222222222
1016. seller_id: 533d46c1b06970e99f09523a61df4972, avg_hours: 377.8675000000000000
1017. seller_id: 5343d0649eca2a983820bfe93fc4d17e, avg_hours: 262.7060580808080808
1018. seller_id: 534a01cc6df1e034e05c32028a291fa2, avg_hours: 248.8456666666666667
1019. seller_id: 535bf14f36346c7f59d87cece104d70c, avg_hours: 77.1441666666666667
1020. seller_id: 537eb890efff034a88679788b647c564, avg_hours: 210.4462589343729695
1021. seller_id: 538caafddff204241cecbf3a02e6b3cf, avg_hours: 406.1827777777777778
1022. seller_id: 539ed9e19811677513447759be5eccfc, avg_hours: 121.3330555555555556
1023. seller_id: 53b0300ca793f9834cd69c0678d35ee8, avg_hours: 139.6883333333333333
1024. seller_id: 53d00c40e32aeb924a84ce72b1af869d, avg_hours: 377.3904084967320261
1025. seller_id: 53e4c6e0f4312d4d2107a8c9cddf45cd, avg_hours: 278.5771999782986111
1026. seller_id: 54065e9aef7e9e9c2dc23b7594db021a, avg_hours: 293.9138194444444444
1027. seller_id: 5415337f1863452476d42d9f14a16a61, avg_hours: 384.8913888888888889
1028. seller_id: 54219883e72aad869adfb2a54b7bfa0f, avg_hours: 398.0625000000000000
1029. seller_id: 542917da124346b47ea1ac79a93ce454, avg_hours: 267.7660694444444444
1030. seller_id: 5444b12c82f21c923f2639ebc722c1ea
1031. seller_id: 544863df86ed3b78a04e0820d41430ee, avg_hours: 53.9969444444444444
1032. seller_id: 54583ab379489add547fe47b628db589, avg_hours: 117.2963888888888889
1033. seller_id: 54965bbe3e4f07ae045b90b0b8541f52, avg_hours: 631.7823868312757202
1034. seller_id: 54a1852d1b8f10312c55e906355666ee, avg_hours: 264.0593798129812981
1035. seller_id: 54aa8463e87776b5612f4bdc4bd5d4de, avg_hours: 308.0813095238095238
1036. seller_id: 54c04bdb5ec46762f8f08c7e8f86ed4a, avg_hours: 361.7822222222222222
1037. seller_id: 55029529919c0123526150bd26ca8f20, avg_hours: 194.0932539682539683
1038. seller_id: 553a440137d6e0cf776aee0bb83ac9f5, avg_hours: 551.7013888888888889
1039. seller_id: 5563732abe64c3036cb97ad924128dd1, avg_hours: 261.8104629629629629
1040. seller_id: 5566627eab3fe93fd6ee08798226101a, avg_hours: 204.3097222222222222
1041. seller_id: 556a6409838156ea299c9d1f9e2dde43, avg_hours: 154.1997222222222222
1042. seller_id: 557f22c76691849db52d2abccf0015d0, avg_hours: 331.0217094017094017
1043. seller_id: 5587130f9850696ed7fafbc91c2cee44, avg_hours: 115.5587500000000000
1044. seller_id: 559d56f3b8f0bc2e5a9a62fe2ce2a39f, avg_hours: 294.8922222222222223
1045. seller_id: 55a5b51f93f2b70ea513f5a047b0262a, avg_hours: 321.3420528455284553
1046. seller_id: 55bb6fe5bebe5012e2d7d9928e1128ff, avg_hours: 387.7349826388888889
1047. seller_id: 55c26bcb609f480eb7868594245febb5, avg_hours: 193.7596759259259260
1048. seller_id: 55c96925041a14097b6a7825554f4ad5, avg_hours: 254.9153240740740741
1049. seller_id: 55d3daac7c404d59e51c2aa2f4dc5a23, avg_hours: 184.6324206349206349
1050. seller_id: 55dedd83e501d8248880557d9073cbfd, avg_hours: 101.3742901234567901
1051. seller_id: 55f7a3319d80f7fdf078b8f03e6725fe, avg_hours: 144.9259595959595960
1052. seller_id: 562f8cfc51f265411f487d07e9c40e7f, avg_hours: 334.4727777777777778
1053. seller_id: 562fc2f2c2863ab7e79a9e4388a58a14, avg_hours: 256.0163710691823899
1054. seller_id: 5656537e588803a555b8eb41f07a944b, avg_hours: 263.7153213213213213
1055. seller_id: 5659d77e8d90378e39b960ad5956f64e, avg_hours: 486.9340277777777778
1056. seller_id: 56642bcb79900e777d68e91915cb4267, avg_hours: 331.8579315476190476
1057. seller_id: 5670f4db5b62c43d542e1b2d56b0cf7c, avg_hours: 188.2767045454545454
1058. seller_id: 56a8b450e802502ba53a9885ee38e29f
1059. seller_id: 56db5c0782e8f7ddc9343f9576ff6d16, avg_hours: 186.7531944444444445
1060. seller_id: 56e361f411e38dcef17cdc2a3d99628b, avg_hours: 235.2965555555555556
1061. seller_id: 56f413900b5166ab4d730e9ac0b12cb0, avg_hours: 239.3100925925925926
1062. seller_id: 570d4583587a5fe2d47c7be89b91ad27, avg_hours: 137.7643055555555556
1063. seller_id: 5721089ba9214e80074f27d5a03fc0eb, avg_hours: 174.2383333333333333
1064. seller_id: 5733d806668f8712c24b9abaefbfa642, avg_hours: 347.9352777777777778
1065. seller_id: 5741dc2bf5044c34d0698681c5081bed, avg_hours: 172.2595370370370370
1066. seller_id: 575df70bde3f9f2b30bf8d2e9910d725, avg_hours: 304.8148120915032680
1067. seller_id: 577719699805dd125d5b6fdde5943bba, avg_hours: 231.3072916666666667
1068. seller_id: 578460d8319c51dab351cd9db95eadfe
1069. seller_id: 578fa3a9cb6b6dceab39231ad59cdaca, avg_hours: 532.6425000000000000
1070. seller_id: 5795aebfe331fbcd02a2c4b679fb7952, avg_hours: 268.7801388888888889
1071. seller_id: 579891617139df7d8671d373f0669622, avg_hours: 420.3177430555555556
1072. seller_id: 57a834594e1e9e9219603bfec184eadc, avg_hours: 146.4027777777777778
1073. seller_id: 57c764b4a836300be881e2ff86e449f9, avg_hours: 364.7863409961685824
1074. seller_id: 57d2ba47f7a3209aa347532ae75c1165, avg_hours: 364.3551388888888889
1075. seller_id: 57df9869a600bd6b7c405f2a862eccfb, avg_hours: 167.9888888888888889
1076. seller_id: 57e632711dec9ec14ca7546769483e7e, avg_hours: 249.8103717948717949
1077. seller_id: 57fe6232e67823593374a2281d7a8af8, avg_hours: 215.0340972222222222
1078. seller_id: 582d4f8675b945722eda7c0cb61ba4c7, avg_hours: 244.8970618153364632
1079. seller_id: 585175ec331ea177fa47199e39a6170a, avg_hours: 174.5966666666666667
1080. seller_id: 586a871d4f1221763fddb6ceefdeb95e, avg_hours: 1617.6522222222222222
1081. seller_id: 5882820ef11c4c068eea0677a7a879b4, avg_hours: 357.0826984126984127
1082. seller_id: 5882f40daf39bc2a465e0cb453ddc222
1083. seller_id: 58b98ccb79873e04eac4357cacc590d9
1084. seller_id: 58c851d1a3c7cd3da329eb59453fed44, avg_hours: 68.6973611111111111
1085. seller_id: 58e4b302b54937e55a678c4d15111da4, avg_hours: 147.1288888888888889
1086. seller_id: 58f1a6197ed863543e0136bdedb3fce2, avg_hours: 237.8247997416020672
1087. seller_id: 59417c56835dd8e2e72f91f809cd4092, avg_hours: 287.7289351851851852
1088. seller_id: 594f9aaa48e5bf431f011ddc5669b0d5, avg_hours: 183.9647733918128655
1089. seller_id: 5962468f885ea01a1b6a97a218797b0a, avg_hours: 253.5641203703703704
1090. seller_id: 596849622429351f47b32e6cae1055ff, avg_hours: 128.0125641025641026
1091. seller_id: 5996cddab893a4652a15592fb58ab8db, avg_hours: 93.4719444444444444
1092. seller_id: 59b22a78efb79a4797979612b885db36, avg_hours: 288.5270760233918129
1093. seller_id: 59bbc819b99a733f02f0d6b49d1c253d, avg_hours: 113.8841666666666667
1094. seller_id: 59cd88080b93f3c18508673122d26169, avg_hours: 307.4916666666666667
1095. seller_id: 59cea8e446d3834393058e7e0666b6fb, avg_hours: 166.2968055555555556
1096. seller_id: 59de1d4c8c057c2a53acd4ca66531af2, avg_hours: 448.1263888888888889
1097. seller_id: 59fb871bf6f4522a87ba567b42dafecf, avg_hours: 282.1208066666666667
1098. seller_id: 5a05a16bb50629ee31afab8a6d4c2674, avg_hours: 152.9567962962962963
1099. seller_id: 5a32c398a06c345440bf2a683b017ad3, avg_hours: 266.2705555555555556
1100. seller_id: 5a413ade68e8f8d93071a7f52a64cb9e, avg_hours: 88.3416666666666667
1101. seller_id: 5a4236931428800e9d9cc04af0987118, avg_hours: 95.3563888888888889
1102. seller_id: 5a425cc503b39b262a847fd6212bf53b, avg_hours: 157.1408134920634921
1103. seller_id: 5a6a02f419701fc8c605af71d4fc57a4, avg_hours: 106.4089898989898990
1104. seller_id: 5a8e7d5003a1f221f9e1d6e411de7c23, avg_hours: 243.3206641837368094
1105. seller_id: 5a93f3ab0ef4c84ed5e1b5dbf23978bc, avg_hours: 344.7327260981912145
1106. seller_id: 5a9b3bcab695173c820e53934574ae80, avg_hours: 148.5377777777777778
1107. seller_id: 5a9c0859cb00fd8aa4db443837f0a700, avg_hours: 215.9020833333333333
1108. seller_id: 5aaa890629f83706d8d9bfecd8377c1c
1109. seller_id: 5ab05b6d86d417796c69ffd6774ec832, avg_hours: 285.4725694444444444
1110. seller_id: 5abb8ea023c77787f2c15da891c8d384, avg_hours: 446.5641666666666667
1111. seller_id: 5acd070dd3fe441bbb2ec1f1ede515ee, avg_hours: 554.5702083333333333
1112. seller_id: 5b07547f10dd980738a1a27f685af669, avg_hours: 137.8341666666666667
1113. seller_id: 5b0cc932433fa5184b5b94bfe6bcc256, avg_hours: 276.1789052287581699
1114. seller_id: 5b179e9e8cc7ab6fd113a46ca584da81, avg_hours: 292.6294521604938272
1115. seller_id: 5b2e94f2c22b39ccc24d34ad0f669672, avg_hours: 225.8623333333333334
1116. seller_id: 5b33b527da3c5b969cc99dc435cad09a, avg_hours: 295.6140196078431372
1117. seller_id: 5b35136197710e16ac5e7b7c2bd4ea85, avg_hours: 468.6153703703703704
1118. seller_id: 5b51032eddd242adc84c38acab88f23d, avg_hours: 274.8639484126984127
1119. seller_id: 5b581417df4480f632484ba681e53944, avg_hours: 484.7012962962962963
1120. seller_id: 5b664594895aefb418afaee6d40a9a23, avg_hours: 243.6439393939393939
1121. seller_id: 5b67882648febfb6e1225e6ad7164f6b, avg_hours: 282.6491111111111111
1122. seller_id: 5b8154610ebb21fb90eb587365e673df, avg_hours: 307.2965138888888889
1123. seller_id: 5b85809efd0d0e4dea1a9544e1280ed9, avg_hours: 174.1571230158730159
1124. seller_id: 5b925e1d006e9476d738aa200751b73b, avg_hours: 253.0580423280423280
1125. seller_id: 5b92bfa4120daa27c574daa2e386c693, avg_hours: 385.8741666666666667
1126. seller_id: 5b97c06a046398e7005b2b7c0d707a92, avg_hours: 621.1594444444444445
1127. seller_id: 5bba18b40e8c973b0f32e748004775b0, avg_hours: 169.0000000000000000
1128. seller_id: 5bc237df65098fe211bb4818f4d26d78, avg_hours: 259.0804166666666667
1129. seller_id: 5bc24d989e71e93c33e50a7782431b0e, avg_hours: 218.0505882352941176
1130. seller_id: 5bc55dbe2f12b6af6d83ed46023e0dc8, avg_hours: 302.2674074074074074
1131. seller_id: 5bf397d04035b5f45cc41e82ec106803, avg_hours: 83.5669444444444445
1132. seller_id: 5bffbafbb22daf6d3bfc216a46db8708, avg_hours: 196.1988647342995169
1133. seller_id: 5c030029b5916fed0986310385ec9009, avg_hours: 124.0510555555555556
1134. seller_id: 5c243662ce92d84573bfaff24c3e3700, avg_hours: 249.6639111111111111
1135. seller_id: 5c3460cd3e8a984382ae254e7dd20d9f, avg_hours: 227.7159722222222222
1136. seller_id: 5c603ffb38cbbf25a0e0698941324143
1137. seller_id: 5c6d4016c2a288f074fa0848a2b653d2, avg_hours: 252.5222385620915033
1138. seller_id: 5c853bb56f70f4d14218944bae111d7a, avg_hours: 195.4043634259259259
1139. seller_id: 5ca5d579b5857ee8709479b1047cecc3, avg_hours: 426.6891666666666667
1140. seller_id: 5cbbd5a299cab112b7bf23862255e43e, avg_hours: 248.6417324561403509
1141. seller_id: 5cf13accae3222c70a9cac40818ae839, avg_hours: 249.0969677419354839
1142. seller_id: 5cf1ec37aea089f45110c70653a166ab, avg_hours: 481.6138888888888889
1143. seller_id: 5d0363b33554b373851fc1622e4d5f3c, avg_hours: 299.1241932624113475
1144. seller_id: 5d043cd5512d4bd2f88e5ccdd5736c38, avg_hours: 229.7627777777777778
1145. seller_id: 5d378b73ab7dd6f0418d743e5dcb0bd1, avg_hours: 716.2835185185185185
1146. seller_id: 5d3bb11474a06bdc23fb9e89f1164ee0, avg_hours: 225.3732552083333333
1147. seller_id: 5d505d2298ad549e4e4e835562fa0c1e, avg_hours: 141.5222222222222223
1148. seller_id: 5d76d80a2f5f39c891b996a1bf4c9853, avg_hours: 230.3349537037037037
1149. seller_id: 5d9dc90a686a8fddacffab6bab5653a3, avg_hours: 205.7265740740740741
1150. seller_id: 5d9f3746e112e696f98ea22c56b3e912, avg_hours: 169.4416666666666667
1151. seller_id: 5db42a6cd9bf1bf0d3aab9582767f168, avg_hours: 404.6191666666666667
1152. seller_id: 5dc203c7b84a0e71e878a179de05fb9a, avg_hours: 191.4128888888888889
1153. seller_id: 5dc4bdaf869e8c77c648078cbe8d59c2
1154. seller_id: 5dceca129747e92ff8ef7a997dc4f8ca, avg_hours: 258.0449708454810496
1155. seller_id: 5de1c80811ce7007f62f00d971236c09, avg_hours: 168.9826388888888889
1156. seller_id: 5debea795b07621e1f90532e18f96145, avg_hours: 229.6213636363636364
1157. seller_id: 5def4c3732941a971cba8fdee992ede1, avg_hours: 99.2407870370370370
1158. seller_id: 5e063e85d44b0f5c3e6ec3131103a57e, avg_hours: 30.7136111111111111
1159. seller_id: 5e105f5c9f63f5f1fd75d6cb942e55b1, avg_hours: 206.2798263888888889
1160. seller_id: 5e106d93b717c2682b9383da480364a1, avg_hours: 174.0238888888888889
1161. seller_id: 5e25c632f9db6cfb8bc100421c2737b6, avg_hours: 144.7175000000000000
1162. seller_id: 5e49e3a44bdeb5aab2684258bbd4f525, avg_hours: 399.4600000000000000
1163. seller_id: 5e9f5bd34e0830569f05c9d4f56e04a8, avg_hours: 240.3894444444444445
1164. seller_id: 5ee7fd217d08dfe5d3e2f51f96a12c9a, avg_hours: 399.8599074074074074
1165. seller_id: 5eeb9c756d9780b96283e5a2ac6da334, avg_hours: 387.4070061728395062
1166. seller_id: 5ef131ac72773e5b3f6c0d63cf424657, avg_hours: 129.1513131313131313
1167. seller_id: 5f0057b677eb963672bf05dfa3f16c34, avg_hours: 162.7477777777777778
1168. seller_id: 5f06030071324cc52bf0304014ac7234, avg_hours: 242.2325000000000000
1169. seller_id: 5f1dc28029d2c244352a68107ec2b542, avg_hours: 217.0998504273504273
1170. seller_id: 5f2684dab12e59f83bef73ae57724e45, avg_hours: 239.5161643835616438
1171. seller_id: 5f26c1408a65b42a7224cd463bdf3292, avg_hours: 146.2276388888888889
1172. seller_id: 5f3ae9136c875522250f8184f253413a, avg_hours: 178.0374259259259259
1173. seller_id: 5f57db27027655e6c6a391601daa0258, avg_hours: 344.8225000000000000
1174. seller_id: 5f5a58930c3c35f3b5af264f34fb8c85, avg_hours: 179.5689814814814815
1175. seller_id: 5f5b43b2bffa8656e4bc6efeb13cc649, avg_hours: 323.7419061302681992
1176. seller_id: 5f67c6082caacb26e431a7b17940cece, avg_hours: 523.8179960317460318
1177. seller_id: 5f7300535881cef3b625fd683cf7d145, avg_hours: 234.4734595959595960
1178. seller_id: 5fd924b4836098a5be0ecf81ba054ce0, avg_hours: 162.4048809523809524
1179. seller_id: 602044f2c16190c2c6e45eb35c2e21cb, avg_hours: 367.9102474747474747
1180. seller_id: 6025c79c035c3d772133b8b8238463b2, avg_hours: 194.3927777777777778
1181. seller_id: 6039e27294dc75811c0d8a39069f52c0, avg_hours: 412.8307207207207207
1182. seller_id: 60562ab00b8054280520d390c8c0045c, avg_hours: 233.1311274509803921
1183. seller_id: 6061155addc1e54b4cfb51c1c2a32ad8, avg_hours: 118.9497138047138047
1184. seller_id: 606ce7768feac12c5e8bd58db8b08f0f, avg_hours: 223.1744444444444445
1185. seller_id: 609e1a9a6c2539919b8205cf7c4e6ff0, avg_hours: 234.8864209401709402
1186. seller_id: 60ad151920c4f6f3ebbe8cfdf6166779
1187. seller_id: 60da8bfa7eebe230b7d66ac4082d79b3, avg_hours: 183.3245370370370370
1188. seller_id: 610f72e407cdd7caaa2f8167b0163fd8, avg_hours: 288.2097712418300654
1189. seller_id: 612170e34b97004b3ba37eae81836b4c, avg_hours: 253.7691010101010101
1190. seller_id: 612a743d294c27884fb7b80d2b19ba35, avg_hours: 189.0395370370370370
1191. seller_id: 615005a3ef192c00c6f0e977cee3d2bc, avg_hours: 304.3349494949494950
1192. seller_id: 615c3462099ffa940d37b17dfda19594, avg_hours: 183.1423611111111111
1193. seller_id: 6179a28a13a726c29b3bf54c070dccab, avg_hours: 605.2866666666666667
1194. seller_id: 6187a137b2af59dfdbad8d9f8c373c14, avg_hours: 301.2448611111111111
1195. seller_id: 61b18775be84fb700a6b2d0ba097bf66, avg_hours: 284.4713333333333333
1196. seller_id: 61b893c57e33626afb104d4112b1be76
1197. seller_id: 61c36f0fc4a47f9532e5512b66668e62, avg_hours: 294.8291666666666667
1198. seller_id: 61f159ef6da2d441951d2c0efa719362
1199. seller_id: 620c87c171fb2a6dd6e8bb4dec959fc6, avg_hours: 301.0717751458244416
1200. seller_id: 6219ba2359cfb97f2e38fd4c321eb309, avg_hours: 555.6945000000000000
1201. seller_id: 6235903333ba7de1928c869e268e5964, avg_hours: 119.1713888888888889
1202. seller_id: 623ad9d0c1e14bb5464a8c72bff7b4af, avg_hours: 577.7686111111111111
1203. seller_id: 624f4ece8da4aafb77699233d480f8ef, avg_hours: 314.5836985596707819
1204. seller_id: 626ab1cd96932367f0eeec2e47046c12, avg_hours: 149.9574074074074074
1205. seller_id: 62760d278921b5f352461620d68a9cee, avg_hours: 448.3707407407407408
1206. seller_id: 6288c69c4ce638e59925e59193f98b16, avg_hours: 225.0984444444444444
1207. seller_id: 62c50c1af4dfdc4149d25c5222043d39, avg_hours: 321.1757026143790850
1208. seller_id: 62d977e2b2aee830de3e039a28490d12
1209. seller_id: 62de60d81c55c29d76a6bce418b31cef, avg_hours: 356.0580555555555556
1210. seller_id: 630008e0f062605a415d694489f6f82e, avg_hours: 407.3233333333333333
1211. seller_id: 63191ead8d3b2f937cd1996fdcbbad20, avg_hours: 285.8438888888888889
1212. seller_id: 63272377184e969942f7fff221be858d, avg_hours: 294.9980555555555556
1213. seller_id: 6338ea67c41078a46ad99cc009654956, avg_hours: 304.7895517676767677
1214. seller_id: 633ecdf879b94b5337cca303328e4a25, avg_hours: 614.8669444444444445
1215. seller_id: 634964b17796e64304cadf1ad3050fb7, avg_hours: 330.2351049191606467
1216. seller_id: 63704069d9bd3a75c1cf59babe56004a, avg_hours: 423.6700000000000000
1217. seller_id: 638cba8be1fb599bbb76fd6948351eb3, avg_hours: 191.0052525252525253
1218. seller_id: 63a79f5a7eb5cb48a7e5787b141c7993, avg_hours: 136.2411868686868687
1219. seller_id: 63b464dbf392c7b80d12d932fa7cafed, avg_hours: 312.2509210526315789
1220. seller_id: 63b9ae557efed31d1f7687917d248a8d, avg_hours: 383.0113492063492063
1221. seller_id: 63bc58679c44e8a998792119fd7ad23e
1222. seller_id: 63ffcb71394dd8ea3872ed9ffda17c74, avg_hours: 303.3833169934640523
1223. seller_id: 640e21a7d01df7614a3b4923e990d40c, avg_hours: 243.8750857843137255
1224. seller_id: 6426d21aca402a131fc0a5d0960a3c90, avg_hours: 251.1285507246376812
1225. seller_id: 643214e62b870443ccbe55ab29a4dccf, avg_hours: 219.6839941077441077
1226. seller_id: 643c01d7c56a724bec0454f4780e8a3e, avg_hours: 232.8608333333333334
1227. seller_id: 6481e96574816ead57975da2c0f6d80d, avg_hours: 158.75884366925064599690
1228. seller_id: 64b87978a11c1ea7501a89eabe8c2c1a
1229. seller_id: 64c9a1db4e73e19aaafd3286dc448c96, avg_hours: 227.0583333333333333
1230. seller_id: 64cc804291f90c81f02bfc2bb58ff55a, avg_hours: 342.0693055555555556
1231. seller_id: 651530bf5c607240ccdd89a30c9c9712, avg_hours: 282.1097222222222222
1232. seller_id: 651fe66032c9520ee5587f694908040d, avg_hours: 158.6558730158730159
1233. seller_id: 6524b847b982cd56bb5d4b02b776ee42, avg_hours: 971.8038888888888889
1234. seller_id: 6548c2550b6e2d8f18053216e1c7b6f3, avg_hours: 143.3367222222222222
1235. seller_id: 655220df33262c7e0c4949a147366f94, avg_hours: 290.8559444444444444
1236. seller_id: 6560211a19b47992c3666cc44a7e94c0, avg_hours: 219.08579088733021598617
1237. seller_id: 6561d6bf844e464b4019442692b40e02, avg_hours: 34.1288888888888889
1238. seller_id: 6562efe88ce0826a4ca4f189f03b4b84, avg_hours: 372.0902777777777778
1239. seller_id: 656591be56071d4c9ef4e5fee78a578a, avg_hours: 325.2562626262626263
1240. seller_id: 6576fd3e23c88f0e5d4d23f39bba0542
1241. seller_id: 657969cca82e884d272385ec0ef06edd, avg_hours: 152.6888888888888889
1242. seller_id: 659e8466eb3ff1b0e8740d74fb7bbedd, avg_hours: 232.2737301587301587
1243. seller_id: 65a7c0788e4d632ccb5e1b594b87f0bb, avg_hours: 272.0842901234567902
1244. seller_id: 65b081a070633e057c462abdd6fb9dd8, avg_hours: 278.4398888888888889
1245. seller_id: 65c255b299faf2d12050937cc219c46c, avg_hours: 153.2181944444444445
1246. seller_id: 65febd49fd28ec955651299159b1f527, avg_hours: 163.8050292397660819
1247. seller_id: 6601ee6383e7f452be71929f8de48bbb, avg_hours: 345.1745833333333334
1248. seller_id: 6614814a00d344b846ae209f95ee7e3f, avg_hours: 114.7852777777777778
1249. seller_id: 661ad5fcc28cdfb8bcadb12bb2272475, avg_hours: 313.3029365079365079
1250. seller_id: 6624bc09786f0e41ae48dfc5eeb1a9e2, avg_hours: 378.8900000000000000
1251. seller_id: 6650fcccd8cd2f7e55ffa524f30c4c59, avg_hours: 194.9461111111111111
1252. seller_id: 666658b8da8370f30e1f89893b1de5e6
1253. seller_id: 668bf321538e5072858eaef6087ce027, avg_hours: 83.3566666666666667
1254. seller_id: 66922902710d126a0e7d26b0e3805106, avg_hours: 264.1920698924731183
1255. seller_id: 669ae81880e08f269a64487cfb287169, avg_hours: 277.0211576576576577
1256. seller_id: 66d5ae34537110d3affc56174dad2b2f
1257. seller_id: 66dc1b1632bd6a3e508510c5b3492107, avg_hours: 238.6270392953929539
1258. seller_id: 66e0557ecc2b4dbea057e93f215f68d8, avg_hours: 756.7653796296296296
1259. seller_id: 66fd84ee7528c0c0de85d0f44a73d5ab, avg_hours: 321.9522354497354497
1260. seller_id: 670a9dda115b5a88b18cfadee8de2332, avg_hours: 279.7713636363636364
1261. seller_id: 670c26e0f1bf8d0576271d5cfaec6d2b, avg_hours: 324.5561175710594315
1262. seller_id: 671585f5a2af58b6e276bc01003c0d2b, avg_hours: 122.0627469135802469
1263. seller_id: 67225bff54a172ff67579aaf583efd78, avg_hours: 312.1585416666666667
1264. seller_id: 674207551483fec113276b67b0d871ff, avg_hours: 44.6291666666666667
1265. seller_id: 6750d71153f00fc58829af2a8ef1bcf1, avg_hours: 225.1067592592592593
1266. seller_id: 67883baaae6134ee81b271a542613728, avg_hours: 132.5100292397660819
1267. seller_id: 679769a98cfcc6da877c8486ff1c13f3, avg_hours: 218.8976587301587302
1268. seller_id: 67bf6941ba2f1fa1d02c375766bc3e53, avg_hours: 283.5949027777777778
1269. seller_id: 67e43d802fde8cfd3f9580124f8167d1
1270. seller_id: 6806dad1da97bfb5a9038eac6881f706, avg_hours: 314.6957142857142857
1271. seller_id: 681fce914360217db47784ae28905a96, avg_hours: 288.9251967592592593
1272. seller_id: 6824a69c9ea0313eba299dd4a2dba09a, avg_hours: 105.1041269841269841
1273. seller_id: 685b870da5b52a710782c9c0fefbeb5b, avg_hours: 914.6156944444444445
1274. seller_id: 6860153b69cc696d5dcfe1cdaaafcf62, avg_hours: 232.1010912698412698
1275. seller_id: 6861de0f40cacb0602e473c51639f980, avg_hours: 242.6324305555555556
1276. seller_id: 686886775c8f6b1191c7b953fb52708c, avg_hours: 84.6163888888888889
1277. seller_id: 6879c4d287a8dd06b11f54ea8f78e4da, avg_hours: 158.5305555555555556
1278. seller_id: 688756f717c462a206ad854c5027a64a, avg_hours: 246.1686531986531987
1279. seller_id: 68ca56ce86830f3d31b1b7ec6a54da3e, avg_hours: 117.1898888888888889
1280. seller_id: 68f86ba270525243e68ae74044f992b9, avg_hours: 250.3846969696969697
1281. seller_id: 6902157ee16728322d61a1321fa79e58, avg_hours: 236.9597222222222223
1282. seller_id: 693660429f9dc4ff704eb3d88dad54d7, avg_hours: 68.5975000000000000
1283. seller_id: 695051e2981c8b19e77cafe450d5bdf3, avg_hours: 484.3566666666666667
1284. seller_id: 6973a06f484aacf400ece213dbf3d946, avg_hours: 350.1382150205761317
1285. seller_id: 698624c6632eeba1774924dbea24c700, avg_hours: 152.8061111111111111
1286. seller_id: 6989574bd97d9773f10d232b6c07da59, avg_hours: 261.7207936507936508
1287. seller_id: 698f5fa55a5f73d0740e9d9a773e8093, avg_hours: 134.1460185185185185
1288. seller_id: 69a43819c758c65a5befb0b471c954d7, avg_hours: 351.1399074074074074
1289. seller_id: 69b5eaa096c3f9d1e5c398c597f567d6, avg_hours: 145.6379166666666667
1290. seller_id: 6a0cbc8af2e8abd1bdfb777943d174c6, avg_hours: 362.9038398692810458
1291. seller_id: 6a3139c7bf09ece22a4713d956acbe5e, avg_hours: 80.2211111111111111
1292. seller_id: 6a38087bc8ad4f89ff453561005f6dea, avg_hours: 275.3363762626262626
1293. seller_id: 6a51fc556dab5f766ced6fbc860bc613, avg_hours: 355.1146774193548387
1294. seller_id: 6a53b90c3ad9e0b56d9fe5c69165fff5, avg_hours: 284.6447222222222222
1295. seller_id: 6a8a889bde935bafa76d7848782dfaf9, avg_hours: 169.72160185185185185593
1296. seller_id: 6a8b085f816a1f75f92dbac6eb545f8f, avg_hours: 335.9402234753550543
1297. seller_id: 6aa3928696eab49a19a466e665a649fd, avg_hours: 195.9288888888888889
1298. seller_id: 6b15924333bd1a741595fe981ea04822, avg_hours: 177.6501190476190476
1299. seller_id: 6b1c4d4d9ccf0be3d8544eb0e71e5318, avg_hours: 266.2191666666666667
1300. seller_id: 6b243f80ed07b10f0e8aa0f21a205f3c, avg_hours: 255.0533520599250936
1301. seller_id: 6b2612338467c08c9b25f0cc55b1578d, avg_hours: 397.2516666666666667
1302. seller_id: 6b333a05bf188ef3e1f1662a86bd9855, avg_hours: 242.2858974358974359
1303. seller_id: 6b3bd31ad8fcda4b2635ec9f3ff2ecdf, avg_hours: 302.6556084656084656
1304. seller_id: 6b536a23086fba0d58c08d68814397f6, avg_hours: 322.1122222222222222
1305. seller_id: 6b803197e03abd5056b4313306b4f29d, avg_hours: 114.4302546296296296
1306. seller_id: 6b89abe95848c850399130d149a39b63, avg_hours: 249.4175694444444445
1307. seller_id: 6b90f847357d8981edd79a1eb1bf0acb, avg_hours: 120.4515780141843972
1308. seller_id: 6b9b80d53ba3676eafe60268a810b5a1, avg_hours: 287.6824382716049383
1309. seller_id: 6ba4733aa33f6386e9fb0c0fd3993b38, avg_hours: 296.8324074074074074
1310. seller_id: 6bb0724edf0b62fb91ac404873a97241, avg_hours: 318.0850000000000000
1311. seller_id: 6bb62a4912377c7bfe7cb17b406bc7e6, avg_hours: 117.2565277777777778
1312. seller_id: 6bb66d9870c2e01c05655c7ed0e7ee13, avg_hours: 184.3417592592592592
1313. seller_id: 6bbcb8924baf70b7fe2fe2097e8cd407, avg_hours: 266.9380303030303030
1314. seller_id: 6bcb2352a2a0c38b845f598298ab9d26, avg_hours: 264.6416666666666667
1315. seller_id: 6bd503a8230299c9316fb0f726933927, avg_hours: 201.7725555555555556
1316. seller_id: 6bd69102ab48df500790a8cecfc285c2, avg_hours: 385.1110555555555556
1317. seller_id: 6bef34c5be6f2bbd70aa5165f6df94b1, avg_hours: 373.3713888888888889
1318. seller_id: 6c12e40690c335dbc2f68a4134d30dc1, avg_hours: 320.2884259259259259
1319. seller_id: 6c177e38df6d3f34182b1f1d427231bf, avg_hours: 340.1209567901234568
1320. seller_id: 6c17baf138731a4aaacc3210adf2037b, avg_hours: 167.6867222222222222
1321. seller_id: 6c1b6d0c604b776f844125f911eb7377, avg_hours: 403.8634027777777778
1322. seller_id: 6c6cc59a5c00cacc5054ca06d65cc282, avg_hours: 221.8925000000000000
1323. seller_id: 6c6e3d67f969468f3bfd33f827a31222, avg_hours: 221.0947222222222222
1324. seller_id: 6c77cd583b36a13aacccf2b3ee23e233, avg_hours: 144.4730555555555556
1325. seller_id: 6c7d50c24b3ccd2fd83b44d8bb34e073, avg_hours: 279.4181216931216931
1326. seller_id: 6c9875b2f94ba781186f0c1aed8d1687, avg_hours: 88.1712500000000000
1327. seller_id: 6c99c983ce3b6ba0ab813e6790e81691, avg_hours: 137.4046604938271605
1328. seller_id: 6cd68b3ed6d59aaa9fece558ad360c0a, avg_hours: 243.4173089171974522
1329. seller_id: 6cf476a4ca74498db55cbccdaa9dcfb6, avg_hours: 819.2378703703703704
1330. seller_id: 6d04126aba80df143fd038e711b8fd96, avg_hours: 889.6691666666666667
1331. seller_id: 6d1b9c9579132c87d2703ec38c30f2c5, avg_hours: 215.8293055555555556
1332. seller_id: 6d22a1fcebb6dd08c9cd90b92a93e8d0, avg_hours: 373.5616452991452992
1333. seller_id: 6d2f2e3b539480db1e0842b3a4e32e6e, avg_hours: 134.1427777777777778
1334. seller_id: 6d66611d7c44cc30ce351abc49a68421, avg_hours: 280.1508780332056194
1335. seller_id: 6d7f8d9d594e28796b6b3205b00f459c, avg_hours: 366.7279629629629630
1336. seller_id: 6d803cb79cc31c41c4c789a75933b3c7, avg_hours: 303.5391372053872054
1337. seller_id: 6d988d6174a2c27441597174f8905515, avg_hours: 461.2784661835748792
1338. seller_id: 6da1992f915d77be95d7fa48b36904af, avg_hours: 208.7477469135802469
1339. seller_id: 6dc9bec584588412a6a338830946a3e4, avg_hours: 521.0633333333333333
1340. seller_id: 6dd7dce75cd55c1ce255dc38d9f0cd46, avg_hours: 293.2972222222222222
1341. seller_id: 6ddc28b61be28373b4503a1f61cf98a9, avg_hours: 150.3037373737373737
1342. seller_id: 6df688df543f90e9b38f4319e75a9d88, avg_hours: 193.3852171717171717
1343. seller_id: 6e0908ef4d4efadbc3cc2b74ea477cb0, avg_hours: 262.4619696969696970
1344. seller_id: 6e13dd869aa7185f601c941423abcc8f, avg_hours: 70.8853240740740741
1345. seller_id: 6e1862e15f33d9994bc25922a85e1efc, avg_hours: 78.7766435185185185
1346. seller_id: 6e2d3e2dc84fb30f6078f39dd3bddd6f
1347. seller_id: 6e386f64c84e482f0b9abf960797ee1b, avg_hours: 238.3840421455938697
1348. seller_id: 6e4a902d1054e4e17aa6eab87fac1c75, avg_hours: 149.5348611111111111
1349. seller_id: 6e4f5ff6b086632ba8dcb558fb10249e, avg_hours: 250.8009444444444444
1350. seller_id: 6e85dc5ecd97a61094b89b046a509d8e
1351. seller_id: 6e864f5c4669eff3d98140a07cc50202, avg_hours: 220.3281623931623932
1352. seller_id: 6eb94e1466490d327a09abf8f3552a50, avg_hours: 189.1153395061728395
1353. seller_id: 6ebf4eceee4dd9847201c82e77ef8123, avg_hours: 360.1888888888888889
1354. seller_id: 6ec1a01e866584bb679eb9b098345919, avg_hours: 335.3922132616487455
1355. seller_id: 6edacfd9f9074789dad6d62ba7950b9c, avg_hours: 209.0469405864197531
1356. seller_id: 6ee85be3693ed79a8e80718743d80655, avg_hours: 671.1247777777777778
1357. seller_id: 6eeed17989b0ae47c9f11ece6f38ea90, avg_hours: 139.6299074074074074
1358. seller_id: 6f1a1263039c76e68f40a8e536b1da6a, avg_hours: 601.0487222222222223
1359. seller_id: 6f229cc508fc6915ed5c499efd93baa4, avg_hours: 218.3001984126984127
1360. seller_id: 6f835fd4be26989b1b064399da346143, avg_hours: 152.8319444444444445
1361. seller_id: 6f83d9e4da896daae20b9b6b2d3ff8d2, avg_hours: 356.1428282828282828
1362. seller_id: 6f892e20a171e98efe17fdb971ff319b, avg_hours: 389.6675333333333333
1363. seller_id: 6fa9202c10491e472dffd59a3e82b2a3, avg_hours: 176.5413888888888889
1364. seller_id: 6fc26fe110feebd80a433e1f012a84f9, avg_hours: 266.0275462962962963
1365. seller_id: 6fd52c528dcb38be2eea044946b811f8, avg_hours: 500.8663359788359788
1366. seller_id: 7008613ea464bad5cb9b83456e1e6a8f, avg_hours: 325.7096235380116959
1367. seller_id: 700f03c207639c22d933381ff60b35c2, avg_hours: 714.0288194444444445
1368. seller_id: 70125af26c2d6d4ef401a1d02ae7701f, avg_hours: 234.4254861111111111
1369. seller_id: 70126eecc6aa1274392a1743866e9678, avg_hours: 113.0351851851851852
1370. seller_id: 701938c450705b8ae65fc923b70f35c7, avg_hours: 292.7243468468468469
1371. seller_id: 702835e4b785b67a084280efca355756, avg_hours: 31.8833333333333333
1372. seller_id: 7040e82f899a04d1b434b795a43b4617, avg_hours: 234.0717027902341804
1373. seller_id: 70849ca4f400aaabb62cb7462a6f1428, avg_hours: 246.3192129629629630
1374. seller_id: 709e16e2b25c7474d980076c6bfc4806, avg_hours: 238.9361631944444444
1375. seller_id: 70a12e78e608ac31179aea7f8422044b, avg_hours: 343.3867019263845889
1376. seller_id: 70b52a4cfc823994561b00bad161b4ed, avg_hours: 295.5638055555555556
1377. seller_id: 70bf57d811208f8923b41bbd499a67a4, avg_hours: 113.8335317460317460
1378. seller_id: 70c0fda4c313d87115644d39e62eec60, avg_hours: 175.8602777777777778
1379. seller_id: 70c27847eca8195c983ed7e798c56743, avg_hours: 256.6014880952380952
1380. seller_id: 70c4eedec9cb4a85cda2f3f9673557b4, avg_hours: 167.8558333333333333
1381. seller_id: 70ee69419916dc13e3aed619061f996c, avg_hours: 346.1927777777777778
1382. seller_id: 70eea00b476a314817cefde4aad4f89a, avg_hours: 311.1746726190476190
1383. seller_id: 70f7e8018e3d46c748c92f026aa2585a, avg_hours: 168.4569444444444444
1384. seller_id: 70f84699be677ec988d1fa824aef7d90, avg_hours: 416.6680000000000000
1385. seller_id: 71039d19d4303bf9054d69e9a9236699, avg_hours: 308.2688157894736842
1386. seller_id: 710e3548e02bc1d2831dfc4f1b5b14d4, avg_hours: 333.6344829683698297
1387. seller_id: 71271995e85f5b8530be99ed54a91b89, avg_hours: 274.9415740740740741
1388. seller_id: 712e6ed8aa4aa1fa65dab41fed5737e4, avg_hours: 556.5248039215686275
1389. seller_id: 712efd3b68f9686dc856b84abd0f21ae, avg_hours: 173.5383333333333333
1390. seller_id: 7139dc5186aa238b006e066d8fbab2e4, avg_hours: 330.4614004629629630
1391. seller_id: 713e3a23ca5e47786eb6f0d99f94cfac, avg_hours: 228.0066666666666667
1392. seller_id: 7142540dd4c91e2237acb7e911c4eba2, avg_hours: 344.6196155149051491
1393. seller_id: 714b9a1332840f257b49f476bea4e341, avg_hours: 750.4418981481481482
1394. seller_id: 71592660bbcb6a4664e97b6f8b68babc, avg_hours: 273.0897222222222222
1395. seller_id: 71593c7413973a1e160057b80d4958f6, avg_hours: 202.8482222222222222
1396. seller_id: 715bbd5ba4e6b74cb0d2f29eb45058b0, avg_hours: 274.8108897569444444
1397. seller_id: 7178e1eaa97257d8b6d4b80efd77a025, avg_hours: 170.7616666666666667
1398. seller_id: 7178f9f4dd81dcef02f62acdf8151e01, avg_hours: 358.4959741602067183
1399. seller_id: 717b78b0950b51ed00b1471d858b0edc, avg_hours: 500.8560000000000000
1400. seller_id: 718539d38d07dd351c76db862760e2e2, avg_hours: 188.1468475452196382
1401. seller_id: 71dc18fd8cbf5fd77f45dd8b427abb34, avg_hours: 253.6904629629629630
1402. seller_id: 7202e2ba20579a9bd1acb29e61fe71f6, avg_hours: 302.7951310272536688
1403. seller_id: 720e6cf846ea7572cbb66b743fb91e6c, avg_hours: 387.5119444444444444
1404. seller_id: 7210cd29727d674c00741e5e387b3ccd, avg_hours: 113.0995299145299145
1405. seller_id: 72146da5774cabf2632faedcae097a76, avg_hours: 628.3269907407407407
1406. seller_id: 7238a95bb63ef7e498389fb863b834a1, avg_hours: 177.7798703703703704
1407. seller_id: 7238f877570096ae403c51898fa64566, avg_hours: 213.7404629629629630
1408. seller_id: 723a46b89fd5c3ed78ccdf039e33ac63, avg_hours: 191.5861111111111111
1409. seller_id: 723cd880edaacdb998898b67c8f9da30, avg_hours: 220.0762731481481481
1410. seller_id: 72431a818f97fe6ab9c81eee3e297e54, avg_hours: 297.6413888888888889
1411. seller_id: 725af026f869236a8dd0ceb98564d156, avg_hours: 325.4173888888888889
1412. seller_id: 725c32fa80c2faacc4fc88450d27314e, avg_hours: 219.09504480286738351135
1413. seller_id: 7299e27ed73d2ad986de7f7c77d919fa, avg_hours: 262.7806595282433271
1414. seller_id: 729b2d09b2a0bdab221076327f13d050, avg_hours: 286.3669444444444445
1415. seller_id: 729f06993dac8e860d4f02d7088ca48a, avg_hours: 248.6780260570304818
1416. seller_id: 72bc2cce903c872fe376a8faaa81d237, avg_hours: 200.7157870370370371
1417. seller_id: 72c38a04bd6a1c3dbc5298425a0db86d, avg_hours: 192.8778333333333333
1418. seller_id: 72c5da29406b4234927b81855e7b64f6, avg_hours: 241.9420430107526882
1419. seller_id: 72c73be2b085b9d57650dd53eb2004c9, avg_hours: 415.9802777777777778
1420. seller_id: 730937bf88cb151eb2eb849f642fc213, avg_hours: 162.0961324786324786
1421. seller_id: 7315baebc0572ff220d226283dc66728, avg_hours: 170.8988888888888889
1422. seller_id: 731ef20c231d9a7103a425e83fd91271, avg_hours: 286.6408333333333334
1423. seller_id: 734def04b237117a09321dd6d8f3f2a2, avg_hours: 54.5059722222222222
1424. seller_id: 7354220fb240bde543b3c40c060d41e7, avg_hours: 253.7322222222222222
1425. seller_id: 7357b52d27cbaa90f81a96cbc1279396, avg_hours: 225.8745833333333333
1426. seller_id: 739c7d7be81f63812dea0d1b1451c651, avg_hours: 410.6961111111111111
1427. seller_id: 73a63f72308aa20a46f4b1632018f196, avg_hours: 258.8829047619047619
1428. seller_id: 73b8eb4a9a729d4019b24ed1be748cbf, avg_hours: 98.6970634920634921
1429. seller_id: 73da1880b39c71de2b262bc7720c1494, avg_hours: 155.5613888888888889
1430. seller_id: 740205fedfe4e90ca6857bc77db0f2b4, avg_hours: 83.4855555555555556
1431. seller_id: 7402d13c03a7e91366337cd1de471144, avg_hours: 202.9526851851851852
1432. seller_id: 741f8c587cb4248ebc5b779a0e8e0e51, avg_hours: 303.8027222222222222
1433. seller_id: 744dac408745240a2c2528fb1b6028f3, avg_hours: 260.3204718875502008
1434. seller_id: 74636e24f01da9268b0ed88dacd8513e, avg_hours: 314.7599305555555556
1435. seller_id: 747c1cdcd1737dcfbd1547f6eb6f2cf3, avg_hours: 322.4858333333333333
1436. seller_id: 747e73c01a4593d4cf60dcf970fd2689, avg_hours: 249.0363888888888889
1437. seller_id: 74871d19219c7d518d0090283e03c137, avg_hours: 82.8965079365079365
1438. seller_id: 7494d0dcba8551df6cf37f1b905dc2f7, avg_hours: 140.3219444444444444
1439. seller_id: 749e7cdabbaf72f16677859e27874ba5, avg_hours: 264.7183333333333333
1440. seller_id: 74a9b9bddf14ece02beb81f52c41a88d, avg_hours: 291.5393055555555556
1441. seller_id: 74bafed391319577bce6f4d2acc0589a, avg_hours: 162.5155555555555556
1442. seller_id: 74c7dec0a384d8a05950e629bd23bde9, avg_hours: 269.9184027777777778
1443. seller_id: 750303a20e9c56b2a6bc45cdce0b897d, avg_hours: 317.4774652777777778
1444. seller_id: 751bdc4d83a466c7206cd42e8f426b03, avg_hours: 257.0787173202614379
1445. seller_id: 751e274377499a8503fd6243ad9c56f6, avg_hours: 47.5519444444444444
1446. seller_id: 75745ef7bc7d4f3ea3380f6f5303f514, avg_hours: 123.5275925925925926
1447. seller_id: 7586919161935337bf6b6d7ff5779648, avg_hours: 354.1704475308641975
1448. seller_id: 75a4764c108403a7a0575140cb22287c, avg_hours: 212.7789814814814815
1449. seller_id: 75d34ebb1bd0bd7dde40dd507b8169c3, avg_hours: 378.0273341625207297
1450. seller_id: 75fbb52eda0cbc24f479d3b2fbfa8d3e, avg_hours: 326.4445392953929539
1451. seller_id: 75fdd0a732287f9497b179f6bd445d32, avg_hours: 261.0277777777777778
1452. seller_id: 761681a821d8275bc79f552116d06869, avg_hours: 183.2926851851851852
1453. seller_id: 762ed976527cddf02787edba70fffa2a, avg_hours: 184.9331250000000000
1454. seller_id: 762fafdaa57a532ee0119731697579dd, avg_hours: 98.2812222222222222
1455. seller_id: 76623fde66e6b63b59440fd34160512d, avg_hours: 81.2018518518518518
1456. seller_id: 7681ef142fd2c19048da7430856b5588, avg_hours: 232.3751900584795322
1457. seller_id: 76833248bbc0e65a0293ec62023e4396, avg_hours: 424.1627777777777778
1458. seller_id: 768a86e36ad6aae3d03ee3c6433d61df, avg_hours: 102.6362908496732026
1459. seller_id: 768de2a4fc06aacecb9a586ccc30746a, avg_hours: 356.0836752136752137
1460. seller_id: 76c47a299e4a8fe992316a85865acbe9, avg_hours: 366.3577500000000000
1461. seller_id: 76d336555bb25f3165d2f0d6da719c40, avg_hours: 275.7097222222222222
1462. seller_id: 76d5af76d0271110f9af36c92573f765, avg_hours: 263.5036469534050179
1463. seller_id: 76d64c4aca3a7baf218bf93ef7fa768d, avg_hours: 250.1188727858293076
1464. seller_id: 76de363de16dacc923eec8daf91df504, avg_hours: 312.6165277777777778
1465. seller_id: 76ea5315acb3f5f7ade3cd261faf922a, avg_hours: 201.5597222222222222
1466. seller_id: 77128dec4bec4878c37ab7d6169d6f26, avg_hours: 287.8191666666666667
1467. seller_id: 7722b1df1b0e383e000397b2c11e3e19, avg_hours: 198.7308969907407407
1468. seller_id: 77530e9772f57a62c906e1c21538ab82, avg_hours: 349.3570946340040828
1469. seller_id: 77714512e8d4dda9c234da8e3faf16e4, avg_hours: 270.0994907407407408
1470. seller_id: 777a0c55737f34ffeb78010f7542ab41, avg_hours: 100.5704629629629630
1471. seller_id: 778323240ce2830d68aab11794e00bfb, avg_hours: 252.8267592592592593
1472. seller_id: 77a515caa36327151d1cc6c32a9f00e1, avg_hours: 233.7048183760683761
1473. seller_id: 77dcbb67ccb3659bd58eaf5661560a30
1474. seller_id: 77e4abfd739aed9c46480f90f81c0eb4, avg_hours: 225.7117901234567901
1475. seller_id: 77fccaae319668a8ab6cd0fd16aec48c, avg_hours: 195.0573842592592593
1476. seller_id: 7813ea3ebd9411dc600b4dd01f7a97b9, avg_hours: 296.1923765432098765
1477. seller_id: 7816cd9c5b1238e320545f5bf7eb80e8, avg_hours: 261.1650000000000000
1478. seller_id: 781a66c0d89e30814d49fe8b5e14cd07, avg_hours: 794.7925000000000000
1479. seller_id: 782f78b632a43875dd5b53e3e49c9564, avg_hours: 237.0080555555555556
1480. seller_id: 784ba75dd9d20200c4caed3d7a77141a, avg_hours: 300.7218308080808081
1481. seller_id: 78744a20ee2f80ba64f6804c25def2b8, avg_hours: 449.7713425925925926
1482. seller_id: 78813699ffac347fe27dba345a5f1551, avg_hours: 216.6397222222222222
1483. seller_id: 788e857f317e53de488d393e65a80f45, avg_hours: 164.4797979797979798
1484. seller_id: 788f22bafdd7ab0e1e79f19db72f16a4, avg_hours: 84.8552777777777778
1485. seller_id: 78a4d36f65a019172c6154468831a69f, avg_hours: 371.9033730158730158
1486. seller_id: 78ba5933c21686d1c2f64669c8c459e7, avg_hours: 156.5677777777777778
1487. seller_id: 78c99c6dff4eeae5be99bf635ed21e3f, avg_hours: 326.6253988603988604
1488. seller_id: 78ef7e885d17f35e2382a47aae8b8cce, avg_hours: 207.7298148148148148
1489. seller_id: 7901646fdd36a55f564ffaf2dbccaaf7, avg_hours: 227.4301851851851852
1490. seller_id: 791cfcfe22fe4a771ece27f90017da92, avg_hours: 640.5466666666666667
1491. seller_id: 79565f7d5603b24ddf07ade262547f2f, avg_hours: 302.1325396825396825
1492. seller_id: 7957cac1a02f45d0a4a7e45626382ec2, avg_hours: 631.4777777777777778
1493. seller_id: 7963e546f34e098b578f9ad102494601, avg_hours: 398.3447222222222222
1494. seller_id: 7994081388d55b9cf976c050653dd359, avg_hours: 311.0555555555555556
1495. seller_id: 7994b065a7ffb14e71c6312cf87b9de2, avg_hours: 208.6588888888888889
1496. seller_id: 79a679c36c08d606b3fd47ead9de109b, avg_hours: 231.7126190476190476
1497. seller_id: 79b93a308a97792cf53ac75f46da00b5, avg_hours: 540.2277777777777778
1498. seller_id: 79ebd9a61bac3eaf882805ed4ecfa12a, avg_hours: 353.0882361111111111
1499. seller_id: 79ed755314cfe6df0daef2c6cd3022cd, avg_hours: 219.1852777777777778
1500. seller_id: 79ee721b6f766066a80264402548d359
1501. seller_id: 7a073a40a9d3f1fee8bc45670ea1e909
1502. seller_id: 7a188843479798ca813108fa7b959286
1503. seller_id: 7a241947449cc45dbfda4f9d0798d9d0, avg_hours: 293.1550799663299663
1504. seller_id: 7a2d2949aea47fab95fd98d6c9f618b1, avg_hours: 260.9747222222222222
1505. seller_id: 7a425d299613df3e613bcf9d2eaf5c49, avg_hours: 278.3381327160493827
1506. seller_id: 7a67c85e85bb2ce8582c35f2203ad736, avg_hours: 257.3842264660493827
1507. seller_id: 7a704e63bb29c446869efde5d57524c8, avg_hours: 180.1127777777777778
1508. seller_id: 7a91bf945c6fae0779f1c61ce97fe45c, avg_hours: 1052.1655555555555556
1509. seller_id: 7a9c12e235c36247c3c81f50d6ea9cea, avg_hours: 295.9686111111111111
1510. seller_id: 7aa4334be125fcdd2ba64b3180029f14, avg_hours: 372.8057454289732771
1511. seller_id: 7aa538dd6e114e503a2e6154ea352253, avg_hours: 190.9883888888888889
1512. seller_id: 7ab0dd5487bab2dc835337b244f689fb, avg_hours: 137.7000000000000000
1513. seller_id: 7ad32824caee82087b3e2e5f33b1bf32, avg_hours: 268.0164969135802469
1514. seller_id: 7ad41305e96a6cab8294cd65891e9a86, avg_hours: 276.9020833333333334
1515. seller_id: 7adbd3210a7b3cc2235e225eef33574d, avg_hours: 195.6041666666666667
1516. seller_id: 7ade73f1b9b4e965f9009a4c3a7e2c15, avg_hours: 223.5603086419753086
1517. seller_id: 7b07b3c7487f0ea825fc6df75abd658b, avg_hours: 221.7380266203703704
1518. seller_id: 7b0df942f46435babab05d49b744b2c4, avg_hours: 252.2007899305555556
1519. seller_id: 7b1222c3624aa89b9558b50a2594188c, avg_hours: 415.1442550505050505
1520. seller_id: 7b3447b497e55af8c15fc7bd89d7b81a, avg_hours: 313.2325000000000000
1521. seller_id: 7b3f6ce5c6c22e9b96e7581ebf0df6e1, avg_hours: 262.6338888888888889
1522. seller_id: 7b7ed56ae755e2880f2b69632e839c1e, avg_hours: 175.0120000000000000
1523. seller_id: 7b7f91e98f8c6def45a1407923304402, avg_hours: 321.0870039682539683
1524. seller_id: 7b8e8ec35bad4b0ef7e3963650b0a87b, avg_hours: 506.2796666666666667
1525. seller_id: 7b98de631987e26dd6d803490c43a13c, avg_hours: 248.5920833333333333
1526. seller_id: 7bac63f6603d382cc8d0832eb6c100a8, avg_hours: 362.9880701754385965
1527. seller_id: 7bb8fac2913a6064ec412e583c6d8b4d, avg_hours: 116.3122222222222222
1528. seller_id: 7bcd7c5f8631701474db233ccf1c094b, avg_hours: 341.4370486111111111
1529. seller_id: 7c1fea10b5b006671d608b1d7c446ec4, avg_hours: 368.3180952380952381
1530. seller_id: 7c4402417d51474d4d0cda9557340e40, avg_hours: 146.8697222222222222
1531. seller_id: 7c4618c82226628831613e95e9c22f44, avg_hours: 253.7764316239316239
1532. seller_id: 7c462184585ae80bd6e5774c62ce50f2, avg_hours: 382.1216666666666667
1533. seller_id: 7c4adcc13272c0e26fa23aac642adb7b, avg_hours: 386.7205555555555556
1534. seller_id: 7c51de0ab286204ce75ff42bf7c10d92, avg_hours: 228.2927777777777778
1535. seller_id: 7c5b05cbdb5542049f38d90d7815b97d, avg_hours: 165.3015579710144928
1536. seller_id: 7c67e1448b00f6e969d365cea6b010ab, avg_hours: 524.2439801148011480
1537. seller_id: 7c9130f5f3729edd32aa059141d92484, avg_hours: 170.8172222222222222
1538. seller_id: 7caa63f175b1cecbfaadd8b5ab9998c7, avg_hours: 51.5719444444444444
1539. seller_id: 7cb946b1ad19faebe28c3e86c2794ec3, avg_hours: 435.3947222222222222
1540. seller_id: 7cf4ea70955b00d6b3c22542598e2715, avg_hours: 155.3888888888888889
1541. seller_id: 7d13fca15225358621be4086e1eb0964, avg_hours: 367.5864064020237400
1542. seller_id: 7d294cf9a6a69dc6a0c3e540fff0e039, avg_hours: 208.1282222222222222
1543. seller_id: 7d456afc660226829370f3173d14520c, avg_hours: 209.0923907615480649
1544. seller_id: 7d484ca289afaac6bf5fc6a1e96d2226, avg_hours: 271.9959722222222222
1545. seller_id: 7d76b645482be4a332374e8223836592, avg_hours: 307.6920309653916211
1546. seller_id: 7d7866a99a8656a42c7ff6352a433410, avg_hours: 101.1242777777777778
1547. seller_id: 7d7d2b7a51328016102d4528c411d630, avg_hours: 225.5557936507936508
1548. seller_id: 7d81e74a4755b552267cd5e081563028, avg_hours: 50.7136111111111111
1549. seller_id: 7d948535954aaf8c5d39db007f74372e, avg_hours: 119.5522916666666667
1550. seller_id: 7daca0837f033a41a6f3428c18657533, avg_hours: 315.3001984126984127
1551. seller_id: 7dc8c42cc750eeafea6c85712ffee9bf, avg_hours: 195.5360500000000000
1552. seller_id: 7dc9a3355bae96dd82008b313d3a456c, avg_hours: 299.4088888888888889
1553. seller_id: 7ddcbb64b5bc1ef36ca8c151f6ec77df, avg_hours: 292.2102852628077179
1554. seller_id: 7dea6f73af847b42cc3985bd620f994d, avg_hours: 126.5850000000000000
1555. seller_id: 7df1fc11cc5cbc518b39faa60cf5d67c, avg_hours: 184.4225555555555555
1556. seller_id: 7e1fb0a3ebfb01ffb3a7dae98bf3238d, avg_hours: 365.4127301117685733
1557. seller_id: 7e26c750b4cb9f6766f58265ff9ebe95, avg_hours: 224.5085596707818930
1558. seller_id: 7e3dde9ffba72d5340f9aaf09b4424be
1559. seller_id: 7e3f87d16fb353f408d467e74fbd8014, avg_hours: 287.9333333333333333
1560. seller_id: 7e79d65b5c6f1f544b7daea036acf720, avg_hours: 194.8152083333333334
1561. seller_id: 7e93a43ef30c4f03f38b393420bc753a, avg_hours: 261.0171256038647343
1562. seller_id: 7e959205cebc10adefcb331f934238a4
1563. seller_id: 7ea5bfa6c340f58f8e71fc1f0412b0d6, avg_hours: 297.6532625272331155
1564. seller_id: 7ecd59e5e20407131822c1a68ac59c1f, avg_hours: 410.0578160919540230
1565. seller_id: 7ecef8194babfec876ca720714327841, avg_hours: 218.7647916666666667
1566. seller_id: 7f02656561b680def9986c0795a8a080, avg_hours: 253.2636111111111111
1567. seller_id: 7f152321c60a266edc53af1925ef96c1, avg_hours: 557.1194583333333333
1568. seller_id: 7f2617c58d5d06806987308b45654351, avg_hours: 287.8938164251207729
1569. seller_id: 7f35f9daf223da737b78738fbae4d977, avg_hours: 184.0645000000000000
1570. seller_id: 7f40d06aa0b5f1aa4f41af8c0480e2ef, avg_hours: 98.8568518518518519
1571. seller_id: 7f5e4d5efad7e44b91115dd1decb65f3, avg_hours: 112.0078086419753087
1572. seller_id: 7f7b8245c336066a1f9933c359f11d77, avg_hours: 177.1377454780361757
1573. seller_id: 7fc87cc3e89b3d1d5cabdca32f8485aa, avg_hours: 459.9684126984126984
1574. seller_id: 7fdb0720c8d7c9075538b365dc8c3a22, avg_hours: 400.6787777777777778
1575. seller_id: 7fe21dd00d2f4943ae09525efa2fd674, avg_hours: 142.5138888888888889
1576. seller_id: 7ff588a03c2aeae4fbd23f9ae64b760d, avg_hours: 117.9527777777777778
1577. seller_id: 800214c63934acd05d47e84214db8ba8, avg_hours: 282.6719444444444445
1578. seller_id: 80146bc52c4f6af5239b23de2a20262b
1579. seller_id: 804287717b9156fb7a787acd9af4fac1, avg_hours: 218.8141666666666667
1580. seller_id: 8060d731897e33b5c5ae575ce1e209e1, avg_hours: 185.5502777777777778
1581. seller_id: 808d4348b916efa08e766ebad39f61eb, avg_hours: 170.6886250000000000
1582. seller_id: 8090490573c6c0aa343a7231ebcb8c86, avg_hours: 227.9993055555555556
1583. seller_id: 809413606dbfe5deefd2db646693ef67, avg_hours: 179.7970555555555555
1584. seller_id: 80ceebb4ee9b31afb6c6a916a574a1e2, avg_hours: 466.8769444444444444
1585. seller_id: 80cfd480be3eb6d6267139f5cb793555, avg_hours: 342.0994444444444444
1586. seller_id: 80e6699fe29150b372a0c8a1ebf7dcc8, avg_hours: 265.3067182130584192
1587. seller_id: 80f2cf9abf6b5a0e5c612b5eea6646e6, avg_hours: 249.7289351851851852
1588. seller_id: 8132b9bd16876e1b0f8808d43825dd48, avg_hours: 403.3052777777777778
1589. seller_id: 813348c996469b40f2e028d5429d3495, avg_hours: 237.0590854700854701
1590. seller_id: 81336a0f57a33776419727a300249e90, avg_hours: 417.3868055555555556
1591. seller_id: 8160255418d5aaa7dbdc9f4c64ebda44, avg_hours: 394.7641902515723270
1592. seller_id: 817245bcc3badd82bbd222e0366951a6, avg_hours: 256.8596275252525253
1593. seller_id: 81783131d2a97c8d44d406a4be81b5d9, avg_hours: 166.5367283950617284
1594. seller_id: 817f85dbb65aa3e70831d90fe75cdf89, avg_hours: 427.8355303030303030
1595. seller_id: 8185694b58b2ba6de20fd41ae608bbea, avg_hours: 251.7540277777777778
1596. seller_id: 818d28f936e791926d33bcb6ee94ef79, avg_hours: 304.5279861111111111
1597. seller_id: 81a1104df0f08b59c68aa5b03cfe398e, avg_hours: 293.0193287037037037
1598. seller_id: 81ed90f07c0bacb7594940ba2ef676aa, avg_hours: 372.3738888888888889
1599. seller_id: 81f89e42267213cb94da7ddc301651da, avg_hours: 175.4918856837606838
1600. seller_id: 820c7c9eaf76d2b226b6c242bcf3f34d, avg_hours: 391.2094444444444444
1601. seller_id: 820cc752a266cdc6c1a1e61dd4583330, avg_hours: 322.1153333333333333
1602. seller_id: 821fb029fc6e495ca4f08a35d51e53a5, avg_hours: 379.0737666666666667
1603. seller_id: 822166ed1e47908f7cfb49946d03c726, avg_hours: 317.1260005144032922
1604. seller_id: 822b63912576852aea9a8436d72317b7, avg_hours: 493.1612301587301587
1605. seller_id: 822bad9bc42b51213ba522fe87b7ab5d, avg_hours: 627.8857716049382716
1606. seller_id: 827f8f69dfa529c561901c4f2e0f332f, avg_hours: 310.4978285256410256
1607. seller_id: 82921991ff5b557b045605b8bbf08d49, avg_hours: 97.7716666666666667
1608. seller_id: 82bd0703a4aefd6b599e5bfdaed378fb, avg_hours: 280.8326570048309179
1609. seller_id: 82cb9f452fe8334df74b22d37824b431, avg_hours: 203.6469598765432099
1610. seller_id: 82e0a475a88cc9595229d8029273f045, avg_hours: 355.7861322081575246
1611. seller_id: 830379336fad8c6f3b15a4a3ddb5c66e, avg_hours: 110.3550000000000000
1612. seller_id: 83353a83fd769dfafa4f21a72b15e3e5, avg_hours: 435.9823888888888889
1613. seller_id: 834f3294fba9f932f56edc879193f925, avg_hours: 328.5930808080808081
1614. seller_id: 834f8533b2ecb6598dd004ff3de7203a, avg_hours: 351.4160802469135803
1615. seller_id: 835f0f7810c76831d6c7d24c7a646d4d, avg_hours: 437.9100983796296296
1616. seller_id: 83645b1645cdee8953ee54c29ceed564, avg_hours: 246.7283531746031746
1617. seller_id: 8378eb36b6b70c5734e83ad7b8cdc3b7, avg_hours: 460.3478632478632479
1618. seller_id: 83a75eea11694e36e56dd0cb2240229a, avg_hours: 89.9961111111111111
1619. seller_id: 83b08de96980757220871b31bf6cffca, avg_hours: 311.7030555555555556
1620. seller_id: 83c465a786b06574376909b35ef6752a, avg_hours: 123.5131481481481482
1621. seller_id: 83c8aafbefb034674a70de0eac5b8954, avg_hours: 113.6915277777777778
1622. seller_id: 83d458c0d6d4f94295d63f091460bd60
1623. seller_id: 83d7070a0b9a8b4625fa8682b819fabb
1624. seller_id: 83deb69e889cf80f82be1dc6d5f2d486, avg_hours: 365.4028240740740741
1625. seller_id: 83e197e95a1bbabc8c75e883ed016c47, avg_hours: 242.4226903292181070
1626. seller_id: 83f2b4881141ce3fcd4e985125d3279e, avg_hours: 426.6693518518518518
1627. seller_id: 8444e55c1f13cd5c179851e5ca5ebd00, avg_hours: 505.4103322440087146
1628. seller_id: 845e8036c3f7bf62099352f5ed910240, avg_hours: 187.0709606481481481
1629. seller_id: 8476243f92442881ddd5b578975cf115, avg_hours: 407.4809490740740741
1630. seller_id: 84c945f15571830c1a91a33978e94009, avg_hours: 226.4904166666666667
1631. seller_id: 84deb808079d1be601c209c1e771b1cc, avg_hours: 139.0719444444444444
1632. seller_id: 8501d82f68d23148b6d78bb7c4a42037
1633. seller_id: 85044848b1b767db2a4a58526adef4b4, avg_hours: 207.1310416666666667
1634. seller_id: 850857dfac77488c307e2b1cbd84ab5a, avg_hours: 69.8941666666666667
1635. seller_id: 850913d59ce317156b00f3705f1c3edb, avg_hours: 311.7353333333333333
1636. seller_id: 850f4f8af5ea87287ac68de36e29107f, avg_hours: 233.5000407213496219
1637. seller_id: 851773c885feb5e2da3b4f82bc2b17ce, avg_hours: 390.2449166666666667
1638. seller_id: 855668e0971d4dfd7bef1b6a4133b41b, avg_hours: 376.4366291532690247
1639. seller_id: 8581055ce74af1daba164fdbd55a40de, avg_hours: 299.3511293688054251
1640. seller_id: 85cc55e048b6bcc90c75afe7f0e72f72, avg_hours: 295.8575000000000000
1641. seller_id: 85d9eb9ddc5d00ca9336a2219c97bb13, avg_hours: 340.3750569661458333
1642. seller_id: 85e7c62c1d6ea078c3897424f867a7c8, avg_hours: 171.3923611111111111
1643. seller_id: 85ecf03781da592876b7844acc1b729f, avg_hours: 337.1751388888888889
1644. seller_id: 8602a61d680a10a82cceeeda0d99ea3d, avg_hours: 183.7655116959064328
1645. seller_id: 8603f0038fe0e52fedd3382d266723de, avg_hours: 500.5462222222222222
1646. seller_id: 8629a7efec1aab257e58cda559f03ba7, avg_hours: 1421.2138888888888889
1647. seller_id: 8629c241b3622ac12cd4118afdc8d394, avg_hours: 354.3595299145299145
1648. seller_id: 863d2ebcd347ce4922de7a0f9a5581d6, avg_hours: 263.4887808641975309
1649. seller_id: 8648b1e89e9b349e32d3741b30ec737e, avg_hours: 216.4580833333333333
1650. seller_id: 86649b1632b1c0e6c0bcb2c90a8b75d8
1651. seller_id: 866558b3bccef2dbc6d29a2b5995016f, avg_hours: 291.4303703703703704
1652. seller_id: 86bb7c4b535e49a541baf3266b1c95b1, avg_hours: 469.9419965277777778
1653. seller_id: 86bf77bdb52e615674772d5817c6212f, avg_hours: 164.3487222222222222
1654. seller_id: 86ccac0b835037332a596a33b6949ee1, avg_hours: 271.3938221153846154
1655. seller_id: 86ff3eaef0267069cc891a2ed9d10a17, avg_hours: 194.7683730158730159
1656. seller_id: 870d0118f7a9d85960f29ad89d5d989a, avg_hours: 349.4619854280510018
1657. seller_id: 87142160b41353c4e5fca2360caf6f92, avg_hours: 247.2218076040642412
1658. seller_id: 8759e7aedd644f487315e5860962f162, avg_hours: 758.5580555555555556
1659. seller_id: 876182d1918783bbe15233febfbd4926, avg_hours: 203.5299074074074074
1660. seller_id: 87b4428a334b8f676fd9a7f3bf544fb5, avg_hours: 166.1386111111111111
1661. seller_id: 87b740daf17b5d1be335a64164ec6842, avg_hours: 431.4875252525252525
1662. seller_id: 87d30a6a0cbf89356e49324971ab1d24, avg_hours: 261.0868300653594771
1663. seller_id: 87d3c3aeb3ead335511b3ce315eb341e, avg_hours: 144.2802407407407407
1664. seller_id: 87d73636a3acf123e842bb890a4db036, avg_hours: 300.1441666666666667
1665. seller_id: 87e24fc7052259b1f7f607d61c10d8be, avg_hours: 361.5148015873015873
1666. seller_id: 87f3e35268860433e13d577825aada95, avg_hours: 1205.4730555555555556
1667. seller_id: 880ce4951cf857ab1d9e0b75c1d856f4, avg_hours: 360.9586111111111111
1668. seller_id: 880eda903e719a5f179f7e9fceb3a69d
1669. seller_id: 883dd81e82754ac2c65e9790a7db8c9a, avg_hours: 165.7442222222222222
1670. seller_id: 88460e8ebdecbfecb5f9601833981930, avg_hours: 430.1755824074074074
1671. seller_id: 888faa8bfb0b159c37de6d898b961c31, avg_hours: 198.7771497584541063
1672. seller_id: 889009a0ed0bb52c87819941192931b8, avg_hours: 267.8827777777777778
1673. seller_id: 88ae906ea2acf6971f26c3e8b7cb4357, avg_hours: 361.8531481481481482
1674. seller_id: 88af55b4a7ca402b27df16f7c7c9b5d2
1675. seller_id: 88cd3681e0a2ba85e190f7d817629c4c, avg_hours: 168.1358333333333333
1676. seller_id: 88cf19ec1fc2c58f161aee259d57142c, avg_hours: 146.1341269841269841
1677. seller_id: 88ef59b51bdaa941d10a853429f2b6ce, avg_hours: 130.1170833333333333
1678. seller_id: 891071be6ba827b591264c90c2ae8a63, avg_hours: 301.9946141975308642
1679. seller_id: 8931a84a914b3fe9b1ddaa4d704947ca, avg_hours: 299.4315017361111111
1680. seller_id: 8936ba0de1073ee888cb3185ae5dc661, avg_hours: 274.2883333333333333
1681. seller_id: 897060da8b9a21f655304d50fd935913, avg_hours: 344.7818422114608555
1682. seller_id: 89757206b887aed36f3e18d858460fea, avg_hours: 220.8565277777777778
1683. seller_id: 89a51f50b8095ea78d5768f34c13a76f, avg_hours: 162.8665909090909091
1684. seller_id: 89ad3263c0931c47f976d7c5778e60f6, avg_hours: 145.6546296296296296
1685. seller_id: 89bc797e2e29667aa035d4368f9b7f92, avg_hours: 345.7875438596491228
1686. seller_id: 89c127985a8b130cfa45c1d36764017a, avg_hours: 251.8464814814814815
1687. seller_id: 89d9a386b0b6e5fc8403071b03f7206a, avg_hours: 326.8356111111111111
1688. seller_id: 89dda63a3c907c468ec88c310ed91213, avg_hours: 610.3416666666666667
1689. seller_id: 89de2d6f23e9746ff309705b23581faa, avg_hours: 217.0530902777777778
1690. seller_id: 89f69225956f951295ca4c7fb1266553, avg_hours: 227.7626157407407407
1691. seller_id: 8a130737016f838139d31878787a39c9, avg_hours: 234.5141980286738351
1692. seller_id: 8a1ff5c35f6595a73fef4c7b96e4908a, avg_hours: 228.6952777777777778
1693. seller_id: 8a207b6080964f3c1fc9d35bd6096ba4, avg_hours: 493.5859259259259259
1694. seller_id: 8a2d12a90e92f012ce5226fc6592b653, avg_hours: 212.8542129629629630
1695. seller_id: 8a32e327fe2c1b3511609d81aaf9f042, avg_hours: 208.9230144641683103
1696. seller_id: 8a40ae794fa3f9892cee24bd5af0488b, avg_hours: 636.4151388888888889
1697. seller_id: 8a43128d7f9a3db592b866e6861a6cce, avg_hours: 147.6850000000000000
1698. seller_id: 8a432f4e5b471f8da497d7dc517666e2, avg_hours: 180.1447824947589099
1699. seller_id: 8a87611c08849ffeeccab52aa798b6c7, avg_hours: 209.5119907407407408
1700. seller_id: 8a8835a43bda99fd37310ad76c457510, avg_hours: 128.5498148148148148
1701. seller_id: 8a9260f2b0340411d6d2a56bcf4f7378, avg_hours: 211.0046604938271605
1702. seller_id: 8ab42aa58097fd4668d60cc648225d5f, avg_hours: 262.1554914529914530
1703. seller_id: 8ae520247981aa06bc94abddf5f46d34, avg_hours: 253.6953717948717949
1704. seller_id: 8b11118053756a9a2932f447e11fc1b5, avg_hours: 285.2061111111111111
1705. seller_id: 8b181ee5518df84f18f4e1a43fe07923, avg_hours: 349.2308333333333333
1706. seller_id: 8b2492b7ff4468839593fafeed55bad9, avg_hours: 347.4921358024691358
1707. seller_id: 8b28d096634035667e8263d57ba3368c, avg_hours: 332.4328734363502575
1708. seller_id: 8b2d4ab22f42c5cfc338b846decfda60, avg_hours: 286.5609259259259259
1709. seller_id: 8b321bb669392f5163d04c59e235e066, avg_hours: 292.83679629629629629701
1710. seller_id: 8b655f0855926bcb49f5835d38dfddf6, avg_hours: 134.3867222222222222
1711. seller_id: 8b87cd0d43d49b9bdf40f56229364d59, avg_hours: 352.6412500000000000
1712. seller_id: 8b8cfc8305aa441e4239358c9f6f2485, avg_hours: 290.2886851851851852
1713. seller_id: 8b9d6eec4a7eb7d0f9d579ce0b38324d, avg_hours: 233.8109241452991453
1714. seller_id: 8bb48dc19fccaa8613b6229bf7f452a2, avg_hours: 256.0537982456140351
1715. seller_id: 8bd0e3abda539b9479c4b44a691be1ec, avg_hours: 547.5265277777777778
1716. seller_id: 8bd0f31cf0a614c658f6763bd02dea69, avg_hours: 229.1266428571428571
1717. seller_id: 8bdd8e3fd58bafa48af76b2c5fd71974, avg_hours: 246.8541666666666667
1718. seller_id: 8c0de775f52fe41590b376a3b7c50f68, avg_hours: 128.6344444444444444
1719. seller_id: 8c16d1f32a54d92897cc437244442e1b, avg_hours: 251.9235734463276836
1720. seller_id: 8c351ed7c326c62123318f4f3246e906, avg_hours: 215.7569444444444445
1721. seller_id: 8c3b533c63cca56240f94f1e3a6b18ef, avg_hours: 1171.2735000000000000
1722. seller_id: 8c5e007d7bd5693fa1386ffefbc99f6c, avg_hours: 277.8678935185185185
1723. seller_id: 8c91bfea4263b8fba54081460693e2a1, avg_hours: 290.9400000000000000
1724. seller_id: 8c9348f33ae3dada25c99c99ade2af78, avg_hours: 237.8466666666666667
1725. seller_id: 8ca1551acf9832a4cf467bbbac15851f, avg_hours: 374.7050925925925926
1726. seller_id: 8ca5b19e0263150d2c57afdde2b3d011, avg_hours: 124.7314583333333333
1727. seller_id: 8cb7c5ddf41f4d506eba76e9a4702a25, avg_hours: 383.2700000000000000
1728. seller_id: 8cbac7e12637ed9cffa18c7875207478, avg_hours: 311.4234465020576132
1729. seller_id: 8cc6a0e5738e61a87b03c78b2ba9db4b, avg_hours: 394.3714004629629630
1730. seller_id: 8ccf3cf69651cc1d8a02c8bfaf3b8568, avg_hours: 616.7962500000000000
1731. seller_id: 8cf21434553b02cbd37c0bbd07e041b0, avg_hours: 266.7425000000000000
1732. seller_id: 8d46553a36e68f95350a200c12f8f2e2, avg_hours: 409.6296717171717172
1733. seller_id: 8d79c8a04e42d722a75097ce5cbcf2ef, avg_hours: 464.6182510288065844
1734. seller_id: 8d899e15a5925f097cca50faa49b15e3, avg_hours: 173.1025833333333333
1735. seller_id: 8d92f3ea807b89465643c219455e7369, avg_hours: 922.8528125000000000
1736. seller_id: 8d956fec2e4337affcb520f56fd8cbfd, avg_hours: 213.1052655408712677
1737. seller_id: 8daab2245ebdc277c51098d01c5ad8ef, avg_hours: 236.2846006944444444
1738. seller_id: 8dd386be0767c330276ea6a3f96532d3, avg_hours: 246.8525000000000000
1739. seller_id: 8de8fe3af4449ed695d2434c933ed73e, avg_hours: 217.4913888888888889
1740. seller_id: 8def3db7f272735afb2ecd03aeca09a7, avg_hours: 63.6429166666666667
1741. seller_id: 8dfbc5ff27df12f6cef751d3b9554222, avg_hours: 213.4773611111111111
1742. seller_id: 8e29d051f810eb22959ede205b462b9f, avg_hours: 749.7841666666666667
1743. seller_id: 8e2b3afb420011ef0c88c9d5f11ea526, avg_hours: 248.9871464646464646
1744. seller_id: 8e34331b7eedd03be4e5d965c1956225, avg_hours: 326.3607777777777778
1745. seller_id: 8e4f041ff58e7845456d3482524014b3, avg_hours: 577.7195833333333334
1746. seller_id: 8e670472e453ba34a379331513d6aab1, avg_hours: 2063.8994444444444444
1747. seller_id: 8e6cc767478edae941d9bd9eb778d77a, avg_hours: 389.1676003086419753
1748. seller_id: 8e6d7754bc7e0f22c96d255ebda59eba, avg_hours: 325.5537790697674419
1749. seller_id: 8e8a7ce9f2f970dc00e2acf6f6e199f6, avg_hours: 282.9740928819444444
1750. seller_id: 8ea394aed8138685abe1eb9f25e1021d, avg_hours: 270.6656944444444445
1751. seller_id: 8eb88b0acb3f90a717ad659221471fa7, avg_hours: 273.3640277777777778
1752. seller_id: 8ec76bb0965af3f007692b26fa9d6623, avg_hours: 249.4397222222222222
1753. seller_id: 8ed8ea9a57c862f2c18c2fe41f601d56, avg_hours: 177.6512134502923977
1754. seller_id: 8f0fbe2cd4d472157dc1cdef6edecaa9, avg_hours: 173.1808333333333334
1755. seller_id: 8f119a0aee85c0c8fc534629734e94fd, avg_hours: 231.6538168724279835
1756. seller_id: 8f2b51a30523cdecddc2f179f351c7d6, avg_hours: 302.0826736111111111
1757. seller_id: 8f2ce03f928b567e3d56181ae20ae952, avg_hours: 332.5157138242894057
1758. seller_id: 8f54d64f28a993550aa7943f12572959, avg_hours: 321.6881597222222222
1759. seller_id: 8f580d36c1e9d6fbce95283403c7d447, avg_hours: 279.4575694444444444
1760. seller_id: 8f78f0903005064036736c7173a5c2ed, avg_hours: 439.1918386243386243
1761. seller_id: 8fb67a334bacec338885b4e9e1708073, avg_hours: 197.0191666666666667
1762. seller_id: 8fb791022c1fc8909664f48ab7dc636d, avg_hours: 128.2037222222222222
1763. seller_id: 8fbd63429be6d3e5e6d1a709b6464802, avg_hours: 193.8094444444444444
1764. seller_id: 8fbe2ee446b97e128471be4ce983dc0d, avg_hours: 190.0655555555555556
1765. seller_id: 8fd3b4468f6425810648177996c14cbd, avg_hours: 238.3905555555555556
1766. seller_id: 8fdca8e349553f99bc738833a62c8802, avg_hours: 240.1192432950191571
1767. seller_id: 8fe8786ee000001ab51d030dfd4a7bf1, avg_hours: 377.4504444444444444
1768. seller_id: 8fec2e460530482132c436cfb5439925, avg_hours: 754.8645000000000000
1769. seller_id: 8ff1a9df749e454105c55cda13e79143, avg_hours: 282.3211309523809524
1770. seller_id: 8ff38bc3969e67c36c48343a07090f66, avg_hours: 401.7501388888888889
1771. seller_id: 8fff28c4263ddec387f28d237fb42773, avg_hours: 181.7833333333333333
1772. seller_id: 900ba814c251a692506d7834c1218441, avg_hours: 284.1258753229974160
1773. seller_id: 901b460cdce0c64e471230d7f2f9f3a3, avg_hours: 371.7376111111111111
1774. seller_id: 902c99f1ac505c0d18778b61bcd636f7, avg_hours: 116.1184259259259259
1775. seller_id: 903037660cf848a717166eb7a06d616e, avg_hours: 267.3167890772128060
1776. seller_id: 90b36c5aeb728d5504a39f435bef0c5f, avg_hours: 281.3811805555555556
1777. seller_id: 90b57083da5d803237da74daec6dcb2b, avg_hours: 163.9688888888888889
1778. seller_id: 90d4125885ab6c86e8820a722be71974
1779. seller_id: 910a922b426b7ff95eaee129ad6c0e1f, avg_hours: 320.6638888888888889
1780. seller_id: 913fd0ebba70bb919f7254a02239173c, avg_hours: 321.2408333333333333
1781. seller_id: 9140bd1d9de28b197dce077bdd687438, avg_hours: 109.0976388888888889
1782. seller_id: 9140ef75cc8211c4035935e80e567204, avg_hours: 268.4419444444444444
1783. seller_id: 91543f9849d68d023e17194926598543, avg_hours: 261.6755092592592593
1784. seller_id: 916748bc99315c2d202898ae58b1617e, avg_hours: 244.4718836805555556
1785. seller_id: 916c9de0b5ad957346eeeb12f332687e, avg_hours: 176.6829115226337449
1786. seller_id: 918717417d88a9f9ae9735567e6c7682, avg_hours: 195.2823611111111111
1787. seller_id: 918f6fbcf3ab724d805867303e593a1b, avg_hours: 135.1819444444444444
1788. seller_id: 9198786624eaeb375793215cad26cfa6, avg_hours: 278.8587037037037037
1789. seller_id: 91f0eec23d4a61d7d7caeefa3f0ad1ca, avg_hours: 617.2039646464646465
1790. seller_id: 91f5779a8731baca4809fdeade81803f, avg_hours: 379.9190277777777778
1791. seller_id: 91f848e9f4be368f4318775aac733370, avg_hours: 238.4297619047619048
1792. seller_id: 9200e6ce317b67196b6b0bad4d4bd567, avg_hours: 325.8811111111111111
1793. seller_id: 921323538c9f1c4e816f2720eac02bea, avg_hours: 187.4262581699346405
1794. seller_id: 9261d76c62caaf0b24677c2ceb7f8f20, avg_hours: 161.2451190476190476
1795. seller_id: 92992bec39dde5766f590d3b1f46d465
1796. seller_id: 929f342384a6607afe143d789ade1316, avg_hours: 107.6438888888888889
1797. seller_id: 92c8bc6e8f925792247656fed09aad65, avg_hours: 321.6848611111111112
1798. seller_id: 92d14edfb62ee5ae7fdff70b0f4e7233, avg_hours: 134.1881837606837607
1799. seller_id: 92eb0f42c21942b6552362b9b114707d, avg_hours: 310.1794040968342644
1800. seller_id: 9315e491484b1b0081ca166fc164108d, avg_hours: 174.5533333333333333
1801. seller_id: 933446e9a59dece7ae9175103820ca8f, avg_hours: 565.4263888888888889
1802. seller_id: 934ed5cd1b9c1c7382d0a94a94b9e639, avg_hours: 314.8963888888888889
1803. seller_id: 939e6227d6964a11a70aa91243e418f2, avg_hours: 125.0929861111111111
1804. seller_id: 939f6e231201f26803cb5c3a3d2940b3, avg_hours: 232.8641666666666667
1805. seller_id: 93b9a99027bd8bd6af682aff18dd19bf, avg_hours: 269.9503194444444444
1806. seller_id: 93bef6edaa84956e8e575016449b6351, avg_hours: 237.9472222222222222
1807. seller_id: 93dc87703c046b603023e75222018b45, avg_hours: 465.6917156862745098
1808. seller_id: 94144541854e298c2d976cb893b81343, avg_hours: 283.2342214912280702
1809. seller_id: 941554c5757b73ba0e50aa7732310afc, avg_hours: 181.1451388888888889
1810. seller_id: 94165aea8a35c3c21499cbcae239b16c, avg_hours: 147.5208333333333333
1811. seller_id: 94231344608e603693b0a8891143f65d, avg_hours: 268.4591666666666667
1812. seller_id: 9449f25aeaf531019b76999ea49a6949, avg_hours: 319.1306481481481481
1813. seller_id: 9485a23c0430ba1d58d359391606fce6, avg_hours: 321.7902083333333334
1814. seller_id: 94b9108d4b637ba65bb4f1e53cfcf8d8, avg_hours: 389.1934375000000000
1815. seller_id: 94c49f20a123aeb9360dbf80ff912bf6, avg_hours: 316.9817592592592593
1816. seller_id: 94ca168e8bcb407ab85c5da308863027, avg_hours: 292.2455000000000000
1817. seller_id: 94d76e96eedd976258cd3278ce56d5f2, avg_hours: 168.5572222222222222
1818. seller_id: 94e93ce877be27a515118dbfd2c2be41, avg_hours: 313.8584885620915033
1819. seller_id: 951e8cef368f09bb3f3d03c00ca4702c, avg_hours: 208.1063405797101449
1820. seller_id: 9523fb39dd240aa958e040f8183d64f3, avg_hours: 501.2716666666666667
1821. seller_id: 9535a841eecebed61a9fb1ac1cbb5597, avg_hours: 204.0191666666666667
1822. seller_id: 9539213aa8e023c01937bef95dc006da, avg_hours: 282.6205555555555555
1823. seller_id: 954e95f20808d7e5d11f0de292d078e0, avg_hours: 261.7377777777777778
1824. seller_id: 9558aa23f77a9e0a0eca83540999f43b, avg_hours: 499.8605555555555556
1825. seller_id: 955fee9216a65b617aa5c0531780ce60, avg_hours: 244.45956729317632850211
1826. seller_id: 9591fc341b1bfb7ef561e2968ec6e011
1827. seller_id: 9596c870880d900012f2e8e6e30d06d7, avg_hours: 302.3822222222222222
1828. seller_id: 9599519be538b98748162a2b48248960, avg_hours: 542.6088888888888889
1829. seller_id: 95b293867b5862941c9cd74f756a3c68, avg_hours: 507.1817592592592593
1830. seller_id: 95cca791657aabeff15a07eb152d7841, avg_hours: 89.0097222222222222
1831. seller_id: 95e03ca3d4146e4011985981aeb959b9, avg_hours: 287.7196403508771930
1832. seller_id: 95ec4458365c4d11f452ccf538377619, avg_hours: 120.2852329749103943
1833. seller_id: 95f83f51203c626648c875dd41874c7f, avg_hours: 256.4432008547008547
1834. seller_id: 960945e1a9535cbc0cd6ddd35fbe7ae8, avg_hours: 138.2893773946360153
1835. seller_id: 9616352088dcf83a7c06637f4ebf1c80, avg_hours: 288.4544959908361970
1836. seller_id: 961dff0a659b4561334372337dd897d9, avg_hours: 476.2267592592592593
1837. seller_id: 9646c3513289980f17226a2fc4720dbd, avg_hours: 295.3543238304093567
1838. seller_id: 96493fab2fbb13a14d0c0e8772eef5c3, avg_hours: 314.5056857638888889
1839. seller_id: 964ff64dc05b13811c6d0f41e0aa5f6b, avg_hours: 160.1416666666666667
1840. seller_id: 966cb4760537b1404caedd472cc610a5, avg_hours: 228.8864220563847430
1841. seller_id: 9674754b5a0cb32b638cec001178f799, avg_hours: 183.9191315789473684
1842. seller_id: 96804ea39d96eb908e7c3afdb671bb9e, avg_hours: 312.4093732193732194
1843. seller_id: 968268a686aa05d1f529fb07dff08130, avg_hours: 215.7800231481481482
1844. seller_id: 968ee78631915a63fef426d6733d7422, avg_hours: 349.5011111111111111
1845. seller_id: 96e5dc09087bad639b4ee193104ec2e5, avg_hours: 103.8598611111111111
1846. seller_id: 96f7c797de9ca20efbe14545bed63eec, avg_hours: 46.3080555555555556
1847. seller_id: 972d0f9cf61b499a4812cf0bfa3ad3c4, avg_hours: 425.0823288113695090
1848. seller_id: 973f21788dfab357250f69a8dcb7ddee, avg_hours: 497.2707748538011696
1849. seller_id: 974cf2cb8f4b7add98709c30df02fe10, avg_hours: 260.8002129629629630
1850. seller_id: 97512d3fc193b2d1dfcdba0f9d1f0f8a, avg_hours: 173.9914102564102564
1851. seller_id: 977f9f63dd360c2a32ece2f93ad6d306, avg_hours: 285.5506250000000000
1852. seller_id: 979e9f8b5b39dd243a2550c8b05aecf0, avg_hours: 191.9429861111111111
1853. seller_id: 97e4a63591ca439a2b8b7efd20e6e19e, avg_hours: 145.5155555555555556
1854. seller_id: 97e50a621f8e801f4baf69e08687c192, avg_hours: 226.0644444444444444
1855. seller_id: 97e995629983723d11830a829bc2b246, avg_hours: 400.8343888888888889
1856. seller_id: 9803a40e82e45418ab7fb84091af5231, avg_hours: 367.3913888888888889
1857. seller_id: 980640c45d7a4635885491d077167e4d, avg_hours: 164.9281746031746032
1858. seller_id: 98115075dd26cb8835946fc6086f5d30, avg_hours: 97.8306250000000000
1859. seller_id: 984c273121e743dd14767befe6cb17f5, avg_hours: 812.0866666666666667
1860. seller_id: 9853a239ab7b7ebbdc3a21248d5b8e1f, avg_hours: 425.9807638888888889
1861. seller_id: 985c92cc412091f8529c12d7f23d3fef, avg_hours: 179.3495833333333333
1862. seller_id: 989becdce12ebc39863c2bceab6f3ca1, avg_hours: 322.6893703703703704
1863. seller_id: 98dac6635aee4995d501a3972e047414, avg_hours: 192.9228786549707602
1864. seller_id: 98dddbc4601dd4443ca174359b237166, avg_hours: 189.9477777777777778
1865. seller_id: 98e164d549402270247f3c96a1a158ef, avg_hours: 197.3804166666666667
1866. seller_id: 98f52e1020fe788c10c0418de4393fec, avg_hours: 222.0786111111111111
1867. seller_id: 99002261c568a84cce14d43fcffb43ea, avg_hours: 396.2528935185185185
1868. seller_id: 9906e7aa42a3c067b7c9a564d01c4320, avg_hours: 380.8469791666666667
1869. seller_id: 994f04b3718c2bab35c2adfa8afecd2a, avg_hours: 317.8871464646464646
1870. seller_id: 9996ae921c50e8dff411ac69c0b4bb8b, avg_hours: 387.3545370370370371
1871. seller_id: 999f6d9a1c7c81f43be44c6b7d076210, avg_hours: 112.4352777777777778
1872. seller_id: 99a25c39b28a74d1151c35c18d178292, avg_hours: 40.1747222222222222
1873. seller_id: 99a54764c341d5dc80b4a8fac4eba3fb, avg_hours: 163.0888594276094276
1874. seller_id: 99cd94252748d2bdde08e17858233602, avg_hours: 66.0441666666666667
1875. seller_id: 99eaacc9e6046db1c82b163c5f84869f, avg_hours: 343.1225082918739635
1876. seller_id: 9a03a4e9eb0b947652fae4f6121a3f5e, avg_hours: 323.5626984126984127
1877. seller_id: 9a1aea68d3efa00862ec88c0768037d0, avg_hours: 300.8140277777777778
1878. seller_id: 9a208dee8f95cfdf00760c4d627828ec
1879. seller_id: 9a84ba99f5367fdbd4598363496f1ea2, avg_hours: 246.4044259259259259
1880. seller_id: 9aa388272ee334b6ae07bc73706e254a, avg_hours: 182.0906349206349206
1881. seller_id: 9ac4f14370b1e24ddc58be041b7f99df, avg_hours: 204.7975000000000000
1882. seller_id: 9ac75591b69c3402684b6ce0310f22ee, avg_hours: 47.7086111111111111
1883. seller_id: 9add47bf45ce8e8c7db6b9cf670b1e09, avg_hours: 282.7279521963824289
1884. seller_id: 9b00cad94ef3078faf6fba2e792c158f, avg_hours: 465.3663888888888889
1885. seller_id: 9b00ed88b7fdb95d6ff76e27c1b52d16, avg_hours: 208.3587666666666667
1886. seller_id: 9b013e03b2ab786505a1d3b5c0756754, avg_hours: 182.6010025252525252
1887. seller_id: 9b1050e85becf3ae99c1cf4934c9bc5d
1888. seller_id: 9b1585752613ec342d03bbab9997ec48, avg_hours: 155.0187037037037037
1889. seller_id: 9b1ab052f5fca308ba743ac789ebb2e1, avg_hours: 244.9380555555555556
1890. seller_id: 9b1f656ca3060f8af17a50d8a024b533, avg_hours: 369.5827777777777778
1891. seller_id: 9b522ba7eae9e1d04082f267144583cc, avg_hours: 633.1932222222222222
1892. seller_id: 9b76ad3d04236f76bc71c59470305e13, avg_hours: 90.6197222222222222
1893. seller_id: 9bade61a92bed55a25d2b67b9f4ed739, avg_hours: 240.5477777777777778
1894. seller_id: 9baf5cb77970f539089d09a38bcec5c3, avg_hours: 348.5532725694444444
1895. seller_id: 9bc484c87d79cd4874e05ca182658045, avg_hours: 307.0787500000000000
1896. seller_id: 9bcdfa7b615b3abb9461d9e3ad9886ae, avg_hours: 269.0250277777777778
1897. seller_id: 9bf11dfc0bec77e5a23028043c3c5a8f, avg_hours: 754.1472222222222222
1898. seller_id: 9c068d10aca38e85c50202e17b4a7e88, avg_hours: 384.5259967320261438
1899. seller_id: 9c0e69c7bf2619675bbadf47b43f655a, avg_hours: 348.3947319444444444
1900. seller_id: 9c1c0c36cd23c20897e473901a8fb149, avg_hours: 127.5917857142857143
1901. seller_id: 9c351405b754cc5ce3e2ecf277bb034a
1902. seller_id: 9c3a1c416c765687bc79a04113269929, avg_hours: 118.3366666666666667
1903. seller_id: 9c3c24eca51c52b91c1de727d2a2ae06, avg_hours: 253.6542592592592593
1904. seller_id: 9c4d31c7e46ab03a43fc06e3142afd4e, avg_hours: 164.6994444444444445
1905. seller_id: 9c54608f0996c32ae4743089d915f845, avg_hours: 285.4274074074074074
1906. seller_id: 9c57bc60cfad5ee62d35d3f1ce4593a1, avg_hours: 759.7388888888888889
1907. seller_id: 9c690ceacd5c66731bf443ea810195cb, avg_hours: 172.6324537037037037
1908. seller_id: 9c7fd21e0aa159b20da593371f08ff7c, avg_hours: 158.3771180555555556
1909. seller_id: 9cad4b68bb993ee401a3c5aaa2bc26dd, avg_hours: 350.0115873015873016
1910. seller_id: 9cea4682e16655f7da87f406902e989e, avg_hours: 213.3815740740740741
1911. seller_id: 9cf787a239c1aa29dbd76f153dc13f9a, avg_hours: 156.7806250000000000
1912. seller_id: 9d213f303afae4983637247556438ede, avg_hours: 158.3954629629629630
1913. seller_id: 9d39404483343dd55c7ae254494d8388, avg_hours: 323.5952777777777778
1914. seller_id: 9d489893ff6af05029671b785f54b998, avg_hours: 148.1499537037037037
1915. seller_id: 9d4db00d65d7760644ac0c14edb5fd86, avg_hours: 185.8497586980920314
1916. seller_id: 9d5604a1f112324ad6b2aa552122e0fb, avg_hours: 278.9875163398692810
1917. seller_id: 9d5a9018aee56acb367ba9c3f05d1d6a, avg_hours: 336.8537820512820513
1918. seller_id: 9d681c7e12db302cb261e721040dde65, avg_hours: 197.0188492063492063
1919. seller_id: 9d69ba0a7a626a64dc5db08e529559cf, avg_hours: 332.5600000000000000
1920. seller_id: 9d7a1d34a5052409006425275ba1c2b4, avg_hours: 302.8834375000000000
1921. seller_id: 9da15f4a4ea758d9eeb49000dbe57e22, avg_hours: 525.5966666666666667
1922. seller_id: 9da1ca0bef29ee170e541927a5aeabdc, avg_hours: 390.2688888888888889
1923. seller_id: 9dc79dd988ac42f4d56c340d7048420a, avg_hours: 156.1598611111111111
1924. seller_id: 9dd459b29a14bf89d47183cf2cd0e4c7, avg_hours: 126.9668055555555556
1925. seller_id: 9dd59e43f0c9f0553244e8f9c2fb247e, avg_hours: 312.2550277777777778
1926. seller_id: 9dda5bbacd45e18d6485fee649205d09, avg_hours: 341.5405934343434343
1927. seller_id: 9de4643a8dbde634fe55621059d92273, avg_hours: 354.5182304526748971
1928. seller_id: 9df5750209b83567ec144eb299d7d634, avg_hours: 321.8871969696969697
1929. seller_id: 9e17b9d64683aebcbb9ee362d06463b4
1930. seller_id: 9e25199f6ef7e7c347120ff175652c3b, avg_hours: 196.6072222222222222
1931. seller_id: 9e6229250fedbe05838fef417b74e7fb, avg_hours: 272.5818073593073593
1932. seller_id: 9e6967d3cf386d284251784b18ccb485, avg_hours: 170.5733585858585858
1933. seller_id: 9e7c5f4d7770eab65738cca38f9efccf, avg_hours: 178.1669444444444445
1934. seller_id: 9e94fa26a70ede4d26226e918e8706a2, avg_hours: 135.1769444444444444
1935. seller_id: 9e9b539eb2806acee3f5c28085c1db9f, avg_hours: 576.5299074074074074
1936. seller_id: 9ed65337433adfbedefd23dd76eaa494, avg_hours: 159.1313425925925926
1937. seller_id: 9ef932e837d8b7f392c0bfee9d359dc2, avg_hours: 874.9902777777777778
1938. seller_id: 9f50216bfd01913736a55a11b55ea842, avg_hours: 232.3469590643274854
1939. seller_id: 9f505651f4a6abe901a56cdc21508025, avg_hours: 184.64493414188836724176
1940. seller_id: 9f56a7a649097b166d8ed286ad86a15c
1941. seller_id: 9fbd5666d8618fa571c4230fafa09bd6, avg_hours: 314.7663888888888889
1942. seller_id: 9fc70243fb26800cba56e8f014797004, avg_hours: 223.6147619047619048
1943. seller_id: 9fe7c6641c79970ab48185498f547c09, avg_hours: 400.8722222222222222
1944. seller_id: a00824eb9093d40e589b940ec45c4eb0, avg_hours: 184.9271296296296296
1945. seller_id: a0415d9b25ede3c4b1e477e9916ffc03, avg_hours: 206.9034876543209876
1946. seller_id: a066df7361163e7ddc5d7452dd17448b, avg_hours: 372.1956535947712418
1947. seller_id: a06c8ff043abea0528ee44171e2140a2, avg_hours: 86.8085069444444444
1948. seller_id: a080fc8a850289b27500f6b49cca2553, avg_hours: 129.8221527777777778
1949. seller_id: a08692680c77d30a0b4280da5df01c5a, avg_hours: 261.0243300653594771
1950. seller_id: a09a13f18ed27932d08438aa6f12756e, avg_hours: 213.7272222222222222
1951. seller_id: a0a14e50070f3225b3eabba5b85da517, avg_hours: 136.7018750000000000
1952. seller_id: a0d7fbb07bb5ebc3b05980e750db56f3, avg_hours: 377.6123611111111111
1953. seller_id: a0e19590a0923cdd0614ea9427713ced
1954. seller_id: a1040efe9ff4a6f93c28b0499eada8f5, avg_hours: 390.6477777777777778
1955. seller_id: a1043bafd471dff536d0c462352beb48, avg_hours: 315.6645892434988180
1956. seller_id: a11a0e0ca67423425691db355cff69b0, avg_hours: 124.5405555555555556
1957. seller_id: a13580f0e8f782b7a543885a0ef99f08, avg_hours: 591.8030833333333334
1958. seller_id: a13aaf2d2886ab9fb30fb9a920160b8f, avg_hours: 211.6302083333333334
1959. seller_id: a1474fd46fd3430168f7ec202da39408, avg_hours: 372.1454166666666667
1960. seller_id: a150c540f572d0fb53992264bc5c10b5, avg_hours: 260.4102777777777778
1961. seller_id: a1544b9ea0b2390e020537d4daa89049, avg_hours: 254.3596180555555556
1962. seller_id: a154d7316f158bb42e6fa18bbe3afd3a, avg_hours: 1139.5258333333333333
1963. seller_id: a17f621c590ea0fab3d5d883e1630ec6, avg_hours: 269.3786538461538462
1964. seller_id: a1bea7061f61f6fdd9a85a6325ba1033, avg_hours: 104.6991666666666667
1965. seller_id: a1bea9970d8f65b240555f99c2214f7f, avg_hours: 222.4205555555555556
1966. seller_id: a1ed30492b3b798bc121845bc4aa7366
1967. seller_id: a20d8058c866dbaeca014d2cd20ac62e, avg_hours: 552.7534722222222223
1968. seller_id: a213f1bd6458f4a158f3746cb2514559, avg_hours: 198.6808333333333333
1969. seller_id: a218df5c097b0ca409cfaac1488cc7f6, avg_hours: 272.9625000000000000
1970. seller_id: a21c11ec5c3f03e7cc9f9203bff9e1c6, avg_hours: 214.4861111111111111
1971. seller_id: a23266650e7c84bb93fbbba502137478, avg_hours: 250.1548784722222222
1972. seller_id: a247197e2e9c19a6a53a6888cb8b660f
1973. seller_id: a254c682cc01e119f83530446f1df9a9, avg_hours: 375.5319047619047619
1974. seller_id: a2a41aedb70551d4a85aa04dc2fced48, avg_hours: 184.1447222222222222
1975. seller_id: a2b5b6105ea5942300631d2e76f4ffe0, avg_hours: 197.3077430555555556
1976. seller_id: a2b911e9ad40dc7d61c142a4683e2d85, avg_hours: 305.7836111111111111
1977. seller_id: a2deecd5398f5df4987110c80a1972a3, avg_hours: 197.0643803418803419
1978. seller_id: a2e85714b56b1cb6bb24a9a6e6cad36f
1979. seller_id: a2e874074c877c5a05abae80ad6e488f, avg_hours: 451.7202910052910053
1980. seller_id: a2fa0bdc798ee84cdb08281337cf4fb6, avg_hours: 445.2939141414141414
1981. seller_id: a3082f442524a1be452e3189e003b361, avg_hours: 294.4634722222222223
1982. seller_id: a35124e2d763d7ca3fbe3b97d143200f, avg_hours: 211.2153571428571429
1983. seller_id: a353b1083c9863d756d9404695016d64, avg_hours: 496.8694444444444444
1984. seller_id: a35ef466c6fd6d052f5d241240d3c5e2, avg_hours: 283.3867592592592593
1985. seller_id: a369d693961cb93b61ca2cc518872a85, avg_hours: 234.4095524691358025
1986. seller_id: a36ac007a4d18f865c8d32c3b2402c2d, avg_hours: 228.4665972222222222
1987. seller_id: a36b125ac6d5fdbc7f50de85c9157bdc, avg_hours: 299.4721888888888889
1988. seller_id: a37c340b91cb0169e8b029db6440fba2, avg_hours: 258.7238888888888889
1989. seller_id: a3a38f4affed601eb87a97788c949667, avg_hours: 292.5141068376068376
1990. seller_id: a3b0df0065e264a91b7bbf5f844af5cd, avg_hours: 320.6702777777777778
1991. seller_id: a3b42d266fa8afc874b909422ce88582, avg_hours: 83.5530555555555556
1992. seller_id: a3dd39f583bc80bd8c5901c95878921e, avg_hours: 293.2567942942942943
1993. seller_id: a3e9a2c700480d9bb01fba070ba80a0e, avg_hours: 307.6646270396270396
1994. seller_id: a3f0b55de503387383c7b1de3ad7f678, avg_hours: 244.3959935897435897
1995. seller_id: a3fa18b3f688ec0fca3eb8bfcbd2d5b3, avg_hours: 342.1091666666666667
1996. seller_id: a414555ce331b8c8aea4a9cb8395194d, avg_hours: 167.1302083333333333
1997. seller_id: a416b6a846a11724393025641d4edd5e, avg_hours: 295.5142219065656566
1998. seller_id: a420f60ff1aa9acc80d0e42959f2b313, avg_hours: 264.2603824476650564
1999. seller_id: a425f92c199eb576938df686728acd20, avg_hours: 406.4664043209876543
2000. seller_id: a435b009cd956ea60748b5cfbddf2e24, avg_hours: 729.6537962962962963
```

#### 📊 Metadata

- **sql:** SELECT oi.seller_id, AVG(EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_approved_at)) / 3600) AS avg_hours FROM analytics.orders o JOIN analytics.order_items oi ON o.order_id = oi.order_id GROUP BY oi.seller_id ORDER BY oi.seller_id
- **row_count:** 2000
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-10"></a>
### Query 10

#### 📝 Input

- **Query:** Identifique gargalos operacionais analisando pedidos com maior tempo de processamento

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.8
- **Reason:** analysis of orders by processing time to find bottlenecks
- **Thread ID:** `ec373956-a8c4-48d7-8f21-445ad44eafe0`

#### 💬 Response

```
Análise dos gargalos operacionais com base no tempo de processamento dos pedidos:

1. Pedido ID: 1612081119e8f23745698ad3367cc14b - Status: indisponível - Tempo de processamento: 4.509,18 horas
2. Pedido ID: 2e5dc86c8c4aa663549caf5e31de840d - Status: em processamento - Tempo de processamento: 1.450,87 horas
3. Pedido ID: 2e7a8482f6fb09756ca50c10d7bfc047 - Status: enviado - Tempo de processamento: 784,05 horas
4. Pedido ID: e5fa5a7210941f7d56d0208e4e071d35 - Status: cancelado - Tempo de processamento: 781,03 horas
5. Pedido ID: 0a5c74ccc786ced7903270de9d6c170a - Status: indisponível - Tempo de processamento: 780,86 horas
6. Pedido ID: 0a93b40850d3f4becf2f276666e01340 - Status: entregue - Tempo de processamento: 741,44 horas
7. Pedido ID: f7923db0430587601c2aef15ec4b8af4 - Status: entregue - Tempo de processamento: 738,45 horas
8. Pedido ID: 490291524fddde2b31c2e6bec3d9e6da - Status: cancelado - Tempo de processamento: 676,07 horas
9. Pedido ID: 809a282bbd5dbcabb6f2f724fca862ec - Status: cancelado - Tempo de processamento: 573,87 horas
10. Pedido ID: fdd647b689626410b725d1cce2ddf37c - Status: em processamento - Tempo de processamento: 555,89 horas

Total de 200 pedidos analisados, com tempos de processamento que indicam possíveis gargalos operacionais. É recomendável investigar os pedidos com maior tempo de processamento para identificar as causas e implementar melhorias.

Dados completos:
1. order_id: 1612081119e8f23745698ad3367cc14b, order_status: unavailable, order_purchase_timestamp: 2016-10-05 18:06:48, order_approved_at: 2017-04-11 15:17:38, processing_time_hours: 4509.1805555555555556
2. order_id: 2e5dc86c8c4aa663549caf5e31de840d, order_status: processing, order_purchase_timestamp: 2017-02-03 00:04:49, order_approved_at: 2017-04-04 10:56:48, processing_time_hours: 1450.8663888888888889
3. order_id: 2e7a8482f6fb09756ca50c10d7bfc047, order_status: shipped, order_purchase_timestamp: 2016-09-04 21:15:19, order_approved_at: 2016-10-07 13:18:03, processing_time_hours: 784.0455555555555556
4. order_id: e5fa5a7210941f7d56d0208e4e071d35, order_status: canceled, order_purchase_timestamp: 2016-09-05 00:15:34, order_approved_at: 2016-10-07 13:17:15, processing_time_hours: 781.0280555555555556
5. order_id: 0a5c74ccc786ced7903270de9d6c170a, order_status: unavailable, order_purchase_timestamp: 2018-01-18 23:14:36, order_approved_at: 2018-02-20 12:05:54, processing_time_hours: 780.8550000000000000
6. order_id: 0a93b40850d3f4becf2f276666e01340, order_status: delivered, order_purchase_timestamp: 2018-01-20 14:24:50, order_approved_at: 2018-02-20 11:51:27, processing_time_hours: 741.4436111111111111
7. order_id: f7923db0430587601c2aef15ec4b8af4, order_status: delivered, order_purchase_timestamp: 2018-01-20 17:38:58, order_approved_at: 2018-02-20 12:05:54, processing_time_hours: 738.4488888888888889
8. order_id: 490291524fddde2b31c2e6bec3d9e6da, order_status: canceled, order_purchase_timestamp: 2017-04-14 22:40:54, order_approved_at: 2017-05-13 02:45:06, processing_time_hours: 676.0700000000000000
9. order_id: 809a282bbd5dbcabb6f2f724fca862ec, order_status: canceled, order_purchase_timestamp: 2016-09-13 15:24:19, order_approved_at: 2016-10-07 13:16:46, processing_time_hours: 573.8741666666666667
10. order_id: fdd647b689626410b725d1cce2ddf37c, order_status: processing, order_purchase_timestamp: 2017-12-04 10:09:35, order_approved_at: 2017-12-27 14:03:00, processing_time_hours: 555.8902777777777778
11. order_id: de0076b42a023f53b398ce9ab0d9009c, order_status: delivered, order_purchase_timestamp: 2017-12-04 11:15:54, order_approved_at: 2017-12-27 14:03:00, processing_time_hours: 554.7850000000000000
12. order_id: daed0f3aefd193de33c31e21b16a3b3a, order_status: delivered, order_purchase_timestamp: 2018-03-12 15:21:32, order_approved_at: 2018-03-29 11:35:16, processing_time_hours: 404.2288888888888889
13. order_id: 9c038e10f14d12a96939a0176c4ecc99, order_status: delivered, order_purchase_timestamp: 2017-05-26 15:30:49, order_approved_at: 2017-06-08 23:02:47, processing_time_hours: 319.5327777777777778
14. order_id: 14ef2221cc3570aa6ce512fc353529b3, order_status: delivered, order_purchase_timestamp: 2018-02-09 09:27:56, order_approved_at: 2018-02-22 11:15:51, processing_time_hours: 313.7986111111111111
15. order_id: 0c1426109d8295a688ee4182016bba59, order_status: delivered, order_purchase_timestamp: 2017-11-24 21:24:29, order_approved_at: 2017-12-07 09:50:08, processing_time_hours: 300.4275000000000000
16. order_id: 483b53ea654d3566427a092cdef047fd, order_status: delivered, order_purchase_timestamp: 2017-08-03 15:59:11, order_approved_at: 2017-08-16 03:30:15, processing_time_hours: 299.5177777777777778
17. order_id: f5194ba2a4560ffa0e87746852c61fc1, order_status: delivered, order_purchase_timestamp: 2017-11-24 22:53:26, order_approved_at: 2017-12-07 09:50:07, processing_time_hours: 298.9447222222222222
18. order_id: 70f357cca87c1162357bf3c0a993cbe5, order_status: delivered, order_purchase_timestamp: 2017-09-01 18:40:11, order_approved_at: 2017-09-13 22:04:49, processing_time_hours: 291.4105555555555556
19. order_id: cf72398d0690f841271b695bbfda82d2, order_status: delivered, order_purchase_timestamp: 2017-09-01 18:45:33, order_approved_at: 2017-09-13 22:04:39, processing_time_hours: 291.3183333333333333
20. order_id: 06eb87385425e5797a1a5c2cdb1b6559, order_status: delivered, order_purchase_timestamp: 2017-09-01 18:53:08, order_approved_at: 2017-09-13 22:10:37, processing_time_hours: 291.2913888888888889
21. order_id: 8554cb37f7158cb0b082a841d24a4589, order_status: delivered, order_purchase_timestamp: 2017-09-01 18:40:44, order_approved_at: 2017-09-13 21:58:04, processing_time_hours: 291.2888888888888889
22. order_id: 77ca435b03fbf991e5027e3776e37885, order_status: delivered, order_purchase_timestamp: 2017-09-01 18:49:54, order_approved_at: 2017-09-13 21:56:08, processing_time_hours: 291.1038888888888889
23. order_id: 1fab4ac9d85079b3da72a11475ae1685, order_status: delivered, order_purchase_timestamp: 2017-09-01 19:04:22, order_approved_at: 2017-09-13 22:06:11, processing_time_hours: 291.0302777777777778
24. order_id: 0184d4ddb259e1a4cfc2871888cf97b8, order_status: delivered, order_purchase_timestamp: 2017-09-01 20:04:28, order_approved_at: 2017-09-13 22:17:15, processing_time_hours: 290.2130555555555556
25. order_id: c3b8c17ee15e0e798c2e178b7d4c7f42, order_status: delivered, order_purchase_timestamp: 2017-09-01 20:04:47, order_approved_at: 2017-09-13 22:08:55, processing_time_hours: 290.0688888888888889
26. order_id: bc4854efd86d9f42140c951c595d20c1, order_status: delivered, order_purchase_timestamp: 2017-09-01 20:05:42, order_approved_at: 2017-09-13 22:00:51, processing_time_hours: 289.9191666666666667
27. order_id: 40de47dfa620d667117e4a6067b6e1ec, order_status: delivered, order_purchase_timestamp: 2017-09-01 20:05:55, order_approved_at: 2017-09-13 21:58:38, processing_time_hours: 289.8786111111111111
28. order_id: 580f3268bc2075c5961b2d2929c7a35b, order_status: delivered, order_purchase_timestamp: 2017-09-01 20:17:09, order_approved_at: 2017-09-13 22:03:42, processing_time_hours: 289.7758333333333333
29. order_id: 1378f9601350615613cc8832d6789c5d, order_status: delivered, order_purchase_timestamp: 2017-09-01 20:28:02, order_approved_at: 2017-09-13 22:03:51, processing_time_hours: 289.5969444444444444
30. order_id: 241adc087f5732067fc042dceb9cc6da, order_status: delivered, order_purchase_timestamp: 2018-02-07 11:48:20, order_approved_at: 2018-02-19 09:06:52, processing_time_hours: 285.3088888888888889
31. order_id: f5942dc9da4bc0e2beac653f4e63a020, order_status: delivered, order_purchase_timestamp: 2017-04-24 02:24:24, order_approved_at: 2017-05-05 14:21:56, processing_time_hours: 275.9588888888888889
32. order_id: a7c0c5a345bb63d37fc8aafab1f86a4d, order_status: delivered, order_purchase_timestamp: 2017-02-18 07:45:01, order_approved_at: 2017-03-01 10:51:24, processing_time_hours: 267.1063888888888889
33. order_id: ed4116f3f55e67e9a26b9f1891ba2497, order_status: delivered, order_purchase_timestamp: 2018-08-09 13:21:48, order_approved_at: 2018-08-20 15:55:42, processing_time_hours: 266.5650000000000000
34. order_id: e454f35044003de39e10f976817edc27, order_status: delivered, order_purchase_timestamp: 2017-09-25 13:39:49, order_approved_at: 2017-10-06 15:14:17, processing_time_hours: 265.5744444444444444
35. order_id: 6e57e23ecac1ae881286657694444267, order_status: delivered, order_purchase_timestamp: 2018-08-09 17:36:47, order_approved_at: 2018-08-20 15:55:42, processing_time_hours: 262.3152777777777778
36. order_id: e73fe43cdcd166f7f0c6e3c2bf11a917, order_status: delivered, order_purchase_timestamp: 2018-08-09 18:06:43, order_approved_at: 2018-08-20 15:57:28, processing_time_hours: 261.8458333333333333
37. order_id: 6fa0c125ee7d870f6602c97e33d87bc5, order_status: delivered, order_purchase_timestamp: 2018-08-09 19:32:42, order_approved_at: 2018-08-20 15:59:54, processing_time_hours: 260.4533333333333333
38. order_id: 6dcf0aeb8b1eb4021c26e1d0e9394979, order_status: delivered, order_purchase_timestamp: 2018-08-09 20:37:34, order_approved_at: 2018-08-20 15:59:18, processing_time_hours: 259.3622222222222222
39. order_id: f6aeaaa897aaaf586ac05fb8d821ed9e, order_status: delivered, order_purchase_timestamp: 2017-11-23 15:43:00, order_approved_at: 2017-12-04 10:54:28, processing_time_hours: 259.1911111111111111
40. order_id: 4387477eec4b3c89b39f3f454940d059, order_status: delivered, order_purchase_timestamp: 2018-08-09 20:45:10, order_approved_at: 2018-08-20 15:56:29, processing_time_hours: 259.1886111111111111
41. order_id: 9eac94dce77597b831e8c0dfc584bc8b, order_status: delivered, order_purchase_timestamp: 2018-01-18 23:16:44, order_approved_at: 2018-01-29 16:53:28, processing_time_hours: 257.6122222222222222
42. order_id: 5958fb8c6e854b986800307f995fd209, order_status: delivered, order_purchase_timestamp: 2017-09-01 20:04:49, order_approved_at: 2017-09-12 12:35:16, processing_time_hours: 256.5075000000000000
43. order_id: 511a2c82e1860031d509e3d925c4b873, order_status: delivered, order_purchase_timestamp: 2017-04-06 19:52:25, order_approved_at: 2017-04-17 08:50:17, processing_time_hours: 252.9644444444444444
44. order_id: ebc94658c583ab37ad4f8e9091c4bef2, order_status: delivered, order_purchase_timestamp: 2018-04-14 08:22:43, order_approved_at: 2018-04-24 18:04:50, processing_time_hours: 249.7019444444444444
45. order_id: 6b80bb20190715d71c43efff617bd659, order_status: delivered, order_purchase_timestamp: 2017-02-19 01:15:03, order_approved_at: 2017-03-01 10:51:46, processing_time_hours: 249.6119444444444444
46. order_id: 7fd4b0e047195ca197c3660772a8d8c0, order_status: canceled, order_purchase_timestamp: 2016-10-08 07:02:33, order_approved_at: 2016-10-18 15:19:10, processing_time_hours: 248.2769444444444444
47. order_id: 8f1e49888948febad9d7dc3ce8ec85c4, order_status: delivered, order_purchase_timestamp: 2017-08-22 12:42:42, order_approved_at: 2017-09-01 17:30:13, processing_time_hours: 244.7919444444444444
48. order_id: 123e27a1a4d0b2481d8618ac3dff7d4e, order_status: canceled, order_purchase_timestamp: 2016-10-08 12:44:32, order_approved_at: 2016-10-18 15:19:08, processing_time_hours: 242.5766666666666667
49. order_id: b9a422aebaeb3396ee0b761b10c0cc08, order_status: delivered, order_purchase_timestamp: 2017-11-26 14:43:00, order_approved_at: 2017-12-06 11:14:49, processing_time_hours: 236.5302777777777778
50. order_id: d1e799b4645be8aef2337253468a31f7, order_status: delivered, order_purchase_timestamp: 2017-09-13 08:19:01, order_approved_at: 2017-09-22 17:10:33, processing_time_hours: 224.8588888888888889
51. order_id: f6f0b2497c5a4ca89670186757ab2684, order_status: delivered, order_purchase_timestamp: 2017-06-26 12:23:32, order_approved_at: 2017-07-05 17:09:11, processing_time_hours: 220.7608333333333333
52. order_id: cb560d710377eef2c41351f25c732da1, order_status: delivered, order_purchase_timestamp: 2018-02-14 13:28:49, order_approved_at: 2018-02-23 10:15:34, processing_time_hours: 212.7791666666666667
53. order_id: 931a32b4ca3fdc36741af29ea645d8bf, order_status: delivered, order_purchase_timestamp: 2017-12-06 14:44:14, order_approved_at: 2017-12-15 10:41:08, processing_time_hours: 211.9483333333333333
54. order_id: 9d1780c1dba60f1e3fc99e1072979110, order_status: delivered, order_purchase_timestamp: 2018-03-17 16:04:08, order_approved_at: 2018-03-26 09:10:13, processing_time_hours: 209.1013888888888889
55. order_id: 5dae8914499e60f98b65ea4094c69880, order_status: delivered, order_purchase_timestamp: 2017-02-28 17:52:26, order_approved_at: 2017-03-09 10:04:24, processing_time_hours: 208.1994444444444444
56. order_id: 5fa78e91b5cb84b6a8ccc42733f95742, order_status: delivered, order_purchase_timestamp: 2017-11-30 01:51:23, order_approved_at: 2017-12-08 16:33:14, processing_time_hours: 206.6975000000000000
57. order_id: 96872d026aa122a9e93957de1e58d427, order_status: delivered, order_purchase_timestamp: 2018-01-18 11:33:56, order_approved_at: 2018-01-26 17:03:26, processing_time_hours: 197.4916666666666667
58. order_id: 5226f1a731e8a1215da5e1bea64e2130, order_status: canceled, order_purchase_timestamp: 2016-10-10 09:51:13, order_approved_at: 2016-10-18 15:19:11, processing_time_hours: 197.4661111111111111
59. order_id: fd1272ba40a94a5fbc6e9548a8486867, order_status: delivered, order_purchase_timestamp: 2017-11-01 09:57:54, order_approved_at: 2017-11-09 15:15:38, processing_time_hours: 197.2955555555555556
60. order_id: cb5b5d9d111d57e734d8e22a09ddffaa, order_status: delivered, order_purchase_timestamp: 2017-07-18 10:53:53, order_approved_at: 2017-07-26 15:55:21, processing_time_hours: 197.0244444444444444
61. order_id: fca9e6e37a25eabc4dead1228fca9d27, order_status: delivered, order_purchase_timestamp: 2018-02-08 11:54:16, order_approved_at: 2018-02-16 16:35:41, processing_time_hours: 196.6902777777777778
62. order_id: e885d4ac4244bd62acf41453b5684377, order_status: delivered, order_purchase_timestamp: 2018-01-18 13:22:26, order_approved_at: 2018-01-26 17:03:34, processing_time_hours: 195.6855555555555556
63. order_id: 8194f59689e6129d3bd13dce90d86c2b, order_status: delivered, order_purchase_timestamp: 2018-01-18 15:29:09, order_approved_at: 2018-01-26 17:03:36, processing_time_hours: 193.5741666666666667
64. order_id: 23c7702588b2b08f1bf4fbdd15f19343, order_status: delivered, order_purchase_timestamp: 2017-03-22 17:52:17, order_approved_at: 2017-03-30 19:10:20, processing_time_hours: 193.3008333333333333
65. order_id: 3e30da31e3bf405f3a0b771a7d935322, order_status: delivered, order_purchase_timestamp: 2018-01-18 19:33:23, order_approved_at: 2018-01-26 17:03:37, processing_time_hours: 189.5038888888888889
66. order_id: 94bde44a48f191d7175f67eb93b9ed67, order_status: canceled, order_purchase_timestamp: 2017-02-01 17:31:17, order_approved_at: 2017-02-09 14:43:11, processing_time_hours: 189.1983333333333333
67. order_id: 4bbe949608f669144f0db3f8cde75cd7, order_status: unavailable, order_purchase_timestamp: 2017-09-05 14:22:59, order_approved_at: 2017-09-13 11:10:20, processing_time_hours: 188.7891666666666667
68. order_id: c064f1af2555ae9dbb9efd65b5381684, order_status: delivered, order_purchase_timestamp: 2018-01-18 20:47:13, order_approved_at: 2018-01-26 17:03:42, processing_time_hours: 188.2747222222222222
69. order_id: 24016340d5156f96d37500c78a7fe591, order_status: delivered, order_purchase_timestamp: 2017-08-17 15:44:39, order_approved_at: 2017-08-25 09:30:19, processing_time_hours: 185.7611111111111111
70. order_id: e7d3f9457c859cd5b63a25a4c2afb2e0, order_status: delivered, order_purchase_timestamp: 2018-01-18 23:26:10, order_approved_at: 2018-01-26 17:03:27, processing_time_hours: 185.6213888888888889
71. order_id: b9555bd71c90a01a953792e5f2af95c5, order_status: delivered, order_purchase_timestamp: 2017-03-30 19:48:12, order_approved_at: 2017-04-07 10:35:25, processing_time_hours: 182.7869444444444444
72. order_id: a9880f780c93ecdc4a6c6cfbeec27925, order_status: delivered, order_purchase_timestamp: 2018-04-06 09:36:48, order_approved_at: 2018-04-13 17:15:23, processing_time_hours: 175.6430555555555556
73. order_id: 26874945bcbf47606ab08580cf923693, order_status: delivered, order_purchase_timestamp: 2018-02-09 00:56:49, order_approved_at: 2018-02-16 08:10:29, processing_time_hours: 175.2277777777777778
74. order_id: e88f99d9e433a6a8968b38b7dd55b080, order_status: delivered, order_purchase_timestamp: 2018-01-19 11:05:41, order_approved_at: 2018-01-26 17:03:53, processing_time_hours: 173.9700000000000000
75. order_id: 708d8f65b7d44e636e299978fa1f11a4, order_status: delivered, order_purchase_timestamp: 2017-12-20 15:14:17, order_approved_at: 2017-12-27 17:37:20, processing_time_hours: 170.3841666666666667
76. order_id: 07bd0c7e13ac7c3a408dd3bc8f18fc78, order_status: delivered, order_purchase_timestamp: 2018-01-30 15:18:07, order_approved_at: 2018-02-06 17:15:32, processing_time_hours: 169.9569444444444444
77. order_id: 5000db43709b8a1e13f508043ff281c9, order_status: delivered, order_purchase_timestamp: 2018-04-17 17:08:56, order_approved_at: 2018-04-24 18:58:37, processing_time_hours: 169.8280555555555556
78. order_id: 1e65b448bd96abe8434d64bc0ae4d609, order_status: delivered, order_purchase_timestamp: 2017-08-21 17:06:20, order_approved_at: 2017-08-28 18:45:12, processing_time_hours: 169.6477777777777778
79. order_id: 02951078a21a2d9341ea16089a4d5031, order_status: delivered, order_purchase_timestamp: 2017-03-16 15:16:53, order_approved_at: 2017-03-23 16:10:18, processing_time_hours: 168.8902777777777778
80. order_id: 6e8ff76e6abbdfadc22d6569bf5b1ae8, order_status: delivered, order_purchase_timestamp: 2017-07-26 10:51:20, order_approved_at: 2017-08-02 11:25:48, processing_time_hours: 168.5744444444444444
81. order_id: e84484718ecfbc4f6c98105b691b2bd8, order_status: delivered, order_purchase_timestamp: 2018-02-09 07:25:50, order_approved_at: 2018-02-16 07:50:26, processing_time_hours: 168.4100000000000000
82. order_id: 732ea3eb55f0450b5da6cd76607c4504, order_status: delivered, order_purchase_timestamp: 2017-05-18 09:56:49, order_approved_at: 2017-05-25 09:35:15, processing_time_hours: 167.6405555555555556
83. order_id: d7f1fc795c94efd3a00141a5f8a2c9d7, order_status: delivered, order_purchase_timestamp: 2018-08-13 15:24:41, order_approved_at: 2018-08-20 14:12:55, processing_time_hours: 166.8038888888888889
84. order_id: f53a2d931e67099351c1cb7cbd9b5e94, order_status: delivered, order_purchase_timestamp: 2017-11-02 18:41:53, order_approved_at: 2017-11-09 15:15:31, processing_time_hours: 164.5605555555555556
85. order_id: 2df2cf698fc8633cca4e90baa85fdf0b, order_status: delivered, order_purchase_timestamp: 2017-03-23 22:17:44, order_approved_at: 2017-03-30 18:45:08, processing_time_hours: 164.4566666666666667
86. order_id: 465c2e1bee4561cb39e0db8c5993aafc, order_status: delivered, order_purchase_timestamp: 2018-02-14 16:34:27, order_approved_at: 2018-02-21 12:28:15, processing_time_hours: 163.8966666666666667
87. order_id: f778c08595fa3873bb689febdda2c509, order_status: delivered, order_purchase_timestamp: 2017-03-17 23:06:09, order_approved_at: 2017-03-24 18:03:20, processing_time_hours: 162.9530555555555556
88. order_id: 6eace5a496456d346454761a9fc00dd2, order_status: delivered, order_purchase_timestamp: 2018-08-13 15:17:31, order_approved_at: 2018-08-20 09:21:49, processing_time_hours: 162.0716666666666667
89. order_id: 737c93fc3e93b56ba3055202da5b219a, order_status: delivered, order_purchase_timestamp: 2018-06-29 00:02:57, order_approved_at: 2018-07-05 16:08:15, processing_time_hours: 160.0883333333333333
90. order_id: 30af846e182aa12984d1454721036e8e, order_status: delivered, order_purchase_timestamp: 2017-11-29 23:33:23, order_approved_at: 2017-12-06 14:56:19, processing_time_hours: 159.3822222222222222
91. order_id: 96ddb703f0673d920cf28984cdcf0139, order_status: delivered, order_purchase_timestamp: 2017-02-24 11:13:35, order_approved_at: 2017-03-03 02:25:32, processing_time_hours: 159.1991666666666667
92. order_id: d0d17a407c7f31de95587389db1cad3d, order_status: delivered, order_purchase_timestamp: 2018-02-09 18:08:32, order_approved_at: 2018-02-16 08:20:24, processing_time_hours: 158.1977777777777778
93. order_id: 7ccdf2db4cb80263b5535a6cfad598e8, order_status: delivered, order_purchase_timestamp: 2018-03-05 22:26:48, order_approved_at: 2018-03-12 11:50:45, processing_time_hours: 157.3991666666666667
94. order_id: 31da75f0c78b03d446ea7342a6c002b9, order_status: delivered, order_purchase_timestamp: 2018-07-05 14:55:38, order_approved_at: 2018-07-12 04:10:14, processing_time_hours: 157.2433333333333333
95. order_id: e7fbf44c317d9ac6b87b0330fed92f1b, order_status: delivered, order_purchase_timestamp: 2017-08-15 20:44:02, order_approved_at: 2017-08-22 08:45:24, processing_time_hours: 156.0227777777777778
96. order_id: 8770d612f74d5015ceb2d739911887a1, order_status: delivered, order_purchase_timestamp: 2018-07-05 16:10:28, order_approved_at: 2018-07-12 03:26:15, processing_time_hours: 155.2630555555555556
97. order_id: 814948d5529f58dfc7bf33ac7f6adba4, order_status: delivered, order_purchase_timestamp: 2018-02-12 21:43:34, order_approved_at: 2018-02-19 08:55:34, processing_time_hours: 155.2000000000000000
98. order_id: 7f8d9a73c2b510f9627ac02f1a79c789, order_status: delivered, order_purchase_timestamp: 2018-08-14 08:27:47, order_approved_at: 2018-08-20 19:09:57, processing_time_hours: 154.7027777777777778
99. order_id: 59c51bdf0c3270d962625e5ebbe22fb1, order_status: delivered, order_purchase_timestamp: 2018-06-29 05:26:29, order_approved_at: 2018-07-05 16:08:11, processing_time_hours: 154.6950000000000000
100. order_id: e1dce34866435728863bd0fb8930d737, order_status: delivered, order_purchase_timestamp: 2017-12-29 12:49:47, order_approved_at: 2018-01-04 23:17:29, processing_time_hours: 154.4616666666666667
101. order_id: 8ef63805460994636446a1e1012ee8b6, order_status: delivered, order_purchase_timestamp: 2018-07-05 17:24:53, order_approved_at: 2018-07-12 03:26:12, processing_time_hours: 154.0219444444444444
102. order_id: 5de443f7adc75b72230b61e63ce5007a, order_status: delivered, order_purchase_timestamp: 2018-06-29 08:12:42, order_approved_at: 2018-07-05 16:02:24, processing_time_hours: 151.8283333333333333
103. order_id: 20baf04dd07db849cacb72e8cc0447aa, order_status: delivered, order_purchase_timestamp: 2018-07-05 19:26:00, order_approved_at: 2018-07-12 03:06:16, processing_time_hours: 151.6711111111111111
104. order_id: f03bbe221b9e5bae09eccab6a0c4120e, order_status: delivered, order_purchase_timestamp: 2017-11-03 11:24:36, order_approved_at: 2017-11-09 18:15:32, processing_time_hours: 150.8488888888888889
105. order_id: 26b5d26aa210d44b8a3f2310d32643f6, order_status: delivered, order_purchase_timestamp: 2018-07-05 21:49:33, order_approved_at: 2018-07-12 03:06:15, processing_time_hours: 149.2783333333333333
106. order_id: 3f6a06dd65ecc8c3c8bf73dd9f5ade29, order_status: delivered, order_purchase_timestamp: 2018-06-29 11:19:19, order_approved_at: 2018-07-05 16:04:10, processing_time_hours: 148.7475000000000000
107. order_id: 489c4ff5e823eea8d6652bfc3dc1b544, order_status: delivered, order_purchase_timestamp: 2017-03-24 14:01:51, order_approved_at: 2017-03-30 18:45:13, processing_time_hours: 148.7227777777777778
108. order_id: d469b51abffc6d74299c8a0a56db5314, order_status: delivered, order_purchase_timestamp: 2017-01-20 17:41:58, order_approved_at: 2017-01-26 20:21:56, processing_time_hours: 146.6661111111111111
109. order_id: d4d70141598f959f855ea0b6266ca5c6, order_status: delivered, order_purchase_timestamp: 2017-12-29 20:39:39, order_approved_at: 2018-01-04 23:17:32, processing_time_hours: 146.6313888888888889
110. order_id: cea25ef7695cbbf27888da010e3ddd2a, order_status: delivered, order_purchase_timestamp: 2018-06-29 14:24:39, order_approved_at: 2018-07-05 16:06:14, processing_time_hours: 145.6930555555555556
111. order_id: c9645496b715730a1a5d07eb97a6bf6b, order_status: delivered, order_purchase_timestamp: 2017-01-18 14:56:47, order_approved_at: 2017-01-24 15:25:11, processing_time_hours: 144.4733333333333333
112. order_id: 8883dd20e652369652c1abd7a411788f, order_status: delivered, order_purchase_timestamp: 2018-08-14 14:24:51, order_approved_at: 2018-08-20 14:36:32, processing_time_hours: 144.1947222222222222
113. order_id: 8af8d03ef1d18e7e6c062eb26d9cb36e, order_status: delivered, order_purchase_timestamp: 2017-11-25 10:48:32, order_approved_at: 2017-12-01 10:18:22, processing_time_hours: 143.4972222222222222
114. order_id: 66b7e4ff35d62613a10899d4eb442216, order_status: delivered, order_purchase_timestamp: 2018-07-23 00:39:48, order_approved_at: 2018-07-28 23:31:04, processing_time_hours: 142.8544444444444444
115. order_id: acc128e9293460781736208a647dd87c, order_status: delivered, order_purchase_timestamp: 2018-01-30 01:00:05, order_approved_at: 2018-02-04 23:31:38, processing_time_hours: 142.5258333333333333
116. order_id: 9675440ebf61a1a3482cc6308e3ebd28, order_status: delivered, order_purchase_timestamp: 2018-08-18 23:35:23, order_approved_at: 2018-08-24 22:05:08, processing_time_hours: 142.4958333333333333
117. order_id: 0a7beb2015960a4d8c4ec8bbde5a1f5f, order_status: shipped, order_purchase_timestamp: 2018-01-20 18:43:17, order_approved_at: 2018-01-26 17:03:49, processing_time_hours: 142.3422222222222222
118. order_id: 92fe083783a81f62019d6dcce018a85f, order_status: delivered, order_purchase_timestamp: 2018-07-22 01:27:12, order_approved_at: 2018-07-27 23:31:15, processing_time_hours: 142.0675000000000000
119. order_id: 942cb81b8e0a2f33510159729f69d8b1, order_status: delivered, order_purchase_timestamp: 2017-01-24 11:24:20, order_approved_at: 2017-01-30 09:28:02, processing_time_hours: 142.0616666666666667
120. order_id: 9fa4fbddf06979761ad62c2cb6fcd315, order_status: delivered, order_purchase_timestamp: 2018-06-29 18:27:05, order_approved_at: 2018-07-05 16:11:45, processing_time_hours: 141.7444444444444444
121. order_id: 09b6daf7c780e789668ee3b7f4bda1c5, order_status: delivered, order_purchase_timestamp: 2018-06-29 18:20:57, order_approved_at: 2018-07-05 16:04:53, processing_time_hours: 141.7322222222222222
122. order_id: 2f64f730b534c45e97b887c36a0ea0fd, order_status: delivered, order_purchase_timestamp: 2018-06-29 18:52:27, order_approved_at: 2018-07-05 16:01:00, processing_time_hours: 141.1425000000000000
123. order_id: 017cf0b342401318dcaeb25478e13a6f, order_status: delivered, order_purchase_timestamp: 2017-12-30 02:09:39, order_approved_at: 2018-01-04 23:17:29, processing_time_hours: 141.1305555555555556
124. order_id: 76a948cd55bf22799753720d4545dd2d, order_status: delivered, order_purchase_timestamp: 2018-01-30 02:41:30, order_approved_at: 2018-02-04 23:31:46, processing_time_hours: 140.8377777777777778
125. order_id: 85bdbf544abea637f0ed3c856bd0a0ca, order_status: delivered, order_purchase_timestamp: 2018-06-29 19:15:06, order_approved_at: 2018-07-05 16:02:57, processing_time_hours: 140.7975000000000000
126. order_id: c32295e5877c879f156074c086bb536e, order_status: delivered, order_purchase_timestamp: 2017-12-30 02:36:20, order_approved_at: 2018-01-04 23:17:35, processing_time_hours: 140.6875000000000000
127. order_id: 6e821c1f2504ac8ae2e154ab1e4f933e, order_status: delivered, order_purchase_timestamp: 2017-09-06 10:54:12, order_approved_at: 2017-09-12 07:35:19, processing_time_hours: 140.6852777777777778
128. order_id: 470d06109882a6e13eccc99f24dce797, order_status: delivered, order_purchase_timestamp: 2018-02-10 11:17:23, order_approved_at: 2018-02-16 07:55:44, processing_time_hours: 140.6391666666666667
129. order_id: 5981ae276b32c4b5d69ed39efd08d0a8, order_status: delivered, order_purchase_timestamp: 2017-04-26 02:02:47, order_approved_at: 2017-05-01 22:34:08, processing_time_hours: 140.5225000000000000
130. order_id: 3322def88876cefd455c98956089a062, order_status: delivered, order_purchase_timestamp: 2018-06-29 20:09:38, order_approved_at: 2018-07-05 16:24:37, processing_time_hours: 140.2497222222222222
131. order_id: ca93131de2c3fc58df457b40df4aff78, order_status: delivered, order_purchase_timestamp: 2017-11-24 19:28:28, order_approved_at: 2017-11-30 15:14:23, processing_time_hours: 139.7652777777777778
132. order_id: e55fa3385fa77f6be6a0041c5daf2fb6, order_status: unavailable, order_purchase_timestamp: 2018-08-01 03:54:30, order_approved_at: 2018-08-06 23:31:35, processing_time_hours: 139.6180555555555556
133. order_id: 327e9810cdacade85a92b9228ab04d1a, order_status: delivered, order_purchase_timestamp: 2017-11-24 19:41:28, order_approved_at: 2017-11-30 15:13:42, processing_time_hours: 139.5372222222222222
134. order_id: 5000591796ae43a6d7638ee69e51ac6e, order_status: delivered, order_purchase_timestamp: 2017-03-02 14:06:01, order_approved_at: 2017-03-08 09:15:19, processing_time_hours: 139.1550000000000000
135. order_id: b6403787453855be6332055dc2d6bde9, order_status: delivered, order_purchase_timestamp: 2017-12-13 15:22:11, order_approved_at: 2017-12-19 10:31:29, processing_time_hours: 139.1550000000000000
136. order_id: 132f1e724165a07f6362532bfb97486e, order_status: approved, order_purchase_timestamp: 2017-04-25 01:25:34, order_approved_at: 2017-04-30 20:32:41, processing_time_hours: 139.1186111111111111
137. order_id: 895764a4b54b7193c02aa784fabbcaeb, order_status: delivered, order_purchase_timestamp: 2018-02-10 13:23:35, order_approved_at: 2018-02-16 08:07:08, processing_time_hours: 138.7258333333333333
138. order_id: d8ff993abef623e4c9956f245c4345e9, order_status: delivered, order_purchase_timestamp: 2018-08-04 04:59:37, order_approved_at: 2018-08-09 23:31:23, processing_time_hours: 138.5294444444444444
139. order_id: b82cf5fe4911adae1a6d2c4b171ec237, order_status: delivered, order_purchase_timestamp: 2018-06-29 21:56:38, order_approved_at: 2018-07-05 16:04:23, processing_time_hours: 138.1291666666666667
140. order_id: 1e89e2312f1a1fd948c615602f200480, order_status: shipped, order_purchase_timestamp: 2018-06-29 22:00:43, order_approved_at: 2018-07-05 16:05:46, processing_time_hours: 138.0841666666666667
141. order_id: 1452442fe3e8cc6d3a1a8d8fc92dc019, order_status: delivered, order_purchase_timestamp: 2018-04-19 00:41:11, order_approved_at: 2018-04-24 18:37:45, processing_time_hours: 137.9427777777777778
142. order_id: 6d70b44b2d0742e51c0434faba7c9afe, order_status: delivered, order_purchase_timestamp: 2018-07-21 05:48:37, order_approved_at: 2018-07-26 23:31:41, processing_time_hours: 137.7177777777777778
143. order_id: a6d4e95420d65bd5f299dc95d3493e0d, order_status: unavailable, order_purchase_timestamp: 2018-07-23 06:11:11, order_approved_at: 2018-07-28 23:31:01, processing_time_hours: 137.3305555555555556
144. order_id: 1536003b9af6a526e0d02b8cd13fd2af, order_status: delivered, order_purchase_timestamp: 2018-06-29 23:30:20, order_approved_at: 2018-07-05 16:14:02, processing_time_hours: 136.7283333333333333
145. order_id: 2daee070f2042c8b7a8e9fdde778a31a, order_status: delivered, order_purchase_timestamp: 2018-06-29 23:30:20, order_approved_at: 2018-07-05 16:11:40, processing_time_hours: 136.6888888888888889
146. order_id: 13ce7f4beebc91755492c12e77093d10, order_status: delivered, order_purchase_timestamp: 2018-05-30 11:33:10, order_approved_at: 2018-06-05 04:12:50, processing_time_hours: 136.6611111111111111
147. order_id: 5aae98560d0aff8d326d8f5767979e22, order_status: delivered, order_purchase_timestamp: 2018-07-05 10:58:26, order_approved_at: 2018-07-11 03:30:15, processing_time_hours: 136.5302777777777778
148. order_id: 5bd56b595a9879fb7f67ae6253450883, order_status: delivered, order_purchase_timestamp: 2018-05-30 12:06:52, order_approved_at: 2018-06-05 04:35:10, processing_time_hours: 136.4716666666666667
149. order_id: 9fff263519b16922d71e07a6706a0ef8, order_status: delivered, order_purchase_timestamp: 2017-02-25 10:09:02, order_approved_at: 2017-03-03 02:30:29, processing_time_hours: 136.3575000000000000
150. order_id: 897b4da63b6edde1a33a9fb7caf1dd10, order_status: unavailable, order_purchase_timestamp: 2018-07-30 07:38:21, order_approved_at: 2018-08-04 23:31:16, processing_time_hours: 135.8819444444444444
151. order_id: 743277e5089af7df0cbd543c93e5d852, order_status: delivered, order_purchase_timestamp: 2018-07-06 11:43:14, order_approved_at: 2018-07-12 03:26:04, processing_time_hours: 135.7138888888888889
152. order_id: b2642502bf8864ede538c80b67275178, order_status: delivered, order_purchase_timestamp: 2018-06-30 00:46:29, order_approved_at: 2018-07-05 16:22:31, processing_time_hours: 135.6005555555555556
153. order_id: 7ac04774ea7d5faea51621289bb084c4, order_status: delivered, order_purchase_timestamp: 2018-02-15 20:59:41, order_approved_at: 2018-02-21 12:10:34, processing_time_hours: 135.1813888888888889
154. order_id: 1d84d00f6d2334d63f35ba528cd0d99d, order_status: delivered, order_purchase_timestamp: 2018-02-10 16:50:42, order_approved_at: 2018-02-16 07:56:27, processing_time_hours: 135.0958333333333333
155. order_id: 4e790ef1ee5dca2f0de38704d806e45d, order_status: delivered, order_purchase_timestamp: 2018-06-30 01:23:27, order_approved_at: 2018-07-05 16:05:22, processing_time_hours: 134.6986111111111111
156. order_id: 0f91be4a9bf9ffd2c1ace53b9e5dd9e2, order_status: delivered, order_purchase_timestamp: 2017-01-18 02:01:36, order_approved_at: 2017-01-23 16:43:02, processing_time_hours: 134.6905555555555556
157. order_id: 6df6c9c9af6ef75b4f06f8a7b9f47e9c, order_status: delivered, order_purchase_timestamp: 2018-07-23 08:50:48, order_approved_at: 2018-07-28 23:31:06, processing_time_hours: 134.6716666666666667
158. order_id: a771d79ec4b8d059bfb6e773f290cc1d, order_status: delivered, order_purchase_timestamp: 2018-07-21 08:57:30, order_approved_at: 2018-07-26 23:32:34, processing_time_hours: 134.5844444444444444
159. order_id: 387c2cbba26c5cfe21c60a8f2208a78d, order_status: delivered, order_purchase_timestamp: 2017-05-04 08:01:35, order_approved_at: 2017-05-09 22:32:39, processing_time_hours: 134.5177777777777778
160. order_id: 0872f22df707596feed1639609f6eba7, order_status: delivered, order_purchase_timestamp: 2018-01-30 09:00:45, order_approved_at: 2018-02-04 23:31:47, processing_time_hours: 134.5172222222222222
161. order_id: 326fa4ef13e06290f3b142da7663d4af, order_status: delivered, order_purchase_timestamp: 2018-08-06 09:33:48, order_approved_at: 2018-08-11 23:31:58, processing_time_hours: 133.9694444444444444
162. order_id: 05d657dbf5a4b2e7a685903cc8bb03f0, order_status: delivered, order_purchase_timestamp: 2018-01-30 09:37:46, order_approved_at: 2018-02-04 23:31:34, processing_time_hours: 133.8966666666666667
163. order_id: f222c56f035b47dfa1e069a88235d730, order_status: delivered, order_purchase_timestamp: 2018-01-30 09:43:45, order_approved_at: 2018-02-04 23:31:47, processing_time_hours: 133.8005555555555556
164. order_id: 84d1f58195cae334b50f9088b38b3495, order_status: delivered, order_purchase_timestamp: 2017-04-26 08:45:44, order_approved_at: 2017-05-01 22:33:38, processing_time_hours: 133.7983333333333333
165. order_id: 1d1e77334238a731c494f066a6c0d500, order_status: delivered, order_purchase_timestamp: 2017-09-15 08:51:48, order_approved_at: 2017-09-20 22:36:09, processing_time_hours: 133.7391666666666667
166. order_id: 73696c4354b75af323cf793aa474acfc, order_status: delivered, order_purchase_timestamp: 2017-05-05 07:48:46, order_approved_at: 2017-05-10 21:32:36, processing_time_hours: 133.7305555555555556
167. order_id: 38e0cb80c67af61efd491a83aed8c8be, order_status: delivered, order_purchase_timestamp: 2018-07-20 09:55:09, order_approved_at: 2018-07-25 23:32:02, processing_time_hours: 133.6147222222222222
168. order_id: 69fd1a4dd8b96b9ab0dc82b95be21efd, order_status: unavailable, order_purchase_timestamp: 2018-07-31 09:55:46, order_approved_at: 2018-08-05 23:30:50, processing_time_hours: 133.5844444444444444
169. order_id: c1b86a370f491b37cc3adb8ef0a21fe5, order_status: delivered, order_purchase_timestamp: 2017-03-21 10:09:06, order_approved_at: 2017-03-26 23:32:51, processing_time_hours: 133.3958333333333333
170. order_id: fb114a7255e9d0f59416a80b564638d4, order_status: delivered, order_purchase_timestamp: 2017-05-04 09:13:21, order_approved_at: 2017-05-09 22:32:27, processing_time_hours: 133.3183333333333333
171. order_id: 49b25de91ca7ebe3b4b740b332b5e0a0, order_status: delivered, order_purchase_timestamp: 2018-01-29 10:15:59, order_approved_at: 2018-02-03 23:31:46, processing_time_hours: 133.2630555555555556
172. order_id: 54c2d9b070b38364a06b2b3066032112, order_status: delivered, order_purchase_timestamp: 2017-03-21 10:22:53, order_approved_at: 2017-03-26 23:32:46, processing_time_hours: 133.1647222222222222
173. order_id: 48ddd457f76f31a99e60ac8007bc8b28, order_status: delivered, order_purchase_timestamp: 2018-01-30 10:24:25, order_approved_at: 2018-02-04 23:31:38, processing_time_hours: 133.1202777777777778
174. order_id: 833fbc971cf15276b9fa3a392f73b4e6, order_status: delivered, order_purchase_timestamp: 2017-05-02 10:28:05, order_approved_at: 2017-05-07 23:32:50, processing_time_hours: 133.0791666666666667
175. order_id: 097c2a2e5ea719c510238bad5d902cef, order_status: delivered, order_purchase_timestamp: 2018-02-09 14:48:12, order_approved_at: 2018-02-15 03:50:53, processing_time_hours: 133.0447222222222222
176. order_id: 27cccab59c02b5c742ec003898dfabec, order_status: delivered, order_purchase_timestamp: 2018-07-23 10:31:16, order_approved_at: 2018-07-28 23:31:04, processing_time_hours: 132.9966666666666667
177. order_id: ebfd75154f8fdbc98038250a80a41875, order_status: delivered, order_purchase_timestamp: 2017-04-26 09:34:47, order_approved_at: 2017-05-01 22:32:53, processing_time_hours: 132.9683333333333333
178. order_id: 9cc8a145d8be894ab07cdbd8503c4887, order_status: delivered, order_purchase_timestamp: 2017-11-28 10:44:35, order_approved_at: 2017-12-03 23:36:19, processing_time_hours: 132.8622222222222222
179. order_id: 81f667f73efffe2771ab8b77d326f1ee, order_status: delivered, order_purchase_timestamp: 2018-02-14 21:17:34, order_approved_at: 2018-02-20 10:07:45, processing_time_hours: 132.8363888888888889
180. order_id: 5990719adf4d9d93dd602a9e14879bc3, order_status: delivered, order_purchase_timestamp: 2018-01-30 10:50:41, order_approved_at: 2018-02-04 23:31:36, processing_time_hours: 132.6819444444444444
181. order_id: a729a5577a90047af954bb2210ebca66, order_status: delivered, order_purchase_timestamp: 2018-07-23 10:52:58, order_approved_at: 2018-07-28 23:30:57, processing_time_hours: 132.6330555555555556
182. order_id: 10710544d8adf2b743de71711a372fa2, order_status: delivered, order_purchase_timestamp: 2017-02-24 15:13:35, order_approved_at: 2017-03-02 03:50:27, processing_time_hours: 132.6144444444444444
183. order_id: a1f5afc5fe7a4ee4bef93aab1e95772f, order_status: delivered, order_purchase_timestamp: 2017-05-06 11:09:15, order_approved_at: 2017-05-11 23:31:25, processing_time_hours: 132.3694444444444444
184. order_id: 9dcef670d743a0deba5b2598d7121679, order_status: delivered, order_purchase_timestamp: 2018-01-30 11:10:42, order_approved_at: 2018-02-04 23:31:46, processing_time_hours: 132.3511111111111111
185. order_id: 656dbb4c6b66cb06a7ffd47823b6345a, order_status: delivered, order_purchase_timestamp: 2018-06-08 11:15:40, order_approved_at: 2018-06-13 23:32:29, processing_time_hours: 132.2802777777777778
186. order_id: 1dcb629bf4ae95dddc7ec77ff8fcdd4a, order_status: delivered, order_purchase_timestamp: 2018-01-30 11:17:47, order_approved_at: 2018-02-04 23:31:46, processing_time_hours: 132.2330555555555556
187. order_id: 97823d6731e59cd6b4f9d3ea113a976e, order_status: delivered, order_purchase_timestamp: 2018-07-23 11:26:36, order_approved_at: 2018-07-28 23:30:58, processing_time_hours: 132.0727777777777778
188. order_id: b635cbb9f7c2bc5de438f7429b8490e5, order_status: unavailable, order_purchase_timestamp: 2018-07-31 11:26:30, order_approved_at: 2018-08-05 23:30:50, processing_time_hours: 132.0722222222222222
189. order_id: 4df92d82d79c3b52c7138679fa9b07fc, order_status: delivered, order_purchase_timestamp: 2018-07-24 11:32:11, order_approved_at: 2018-07-29 23:30:52, processing_time_hours: 131.9780555555555556
190. order_id: d5292f531e571c16fcd72df9fc07336d, order_status: delivered, order_purchase_timestamp: 2017-04-26 10:48:55, order_approved_at: 2017-05-01 22:34:22, processing_time_hours: 131.7575000000000000
191. order_id: a49dc0169f9bb6d3ac9829bdebd12299, order_status: delivered, order_purchase_timestamp: 2018-07-21 11:46:28, order_approved_at: 2018-07-26 23:31:27, processing_time_hours: 131.7497222222222222
192. order_id: bc1b85147b5edbb7cbefcf5c1bd5ded9, order_status: delivered, order_purchase_timestamp: 2018-07-24 11:50:06, order_approved_at: 2018-07-29 23:30:54, processing_time_hours: 131.6800000000000000
193. order_id: 846de1a3e7ca6bf29333e1db02040ab6, order_status: delivered, order_purchase_timestamp: 2018-01-30 11:51:07, order_approved_at: 2018-02-04 23:31:38, processing_time_hours: 131.6752777777777778
194. order_id: 3d85885db63d8328e4dbaa59804ad1ee, order_status: delivered, order_purchase_timestamp: 2018-07-22 11:51:42, order_approved_at: 2018-07-27 23:31:16, processing_time_hours: 131.6594444444444444
195. order_id: 9c9caabac80e005ba36cb7c06afc0fe3, order_status: delivered, order_purchase_timestamp: 2018-06-30 04:40:59, order_approved_at: 2018-07-05 16:11:04, processing_time_hours: 131.5013888888888889
196. order_id: 2a16183656d9858dd244568f629e8c13, order_status: delivered, order_purchase_timestamp: 2017-04-20 10:11:32, order_approved_at: 2017-04-25 21:36:57, processing_time_hours: 131.4236111111111111
197. order_id: e713dc6c1f73c883bc8e42bff335eb8e, order_status: delivered, order_purchase_timestamp: 2018-02-10 20:40:34, order_approved_at: 2018-02-16 07:55:52, processing_time_hours: 131.2550000000000000
198. order_id: 559e3bc7d9dd587ccb23c90505340ee1, order_status: delivered, order_purchase_timestamp: 2018-04-19 06:56:40, order_approved_at: 2018-04-24 18:05:00, processing_time_hours: 131.1388888888888889
199. order_id: 2d3b451fae025eca7a05641e05e452bb, order_status: delivered, order_purchase_timestamp: 2018-07-23 12:35:34, order_approved_at: 2018-07-28 23:31:07, processing_time_hours: 130.9258333333333333
200. order_id: 172f9fee6f5a8b311968d1c27b336438, order_status: delivered, order_purchase_timestamp: 2018-07-05 16:40:36, order_approved_at: 2018-07-11 03:30:22, processing_time_hours: 130.8294444444444444
```

#### 📊 Metadata

- **sql:** SELECT o.order_id, o.order_status, o.order_purchase_timestamp, o.order_approved_at, EXTRACT(EPOCH FROM (o.order_approved_at - o.order_purchase_timestamp)) / 3600 AS processing_time_hours FROM analytics.orders o WHERE o.order_approved_at IS NOT NULL ORDER BY processing_time_hours DESC LIMIT 200
- **row_count:** 200
- **limit_applied:** True

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-11"></a>
### Query 11

#### 📝 Input

- **Query:** Qual é a taxa de pedidos entregues no prazo estimado, segmentada por região?

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.9
- **Reason:** delivery performance rate by region segmentation
- **Thread ID:** `f3c8df72-a465-4c2e-9d73-b271cc9a9017`

#### 💬 Response

```
Taxa de pedidos entregues no prazo estimado por região:
  AC: 95,06%
  AL: 73,12%
  AM: 93,92%
  AP: 94,12%
  BA: 82,81%
  CE: 81,06%
  DF: 90,33%
  ES: 86,13%
  GO: 88,96%
  MA: 77,11%
  MG: 92,11%
  MS: 86,71%
  MT: 91,07%
  PA: 85,03%
  PB: 85,82%
  PE: 86,02%
  PI: 80,81%
  PR: 92,71%
  RJ: 83,17%
  RN: 87,22%
  RO: 93,28%
  RR: 78,26%
  RS: 90,78%
  SC: 88,01%
  SE: 81,14%
  SP: 91,29%
  TO: 85,36%
```

#### 📊 Metadata

- **sql:** SELECT c.customer_state, 100.0 * SUM(CASE WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date THEN 1 END) / NULLIF(COUNT(*), 0) AS on_time_delivery_rate FROM analytics.orders o JOIN analytics.customers c ON o.customer_id = c.customer_id GROUP BY c.customer_state ORDER BY c.customer_state
- **row_count:** 27
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-12"></a>
### Query 12

#### 📝 Input

- **Query:** Compare a eficiência logística entre diferentes faixas de CEP de origem dos vendedores

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.85
- **Reason:** compare logistics efficiency by seller zip code ranges
- **Thread ID:** `fafa9647-a1dc-4237-bcca-5e15426dcda5`

#### 💬 Response

```
Análise da eficiência logística por faixa de CEP de origem dos vendedores:

14940: 7.750 pedidos, Receita total: R$ 762.274,01
5849: 2.047 pedidos, Receita total: R$ 152.709,22
15025: 2.008 pedidos, Receita total: R$ 151.335,05
9015: 1.781 pedidos, Receita total: R$ 131.464,58
13405: 1.567 pedidos, Receita total: R$ 192.669,28
4782: 1.518 pedidos, Receita total: R$ 163.698,71
8577: 1.456 pedidos, Receita total: R$ 259.289,99
3204: 1.428 pedidos, Receita total: R$ 172.860,69
4160: 1.229 pedidos, Receita total: R$ 58.564,99
13232: 1.195 pedidos, Receita total: R$ 124.650,04

Total: 2000 pedidos distribuídos entre diversas faixas de CEP. A faixa 14940 se destaca com o maior número de pedidos e receita total significativa.

Dados completos:
1. seller_zip_code_prefix: 14,940, total_orders: 7,750, total_revenue: 762274.01
2. seller_zip_code_prefix: 5,849, total_orders: 2,047, total_revenue: 152709.22
3. seller_zip_code_prefix: 15,025, total_orders: 2,008, total_revenue: 151335.05
4. seller_zip_code_prefix: 9,015, total_orders: 1,781, total_revenue: 131464.58
5. seller_zip_code_prefix: 13,405, total_orders: 1,567, total_revenue: 192669.28
6. seller_zip_code_prefix: 4,782, total_orders: 1,518, total_revenue: 163698.71
7. seller_zip_code_prefix: 8,577, total_orders: 1,456, total_revenue: 259289.99
8. seller_zip_code_prefix: 3,204, total_orders: 1,428, total_revenue: 172860.69
9. seller_zip_code_prefix: 4,160, total_orders: 1,229, total_revenue: 58564.99
10. seller_zip_code_prefix: 13,232, total_orders: 1,195, total_revenue: 124650.04
11. seller_zip_code_prefix: 3,426, total_orders: 1,171, total_revenue: 162648.38
12. seller_zip_code_prefix: 14,840, total_orders: 1,156, total_revenue: 249640.70
13. seller_zip_code_prefix: 1,212, total_orders: 1,024, total_revenue: 33345.19
14. seller_zip_code_prefix: 25,645, total_orders: 798, total_revenue: 128909.71
15. seller_zip_code_prefix: 31,255, total_orders: 793, total_revenue: 50799.64
16. seller_zip_code_prefix: 12,327, total_orders: 784, total_revenue: 89824.61
17. seller_zip_code_prefix: 37,175, total_orders: 770, total_revenue: 133745.25
18. seller_zip_code_prefix: 11,701, total_orders: 753, total_revenue: 53672.59
19. seller_zip_code_prefix: 13,324, total_orders: 724, total_revenue: 63079.80
20. seller_zip_code_prefix: 14,050, total_orders: 710, total_revenue: 143038.21
21. seller_zip_code_prefix: 13,920, total_orders: 708, total_revenue: 57272.56
22. seller_zip_code_prefix: 87,050, total_orders: 603, total_revenue: 27698.82
23. seller_zip_code_prefix: 13,170, total_orders: 596, total_revenue: 205099.35
24. seller_zip_code_prefix: 80,310, total_orders: 582, total_revenue: 134579.60
25. seller_zip_code_prefix: 22,240, total_orders: 542, total_revenue: 139909.69
26. seller_zip_code_prefix: 11,704, total_orders: 537, total_revenue: 50299.10
27. seller_zip_code_prefix: 14,092, total_orders: 514, total_revenue: 37461.65
28. seller_zip_code_prefix: 37,564, total_orders: 511, total_revenue: 50252.75
29. seller_zip_code_prefix: 87,025, total_orders: 470, total_revenue: 62329.22
30. seller_zip_code_prefix: 12,940, total_orders: 468, total_revenue: 36374.96
31. seller_zip_code_prefix: 7,112, total_orders: 435, total_revenue: 74584.30
32. seller_zip_code_prefix: 4,102, total_orders: 430, total_revenue: 32391.86
33. seller_zip_code_prefix: 8,250, total_orders: 429, total_revenue: 18426.25
34. seller_zip_code_prefix: 14,070, total_orders: 427, total_revenue: 62737.54
35. seller_zip_code_prefix: 42,738, total_orders: 411, total_revenue: 238675.42
36. seller_zip_code_prefix: 65,072, total_orders: 405, total_revenue: 48550.24
37. seller_zip_code_prefix: 17,209, total_orders: 396, total_revenue: 51655.46
38. seller_zip_code_prefix: 51,250, total_orders: 379, total_revenue: 65112.75
39. seller_zip_code_prefix: 7,133, total_orders: 373, total_revenue: 51217.22
40. seller_zip_code_prefix: 14,085, total_orders: 372, total_revenue: 67398.33
41. seller_zip_code_prefix: 3,504, total_orders: 365, total_revenue: 11492.67
42. seller_zip_code_prefix: 3,470, total_orders: 363, total_revenue: 58173.02
43. seller_zip_code_prefix: 38,440, total_orders: 361, total_revenue: 41581.08
44. seller_zip_code_prefix: 13,481, total_orders: 360, total_revenue: 43517.35
45. seller_zip_code_prefix: 90,230, total_orders: 357, total_revenue: 52880.05
46. seller_zip_code_prefix: 2,310, total_orders: 355, total_revenue: 21214.80
47. seller_zip_code_prefix: 13,450, total_orders: 350, total_revenue: 126229.33
48. seller_zip_code_prefix: 3,933, total_orders: 346, total_revenue: 18989.84
49. seller_zip_code_prefix: 88,359, total_orders: 346, total_revenue: 39417.27
50. seller_zip_code_prefix: 3,569, total_orders: 344, total_revenue: 15812.36
51. seller_zip_code_prefix: 4,403, total_orders: 343, total_revenue: 63525.29
52. seller_zip_code_prefix: 6,429, total_orders: 340, total_revenue: 182754.05
53. seller_zip_code_prefix: 13,186, total_orders: 338, total_revenue: 40476.28
54. seller_zip_code_prefix: 16,301, total_orders: 331, total_revenue: 44289.16
55. seller_zip_code_prefix: 4,265, total_orders: 328, total_revenue: 13055.36
56. seller_zip_code_prefix: 13,257, total_orders: 327, total_revenue: 40005.36
57. seller_zip_code_prefix: 21,840, total_orders: 326, total_revenue: 45420.53
58. seller_zip_code_prefix: 13,030, total_orders: 325, total_revenue: 73160.74
59. seller_zip_code_prefix: 12,230, total_orders: 324, total_revenue: 49056.28
60. seller_zip_code_prefix: 80,610, total_orders: 307, total_revenue: 49127.81
61. seller_zip_code_prefix: 1,026, total_orders: 303, total_revenue: 30838.04
62. seller_zip_code_prefix: 87,030, total_orders: 303, total_revenue: 36577.00
63. seller_zip_code_prefix: 89,560, total_orders: 303, total_revenue: 88183.05
64. seller_zip_code_prefix: 13,070, total_orders: 300, total_revenue: 15859.56
65. seller_zip_code_prefix: 11,010, total_orders: 299, total_revenue: 22705.42
66. seller_zip_code_prefix: 18,500, total_orders: 298, total_revenue: 26442.29
67. seller_zip_code_prefix: 87,083, total_orders: 293, total_revenue: 41566.45
68. seller_zip_code_prefix: 3,702, total_orders: 281, total_revenue: 63308.18
69. seller_zip_code_prefix: 4,248, total_orders: 281, total_revenue: 61433.88
70. seller_zip_code_prefix: 35,700, total_orders: 277, total_revenue: 16996.61
71. seller_zip_code_prefix: 9,350, total_orders: 275, total_revenue: 18052.27
72. seller_zip_code_prefix: 35,680, total_orders: 270, total_revenue: 61848.33
73. seller_zip_code_prefix: 37,580, total_orders: 269, total_revenue: 35850.79
74. seller_zip_code_prefix: 89,204, total_orders: 263, total_revenue: 31775.27
75. seller_zip_code_prefix: 37,410, total_orders: 263, total_revenue: 28170.88
76. seller_zip_code_prefix: 9,220, total_orders: 262, total_revenue: 25290.63
77. seller_zip_code_prefix: 9,780, total_orders: 262, total_revenue: 21189.12
78. seller_zip_code_prefix: 80,330, total_orders: 260, total_revenue: 39310.29
79. seller_zip_code_prefix: 14,580, total_orders: 259, total_revenue: 42197.18
80. seller_zip_code_prefix: 18,110, total_orders: 258, total_revenue: 24699.71
81. seller_zip_code_prefix: 13,483, total_orders: 255, total_revenue: 11112.62
82. seller_zip_code_prefix: 17,900, total_orders: 240, total_revenue: 9417.70
83. seller_zip_code_prefix: 29,156, total_orders: 239, total_revenue: 33934.17
84. seller_zip_code_prefix: 87,047, total_orders: 234, total_revenue: 22807.22
85. seller_zip_code_prefix: 9,628, total_orders: 230, total_revenue: 72736.01
86. seller_zip_code_prefix: 13,660, total_orders: 230, total_revenue: 20522.37
87. seller_zip_code_prefix: 11,450, total_orders: 225, total_revenue: 11631.61
88. seller_zip_code_prefix: 2,030, total_orders: 224, total_revenue: 27415.62
89. seller_zip_code_prefix: 13,484, total_orders: 222, total_revenue: 19305.10
90. seller_zip_code_prefix: 2,972, total_orders: 220, total_revenue: 12589.29
91. seller_zip_code_prefix: 89,041, total_orders: 219, total_revenue: 22248.40
92. seller_zip_code_prefix: 3,573, total_orders: 219, total_revenue: 12970.02
93. seller_zip_code_prefix: 7,135, total_orders: 219, total_revenue: 16087.60
94. seller_zip_code_prefix: 2,066, total_orders: 215, total_revenue: 24685.01
95. seller_zip_code_prefix: 15,081, total_orders: 214, total_revenue: 14498.75
96. seller_zip_code_prefix: 13,456, total_orders: 214, total_revenue: 21676.21
97. seller_zip_code_prefix: 13,101, total_orders: 212, total_revenue: 45860.10
98. seller_zip_code_prefix: 3,821, total_orders: 211, total_revenue: 59249.02
99. seller_zip_code_prefix: 2,252, total_orders: 209, total_revenue: 14295.24
100. seller_zip_code_prefix: 3,564, total_orders: 207, total_revenue: 12989.85
101. seller_zip_code_prefix: 85,801, total_orders: 203, total_revenue: 68879.77
102. seller_zip_code_prefix: 13,206, total_orders: 202, total_revenue: 14800.43
103. seller_zip_code_prefix: 7,790, total_orders: 202, total_revenue: 29850.89
104. seller_zip_code_prefix: 13,419, total_orders: 200, total_revenue: 25404.13
105. seller_zip_code_prefix: 14,403, total_orders: 198, total_revenue: 32517.58
106. seller_zip_code_prefix: 13,930, total_orders: 198, total_revenue: 30495.87
107. seller_zip_code_prefix: 21,210, total_orders: 195, total_revenue: 14332.06
108. seller_zip_code_prefix: 37,443, total_orders: 194, total_revenue: 32097.48
109. seller_zip_code_prefix: 13,321, total_orders: 194, total_revenue: 18839.96
110. seller_zip_code_prefix: 7,031, total_orders: 193, total_revenue: 23766.42
111. seller_zip_code_prefix: 4,367, total_orders: 193, total_revenue: 49981.63
112. seller_zip_code_prefix: 38,414, total_orders: 191, total_revenue: 38551.77
113. seller_zip_code_prefix: 89,160, total_orders: 191, total_revenue: 17875.81
114. seller_zip_code_prefix: 5,141, total_orders: 189, total_revenue: 27494.04
115. seller_zip_code_prefix: 72,015, total_orders: 188, total_revenue: 11442.96
116. seller_zip_code_prefix: 1,511, total_orders: 187, total_revenue: 6431.54
117. seller_zip_code_prefix: 24,451, total_orders: 185, total_revenue: 22875.21
118. seller_zip_code_prefix: 90,010, total_orders: 183, total_revenue: 10225.31
119. seller_zip_code_prefix: 86,600, total_orders: 183, total_revenue: 36172.36
120. seller_zip_code_prefix: 87,114, total_orders: 183, total_revenue: 28999.25
121. seller_zip_code_prefix: 13,076, total_orders: 181, total_revenue: 13866.19
122. seller_zip_code_prefix: 5,530, total_orders: 181, total_revenue: 29081.81
123. seller_zip_code_prefix: 8,752, total_orders: 180, total_revenue: 18653.09
124. seller_zip_code_prefix: 4,461, total_orders: 180, total_revenue: 14384.65
125. seller_zip_code_prefix: 2,443, total_orders: 180, total_revenue: 8792.04
126. seller_zip_code_prefix: 89,224, total_orders: 178, total_revenue: 27594.12
127. seller_zip_code_prefix: 4,378, total_orders: 176, total_revenue: 16854.37
128. seller_zip_code_prefix: 32,604, total_orders: 176, total_revenue: 19794.90
129. seller_zip_code_prefix: 25,957, total_orders: 175, total_revenue: 83189.65
130. seller_zip_code_prefix: 4,850, total_orders: 173, total_revenue: 15122.37
131. seller_zip_code_prefix: 20,270, total_orders: 173, total_revenue: 7178.90
132. seller_zip_code_prefix: 3,333, total_orders: 172, total_revenue: 23440.66
133. seller_zip_code_prefix: 13,360, total_orders: 172, total_revenue: 21295.96
134. seller_zip_code_prefix: 3,237, total_orders: 169, total_revenue: 4881.88
135. seller_zip_code_prefix: 30,111, total_orders: 168, total_revenue: 19270.61
136. seller_zip_code_prefix: 6,060, total_orders: 167, total_revenue: 36438.75
137. seller_zip_code_prefix: 8,550, total_orders: 165, total_revenue: 11265.25
138. seller_zip_code_prefix: 1,319, total_orders: 165, total_revenue: 12551.76
139. seller_zip_code_prefix: 14,850, total_orders: 165, total_revenue: 50893.67
140. seller_zip_code_prefix: 3,880, total_orders: 165, total_revenue: 9176.07
141. seller_zip_code_prefix: 88,301, total_orders: 165, total_revenue: 16995.31
142. seller_zip_code_prefix: 3,006, total_orders: 164, total_revenue: 13011.87
143. seller_zip_code_prefix: 3,804, total_orders: 162, total_revenue: 6048.43
144. seller_zip_code_prefix: 9,720, total_orders: 161, total_revenue: 60356.36
145. seller_zip_code_prefix: 3,194, total_orders: 159, total_revenue: 37541.56
146. seller_zip_code_prefix: 35,570, total_orders: 158, total_revenue: 41699.03
147. seller_zip_code_prefix: 89,460, total_orders: 157, total_revenue: 10965.33
148. seller_zip_code_prefix: 3,872, total_orders: 157, total_revenue: 8475.87
149. seller_zip_code_prefix: 31,842, total_orders: 156, total_revenue: 17581.07
150. seller_zip_code_prefix: 38,700, total_orders: 156, total_revenue: 17402.47
151. seller_zip_code_prefix: 12,243, total_orders: 155, total_revenue: 11967.15
152. seller_zip_code_prefix: 36,500, total_orders: 153, total_revenue: 35779.37
153. seller_zip_code_prefix: 71,070, total_orders: 153, total_revenue: 21901.93
154. seller_zip_code_prefix: 27,277, total_orders: 151, total_revenue: 15183.64
155. seller_zip_code_prefix: 13,330, total_orders: 150, total_revenue: 26688.95
156. seller_zip_code_prefix: 38,442, total_orders: 149, total_revenue: 12596.13
157. seller_zip_code_prefix: 3,542, total_orders: 149, total_revenue: 6916.06
158. seller_zip_code_prefix: 13,843, total_orders: 149, total_revenue: 49531.57
159. seller_zip_code_prefix: 30,190, total_orders: 148, total_revenue: 18106.57
160. seller_zip_code_prefix: 7,084, total_orders: 146, total_revenue: 13388.82
161. seller_zip_code_prefix: 3,126, total_orders: 146, total_revenue: 5421.64
162. seller_zip_code_prefix: 3,809, total_orders: 146, total_revenue: 16490.14
163. seller_zip_code_prefix: 85,802, total_orders: 145, total_revenue: 20780.95
164. seller_zip_code_prefix: 9,715, total_orders: 145, total_revenue: 9165.30
165. seller_zip_code_prefix: 92,030, total_orders: 145, total_revenue: 19756.56
166. seller_zip_code_prefix: 14,401, total_orders: 144, total_revenue: 27585.10
167. seller_zip_code_prefix: 3,471, total_orders: 143, total_revenue: 12072.00
168. seller_zip_code_prefix: 95,780, total_orders: 142, total_revenue: 31077.26
169. seller_zip_code_prefix: 13,290, total_orders: 142, total_revenue: 18460.22
170. seller_zip_code_prefix: 35,530, total_orders: 141, total_revenue: 12398.48
171. seller_zip_code_prefix: 4,361, total_orders: 139, total_revenue: 13231.18
172. seller_zip_code_prefix: 6,871, total_orders: 139, total_revenue: 12766.71
173. seller_zip_code_prefix: 38,408, total_orders: 138, total_revenue: 9465.52
174. seller_zip_code_prefix: 6,506, total_orders: 137, total_revenue: 15001.43
175. seller_zip_code_prefix: 2,285, total_orders: 137, total_revenue: 16782.16
176. seller_zip_code_prefix: 22,775, total_orders: 136, total_revenue: 20669.61
177. seller_zip_code_prefix: 14,709, total_orders: 135, total_revenue: 8196.96
178. seller_zip_code_prefix: 14,802, total_orders: 135, total_revenue: 11179.58
179. seller_zip_code_prefix: 5,138, total_orders: 133, total_revenue: 20108.77
180. seller_zip_code_prefix: 16,200, total_orders: 133, total_revenue: 13966.77
181. seller_zip_code_prefix: 19,025, total_orders: 132, total_revenue: 11795.03
182. seller_zip_code_prefix: 13,322, total_orders: 132, total_revenue: 16543.31
183. seller_zip_code_prefix: 13,087, total_orders: 132, total_revenue: 8673.04
184. seller_zip_code_prefix: 3,910, total_orders: 132, total_revenue: 5434.07
185. seller_zip_code_prefix: 13,347, total_orders: 132, total_revenue: 10766.10
186. seller_zip_code_prefix: 88,115, total_orders: 131, total_revenue: 11673.20
187. seller_zip_code_prefix: 86,050, total_orders: 131, total_revenue: 17690.07
188. seller_zip_code_prefix: 12,233, total_orders: 130, total_revenue: 16212.51
189. seller_zip_code_prefix: 3,655, total_orders: 130, total_revenue: 23944.92
190. seller_zip_code_prefix: 31,140, total_orders: 130, total_revenue: 7912.71
191. seller_zip_code_prefix: 15,502, total_orders: 130, total_revenue: 22335.93
192. seller_zip_code_prefix: 9,230, total_orders: 129, total_revenue: 15212.48
193. seller_zip_code_prefix: 32,677, total_orders: 129, total_revenue: 12120.72
194. seller_zip_code_prefix: 3,431, total_orders: 129, total_revenue: 12183.45
195. seller_zip_code_prefix: 31,570, total_orders: 126, total_revenue: 15639.29
196. seller_zip_code_prefix: 14,110, total_orders: 126, total_revenue: 15512.82
197. seller_zip_code_prefix: 1,233, total_orders: 125, total_revenue: 17254.59
198. seller_zip_code_prefix: 1,031, total_orders: 124, total_revenue: 4867.20
199. seller_zip_code_prefix: 87,015, total_orders: 123, total_revenue: 24829.17
200. seller_zip_code_prefix: 83,408, total_orders: 121, total_revenue: 28972.82
201. seller_zip_code_prefix: 24,440, total_orders: 121, total_revenue: 10140.99
202. seller_zip_code_prefix: 88,730, total_orders: 119, total_revenue: 18146.45
203. seller_zip_code_prefix: 31,030, total_orders: 119, total_revenue: 6383.28
204. seller_zip_code_prefix: 89,023, total_orders: 118, total_revenue: 7754.67
205. seller_zip_code_prefix: 86,010, total_orders: 118, total_revenue: 20433.53
206. seller_zip_code_prefix: 3,929, total_orders: 118, total_revenue: 8768.26
207. seller_zip_code_prefix: 12,308, total_orders: 117, total_revenue: 9983.79
208. seller_zip_code_prefix: 5,503, total_orders: 117, total_revenue: 13396.85
209. seller_zip_code_prefix: 18,048, total_orders: 116, total_revenue: 8349.56
210. seller_zip_code_prefix: 86,800, total_orders: 116, total_revenue: 14256.87
211. seller_zip_code_prefix: 17,400, total_orders: 115, total_revenue: 25592.50
212. seller_zip_code_prefix: 13,250, total_orders: 114, total_revenue: 34764.17
213. seller_zip_code_prefix: 89,120, total_orders: 114, total_revenue: 13038.90
214. seller_zip_code_prefix: 2,028, total_orders: 112, total_revenue: 9678.79
215. seller_zip_code_prefix: 15,014, total_orders: 112, total_revenue: 15792.12
216. seller_zip_code_prefix: 9,270, total_orders: 111, total_revenue: 12393.23
217. seller_zip_code_prefix: 4,809, total_orders: 111, total_revenue: 9440.79
218. seller_zip_code_prefix: 16,304, total_orders: 111, total_revenue: 13127.72
219. seller_zip_code_prefix: 31,573, total_orders: 110, total_revenue: 8386.96
220. seller_zip_code_prefix: 93,542, total_orders: 110, total_revenue: 25372.08
221. seller_zip_code_prefix: 37,584, total_orders: 109, total_revenue: 24951.27
222. seller_zip_code_prefix: 37,540, total_orders: 108, total_revenue: 18149.83
223. seller_zip_code_prefix: 25,803, total_orders: 108, total_revenue: 5535.95
224. seller_zip_code_prefix: 13,327, total_orders: 108, total_revenue: 14315.88
225. seller_zip_code_prefix: 14,407, total_orders: 106, total_revenue: 8811.20
226. seller_zip_code_prefix: 86,706, total_orders: 106, total_revenue: 15488.20
227. seller_zip_code_prefix: 19,042, total_orders: 106, total_revenue: 9520.11
228. seller_zip_code_prefix: 8,275, total_orders: 106, total_revenue: 7598.21
229. seller_zip_code_prefix: 3,017, total_orders: 106, total_revenue: 10574.25
230. seller_zip_code_prefix: 83,323, total_orders: 105, total_revenue: 14446.82
231. seller_zip_code_prefix: 85,807, total_orders: 105, total_revenue: 15716.72
232. seller_zip_code_prefix: 81,350, total_orders: 105, total_revenue: 7347.79
233. seller_zip_code_prefix: 3,029, total_orders: 105, total_revenue: 25767.87
234. seller_zip_code_prefix: 5,734, total_orders: 104, total_revenue: 20593.93
235. seller_zip_code_prefix: 30,180, total_orders: 104, total_revenue: 12663.88
236. seller_zip_code_prefix: 81,880, total_orders: 104, total_revenue: 5003.96
237. seller_zip_code_prefix: 4,438, total_orders: 103, total_revenue: 7410.32
238. seller_zip_code_prefix: 15,601, total_orders: 102, total_revenue: 8941.24
239. seller_zip_code_prefix: 7,094, total_orders: 101, total_revenue: 7901.45
240. seller_zip_code_prefix: 15,704, total_orders: 101, total_revenue: 6749.47
241. seller_zip_code_prefix: 18,025, total_orders: 100, total_revenue: 11512.81
242. seller_zip_code_prefix: 13,320, total_orders: 100, total_revenue: 6519.90
243. seller_zip_code_prefix: 20,930, total_orders: 100, total_revenue: 14857.68
244. seller_zip_code_prefix: 8,290, total_orders: 99, total_revenue: 18806.21
245. seller_zip_code_prefix: 20,756, total_orders: 99, total_revenue: 7951.76
246. seller_zip_code_prefix: 2,634, total_orders: 99, total_revenue: 5192.82
247. seller_zip_code_prefix: 5,588, total_orders: 99, total_revenue: 6472.77
248. seller_zip_code_prefix: 18,683, total_orders: 98, total_revenue: 10512.15
249. seller_zip_code_prefix: 31,710, total_orders: 98, total_revenue: 5183.10
250. seller_zip_code_prefix: 87,504, total_orders: 98, total_revenue: 7490.57
251. seller_zip_code_prefix: 2,016, total_orders: 98, total_revenue: 11074.64
252. seller_zip_code_prefix: 4,273, total_orders: 98, total_revenue: 10482.25
253. seller_zip_code_prefix: 37,590, total_orders: 97, total_revenue: 12243.48
254. seller_zip_code_prefix: 9,360, total_orders: 97, total_revenue: 6185.20
255. seller_zip_code_prefix: 35,430, total_orders: 97, total_revenue: 11522.66
256. seller_zip_code_prefix: 3,306, total_orders: 97, total_revenue: 11271.47
257. seller_zip_code_prefix: 9,416, total_orders: 97, total_revenue: 9068.82
258. seller_zip_code_prefix: 9,171, total_orders: 96, total_revenue: 14061.27
259. seller_zip_code_prefix: 85,851, total_orders: 96, total_revenue: 13672.96
260. seller_zip_code_prefix: 9,320, total_orders: 96, total_revenue: 9157.73
261. seller_zip_code_prefix: 12,701, total_orders: 95, total_revenue: 7968.67
262. seller_zip_code_prefix: 91,350, total_orders: 95, total_revenue: 24381.84
263. seller_zip_code_prefix: 2,955, total_orders: 95, total_revenue: 5807.03
264. seller_zip_code_prefix: 87,040, total_orders: 95, total_revenue: 16068.36
265. seller_zip_code_prefix: 12,952, total_orders: 95, total_revenue: 8802.97
266. seller_zip_code_prefix: 19,803, total_orders: 95, total_revenue: 6048.12
267. seller_zip_code_prefix: 88,215, total_orders: 94, total_revenue: 63184.99
268. seller_zip_code_prefix: 18,015, total_orders: 94, total_revenue: 10105.81
269. seller_zip_code_prefix: 3,320, total_orders: 93, total_revenue: 9166.66
270. seller_zip_code_prefix: 4,773, total_orders: 93, total_revenue: 9536.01
271. seller_zip_code_prefix: 6,341, total_orders: 93, total_revenue: 11193.82
272. seller_zip_code_prefix: 71,200, total_orders: 92, total_revenue: 12692.73
273. seller_zip_code_prefix: 13,403, total_orders: 92, total_revenue: 22657.60
274. seller_zip_code_prefix: 5,729, total_orders: 92, total_revenue: 15352.47
275. seller_zip_code_prefix: 81,770, total_orders: 92, total_revenue: 13692.25
276. seller_zip_code_prefix: 87,230, total_orders: 92, total_revenue: 14916.39
277. seller_zip_code_prefix: 7,194, total_orders: 91, total_revenue: 7550.67
278. seller_zip_code_prefix: 8,820, total_orders: 91, total_revenue: 9857.87
279. seller_zip_code_prefix: 14,090, total_orders: 91, total_revenue: 14156.34
280. seller_zip_code_prefix: 3,971, total_orders: 90, total_revenue: 12011.13
281. seller_zip_code_prefix: 71,691, total_orders: 90, total_revenue: 9128.47
282. seller_zip_code_prefix: 81,825, total_orders: 89, total_revenue: 7807.40
283. seller_zip_code_prefix: 8,180, total_orders: 89, total_revenue: 9287.75
284. seller_zip_code_prefix: 13,720, total_orders: 89, total_revenue: 11322.68
285. seller_zip_code_prefix: 14,882, total_orders: 89, total_revenue: 12053.88
286. seller_zip_code_prefix: 5,424, total_orders: 88, total_revenue: 13854.57
287. seller_zip_code_prefix: 13,328, total_orders: 88, total_revenue: 31467.94
288. seller_zip_code_prefix: 9,850, total_orders: 88, total_revenue: 3511.89
289. seller_zip_code_prefix: 88,501, total_orders: 87, total_revenue: 48992.88
290. seller_zip_code_prefix: 13,457, total_orders: 87, total_revenue: 5815.36
291. seller_zip_code_prefix: 88,085, total_orders: 86, total_revenue: 6544.21
292. seller_zip_code_prefix: 2,274, total_orders: 86, total_revenue: 7453.59
293. seller_zip_code_prefix: 8,710, total_orders: 86, total_revenue: 13564.45
294. seller_zip_code_prefix: 1,512, total_orders: 85, total_revenue: 5800.42
295. seller_zip_code_prefix: 19,800, total_orders: 85, total_revenue: 6355.29
296. seller_zip_code_prefix: 87,502, total_orders: 85, total_revenue: 26319.74
297. seller_zip_code_prefix: 1,257, total_orders: 85, total_revenue: 6149.27
298. seller_zip_code_prefix: 8,598, total_orders: 85, total_revenue: 13657.34
299. seller_zip_code_prefix: 82,810, total_orders: 84, total_revenue: 33803.97
300. seller_zip_code_prefix: 2,407, total_orders: 84, total_revenue: 4826.86
301. seller_zip_code_prefix: 4,186, total_orders: 84, total_revenue: 8990.51
302. seller_zip_code_prefix: 80,230, total_orders: 84, total_revenue: 11042.72
303. seller_zip_code_prefix: 22,230, total_orders: 84, total_revenue: 8109.32
304. seller_zip_code_prefix: 6,440, total_orders: 83, total_revenue: 4826.45
305. seller_zip_code_prefix: 6,097, total_orders: 83, total_revenue: 15544.88
306. seller_zip_code_prefix: 89,254, total_orders: 82, total_revenue: 4654.35
307. seller_zip_code_prefix: 89,225, total_orders: 81, total_revenue: 19282.41
308. seller_zip_code_prefix: 4,208, total_orders: 81, total_revenue: 6344.98
309. seller_zip_code_prefix: 9,920, total_orders: 80, total_revenue: 53223.42
310. seller_zip_code_prefix: 18,055, total_orders: 80, total_revenue: 3901.54
311. seller_zip_code_prefix: 12,215, total_orders: 80, total_revenue: 4316.01
312. seller_zip_code_prefix: 89,251, total_orders: 80, total_revenue: 18841.18
313. seller_zip_code_prefix: 80,215, total_orders: 80, total_revenue: 26266.84
314. seller_zip_code_prefix: 3,417, total_orders: 80, total_revenue: 12415.92
315. seller_zip_code_prefix: 83,020, total_orders: 80, total_revenue: 13188.68
316. seller_zip_code_prefix: 17,602, total_orders: 79, total_revenue: 16043.51
317. seller_zip_code_prefix: 74,930, total_orders: 79, total_revenue: 11982.21
318. seller_zip_code_prefix: 18,608, total_orders: 79, total_revenue: 8260.17
319. seller_zip_code_prefix: 84,530, total_orders: 78, total_revenue: 15008.74
320. seller_zip_code_prefix: 16,800, total_orders: 78, total_revenue: 14986.65
321. seller_zip_code_prefix: 8,583, total_orders: 78, total_revenue: 13077.93
322. seller_zip_code_prefix: 17,504, total_orders: 78, total_revenue: 18494.93
323. seller_zip_code_prefix: 5,126, total_orders: 78, total_revenue: 3803.46
324. seller_zip_code_prefix: 7,074, total_orders: 77, total_revenue: 34857.93
325. seller_zip_code_prefix: 81,020, total_orders: 76, total_revenue: 4309.28
326. seller_zip_code_prefix: 94,451, total_orders: 76, total_revenue: 18715.65
327. seller_zip_code_prefix: 11,900, total_orders: 76, total_revenue: 18330.03
328. seller_zip_code_prefix: 11,075, total_orders: 76, total_revenue: 5285.70
329. seller_zip_code_prefix: 14,400, total_orders: 75, total_revenue: 14903.24
330. seller_zip_code_prefix: 6,162, total_orders: 75, total_revenue: 16047.17
331. seller_zip_code_prefix: 3,334, total_orders: 75, total_revenue: 3342.61
332. seller_zip_code_prefix: 18,130, total_orders: 74, total_revenue: 9667.83
333. seller_zip_code_prefix: 18,950, total_orders: 74, total_revenue: 8699.32
334. seller_zip_code_prefix: 41,820, total_orders: 74, total_revenue: 16587.51
335. seller_zip_code_prefix: 85,863, total_orders: 74, total_revenue: 11115.95
336. seller_zip_code_prefix: 8,673, total_orders: 74, total_revenue: 8794.80
337. seller_zip_code_prefix: 4,131, total_orders: 74, total_revenue: 6176.52
338. seller_zip_code_prefix: 5,125, total_orders: 74, total_revenue: 10123.06
339. seller_zip_code_prefix: 7,032, total_orders: 73, total_revenue: 9273.33
340. seller_zip_code_prefix: 13,270, total_orders: 73, total_revenue: 3863.51
341. seller_zip_code_prefix: 35,501, total_orders: 73, total_revenue: 14512.06
342. seller_zip_code_prefix: 82,510, total_orders: 72, total_revenue: 14911.87
343. seller_zip_code_prefix: 4,007, total_orders: 72, total_revenue: 6226.61
344. seller_zip_code_prefix: 11,250, total_orders: 71, total_revenue: 5683.93
345. seller_zip_code_prefix: 14,808, total_orders: 71, total_revenue: 44643.43
346. seller_zip_code_prefix: 9,405, total_orders: 71, total_revenue: 7703.74
347. seller_zip_code_prefix: 5,767, total_orders: 71, total_revenue: 6375.47
348. seller_zip_code_prefix: 15,013, total_orders: 70, total_revenue: 13837.30
349. seller_zip_code_prefix: 9,210, total_orders: 70, total_revenue: 8046.74
350. seller_zip_code_prefix: 36,502, total_orders: 70, total_revenue: 10645.30
351. seller_zip_code_prefix: 8,215, total_orders: 70, total_revenue: 4900.20
352. seller_zip_code_prefix: 85,603, total_orders: 69, total_revenue: 11895.18
353. seller_zip_code_prefix: 9,951, total_orders: 69, total_revenue: 12175.46
354. seller_zip_code_prefix: 88,715, total_orders: 68, total_revenue: 4592.58
355. seller_zip_code_prefix: 7,097, total_orders: 68, total_revenue: 5311.52
356. seller_zip_code_prefix: 95,012, total_orders: 68, total_revenue: 34195.49
357. seller_zip_code_prefix: 37,135, total_orders: 68, total_revenue: 8397.71
358. seller_zip_code_prefix: 2,134, total_orders: 68, total_revenue: 4199.78
359. seller_zip_code_prefix: 17,510, total_orders: 68, total_revenue: 6050.52
360. seller_zip_code_prefix: 30,882, total_orders: 67, total_revenue: 4075.88
361. seller_zip_code_prefix: 35,500, total_orders: 67, total_revenue: 20529.11
362. seller_zip_code_prefix: 3,273, total_orders: 67, total_revenue: 5026.26
363. seller_zip_code_prefix: 3,167, total_orders: 67, total_revenue: 4316.51
364. seller_zip_code_prefix: 26,379, total_orders: 66, total_revenue: 13639.41
365. seller_zip_code_prefix: 88,370, total_orders: 66, total_revenue: 17823.57
366. seller_zip_code_prefix: 24,710, total_orders: 66, total_revenue: 10284.82
367. seller_zip_code_prefix: 15,015, total_orders: 66, total_revenue: 13427.20
368. seller_zip_code_prefix: 14,600, total_orders: 66, total_revenue: 9925.07
369. seller_zip_code_prefix: 8,270, total_orders: 66, total_revenue: 9143.28
370. seller_zip_code_prefix: 9,560, total_orders: 65, total_revenue: 7566.42
371. seller_zip_code_prefix: 80,010, total_orders: 65, total_revenue: 16802.45
372. seller_zip_code_prefix: 19,830, total_orders: 65, total_revenue: 4623.96
373. seller_zip_code_prefix: 88,372, total_orders: 65, total_revenue: 7558.04
374. seller_zip_code_prefix: 9,020, total_orders: 64, total_revenue: 8555.80
375. seller_zip_code_prefix: 5,537, total_orders: 64, total_revenue: 20181.23
376. seller_zip_code_prefix: 3,275, total_orders: 64, total_revenue: 10050.12
377. seller_zip_code_prefix: 4,567, total_orders: 63, total_revenue: 8801.84
378. seller_zip_code_prefix: 9,291, total_orders: 63, total_revenue: 4220.42
379. seller_zip_code_prefix: 3,613, total_orders: 63, total_revenue: 4111.19
380. seller_zip_code_prefix: 31,910, total_orders: 63, total_revenue: 15788.30
381. seller_zip_code_prefix: 14,405, total_orders: 62, total_revenue: 3489.70
382. seller_zip_code_prefix: 98,803, total_orders: 62, total_revenue: 23808.17
383. seller_zip_code_prefix: 9,541, total_orders: 62, total_revenue: 45703.98
384. seller_zip_code_prefix: 3,187, total_orders: 62, total_revenue: 5064.32
385. seller_zip_code_prefix: 1,547, total_orders: 62, total_revenue: 6872.34
386. seller_zip_code_prefix: 3,331, total_orders: 61, total_revenue: 9289.37
387. seller_zip_code_prefix: 14,020, total_orders: 61, total_revenue: 6690.31
388. seller_zip_code_prefix: 17,320, total_orders: 61, total_revenue: 2768.66
389. seller_zip_code_prefix: 13,908, total_orders: 61, total_revenue: 11896.04
390. seller_zip_code_prefix: 11,045, total_orders: 61, total_revenue: 6047.91
391. seller_zip_code_prefix: 9,725, total_orders: 61, total_revenue: 14254.01
392. seller_zip_code_prefix: 3,477, total_orders: 61, total_revenue: 4413.61
393. seller_zip_code_prefix: 36,010, total_orders: 61, total_revenue: 6713.41
394. seller_zip_code_prefix: 37,708, total_orders: 61, total_revenue: 4428.03
395. seller_zip_code_prefix: 2,215, total_orders: 61, total_revenue: 1907.90
396. seller_zip_code_prefix: 3,908, total_orders: 61, total_revenue: 57812.43
397. seller_zip_code_prefix: 4,811, total_orders: 61, total_revenue: 4161.86
398. seller_zip_code_prefix: 38,400, total_orders: 60, total_revenue: 5770.07
399. seller_zip_code_prefix: 95,913, total_orders: 60, total_revenue: 8721.44
400. seller_zip_code_prefix: 13,473, total_orders: 60, total_revenue: 4666.20
401. seller_zip_code_prefix: 88,820, total_orders: 60, total_revenue: 7875.71
402. seller_zip_code_prefix: 6,713, total_orders: 60, total_revenue: 20153.04
403. seller_zip_code_prefix: 80,240, total_orders: 60, total_revenue: 10898.85
404. seller_zip_code_prefix: 3,087, total_orders: 59, total_revenue: 15196.12
405. seller_zip_code_prefix: 3,562, total_orders: 59, total_revenue: 2157.34
406. seller_zip_code_prefix: 14,406, total_orders: 58, total_revenue: 11430.91
407. seller_zip_code_prefix: 94,910, total_orders: 58, total_revenue: 22570.13
408. seller_zip_code_prefix: 25,963, total_orders: 58, total_revenue: 53913.76
409. seller_zip_code_prefix: 4,142, total_orders: 58, total_revenue: 5795.97
410. seller_zip_code_prefix: 74,323, total_orders: 58, total_revenue: 7693.63
411. seller_zip_code_prefix: 26,562, total_orders: 58, total_revenue: 6799.05
412. seller_zip_code_prefix: 83,605, total_orders: 58, total_revenue: 12299.77
413. seller_zip_code_prefix: 13,912, total_orders: 57, total_revenue: 4221.21
414. seller_zip_code_prefix: 13,480, total_orders: 57, total_revenue: 51115.07
415. seller_zip_code_prefix: 70,235, total_orders: 57, total_revenue: 3938.54
416. seller_zip_code_prefix: 37,795, total_orders: 57, total_revenue: 18309.28
417. seller_zip_code_prefix: 74,333, total_orders: 57, total_revenue: 9394.81
418. seller_zip_code_prefix: 99,500, total_orders: 57, total_revenue: 10525.67
419. seller_zip_code_prefix: 80,430, total_orders: 56, total_revenue: 9376.53
420. seller_zip_code_prefix: 9,271, total_orders: 56, total_revenue: 4105.03
421. seller_zip_code_prefix: 12,913, total_orders: 56, total_revenue: 13966.71
422. seller_zip_code_prefix: 31,230, total_orders: 56, total_revenue: 2733.56
423. seller_zip_code_prefix: 25,900, total_orders: 56, total_revenue: 7978.11
424. seller_zip_code_prefix: 3,701, total_orders: 56, total_revenue: 4471.79
425. seller_zip_code_prefix: 30,494, total_orders: 55, total_revenue: 3631.40
426. seller_zip_code_prefix: 19,806, total_orders: 55, total_revenue: 7237.87
427. seller_zip_code_prefix: 87,303, total_orders: 55, total_revenue: 16120.66
428. seller_zip_code_prefix: 17,056, total_orders: 55, total_revenue: 6984.09
429. seller_zip_code_prefix: 8,011, total_orders: 55, total_revenue: 4087.60
430. seller_zip_code_prefix: 78,552, total_orders: 55, total_revenue: 9844.56
431. seller_zip_code_prefix: 86,300, total_orders: 54, total_revenue: 3964.73
432. seller_zip_code_prefix: 6,365, total_orders: 54, total_revenue: 6077.34
433. seller_zip_code_prefix: 7,077, total_orders: 54, total_revenue: 13426.01
434. seller_zip_code_prefix: 4,733, total_orders: 54, total_revenue: 24535.10
435. seller_zip_code_prefix: 2,804, total_orders: 54, total_revenue: 3557.21
436. seller_zip_code_prefix: 83,830, total_orders: 54, total_revenue: 6993.94
437. seller_zip_code_prefix: 14,075, total_orders: 53, total_revenue: 7912.47
438. seller_zip_code_prefix: 3,031, total_orders: 53, total_revenue: 6012.66
439. seller_zip_code_prefix: 9,190, total_orders: 53, total_revenue: 4756.91
440. seller_zip_code_prefix: 4,119, total_orders: 53, total_revenue: 3335.33
441. seller_zip_code_prefix: 78,020, total_orders: 52, total_revenue: 6200.62
442. seller_zip_code_prefix: 19,063, total_orders: 52, total_revenue: 4721.18
443. seller_zip_code_prefix: 5,303, total_orders: 52, total_revenue: 11167.98
444. seller_zip_code_prefix: 3,028, total_orders: 52, total_revenue: 3725.71
445. seller_zip_code_prefix: 86,385, total_orders: 51, total_revenue: 1660.28
446. seller_zip_code_prefix: 16,012, total_orders: 51, total_revenue: 3280.19
447. seller_zip_code_prefix: 5,455, total_orders: 51, total_revenue: 2680.70
448. seller_zip_code_prefix: 2,258, total_orders: 51, total_revenue: 8145.17
449. seller_zip_code_prefix: 8,030, total_orders: 50, total_revenue: 6094.03
450. seller_zip_code_prefix: 6,716, total_orders: 50, total_revenue: 2359.55
451. seller_zip_code_prefix: 21,235, total_orders: 50, total_revenue: 18158.23
452. seller_zip_code_prefix: 35,590, total_orders: 49, total_revenue: 6466.75
453. seller_zip_code_prefix: 23,092, total_orders: 49, total_revenue: 4966.62
454. seller_zip_code_prefix: 1,550, total_orders: 49, total_revenue: 2061.77
455. seller_zip_code_prefix: 12,570, total_orders: 48, total_revenue: 1533.95
456. seller_zip_code_prefix: 14,870, total_orders: 48, total_revenue: 5433.61
457. seller_zip_code_prefix: 28,630, total_orders: 48, total_revenue: 9802.63
458. seller_zip_code_prefix: 8,260, total_orders: 48, total_revenue: 17229.32
459. seller_zip_code_prefix: 38,022, total_orders: 48, total_revenue: 17547.38
460. seller_zip_code_prefix: 15,070, total_orders: 48, total_revenue: 11099.36
461. seller_zip_code_prefix: 3,476, total_orders: 48, total_revenue: 4308.02
462. seller_zip_code_prefix: 82,400, total_orders: 48, total_revenue: 12607.42
463. seller_zip_code_prefix: 11,600, total_orders: 48, total_revenue: 9574.27
464. seller_zip_code_prefix: 91,510, total_orders: 47, total_revenue: 9431.86
465. seller_zip_code_prefix: 88,303, total_orders: 47, total_revenue: 15621.16
466. seller_zip_code_prefix: 5,181, total_orders: 47, total_revenue: 5496.31
467. seller_zip_code_prefix: 33,936, total_orders: 47, total_revenue: 6085.70
468. seller_zip_code_prefix: 31,730, total_orders: 47, total_revenue: 4320.64
469. seller_zip_code_prefix: 7,152, total_orders: 47, total_revenue: 4059.73
470. seller_zip_code_prefix: 9,710, total_orders: 47, total_revenue: 2302.48
471. seller_zip_code_prefix: 3,813, total_orders: 47, total_revenue: 1859.02
472. seller_zip_code_prefix: 20,061, total_orders: 47, total_revenue: 3461.70
473. seller_zip_code_prefix: 6,790, total_orders: 46, total_revenue: 1433.37
474. seller_zip_code_prefix: 38,230, total_orders: 46, total_revenue: 5618.40
475. seller_zip_code_prefix: 13,568, total_orders: 45, total_revenue: 2828.66
476. seller_zip_code_prefix: 21,041, total_orders: 45, total_revenue: 3787.43
477. seller_zip_code_prefix: 14,781, total_orders: 45, total_revenue: 3970.98
478. seller_zip_code_prefix: 89,031, total_orders: 45, total_revenue: 9299.03
479. seller_zip_code_prefix: 13,088, total_orders: 45, total_revenue: 1977.95
480. seller_zip_code_prefix: 22,793, total_orders: 45, total_revenue: 6717.31
481. seller_zip_code_prefix: 7,023, total_orders: 45, total_revenue: 4815.54
482. seller_zip_code_prefix: 36,407, total_orders: 45, total_revenue: 7903.69
483. seller_zip_code_prefix: 88,056, total_orders: 44, total_revenue: 6329.27
484. seller_zip_code_prefix: 12,250, total_orders: 44, total_revenue: 3035.39
485. seller_zip_code_prefix: 89,214, total_orders: 44, total_revenue: 5557.24
486. seller_zip_code_prefix: 13,800, total_orders: 44, total_revenue: 2913.96
487. seller_zip_code_prefix: 82,940, total_orders: 44, total_revenue: 8915.71
488. seller_zip_code_prefix: 7,140, total_orders: 44, total_revenue: 45778.22
489. seller_zip_code_prefix: 32,110, total_orders: 44, total_revenue: 5923.66
490. seller_zip_code_prefix: 18,611, total_orders: 44, total_revenue: 7207.63
491. seller_zip_code_prefix: 74,645, total_orders: 44, total_revenue: 8733.61
492. seller_zip_code_prefix: 13,566, total_orders: 44, total_revenue: 9525.94
493. seller_zip_code_prefix: 95,170, total_orders: 44, total_revenue: 3210.39
494. seller_zip_code_prefix: 4,180, total_orders: 43, total_revenue: 4648.15
495. seller_zip_code_prefix: 7,160, total_orders: 43, total_revenue: 1979.17
496. seller_zip_code_prefix: 16,500, total_orders: 43, total_revenue: 5942.69
497. seller_zip_code_prefix: 25,561, total_orders: 43, total_revenue: 4919.77
498. seller_zip_code_prefix: 5,101, total_orders: 43, total_revenue: 3027.54
499. seller_zip_code_prefix: 18,072, total_orders: 43, total_revenue: 4340.86
500. seller_zip_code_prefix: 6,853, total_orders: 43, total_revenue: 4627.20
501. seller_zip_code_prefix: 74,560, total_orders: 43, total_revenue: 2074.51
502. seller_zip_code_prefix: 12,328, total_orders: 42, total_revenue: 7833.39
503. seller_zip_code_prefix: 17,210, total_orders: 42, total_revenue: 4449.26
504. seller_zip_code_prefix: 35,170, total_orders: 42, total_revenue: 6723.63
505. seller_zip_code_prefix: 2,963, total_orders: 42, total_revenue: 7256.54
506. seller_zip_code_prefix: 19,029, total_orders: 42, total_revenue: 4474.27
507. seller_zip_code_prefix: 7,013, total_orders: 42, total_revenue: 3682.67
508. seller_zip_code_prefix: 12,942, total_orders: 41, total_revenue: 3725.62
509. seller_zip_code_prefix: 13,844, total_orders: 41, total_revenue: 13141.80
510. seller_zip_code_prefix: 7,174, total_orders: 41, total_revenue: 13652.89
511. seller_zip_code_prefix: 12,246, total_orders: 41, total_revenue: 10474.98
512. seller_zip_code_prefix: 31,310, total_orders: 41, total_revenue: 2938.06
513. seller_zip_code_prefix: 36,301, total_orders: 41, total_revenue: 4849.38
514. seller_zip_code_prefix: 36,415, total_orders: 41, total_revenue: 14404.28
515. seller_zip_code_prefix: 87,900, total_orders: 40, total_revenue: 5350.68
516. seller_zip_code_prefix: 71,551, total_orders: 40, total_revenue: 8487.84
517. seller_zip_code_prefix: 15,076, total_orders: 40, total_revenue: 9048.72
518. seller_zip_code_prefix: 11,431, total_orders: 40, total_revenue: 8125.52
519. seller_zip_code_prefix: 38,950, total_orders: 40, total_revenue: 4365.76
520. seller_zip_code_prefix: 3,265, total_orders: 40, total_revenue: 2471.34
521. seller_zip_code_prefix: 22,790, total_orders: 40, total_revenue: 4029.35
522. seller_zip_code_prefix: 14,079, total_orders: 40, total_revenue: 1910.56
523. seller_zip_code_prefix: 9,010, total_orders: 40, total_revenue: 6366.43
524. seller_zip_code_prefix: 3,111, total_orders: 40, total_revenue: 9191.59
525. seller_zip_code_prefix: 2,537, total_orders: 40, total_revenue: 2477.32
526. seller_zip_code_prefix: 3,035, total_orders: 40, total_revenue: 4726.57
527. seller_zip_code_prefix: 83,010, total_orders: 40, total_revenue: 5225.75
528. seller_zip_code_prefix: 80,040, total_orders: 39, total_revenue: 6087.48
529. seller_zip_code_prefix: 1,021, total_orders: 39, total_revenue: 7765.30
530. seller_zip_code_prefix: 2,124, total_orders: 39, total_revenue: 17102.96
531. seller_zip_code_prefix: 75,650, total_orders: 39, total_revenue: 3973.12
532. seller_zip_code_prefix: 14,910, total_orders: 39, total_revenue: 6029.47
533. seller_zip_code_prefix: 27,930, total_orders: 39, total_revenue: 26368.49
534. seller_zip_code_prefix: 2,034, total_orders: 39, total_revenue: 7662.25
535. seller_zip_code_prefix: 3,916, total_orders: 39, total_revenue: 4396.75
536. seller_zip_code_prefix: 86,073, total_orders: 39, total_revenue: 31954.84
537. seller_zip_code_prefix: 88,504, total_orders: 38, total_revenue: 11854.42
538. seller_zip_code_prefix: 9,131, total_orders: 38, total_revenue: 4441.00
539. seller_zip_code_prefix: 85,875, total_orders: 38, total_revenue: 3427.40
540. seller_zip_code_prefix: 6,653, total_orders: 38, total_revenue: 6735.95
541. seller_zip_code_prefix: 83,324, total_orders: 38, total_revenue: 3385.21
542. seller_zip_code_prefix: 12,080, total_orders: 38, total_revenue: 3953.52
543. seller_zip_code_prefix: 32,185, total_orders: 38, total_revenue: 4136.41
544. seller_zip_code_prefix: 13,500, total_orders: 38, total_revenue: 5177.13
545. seller_zip_code_prefix: 14,096, total_orders: 38, total_revenue: 6493.64
546. seller_zip_code_prefix: 4,133, total_orders: 38, total_revenue: 4273.00
547. seller_zip_code_prefix: 3,210, total_orders: 38, total_revenue: 5899.05
548. seller_zip_code_prefix: 81,070, total_orders: 38, total_revenue: 6836.31
549. seller_zip_code_prefix: 3,018, total_orders: 38, total_revenue: 4158.65
550. seller_zip_code_prefix: 4,362, total_orders: 38, total_revenue: 1522.68
551. seller_zip_code_prefix: 6,717, total_orders: 38, total_revenue: 5009.48
552. seller_zip_code_prefix: 13,730, total_orders: 38, total_revenue: 2968.77
553. seller_zip_code_prefix: 3,287, total_orders: 38, total_revenue: 3329.36
554. seller_zip_code_prefix: 2,839, total_orders: 37, total_revenue: 1508.01
555. seller_zip_code_prefix: 26,020, total_orders: 37, total_revenue: 1530.25
556. seller_zip_code_prefix: 36,050, total_orders: 37, total_revenue: 1621.50
557. seller_zip_code_prefix: 1,123, total_orders: 37, total_revenue: 12135.64
558. seller_zip_code_prefix: 1,209, total_orders: 37, total_revenue: 4098.93
559. seller_zip_code_prefix: 6,317, total_orders: 37, total_revenue: 6632.75
560. seller_zip_code_prefix: 81,650, total_orders: 37, total_revenue: 7944.58
561. seller_zip_code_prefix: 7,170, total_orders: 37, total_revenue: 7420.96
562. seller_zip_code_prefix: 41,342, total_orders: 37, total_revenue: 5412.16
563. seller_zip_code_prefix: 55,325, total_orders: 36, total_revenue: 4829.71
564. seller_zip_code_prefix: 6,144, total_orders: 36, total_revenue: 12655.65
565. seller_zip_code_prefix: 7,025, total_orders: 36, total_revenue: 3466.43
566. seller_zip_code_prefix: 4,445, total_orders: 36, total_revenue: 2255.44
567. seller_zip_code_prefix: 78,095, total_orders: 36, total_revenue: 5188.33
568. seller_zip_code_prefix: 24,120, total_orders: 36, total_revenue: 14452.65
569. seller_zip_code_prefix: 13,520, total_orders: 36, total_revenue: 5768.34
570. seller_zip_code_prefix: 30,315, total_orders: 36, total_revenue: 9206.29
571. seller_zip_code_prefix: 13,253, total_orders: 36, total_revenue: 4881.38
572. seller_zip_code_prefix: 13,043, total_orders: 36, total_revenue: 16707.97
573. seller_zip_code_prefix: 17,300, total_orders: 36, total_revenue: 4972.57
574. seller_zip_code_prefix: 13,560, total_orders: 35, total_revenue: 3430.41
575. seller_zip_code_prefix: 3,437, total_orders: 35, total_revenue: 4581.51
576. seller_zip_code_prefix: 17,250, total_orders: 35, total_revenue: 12388.97
577. seller_zip_code_prefix: 80,220, total_orders: 35, total_revenue: 10809.05
578. seller_zip_code_prefix: 3,550, total_orders: 35, total_revenue: 1961.06
579. seller_zip_code_prefix: 14,312, total_orders: 35, total_revenue: 4639.42
580. seller_zip_code_prefix: 80,620, total_orders: 35, total_revenue: 7750.36
581. seller_zip_code_prefix: 19,013, total_orders: 35, total_revenue: 2746.47
582. seller_zip_code_prefix: 1,222, total_orders: 35, total_revenue: 5423.32
583. seller_zip_code_prefix: 11,015, total_orders: 35, total_revenue: 1992.25
584. seller_zip_code_prefix: 81,130, total_orders: 34, total_revenue: 666.00
585. seller_zip_code_prefix: 30,270, total_orders: 34, total_revenue: 2304.48
586. seller_zip_code_prefix: 37,704, total_orders: 34, total_revenue: 2487.25
587. seller_zip_code_prefix: 4,424, total_orders: 34, total_revenue: 2958.89
588. seller_zip_code_prefix: 5,373, total_orders: 34, total_revenue: 10332.19
589. seller_zip_code_prefix: 15,075, total_orders: 34, total_revenue: 6163.42
590. seller_zip_code_prefix: 13,224, total_orders: 34, total_revenue: 1205.77
591. seller_zip_code_prefix: 18,040, total_orders: 34, total_revenue: 949.36
592. seller_zip_code_prefix: 13,060, total_orders: 33, total_revenue: 4101.59
593. seller_zip_code_prefix: 17,500, total_orders: 33, total_revenue: 8370.25
594. seller_zip_code_prefix: 87,045, total_orders: 33, total_revenue: 10241.74
595. seller_zip_code_prefix: 17,580, total_orders: 33, total_revenue: 9142.23
596. seller_zip_code_prefix: 72,460, total_orders: 33, total_revenue: 10105.35
597. seller_zip_code_prefix: 88,330, total_orders: 33, total_revenue: 7090.98
598. seller_zip_code_prefix: 14,021, total_orders: 33, total_revenue: 1945.54
599. seller_zip_code_prefix: 13,375, total_orders: 33, total_revenue: 3624.01
600. seller_zip_code_prefix: 85,816, total_orders: 33, total_revenue: 2958.79
601. seller_zip_code_prefix: 3,106, total_orders: 32, total_revenue: 4364.99
602. seller_zip_code_prefix: 5,030, total_orders: 32, total_revenue: 1297.90
603. seller_zip_code_prefix: 32,240, total_orders: 32, total_revenue: 3661.68
604. seller_zip_code_prefix: 13,033, total_orders: 32, total_revenue: 1686.97
605. seller_zip_code_prefix: 82,300, total_orders: 32, total_revenue: 6030.17
606. seller_zip_code_prefix: 70,740, total_orders: 32, total_revenue: 2737.55
607. seller_zip_code_prefix: 21,340, total_orders: 32, total_revenue: 5636.88
608. seller_zip_code_prefix: 2,242, total_orders: 32, total_revenue: 1839.67
609. seller_zip_code_prefix: 36,570, total_orders: 32, total_revenue: 26790.59
610. seller_zip_code_prefix: 11,040, total_orders: 32, total_revenue: 5063.76
611. seller_zip_code_prefix: 19,804, total_orders: 32, total_revenue: 4178.82
612. seller_zip_code_prefix: 8,410, total_orders: 32, total_revenue: 5092.89
613. seller_zip_code_prefix: 12,924, total_orders: 32, total_revenue: 23272.78
614. seller_zip_code_prefix: 9,810, total_orders: 32, total_revenue: 3590.25
615. seller_zip_code_prefix: 17,051, total_orders: 32, total_revenue: 2563.79
616. seller_zip_code_prefix: 23,050, total_orders: 32, total_revenue: 4757.16
617. seller_zip_code_prefix: 4,771, total_orders: 31, total_revenue: 12977.99
618. seller_zip_code_prefix: 14,960, total_orders: 31, total_revenue: 7086.13
619. seller_zip_code_prefix: 7,091, total_orders: 31, total_revenue: 2087.13
620. seller_zip_code_prefix: 95,360, total_orders: 31, total_revenue: 7549.71
621. seller_zip_code_prefix: 28,615, total_orders: 31, total_revenue: 51629.49
622. seller_zip_code_prefix: 13,503, total_orders: 31, total_revenue: 4890.66
623. seller_zip_code_prefix: 3,211, total_orders: 31, total_revenue: 3131.82
624. seller_zip_code_prefix: 95,705, total_orders: 31, total_revenue: 4241.20
625. seller_zip_code_prefix: 8,541, total_orders: 30, total_revenue: 3162.32
626. seller_zip_code_prefix: 9,111, total_orders: 30, total_revenue: 2907.18
627. seller_zip_code_prefix: 17,026, total_orders: 30, total_revenue: 2823.10
628. seller_zip_code_prefix: 1,545, total_orders: 30, total_revenue: 5077.03
629. seller_zip_code_prefix: 19,814, total_orders: 30, total_revenue: 5501.01
630. seller_zip_code_prefix: 13,601, total_orders: 30, total_revenue: 5032.71
631. seller_zip_code_prefix: 45,816, total_orders: 30, total_revenue: 8435.21
632. seller_zip_code_prefix: 9,400, total_orders: 30, total_revenue: 2182.72
633. seller_zip_code_prefix: 89,259, total_orders: 30, total_revenue: 2265.28
634. seller_zip_code_prefix: 18,087, total_orders: 30, total_revenue: 1842.26
635. seller_zip_code_prefix: 2,976, total_orders: 30, total_revenue: 5701.45
636. seller_zip_code_prefix: 6,018, total_orders: 30, total_revenue: 4803.94
637. seller_zip_code_prefix: 80,045, total_orders: 30, total_revenue: 7926.03
638. seller_zip_code_prefix: 1,539, total_orders: 30, total_revenue: 13563.66
639. seller_zip_code_prefix: 6,696, total_orders: 29, total_revenue: 4554.46
640. seller_zip_code_prefix: 2,189, total_orders: 29, total_revenue: 1370.22
641. seller_zip_code_prefix: 88,704, total_orders: 29, total_revenue: 6269.80
642. seller_zip_code_prefix: 3,186, total_orders: 29, total_revenue: 6892.73
643. seller_zip_code_prefix: 95,020, total_orders: 29, total_revenue: 3699.02
644. seller_zip_code_prefix: 4,880, total_orders: 29, total_revenue: 4232.65
645. seller_zip_code_prefix: 3,632, total_orders: 29, total_revenue: 4568.71
646. seller_zip_code_prefix: 70,719, total_orders: 29, total_revenue: 2054.52
647. seller_zip_code_prefix: 1,224, total_orders: 29, total_revenue: 1213.03
648. seller_zip_code_prefix: 17,032, total_orders: 29, total_revenue: 7477.33
649. seller_zip_code_prefix: 61,658, total_orders: 28, total_revenue: 3535.16
650. seller_zip_code_prefix: 13,085, total_orders: 28, total_revenue: 3495.52
651. seller_zip_code_prefix: 89,228, total_orders: 28, total_revenue: 11003.89
652. seller_zip_code_prefix: 2,150, total_orders: 28, total_revenue: 5790.48
653. seller_zip_code_prefix: 93,348, total_orders: 28, total_revenue: 9042.36
654. seller_zip_code_prefix: 19,023, total_orders: 28, total_revenue: 14674.03
655. seller_zip_code_prefix: 9,751, total_orders: 28, total_revenue: 3630.03
656. seller_zip_code_prefix: 1,239, total_orders: 28, total_revenue: 1811.27
657. seller_zip_code_prefix: 2,265, total_orders: 28, total_revenue: 4310.21
658. seller_zip_code_prefix: 4,250, total_orders: 28, total_revenue: 1185.42
659. seller_zip_code_prefix: 93,180, total_orders: 28, total_revenue: 2614.26
660. seller_zip_code_prefix: 6,236, total_orders: 27, total_revenue: 1559.73
661. seller_zip_code_prefix: 80,510, total_orders: 27, total_revenue: 1692.11
662. seller_zip_code_prefix: 4,087, total_orders: 27, total_revenue: 1074.29
663. seller_zip_code_prefix: 20,021, total_orders: 27, total_revenue: 12478.83
664. seller_zip_code_prefix: 88,350, total_orders: 27, total_revenue: 15196.53
665. seller_zip_code_prefix: 88,075, total_orders: 27, total_revenue: 5841.88
666. seller_zip_code_prefix: 12,020, total_orders: 27, total_revenue: 2107.06
667. seller_zip_code_prefix: 81,530, total_orders: 27, total_revenue: 5563.63
668. seller_zip_code_prefix: 4,156, total_orders: 27, total_revenue: 5932.51
669. seller_zip_code_prefix: 8,832, total_orders: 27, total_revenue: 3794.87
670. seller_zip_code_prefix: 3,161, total_orders: 26, total_revenue: 2831.62
671. seller_zip_code_prefix: 29,480, total_orders: 26, total_revenue: 5019.60
672. seller_zip_code_prefix: 3,178, total_orders: 26, total_revenue: 3686.66
673. seller_zip_code_prefix: 18,185, total_orders: 26, total_revenue: 3501.69
674. seller_zip_code_prefix: 4,130, total_orders: 26, total_revenue: 4298.03
675. seller_zip_code_prefix: 13,840, total_orders: 26, total_revenue: 7322.77
676. seller_zip_code_prefix: 9,070, total_orders: 26, total_revenue: 1353.04
677. seller_zip_code_prefix: 12,242, total_orders: 26, total_revenue: 913.87
678. seller_zip_code_prefix: 35,670, total_orders: 26, total_revenue: 9351.60
679. seller_zip_code_prefix: 74,150, total_orders: 26, total_revenue: 3210.39
680. seller_zip_code_prefix: 9,912, total_orders: 26, total_revenue: 2613.58
681. seller_zip_code_prefix: 7,070, total_orders: 26, total_revenue: 1323.48
682. seller_zip_code_prefix: 8,411, total_orders: 26, total_revenue: 3150.59
683. seller_zip_code_prefix: 13,465, total_orders: 26, total_revenue: 1805.24
684. seller_zip_code_prefix: 80,740, total_orders: 26, total_revenue: 2089.37
685. seller_zip_code_prefix: 3,520, total_orders: 26, total_revenue: 7043.45
686. seller_zip_code_prefix: 14,315, total_orders: 26, total_revenue: 1198.78
687. seller_zip_code_prefix: 89,701, total_orders: 26, total_revenue: 4272.65
688. seller_zip_code_prefix: 1,310, total_orders: 26, total_revenue: 8939.01
689. seller_zip_code_prefix: 25,850, total_orders: 25, total_revenue: 5118.75
690. seller_zip_code_prefix: 11,013, total_orders: 25, total_revenue: 1542.50
691. seller_zip_code_prefix: 85,812, total_orders: 25, total_revenue: 3251.50
692. seller_zip_code_prefix: 4,243, total_orders: 25, total_revenue: 1956.99
693. seller_zip_code_prefix: 81,050, total_orders: 25, total_revenue: 3196.41
694. seller_zip_code_prefix: 26,510, total_orders: 25, total_revenue: 3791.81
695. seller_zip_code_prefix: 85,853, total_orders: 25, total_revenue: 2687.43
696. seller_zip_code_prefix: 37,706, total_orders: 25, total_revenue: 2340.70
697. seller_zip_code_prefix: 4,870, total_orders: 25, total_revenue: 2568.75
698. seller_zip_code_prefix: 23,062, total_orders: 25, total_revenue: 1119.62
699. seller_zip_code_prefix: 9,163, total_orders: 25, total_revenue: 1419.91
700. seller_zip_code_prefix: 6,132, total_orders: 24, total_revenue: 2859.16
701. seller_zip_code_prefix: 83,709, total_orders: 24, total_revenue: 4571.80
702. seller_zip_code_prefix: 22,785, total_orders: 24, total_revenue: 1178.13
703. seller_zip_code_prefix: 13,160, total_orders: 24, total_revenue: 2973.98
704. seller_zip_code_prefix: 6,080, total_orders: 24, total_revenue: 4811.84
705. seller_zip_code_prefix: 85,904, total_orders: 24, total_revenue: 3099.02
706. seller_zip_code_prefix: 5,632, total_orders: 24, total_revenue: 932.91
707. seller_zip_code_prefix: 3,461, total_orders: 24, total_revenue: 2425.38
708. seller_zip_code_prefix: 82,515, total_orders: 24, total_revenue: 1655.96
709. seller_zip_code_prefix: 37,074, total_orders: 24, total_revenue: 10615.33
710. seller_zip_code_prefix: 13,901, total_orders: 24, total_revenue: 2247.93
711. seller_zip_code_prefix: 1,040, total_orders: 24, total_revenue: 8924.95
712. seller_zip_code_prefix: 4,122, total_orders: 24, total_revenue: 10022.07
713. seller_zip_code_prefix: 6,715, total_orders: 24, total_revenue: 514.19
714. seller_zip_code_prefix: 6,711, total_orders: 24, total_revenue: 640.03
715. seller_zip_code_prefix: 4,761, total_orders: 24, total_revenue: 2422.22
716. seller_zip_code_prefix: 9,121, total_orders: 24, total_revenue: 5742.40
717. seller_zip_code_prefix: 85,640, total_orders: 24, total_revenue: 2033.27
718. seller_zip_code_prefix: 89,520, total_orders: 24, total_revenue: 5851.79
719. seller_zip_code_prefix: 5,201, total_orders: 24, total_revenue: 1345.46
720. seller_zip_code_prefix: 13,960, total_orders: 24, total_revenue: 2160.85
721. seller_zip_code_prefix: 7,600, total_orders: 23, total_revenue: 2724.11
722. seller_zip_code_prefix: 15,840, total_orders: 23, total_revenue: 11488.55
723. seller_zip_code_prefix: 95,013, total_orders: 23, total_revenue: 1432.78
724. seller_zip_code_prefix: 4,571, total_orders: 23, total_revenue: 3983.27
725. seller_zip_code_prefix: 9,090, total_orders: 23, total_revenue: 1655.97
726. seller_zip_code_prefix: 3,059, total_orders: 23, total_revenue: 2272.93
727. seller_zip_code_prefix: 36,325, total_orders: 23, total_revenue: 3426.91
728. seller_zip_code_prefix: 88,750, total_orders: 23, total_revenue: 2945.00
729. seller_zip_code_prefix: 13,140, total_orders: 23, total_revenue: 5171.57
730. seller_zip_code_prefix: 4,613, total_orders: 23, total_revenue: 1273.73
731. seller_zip_code_prefix: 5,634, total_orders: 23, total_revenue: 1830.15
732. seller_zip_code_prefix: 87,070, total_orders: 23, total_revenue: 737.20
733. seller_zip_code_prefix: 14,091, total_orders: 23, total_revenue: 1593.82
734. seller_zip_code_prefix: 24,346, total_orders: 23, total_revenue: 2437.97
735. seller_zip_code_prefix: 9,175, total_orders: 23, total_revenue: 2013.13
736. seller_zip_code_prefix: 17,512, total_orders: 23, total_revenue: 1401.36
737. seller_zip_code_prefix: 59,020, total_orders: 23, total_revenue: 971.92
738. seller_zip_code_prefix: 95,995, total_orders: 23, total_revenue: 4049.36
739. seller_zip_code_prefix: 26,525, total_orders: 23, total_revenue: 5694.20
740. seller_zip_code_prefix: 1,129, total_orders: 23, total_revenue: 1960.90
741. seller_zip_code_prefix: 25,750, total_orders: 22, total_revenue: 1235.18
742. seller_zip_code_prefix: 83,280, total_orders: 22, total_revenue: 2940.92
743. seller_zip_code_prefix: 13,482, total_orders: 22, total_revenue: 2839.42
744. seller_zip_code_prefix: 15,115, total_orders: 22, total_revenue: 4434.02
745. seller_zip_code_prefix: 19,020, total_orders: 22, total_revenue: 3088.24
746. seller_zip_code_prefix: 3,725, total_orders: 22, total_revenue: 5321.90
747. seller_zip_code_prefix: 20,051, total_orders: 22, total_revenue: 1333.69
748. seller_zip_code_prefix: 4,776, total_orders: 22, total_revenue: 3433.89
749. seller_zip_code_prefix: 3,514, total_orders: 22, total_revenue: 2250.70
750. seller_zip_code_prefix: 6,056, total_orders: 22, total_revenue: 3420.45
751. seller_zip_code_prefix: 90,240, total_orders: 22, total_revenue: 2316.56
752. seller_zip_code_prefix: 26,285, total_orders: 22, total_revenue: 2410.68
753. seller_zip_code_prefix: 75,123, total_orders: 22, total_revenue: 2381.35
754. seller_zip_code_prefix: 3,068, total_orders: 22, total_revenue: 3049.29
755. seller_zip_code_prefix: 3,694, total_orders: 22, total_revenue: 7212.65
756. seller_zip_code_prefix: 15,041, total_orders: 22, total_revenue: 10561.09
757. seller_zip_code_prefix: 46,430, total_orders: 22, total_revenue: 18733.18
758. seller_zip_code_prefix: 87,120, total_orders: 22, total_revenue: 1788.34
759. seller_zip_code_prefix: 3,533, total_orders: 22, total_revenue: 3415.20
760. seller_zip_code_prefix: 26,551, total_orders: 22, total_revenue: 1515.35
761. seller_zip_code_prefix: 76,400, total_orders: 22, total_revenue: 3002.84
762. seller_zip_code_prefix: 8,599, total_orders: 22, total_revenue: 3909.94
763. seller_zip_code_prefix: 4,281, total_orders: 22, total_revenue: 7799.52
764. seller_zip_code_prefix: 29,260, total_orders: 21, total_revenue: 1237.06
765. seller_zip_code_prefix: 82,540, total_orders: 21, total_revenue: 8051.34
766. seller_zip_code_prefix: 83,070, total_orders: 21, total_revenue: 2337.01
767. seller_zip_code_prefix: 98,975, total_orders: 21, total_revenue: 1891.30
768. seller_zip_code_prefix: 80,420, total_orders: 21, total_revenue: 8616.72
769. seller_zip_code_prefix: 45,658, total_orders: 21, total_revenue: 9644.62
770. seller_zip_code_prefix: 35,162, total_orders: 21, total_revenue: 7467.39
771. seller_zip_code_prefix: 87,005, total_orders: 21, total_revenue: 1436.21
772. seller_zip_code_prefix: 7,402, total_orders: 21, total_revenue: 1983.99
773. seller_zip_code_prefix: 6,900, total_orders: 21, total_revenue: 727.33
774. seller_zip_code_prefix: 4,857, total_orders: 21, total_revenue: 3704.63
775. seller_zip_code_prefix: 3,679, total_orders: 21, total_revenue: 2485.24
776. seller_zip_code_prefix: 83,321, total_orders: 21, total_revenue: 9797.41
777. seller_zip_code_prefix: 81,460, total_orders: 21, total_revenue: 2228.07
778. seller_zip_code_prefix: 2,336, total_orders: 21, total_revenue: 1014.92
779. seller_zip_code_prefix: 13,830, total_orders: 21, total_revenue: 4665.98
780. seller_zip_code_prefix: 1,201, total_orders: 21, total_revenue: 14835.86
781. seller_zip_code_prefix: 85,960, total_orders: 21, total_revenue: 2023.56
782. seller_zip_code_prefix: 13,835, total_orders: 21, total_revenue: 3627.27
783. seller_zip_code_prefix: 81,730, total_orders: 21, total_revenue: 9332.18
784. seller_zip_code_prefix: 89,108, total_orders: 21, total_revenue: 3373.13
785. seller_zip_code_prefix: 89,030, total_orders: 20, total_revenue: 4707.44
786. seller_zip_code_prefix: 1,230, total_orders: 20, total_revenue: 2694.72
787. seller_zip_code_prefix: 28,495, total_orders: 20, total_revenue: 1926.18
788. seller_zip_code_prefix: 4,696, total_orders: 20, total_revenue: 9968.50
789. seller_zip_code_prefix: 80,030, total_orders: 20, total_revenue: 2828.66
790. seller_zip_code_prefix: 89,053, total_orders: 20, total_revenue: 2523.79
791. seller_zip_code_prefix: 30,620, total_orders: 20, total_revenue: 4850.51
792. seller_zip_code_prefix: 5,713, total_orders: 20, total_revenue: 8263.28
793. seller_zip_code_prefix: 95,034, total_orders: 20, total_revenue: 12863.41
794. seller_zip_code_prefix: 88,306, total_orders: 20, total_revenue: 2772.43
795. seller_zip_code_prefix: 3,563, total_orders: 20, total_revenue: 1413.52
796. seller_zip_code_prefix: 88,037, total_orders: 20, total_revenue: 3785.37
797. seller_zip_code_prefix: 18,760, total_orders: 20, total_revenue: 2227.59
798. seller_zip_code_prefix: 3,322, total_orders: 20, total_revenue: 5909.15
799. seller_zip_code_prefix: 14,055, total_orders: 20, total_revenue: 2096.49
800. seller_zip_code_prefix: 72,233, total_orders: 20, total_revenue: 2101.82
801. seller_zip_code_prefix: 13,145, total_orders: 20, total_revenue: 5000.38
802. seller_zip_code_prefix: 79,107, total_orders: 20, total_revenue: 4066.72
803. seller_zip_code_prefix: 2,969, total_orders: 20, total_revenue: 659.45
804. seller_zip_code_prefix: 88,801, total_orders: 20, total_revenue: 4471.92
805. seller_zip_code_prefix: 8,140, total_orders: 20, total_revenue: 23695.20
806. seller_zip_code_prefix: 5,008, total_orders: 20, total_revenue: 3476.70
807. seller_zip_code_prefix: 82,560, total_orders: 20, total_revenue: 1667.08
808. seller_zip_code_prefix: 13,424, total_orders: 20, total_revenue: 1449.77
809. seller_zip_code_prefix: 93,700, total_orders: 20, total_revenue: 10691.53
810. seller_zip_code_prefix: 81,560, total_orders: 20, total_revenue: 1993.76
811. seller_zip_code_prefix: 18,017, total_orders: 19, total_revenue: 654.44
812. seller_zip_code_prefix: 1,001, total_orders: 19, total_revenue: 1079.90
813. seller_zip_code_prefix: 80,060, total_orders: 19, total_revenue: 2493.51
814. seller_zip_code_prefix: 91,920, total_orders: 19, total_revenue: 4292.71
815. seller_zip_code_prefix: 5,468, total_orders: 19, total_revenue: 2195.61
816. seller_zip_code_prefix: 87,160, total_orders: 19, total_revenue: 1030.18
817. seller_zip_code_prefix: 89,069, total_orders: 19, total_revenue: 1980.27
818. seller_zip_code_prefix: 20,910, total_orders: 19, total_revenue: 1219.26
819. seller_zip_code_prefix: 81,810, total_orders: 19, total_revenue: 1601.35
820. seller_zip_code_prefix: 11,085, total_orders: 19, total_revenue: 573.40
821. seller_zip_code_prefix: 81,210, total_orders: 19, total_revenue: 1956.14
822. seller_zip_code_prefix: 24,020, total_orders: 19, total_revenue: 3626.15
823. seller_zip_code_prefix: 15,085, total_orders: 19, total_revenue: 6084.33
824. seller_zip_code_prefix: 14,095, total_orders: 19, total_revenue: 1978.23
825. seller_zip_code_prefix: 11,680, total_orders: 19, total_revenue: 1747.69
826. seller_zip_code_prefix: 9,411, total_orders: 19, total_revenue: 800.27
827. seller_zip_code_prefix: 9,921, total_orders: 19, total_revenue: 2443.22
828. seller_zip_code_prefix: 88,020, total_orders: 19, total_revenue: 2386.20
829. seller_zip_code_prefix: 6,380, total_orders: 18, total_revenue: 743.67
830. seller_zip_code_prefix: 86,030, total_orders: 18, total_revenue: 3206.98
831. seller_zip_code_prefix: 4,104, total_orders: 18, total_revenue: 3974.85
832. seller_zip_code_prefix: 3,390, total_orders: 18, total_revenue: 25185.49
833. seller_zip_code_prefix: 70,767, total_orders: 18, total_revenue: 4092.21
834. seller_zip_code_prefix: 25,730, total_orders: 18, total_revenue: 1949.44
835. seller_zip_code_prefix: 84,178, total_orders: 18, total_revenue: 9624.26
836. seller_zip_code_prefix: 4,693, total_orders: 18, total_revenue: 2404.97
837. seller_zip_code_prefix: 14,150, total_orders: 18, total_revenue: 12758.93
838. seller_zip_code_prefix: 21,921, total_orders: 18, total_revenue: 1994.93
839. seller_zip_code_prefix: 12,240, total_orders: 18, total_revenue: 2615.59
840. seller_zip_code_prefix: 31,844, total_orders: 18, total_revenue: 1862.33
841. seller_zip_code_prefix: 3,303, total_orders: 18, total_revenue: 1549.39
842. seller_zip_code_prefix: 9,041, total_orders: 18, total_revenue: 1503.55
843. seller_zip_code_prefix: 6,700, total_orders: 18, total_revenue: 4416.52
844. seller_zip_code_prefix: 75,901, total_orders: 18, total_revenue: 4791.38
845. seller_zip_code_prefix: 15,137, total_orders: 18, total_revenue: 1420.20
846. seller_zip_code_prefix: 18,550, total_orders: 18, total_revenue: 1215.40
847. seller_zip_code_prefix: 37,165, total_orders: 18, total_revenue: 4092.64
848. seller_zip_code_prefix: 35,400, total_orders: 18, total_revenue: 2188.86
849. seller_zip_code_prefix: 13,150, total_orders: 17, total_revenue: 6339.51
850. seller_zip_code_prefix: 13,165, total_orders: 17, total_revenue: 1047.15
851. seller_zip_code_prefix: 4,726, total_orders: 17, total_revenue: 12028.79
852. seller_zip_code_prefix: 86,065, total_orders: 17, total_revenue: 7598.11
853. seller_zip_code_prefix: 88,308, total_orders: 17, total_revenue: 1300.64
854. seller_zip_code_prefix: 11,720, total_orders: 17, total_revenue: 1571.71
855. seller_zip_code_prefix: 32,310, total_orders: 17, total_revenue: 1804.07
856. seller_zip_code_prefix: 73,020, total_orders: 17, total_revenue: 6042.42
857. seller_zip_code_prefix: 87,702, total_orders: 17, total_revenue: 2238.34
858. seller_zip_code_prefix: 13,215, total_orders: 17, total_revenue: 3924.29
859. seller_zip_code_prefix: 24,813, total_orders: 17, total_revenue: 663.72
860. seller_zip_code_prefix: 4,905, total_orders: 17, total_revenue: 2101.35
861. seller_zip_code_prefix: 4,719, total_orders: 17, total_revenue: 2660.91
862. seller_zip_code_prefix: 88,960, total_orders: 17, total_revenue: 13304.14
863. seller_zip_code_prefix: 1,035, total_orders: 17, total_revenue: 720.53
864. seller_zip_code_prefix: 1,529, total_orders: 17, total_revenue: 767.70
865. seller_zip_code_prefix: 16,022, total_orders: 17, total_revenue: 1411.13
866. seller_zip_code_prefix: 2,036, total_orders: 17, total_revenue: 2349.91
867. seller_zip_code_prefix: 83,402, total_orders: 17, total_revenue: 1033.27
868. seller_zip_code_prefix: 4,714, total_orders: 17, total_revenue: 1569.24
869. seller_zip_code_prefix: 85,804, total_orders: 17, total_revenue: 1318.49
870. seller_zip_code_prefix: 6,703, total_orders: 17, total_revenue: 2641.44
871. seller_zip_code_prefix: 80,710, total_orders: 17, total_revenue: 2972.68
872. seller_zip_code_prefix: 3,445, total_orders: 17, total_revenue: 1313.16
873. seller_zip_code_prefix: 86,702, total_orders: 17, total_revenue: 2006.41
874. seller_zip_code_prefix: 13,690, total_orders: 17, total_revenue: 3603.58
875. seller_zip_code_prefix: 27,321, total_orders: 17, total_revenue: 2896.23
876. seller_zip_code_prefix: 95,076, total_orders: 17, total_revenue: 1402.58
877. seller_zip_code_prefix: 79,400, total_orders: 17, total_revenue: 3108.83
878. seller_zip_code_prefix: 89,036, total_orders: 17, total_revenue: 1691.82
879. seller_zip_code_prefix: 4,058, total_orders: 17, total_revenue: 998.61
880. seller_zip_code_prefix: 20,751, total_orders: 16, total_revenue: 2654.24
881. seller_zip_code_prefix: 8,072, total_orders: 16, total_revenue: 1557.55
882. seller_zip_code_prefix: 4,476, total_orders: 16, total_revenue: 702.94
883. seller_zip_code_prefix: 3,480, total_orders: 16, total_revenue: 1427.97
884. seller_zip_code_prefix: 87,065, total_orders: 16, total_revenue: 3115.60
885. seller_zip_code_prefix: 20,040, total_orders: 16, total_revenue: 8377.28
886. seller_zip_code_prefix: 28,470, total_orders: 16, total_revenue: 2922.33
887. seller_zip_code_prefix: 15,170, total_orders: 16, total_revenue: 2021.62
888. seller_zip_code_prefix: 5,170, total_orders: 16, total_revenue: 1061.28
889. seller_zip_code_prefix: 13,478, total_orders: 16, total_revenue: 8234.36
890. seller_zip_code_prefix: 23,080, total_orders: 16, total_revenue: 1149.86
891. seller_zip_code_prefix: 90,220, total_orders: 16, total_revenue: 1791.44
892. seller_zip_code_prefix: 35,160, total_orders: 16, total_revenue: 3133.12
893. seller_zip_code_prefix: 59,077, total_orders: 16, total_revenue: 6399.95
894. seller_zip_code_prefix: 86,020, total_orders: 16, total_revenue: 13200.16
895. seller_zip_code_prefix: 14,801, total_orders: 16, total_revenue: 7808.64
896. seller_zip_code_prefix: 5,043, total_orders: 16, total_revenue: 1119.53
897. seller_zip_code_prefix: 96,203, total_orders: 16, total_revenue: 1175.75
898. seller_zip_code_prefix: 7,183, total_orders: 16, total_revenue: 1403.38
899. seller_zip_code_prefix: 6,283, total_orders: 16, total_revenue: 4009.34
900. seller_zip_code_prefix: 22,745, total_orders: 16, total_revenue: 5800.98
901. seller_zip_code_prefix: 6,730, total_orders: 16, total_revenue: 2697.83
902. seller_zip_code_prefix: 60,710, total_orders: 16, total_revenue: 8174.80
903. seller_zip_code_prefix: 13,056, total_orders: 16, total_revenue: 969.60
904. seller_zip_code_prefix: 13,418, total_orders: 16, total_revenue: 1561.42
905. seller_zip_code_prefix: 72,801, total_orders: 16, total_revenue: 2720.93
906. seller_zip_code_prefix: 20,770, total_orders: 16, total_revenue: 1164.38
907. seller_zip_code_prefix: 17,052, total_orders: 16, total_revenue: 2393.02
908. seller_zip_code_prefix: 15,130, total_orders: 16, total_revenue: 2713.47
909. seller_zip_code_prefix: 22,640, total_orders: 16, total_revenue: 4517.52
910. seller_zip_code_prefix: 6,513, total_orders: 16, total_revenue: 4607.15
911. seller_zip_code_prefix: 37,570, total_orders: 16, total_revenue: 3135.23
912. seller_zip_code_prefix: 88,210, total_orders: 16, total_revenue: 1721.29
913. seller_zip_code_prefix: 81,320, total_orders: 16, total_revenue: 2375.45
914. seller_zip_code_prefix: 58,280, total_orders: 16, total_revenue: 15046.63
915. seller_zip_code_prefix: 45,810, total_orders: 15, total_revenue: 1774.94
916. seller_zip_code_prefix: 15,350, total_orders: 15, total_revenue: 1123.99
917. seller_zip_code_prefix: 8,420, total_orders: 15, total_revenue: 2861.11
918. seller_zip_code_prefix: 89,070, total_orders: 15, total_revenue: 2101.48
919. seller_zip_code_prefix: 35,180, total_orders: 15, total_revenue: 7686.31
920. seller_zip_code_prefix: 4,270, total_orders: 15, total_revenue: 631.32
921. seller_zip_code_prefix: 8,430, total_orders: 15, total_revenue: 1244.65
922. seller_zip_code_prefix: 86,060, total_orders: 15, total_revenue: 2455.20
923. seller_zip_code_prefix: 15,290, total_orders: 15, total_revenue: 2917.37
924. seller_zip_code_prefix: 38,405, total_orders: 15, total_revenue: 4182.53
925. seller_zip_code_prefix: 28,990, total_orders: 15, total_revenue: 555.49
926. seller_zip_code_prefix: 4,213, total_orders: 15, total_revenue: 1311.08
927. seller_zip_code_prefix: 3,191, total_orders: 15, total_revenue: 1001.32
928. seller_zip_code_prefix: 2,451, total_orders: 15, total_revenue: 2378.63
929. seller_zip_code_prefix: 3,667, total_orders: 15, total_revenue: 24487.60
930. seller_zip_code_prefix: 11,707, total_orders: 15, total_revenue: 1039.32
931. seller_zip_code_prefix: 4,363, total_orders: 15, total_revenue: 959.35
932. seller_zip_code_prefix: 84,010, total_orders: 15, total_revenue: 1799.00
933. seller_zip_code_prefix: 1,206, total_orders: 15, total_revenue: 1828.59
934. seller_zip_code_prefix: 7,180, total_orders: 15, total_revenue: 3706.50
935. seller_zip_code_prefix: 13,570, total_orders: 15, total_revenue: 1680.42
936. seller_zip_code_prefix: 4,275, total_orders: 15, total_revenue: 2699.92
937. seller_zip_code_prefix: 13,487, total_orders: 15, total_revenue: 2835.11
938. seller_zip_code_prefix: 21,825, total_orders: 15, total_revenue: 1225.06
939. seller_zip_code_prefix: 13,505, total_orders: 15, total_revenue: 1274.45
940. seller_zip_code_prefix: 83,800, total_orders: 15, total_revenue: 4005.32
941. seller_zip_code_prefix: 89,255, total_orders: 15, total_revenue: 783.00
942. seller_zip_code_prefix: 88,063, total_orders: 15, total_revenue: 718.77
943. seller_zip_code_prefix: 21,931, total_orders: 14, total_revenue: 2988.68
944. seller_zip_code_prefix: 6,154, total_orders: 14, total_revenue: 620.49
945. seller_zip_code_prefix: 59,152, total_orders: 14, total_revenue: 3710.64
946. seller_zip_code_prefix: 14,078, total_orders: 14, total_revenue: 684.21
947. seller_zip_code_prefix: 3,345, total_orders: 14, total_revenue: 1910.87
948. seller_zip_code_prefix: 60,348, total_orders: 14, total_revenue: 8622.26
949. seller_zip_code_prefix: 28,035, total_orders: 14, total_revenue: 2118.08
950. seller_zip_code_prefix: 82,320, total_orders: 14, total_revenue: 3229.52
951. seller_zip_code_prefix: 30,130, total_orders: 14, total_revenue: 2661.69
952. seller_zip_code_prefix: 9,080, total_orders: 14, total_revenue: 3207.38
953. seller_zip_code_prefix: 15,054, total_orders: 14, total_revenue: 2286.61
954. seller_zip_code_prefix: 89,136, total_orders: 14, total_revenue: 4088.79
955. seller_zip_code_prefix: 7,123, total_orders: 14, total_revenue: 2835.82
956. seller_zip_code_prefix: 2,119, total_orders: 14, total_revenue: 2864.78
957. seller_zip_code_prefix: 13,603, total_orders: 14, total_revenue: 5389.16
958. seller_zip_code_prefix: 17,017, total_orders: 14, total_revenue: 951.72
959. seller_zip_code_prefix: 3,185, total_orders: 14, total_revenue: 2233.82
960. seller_zip_code_prefix: 95,082, total_orders: 14, total_revenue: 10664.81
961. seller_zip_code_prefix: 13,040, total_orders: 14, total_revenue: 3337.48
962. seller_zip_code_prefix: 89,218, total_orders: 14, total_revenue: 503.65
963. seller_zip_code_prefix: 45,820, total_orders: 14, total_revenue: 1880.00
964. seller_zip_code_prefix: 13,501, total_orders: 14, total_revenue: 1246.66
965. seller_zip_code_prefix: 17,509, total_orders: 14, total_revenue: 1677.81
966. seller_zip_code_prefix: 93,608, total_orders: 14, total_revenue: 1092.10
967. seller_zip_code_prefix: 88,090, total_orders: 14, total_revenue: 7452.36
968. seller_zip_code_prefix: 13,420, total_orders: 14, total_revenue: 909.62
969. seller_zip_code_prefix: 88,495, total_orders: 14, total_revenue: 2983.90
970. seller_zip_code_prefix: 88,780, total_orders: 14, total_revenue: 1494.67
971. seller_zip_code_prefix: 13,845, total_orders: 14, total_revenue: 796.22
972. seller_zip_code_prefix: 70,645, total_orders: 14, total_revenue: 713.53
973. seller_zip_code_prefix: 85,200, total_orders: 14, total_revenue: 1905.08
974. seller_zip_code_prefix: 71,825, total_orders: 14, total_revenue: 965.99
975. seller_zip_code_prefix: 88,316, total_orders: 14, total_revenue: 2632.93
976. seller_zip_code_prefix: 3,001, total_orders: 14, total_revenue: 1677.95
977. seller_zip_code_prefix: 86,035, total_orders: 13, total_revenue: 2690.64
978. seller_zip_code_prefix: 2,376, total_orders: 13, total_revenue: 724.47
979. seller_zip_code_prefix: 9,572, total_orders: 13, total_revenue: 1271.59
980. seller_zip_code_prefix: 28,941, total_orders: 13, total_revenue: 984.58
981. seller_zip_code_prefix: 21,635, total_orders: 13, total_revenue: 2107.42
982. seller_zip_code_prefix: 18,136, total_orders: 13, total_revenue: 499.47
983. seller_zip_code_prefix: 3,279, total_orders: 13, total_revenue: 874.18
984. seller_zip_code_prefix: 7,241, total_orders: 13, total_revenue: 1501.37
985. seller_zip_code_prefix: 1,303, total_orders: 13, total_revenue: 2298.16
986. seller_zip_code_prefix: 9,891, total_orders: 13, total_revenue: 1818.28
987. seller_zip_code_prefix: 6,040, total_orders: 13, total_revenue: 1600.88
988. seller_zip_code_prefix: 88,050, total_orders: 13, total_revenue: 2376.30
989. seller_zip_code_prefix: 3,937, total_orders: 13, total_revenue: 655.32
990. seller_zip_code_prefix: 8,730, total_orders: 13, total_revenue: 1410.93
991. seller_zip_code_prefix: 98,910, total_orders: 13, total_revenue: 845.34
992. seller_zip_code_prefix: 8,223, total_orders: 13, total_revenue: 1244.88
993. seller_zip_code_prefix: 89,288, total_orders: 13, total_revenue: 2501.75
994. seller_zip_code_prefix: 8,615, total_orders: 13, total_revenue: 16182.38
995. seller_zip_code_prefix: 3,304, total_orders: 13, total_revenue: 986.39
996. seller_zip_code_prefix: 72,304, total_orders: 13, total_revenue: 4554.88
997. seller_zip_code_prefix: 30,575, total_orders: 13, total_revenue: 966.25
998. seller_zip_code_prefix: 1,421, total_orders: 13, total_revenue: 643.55
999. seller_zip_code_prefix: 31,210, total_orders: 13, total_revenue: 1174.10
1000. seller_zip_code_prefix: 8,280, total_orders: 13, total_revenue: 1496.63
1001. seller_zip_code_prefix: 31,555, total_orders: 13, total_revenue: 2874.22
1002. seller_zip_code_prefix: 5,639, total_orders: 13, total_revenue: 932.36
1003. seller_zip_code_prefix: 2,752, total_orders: 13, total_revenue: 859.57
1004. seller_zip_code_prefix: 19,820, total_orders: 13, total_revenue: 2115.83
1005. seller_zip_code_prefix: 32,372, total_orders: 13, total_revenue: 4058.11
1006. seller_zip_code_prefix: 2,992, total_orders: 13, total_revenue: 1539.70
1007. seller_zip_code_prefix: 89,215, total_orders: 13, total_revenue: 946.43
1008. seller_zip_code_prefix: 9,550, total_orders: 13, total_revenue: 957.26
1009. seller_zip_code_prefix: 89,220, total_orders: 13, total_revenue: 910.72
1010. seller_zip_code_prefix: 13,880, total_orders: 12, total_revenue: 2150.10
1011. seller_zip_code_prefix: 13,561, total_orders: 12, total_revenue: 691.09
1012. seller_zip_code_prefix: 88,135, total_orders: 12, total_revenue: 1030.32
1013. seller_zip_code_prefix: 86,707, total_orders: 12, total_revenue: 2775.63
1014. seller_zip_code_prefix: 13,205, total_orders: 12, total_revenue: 805.65
1015. seller_zip_code_prefix: 95,098, total_orders: 12, total_revenue: 3556.55
1016. seller_zip_code_prefix: 11,990, total_orders: 12, total_revenue: 1862.35
1017. seller_zip_code_prefix: 3,363, total_orders: 12, total_revenue: 1289.53
1018. seller_zip_code_prefix: 95,059, total_orders: 12, total_revenue: 753.62
1019. seller_zip_code_prefix: 52,010, total_orders: 12, total_revenue: 23823.99
1020. seller_zip_code_prefix: 25,035, total_orders: 12, total_revenue: 1149.78
1021. seller_zip_code_prefix: 15,804, total_orders: 12, total_revenue: 756.00
1022. seller_zip_code_prefix: 19,815, total_orders: 12, total_revenue: 2142.85
1023. seller_zip_code_prefix: 4,763, total_orders: 12, total_revenue: 803.05
1024. seller_zip_code_prefix: 5,528, total_orders: 12, total_revenue: 3231.86
1025. seller_zip_code_prefix: 12,943, total_orders: 12, total_revenue: 1724.81
1026. seller_zip_code_prefix: 37,650, total_orders: 12, total_revenue: 1121.02
1027. seller_zip_code_prefix: 27,700, total_orders: 12, total_revenue: 1318.71
1028. seller_zip_code_prefix: 5,705, total_orders: 12, total_revenue: 17057.28
1029. seller_zip_code_prefix: 4,041, total_orders: 12, total_revenue: 1332.87
1030. seller_zip_code_prefix: 86,804, total_orders: 12, total_revenue: 8806.18
1031. seller_zip_code_prefix: 11,030, total_orders: 12, total_revenue: 11062.72
1032. seller_zip_code_prefix: 36,300, total_orders: 12, total_revenue: 1606.63
1033. seller_zip_code_prefix: 2,475, total_orders: 12, total_revenue: 1720.95
1034. seller_zip_code_prefix: 36,032, total_orders: 12, total_revenue: 551.73
1035. seller_zip_code_prefix: 83,607, total_orders: 12, total_revenue: 2442.94
1036. seller_zip_code_prefix: 64,033, total_orders: 12, total_revenue: 2965.32
1037. seller_zip_code_prefix: 70,856, total_orders: 12, total_revenue: 4877.64
1038. seller_zip_code_prefix: 13,820, total_orders: 12, total_revenue: 756.42
1039. seller_zip_code_prefix: 33,400, total_orders: 12, total_revenue: 1545.83
1040. seller_zip_code_prefix: 81,720, total_orders: 12, total_revenue: 880.68
1041. seller_zip_code_prefix: 1,530, total_orders: 12, total_revenue: 4880.84
1042. seller_zip_code_prefix: 25,070, total_orders: 12, total_revenue: 7334.10
1043. seller_zip_code_prefix: 72,251, total_orders: 12, total_revenue: 1531.79
1044. seller_zip_code_prefix: 9,182, total_orders: 12, total_revenue: 10567.66
1045. seller_zip_code_prefix: 20,060, total_orders: 12, total_revenue: 7723.87
1046. seller_zip_code_prefix: 21,941, total_orders: 12, total_revenue: 1071.31
1047. seller_zip_code_prefix: 72,210, total_orders: 12, total_revenue: 851.98
1048. seller_zip_code_prefix: 36,576, total_orders: 12, total_revenue: 789.92
1049. seller_zip_code_prefix: 3,612, total_orders: 12, total_revenue: 606.79
1050. seller_zip_code_prefix: 81,930, total_orders: 12, total_revenue: 791.29
1051. seller_zip_code_prefix: 9,721, total_orders: 12, total_revenue: 771.65
1052. seller_zip_code_prefix: 13,504, total_orders: 12, total_revenue: 1763.52
1053. seller_zip_code_prefix: 14,270, total_orders: 12, total_revenue: 2646.94
1054. seller_zip_code_prefix: 13,105, total_orders: 12, total_revenue: 826.60
1055. seller_zip_code_prefix: 99,730, total_orders: 12, total_revenue: 1477.38
1056. seller_zip_code_prefix: 3,062, total_orders: 12, total_revenue: 1065.49
1057. seller_zip_code_prefix: 13,015, total_orders: 12, total_revenue: 3096.88
1058. seller_zip_code_prefix: 13,380, total_orders: 12, total_revenue: 880.23
1059. seller_zip_code_prefix: 95,088, total_orders: 11, total_revenue: 837.67
1060. seller_zip_code_prefix: 30,431, total_orders: 11, total_revenue: 567.40
1061. seller_zip_code_prefix: 34,006, total_orders: 11, total_revenue: 1348.53
1062. seller_zip_code_prefix: 62,170, total_orders: 11, total_revenue: 809.41
1063. seller_zip_code_prefix: 85,830, total_orders: 11, total_revenue: 1644.08
1064. seller_zip_code_prefix: 2,350, total_orders: 11, total_revenue: 2785.96
1065. seller_zip_code_prefix: 29,100, total_orders: 11, total_revenue: 1008.97
1066. seller_zip_code_prefix: 6,453, total_orders: 11, total_revenue: 777.07
1067. seller_zip_code_prefix: 85,880, total_orders: 11, total_revenue: 1646.78
1068. seller_zip_code_prefix: 74,563, total_orders: 11, total_revenue: 984.21
1069. seller_zip_code_prefix: 31,160, total_orders: 11, total_revenue: 1113.17
1070. seller_zip_code_prefix: 93,032, total_orders: 11, total_revenue: 5176.30
1071. seller_zip_code_prefix: 2,047, total_orders: 11, total_revenue: 860.94
1072. seller_zip_code_prefix: 4,708, total_orders: 11, total_revenue: 1115.07
1073. seller_zip_code_prefix: 1,552, total_orders: 11, total_revenue: 2515.55
1074. seller_zip_code_prefix: 83,450, total_orders: 11, total_revenue: 2490.40
1075. seller_zip_code_prefix: 5,104, total_orders: 11, total_revenue: 751.76
1076. seller_zip_code_prefix: 84,920, total_orders: 11, total_revenue: 3835.70
1077. seller_zip_code_prefix: 30,775, total_orders: 11, total_revenue: 1028.99
1078. seller_zip_code_prefix: 5,676, total_orders: 11, total_revenue: 531.88
1079. seller_zip_code_prefix: 12,331, total_orders: 11, total_revenue: 787.75
1080. seller_zip_code_prefix: 3,543, total_orders: 11, total_revenue: 1900.09
1081. seller_zip_code_prefix: 9,633, total_orders: 11, total_revenue: 1692.03
1082. seller_zip_code_prefix: 13,304, total_orders: 11, total_revenue: 442.14
1083. seller_zip_code_prefix: 6,016, total_orders: 11, total_revenue: 1731.55
1084. seller_zip_code_prefix: 38,701, total_orders: 11, total_revenue: 1015.93
1085. seller_zip_code_prefix: 2,929, total_orders: 11, total_revenue: 295.07
1086. seller_zip_code_prefix: 89,052, total_orders: 11, total_revenue: 906.52
1087. seller_zip_code_prefix: 95,110, total_orders: 11, total_revenue: 1023.38
1088. seller_zip_code_prefix: 2,470, total_orders: 11, total_revenue: 1829.91
1089. seller_zip_code_prefix: 13,023, total_orders: 11, total_revenue: 1363.79
1090. seller_zip_code_prefix: 3,319, total_orders: 11, total_revenue: 669.18
1091. seller_zip_code_prefix: 18,604, total_orders: 11, total_revenue: 964.08
1092. seller_zip_code_prefix: 3,318, total_orders: 11, total_revenue: 1213.15
1093. seller_zip_code_prefix: 8,790, total_orders: 11, total_revenue: 1667.91
1094. seller_zip_code_prefix: 89,217, total_orders: 11, total_revenue: 622.38
1095. seller_zip_code_prefix: 32,315, total_orders: 11, total_revenue: 1908.11
1096. seller_zip_code_prefix: 6,766, total_orders: 11, total_revenue: 2243.63
1097. seller_zip_code_prefix: 13,211, total_orders: 11, total_revenue: 4565.04
1098. seller_zip_code_prefix: 14,010, total_orders: 11, total_revenue: 3372.49
1099. seller_zip_code_prefix: 88,137, total_orders: 11, total_revenue: 1241.16
1100. seller_zip_code_prefix: 30,220, total_orders: 11, total_revenue: 9164.51
1101. seller_zip_code_prefix: 3,963, total_orders: 11, total_revenue: 417.47
1102. seller_zip_code_prefix: 23,095, total_orders: 11, total_revenue: 3519.45
1103. seller_zip_code_prefix: 7,242, total_orders: 11, total_revenue: 338.25
1104. seller_zip_code_prefix: 9,571, total_orders: 11, total_revenue: 2058.46
1105. seller_zip_code_prefix: 6,150, total_orders: 11, total_revenue: 1101.41
1106. seller_zip_code_prefix: 18,131, total_orders: 11, total_revenue: 858.85
1107. seller_zip_code_prefix: 3,423, total_orders: 11, total_revenue: 575.49
1108. seller_zip_code_prefix: 18,053, total_orders: 11, total_revenue: 2333.83
1109. seller_zip_code_prefix: 95,270, total_orders: 11, total_revenue: 1987.18
1110. seller_zip_code_prefix: 4,674, total_orders: 11, total_revenue: 3452.63
1111. seller_zip_code_prefix: 7,093, total_orders: 11, total_revenue: 2831.32
1112. seller_zip_code_prefix: 75,124, total_orders: 11, total_revenue: 2495.41
1113. seller_zip_code_prefix: 13,272, total_orders: 11, total_revenue: 1629.11
1114. seller_zip_code_prefix: 96,080, total_orders: 11, total_revenue: 482.47
1115. seller_zip_code_prefix: 60,741, total_orders: 11, total_revenue: 1136.52
1116. seller_zip_code_prefix: 18,279, total_orders: 11, total_revenue: 485.05
1117. seller_zip_code_prefix: 71,931, total_orders: 11, total_revenue: 854.26
1118. seller_zip_code_prefix: 84,925, total_orders: 11, total_revenue: 985.04
1119. seller_zip_code_prefix: 6,246, total_orders: 11, total_revenue: 628.63
1120. seller_zip_code_prefix: 9,180, total_orders: 11, total_revenue: 2021.20
1121. seller_zip_code_prefix: 81,520, total_orders: 11, total_revenue: 1245.58
1122. seller_zip_code_prefix: 92,020, total_orders: 11, total_revenue: 836.83
1123. seller_zip_code_prefix: 18,530, total_orders: 11, total_revenue: 1783.89
1124. seller_zip_code_prefix: 24,900, total_orders: 11, total_revenue: 1787.94
1125. seller_zip_code_prefix: 89,165, total_orders: 10, total_revenue: 1654.32
1126. seller_zip_code_prefix: 39,740, total_orders: 10, total_revenue: 1478.43
1127. seller_zip_code_prefix: 31,340, total_orders: 10, total_revenue: 2212.60
1128. seller_zip_code_prefix: 87,020, total_orders: 10, total_revenue: 973.71
1129. seller_zip_code_prefix: 7,113, total_orders: 10, total_revenue: 3155.76
1130. seller_zip_code_prefix: 86,690, total_orders: 10, total_revenue: 1035.70
1131. seller_zip_code_prefix: 2,727, total_orders: 10, total_revenue: 685.35
1132. seller_zip_code_prefix: 3,551, total_orders: 10, total_revenue: 705.56
1133. seller_zip_code_prefix: 38,680, total_orders: 10, total_revenue: 862.25
1134. seller_zip_code_prefix: 3,057, total_orders: 10, total_revenue: 3188.24
1135. seller_zip_code_prefix: 13,339, total_orders: 10, total_revenue: 1799.46
1136. seller_zip_code_prefix: 5,879, total_orders: 10, total_revenue: 281.37
1137. seller_zip_code_prefix: 87,505, total_orders: 10, total_revenue: 7479.63
1138. seller_zip_code_prefix: 1,126, total_orders: 10, total_revenue: 2222.91
1139. seller_zip_code_prefix: 1,214, total_orders: 10, total_revenue: 1340.14
1140. seller_zip_code_prefix: 74,305, total_orders: 10, total_revenue: 1148.94
1141. seller_zip_code_prefix: 15,046, total_orders: 10, total_revenue: 1182.77
1142. seller_zip_code_prefix: 4,308, total_orders: 10, total_revenue: 421.27
1143. seller_zip_code_prefix: 87,013, total_orders: 10, total_revenue: 3143.96
1144. seller_zip_code_prefix: 28,605, total_orders: 10, total_revenue: 3195.67
1145. seller_zip_code_prefix: 30,310, total_orders: 10, total_revenue: 659.69
1146. seller_zip_code_prefix: 18,120, total_orders: 10, total_revenue: 722.97
1147. seller_zip_code_prefix: 86,047, total_orders: 10, total_revenue: 1274.26
1148. seller_zip_code_prefix: 12,228, total_orders: 10, total_revenue: 2959.28
1149. seller_zip_code_prefix: 2,532, total_orders: 10, total_revenue: 458.50
1150. seller_zip_code_prefix: 26,255, total_orders: 10, total_revenue: 4247.98
1151. seller_zip_code_prefix: 3,448, total_orders: 10, total_revenue: 5481.98
1152. seller_zip_code_prefix: 1,044, total_orders: 10, total_revenue: 434.28
1153. seller_zip_code_prefix: 7,145, total_orders: 10, total_revenue: 599.13
1154. seller_zip_code_prefix: 2,122, total_orders: 10, total_revenue: 483.37
1155. seller_zip_code_prefix: 9,726, total_orders: 10, total_revenue: 1815.40
1156. seller_zip_code_prefix: 8,041, total_orders: 10, total_revenue: 1080.70
1157. seller_zip_code_prefix: 29,056, total_orders: 10, total_revenue: 1972.08
1158. seller_zip_code_prefix: 3,567, total_orders: 10, total_revenue: 4719.44
1159. seller_zip_code_prefix: 21,040, total_orders: 10, total_revenue: 2225.84
1160. seller_zip_code_prefix: 4,141, total_orders: 10, total_revenue: 1107.64
1161. seller_zip_code_prefix: 85,501, total_orders: 10, total_revenue: 458.20
1162. seller_zip_code_prefix: 7,179, total_orders: 10, total_revenue: 888.05
1163. seller_zip_code_prefix: 9,911, total_orders: 10, total_revenue: 4722.97
1164. seller_zip_code_prefix: 22,713, total_orders: 10, total_revenue: 781.12
1165. seller_zip_code_prefix: 88,352, total_orders: 10, total_revenue: 749.00
1166. seller_zip_code_prefix: 89,170, total_orders: 10, total_revenue: 695.36
1167. seller_zip_code_prefix: 13,219, total_orders: 10, total_revenue: 1749.77
1168. seller_zip_code_prefix: 3,168, total_orders: 10, total_revenue: 1172.36
1169. seller_zip_code_prefix: 31,980, total_orders: 9, total_revenue: 528.30
1170. seller_zip_code_prefix: 9,340, total_orders: 9, total_revenue: 1250.66
1171. seller_zip_code_prefix: 5,004, total_orders: 9, total_revenue: 1017.17
1172. seller_zip_code_prefix: 91,150, total_orders: 9, total_revenue: 993.80
1173. seller_zip_code_prefix: 58,030, total_orders: 9, total_revenue: 1128.24
1174. seller_zip_code_prefix: 88,802, total_orders: 9, total_revenue: 774.16
1175. seller_zip_code_prefix: 2,515, total_orders: 9, total_revenue: 1514.34
1176. seller_zip_code_prefix: 27,345, total_orders: 9, total_revenue: 501.76
1177. seller_zip_code_prefix: 87,060, total_orders: 9, total_revenue: 720.79
1178. seller_zip_code_prefix: 13,178, total_orders: 9, total_revenue: 808.03
1179. seller_zip_code_prefix: 13,900, total_orders: 9, total_revenue: 1584.35
1180. seller_zip_code_prefix: 17,280, total_orders: 9, total_revenue: 1459.53
1181. seller_zip_code_prefix: 5,417, total_orders: 9, total_revenue: 4214.29
1182. seller_zip_code_prefix: 58,865, total_orders: 9, total_revenue: 964.99
1183. seller_zip_code_prefix: 83,820, total_orders: 9, total_revenue: 643.32
1184. seller_zip_code_prefix: 13,041, total_orders: 9, total_revenue: 1158.68
1185. seller_zip_code_prefix: 14,780, total_orders: 9, total_revenue: 843.96
1186. seller_zip_code_prefix: 5,782, total_orders: 9, total_revenue: 384.12
1187. seller_zip_code_prefix: 14,080, total_orders: 9, total_revenue: 1376.74
1188. seller_zip_code_prefix: 76,500, total_orders: 9, total_revenue: 417.92
1189. seller_zip_code_prefix: 7,071, total_orders: 9, total_revenue: 7188.62
1190. seller_zip_code_prefix: 6,311, total_orders: 9, total_revenue: 910.88
1191. seller_zip_code_prefix: 3,244, total_orders: 9, total_revenue: 1221.69
1192. seller_zip_code_prefix: 8,050, total_orders: 9, total_revenue: 5993.92
1193. seller_zip_code_prefix: 18,085, total_orders: 9, total_revenue: 12533.60
1194. seller_zip_code_prefix: 83,707, total_orders: 9, total_revenue: 219.23
1195. seller_zip_code_prefix: 3,673, total_orders: 9, total_revenue: 319.04
1196. seller_zip_code_prefix: 2,422, total_orders: 9, total_revenue: 1269.87
1197. seller_zip_code_prefix: 95,072, total_orders: 9, total_revenue: 927.05
1198. seller_zip_code_prefix: 82,520, total_orders: 9, total_revenue: 1229.40
1199. seller_zip_code_prefix: 4,088, total_orders: 9, total_revenue: 15150.37
1200. seller_zip_code_prefix: 15,055, total_orders: 9, total_revenue: 2326.29
1201. seller_zip_code_prefix: 9,570, total_orders: 9, total_revenue: 1124.92
1202. seller_zip_code_prefix: 30,120, total_orders: 9, total_revenue: 2209.82
1203. seller_zip_code_prefix: 35,660, total_orders: 9, total_revenue: 444.93
1204. seller_zip_code_prefix: 3,654, total_orders: 9, total_revenue: 3067.41
1205. seller_zip_code_prefix: 9,443, total_orders: 9, total_revenue: 215.55
1206. seller_zip_code_prefix: 95,625, total_orders: 9, total_revenue: 3628.17
1207. seller_zip_code_prefix: 22,061, total_orders: 9, total_revenue: 1166.09
1208. seller_zip_code_prefix: 3,548, total_orders: 9, total_revenue: 491.21
1209. seller_zip_code_prefix: 82,040, total_orders: 9, total_revenue: 928.04
1210. seller_zip_code_prefix: 85,900, total_orders: 9, total_revenue: 569.40
1211. seller_zip_code_prefix: 87,140, total_orders: 9, total_revenue: 10918.74
1212. seller_zip_code_prefix: 12,306, total_orders: 9, total_revenue: 257.32
1213. seller_zip_code_prefix: 4,516, total_orders: 9, total_revenue: 246.49
1214. seller_zip_code_prefix: 13,806, total_orders: 9, total_revenue: 1125.61
1215. seller_zip_code_prefix: 6,455, total_orders: 9, total_revenue: 1536.97
1216. seller_zip_code_prefix: 32,180, total_orders: 9, total_revenue: 1396.94
1217. seller_zip_code_prefix: 95,800, total_orders: 9, total_revenue: 1534.52
1218. seller_zip_code_prefix: 18,052, total_orders: 8, total_revenue: 268.22
1219. seller_zip_code_prefix: 9,130, total_orders: 8, total_revenue: 1240.97
1220. seller_zip_code_prefix: 12,914, total_orders: 8, total_revenue: 631.99
1221. seller_zip_code_prefix: 2,611, total_orders: 8, total_revenue: 1227.00
1222. seller_zip_code_prefix: 89,128, total_orders: 8, total_revenue: 7186.89
1223. seller_zip_code_prefix: 31,050, total_orders: 8, total_revenue: 4301.77
1224. seller_zip_code_prefix: 35,557, total_orders: 8, total_revenue: 617.88
1225. seller_zip_code_prefix: 8,573, total_orders: 8, total_revenue: 574.84
1226. seller_zip_code_prefix: 4,251, total_orders: 8, total_revenue: 699.06
1227. seller_zip_code_prefix: 84,430, total_orders: 8, total_revenue: 733.72
1228. seller_zip_code_prefix: 87,035, total_orders: 8, total_revenue: 435.25
1229. seller_zip_code_prefix: 76,900, total_orders: 8, total_revenue: 1621.13
1230. seller_zip_code_prefix: 19,802, total_orders: 8, total_revenue: 777.23
1231. seller_zip_code_prefix: 18,080, total_orders: 8, total_revenue: 1579.66
1232. seller_zip_code_prefix: 3,554, total_orders: 8, total_revenue: 1284.34
1233. seller_zip_code_prefix: 94,965, total_orders: 8, total_revenue: 1484.90
1234. seller_zip_code_prefix: 5,353, total_orders: 8, total_revenue: 275.39
1235. seller_zip_code_prefix: 9,812, total_orders: 8, total_revenue: 218.82
1236. seller_zip_code_prefix: 36,401, total_orders: 8, total_revenue: 433.95
1237. seller_zip_code_prefix: 88,010, total_orders: 8, total_revenue: 357.96
1238. seller_zip_code_prefix: 33,200, total_orders: 8, total_revenue: 1802.80
1239. seller_zip_code_prefix: 6,764, total_orders: 8, total_revenue: 1602.57
1240. seller_zip_code_prefix: 95,150, total_orders: 8, total_revenue: 1287.36
1241. seller_zip_code_prefix: 89,219, total_orders: 8, total_revenue: 1690.75
1242. seller_zip_code_prefix: 83,005, total_orders: 8, total_revenue: 362.61
1243. seller_zip_code_prefix: 89,820, total_orders: 8, total_revenue: 2490.85
1244. seller_zip_code_prefix: 4,710, total_orders: 8, total_revenue: 1641.74
1245. seller_zip_code_prefix: 6,420, total_orders: 8, total_revenue: 590.44
1246. seller_zip_code_prefix: 23,550, total_orders: 8, total_revenue: 913.71
1247. seller_zip_code_prefix: 3,820, total_orders: 8, total_revenue: 1662.85
1248. seller_zip_code_prefix: 4,795, total_orders: 8, total_revenue: 4466.31
1249. seller_zip_code_prefix: 3,449, total_orders: 8, total_revenue: 223.10
1250. seller_zip_code_prefix: 14,015, total_orders: 8, total_revenue: 1573.77
1251. seller_zip_code_prefix: 18,090, total_orders: 8, total_revenue: 695.70
1252. seller_zip_code_prefix: 74,435, total_orders: 8, total_revenue: 629.62
1253. seller_zip_code_prefix: 4,578, total_orders: 8, total_revenue: 711.32
1254. seller_zip_code_prefix: 14,804, total_orders: 8, total_revenue: 494.07
1255. seller_zip_code_prefix: 36,052, total_orders: 8, total_revenue: 5465.49
1256. seller_zip_code_prefix: 13,573, total_orders: 8, total_revenue: 931.22
1257. seller_zip_code_prefix: 11,443, total_orders: 8, total_revenue: 1139.93
1258. seller_zip_code_prefix: 75,640, total_orders: 8, total_revenue: 1465.73
1259. seller_zip_code_prefix: 88,132, total_orders: 8, total_revenue: 2228.04
1260. seller_zip_code_prefix: 3,307, total_orders: 8, total_revenue: 1983.29
1261. seller_zip_code_prefix: 72,125, total_orders: 8, total_revenue: 2019.22
1262. seller_zip_code_prefix: 21,510, total_orders: 8, total_revenue: 10255.21
1263. seller_zip_code_prefix: 31,365, total_orders: 8, total_revenue: 1695.07
1264. seller_zip_code_prefix: 86,039, total_orders: 8, total_revenue: 762.46
1265. seller_zip_code_prefix: 6,501, total_orders: 8, total_revenue: 1090.65
1266. seller_zip_code_prefix: 16,074, total_orders: 8, total_revenue: 336.49
1267. seller_zip_code_prefix: 7,221, total_orders: 8, total_revenue: 334.09
1268. seller_zip_code_prefix: 85,988, total_orders: 8, total_revenue: 4633.46
1269. seller_zip_code_prefix: 4,705, total_orders: 8, total_revenue: 816.51
1270. seller_zip_code_prefix: 13,203, total_orders: 8, total_revenue: 886.37
1271. seller_zip_code_prefix: 3,280, total_orders: 8, total_revenue: 918.40
1272. seller_zip_code_prefix: 91,360, total_orders: 8, total_revenue: 896.83
1273. seller_zip_code_prefix: 6,180, total_orders: 8, total_revenue: 921.80
1274. seller_zip_code_prefix: 7,400, total_orders: 8, total_revenue: 971.43
1275. seller_zip_code_prefix: 17,350, total_orders: 8, total_revenue: 494.01
1276. seller_zip_code_prefix: 89,256, total_orders: 8, total_revenue: 3246.62
1277. seller_zip_code_prefix: 13,506, total_orders: 8, total_revenue: 1701.13
1278. seller_zip_code_prefix: 3,052, total_orders: 8, total_revenue: 252.77
1279. seller_zip_code_prefix: 5,743, total_orders: 8, total_revenue: 1466.12
1280. seller_zip_code_prefix: 3,638, total_orders: 8, total_revenue: 1693.59
1281. seller_zip_code_prefix: 18,401, total_orders: 8, total_revenue: 1078.43
1282. seller_zip_code_prefix: 15,805, total_orders: 8, total_revenue: 2227.73
1283. seller_zip_code_prefix: 3,641, total_orders: 8, total_revenue: 457.03
1284. seller_zip_code_prefix: 95,690, total_orders: 8, total_revenue: 516.20
1285. seller_zip_code_prefix: 13,090, total_orders: 8, total_revenue: 648.23
1286. seller_zip_code_prefix: 4,833, total_orders: 8, total_revenue: 1176.23
1287. seller_zip_code_prefix: 15,806, total_orders: 8, total_revenue: 1501.71
1288. seller_zip_code_prefix: 94,810, total_orders: 7, total_revenue: 592.73
1289. seller_zip_code_prefix: 18,044, total_orders: 7, total_revenue: 874.51
1290. seller_zip_code_prefix: 13,214, total_orders: 7, total_revenue: 409.45
1291. seller_zip_code_prefix: 4,282, total_orders: 7, total_revenue: 538.88
1292. seller_zip_code_prefix: 7,866, total_orders: 7, total_revenue: 869.73
1293. seller_zip_code_prefix: 89,164, total_orders: 7, total_revenue: 1372.93
1294. seller_zip_code_prefix: 87,043, total_orders: 7, total_revenue: 265.96
1295. seller_zip_code_prefix: 30,550, total_orders: 7, total_revenue: 772.83
1296. seller_zip_code_prefix: 11,702, total_orders: 7, total_revenue: 717.04
1297. seller_zip_code_prefix: 4,365, total_orders: 7, total_revenue: 2971.55
1298. seller_zip_code_prefix: 17,018, total_orders: 7, total_revenue: 1768.90
1299. seller_zip_code_prefix: 4,676, total_orders: 7, total_revenue: 716.54
1300. seller_zip_code_prefix: 29,142, total_orders: 7, total_revenue: 597.34
1301. seller_zip_code_prefix: 34,710, total_orders: 7, total_revenue: 1382.68
1302. seller_zip_code_prefix: 4,101, total_orders: 7, total_revenue: 551.54
1303. seller_zip_code_prefix: 3,644, total_orders: 7, total_revenue: 333.18
1304. seller_zip_code_prefix: 15,155, total_orders: 7, total_revenue: 1903.23
1305. seller_zip_code_prefix: 81,260, total_orders: 7, total_revenue: 529.16
1306. seller_zip_code_prefix: 4,615, total_orders: 7, total_revenue: 1063.65
1307. seller_zip_code_prefix: 71,215, total_orders: 7, total_revenue: 837.13
1308. seller_zip_code_prefix: 86,061, total_orders: 7, total_revenue: 586.79
1309. seller_zip_code_prefix: 36,886, total_orders: 7, total_revenue: 861.46
1310. seller_zip_code_prefix: 17,515, total_orders: 7, total_revenue: 1482.47
1311. seller_zip_code_prefix: 13,312, total_orders: 7, total_revenue: 531.38
1312. seller_zip_code_prefix: 84,020, total_orders: 7, total_revenue: 745.05
1313. seller_zip_code_prefix: 19,470, total_orders: 7, total_revenue: 787.26
1314. seller_zip_code_prefix: 14,470, total_orders: 7, total_revenue: 745.92
1315. seller_zip_code_prefix: 1,408, total_orders: 7, total_revenue: 312.57
1316. seller_zip_code_prefix: 5,186, total_orders: 7, total_revenue: 496.03
1317. seller_zip_code_prefix: 87,240, total_orders: 7, total_revenue: 1334.18
1318. seller_zip_code_prefix: 21,820, total_orders: 7, total_revenue: 1758.38
1319. seller_zip_code_prefix: 24,355, total_orders: 7, total_revenue: 7036.19
1320. seller_zip_code_prefix: 19,300, total_orders: 7, total_revenue: 591.83
1321. seller_zip_code_prefix: 2,510, total_orders: 7, total_revenue: 935.19
1322. seller_zip_code_prefix: 2,040, total_orders: 7, total_revenue: 438.99
1323. seller_zip_code_prefix: 81,200, total_orders: 7, total_revenue: 1703.21
1324. seller_zip_code_prefix: 29,032, total_orders: 7, total_revenue: 769.38
1325. seller_zip_code_prefix: 82,800, total_orders: 7, total_revenue: 1197.94
1326. seller_zip_code_prefix: 80,020, total_orders: 7, total_revenue: 649.97
1327. seller_zip_code_prefix: 2,820, total_orders: 7, total_revenue: 646.62
1328. seller_zip_code_prefix: 15,052, total_orders: 7, total_revenue: 570.37
1329. seller_zip_code_prefix: 86,703, total_orders: 7, total_revenue: 3574.06
1330. seller_zip_code_prefix: 6,663, total_orders: 7, total_revenue: 310.67
1331. seller_zip_code_prefix: 5,059, total_orders: 7, total_revenue: 4158.58
1332. seller_zip_code_prefix: 55,002, total_orders: 7, total_revenue: 426.33
1333. seller_zip_code_prefix: 6,763, total_orders: 7, total_revenue: 580.32
1334. seller_zip_code_prefix: 1,411, total_orders: 7, total_revenue: 1267.48
1335. seller_zip_code_prefix: 82,620, total_orders: 7, total_revenue: 1171.47
1336. seller_zip_code_prefix: 83,040, total_orders: 7, total_revenue: 745.57
1337. seller_zip_code_prefix: 14,057, total_orders: 7, total_revenue: 533.88
1338. seller_zip_code_prefix: 1,541, total_orders: 7, total_revenue: 696.62
1339. seller_zip_code_prefix: 88,490, total_orders: 7, total_revenue: 2590.92
1340. seller_zip_code_prefix: 3,581, total_orders: 7, total_revenue: 356.84
1341. seller_zip_code_prefix: 12,224, total_orders: 7, total_revenue: 630.65
1342. seller_zip_code_prefix: 6,465, total_orders: 7, total_revenue: 7615.07
1343. seller_zip_code_prefix: 81,510, total_orders: 7, total_revenue: 358.97
1344. seller_zip_code_prefix: 90,020, total_orders: 7, total_revenue: 1027.37
1345. seller_zip_code_prefix: 4,650, total_orders: 7, total_revenue: 637.91
1346. seller_zip_code_prefix: 88,032, total_orders: 7, total_revenue: 1352.89
1347. seller_zip_code_prefix: 15,050, total_orders: 7, total_revenue: 1493.23
1348. seller_zip_code_prefix: 31,130, total_orders: 7, total_revenue: 1515.27
1349. seller_zip_code_prefix: 2,873, total_orders: 7, total_revenue: 1125.50
1350. seller_zip_code_prefix: 88,138, total_orders: 7, total_revenue: 1216.24
1351. seller_zip_code_prefix: 20,761, total_orders: 7, total_revenue: 1013.59
1352. seller_zip_code_prefix: 32,280, total_orders: 7, total_revenue: 588.83
1353. seller_zip_code_prefix: 83,075, total_orders: 7, total_revenue: 397.42
1354. seller_zip_code_prefix: 13,825, total_orders: 7, total_revenue: 1442.09
1355. seller_zip_code_prefix: 13,310, total_orders: 6, total_revenue: 840.33
1356. seller_zip_code_prefix: 8,020, total_orders: 6, total_revenue: 655.96
1357. seller_zip_code_prefix: 89,295, total_orders: 6, total_revenue: 1609.73
1358. seller_zip_code_prefix: 13,471, total_orders: 6, total_revenue: 1743.00
1359. seller_zip_code_prefix: 80,210, total_orders: 6, total_revenue: 1494.03
1360. seller_zip_code_prefix: 2,522, total_orders: 6, total_revenue: 409.98
1361. seller_zip_code_prefix: 9,750, total_orders: 6, total_revenue: 299.28
1362. seller_zip_code_prefix: 2,281, total_orders: 6, total_revenue: 1787.71
1363. seller_zip_code_prefix: 4,307, total_orders: 6, total_revenue: 644.02
1364. seller_zip_code_prefix: 13,416, total_orders: 6, total_revenue: 336.75
1365. seller_zip_code_prefix: 3,343, total_orders: 6, total_revenue: 258.70
1366. seller_zip_code_prefix: 7,901, total_orders: 6, total_revenue: 293.38
1367. seller_zip_code_prefix: 5,127, total_orders: 6, total_revenue: 699.74
1368. seller_zip_code_prefix: 29,600, total_orders: 6, total_revenue: 413.26
1369. seller_zip_code_prefix: 5,727, total_orders: 6, total_revenue: 1409.75
1370. seller_zip_code_prefix: 29,161, total_orders: 6, total_revenue: 405.27
1371. seller_zip_code_prefix: 2,236, total_orders: 6, total_revenue: 218.70
1372. seller_zip_code_prefix: 9,690, total_orders: 6, total_revenue: 313.68
1373. seller_zip_code_prefix: 19,160, total_orders: 6, total_revenue: 226.81
1374. seller_zip_code_prefix: 5,462, total_orders: 6, total_revenue: 1343.65
1375. seller_zip_code_prefix: 38,650, total_orders: 6, total_revenue: 800.64
1376. seller_zip_code_prefix: 7,056, total_orders: 6, total_revenue: 348.98
1377. seller_zip_code_prefix: 50,751, total_orders: 6, total_revenue: 3068.85
1378. seller_zip_code_prefix: 39,400, total_orders: 6, total_revenue: 3994.63
1379. seller_zip_code_prefix: 7,051, total_orders: 6, total_revenue: 474.26
1380. seller_zip_code_prefix: 38,402, total_orders: 6, total_revenue: 544.53
1381. seller_zip_code_prefix: 3,731, total_orders: 6, total_revenue: 228.05
1382. seller_zip_code_prefix: 36,504, total_orders: 6, total_revenue: 4195.46
1383. seller_zip_code_prefix: 5,685, total_orders: 6, total_revenue: 896.93
1384. seller_zip_code_prefix: 4,843, total_orders: 6, total_revenue: 1655.65
1385. seller_zip_code_prefix: 20,031, total_orders: 6, total_revenue: 1402.39
1386. seller_zip_code_prefix: 3,827, total_orders: 6, total_revenue: 517.62
1387. seller_zip_code_prefix: 5,311, total_orders: 6, total_revenue: 598.08
1388. seller_zip_code_prefix: 92,120, total_orders: 6, total_revenue: 1744.26
1389. seller_zip_code_prefix: 5,041, total_orders: 6, total_revenue: 149.75
1390. seller_zip_code_prefix: 15,500, total_orders: 6, total_revenue: 1612.03
1391. seller_zip_code_prefix: 14,620, total_orders: 6, total_revenue: 921.24
1392. seller_zip_code_prefix: 3,951, total_orders: 6, total_revenue: 1175.80
1393. seller_zip_code_prefix: 91,740, total_orders: 6, total_revenue: 556.81
1394. seller_zip_code_prefix: 86,820, total_orders: 6, total_revenue: 8492.65
1395. seller_zip_code_prefix: 2,334, total_orders: 6, total_revenue: 280.27
1396. seller_zip_code_prefix: 4,276, total_orders: 6, total_revenue: 275.87
1397. seller_zip_code_prefix: 28,800, total_orders: 6, total_revenue: 3626.50
1398. seller_zip_code_prefix: 15,910, total_orders: 6, total_revenue: 1658.09
1399. seller_zip_code_prefix: 23,954, total_orders: 6, total_revenue: 2519.63
1400. seller_zip_code_prefix: 19,027, total_orders: 6, total_revenue: 1041.04
1401. seller_zip_code_prefix: 1,244, total_orders: 6, total_revenue: 1109.65
1402. seller_zip_code_prefix: 83,823, total_orders: 6, total_revenue: 400.51
1403. seller_zip_code_prefix: 89,248, total_orders: 6, total_revenue: 404.93
1404. seller_zip_code_prefix: 19,400, total_orders: 6, total_revenue: 426.76
1405. seller_zip_code_prefix: 6,186, total_orders: 6, total_revenue: 677.13
1406. seller_zip_code_prefix: 88,790, total_orders: 6, total_revenue: 596.59
1407. seller_zip_code_prefix: 7,052, total_orders: 6, total_revenue: 2647.95
1408. seller_zip_code_prefix: 13,613, total_orders: 6, total_revenue: 401.24
1409. seller_zip_code_prefix: 3,647, total_orders: 6, total_revenue: 931.57
1410. seller_zip_code_prefix: 88,113, total_orders: 6, total_revenue: 334.42
1411. seller_zip_code_prefix: 30,150, total_orders: 6, total_revenue: 419.07
1412. seller_zip_code_prefix: 79,090, total_orders: 6, total_revenue: 1154.72
1413. seller_zip_code_prefix: 8,226, total_orders: 6, total_revenue: 2310.95
1414. seller_zip_code_prefix: 6,192, total_orders: 6, total_revenue: 1208.77
1415. seller_zip_code_prefix: 5,051, total_orders: 6, total_revenue: 564.88
1416. seller_zip_code_prefix: 20,261, total_orders: 6, total_revenue: 1564.72
1417. seller_zip_code_prefix: 2,110, total_orders: 6, total_revenue: 590.55
1418. seller_zip_code_prefix: 20,520, total_orders: 6, total_revenue: 515.24
1419. seller_zip_code_prefix: 4,360, total_orders: 6, total_revenue: 484.39
1420. seller_zip_code_prefix: 13,575, total_orders: 6, total_revenue: 801.25
1421. seller_zip_code_prefix: 5,594, total_orders: 6, total_revenue: 421.68
1422. seller_zip_code_prefix: 70,070, total_orders: 6, total_revenue: 1173.93
1423. seller_zip_code_prefix: 2,113, total_orders: 6, total_revenue: 201.04
1424. seller_zip_code_prefix: 3,572, total_orders: 6, total_revenue: 363.28
1425. seller_zip_code_prefix: 76,804, total_orders: 6, total_revenue: 3853.85
1426. seller_zip_code_prefix: 13,084, total_orders: 5, total_revenue: 3018.86
1427. seller_zip_code_prefix: 4,111, total_orders: 5, total_revenue: 1853.90
1428. seller_zip_code_prefix: 8,021, total_orders: 5, total_revenue: 400.87
1429. seller_zip_code_prefix: 1,022, total_orders: 5, total_revenue: 560.36
1430. seller_zip_code_prefix: 79,112, total_orders: 5, total_revenue: 1171.96
1431. seller_zip_code_prefix: 40,243, total_orders: 5, total_revenue: 606.96
1432. seller_zip_code_prefix: 1,220, total_orders: 5, total_revenue: 942.56
1433. seller_zip_code_prefix: 3,407, total_orders: 5, total_revenue: 345.35
1434. seller_zip_code_prefix: 3,410, total_orders: 5, total_revenue: 210.90
1435. seller_zip_code_prefix: 3,103, total_orders: 5, total_revenue: 235.25
1436. seller_zip_code_prefix: 1,023, total_orders: 5, total_revenue: 208.12
1437. seller_zip_code_prefix: 22,050, total_orders: 5, total_revenue: 397.00
1438. seller_zip_code_prefix: 4,827, total_orders: 5, total_revenue: 541.27
1439. seller_zip_code_prefix: 3,589, total_orders: 5, total_revenue: 481.67
1440. seller_zip_code_prefix: 3,560, total_orders: 5, total_revenue: 13273.42
1441. seller_zip_code_prefix: 88,351, total_orders: 5, total_revenue: 518.77
1442. seller_zip_code_prefix: 9,321, total_orders: 5, total_revenue: 354.65
1443. seller_zip_code_prefix: 3,311, total_orders: 5, total_revenue: 347.48
1444. seller_zip_code_prefix: 96,530, total_orders: 5, total_revenue: 403.43
1445. seller_zip_code_prefix: 6,780, total_orders: 5, total_revenue: 1342.95
1446. seller_zip_code_prefix: 12,238, total_orders: 5, total_revenue: 483.77
1447. seller_zip_code_prefix: 4,293, total_orders: 5, total_revenue: 8359.02
1448. seller_zip_code_prefix: 5,786, total_orders: 5, total_revenue: 674.33
1449. seller_zip_code_prefix: 49,055, total_orders: 5, total_revenue: 1229.10
1450. seller_zip_code_prefix: 94,410, total_orders: 5, total_revenue: 379.38
1451. seller_zip_code_prefix: 29,090, total_orders: 5, total_revenue: 972.65
1452. seller_zip_code_prefix: 4,711, total_orders: 5, total_revenue: 779.66
1453. seller_zip_code_prefix: 9,434, total_orders: 5, total_revenue: 837.10
1454. seller_zip_code_prefix: 27,274, total_orders: 5, total_revenue: 761.29
1455. seller_zip_code_prefix: 88,390, total_orders: 5, total_revenue: 451.38
1456. seller_zip_code_prefix: 18,060, total_orders: 5, total_revenue: 7579.55
1457. seller_zip_code_prefix: 12,600, total_orders: 5, total_revenue: 1350.14
1458. seller_zip_code_prefix: 25,530, total_orders: 5, total_revenue: 536.08
1459. seller_zip_code_prefix: 15,803, total_orders: 5, total_revenue: 1415.00
1460. seller_zip_code_prefix: 9,831, total_orders: 5, total_revenue: 3221.53
1461. seller_zip_code_prefix: 76,330, total_orders: 5, total_revenue: 436.65
1462. seller_zip_code_prefix: 89,812, total_orders: 5, total_revenue: 837.83
1463. seller_zip_code_prefix: 37,640, total_orders: 5, total_revenue: 1428.22
1464. seller_zip_code_prefix: 3,063, total_orders: 5, total_revenue: 1002.90
1465. seller_zip_code_prefix: 4,083, total_orders: 5, total_revenue: 1194.30
1466. seller_zip_code_prefix: 13,311, total_orders: 5, total_revenue: 260.87
1467. seller_zip_code_prefix: 88,901, total_orders: 5, total_revenue: 594.58
1468. seller_zip_code_prefix: 88,705, total_orders: 5, total_revenue: 2616.30
1469. seller_zip_code_prefix: 1,309, total_orders: 5, total_revenue: 379.89
1470. seller_zip_code_prefix: 4,009, total_orders: 5, total_revenue: 210.44
1471. seller_zip_code_prefix: 4,296, total_orders: 5, total_revenue: 168.20
1472. seller_zip_code_prefix: 22,051, total_orders: 5, total_revenue: 379.48
1473. seller_zip_code_prefix: 36,071, total_orders: 5, total_revenue: 2612.56
1474. seller_zip_code_prefix: 18,680, total_orders: 5, total_revenue: 328.36
1475. seller_zip_code_prefix: 1,320, total_orders: 5, total_revenue: 207.38
1476. seller_zip_code_prefix: 9,110, total_orders: 5, total_revenue: 157.64
1477. seller_zip_code_prefix: 15,807, total_orders: 5, total_revenue: 1118.60
1478. seller_zip_code_prefix: 44,600, total_orders: 5, total_revenue: 1751.21
1479. seller_zip_code_prefix: 74,230, total_orders: 5, total_revenue: 456.60
1480. seller_zip_code_prefix: 6,332, total_orders: 5, total_revenue: 171.25
1481. seller_zip_code_prefix: 1,210, total_orders: 5, total_revenue: 15200.56
1482. seller_zip_code_prefix: 6,033, total_orders: 5, total_revenue: 253.35
1483. seller_zip_code_prefix: 2,918, total_orders: 5, total_revenue: 412.93
1484. seller_zip_code_prefix: 13,202, total_orders: 5, total_revenue: 6508.70
1485. seller_zip_code_prefix: 91,910, total_orders: 5, total_revenue: 2484.30
1486. seller_zip_code_prefix: 48,602, total_orders: 5, total_revenue: 1089.04
1487. seller_zip_code_prefix: 12,604, total_orders: 5, total_revenue: 598.87
1488. seller_zip_code_prefix: 86,026, total_orders: 5, total_revenue: 7162.33
1489. seller_zip_code_prefix: 21,020, total_orders: 5, total_revenue: 1960.97
1490. seller_zip_code_prefix: 13,073, total_orders: 5, total_revenue: 178.01
1491. seller_zip_code_prefix: 3,976, total_orders: 5, total_revenue: 8483.35
1492. seller_zip_code_prefix: 16,250, total_orders: 5, total_revenue: 311.66
1493. seller_zip_code_prefix: 4,602, total_orders: 5, total_revenue: 247.05
1494. seller_zip_code_prefix: 7,411, total_orders: 5, total_revenue: 927.83
1495. seller_zip_code_prefix: 2,112, total_orders: 5, total_revenue: 921.49
1496. seller_zip_code_prefix: 5,571, total_orders: 5, total_revenue: 1354.24
1497. seller_zip_code_prefix: 29,300, total_orders: 5, total_revenue: 427.13
1498. seller_zip_code_prefix: 13,091, total_orders: 5, total_revenue: 147.67
1499. seller_zip_code_prefix: 4,364, total_orders: 5, total_revenue: 397.94
1500. seller_zip_code_prefix: 20,081, total_orders: 5, total_revenue: 802.61
1501. seller_zip_code_prefix: 49,980, total_orders: 5, total_revenue: 695.59
1502. seller_zip_code_prefix: 83,602, total_orders: 5, total_revenue: 471.01
1503. seller_zip_code_prefix: 90,620, total_orders: 5, total_revenue: 2012.56
1504. seller_zip_code_prefix: 86,360, total_orders: 5, total_revenue: 769.44
1505. seller_zip_code_prefix: 11,446, total_orders: 5, total_revenue: 491.91
1506. seller_zip_code_prefix: 71,906, total_orders: 5, total_revenue: 661.81
1507. seller_zip_code_prefix: 13,251, total_orders: 5, total_revenue: 446.82
1508. seller_zip_code_prefix: 85,903, total_orders: 5, total_revenue: 483.92
1509. seller_zip_code_prefix: 18,220, total_orders: 5, total_revenue: 219.75
1510. seller_zip_code_prefix: 31,565, total_orders: 5, total_revenue: 267.62
1511. seller_zip_code_prefix: 29,107, total_orders: 5, total_revenue: 7168.41
1512. seller_zip_code_prefix: 30,285, total_orders: 5, total_revenue: 1110.01
1513. seller_zip_code_prefix: 5,522, total_orders: 4, total_revenue: 110.17
1514. seller_zip_code_prefix: 11,442, total_orders: 4, total_revenue: 237.80
1515. seller_zip_code_prefix: 86,181, total_orders: 4, total_revenue: 659.57
1516. seller_zip_code_prefix: 21,070, total_orders: 4, total_revenue: 183.72
1517. seller_zip_code_prefix: 29,104, total_orders: 4, total_revenue: 438.88
1518. seller_zip_code_prefix: 1,403, total_orders: 4, total_revenue: 222.06
1519. seller_zip_code_prefix: 9,060, total_orders: 4, total_revenue: 3548.10
1520. seller_zip_code_prefix: 14,784, total_orders: 4, total_revenue: 1326.31
1521. seller_zip_code_prefix: 29,315, total_orders: 4, total_revenue: 1962.41
1522. seller_zip_code_prefix: 88,380, total_orders: 4, total_revenue: 908.64
1523. seller_zip_code_prefix: 5,547, total_orders: 4, total_revenue: 389.22
1524. seller_zip_code_prefix: 17,700, total_orders: 4, total_revenue: 1312.20
1525. seller_zip_code_prefix: 4,558, total_orders: 4, total_revenue: 171.88
1526. seller_zip_code_prefix: 21,545, total_orders: 4, total_revenue: 191.06
1527. seller_zip_code_prefix: 4,679, total_orders: 4, total_revenue: 148.70
1528. seller_zip_code_prefix: 4,319, total_orders: 4, total_revenue: 158.93
1529. seller_zip_code_prefix: 82,900, total_orders: 4, total_revenue: 1657.45
1530. seller_zip_code_prefix: 9,370, total_orders: 4, total_revenue: 515.33
1531. seller_zip_code_prefix: 12,270, total_orders: 4, total_revenue: 1376.94
1532. seller_zip_code_prefix: 81,630, total_orders: 4, total_revenue: 362.97
1533. seller_zip_code_prefix: 3,064, total_orders: 4, total_revenue: 649.23
1534. seller_zip_code_prefix: 95,910, total_orders: 4, total_revenue: 651.49
1535. seller_zip_code_prefix: 4,144, total_orders: 4, total_revenue: 1572.28
1536. seller_zip_code_prefix: 89,082, total_orders: 4, total_revenue: 226.47
1537. seller_zip_code_prefix: 7,747, total_orders: 4, total_revenue: 963.00
1538. seller_zip_code_prefix: 4,317, total_orders: 4, total_revenue: 556.56
1539. seller_zip_code_prefix: 89,207, total_orders: 4, total_revenue: 1085.83
1540. seller_zip_code_prefix: 71,065, total_orders: 4, total_revenue: 575.07
1541. seller_zip_code_prefix: 84,500, total_orders: 4, total_revenue: 612.39
1542. seller_zip_code_prefix: 8,431, total_orders: 4, total_revenue: 178.66
1543. seller_zip_code_prefix: 17,201, total_orders: 4, total_revenue: 186.82
1544. seller_zip_code_prefix: 17,370, total_orders: 4, total_revenue: 215.10
1545. seller_zip_code_prefix: 1,207, total_orders: 4, total_revenue: 727.39
1546. seller_zip_code_prefix: 35,930, total_orders: 4, total_revenue: 277.96
1547. seller_zip_code_prefix: 38,770, total_orders: 4, total_revenue: 1769.59
1548. seller_zip_code_prefix: 13,530, total_orders: 4, total_revenue: 373.07
1549. seller_zip_code_prefix: 83,327, total_orders: 4, total_revenue: 1098.33
1550. seller_zip_code_prefix: 7,024, total_orders: 4, total_revenue: 478.82
1551. seller_zip_code_prefix: 88,353, total_orders: 4, total_revenue: 2353.44
1552. seller_zip_code_prefix: 8,840, total_orders: 4, total_revenue: 5760.96
1553. seller_zip_code_prefix: 6,036, total_orders: 4, total_revenue: 182.22
1554. seller_zip_code_prefix: 90,630, total_orders: 4, total_revenue: 1210.76
1555. seller_zip_code_prefix: 5,315, total_orders: 4, total_revenue: 139.74
1556. seller_zip_code_prefix: 80,250, total_orders: 4, total_revenue: 177.75
1557. seller_zip_code_prefix: 36,773, total_orders: 4, total_revenue: 1963.08
1558. seller_zip_code_prefix: 17,380, total_orders: 4, total_revenue: 63.05
1559. seller_zip_code_prefix: 36,525, total_orders: 4, total_revenue: 433.62
1560. seller_zip_code_prefix: 11,709, total_orders: 4, total_revenue: 366.01
1561. seller_zip_code_prefix: 2,261, total_orders: 4, total_revenue: 89.61
1562. seller_zip_code_prefix: 2,415, total_orders: 4, total_revenue: 381.56
1563. seller_zip_code_prefix: 74,835, total_orders: 4, total_revenue: 1174.41
1564. seller_zip_code_prefix: 3,138, total_orders: 4, total_revenue: 403.22
1565. seller_zip_code_prefix: 29,704, total_orders: 4, total_revenue: 770.12
1566. seller_zip_code_prefix: 6,473, total_orders: 4, total_revenue: 687.95
1567. seller_zip_code_prefix: 98,780, total_orders: 4, total_revenue: 336.96
1568. seller_zip_code_prefix: 89,080, total_orders: 4, total_revenue: 3686.68
1569. seller_zip_code_prefix: 81,900, total_orders: 4, total_revenue: 248.64
1570. seller_zip_code_prefix: 86,975, total_orders: 4, total_revenue: 2027.40
1571. seller_zip_code_prefix: 60,110, total_orders: 4, total_revenue: 841.33
1572. seller_zip_code_prefix: 15,051, total_orders: 4, total_revenue: 569.26
1573. seller_zip_code_prefix: 9,336, total_orders: 4, total_revenue: 224.68
1574. seller_zip_code_prefix: 5,741, total_orders: 4, total_revenue: 220.56
1575. seller_zip_code_prefix: 15,603, total_orders: 4, total_revenue: 3216.31
1576. seller_zip_code_prefix: 4,794, total_orders: 4, total_revenue: 154.26
1577. seller_zip_code_prefix: 83,409, total_orders: 4, total_revenue: 980.45
1578. seller_zip_code_prefix: 14,806, total_orders: 4, total_revenue: 240.70
1579. seller_zip_code_prefix: 1,311, total_orders: 4, total_revenue: 2138.20
1580. seller_zip_code_prefix: 1,208, total_orders: 4, total_revenue: 1330.88
1581. seller_zip_code_prefix: 92,420, total_orders: 4, total_revenue: 205.81
1582. seller_zip_code_prefix: 3,378, total_orders: 4, total_revenue: 127.12
1583. seller_zip_code_prefix: 20,020, total_orders: 4, total_revenue: 1475.24
1584. seller_zip_code_prefix: 13,490, total_orders: 4, total_revenue: 210.57
1585. seller_zip_code_prefix: 3,382, total_orders: 4, total_revenue: 435.57
1586. seller_zip_code_prefix: 74,110, total_orders: 4, total_revenue: 352.64
1587. seller_zip_code_prefix: 2,523, total_orders: 4, total_revenue: 1653.63
1588. seller_zip_code_prefix: 36,408, total_orders: 4, total_revenue: 488.25
1589. seller_zip_code_prefix: 2,518, total_orders: 4, total_revenue: 438.38
1590. seller_zip_code_prefix: 6,268, total_orders: 4, total_revenue: 493.45
1591. seller_zip_code_prefix: 9,687, total_orders: 4, total_revenue: 491.20
1592. seller_zip_code_prefix: 86,046, total_orders: 4, total_revenue: 2218.19
1593. seller_zip_code_prefix: 30,421, total_orders: 4, total_revenue: 1008.49
1594. seller_zip_code_prefix: 82,220, total_orders: 4, total_revenue: 194.78
1595. seller_zip_code_prefix: 16,306, total_orders: 4, total_revenue: 507.13
1596. seller_zip_code_prefix: 2,751, total_orders: 4, total_revenue: 491.33
1597. seller_zip_code_prefix: 2,941, total_orders: 4, total_revenue: 1048.61
1598. seller_zip_code_prefix: 5,319, total_orders: 4, total_revenue: 381.89
1599. seller_zip_code_prefix: 28,950, total_orders: 4, total_revenue: 332.15
1600. seller_zip_code_prefix: 3,658, total_orders: 4, total_revenue: 616.24
1601. seller_zip_code_prefix: 3,565, total_orders: 4, total_revenue: 1512.99
1602. seller_zip_code_prefix: 3,688, total_orders: 4, total_revenue: 134.31
1603. seller_zip_code_prefix: 8,080, total_orders: 4, total_revenue: 1058.49
1604. seller_zip_code_prefix: 14,076, total_orders: 4, total_revenue: 892.03
1605. seller_zip_code_prefix: 31,560, total_orders: 4, total_revenue: 905.55
1606. seller_zip_code_prefix: 17,514, total_orders: 4, total_revenue: 884.31
1607. seller_zip_code_prefix: 35,900, total_orders: 4, total_revenue: 183.53
1608. seller_zip_code_prefix: 89,201, total_orders: 4, total_revenue: 269.56
1609. seller_zip_code_prefix: 36,015, total_orders: 4, total_revenue: 570.83
1610. seller_zip_code_prefix: 8,500, total_orders: 4, total_revenue: 1085.18
1611. seller_zip_code_prefix: 18,111, total_orders: 4, total_revenue: 164.32
1612. seller_zip_code_prefix: 20,551, total_orders: 4, total_revenue: 356.96
1613. seller_zip_code_prefix: 17,030, total_orders: 4, total_revenue: 240.44
1614. seller_zip_code_prefix: 88,813, total_orders: 4, total_revenue: 1168.67
1615. seller_zip_code_prefix: 26,051, total_orders: 4, total_revenue: 765.22
1616. seller_zip_code_prefix: 1,156, total_orders: 4, total_revenue: 299.40
1617. seller_zip_code_prefix: 3,659, total_orders: 4, total_revenue: 3762.08
1618. seller_zip_code_prefix: 52,020, total_orders: 3, total_revenue: 3873.57
1619. seller_zip_code_prefix: 69,005, total_orders: 3, total_revenue: 1258.80
1620. seller_zip_code_prefix: 31,920, total_orders: 3, total_revenue: 1288.59
1621. seller_zip_code_prefix: 93,336, total_orders: 3, total_revenue: 487.44
1622. seller_zip_code_prefix: 89,190, total_orders: 3, total_revenue: 315.44
1623. seller_zip_code_prefix: 17,047, total_orders: 3, total_revenue: 135.73
1624. seller_zip_code_prefix: 14,093, total_orders: 3, total_revenue: 95.24
1625. seller_zip_code_prefix: 6,694, total_orders: 3, total_revenue: 234.04
1626. seller_zip_code_prefix: 12,226, total_orders: 3, total_revenue: 123.75
1627. seller_zip_code_prefix: 1,215, total_orders: 3, total_revenue: 2260.22
1628. seller_zip_code_prefix: 18,076, total_orders: 3, total_revenue: 194.24
1629. seller_zip_code_prefix: 35,300, total_orders: 3, total_revenue: 445.53
1630. seller_zip_code_prefix: 12,916, total_orders: 3, total_revenue: 199.68
1631. seller_zip_code_prefix: 21,320, total_orders: 3, total_revenue: 283.74
1632. seller_zip_code_prefix: 85,301, total_orders: 3, total_revenue: 1546.84
1633. seller_zip_code_prefix: 3,182, total_orders: 3, total_revenue: 199.31
1634. seller_zip_code_prefix: 92,010, total_orders: 3, total_revenue: 185.80
1635. seller_zip_code_prefix: 13,454, total_orders: 3, total_revenue: 151.14
1636. seller_zip_code_prefix: 85,065, total_orders: 3, total_revenue: 820.27
1637. seller_zip_code_prefix: 3,384, total_orders: 3, total_revenue: 299.57
1638. seller_zip_code_prefix: 85,601, total_orders: 3, total_revenue: 295.77
1639. seller_zip_code_prefix: 8,490, total_orders: 3, total_revenue: 695.70
1640. seller_zip_code_prefix: 14,530, total_orders: 3, total_revenue: 380.44
1641. seller_zip_code_prefix: 18,200, total_orders: 3, total_revenue: 532.48
1642. seller_zip_code_prefix: 82,640, total_orders: 3, total_revenue: 130.65
1643. seller_zip_code_prefix: 70,610, total_orders: 3, total_revenue: 846.62
1644. seller_zip_code_prefix: 12,955, total_orders: 3, total_revenue: 203.48
1645. seller_zip_code_prefix: 88,136, total_orders: 3, total_revenue: 230.54
1646. seller_zip_code_prefix: 93,347, total_orders: 3, total_revenue: 649.55
1647. seller_zip_code_prefix: 5,615, total_orders: 3, total_revenue: 306.97
1648. seller_zip_code_prefix: 37,975, total_orders: 3, total_revenue: 227.67
1649. seller_zip_code_prefix: 18,103, total_orders: 3, total_revenue: 188.50
1650. seller_zip_code_prefix: 6,280, total_orders: 3, total_revenue: 192.10
1651. seller_zip_code_prefix: 8,246, total_orders: 3, total_revenue: 572.17
1652. seller_zip_code_prefix: 18,590, total_orders: 3, total_revenue: 9779.46
1653. seller_zip_code_prefix: 15,400, total_orders: 3, total_revenue: 270.49
1654. seller_zip_code_prefix: 2,118, total_orders: 3, total_revenue: 827.97
1655. seller_zip_code_prefix: 5,108, total_orders: 3, total_revenue: 1487.88
1656. seller_zip_code_prefix: 35,540, total_orders: 3, total_revenue: 102.30
1657. seller_zip_code_prefix: 21,240, total_orders: 3, total_revenue: 1328.18
1658. seller_zip_code_prefix: 16,072, total_orders: 3, total_revenue: 192.26
1659. seller_zip_code_prefix: 88,058, total_orders: 3, total_revenue: 768.94
1660. seller_zip_code_prefix: 80,050, total_orders: 3, total_revenue: 477.01
1661. seller_zip_code_prefix: 85,948, total_orders: 3, total_revenue: 231.96
1662. seller_zip_code_prefix: 6,519, total_orders: 3, total_revenue: 1249.52
1663. seller_zip_code_prefix: 60,025, total_orders: 3, total_revenue: 187.20
1664. seller_zip_code_prefix: 4,386, total_orders: 3, total_revenue: 554.45
1665. seller_zip_code_prefix: 4,193, total_orders: 3, total_revenue: 354.37
1666. seller_zip_code_prefix: 8,452, total_orders: 3, total_revenue: 831.26
1667. seller_zip_code_prefix: 89,650, total_orders: 3, total_revenue: 391.07
1668. seller_zip_code_prefix: 13,600, total_orders: 3, total_revenue: 242.43
1669. seller_zip_code_prefix: 44,002, total_orders: 3, total_revenue: 1296.77
1670. seller_zip_code_prefix: 89,210, total_orders: 3, total_revenue: 174.61
1671. seller_zip_code_prefix: 2,916, total_orders: 3, total_revenue: 90.66
1672. seller_zip_code_prefix: 36,213, total_orders: 3, total_revenue: 1113.02
1673. seller_zip_code_prefix: 29,160, total_orders: 3, total_revenue: 215.98
1674. seller_zip_code_prefix: 20,921, total_orders: 3, total_revenue: 910.83
1675. seller_zip_code_prefix: 38,182, total_orders: 3, total_revenue: 1110.54
1676. seller_zip_code_prefix: 70,384, total_orders: 3, total_revenue: 277.32
1677. seller_zip_code_prefix: 86,170, total_orders: 3, total_revenue: 235.11
1678. seller_zip_code_prefix: 95,560, total_orders: 3, total_revenue: 209.88
1679. seller_zip_code_prefix: 29,313, total_orders: 3, total_revenue: 1460.85
1680. seller_zip_code_prefix: 5,061, total_orders: 3, total_revenue: 518.70
1681. seller_zip_code_prefix: 4,537, total_orders: 3, total_revenue: 440.41
1682. seller_zip_code_prefix: 33,600, total_orders: 3, total_revenue: 230.80
1683. seller_zip_code_prefix: 9,380, total_orders: 3, total_revenue: 949.17
1684. seller_zip_code_prefix: 88,036, total_orders: 3, total_revenue: 357.35
1685. seller_zip_code_prefix: 15,062, total_orders: 3, total_revenue: 72.18
1686. seller_zip_code_prefix: 84,172, total_orders: 3, total_revenue: 275.91
1687. seller_zip_code_prefix: 6,449, total_orders: 3, total_revenue: 144.74
1688. seller_zip_code_prefix: 15,800, total_orders: 3, total_revenue: 291.62
1689. seller_zip_code_prefix: 89,900, total_orders: 3, total_revenue: 792.93
1690. seller_zip_code_prefix: 2,544, total_orders: 3, total_revenue: 204.86
1691. seller_zip_code_prefix: 5,048, total_orders: 3, total_revenue: 1390.47
1692. seller_zip_code_prefix: 9,931, total_orders: 3, total_revenue: 1632.99
1693. seller_zip_code_prefix: 95,900, total_orders: 3, total_revenue: 1569.94
1694. seller_zip_code_prefix: 8,070, total_orders: 3, total_revenue: 77.17
1695. seller_zip_code_prefix: 9,251, total_orders: 3, total_revenue: 793.34
1696. seller_zip_code_prefix: 7,062, total_orders: 3, total_revenue: 78.36
1697. seller_zip_code_prefix: 6,539, total_orders: 3, total_revenue: 251.46
1698. seller_zip_code_prefix: 55,602, total_orders: 3, total_revenue: 2341.76
1699. seller_zip_code_prefix: 3,521, total_orders: 3, total_revenue: 76.33
1700. seller_zip_code_prefix: 83,535, total_orders: 3, total_revenue: 905.85
1701. seller_zip_code_prefix: 13,905, total_orders: 3, total_revenue: 529.47
1702. seller_zip_code_prefix: 13,273, total_orders: 3, total_revenue: 112.58
1703. seller_zip_code_prefix: 96,816, total_orders: 3, total_revenue: 453.44
1704. seller_zip_code_prefix: 17,606, total_orders: 3, total_revenue: 514.90
1705. seller_zip_code_prefix: 3,635, total_orders: 3, total_revenue: 7114.69
1706. seller_zip_code_prefix: 81,925, total_orders: 3, total_revenue: 249.98
1707. seller_zip_code_prefix: 4,660, total_orders: 3, total_revenue: 84.01
1708. seller_zip_code_prefix: 86,808, total_orders: 3, total_revenue: 514.93
1709. seller_zip_code_prefix: 3,370, total_orders: 3, total_revenue: 1405.83
1710. seller_zip_code_prefix: 6,409, total_orders: 3, total_revenue: 373.38
1711. seller_zip_code_prefix: 6,286, total_orders: 3, total_revenue: 358.48
1712. seller_zip_code_prefix: 95,840, total_orders: 3, total_revenue: 316.23
1713. seller_zip_code_prefix: 27,972, total_orders: 3, total_revenue: 377.39
1714. seller_zip_code_prefix: 11,440, total_orders: 3, total_revenue: 740.50
1715. seller_zip_code_prefix: 19,865, total_orders: 3, total_revenue: 240.06
1716. seller_zip_code_prefix: 2,880, total_orders: 3, total_revenue: 404.10
1717. seller_zip_code_prefix: 9,540, total_orders: 3, total_revenue: 258.54
1718. seller_zip_code_prefix: 33,940, total_orders: 3, total_revenue: 117.87
1719. seller_zip_code_prefix: 86,802, total_orders: 3, total_revenue: 400.76
1720. seller_zip_code_prefix: 89,180, total_orders: 3, total_revenue: 152.80
1721. seller_zip_code_prefix: 11,430, total_orders: 3, total_revenue: 520.84
1722. seller_zip_code_prefix: 6,436, total_orders: 3, total_revenue: 4874.36
1723. seller_zip_code_prefix: 97,110, total_orders: 3, total_revenue: 1361.28
1724. seller_zip_code_prefix: 96,503, total_orders: 3, total_revenue: 359.03
1725. seller_zip_code_prefix: 83,322, total_orders: 3, total_revenue: 123.73
1726. seller_zip_code_prefix: 6,330, total_orders: 3, total_revenue: 140.29
1727. seller_zip_code_prefix: 74,045, total_orders: 3, total_revenue: 100.78
1728. seller_zip_code_prefix: 31,110, total_orders: 3, total_revenue: 1475.78
1729. seller_zip_code_prefix: 12,995, total_orders: 3, total_revenue: 99.14
1730. seller_zip_code_prefix: 3,416, total_orders: 3, total_revenue: 516.91
1731. seller_zip_code_prefix: 15,061, total_orders: 3, total_revenue: 1199.31
1732. seller_zip_code_prefix: 95,650, total_orders: 3, total_revenue: 394.22
1733. seller_zip_code_prefix: 12,941, total_orders: 3, total_revenue: 83.97
1734. seller_zip_code_prefix: 81,110, total_orders: 3, total_revenue: 124.29
1735. seller_zip_code_prefix: 18,480, total_orders: 3, total_revenue: 270.36
1736. seller_zip_code_prefix: 15,940, total_orders: 3, total_revenue: 125.27
1737. seller_zip_code_prefix: 7,192, total_orders: 3, total_revenue: 441.60
1738. seller_zip_code_prefix: 20,950, total_orders: 3, total_revenue: 386.99
1739. seller_zip_code_prefix: 4,209, total_orders: 3, total_revenue: 320.52
1740. seller_zip_code_prefix: 3,060, total_orders: 3, total_revenue: 137.09
1741. seller_zip_code_prefix: 19,906, total_orders: 3, total_revenue: 498.35
1742. seller_zip_code_prefix: 14,140, total_orders: 3, total_revenue: 176.97
1743. seller_zip_code_prefix: 4,123, total_orders: 3, total_revenue: 676.01
1744. seller_zip_code_prefix: 18,030, total_orders: 3, total_revenue: 7939.25
1745. seller_zip_code_prefix: 17,605, total_orders: 3, total_revenue: 73.37
1746. seller_zip_code_prefix: 7,124, total_orders: 3, total_revenue: 88.74
1747. seller_zip_code_prefix: 6,852, total_orders: 3, total_revenue: 423.90
1748. seller_zip_code_prefix: 38,401, total_orders: 3, total_revenue: 417.42
1749. seller_zip_code_prefix: 6,038, total_orders: 3, total_revenue: 120.22
1750. seller_zip_code_prefix: 91,520, total_orders: 3, total_revenue: 824.18
1751. seller_zip_code_prefix: 74,210, total_orders: 3, total_revenue: 6999.88
1752. seller_zip_code_prefix: 83,833, total_orders: 3, total_revenue: 251.92
1753. seller_zip_code_prefix: 12,401, total_orders: 2, total_revenue: 181.32
1754. seller_zip_code_prefix: 17,560, total_orders: 2, total_revenue: 141.33
1755. seller_zip_code_prefix: 89,825, total_orders: 2, total_revenue: 410.42
1756. seller_zip_code_prefix: 78,820, total_orders: 2, total_revenue: 468.94
1757. seller_zip_code_prefix: 8,150, total_orders: 2, total_revenue: 157.08
1758. seller_zip_code_prefix: 88,270, total_orders: 2, total_revenue: 857.70
1759. seller_zip_code_prefix: 6,807, total_orders: 2, total_revenue: 1320.95
1760. seller_zip_code_prefix: 13,097, total_orders: 2, total_revenue: 235.84
1761. seller_zip_code_prefix: 85,813, total_orders: 2, total_revenue: 380.17
1762. seller_zip_code_prefix: 25,251, total_orders: 2, total_revenue: 70.42
1763. seller_zip_code_prefix: 2,050, total_orders: 2, total_revenue: 70.02
1764. seller_zip_code_prefix: 9,640, total_orders: 2, total_revenue: 107.22
1765. seller_zip_code_prefix: 4,255, total_orders: 2, total_revenue: 507.43
1766. seller_zip_code_prefix: 99,300, total_orders: 2, total_revenue: 609.50
1767. seller_zip_code_prefix: 15,030, total_orders: 2, total_revenue: 422.04
1768. seller_zip_code_prefix: 96,020, total_orders: 2, total_revenue: 81.51
1769. seller_zip_code_prefix: 2,562, total_orders: 2, total_revenue: 222.88
1770. seller_zip_code_prefix: 5,083, total_orders: 2, total_revenue: 187.42
1771. seller_zip_code_prefix: 13,180, total_orders: 2, total_revenue: 51.36
1772. seller_zip_code_prefix: 9,862, total_orders: 2, total_revenue: 62.66
1773. seller_zip_code_prefix: 89,870, total_orders: 2, total_revenue: 262.78
1774. seller_zip_code_prefix: 95,240, total_orders: 2, total_revenue: 330.06
1775. seller_zip_code_prefix: 2,117, total_orders: 2, total_revenue: 759.59
1776. seller_zip_code_prefix: 3,122, total_orders: 2, total_revenue: 55.64
1777. seller_zip_code_prefix: 13,604, total_orders: 2, total_revenue: 1281.23
1778. seller_zip_code_prefix: 5,524, total_orders: 2, total_revenue: 484.80
1779. seller_zip_code_prefix: 89,240, total_orders: 2, total_revenue: 1454.44
1780. seller_zip_code_prefix: 6,795, total_orders: 2, total_revenue: 363.43
1781. seller_zip_code_prefix: 15,131, total_orders: 2, total_revenue: 813.28
1782. seller_zip_code_prefix: 93,900, total_orders: 2, total_revenue: 1474.76
1783. seller_zip_code_prefix: 16,021, total_orders: 2, total_revenue: 237.53
1784. seller_zip_code_prefix: 3,340, total_orders: 2, total_revenue: 216.23
1785. seller_zip_code_prefix: 13,271, total_orders: 2, total_revenue: 4184.77
1786. seller_zip_code_prefix: 6,544, total_orders: 2, total_revenue: 422.25
1787. seller_zip_code_prefix: 18,681, total_orders: 2, total_revenue: 368.95
1788. seller_zip_code_prefix: 4,001, total_orders: 2, total_revenue: 161.80
1789. seller_zip_code_prefix: 80,730, total_orders: 2, total_revenue: 241.21
1790. seller_zip_code_prefix: 28,810, total_orders: 2, total_revenue: 237.60
1791. seller_zip_code_prefix: 38,410, total_orders: 2, total_revenue: 183.89
1792. seller_zip_code_prefix: 4,176, total_orders: 2, total_revenue: 363.88
1793. seller_zip_code_prefix: 80,410, total_orders: 2, total_revenue: 432.12
1794. seller_zip_code_prefix: 6,760, total_orders: 2, total_revenue: 166.99
1795. seller_zip_code_prefix: 86,040, total_orders: 2, total_revenue: 232.47
1796. seller_zip_code_prefix: 9,551, total_orders: 2, total_revenue: 1226.55
1797. seller_zip_code_prefix: 95,500, total_orders: 2, total_revenue: 414.79
1798. seller_zip_code_prefix: 8,596, total_orders: 2, total_revenue: 100.90
1799. seller_zip_code_prefix: 8,220, total_orders: 2, total_revenue: 233.25
1800. seller_zip_code_prefix: 81,030, total_orders: 2, total_revenue: 201.27
1801. seller_zip_code_prefix: 28,660, total_orders: 2, total_revenue: 154.44
1802. seller_zip_code_prefix: 5,269, total_orders: 2, total_revenue: 50.83
1803. seller_zip_code_prefix: 14,025, total_orders: 2, total_revenue: 157.51
1804. seller_zip_code_prefix: 2,750, total_orders: 2, total_revenue: 60.33
1805. seller_zip_code_prefix: 83,091, total_orders: 2, total_revenue: 1882.80
1806. seller_zip_code_prefix: 3,553, total_orders: 2, total_revenue: 249.06
1807. seller_zip_code_prefix: 87,014, total_orders: 2, total_revenue: 289.80
1808. seller_zip_code_prefix: 3,270, total_orders: 2, total_revenue: 667.83
1809. seller_zip_code_prefix: 81,250, total_orders: 2, total_revenue: 564.14
1810. seller_zip_code_prefix: 4,607, total_orders: 2, total_revenue: 436.67
1811. seller_zip_code_prefix: 14,860, total_orders: 2, total_revenue: 71.18
1812. seller_zip_code_prefix: 1,223, total_orders: 2, total_revenue: 546.55
1813. seller_zip_code_prefix: 12,209, total_orders: 2, total_revenue: 1238.90
1814. seller_zip_code_prefix: 17,011, total_orders: 2, total_revenue: 568.36
1815. seller_zip_code_prefix: 89,222, total_orders: 2, total_revenue: 246.65
1816. seller_zip_code_prefix: 3,121, total_orders: 2, total_revenue: 176.14
1817. seller_zip_code_prefix: 3,962, total_orders: 2, total_revenue: 120.88
1818. seller_zip_code_prefix: 89,504, total_orders: 2, total_revenue: 160.67
1819. seller_zip_code_prefix: 92,025, total_orders: 2, total_revenue: 225.65
1820. seller_zip_code_prefix: 15,505, total_orders: 2, total_revenue: 287.51
1821. seller_zip_code_prefix: 21,740, total_orders: 2, total_revenue: 165.50
1822. seller_zip_code_prefix: 30,710, total_orders: 2, total_revenue: 115.52
1823. seller_zip_code_prefix: 5,856, total_orders: 2, total_revenue: 108.73
1824. seller_zip_code_prefix: 3,172, total_orders: 2, total_revenue: 1043.43
1825. seller_zip_code_prefix: 3,643, total_orders: 2, total_revenue: 84.20
1826. seller_zip_code_prefix: 71,936, total_orders: 2, total_revenue: 129.32
1827. seller_zip_code_prefix: 20,785, total_orders: 2, total_revenue: 1262.72
1828. seller_zip_code_prefix: 31,035, total_orders: 2, total_revenue: 202.90
1829. seller_zip_code_prefix: 9,510, total_orders: 2, total_revenue: 345.20
1830. seller_zip_code_prefix: 25,550, total_orders: 2, total_revenue: 347.73
1831. seller_zip_code_prefix: 6,768, total_orders: 2, total_revenue: 232.47
1832. seller_zip_code_prefix: 86,801, total_orders: 2, total_revenue: 155.58
1833. seller_zip_code_prefix: 4,291, total_orders: 2, total_revenue: 86.26
1834. seller_zip_code_prefix: 72,580, total_orders: 2, total_revenue: 264.24
1835. seller_zip_code_prefix: 31,525, total_orders: 2, total_revenue: 327.43
1836. seller_zip_code_prefix: 75,110, total_orders: 2, total_revenue: 182.37
1837. seller_zip_code_prefix: 89,287, total_orders: 2, total_revenue: 458.24
1838. seller_zip_code_prefix: 2,737, total_orders: 2, total_revenue: 163.17
1839. seller_zip_code_prefix: 6,460, total_orders: 2, total_revenue: 171.85
1840. seller_zip_code_prefix: 6,787, total_orders: 2, total_revenue: 369.77
1841. seller_zip_code_prefix: 11,370, total_orders: 2, total_revenue: 397.61
1842. seller_zip_code_prefix: 4,557, total_orders: 2, total_revenue: 84.26
1843. seller_zip_code_prefix: 58,400, total_orders: 2, total_revenue: 149.30
1844. seller_zip_code_prefix: 8,593, total_orders: 2, total_revenue: 334.29
1845. seller_zip_code_prefix: 91,310, total_orders: 2, total_revenue: 183.94
1846. seller_zip_code_prefix: 1,314, total_orders: 2, total_revenue: 277.68
1847. seller_zip_code_prefix: 90,670, total_orders: 2, total_revenue: 2822.75
1848. seller_zip_code_prefix: 15,056, total_orders: 2, total_revenue: 941.07
1849. seller_zip_code_prefix: 6,340, total_orders: 2, total_revenue: 364.93
1850. seller_zip_code_prefix: 17,506, total_orders: 2, total_revenue: 125.00
1851. seller_zip_code_prefix: 1,452, total_orders: 2, total_revenue: 740.97
1852. seller_zip_code_prefix: 1,140, total_orders: 2, total_revenue: 51.54
1853. seller_zip_code_prefix: 88,220, total_orders: 2, total_revenue: 87.70
1854. seller_zip_code_prefix: 11,070, total_orders: 2, total_revenue: 277.22
1855. seller_zip_code_prefix: 88,061, total_orders: 2, total_revenue: 695.03
1856. seller_zip_code_prefix: 91,901, total_orders: 2, total_revenue: 123.87
1857. seller_zip_code_prefix: 2,614, total_orders: 2, total_revenue: 206.82
1858. seller_zip_code_prefix: 30,170, total_orders: 2, total_revenue: 481.00
1859. seller_zip_code_prefix: 3,124, total_orders: 2, total_revenue: 84.68
1860. seller_zip_code_prefix: 17,604, total_orders: 2, total_revenue: 53.83
1861. seller_zip_code_prefix: 6,322, total_orders: 2, total_revenue: 150.67
1862. seller_zip_code_prefix: 13,082, total_orders: 2, total_revenue: 163.20
1863. seller_zip_code_prefix: 13,486, total_orders: 2, total_revenue: 159.68
1864. seller_zip_code_prefix: 99,700, total_orders: 2, total_revenue: 521.67
1865. seller_zip_code_prefix: 90,850, total_orders: 2, total_revenue: 212.57
1866. seller_zip_code_prefix: 37,480, total_orders: 2, total_revenue: 225.61
1867. seller_zip_code_prefix: 90,560, total_orders: 2, total_revenue: 274.86
1868. seller_zip_code_prefix: 8,517, total_orders: 2, total_revenue: 149.22
1869. seller_zip_code_prefix: 87,111, total_orders: 2, total_revenue: 211.67
1870. seller_zip_code_prefix: 15,600, total_orders: 2, total_revenue: 223.20
1871. seller_zip_code_prefix: 9,170, total_orders: 2, total_revenue: 148.12
1872. seller_zip_code_prefix: 12,062, total_orders: 2, total_revenue: 213.13
1873. seller_zip_code_prefix: 79,104, total_orders: 2, total_revenue: 248.42
1874. seller_zip_code_prefix: 89,803, total_orders: 2, total_revenue: 329.68
1875. seller_zip_code_prefix: 13,042, total_orders: 2, total_revenue: 834.94
1876. seller_zip_code_prefix: 90,250, total_orders: 2, total_revenue: 182.39
1877. seller_zip_code_prefix: 81,830, total_orders: 2, total_revenue: 52.27
1878. seller_zip_code_prefix: 3,308, total_orders: 2, total_revenue: 53.48
1879. seller_zip_code_prefix: 89,258, total_orders: 2, total_revenue: 105.64
1880. seller_zip_code_prefix: 30,240, total_orders: 2, total_revenue: 1070.39
1881. seller_zip_code_prefix: 4,256, total_orders: 2, total_revenue: 155.25
1882. seller_zip_code_prefix: 4,311, total_orders: 2, total_revenue: 103.49
1883. seller_zip_code_prefix: 31,520, total_orders: 2, total_revenue: 63.92
1884. seller_zip_code_prefix: 4,137, total_orders: 2, total_revenue: 152.04
1885. seller_zip_code_prefix: 13,086, total_orders: 2, total_revenue: 77.64
1886. seller_zip_code_prefix: 4,216, total_orders: 2, total_revenue: 74.86
1887. seller_zip_code_prefix: 13,870, total_orders: 2, total_revenue: 355.39
1888. seller_zip_code_prefix: 3,526, total_orders: 2, total_revenue: 38.48
1889. seller_zip_code_prefix: 3,225, total_orders: 2, total_revenue: 99.67
1890. seller_zip_code_prefix: 9,895, total_orders: 2, total_revenue: 329.92
1891. seller_zip_code_prefix: 89,203, total_orders: 2, total_revenue: 97.62
1892. seller_zip_code_prefix: 72,318, total_orders: 2, total_revenue: 382.47
1893. seller_zip_code_prefix: 4,716, total_orders: 2, total_revenue: 198.82
1894. seller_zip_code_prefix: 4,508, total_orders: 2, total_revenue: 231.34
1895. seller_zip_code_prefix: 83,507, total_orders: 2, total_revenue: 68.20
1896. seller_zip_code_prefix: 35,044, total_orders: 2, total_revenue: 228.26
1897. seller_zip_code_prefix: 13,911, total_orders: 2, total_revenue: 292.39
1898. seller_zip_code_prefix: 9,785, total_orders: 2, total_revenue: 115.11
1899. seller_zip_code_prefix: 2,851, total_orders: 2, total_revenue: 78.04
1900. seller_zip_code_prefix: 74,043, total_orders: 2, total_revenue: 183.63
1901. seller_zip_code_prefix: 81,280, total_orders: 2, total_revenue: 229.25
1902. seller_zip_code_prefix: 88,340, total_orders: 2, total_revenue: 254.98
1903. seller_zip_code_prefix: 7,082, total_orders: 2, total_revenue: 430.08
1904. seller_zip_code_prefix: 36,320, total_orders: 2, total_revenue: 385.42
1905. seller_zip_code_prefix: 12,231, total_orders: 2, total_revenue: 557.85
1906. seller_zip_code_prefix: 88,102, total_orders: 2, total_revenue: 162.13
1907. seller_zip_code_prefix: 98,920, total_orders: 2, total_revenue: 785.75
1908. seller_zip_code_prefix: 24,855, total_orders: 2, total_revenue: 261.05
1909. seller_zip_code_prefix: 22,783, total_orders: 2, total_revenue: 93.23
1910. seller_zip_code_prefix: 7,412, total_orders: 2, total_revenue: 171.39
1911. seller_zip_code_prefix: 18,047, total_orders: 2, total_revenue: 101.99
1912. seller_zip_code_prefix: 15,813, total_orders: 2, total_revenue: 862.37
1913. seller_zip_code_prefix: 4,447, total_orders: 2, total_revenue: 79.73
1914. seller_zip_code_prefix: 9,820, total_orders: 2, total_revenue: 670.98
1915. seller_zip_code_prefix: 89,540, total_orders: 2, total_revenue: 638.58
1916. seller_zip_code_prefix: 24,725, total_orders: 2, total_revenue: 165.63
1917. seller_zip_code_prefix: 1,417, total_orders: 2, total_revenue: 111.83
1918. seller_zip_code_prefix: 5,763, total_orders: 2, total_revenue: 353.26
1919. seller_zip_code_prefix: 37,048, total_orders: 2, total_revenue: 686.24
1920. seller_zip_code_prefix: 90,640, total_orders: 2, total_revenue: 282.14
1921. seller_zip_code_prefix: 3,065, total_orders: 2, total_revenue: 177.42
1922. seller_zip_code_prefix: 85,906, total_orders: 2, total_revenue: 571.22
1923. seller_zip_code_prefix: 85,810, total_orders: 2, total_revenue: 726.15
1924. seller_zip_code_prefix: 14,027, total_orders: 2, total_revenue: 181.94
1925. seller_zip_code_prefix: 85,865, total_orders: 2, total_revenue: 734.75
1926. seller_zip_code_prefix: 9,981, total_orders: 2, total_revenue: 94.04
1927. seller_zip_code_prefix: 93,040, total_orders: 2, total_revenue: 606.45
1928. seller_zip_code_prefix: 7,791, total_orders: 2, total_revenue: 329.11
1929. seller_zip_code_prefix: 38,445, total_orders: 2, total_revenue: 656.16
1930. seller_zip_code_prefix: 13,212, total_orders: 2, total_revenue: 486.98
1931. seller_zip_code_prefix: 1,041, total_orders: 2, total_revenue: 937.71
1932. seller_zip_code_prefix: 2,220, total_orders: 2, total_revenue: 148.92
1933. seller_zip_code_prefix: 2,035, total_orders: 2, total_revenue: 4874.32
1934. seller_zip_code_prefix: 37,004, total_orders: 2, total_revenue: 393.61
1935. seller_zip_code_prefix: 2,755, total_orders: 2, total_revenue: 94.76
1936. seller_zip_code_prefix: 63,540, total_orders: 2, total_revenue: 757.75
1937. seller_zip_code_prefix: 15,810, total_orders: 2, total_revenue: 831.01
1938. seller_zip_code_prefix: 74,343, total_orders: 2, total_revenue: 188.47
1939. seller_zip_code_prefix: 8,810, total_orders: 2, total_revenue: 212.57
1940. seller_zip_code_prefix: 6,753, total_orders: 2, total_revenue: 76.78
1941. seller_zip_code_prefix: 9,561, total_orders: 1, total_revenue: 121.62
1942. seller_zip_code_prefix: 26,210, total_orders: 1, total_revenue: 250.88
1943. seller_zip_code_prefix: 4,911, total_orders: 1, total_revenue: 195.81
1944. seller_zip_code_prefix: 84,600, total_orders: 1, total_revenue: 77.38
1945. seller_zip_code_prefix: 5,715, total_orders: 1, total_revenue: 55.72
1946. seller_zip_code_prefix: 87,210, total_orders: 1, total_revenue: 71.45
1947. seller_zip_code_prefix: 2,610, total_orders: 1, total_revenue: 15.22
1948. seller_zip_code_prefix: 89,063, total_orders: 1, total_revenue: 158.97
1949. seller_zip_code_prefix: 4,154, total_orders: 1, total_revenue: 204.06
1950. seller_zip_code_prefix: 16,208, total_orders: 1, total_revenue: 98.56
1951. seller_zip_code_prefix: 3,171, total_orders: 1, total_revenue: 1370.41
1952. seller_zip_code_prefix: 1,238, total_orders: 1, total_revenue: 313.43
1953. seller_zip_code_prefix: 13,185, total_orders: 1, total_revenue: 318.30
1954. seller_zip_code_prefix: 15,802, total_orders: 1, total_revenue: 39.09
1955. seller_zip_code_prefix: 7,122, total_orders: 1, total_revenue: 61.74
1956. seller_zip_code_prefix: 17,600, total_orders: 1, total_revenue: 78.12
1957. seller_zip_code_prefix: 86,990, total_orders: 1, total_revenue: 113.87
1958. seller_zip_code_prefix: 4,054, total_orders: 1, total_revenue: 107.90
1959. seller_zip_code_prefix: 88,107, total_orders: 1, total_revenue: 147.35
1960. seller_zip_code_prefix: 18,035, total_orders: 1, total_revenue: 135.49
1961. seller_zip_code_prefix: 87,360, total_orders: 1, total_revenue: 54.98
1962. seller_zip_code_prefix: 39,801, total_orders: 1, total_revenue: 359.91
1963. seller_zip_code_prefix: 6,290, total_orders: 1, total_revenue: 234.61
1964. seller_zip_code_prefix: 85,884, total_orders: 1, total_revenue: 77.66
1965. seller_zip_code_prefix: 1,042, total_orders: 1, total_revenue: 87.82
1966. seller_zip_code_prefix: 6,714, total_orders: 1, total_revenue: 214.56
1967. seller_zip_code_prefix: 5,595, total_orders: 1, total_revenue: 34.01
1968. seller_zip_code_prefix: 97,050, total_orders: 1, total_revenue: 68.35
1969. seller_zip_code_prefix: 30,668, total_orders: 1, total_revenue: 113.69
1970. seller_zip_code_prefix: 28,633, total_orders: 1, total_revenue: 625.33
1971. seller_zip_code_prefix: 63,020, total_orders: 1, total_revenue: 62.11
1972. seller_zip_code_prefix: 36,200, total_orders: 1, total_revenue: 93.54
1973. seller_zip_code_prefix: 55,004, total_orders: 1, total_revenue: 63.08
1974. seller_zip_code_prefix: 1,125, total_orders: 1, total_revenue: 204.81
1975. seller_zip_code_prefix: 13,408, total_orders: 1, total_revenue: 37.16
1976. seller_zip_code_prefix: 74,223, total_orders: 1, total_revenue: 64.11
1977. seller_zip_code_prefix: 13,848, total_orders: 1, total_revenue: 217.00
1978. seller_zip_code_prefix: 20,091, total_orders: 1, total_revenue: 108.86
1979. seller_zip_code_prefix: 32,140, total_orders: 1, total_revenue: 132.06
1980. seller_zip_code_prefix: 74,565, total_orders: 1, total_revenue: 139.38
1981. seller_zip_code_prefix: 5,302, total_orders: 1, total_revenue: 30.32
1982. seller_zip_code_prefix: 73,801, total_orders: 1, total_revenue: 107.30
1983. seller_zip_code_prefix: 37,400, total_orders: 1, total_revenue: 106.39
1984. seller_zip_code_prefix: 89,819, total_orders: 1, total_revenue: 76.50
1985. seller_zip_code_prefix: 93,510, total_orders: 1, total_revenue: 36.56
1986. seller_zip_code_prefix: 15,845, total_orders: 1, total_revenue: 182.59
1987. seller_zip_code_prefix: 32,672, total_orders: 1, total_revenue: 114.57
1988. seller_zip_code_prefix: 2,372, total_orders: 1, total_revenue: 179.92
1989. seller_zip_code_prefix: 4,781, total_orders: 1, total_revenue: 30.13
1990. seller_zip_code_prefix: 2,925, total_orders: 1, total_revenue: 135.49
1991. seller_zip_code_prefix: 14,750, total_orders: 1, total_revenue: 93.53
1992. seller_zip_code_prefix: 13,790, total_orders: 1, total_revenue: 76.64
1993. seller_zip_code_prefix: 8,780, total_orders: 1, total_revenue: 53.72
1994. seller_zip_code_prefix: 3,236, total_orders: 1, total_revenue: 56.60
1995. seller_zip_code_prefix: 97,502, total_orders: 1, total_revenue: 45.09
1996. seller_zip_code_prefix: 26,230, total_orders: 1, total_revenue: 262.10
1997. seller_zip_code_prefix: 95,660, total_orders: 1, total_revenue: 174.68
1998. seller_zip_code_prefix: 60,346, total_orders: 1, total_revenue: 86.43
1999. seller_zip_code_prefix: 1,425, total_orders: 1, total_revenue: 35.13
2000. seller_zip_code_prefix: 13,390, total_orders: 1, total_revenue: 249.39
```

#### 📊 Metadata

- **sql:** SELECT s.seller_zip_code_prefix, COUNT(o.order_id) AS total_orders, SUM(oi.price + oi.freight_value) AS total_revenue FROM analytics.sellers s JOIN analytics.order_items oi ON s.seller_id = oi.seller_id JOIN analytics.orders o ON oi.order_id = o.order_id GROUP BY s.seller_zip_code_prefix ORDER BY total_orders DESC
- **row_count:** 2000
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-13"></a>
### Query 13

#### 📝 Input

- **Query:** Quais categorias de produtos têm maior crescimento de vendas trimestre a trimestre?

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.85
- **Reason:** time series growth analysis by product category
- **Thread ID:** `18557b5b-3880-48be-bae7-9547c5727dbd`

#### 💬 Response

```
Análise do crescimento de vendas por categoria de produtos trimestre a trimestre:

**Trimestre 3 de 2016:**
  - Beleza e Saúde: 3 vendas
  - Móveis e Decoração: 2 vendas
  - Telefonia: 1 venda

**Trimestre 4 de 2016:**
  - Móveis e Decoração: 67 vendas
  - Beleza e Saúde: 48 vendas
  - Perfumaria: 33 vendas
  - Brinquedos: 27 vendas
  - Informática e Acessórios: 21 vendas
  - Esporte e Lazer: 19 vendas
  - Bebês: 14 vendas
  - Marketplace: 13 vendas
  - Utilidades Domésticas: 12 vendas
  - Automotivo: 12 vendas
  - Moda (Bolsas e Acessórios): 10 vendas
  - Climatização: 10 vendas
  - Telefonia: 10 vendas
  - Consoles e Games: 10 vendas
  - Cama, Mesa e Banho: 8 vendas
  - Cool Stuff: 8 vendas
  - Móveis de Escritório: 6 vendas
  - Telefonia Fixa: 5 vendas
  - Ferramentas de Jardim: 5 vendas
  - Relógios e Presentes: 5 vendas
  - Pet Shop: 4 vendas
  - Indústria, Comércio e Negócios: 4 vendas
  - Eletrônicos: 2 vendas
  - Áudio: 2 vendas
  - Livros (Interesse Geral): 1 venda
  - Moda (Calçados): 1 venda
  - Livros (Técnicos): 1 venda
  - Moda (Roupa Masculina): 1 venda
  - Moda (Roupa Feminina): 1 venda
  - Fraldas e Higiene: 1 venda
  - Alimentos: 1 venda

**Trimestre 1 de 2017:**
  - Móveis e Decoração: 776 vendas
  - Cama, Mesa e Banho: 502 vendas
  - Beleza e Saúde: 462 vendas
  - Esporte e Lazer: 435 vendas
  - Utilidades Domésticas: 313 vendas
  - Informática e Acessórios: 311 vendas
  - Telefonia: 309 vendas
  - Ferramentas de Jardim: 280 vendas
  - Cool Stuff: 233 vendas
  - Brinquedos: 213 vendas
  - Automotivo: 207 vendas
  - Perfumaria: 191 vendas
  - Móveis de Escritório: 151 vendas
  - Moda (Bolsas e Acessórios): 142 vendas

Total de registros analisados: 509. O crescimento mais significativo foi observado na categoria Móveis e Decoração, que saltou de 2 vendas no terceiro trimestre de 2016 para 776 vendas no primeiro trimestre de 2017.

Dados por categoria:
beleza_saude: quarter: 2016-07-01 00:00:00, sales_count: 3
moveis_decoracao: quarter: 2016-07-01 00:00:00, sales_count: 2
telefonia: quarter: 2016-07-01 00:00:00, sales_count: 1
moveis_decoracao: quarter: 2016-10-01 00:00:00, sales_count: 67
beleza_saude: quarter: 2016-10-01 00:00:00, sales_count: 48
perfumaria: quarter: 2016-10-01 00:00:00, sales_count: 33
brinquedos: quarter: 2016-10-01 00:00:00, sales_count: 27
informatica_acessorios: quarter: 2016-10-01 00:00:00, sales_count: 21
esporte_lazer: quarter: 2016-10-01 00:00:00, sales_count: 19
bebes: quarter: 2016-10-01 00:00:00, sales_count: 14
market_place: quarter: 2016-10-01 00:00:00, sales_count: 13
utilidades_domesticas: quarter: 2016-10-01 00:00:00, sales_count: 12
automotivo: quarter: 2016-10-01 00:00:00, sales_count: 12
fashion_bolsas_e_acessorios: quarter: 2016-10-01 00:00:00, sales_count: 10
climatizacao: quarter: 2016-10-01 00:00:00, sales_count: 10
telefonia: quarter: 2016-10-01 00:00:00, sales_count: 10
consoles_games: quarter: 2016-10-01 00:00:00, sales_count: 10
cama_mesa_banho: quarter: 2016-10-01 00:00:00, sales_count: 8
cool_stuff: quarter: 2016-10-01 00:00:00, sales_count: 8
moveis_escritorio: quarter: 2016-10-01 00:00:00, sales_count: 6
telefonia_fixa: quarter: 2016-10-01 00:00:00, sales_count: 5
ferramentas_jardim: quarter: 2016-10-01 00:00:00, sales_count: 5
relogios_presentes: quarter: 2016-10-01 00:00:00, sales_count: 5
pet_shop: quarter: 2016-10-01 00:00:00, sales_count: 4
industria_comercio_e_negocios: quarter: 2016-10-01 00:00:00, sales_count: 4
eletronicos: quarter: 2016-10-01 00:00:00, sales_count: 2
audio: quarter: 2016-10-01 00:00:00, sales_count: 2
livros_interesse_geral: quarter: 2016-10-01 00:00:00, sales_count: 1
fashion_calcados: quarter: 2016-10-01 00:00:00, sales_count: 1
livros_tecnicos: quarter: 2016-10-01 00:00:00, sales_count: 1
fashion_roupa_masculina: quarter: 2016-10-01 00:00:00, sales_count: 1
fashion_roupa_feminina: quarter: 2016-10-01 00:00:00, sales_count: 1
fraldas_higiene: quarter: 2016-10-01 00:00:00, sales_count: 1
alimentos: quarter: 2016-10-01 00:00:00, sales_count: 1
moveis_decoracao: quarter: 2017-01-01 00:00:00, sales_count: 776
cama_mesa_banho: quarter: 2017-01-01 00:00:00, sales_count: 502
beleza_saude: quarter: 2017-01-01 00:00:00, sales_count: 462
esporte_lazer: quarter: 2017-01-01 00:00:00, sales_count: 435
utilidades_domesticas: quarter: 2017-01-01 00:00:00, sales_count: 313
informatica_acessorios: quarter: 2017-01-01 00:00:00, sales_count: 311
telefonia: quarter: 2017-01-01 00:00:00, sales_count: 309
ferramentas_jardim: quarter: 2017-01-01 00:00:00, sales_count: 280
cool_stuff: quarter: 2017-01-01 00:00:00, sales_count: 233
brinquedos: quarter: 2017-01-01 00:00:00, sales_count: 213
automotivo: quarter: 2017-01-01 00:00:00, sales_count: 207
perfumaria: quarter: 2017-01-01 00:00:00, sales_count: 191
moveis_escritorio: quarter: 2017-01-01 00:00:00, sales_count: 151
fashion_bolsas_e_acessorios: quarter: 2017-01-01 00:00:00, sales_count: 142
relogios_presentes: quarter: 2017-01-01 00:00:00, sales_count: 129
bebes: quarter: 2017-01-01 00:00:00, sales_count: 119
pet_shop: quarter: 2017-01-01 00:00:00, sales_count: 100
consoles_games: quarter: 2017-01-01 00:00:00, sales_count: 91
papelaria: quarter: 2017-01-01 00:00:00, sales_count: 89
eletronicos: quarter: 2017-01-01 00:00:00, sales_count: 67
telefonia_fixa: quarter: 2017-01-01 00:00:00, sales_count: 65
eletroportateis: quarter: 2017-01-01 00:00:00, sales_count: 65
malas_acessorios: quarter: 2017-01-01 00:00:00, sales_count: 64
moveis_sala: quarter: 2017-01-01 00:00:00, sales_count: 58
market_place: quarter: 2017-01-01 00:00:00, sales_count: 45
alimentos: quarter: 2017-01-01 00:00:00, sales_count: 35
livros_interesse_geral: quarter: 2017-01-01 00:00:00, sales_count: 35
climatizacao: quarter: 2017-01-01 00:00:00, sales_count: 33
instrumentos_musicais: quarter: 2017-01-01 00:00:00, sales_count: 20
audio: quarter: 2017-01-01 00:00:00, sales_count: 19
fashion_calcados: quarter: 2017-01-01 00:00:00, sales_count: 18
fashion_roupa_masculina: quarter: 2017-01-01 00:00:00, sales_count: 17
eletrodomesticos: quarter: 2017-01-01 00:00:00, sales_count: 17
casa_conforto: quarter: 2017-01-01 00:00:00, sales_count: 16
fashion_underwear_e_moda_praia: quarter: 2017-01-01 00:00:00, sales_count: 16
casa_construcao: quarter: 2017-01-01 00:00:00, sales_count: 14
tablets_impressao_imagem: quarter: 2017-01-01 00:00:00, sales_count: 13
agro_industria_e_comercio: quarter: 2017-01-01 00:00:00, sales_count: 12
eletrodomesticos_2: quarter: 2017-01-01 00:00:00, sales_count: 11
moveis_quarto: quarter: 2017-01-01 00:00:00, sales_count: 9
dvds_blu_ray: quarter: 2017-01-01 00:00:00, sales_count: 8
construcao_ferramentas_construcao: quarter: 2017-01-01 00:00:00, sales_count: 8
fashion_roupa_feminina: quarter: 2017-01-01 00:00:00, sales_count: 7
moveis_cozinha_area_de_servico_jantar_e_jardim: quarter: 2017-01-01 00:00:00, sales_count: 6
bebidas: quarter: 2017-01-01 00:00:00, sales_count: 5
casa_conforto_2: quarter: 2017-01-01 00:00:00, sales_count: 5
artes: quarter: 2017-01-01 00:00:00, sales_count: 5
alimentos_bebidas: quarter: 2017-01-01 00:00:00, sales_count: 5
livros_tecnicos: quarter: 2017-01-01 00:00:00, sales_count: 3
industria_comercio_e_negocios: quarter: 2017-01-01 00:00:00, sales_count: 3
construcao_ferramentas_seguranca: quarter: 2017-01-01 00:00:00, sales_count: 3
musica: quarter: 2017-01-01 00:00:00, sales_count: 3
pcs: quarter: 2017-01-01 00:00:00, sales_count: 2
construcao_ferramentas_jardim: quarter: 2017-01-01 00:00:00, sales_count: 2
livros_importados: quarter: 2017-01-01 00:00:00, sales_count: 1
sinalizacao_e_seguranca: quarter: 2017-01-01 00:00:00, sales_count: 1
cine_foto: quarter: 2017-01-01 00:00:00, sales_count: 1
seguros_e_servicos: quarter: 2017-01-01 00:00:00, sales_count: 1
fashion_esporte: quarter: 2017-01-01 00:00:00, sales_count: 1
cama_mesa_banho: quarter: 2017-04-01 00:00:00, sales_count: 1,025
utilidades_domesticas: quarter: 2017-04-01 00:00:00, sales_count: 821
esporte_lazer: quarter: 2017-04-01 00:00:00, sales_count: 811
beleza_saude: quarter: 2017-04-01 00:00:00, sales_count: 739
informatica_acessorios: quarter: 2017-04-01 00:00:00, sales_count: 717
moveis_decoracao: quarter: 2017-04-01 00:00:00, sales_count: 715
cool_stuff: quarter: 2017-04-01 00:00:00, sales_count: 569
telefonia: quarter: 2017-04-01 00:00:00, sales_count: 529
brinquedos: quarter: 2017-04-01 00:00:00, sales_count: 471
perfumaria: quarter: 2017-04-01 00:00:00, sales_count: 404
ferramentas_jardim: quarter: 2017-04-01 00:00:00, sales_count: 374
relogios_presentes: quarter: 2017-04-01 00:00:00, sales_count: 356
automotivo: quarter: 2017-04-01 00:00:00, sales_count: 325
fashion_bolsas_e_acessorios: quarter: 2017-04-01 00:00:00, sales_count: 243
bebes: quarter: 2017-04-01 00:00:00, sales_count: 237
pet_shop: quarter: 2017-04-01 00:00:00, sales_count: 188
malas_acessorios: quarter: 2017-04-01 00:00:00, sales_count: 180
moveis_escritorio: quarter: 2017-04-01 00:00:00, sales_count: 164
eletronicos: quarter: 2017-04-01 00:00:00, sales_count: 158
papelaria: quarter: 2017-04-01 00:00:00, sales_count: 140
eletrodomesticos: quarter: 2017-04-01 00:00:00, sales_count: 81
consoles_games: quarter: 2017-04-01 00:00:00, sales_count: 76
casa_conforto: quarter: 2017-04-01 00:00:00, sales_count: 72
fashion_calcados: quarter: 2017-04-01 00:00:00, sales_count: 65
eletroportateis: quarter: 2017-04-01 00:00:00, sales_count: 62
moveis_sala: quarter: 2017-04-01 00:00:00, sales_count: 61
market_place: quarter: 2017-04-01 00:00:00, sales_count: 58
instrumentos_musicais: quarter: 2017-04-01 00:00:00, sales_count: 57
livros_interesse_geral: quarter: 2017-04-01 00:00:00, sales_count: 53
audio: quarter: 2017-04-01 00:00:00, sales_count: 39
climatizacao: quarter: 2017-04-01 00:00:00, sales_count: 35
telefonia_fixa: quarter: 2017-04-01 00:00:00, sales_count: 33
tablets_impressao_imagem: quarter: 2017-04-01 00:00:00, sales_count: 24
moveis_cozinha_area_de_servico_jantar_e_jardim: quarter: 2017-04-01 00:00:00, sales_count: 22
alimentos_bebidas: quarter: 2017-04-01 00:00:00, sales_count: 22
fashion_roupa_masculina: quarter: 2017-04-01 00:00:00, sales_count: 21
construcao_ferramentas_jardim: quarter: 2017-04-01 00:00:00, sales_count: 20
casa_construcao: quarter: 2017-04-01 00:00:00, sales_count: 20
artes: quarter: 2017-04-01 00:00:00, sales_count: 19
eletrodomesticos_2: quarter: 2017-04-01 00:00:00, sales_count: 17
moveis_quarto: quarter: 2017-04-01 00:00:00, sales_count: 16
fashion_esporte: quarter: 2017-04-01 00:00:00, sales_count: 13
alimentos: quarter: 2017-04-01 00:00:00, sales_count: 12
fashion_underwear_e_moda_praia: quarter: 2017-04-01 00:00:00, sales_count: 12
dvds_blu_ray: quarter: 2017-04-01 00:00:00, sales_count: 10
fashion_roupa_feminina: quarter: 2017-04-01 00:00:00, sales_count: 9
construcao_ferramentas_construcao: quarter: 2017-04-01 00:00:00, sales_count: 9
bebidas: quarter: 2017-04-01 00:00:00, sales_count: 9
sinalizacao_e_seguranca: quarter: 2017-04-01 00:00:00, sales_count: 9
livros_tecnicos: quarter: 2017-04-01 00:00:00, sales_count: 6
musica: quarter: 2017-04-01 00:00:00, sales_count: 6
agro_industria_e_comercio: quarter: 2017-04-01 00:00:00, sales_count: 5
pc_gamer: quarter: 2017-04-01 00:00:00, sales_count: 4
moveis_colchao_e_estofado: quarter: 2017-04-01 00:00:00, sales_count: 4
cine_foto: quarter: 2017-04-01 00:00:00, sales_count: 4
industria_comercio_e_negocios: quarter: 2017-04-01 00:00:00, sales_count: 4
artigos_de_natal: quarter: 2017-04-01 00:00:00, sales_count: 4
construcao_ferramentas_ferramentas: quarter: 2017-04-01 00:00:00, sales_count: 3
livros_importados: quarter: 2017-04-01 00:00:00, sales_count: 3
fashion_roupa_infanto_juvenil: quarter: 2017-04-01 00:00:00, sales_count: 2
la_cuisine: quarter: 2017-04-01 00:00:00, sales_count: 2
casa_conforto_2: quarter: 2017-04-01 00:00:00, sales_count: 2
artes_e_artesanato: quarter: 2017-04-01 00:00:00, sales_count: 1
portateis_casa_forno_e_cafe: quarter: 2017-04-01 00:00:00, sales_count: 1
cama_mesa_banho: quarter: 2017-07-01 00:00:00, sales_count: 1,624
esporte_lazer: quarter: 2017-07-01 00:00:00, sales_count: 1,273
moveis_decoracao: quarter: 2017-07-01 00:00:00, sales_count: 1,104
beleza_saude: quarter: 2017-07-01 00:00:00, sales_count: 1,056
informatica_acessorios: quarter: 2017-07-01 00:00:00, sales_count: 929
utilidades_domesticas: quarter: 2017-07-01 00:00:00, sales_count: 819
cool_stuff: quarter: 2017-07-01 00:00:00, sales_count: 701
brinquedos: quarter: 2017-07-01 00:00:00, sales_count: 688
ferramentas_jardim: quarter: 2017-07-01 00:00:00, sales_count: 653
relogios_presentes: quarter: 2017-07-01 00:00:00, sales_count: 648
telefonia: quarter: 2017-07-01 00:00:00, sales_count: 457
bebes: quarter: 2017-07-01 00:00:00, sales_count: 435
perfumaria: quarter: 2017-07-01 00:00:00, sales_count: 414
automotivo: quarter: 2017-07-01 00:00:00, sales_count: 391
fashion_bolsas_e_acessorios: quarter: 2017-07-01 00:00:00, sales_count: 311
pet_shop: quarter: 2017-07-01 00:00:00, sales_count: 247
papelaria: quarter: 2017-07-01 00:00:00, sales_count: 237
moveis_escritorio: quarter: 2017-07-01 00:00:00, sales_count: 234
eletronicos: quarter: 2017-07-01 00:00:00, sales_count: 220
consoles_games: quarter: 2017-07-01 00:00:00, sales_count: 204
malas_acessorios: quarter: 2017-07-01 00:00:00, sales_count: 179
casa_conforto: quarter: 2017-07-01 00:00:00, sales_count: 104
eletroportateis: quarter: 2017-07-01 00:00:00, sales_count: 103
eletrodomesticos: quarter: 2017-07-01 00:00:00, sales_count: 96
instrumentos_musicais: quarter: 2017-07-01 00:00:00, sales_count: 87
pcs: quarter: 2017-07-01 00:00:00, sales_count: 70
moveis_sala: quarter: 2017-07-01 00:00:00, sales_count: 65
livros_interesse_geral: quarter: 2017-07-01 00:00:00, sales_count: 57
fashion_calcados: quarter: 2017-07-01 00:00:00, sales_count: 56
market_place: quarter: 2017-07-01 00:00:00, sales_count: 47
telefonia_fixa: quarter: 2017-07-01 00:00:00, sales_count: 42
fashion_roupa_masculina: quarter: 2017-07-01 00:00:00, sales_count: 40
fashion_underwear_e_moda_praia: quarter: 2017-07-01 00:00:00, sales_count: 34
alimentos_bebidas: quarter: 2017-07-01 00:00:00, sales_count: 32
alimentos: quarter: 2017-07-01 00:00:00, sales_count: 32
eletrodomesticos_2: quarter: 2017-07-01 00:00:00, sales_count: 30
climatizacao: quarter: 2017-07-01 00:00:00, sales_count: 28
audio: quarter: 2017-07-01 00:00:00, sales_count: 24
construcao_ferramentas_jardim: quarter: 2017-07-01 00:00:00, sales_count: 24
construcao_ferramentas_construcao: quarter: 2017-07-01 00:00:00, sales_count: 24
moveis_cozinha_area_de_servico_jantar_e_jardim: quarter: 2017-07-01 00:00:00, sales_count: 23
sinalizacao_e_seguranca: quarter: 2017-07-01 00:00:00, sales_count: 19
livros_tecnicos: quarter: 2017-07-01 00:00:00, sales_count: 19
casa_construcao: quarter: 2017-07-01 00:00:00, sales_count: 14
bebidas: quarter: 2017-07-01 00:00:00, sales_count: 13
moveis_quarto: quarter: 2017-07-01 00:00:00, sales_count: 12
fashion_roupa_feminina: quarter: 2017-07-01 00:00:00, sales_count: 12
dvds_blu_ray: quarter: 2017-07-01 00:00:00, sales_count: 12
tablets_impressao_imagem: quarter: 2017-07-01 00:00:00, sales_count: 11
artes: quarter: 2017-07-01 00:00:00, sales_count: 10
agro_industria_e_comercio: quarter: 2017-07-01 00:00:00, sales_count: 9
fashion_esporte: quarter: 2017-07-01 00:00:00, sales_count: 8
cds_dvds_musicais: quarter: 2017-07-01 00:00:00, sales_count: 8
artigos_de_natal: quarter: 2017-07-01 00:00:00, sales_count: 7
industria_comercio_e_negocios: quarter: 2017-07-01 00:00:00, sales_count: 7
la_cuisine: quarter: 2017-07-01 00:00:00, sales_count: 6
construcao_ferramentas_seguranca: quarter: 2017-07-01 00:00:00, sales_count: 6
casa_conforto_2: quarter: 2017-07-01 00:00:00, sales_count: 5
livros_importados: quarter: 2017-07-01 00:00:00, sales_count: 5
construcao_ferramentas_iluminacao: quarter: 2017-07-01 00:00:00, sales_count: 4
moveis_colchao_e_estofado: quarter: 2017-07-01 00:00:00, sales_count: 4
construcao_ferramentas_ferramentas: quarter: 2017-07-01 00:00:00, sales_count: 3
portateis_casa_forno_e_cafe: quarter: 2017-07-01 00:00:00, sales_count: 3
artigos_de_festas: quarter: 2017-07-01 00:00:00, sales_count: 3
fashion_roupa_infanto_juvenil: quarter: 2017-07-01 00:00:00, sales_count: 2
musica: quarter: 2017-07-01 00:00:00, sales_count: 1
cine_foto: quarter: 2017-07-01 00:00:00, sales_count: 1
artes_e_artesanato: quarter: 2017-07-01 00:00:00, sales_count: 1
seguros_e_servicos: quarter: 2017-07-01 00:00:00, sales_count: 1
cama_mesa_banho: quarter: 2017-10-01 00:00:00, sales_count: 2,072
esporte_lazer: quarter: 2017-10-01 00:00:00, sales_count: 1,576
moveis_decoracao: quarter: 2017-10-01 00:00:00, sales_count: 1,552
beleza_saude: quarter: 2017-10-01 00:00:00, sales_count: 1,411
brinquedos: quarter: 2017-10-01 00:00:00, sales_count: 1,230
ferramentas_jardim: quarter: 2017-10-01 00:00:00, sales_count: 1,156
relogios_presentes: quarter: 2017-10-01 00:00:00, sales_count: 1,150
informatica_acessorios: quarter: 2017-10-01 00:00:00, sales_count: 1,141
utilidades_domesticas: quarter: 2017-10-01 00:00:00, sales_count: 953
telefonia: quarter: 2017-10-01 00:00:00, sales_count: 903
cool_stuff: quarter: 2017-10-01 00:00:00, sales_count: 812
perfumaria: quarter: 2017-10-01 00:00:00, sales_count: 741
automotivo: quarter: 2017-10-01 00:00:00, sales_count: 681
papelaria: quarter: 2017-10-01 00:00:00, sales_count: 518
bebes: quarter: 2017-10-01 00:00:00, sales_count: 484
eletronicos: quarter: 2017-10-01 00:00:00, sales_count: 457
fashion_bolsas_e_acessorios: quarter: 2017-10-01 00:00:00, sales_count: 445
consoles_games: quarter: 2017-10-01 00:00:00, sales_count: 336
moveis_escritorio: quarter: 2017-10-01 00:00:00, sales_count: 253
pet_shop: quarter: 2017-10-01 00:00:00, sales_count: 249
malas_acessorios: quarter: 2017-10-01 00:00:00, sales_count: 175
instrumentos_musicais: quarter: 2017-10-01 00:00:00, sales_count: 118
casa_construcao: quarter: 2017-10-01 00:00:00, sales_count: 95
construcao_ferramentas_construcao: quarter: 2017-10-01 00:00:00, sales_count: 93
eletroportateis: quarter: 2017-10-01 00:00:00, sales_count: 92
livros_interesse_geral: quarter: 2017-10-01 00:00:00, sales_count: 91
casa_conforto: quarter: 2017-10-01 00:00:00, sales_count: 86
audio: quarter: 2017-10-01 00:00:00, sales_count: 85
moveis_sala: quarter: 2017-10-01 00:00:00, sales_count: 78
alimentos_bebidas: quarter: 2017-10-01 00:00:00, sales_count: 72
moveis_cozinha_area_de_servico_jantar_e_jardim: quarter: 2017-10-01 00:00:00, sales_count: 69
bebidas: quarter: 2017-10-01 00:00:00, sales_count: 65
pcs: quarter: 2017-10-01 00:00:00, sales_count: 57
artigos_de_natal: quarter: 2017-10-01 00:00:00, sales_count: 52
fashion_calcados: quarter: 2017-10-01 00:00:00, sales_count: 51
eletrodomesticos: quarter: 2017-10-01 00:00:00, sales_count: 49
alimentos: quarter: 2017-10-01 00:00:00, sales_count: 48
market_place: quarter: 2017-10-01 00:00:00, sales_count: 41
agro_industria_e_comercio: quarter: 2017-10-01 00:00:00, sales_count: 35
climatizacao: quarter: 2017-10-01 00:00:00, sales_count: 34
construcao_ferramentas_seguranca: quarter: 2017-10-01 00:00:00, sales_count: 34
construcao_ferramentas_jardim: quarter: 2017-10-01 00:00:00, sales_count: 32
eletrodomesticos_2: quarter: 2017-10-01 00:00:00, sales_count: 31
fashion_roupa_masculina: quarter: 2017-10-01 00:00:00, sales_count: 27
fashion_underwear_e_moda_praia: quarter: 2017-10-01 00:00:00, sales_count: 26
industria_comercio_e_negocios: quarter: 2017-10-01 00:00:00, sales_count: 21
sinalizacao_e_seguranca: quarter: 2017-10-01 00:00:00, sales_count: 17
telefonia_fixa: quarter: 2017-10-01 00:00:00, sales_count: 17
construcao_ferramentas_ferramentas: quarter: 2017-10-01 00:00:00, sales_count: 16
livros_tecnicos: quarter: 2017-10-01 00:00:00, sales_count: 16
construcao_ferramentas_iluminacao: quarter: 2017-10-01 00:00:00, sales_count: 14
tablets_impressao_imagem: quarter: 2017-10-01 00:00:00, sales_count: 13
moveis_colchao_e_estofado: quarter: 2017-10-01 00:00:00, sales_count: 10
dvds_blu_ray: quarter: 2017-10-01 00:00:00, sales_count: 9
artigos_de_festas: quarter: 2017-10-01 00:00:00, sales_count: 8
moveis_quarto: quarter: 2017-10-01 00:00:00, sales_count: 8
casa_conforto_2: quarter: 2017-10-01 00:00:00, sales_count: 8
flores: quarter: 2017-10-01 00:00:00, sales_count: 8
livros_importados: quarter: 2017-10-01 00:00:00, sales_count: 7
artes: quarter: 2017-10-01 00:00:00, sales_count: 7
cds_dvds_musicais: quarter: 2017-10-01 00:00:00, sales_count: 5
fashion_roupa_feminina: quarter: 2017-10-01 00:00:00, sales_count: 3
fashion_esporte: quarter: 2017-10-01 00:00:00, sales_count: 3
fraldas_higiene: quarter: 2017-10-01 00:00:00, sales_count: 2
la_cuisine: quarter: 2017-10-01 00:00:00, sales_count: 2
cine_foto: quarter: 2017-10-01 00:00:00, sales_count: 2
fashion_roupa_infanto_juvenil: quarter: 2017-10-01 00:00:00, sales_count: 1
musica: quarter: 2017-10-01 00:00:00, sales_count: 1
informatica_acessorios: quarter: 2018-01-01 00:00:00, sales_count: 2,446
cama_mesa_banho: quarter: 2018-01-01 00:00:00, sales_count: 2,336
esporte_lazer: quarter: 2018-01-01 00:00:00, sales_count: 2,066
beleza_saude: quarter: 2018-01-01 00:00:00, sales_count: 1,969
moveis_decoracao: quarter: 2018-01-01 00:00:00, sales_count: 1,641
utilidades_domesticas: quarter: 2018-01-01 00:00:00, sales_count: 1,166
relogios_presentes: quarter: 2018-01-01 00:00:00, sales_count: 1,137
telefonia: quarter: 2018-01-01 00:00:00, sales_count: 1,075
eletronicos: quarter: 2018-01-01 00:00:00, sales_count: 944
automotivo: quarter: 2018-01-01 00:00:00, sales_count: 931
ferramentas_jardim: quarter: 2018-01-01 00:00:00, sales_count: 798
cool_stuff: quarter: 2018-01-01 00:00:00, sales_count: 743
papelaria: quarter: 2018-01-01 00:00:00, sales_count: 720
perfumaria: quarter: 2018-01-01 00:00:00, sales_count: 646
bebes: quarter: 2018-01-01 00:00:00, sales_count: 623
brinquedos: quarter: 2018-01-01 00:00:00, sales_count: 545
moveis_escritorio: quarter: 2018-01-01 00:00:00, sales_count: 456
fashion_bolsas_e_acessorios: quarter: 2018-01-01 00:00:00, sales_count: 371
pet_shop: quarter: 2018-01-01 00:00:00, sales_count: 316
malas_acessorios: quarter: 2018-01-01 00:00:00, sales_count: 232
construcao_ferramentas_construcao: quarter: 2018-01-01 00:00:00, sales_count: 188
consoles_games: quarter: 2018-01-01 00:00:00, sales_count: 164
instrumentos_musicais: quarter: 2018-01-01 00:00:00, sales_count: 152
eletrodomesticos: quarter: 2018-01-01 00:00:00, sales_count: 147
casa_construcao: quarter: 2018-01-01 00:00:00, sales_count: 125
eletroportateis: quarter: 2018-01-01 00:00:00, sales_count: 124
livros_interesse_geral: quarter: 2018-01-01 00:00:00, sales_count: 113
bebidas: quarter: 2018-01-01 00:00:00, sales_count: 105
alimentos: quarter: 2018-01-01 00:00:00, sales_count: 94
industria_comercio_e_negocios: quarter: 2018-01-01 00:00:00, sales_count: 85
audio: quarter: 2018-01-01 00:00:00, sales_count: 75
agro_industria_e_comercio: quarter: 2018-01-01 00:00:00, sales_count: 73
construcao_ferramentas_jardim: quarter: 2018-01-01 00:00:00, sales_count: 67
moveis_sala: quarter: 2018-01-01 00:00:00, sales_count: 67
climatizacao: quarter: 2018-01-01 00:00:00, sales_count: 66
casa_conforto: quarter: 2018-01-01 00:00:00, sales_count: 60
livros_tecnicos: quarter: 2018-01-01 00:00:00, sales_count: 60
market_place: quarter: 2018-01-01 00:00:00, sales_count: 59
alimentos_bebidas: quarter: 2018-01-01 00:00:00, sales_count: 54
moveis_cozinha_area_de_servico_jantar_e_jardim: quarter: 2018-01-01 00:00:00, sales_count: 53
artigos_de_natal: quarter: 2018-01-01 00:00:00, sales_count: 46
eletrodomesticos_2: quarter: 2018-01-01 00:00:00, sales_count: 46
construcao_ferramentas_seguranca: quarter: 2018-01-01 00:00:00, sales_count: 41
artes: quarter: 2018-01-01 00:00:00, sales_count: 39
construcao_ferramentas_iluminacao: quarter: 2018-01-01 00:00:00, sales_count: 37
telefonia_fixa: quarter: 2018-01-01 00:00:00, sales_count: 36
sinalizacao_e_seguranca: quarter: 2018-01-01 00:00:00, sales_count: 32
fashion_calcados: quarter: 2018-01-01 00:00:00, sales_count: 32
construcao_ferramentas_ferramentas: quarter: 2018-01-01 00:00:00, sales_count: 29
fashion_underwear_e_moda_praia: quarter: 2018-01-01 00:00:00, sales_count: 20
moveis_colchao_e_estofado: quarter: 2018-01-01 00:00:00, sales_count: 19
moveis_quarto: quarter: 2018-01-01 00:00:00, sales_count: 19
tablets_impressao_imagem: quarter: 2018-01-01 00:00:00, sales_count: 19
flores: quarter: 2018-01-01 00:00:00, sales_count: 17
fraldas_higiene: quarter: 2018-01-01 00:00:00, sales_count: 15
portateis_casa_forno_e_cafe: quarter: 2018-01-01 00:00:00, sales_count: 13
livros_importados: quarter: 2018-01-01 00:00:00, sales_count: 12
pcs: quarter: 2018-01-01 00:00:00, sales_count: 12
cine_foto: quarter: 2018-01-01 00:00:00, sales_count: 11
fashion_roupa_masculina: quarter: 2018-01-01 00:00:00, sales_count: 9
fashion_roupa_feminina: quarter: 2018-01-01 00:00:00, sales_count: 8
artigos_de_festas: quarter: 2018-01-01 00:00:00, sales_count: 8
musica: quarter: 2018-01-01 00:00:00, sales_count: 5
dvds_blu_ray: quarter: 2018-01-01 00:00:00, sales_count: 5
casa_conforto_2: quarter: 2018-01-01 00:00:00, sales_count: 4
fashion_esporte: quarter: 2018-01-01 00:00:00, sales_count: 3
la_cuisine: quarter: 2018-01-01 00:00:00, sales_count: 2
fashion_roupa_infanto_juvenil: quarter: 2018-01-01 00:00:00, sales_count: 2
pc_gamer: quarter: 2018-01-01 00:00:00, sales_count: 1
beleza_saude: quarter: 2018-04-01 00:00:00, sales_count: 2,349
cama_mesa_banho: quarter: 2018-04-01 00:00:00, sales_count: 2,266
utilidades_domesticas: quarter: 2018-04-01 00:00:00, sales_count: 1,674
relogios_presentes: quarter: 2018-04-01 00:00:00, sales_count: 1,622
moveis_decoracao: quarter: 2018-04-01 00:00:00, sales_count: 1,604
esporte_lazer: quarter: 2018-04-01 00:00:00, sales_count: 1,518
informatica_acessorios: quarter: 2018-04-01 00:00:00, sales_count: 1,416
automotivo: quarter: 2018-04-01 00:00:00, sales_count: 967
ferramentas_jardim: quarter: 2018-04-01 00:00:00, sales_count: 764
telefonia: quarter: 2018-04-01 00:00:00, sales_count: 759
bebes: quarter: 2018-04-01 00:00:00, sales_count: 714
eletronicos: quarter: 2018-04-01 00:00:00, sales_count: 640
brinquedos: quarter: 2018-04-01 00:00:00, sales_count: 617
perfumaria: quarter: 2018-04-01 00:00:00, sales_count: 562
cool_stuff: quarter: 2018-04-01 00:00:00, sales_count: 486
pet_shop: quarter: 2018-04-01 00:00:00, sales_count: 484
papelaria: quarter: 2018-04-01 00:00:00, sales_count: 452
construcao_ferramentas_construcao: quarter: 2018-04-01 00:00:00, sales_count: 330
moveis_escritorio: quarter: 2018-04-01 00:00:00, sales_count: 315
fashion_bolsas_e_acessorios: quarter: 2018-04-01 00:00:00, sales_count: 305
eletrodomesticos: quarter: 2018-04-01 00:00:00, sales_count: 237
casa_construcao: quarter: 2018-04-01 00:00:00, sales_count: 226
instrumentos_musicais: quarter: 2018-04-01 00:00:00, sales_count: 168
eletroportateis: quarter: 2018-04-01 00:00:00, sales_count: 165
consoles_games: quarter: 2018-04-01 00:00:00, sales_count: 145
livros_interesse_geral: quarter: 2018-04-01 00:00:00, sales_count: 142
malas_acessorios: quarter: 2018-04-01 00:00:00, sales_count: 142
bebidas: quarter: 2018-04-01 00:00:00, sales_count: 135
construcao_ferramentas_iluminacao: quarter: 2018-04-01 00:00:00, sales_count: 132
industria_comercio_e_negocios: quarter: 2018-04-01 00:00:00, sales_count: 120
alimentos: quarter: 2018-04-01 00:00:00, sales_count: 108
livros_tecnicos: quarter: 2018-04-01 00:00:00, sales_count: 105
artes: quarter: 2018-04-01 00:00:00, sales_count: 90
moveis_sala: quarter: 2018-04-01 00:00:00, sales_count: 79
audio: quarter: 2018-04-01 00:00:00, sales_count: 72
sinalizacao_e_seguranca: quarter: 2018-04-01 00:00:00, sales_count: 70
construcao_ferramentas_seguranca: quarter: 2018-04-01 00:00:00, sales_count: 69
eletrodomesticos_2: quarter: 2018-04-01 00:00:00, sales_count: 65
moveis_cozinha_area_de_servico_jantar_e_jardim: quarter: 2018-04-01 00:00:00, sales_count: 63
casa_conforto: quarter: 2018-04-01 00:00:00, sales_count: 56
alimentos_bebidas: quarter: 2018-04-01 00:00:00, sales_count: 54
climatizacao: quarter: 2018-04-01 00:00:00, sales_count: 53
construcao_ferramentas_jardim: quarter: 2018-04-01 00:00:00, sales_count: 45
telefonia_fixa: quarter: 2018-04-01 00:00:00, sales_count: 45
pcs: quarter: 2018-04-01 00:00:00, sales_count: 42
market_place: quarter: 2018-04-01 00:00:00, sales_count: 36
cine_foto: quarter: 2018-04-01 00:00:00, sales_count: 36
fashion_calcados: quarter: 2018-04-01 00:00:00, sales_count: 31
agro_industria_e_comercio: quarter: 2018-04-01 00:00:00, sales_count: 30
portateis_casa_forno_e_cafe: quarter: 2018-04-01 00:00:00, sales_count: 27
construcao_ferramentas_ferramentas: quarter: 2018-04-01 00:00:00, sales_count: 26
artigos_de_natal: quarter: 2018-04-01 00:00:00, sales_count: 25
livros_importados: quarter: 2018-04-01 00:00:00, sales_count: 23
moveis_quarto: quarter: 2018-04-01 00:00:00, sales_count: 23
fashion_underwear_e_moda_praia: quarter: 2018-04-01 00:00:00, sales_count: 19
dvds_blu_ray: quarter: 2018-04-01 00:00:00, sales_count: 18
fraldas_higiene: quarter: 2018-04-01 00:00:00, sales_count: 14
musica: quarter: 2018-04-01 00:00:00, sales_count: 13
fashion_roupa_masculina: quarter: 2018-04-01 00:00:00, sales_count: 9
artigos_de_festas: quarter: 2018-04-01 00:00:00, sales_count: 8
flores: quarter: 2018-04-01 00:00:00, sales_count: 6
fashion_roupa_feminina: quarter: 2018-04-01 00:00:00, sales_count: 5
tablets_impressao_imagem: quarter: 2018-04-01 00:00:00, sales_count: 3
casa_conforto_2: quarter: 2018-04-01 00:00:00, sales_count: 3
artes_e_artesanato: quarter: 2018-04-01 00:00:00, sales_count: 2
portateis_cozinha_e_preparadores_de_alimentos: quarter: 2018-04-01 00:00:00, sales_count: 2
la_cuisine: quarter: 2018-04-01 00:00:00, sales_count: 2
cds_dvds_musicais: quarter: 2018-04-01 00:00:00, sales_count: 1
fashion_esporte: quarter: 2018-04-01 00:00:00, sales_count: 1
fashion_roupa_infanto_juvenil: quarter: 2018-04-01 00:00:00, sales_count: 1
beleza_saude: quarter: 2018-07-01 00:00:00, sales_count: 1,633
cama_mesa_banho: quarter: 2018-07-01 00:00:00, sales_count: 1,282
utilidades_domesticas: quarter: 2018-07-01 00:00:00, sales_count: 1,206
relogios_presentes: quarter: 2018-07-01 00:00:00, sales_count: 944
esporte_lazer: quarter: 2018-07-01 00:00:00, sales_count: 943
moveis_decoracao: quarter: 2018-07-01 00:00:00, sales_count: 873
informatica_acessorios: quarter: 2018-07-01 00:00:00, sales_count: 846
automotivo: quarter: 2018-07-01 00:00:00, sales_count: 721
telefonia: quarter: 2018-07-01 00:00:00, sales_count: 502
bebes: quarter: 2018-07-01 00:00:00, sales_count: 439
perfumaria: quarter: 2018-07-01 00:00:00, sales_count: 428
papelaria: quarter: 2018-07-01 00:00:00, sales_count: 361
pet_shop: quarter: 2018-07-01 00:00:00, sales_count: 359
brinquedos: quarter: 2018-07-01 00:00:00, sales_count: 326
ferramentas_jardim: quarter: 2018-07-01 00:00:00, sales_count: 317
eletronicos: quarter: 2018-07-01 00:00:00, sales_count: 279
construcao_ferramentas_construcao: quarter: 2018-07-01 00:00:00, sales_count: 277
cool_stuff: quarter: 2018-07-01 00:00:00, sales_count: 244
fashion_bolsas_e_acessorios: quarter: 2018-07-01 00:00:00, sales_count: 204
alimentos: quarter: 2018-07-01 00:00:00, sales_count: 180
eletrodomesticos: quarter: 2018-07-01 00:00:00, sales_count: 144
malas_acessorios: quarter: 2018-07-01 00:00:00, sales_count: 120
construcao_ferramentas_iluminacao: quarter: 2018-07-01 00:00:00, sales_count: 117
moveis_escritorio: quarter: 2018-07-01 00:00:00, sales_count: 112
consoles_games: quarter: 2018-07-01 00:00:00, sales_count: 111
casa_construcao: quarter: 2018-07-01 00:00:00, sales_count: 110
moveis_sala: quarter: 2018-07-01 00:00:00, sales_count: 95
instrumentos_musicais: quarter: 2018-07-01 00:00:00, sales_count: 78
eletroportateis: quarter: 2018-07-01 00:00:00, sales_count: 68
livros_interesse_geral: quarter: 2018-07-01 00:00:00, sales_count: 61
livros_tecnicos: quarter: 2018-07-01 00:00:00, sales_count: 57
sinalizacao_e_seguranca: quarter: 2018-07-01 00:00:00, sales_count: 51
construcao_ferramentas_jardim: quarter: 2018-07-01 00:00:00, sales_count: 48
agro_industria_e_comercio: quarter: 2018-07-01 00:00:00, sales_count: 48
audio: quarter: 2018-07-01 00:00:00, sales_count: 48
bebidas: quarter: 2018-07-01 00:00:00, sales_count: 47
moveis_cozinha_area_de_servico_jantar_e_jardim: quarter: 2018-07-01 00:00:00, sales_count: 45
construcao_ferramentas_seguranca: quarter: 2018-07-01 00:00:00, sales_count: 41
casa_conforto: quarter: 2018-07-01 00:00:00, sales_count: 40
artes: quarter: 2018-07-01 00:00:00, sales_count: 39
alimentos_bebidas: quarter: 2018-07-01 00:00:00, sales_count: 39
eletrodomesticos_2: quarter: 2018-07-01 00:00:00, sales_count: 38
climatizacao: quarter: 2018-07-01 00:00:00, sales_count: 38
portateis_casa_forno_e_cafe: quarter: 2018-07-01 00:00:00, sales_count: 32
construcao_ferramentas_ferramentas: quarter: 2018-07-01 00:00:00, sales_count: 26
industria_comercio_e_negocios: quarter: 2018-07-01 00:00:00, sales_count: 24
moveis_quarto: quarter: 2018-07-01 00:00:00, sales_count: 22
telefonia_fixa: quarter: 2018-07-01 00:00:00, sales_count: 21
artes_e_artesanato: quarter: 2018-07-01 00:00:00, sales_count: 20
pcs: quarter: 2018-07-01 00:00:00, sales_count: 20
artigos_de_natal: quarter: 2018-07-01 00:00:00, sales_count: 19
cine_foto: quarter: 2018-07-01 00:00:00, sales_count: 17
artigos_de_festas: quarter: 2018-07-01 00:00:00, sales_count: 16
portateis_cozinha_e_preparadores_de_alimentos: quarter: 2018-07-01 00:00:00, sales_count: 13
market_place: quarter: 2018-07-01 00:00:00, sales_count: 12
musica: quarter: 2018-07-01 00:00:00, sales_count: 9
livros_importados: quarter: 2018-07-01 00:00:00, sales_count: 9
fashion_calcados: quarter: 2018-07-01 00:00:00, sales_count: 8
fashion_roupa_masculina: quarter: 2018-07-01 00:00:00, sales_count: 8
fraldas_higiene: quarter: 2018-07-01 00:00:00, sales_count: 7
fashion_underwear_e_moda_praia: quarter: 2018-07-01 00:00:00, sales_count: 4
pc_gamer: quarter: 2018-07-01 00:00:00, sales_count: 4
fashion_roupa_feminina: quarter: 2018-07-01 00:00:00, sales_count: 3
casa_conforto_2: quarter: 2018-07-01 00:00:00, sales_count: 3
flores: quarter: 2018-07-01 00:00:00, sales_count: 2
dvds_blu_ray: quarter: 2018-07-01 00:00:00, sales_count: 2
moveis_colchao_e_estofado: quarter: 2018-07-01 00:00:00, sales_count: 1
fashion_esporte: quarter: 2018-07-01 00:00:00, sales_count: 1
```

#### 📊 Metadata

- **sql:** SELECT p.product_category_name AS category, date_trunc('quarter', o.order_purchase_timestamp) AS quarter, COUNT(oi.order_id) AS sales_count FROM analytics.orders o JOIN analytics.order_items oi ON o.order_id = oi.order_id JOIN analytics.products p ON oi.product_id = p.product_id GROUP BY category, quarter ORDER BY quarter, sales_count DESC
- **row_count:** 509
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-14"></a>
### Query 14

#### 📝 Input

- **Query:** Identifique produtos com alta demanda mas baixa satisfação do cliente (score de review)

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.85
- **Reason:** identify products with high demand and low review scores
- **Thread ID:** `290152d9-083d-4281-b1cb-4d526c6998d2`

#### 💬 Response

```
Identificamos produtos com alta demanda, mas baixa satisfação do cliente (score de review abaixo de 3):

1. Produto ID: b5e13c9a353102f79c6206ff5cb61a50: 91 pedidos, média de avaliação 2,87
2. Produto ID: 362b773250263786dd58670d2df42c3b: 73 pedidos, média de avaliação 2,92
3. Produto ID: 89b121bee266dcd25688a1ba72eefb61: 68 pedidos, média de avaliação 2,40
4. Produto ID: b1d207586fca400a2370d50a9ba1da98: 48 pedidos, média de avaliação 1,92
5. Produto ID: 9ad75bd7267e5c724cb42c71ac56ca72: 44 pedidos, média de avaliação 2,98
6. Produto ID: 25c38557cf793876c5abdd5931f922db: 38 pedidos, média de avaliação 2,68
7. Produto ID: 1dec4c88c685d5a07bf01dcb0f8bf9f8: 35 pedidos, média de avaliação 2,74
8. Produto ID: 0cf41187284d7f099adc8415a743ebbd: 35 pedidos, média de avaliação 2,89
9. Produto ID: ee3d532c8a438679776d222e997606b3: 32 pedidos, média de avaliação 1,88
10. Produto ID: 51f876eb62be778c757503cf7f8a3b74: 32 pedidos, média de avaliação 2,94

Total de 68 produtos identificados com essas características.

Dados completos:
1. product_id: b5e13c9a353102f79c6206ff5cb61a50, demand: 91, avg_review_score: 2.8666666666666667
2. product_id: 362b773250263786dd58670d2df42c3b, demand: 73, avg_review_score: 2.9178082191780822
3. product_id: 89b121bee266dcd25688a1ba72eefb61, demand: 68, avg_review_score: 2.4029850746268657
4. product_id: b1d207586fca400a2370d50a9ba1da98, demand: 48, avg_review_score: 1.9166666666666667
5. product_id: 9ad75bd7267e5c724cb42c71ac56ca72, demand: 44, avg_review_score: 2.9767441860465116
6. product_id: 25c38557cf793876c5abdd5931f922db, demand: 38, avg_review_score: 2.6756756756756757
7. product_id: 1dec4c88c685d5a07bf01dcb0f8bf9f8, demand: 35, avg_review_score: 2.7352941176470588
8. product_id: 0cf41187284d7f099adc8415a743ebbd, demand: 35, avg_review_score: 2.8857142857142857
9. product_id: ee3d532c8a438679776d222e997606b3, demand: 32, avg_review_score: 1.8750000000000000
10. product_id: 51f876eb62be778c757503cf7f8a3b74, demand: 32, avg_review_score: 2.9375000000000000
11. product_id: cd46a885543f0e169a49f1eb25c04e43, demand: 30, avg_review_score: 1.8333333333333333
12. product_id: e8316a4667e5870c85e906b1f062bde1, demand: 30, avg_review_score: 2.7666666666666667
13. product_id: fb01a5fc09b9b9563c2ee41a22f07d54, demand: 24, avg_review_score: 2.9545454545454545
14. product_id: 7b35ccd93a2184646c03b70326626923, demand: 23, avg_review_score: 2.6818181818181818
15. product_id: 54d7ad85b648d3cb2b7069ed446d7f35, demand: 23, avg_review_score: 2.8260869565217391
16. product_id: 812f428f6757ab16c46cffc68f2e90c5, demand: 22, avg_review_score: 2.5454545454545455
17. product_id: ad4b5def91ac7c575dbdf65b5be311f4, demand: 22, avg_review_score: 1.5454545454545455
18. product_id: 0a9bdadab17a9b0f258f64d11a0adf7b, demand: 22, avg_review_score: 2.3636363636363636
19. product_id: ead3077a141a9c800d6a4bb9d0d415b6, demand: 21, avg_review_score: 2.8571428571428571
20. product_id: eebbed5ed3b134eceb717496c47652ba, demand: 21, avg_review_score: 2.9000000000000000
21. product_id: 43ee88561093499d9e571d4db5f20b79, demand: 20, avg_review_score: 2.5500000000000000
22. product_id: b4b817e5f2c4efc8253b4b679c653847, demand: 19, avg_review_score: 2.6666666666666667
23. product_id: 4c1bbc12438daec98a77243c2bf7a3ba, demand: 19, avg_review_score: 2.7894736842105263
24. product_id: 1bfe62f326ac7bec0f5a83c10cfff228, demand: 19, avg_review_score: 2.7647058823529412
25. product_id: a3daee3915d4fb98376e039ede6bdea6, demand: 18, avg_review_score: 2.3333333333333333
26. product_id: 3713f19c71c4be21ced80738e2fa49bc, demand: 18, avg_review_score: 2.2222222222222222
27. product_id: 00de7f393d962717eeeb2d7131a40dba, demand: 18, avg_review_score: 2.7777777777777778
28. product_id: 6d2fde7d12bb6ff367dbda120ba8828e, demand: 18, avg_review_score: 2.0555555555555556
29. product_id: b36f3c918c91478c4559160022d3f14e, demand: 17, avg_review_score: 1.8125000000000000
30. product_id: c230b471b7e21ff9060e68ee154afd70, demand: 17, avg_review_score: 1.1176470588235294
31. product_id: 547b95702aec86f05ac37e61d164891c, demand: 17, avg_review_score: 2.9411764705882353
32. product_id: 49eeae59754cbcf1abeeffb8f51184ee, demand: 17, avg_review_score: 2.8235294117647059
33. product_id: 44a5d24dd383324a421569ca697b13c2, demand: 16, avg_review_score: 1.4375000000000000
34. product_id: e6b314a2236c162ede1a879f1075430f, demand: 16, avg_review_score: 1.5625000000000000
35. product_id: 08c816d9a716567bf436173ef6f5f12e, demand: 16, avg_review_score: 2.8125000000000000
36. product_id: 226be9996759442f90f73b7d24c6baff, demand: 15, avg_review_score: 2.6000000000000000
37. product_id: b40ec43bdfc6d6fdd65e882066a5c895, demand: 15, avg_review_score: 2.9333333333333333
38. product_id: 97f1396a5a1f7c07ba51784efdec44b8, demand: 15, avg_review_score: 2.6000000000000000
39. product_id: dc68ee0fcb033a1ab6714fbb5db60c15, demand: 14, avg_review_score: 2.9285714285714286
40. product_id: 145028037adecb27b1a58cf9597676cc, demand: 14, avg_review_score: 2.4285714285714286
41. product_id: 3fdb534dccf5bc9ab0406944b913787d, demand: 14, avg_review_score: 2.2857142857142857
42. product_id: 16bf176650a888512655cc94f61860e3, demand: 13, avg_review_score: 2.2307692307692308
43. product_id: cae79e3b5c787c231543fa415a20b5cc, demand: 13, avg_review_score: 2.3846153846153846
44. product_id: 63085bb4366ded27bcb63cbb59b4103a, demand: 13, avg_review_score: 2.7500000000000000
45. product_id: 4d0ec1e9b95fb62f9a1fbe21808bf3b1, demand: 13, avg_review_score: 2.8461538461538462
46. product_id: 9ac1378f05cd222b3fb34a3cccc626c7, demand: 12, avg_review_score: 2.7500000000000000
47. product_id: 5f00c50de3d989194f0439e343480372, demand: 12, avg_review_score: 2.8333333333333333
48. product_id: 4a90b44b456e79e7a33435fdd36e551f, demand: 12, avg_review_score: 2.9166666666666667
49. product_id: ab1ecbce7afd9f6e661baa24a5706c9c, demand: 12, avg_review_score: 2.8333333333333333
50. product_id: 70120d2f9b9193aa0030342072d8adec, demand: 12, avg_review_score: 2.5454545454545455
51. product_id: 12dc5e5d178b930cf87cf16e812fc2d5, demand: 12, avg_review_score: 2.3333333333333333
52. product_id: 83e68070fbf16ac859fc13285a5ba9ba, demand: 12, avg_review_score: 2.9166666666666667
53. product_id: 391a014a66920fa0ce468319264e0232, demand: 12, avg_review_score: 2.5454545454545455
54. product_id: 86ecc269de40ba13205e7beeee12f26f, demand: 12, avg_review_score: 2.6666666666666667
55. product_id: b47865eeb745bcbfca95513b46bd977d, demand: 12, avg_review_score: 2.9166666666666667
56. product_id: 588ea3decc0d8e1d19ce6160c5b0da1b, demand: 12, avg_review_score: 2.7500000000000000
57. product_id: 0db4869ac8a908414823d44d742f5ba3, demand: 12, avg_review_score: 2.7500000000000000
58. product_id: d1847c3f994dc0bb4d1248520ecb81f3, demand: 12, avg_review_score: 2.9166666666666667
59. product_id: f32af0a8b0bcb05b60f05e8907ad8866, demand: 11, avg_review_score: 2.7272727272727273
60. product_id: f919da4f716dc149cef4551a322001fd, demand: 11, avg_review_score: 1.8181818181818182
61. product_id: e5989cd466f0714e1439b95bf6a279da, demand: 11, avg_review_score: 1.7272727272727273
62. product_id: 79706e79825f7409ef032653a271fba2, demand: 11, avg_review_score: 2.2727272727272727
63. product_id: 6a057a401eab3b3cb8083d9e42972233, demand: 11, avg_review_score: 2.9090909090909091
64. product_id: 2d27434c710806b971a721da337a112a, demand: 11, avg_review_score: 2.9000000000000000
65. product_id: 41801d2ed5124923137ec39aeeea1e93, demand: 11, avg_review_score: 2.8000000000000000
66. product_id: de17feec1983829fec4bc58cadaa43f3, demand: 11, avg_review_score: 2.1818181818181818
67. product_id: a5c9c1711f61d2b63cf996b4928092ed, demand: 11, avg_review_score: 2.3636363636363636
68. product_id: fd0065af7f09af4b82a0ca8f3eed1852, demand: 11, avg_review_score: 1.1818181818181818
```

#### 📊 Metadata

- **sql:** SELECT oi.product_id, COUNT(oi.order_id) AS demand, AVG(r.review_score) AS avg_review_score FROM analytics.order_items oi JOIN analytics.orders o ON oi.order_id = o.order_id LEFT JOIN analytics.order_reviews r ON o.order_id = r.order_id GROUP BY oi.product_id HAVING COUNT(oi.order_id) > 10 AND AVG(r.review_score) < 3 ORDER BY demand DESC
- **row_count:** 68
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-15"></a>
### Query 15

#### 📝 Input

- **Query:** Qual é a penetração de cada categoria de produto por estado brasileiro?

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.85
- **Reason:** category penetration by state involves product and customer location data
- **Thread ID:** `90cae143-fe24-4add-9856-7d98fc40b002`

#### 💬 Response

```
Encontrados 1394 registros.

Penetração por estado:
AC: artigos_de_natal: 1, automotivo: 4, bebes: 3, beleza_saude: 6, brinquedos: 3, cama_mesa_banho: 3, consoles_games: 1, cool_stuff: 1, eletronicos: 4, eletroportateis: 1, esporte_lazer: 9, fashion_bolsas_e_acessorios: 1, fashion_calcados: 2, ferramentas_jardim: 2, informatica_acessorios: 7, instrumentos_musicais: 1, livros_interesse_geral: 2, malas_acessorios: 2, market_place: 1, moveis_decoracao: 7, moveis_sala: 1, papelaria: 2, pcs: 1, perfumaria: 3, relogios_presentes: 4, telefonia: 5, utilidades_domesticas: 3
AL: agro_industria_e_comercio: 1, alimentos: 1, alimentos_bebidas: 1, audio: 5, automotivo: 21, bebes: 7, bebidas: 1, beleza_saude: 63, brinquedos: 12, cama_mesa_banho: 19, casa_conforto: 1, casa_construcao: 3, climatizacao: 1, consoles_games: 7, construcao_ferramentas_construcao: 2, cool_stuff: 16, dvds_blu_ray: 1, eletrodomesticos: 3, eletrodomesticos_2: 2, eletronicos: 13, esporte_lazer: 32, fashion_bolsas_e_acessorios: 4, fashion_calcados: 3, ferramentas_jardim: 13, industria_comercio_e_negocios: 1, informatica_acessorios: 34, instrumentos_musicais: 1, livros_interesse_geral: 1, malas_acessorios: 5, market_place: 2, moveis_cozinha_area_de_servico_jantar_e_jardim: 1, moveis_decoracao: 25, moveis_escritorio: 3, moveis_sala: 3, papelaria: 8, pcs: 2, perfumaria: 12, pet_shop: 3, relogios_presentes: 35, telefonia: 26, telefonia_fixa: 4, utilidades_domesticas: 9
AM: alimentos: 1, artes: 1, audio: 1, automotivo: 4, bebes: 5, bebidas: 1, beleza_saude: 15, brinquedos: 6, cama_mesa_banho: 7, casa_construcao: 4, climatizacao: 1, consoles_games: 2, construcao_ferramentas_jardim: 2, cool_stuff: 4, eletrodomesticos: 2, eletrodomesticos_2: 1, eletronicos: 4, esporte_lazer: 12, fashion_bolsas_e_acessorios: 1, ferramentas_jardim: 5, informatica_acessorios: 11, instrumentos_musicais: 1, livros_interesse_geral: 1, malas_acessorios: 2, market_place: 1, moveis_decoracao: 4, moveis_escritorio: 2, musica: 1, papelaria: 6, pcs: 1, perfumaria: 2, pet_shop: 4, relogios_presentes: 11, tablets_impressao_imagem: 1, telefonia: 14, telefonia_fixa: 1, utilidades_domesticas: 4
AP: agro_industria_e_comercio: 1, artes: 2, automotivo: 3, beleza_saude: 10, brinquedos: 3, cama_mesa_banho: 3, consoles_games: 1, cool_stuff: 2, eletronicos: 3, esporte_lazer: 6, ferramentas_jardim: 2, informatica_acessorios: 7, instrumentos_musicais: 2, moveis_decoracao: 2, papelaria: 2, pcs: 1, pet_shop: 1, relogios_presentes: 7, telefonia: 4, telefonia_fixa: 2, utilidades_domesticas: 4
BA: agro_industria_e_comercio: 3, alimentos: 15, alimentos_bebidas: 6, artes: 10, artigos_de_natal: 8, audio: 14, automotivo: 148, bebes: 95, bebidas: 6, beleza_saude: 329, brinquedos: 116, cama_mesa_banho: 223, casa_conforto: 10, casa_conforto_2: 1, casa_construcao: 11, cine_foto: 3, climatizacao: 6, consoles_games: 33, construcao_ferramentas_construcao: 26, construcao_ferramentas_ferramentas: 4, construcao_ferramentas_iluminacao: 6, construcao_ferramentas_jardim: 7, construcao_ferramentas_seguranca: 7, cool_stuff: 139, eletrodomesticos: 38, eletrodomesticos_2: 6, eletronicos: 98, eletroportateis: 18, esporte_lazer: 257, fashion_bolsas_e_acessorios: 70, fashion_calcados: 7, fashion_esporte: 2, fashion_roupa_feminina: 1, fashion_roupa_infanto_juvenil: 1, fashion_roupa_masculina: 7, fashion_underwear_e_moda_praia: 6, ferramentas_jardim: 145, fraldas_higiene: 1, industria_comercio_e_negocios: 4, informatica_acessorios: 222, instrumentos_musicais: 33, livros_importados: 1, livros_interesse_geral: 15, livros_tecnicos: 10, malas_acessorios: 32, market_place: 4, moveis_cozinha_area_de_servico_jantar_e_jardim: 3, moveis_decoracao: 202, moveis_escritorio: 61, moveis_quarto: 4, moveis_sala: 17, papelaria: 76, pcs: 19, perfumaria: 80, pet_shop: 54, portateis_casa_forno_e_cafe: 3, portateis_cozinha_e_preparadores_de_alimentos: 1, relogios_presentes: 222, sinalizacao_e_seguranca: 6, tablets_impressao_imagem: 5, telefonia: 229, telefonia_fixa: 8, utilidades_domesticas: 143
CE: agro_industria_e_comercio: 2, alimentos: 5, alimentos_bebidas: 3, artigos_de_natal: 2, audio: 5, automotivo: 54, bebes: 30, bebidas: 2, beleza_saude: 156, brinquedos: 63, cama_mesa_banho: 68, casa_conforto: 4, casa_construcao: 7, climatizacao: 2, consoles_games: 16, construcao_ferramentas_construcao: 9, construcao_ferramentas_ferramentas: 1, construcao_ferramentas_iluminacao: 1, construcao_ferramentas_jardim: 7, construcao_ferramentas_seguranca: 5, cool_stuff: 48, eletrodomesticos: 7, eletrodomesticos_2: 3, eletronicos: 41, eletroportateis: 8, esporte_lazer: 89, fashion_bolsas_e_acessorios: 28, fashion_calcados: 2, fashion_roupa_masculina: 1, ferramentas_jardim: 46, fraldas_higiene: 1, industria_comercio_e_negocios: 2, informatica_acessorios: 85, instrumentos_musicais: 7, livros_interesse_geral: 7, livros_tecnicos: 4, malas_acessorios: 21, market_place: 4, moveis_cozinha_area_de_servico_jantar_e_jardim: 1, moveis_decoracao: 68, moveis_escritorio: 22, moveis_sala: 2, musica: 1, papelaria: 31, pcs: 6, perfumaria: 54, pet_shop: 13, relogios_presentes: 129, tablets_impressao_imagem: 1, telefonia: 95, telefonia_fixa: 3, utilidades_domesticas: 47
DF: alimentos: 7, alimentos_bebidas: 4, artes: 6, artes_e_artesanato: 1, artigos_de_festas: 1, artigos_de_natal: 5, audio: 16, automotivo: 104, bebes: 66, bebidas: 5, beleza_saude: 223, brinquedos: 91, cama_mesa_banho: 173, casa_conforto: 6, casa_construcao: 7, cine_foto: 1, climatizacao: 3, consoles_games: 28, construcao_ferramentas_construcao: 10, construcao_ferramentas_iluminacao: 4, construcao_ferramentas_jardim: 5, construcao_ferramentas_seguranca: 3, cool_stuff: 79, dvds_blu_ray: 3, eletrodomesticos: 15, eletrodomesticos_2: 5, eletronicos: 50, eletroportateis: 23, esporte_lazer: 194, fashion_bolsas_e_acessorios: 41, fashion_calcados: 7, fashion_esporte: 1, fashion_roupa_feminina: 1, fashion_underwear_e_moda_praia: 2, ferramentas_jardim: 45, industria_comercio_e_negocios: 5, informatica_acessorios: 136, instrumentos_musicais: 10, livros_interesse_geral: 17, livros_tecnicos: 4, malas_acessorios: 23, market_place: 4, moveis_colchao_e_estofado: 1, moveis_cozinha_area_de_servico_jantar_e_jardim: 5, moveis_decoracao: 109, moveis_escritorio: 19, moveis_quarto: 1, moveis_sala: 7, musica: 1, papelaria: 45, pcs: 6, perfumaria: 82, pet_shop: 35, portateis_casa_forno_e_cafe: 1, relogios_presentes: 143, seguros_e_servicos: 1, sinalizacao_e_seguranca: 4, telefonia: 85, telefonia_fixa: 3, utilidades_domesticas: 123
ES: agro_industria_e_comercio: 2, alimentos: 14, alimentos_bebidas: 6, artes: 1, artigos_de_festas: 2, artigos_de_natal: 2, audio: 13, automotivo: 82, bebes: 62, bebidas: 5, beleza_saude: 153, brinquedos: 93, cama_mesa_banho: 199, casa_conforto: 11, casa_conforto_2: 1, casa_construcao: 14, cine_foto: 1, climatizacao: 6, consoles_games: 22, construcao_ferramentas_construcao: 10, construcao_ferramentas_ferramentas: 4, construcao_ferramentas_iluminacao: 5, construcao_ferramentas_jardim: 3, cool_stuff: 63, eletrodomesticos: 15, eletrodomesticos_2: 3, eletronicos: 73, eletroportateis: 3, esporte_lazer: 157, fashion_bolsas_e_acessorios: 45, fashion_calcados: 5, fashion_roupa_feminina: 1, fashion_roupa_masculina: 3, fashion_underwear_e_moda_praia: 1, ferramentas_jardim: 85, flores: 2, industria_comercio_e_negocios: 2, informatica_acessorios: 139, instrumentos_musicais: 19, livros_interesse_geral: 8, livros_tecnicos: 14, malas_acessorios: 15, market_place: 7, moveis_cozinha_area_de_servico_jantar_e_jardim: 1, moveis_decoracao: 114, moveis_escritorio: 24, moveis_quarto: 1, moveis_sala: 11, papelaria: 47, pcs: 3, perfumaria: 60, pet_shop: 21, relogios_presentes: 145, sinalizacao_e_seguranca: 4, tablets_impressao_imagem: 4, telefonia: 104, telefonia_fixa: 6, utilidades_domesticas: 103
GO: agro_industria_e_comercio: 6, alimentos: 6, artes: 4, artigos_de_festas: 1, artigos_de_natal: 3, audio: 7, automotivo: 75, bebes: 54, bebidas: 4, beleza_saude: 208, brinquedos: 76, cama_mesa_banho: 192, casa_conforto: 8, casa_conforto_2: 4, casa_construcao: 12, cine_foto: 1, climatizacao: 6, consoles_games: 21, construcao_ferramentas_construcao: 8, construcao_ferramentas_ferramentas: 5, construcao_ferramentas_iluminacao: 5, construcao_ferramentas_jardim: 5, construcao_ferramentas_seguranca: 6, cool_stuff: 86, dvds_blu_ray: 1, eletrodomesticos: 14, eletrodomesticos_2: 3, eletronicos: 32, eletroportateis: 10, esporte_lazer: 151, fashion_bolsas_e_acessorios: 45, fashion_calcados: 6, fashion_roupa_feminina: 2, fashion_roupa_masculina: 3, fashion_underwear_e_moda_praia: 5, ferramentas_jardim: 76, flores: 1, industria_comercio_e_negocios: 6, informatica_acessorios: 111, instrumentos_musicais: 9, la_cuisine: 1, livros_interesse_geral: 13, livros_tecnicos: 2, malas_acessorios: 12, market_place: 7, moveis_colchao_e_estofado: 1, moveis_cozinha_area_de_servico_jantar_e_jardim: 2, moveis_decoracao: 104, moveis_escritorio: 21, moveis_quarto: 1, moveis_sala: 10, musica: 1, papelaria: 43, pcs: 2, perfumaria: 85, pet_shop: 25, portateis_cozinha_e_preparadores_de_alimentos: 1, relogios_presentes: 143, sinalizacao_e_seguranca: 5, tablets_impressao_imagem: 1, telefonia: 115, telefonia_fixa: 5, utilidades_domesticas: 101
MA: agro_industria_e_comercio: 1, alimentos_bebidas: 2, artigos_de_natal: 1, audio: 3, automotivo: 38, bebes: 27, beleza_saude: 83, brinquedos: 21, cama_mesa_banho: 32, casa_conforto: 2, casa_construcao: 4, cds_dvds_musicais: 1, cine_foto: 1, climatizacao: 1, consoles_games: 6, construcao_ferramentas_construcao: 1, construcao_ferramentas_iluminacao: 1, cool_stuff: 35, eletrodomesticos: 3, eletronicos: 13, eletroportateis: 2, esporte_lazer: 59, fashion_bolsas_e_acessorios: 22, fashion_calcados: 1, fashion_esporte: 1, fashion_roupa_masculina: 1, ferramentas_jardim: 19, industria_comercio_e_negocios: 1, informatica_acessorios: 65, instrumentos_musicais: 9, livros_importados: 1, livros_interesse_geral: 3, livros_tecnicos: 3, malas_acessorios: 8, market_place: 4, moveis_decoracao: 40, moveis_escritorio: 14, moveis_sala: 2, papelaria: 16, pcs: 5, perfumaria: 30, pet_shop: 9, relogios_presentes: 58, tablets_impressao_imagem: 1, telefonia: 60, telefonia_fixa: 1, utilidades_domesticas: 22
MG: agro_industria_e_comercio: 14, alimentos: 35, alimentos_bebidas: 20, artes: 18, artes_e_artesanato: 6, artigos_de_festas: 4, artigos_de_natal: 18, audio: 33, automotivo: 471, bebes: 345, bebidas: 20, beleza_saude: 1011, brinquedos: 458, cama_mesa_banho: 1129, casa_conforto: 53, casa_conforto_2: 3, casa_construcao: 58, cine_foto: 6, climatizacao: 18, consoles_games: 122, construcao_ferramentas_construcao: 99, construcao_ferramentas_ferramentas: 17, construcao_ferramentas_iluminacao: 36, construcao_ferramentas_jardim: 21, construcao_ferramentas_seguranca: 25, cool_stuff: 434, dvds_blu_ray: 4, eletrodomesticos: 85, eletrodomesticos_2: 20, eletronicos: 260, eletroportateis: 61, esporte_lazer: 867, fashion_bolsas_e_acessorios: 248, fashion_calcados: 41, fashion_esporte: 2, fashion_roupa_feminina: 7, fashion_roupa_masculina: 14, fashion_underwear_e_moda_praia: 13, ferramentas_jardim: 488, flores: 4, fraldas_higiene: 1, industria_comercio_e_negocios: 14, informatica_acessorios: 877, instrumentos_musicais: 71, la_cuisine: 2, livros_importados: 6, livros_interesse_geral: 50, livros_tecnicos: 28, malas_acessorios: 176, market_place: 31, moveis_colchao_e_estofado: 3, moveis_cozinha_area_de_servico_jantar_e_jardim: 27, moveis_decoracao: 727, moveis_escritorio: 134, moveis_quarto: 7, moveis_sala: 43, musica: 6, papelaria: 243, pc_gamer: 1, pcs: 18, perfumaria: 379, pet_shop: 222, portateis_casa_forno_e_cafe: 10, portateis_cozinha_e_preparadores_de_alimentos: 2, relogios_presentes: 611, sinalizacao_e_seguranca: 10, tablets_impressao_imagem: 9, telefonia: 460, telefonia_fixa: 17, utilidades_domesticas: 702
MS: agro_industria_e_comercio: 3, alimentos: 4, alimentos_bebidas: 1, artes: 1, artigos_de_natal: 1, audio: 1, automotivo: 24, bebes: 28, bebidas: 4, beleza_saude: 58, brinquedos: 34, cama_mesa_banho: 57, casa_conforto: 1, casa_construcao: 7, consoles_games: 6, construcao_ferramentas_construcao: 8, construcao_ferramentas_ferramentas: 1, construcao_ferramentas_iluminacao: 5, construcao_ferramentas_jardim: 2, construcao_ferramentas_seguranca: 2, cool_stuff: 26, dvds_blu_ray: 3, eletrodomesticos: 6, eletrodomesticos_2: 3, eletronicos: 20, eletroportateis: 5, esporte_lazer: 61, fashion_bolsas_e_acessorios: 14, fashion_calcados: 4, fashion_underwear_e_moda_praia: 3, ferramentas_jardim: 20, flores: 1, industria_comercio_e_negocios: 1, informatica_acessorios: 55, instrumentos_musicais: 7, livros_interesse_geral: 2, livros_tecnicos: 4, malas_acessorios: 9, market_place: 2, moveis_decoracao: 45, moveis_escritorio: 4, moveis_quarto: 1, moveis_sala: 3, papelaria: 19, pcs: 1, perfumaria: 21, pet_shop: 22, portateis_casa_forno_e_cafe: 1, relogios_presentes: 29, sinalizacao_e_seguranca: 1, tablets_impressao_imagem: 1, telefonia: 26, telefonia_fixa: 1, utilidades_domesticas: 34
MT: agro_industria_e_comercio: 2, alimentos: 6, artes: 1, artigos_de_natal: 1, audio: 4, automotivo: 51, bebes: 34, bebidas: 1, beleza_saude: 84, brinquedos: 39, cama_mesa_banho: 56, casa_conforto: 3, casa_construcao: 6, cine_foto: 1, climatizacao: 3, consoles_games: 9, construcao_ferramentas_construcao: 7, construcao_ferramentas_ferramentas: 1, construcao_ferramentas_iluminacao: 3, construcao_ferramentas_seguranca: 4, cool_stuff: 45, eletrodomesticos: 8, eletrodomesticos_2: 3, eletronicos: 22, eletroportateis: 7, esporte_lazer: 70, fashion_bolsas_e_acessorios: 13, fashion_calcados: 3, fashion_roupa_feminina: 1, fashion_roupa_masculina: 1, fashion_underwear_e_moda_praia: 1, ferramentas_jardim: 37, industria_comercio_e_negocios: 3, informatica_acessorios: 45, instrumentos_musicais: 5, livros_interesse_geral: 2, livros_tecnicos: 5, malas_acessorios: 8, market_place: 5, moveis_cozinha_area_de_servico_jantar_e_jardim: 2, moveis_decoracao: 54, moveis_escritorio: 14, moveis_quarto: 1, moveis_sala: 3, papelaria: 24, pcs: 2, perfumaria: 22, pet_shop: 14, portateis_casa_forno_e_cafe: 1, relogios_presentes: 59, sinalizacao_e_seguranca: 1, tablets_impressao_imagem: 2, telefonia: 60, utilidades_domesticas: 40
PA: agro_industria_e_comercio: 2, alimentos_bebidas: 1, artes: 2, artigos_de_natal: 1, audio: 1, automotivo: 45, bebes: 42, bebidas: 1, beleza_saude: 101, brinquedos: 29, cama_mesa_banho: 34, casa_construcao: 2, cine_foto: 2, consoles_games: 14, construcao_ferramentas_construcao: 2, construcao_ferramentas_ferramentas: 1, construcao_ferramentas_iluminacao: 1, construcao_ferramentas_jardim: 1, cool_stuff: 48, eletrodomesticos: 10, eletronicos: 27, eletroportateis: 8, esporte_lazer: 76, fashion_bolsas_e_acessorios: 29, fashion_calcados: 4, fashion_esporte: 1, fashion_roupa_masculina: 2, fashion_underwear_e_moda_praia: 3, ferramentas_jardim: 27, informatica_acessorios: 84, instrumentos_musicais: 9, livros_importados: 1, livros_interesse_geral: 3, livros_tecnicos: 2, malas_acessorios: 7, market_place: 5, moveis_cozinha_area_de_servico_jantar_e_jardim: 1, moveis_decoracao: 54, moveis_escritorio: 21, moveis_sala: 1, papelaria: 22, pcs: 4, perfumaria: 33, pet_shop: 11, portateis_cozinha_e_preparadores_de_alimentos: 1, relogios_presentes: 74, sinalizacao_e_seguranca: 1, tablets_impressao_imagem: 4, telefonia: 70, telefonia_fixa: 1, utilidades_domesticas: 31
PB: agro_industria_e_comercio: 2, alimentos: 3, artes: 1, audio: 1, automotivo: 22, bebes: 13, beleza_saude: 77, brinquedos: 15, cama_mesa_banho: 29, casa_conforto: 1, casa_construcao: 5, climatizacao: 1, consoles_games: 7, construcao_ferramentas_construcao: 1, construcao_ferramentas_ferramentas: 1, construcao_ferramentas_jardim: 1, construcao_ferramentas_seguranca: 3, cool_stuff: 22, eletrodomesticos: 2, eletronicos: 13, eletroportateis: 4, esporte_lazer: 32, fashion_bolsas_e_acessorios: 12, fashion_calcados: 1, fashion_roupa_feminina: 1, ferramentas_jardim: 14, fraldas_higiene: 1, industria_comercio_e_negocios: 3, informatica_acessorios: 41, instrumentos_musicais: 4, livros_interesse_geral: 3, malas_acessorios: 7, market_place: 2, moveis_cozinha_area_de_servico_jantar_e_jardim: 1, moveis_decoracao: 31, moveis_escritorio: 7, moveis_sala: 3, papelaria: 16, pcs: 4, perfumaria: 18, pet_shop: 8, relogios_presentes: 43, sinalizacao_e_seguranca: 1, telefonia: 25, telefonia_fixa: 4, utilidades_domesticas: 18
PE: agro_industria_e_comercio: 5, alimentos: 8, alimentos_bebidas: 5, artes: 1, artigos_de_natal: 4, audio: 4, automotivo: 82, bebes: 41, beleza_saude: 226, brinquedos: 57, cama_mesa_banho: 82, casa_conforto: 6, casa_construcao: 6, cine_foto: 1, climatizacao: 2, consoles_games: 20, construcao_ferramentas_construcao: 9, construcao_ferramentas_ferramentas: 1, construcao_ferramentas_iluminacao: 3, construcao_ferramentas_jardim: 6, construcao_ferramentas_seguranca: 4, cool_stuff: 73, dvds_blu_ray: 2, eletrodomesticos: 5, eletrodomesticos_2: 2, eletronicos: 37, eletroportateis: 3, esporte_lazer: 135, fashion_bolsas_e_acessorios: 34, fashion_calcados: 11, fashion_underwear_e_moda_praia: 2, ferramentas_jardim: 58, flores: 1, industria_comercio_e_negocios: 4, informatica_acessorios: 100, instrumentos_musicais: 11, livros_interesse_geral: 8, livros_tecnicos: 4, malas_acessorios: 13, market_place: 3, moveis_cozinha_area_de_servico_jantar_e_jardim: 4, moveis_decoracao: 73, moveis_escritorio: 19, moveis_quarto: 1, moveis_sala: 4, papelaria: 47, pc_gamer: 1, pcs: 9, perfumaria: 47, pet_shop: 22, portateis_casa_forno_e_cafe: 1, relogios_presentes: 147, sinalizacao_e_seguranca: 1, tablets_impressao_imagem: 2, telefonia: 122, telefonia_fixa: 3, utilidades_domesticas: 55
PI: agro_industria_e_comercio: 3, alimentos: 1, alimentos_bebidas: 1, artes: 1, artigos_de_festas: 1, audio: 4, automotivo: 28, bebes: 11, bebidas: 1, beleza_saude: 51, brinquedos: 28, cama_mesa_banho: 24, casa_conforto: 3, casa_construcao: 4, climatizacao: 3, consoles_games: 7, construcao_ferramentas_construcao: 1, construcao_ferramentas_iluminacao: 1, construcao_ferramentas_jardim: 4, cool_stuff: 20, dvds_blu_ray: 1, eletrodomesticos: 4, eletrodomesticos_2: 1, eletronicos: 22, esporte_lazer: 31, fashion_bolsas_e_acessorios: 5, fashion_calcados: 1, fashion_underwear_e_moda_praia: 1, ferramentas_jardim: 17, industria_comercio_e_negocios: 3, informatica_acessorios: 36, instrumentos_musicais: 5, livros_interesse_geral: 1, livros_tecnicos: 2, malas_acessorios: 5, market_place: 3, moveis_decoracao: 15, moveis_escritorio: 9, moveis_sala: 2, papelaria: 10, pcs: 3, perfumaria: 16, pet_shop: 7, relogios_presentes: 38, tablets_impressao_imagem: 3, telefonia: 35, telefonia_fixa: 2, utilidades_domesticas: 14
PR: agro_industria_e_comercio: 12, alimentos: 27, alimentos_bebidas: 13, artes: 9, artigos_de_festas: 2, artigos_de_natal: 6, audio: 17, automotivo: 209, bebes: 152, bebidas: 10, beleza_saude: 381, brinquedos: 201, cama_mesa_banho: 402, casa_conforto: 13, casa_conforto_2: 1, casa_construcao: 21, cine_foto: 2, climatizacao: 10, consoles_games: 41, construcao_ferramentas_construcao: 46, construcao_ferramentas_ferramentas: 7, construcao_ferramentas_iluminacao: 13, construcao_ferramentas_jardim: 5, construcao_ferramentas_seguranca: 13, cool_stuff: 203, dvds_blu_ray: 3, eletrodomesticos: 42, eletrodomesticos_2: 14, eletronicos: 168, eletroportateis: 39, esporte_lazer: 428, fashion_bolsas_e_acessorios: 107, fashion_calcados: 16, fashion_esporte: 1, fashion_roupa_feminina: 2, fashion_roupa_masculina: 10, fashion_underwear_e_moda_praia: 6, ferramentas_jardim: 174, fraldas_higiene: 2, industria_comercio_e_negocios: 10, informatica_acessorios: 338, instrumentos_musicais: 34, livros_importados: 2, livros_interesse_geral: 34, livros_tecnicos: 15, malas_acessorios: 49, market_place: 14, moveis_cozinha_area_de_servico_jantar_e_jardim: 12, moveis_decoracao: 397, moveis_escritorio: 55, moveis_quarto: 8, moveis_sala: 14, musica: 7, papelaria: 121, pcs: 4, perfumaria: 138, pet_shop: 82, portateis_casa_forno_e_cafe: 8, relogios_presentes: 274, sinalizacao_e_seguranca: 3, tablets_impressao_imagem: 3, telefonia: 226, telefonia_fixa: 6, utilidades_domesticas: 283
RJ: agro_industria_e_comercio: 25, alimentos: 41, alimentos_bebidas: 41, artes: 32, artigos_de_festas: 5, artigos_de_natal: 12, audio: 54, automotivo: 413, bebes: 345, bebidas: 41, beleza_saude: 974, brinquedos: 552, cama_mesa_banho: 1393, casa_conforto: 56, casa_conforto_2: 2, casa_construcao: 51, cds_dvds_musicais: 2, cine_foto: 5, climatizacao: 60, consoles_games: 131, construcao_ferramentas_construcao: 105, construcao_ferramentas_ferramentas: 9, construcao_ferramentas_iluminacao: 19, construcao_ferramentas_jardim: 29, construcao_ferramentas_seguranca: 17, cool_stuff: 503, dvds_blu_ray: 12, eletrodomesticos: 83, eletrodomesticos_2: 45, eletronicos: 400, eletroportateis: 85, esporte_lazer: 925, fashion_bolsas_e_acessorios: 185, fashion_calcados: 23, fashion_esporte: 2, fashion_roupa_feminina: 2, fashion_roupa_infanto_juvenil: 1, fashion_roupa_masculina: 12, fashion_underwear_e_moda_praia: 14, ferramentas_jardim: 550, flores: 7, fraldas_higiene: 2, industria_comercio_e_negocios: 23, informatica_acessorios: 859, instrumentos_musicais: 76, livros_importados: 5, livros_interesse_geral: 55, livros_tecnicos: 29, malas_acessorios: 117, market_place: 34, moveis_colchao_e_estofado: 8, moveis_cozinha_area_de_servico_jantar_e_jardim: 43, moveis_decoracao: 858, moveis_escritorio: 217, moveis_quarto: 17, moveis_sala: 96, musica: 8, papelaria: 305, pc_gamer: 2, pcs: 22, perfumaria: 415, pet_shop: 199, portateis_casa_forno_e_cafe: 7, portateis_cozinha_e_preparadores_de_alimentos: 1, relogios_presentes: 817, sinalizacao_e_seguranca: 17, tablets_impressao_imagem: 10, telefonia: 407, telefonia_fixa: 27, utilidades_domesticas: 746
RN: alimentos: 2, alimentos_bebidas: 4, artes: 1, artigos_de_natal: 1, audio: 1, automotivo: 17, bebes: 15, beleza_saude: 57, brinquedos: 23, cama_mesa_banho: 24, casa_conforto: 1, casa_construcao: 1, consoles_games: 6, construcao_ferramentas_construcao: 6, construcao_ferramentas_jardim: 3, construcao_ferramentas_seguranca: 1, cool_stuff: 21, dvds_blu_ray: 1, eletrodomesticos: 2, eletrodomesticos_2: 2, eletronicos: 14, eletroportateis: 3, esporte_lazer: 20, fashion_bolsas_e_acessorios: 7, fashion_calcados: 2, ferramentas_jardim: 16, industria_comercio_e_negocios: 1, informatica_acessorios: 27, instrumentos_musicais: 2, livros_interesse_geral: 22, livros_tecnicos: 1, malas_acessorios: 1, market_place: 2, moveis_colchao_e_estofado: 1, moveis_cozinha_area_de_servico_jantar_e_jardim: 2, moveis_decoracao: 29, moveis_escritorio: 5, moveis_quarto: 2, papelaria: 11, perfumaria: 21, pet_shop: 9, relogios_presentes: 47, sinalizacao_e_seguranca: 1, telefonia: 22, utilidades_domesticas: 22
RO: agro_industria_e_comercio: 1, alimentos: 1, artes: 2, artigos_de_natal: 2, automotivo: 10, bebes: 11, beleza_saude: 23, brinquedos: 13, cama_mesa_banho: 15, casa_conforto: 1, consoles_games: 1, construcao_ferramentas_construcao: 4, construcao_ferramentas_jardim: 2, construcao_ferramentas_seguranca: 1, cool_stuff: 12, dvds_blu_ray: 1, eletrodomesticos: 2, eletronicos: 6, eletroportateis: 1, esporte_lazer: 17, fashion_bolsas_e_acessorios: 7, fashion_calcados: 1, ferramentas_jardim: 6, industria_comercio_e_negocios: 1, informatica_acessorios: 17, instrumentos_musicais: 1, livros_interesse_geral: 1, malas_acessorios: 6, market_place: 1, moveis_decoracao: 10, moveis_escritorio: 5, moveis_sala: 1, papelaria: 7, pcs: 2, perfumaria: 6, pet_shop: 8, portateis_casa_forno_e_cafe: 1, relogios_presentes: 14, seguros_e_servicos: 1, telefonia: 17, utilidades_domesticas: 5
RR: automotivo: 1, bebes: 2, beleza_saude: 6, cama_mesa_banho: 2, cool_stuff: 2, eletrodomesticos: 3, eletronicos: 2, esporte_lazer: 6, ferramentas_jardim: 2, informatica_acessorios: 5, moveis_decoracao: 4, moveis_escritorio: 1, papelaria: 2, perfumaria: 1, relogios_presentes: 1, telefonia: 4
RS: agro_industria_e_comercio: 9, alimentos: 12, alimentos_bebidas: 4, artes: 9, artigos_de_festas: 3, artigos_de_natal: 5, audio: 16, automotivo: 176, bebes: 201, bebidas: 14, beleza_saude: 396, brinquedos: 203, cama_mesa_banho: 540, casa_conforto: 19, casa_conforto_2: 1, casa_construcao: 37, cds_dvds_musicais: 3, cine_foto: 9, climatizacao: 12, consoles_games: 58, construcao_ferramentas_construcao: 35, construcao_ferramentas_ferramentas: 8, construcao_ferramentas_iluminacao: 18, construcao_ferramentas_jardim: 7, construcao_ferramentas_seguranca: 7, cool_stuff: 255, dvds_blu_ray: 4, eletrodomesticos: 44, eletrodomesticos_2: 12, eletronicos: 157, eletroportateis: 39, esporte_lazer: 421, fashion_bolsas_e_acessorios: 77, fashion_calcados: 10, fashion_esporte: 2, fashion_roupa_masculina: 7, fashion_underwear_e_moda_praia: 3, ferramentas_jardim: 232, flores: 3, industria_comercio_e_negocios: 19, informatica_acessorios: 390, instrumentos_musicais: 30, la_cuisine: 3, livros_importados: 2, livros_interesse_geral: 28, livros_tecnicos: 12, malas_acessorios: 56, market_place: 21, moveis_cozinha_area_de_servico_jantar_e_jardim: 12, moveis_decoracao: 444, moveis_escritorio: 56, moveis_quarto: 2, moveis_sala: 22, musica: 1, papelaria: 137, pc_gamer: 1, pcs: 8, perfumaria: 146, pet_shop: 84, portateis_casa_forno_e_cafe: 3, portateis_cozinha_e_preparadores_de_alimentos: 1, relogios_presentes: 227, sinalizacao_e_seguranca: 14, tablets_impressao_imagem: 1, telefonia: 255, telefonia_fixa: 18, utilidades_domesticas: 350
SC: agro_industria_e_comercio: 3, alimentos: 14, alimentos_bebidas: 3, artes: 6, artes_e_artesanato: 1, artigos_de_festas: 2, artigos_de_natal: 11, audio: 10, automotivo: 164, bebes: 97, bebidas: 14, beleza_saude: 287, brinquedos: 115, cama_mesa_banho: 272, casa_conforto: 12, casa_construcao: 22, cine_foto: 4, climatizacao: 1, consoles_games: 33, construcao_ferramentas_construcao: 21, construcao_ferramentas_ferramentas: 5, construcao_ferramentas_iluminacao: 10, construcao_ferramentas_jardim: 4, construcao_ferramentas_seguranca: 12, cool_stuff: 148, dvds_blu_ray: 2, eletrodomesticos: 24, eletrodomesticos_2: 17, eletronicos: 114, eletroportateis: 26, esporte_lazer: 315, fashion_bolsas_e_acessorios: 75, fashion_calcados: 5, fashion_esporte: 3, fashion_roupa_feminina: 1, fashion_roupa_infanto_juvenil: 2, fashion_roupa_masculina: 2, fashion_underwear_e_moda_praia: 7, ferramentas_jardim: 145, industria_comercio_e_negocios: 13, informatica_acessorios: 267, instrumentos_musicais: 24, la_cuisine: 2, livros_importados: 1, livros_interesse_geral: 20, livros_tecnicos: 9, malas_acessorios: 35, market_place: 14, moveis_colchao_e_estofado: 2, moveis_cozinha_area_de_servico_jantar_e_jardim: 6, moveis_decoracao: 276, moveis_escritorio: 42, moveis_quarto: 3, moveis_sala: 12, papelaria: 83, pcs: 5, perfumaria: 108, pet_shop: 79, portateis_casa_forno_e_cafe: 4, relogios_presentes: 164, sinalizacao_e_seguranca: 5, telefonia: 165, telefonia_fixa: 5, utilidades_domesticas: 224
SE: alimentos: 1, alimentos_bebidas: 1, automotivo: 20, bebes: 8, beleza_saude: 40, brinquedos: 11, cama_mesa_banho: 14, casa_conforto: 1, casa_construcao: 3, consoles_games: 5, construcao_ferramentas_construcao: 1, construcao_ferramentas_iluminacao: 1, construcao_ferramentas_seguranca: 1, cool_stuff: 17, eletrodomesticos: 1, eletrodomesticos_2: 1, eletronicos: 13, eletroportateis: 3, esporte_lazer: 31, fashion_bolsas_e_acessorios: 8, ferramentas_jardim: 19, industria_comercio_e_negocios: 3, informatica_acessorios: 33, instrumentos_musicais: 3, livros_importados: 1, livros_interesse_geral: 1, malas_acessorios: 3, market_place: 3, moveis_decoracao: 19, moveis_escritorio: 3, moveis_quarto: 2, moveis_sala: 2, papelaria: 3, pcs: 2, perfumaria: 6, pet_shop: 3, relogios_presentes: 20, sinalizacao_e_seguranca: 1, telefonia: 27, telefonia_fixa: 1, utilidades_domesticas: 8
SP: agro_industria_e_comercio: 85, alimentos: 246, alimentos_bebidas: 111, artes: 94, artes_e_artesanato: 15, artigos_de_festas: 18, artigos_de_natal: 44, audio: 139, automotivo: 1615, bebes: 1184, bebidas: 167, beleza_saude: 3789, brinquedos: 1612, cama_mesa_banho: 4416, casa_conforto: 184, casa_conforto_2: 11, casa_construcao: 204, cds_dvds_musicais: 6, cine_foto: 28, climatizacao: 117, consoles_games: 462, construcao_ferramentas_construcao: 337, construcao_ferramentas_ferramentas: 32, construcao_ferramentas_iluminacao: 110, construcao_ferramentas_jardim: 80, construcao_ferramentas_seguranca: 56, cool_stuff: 1314, dvds_blu_ray: 21, eletrodomesticos: 345, eletrodomesticos_2: 88, eletronicos: 938, eletroportateis: 281, esporte_lazer: 3296, fashion_bolsas_e_acessorios: 780, fashion_calcados: 84, fashion_esporte: 12, fashion_roupa_feminina: 20, fashion_roupa_infanto_juvenil: 4, fashion_roupa_masculina: 49, fashion_underwear_e_moda_praia: 54, ferramentas_jardim: 1267, flores: 10, fraldas_higiene: 19, industria_comercio_e_negocios: 115, informatica_acessorios: 2679, instrumentos_musicais: 253, la_cuisine: 5, livros_importados: 33, livros_interesse_geral: 214, livros_tecnicos: 110, malas_acessorios: 420, market_place: 105, moveis_colchao_e_estofado: 22, moveis_cozinha_area_de_servico_jantar_e_jardim: 124, moveis_decoracao: 2724, moveis_escritorio: 510, moveis_quarto: 44, moveis_sala: 161, musica: 12, papelaria: 982, pc_gamer: 3, pcs: 50, perfumaria: 1365, pet_shop: 771, portateis_casa_forno_e_cafe: 34, portateis_cozinha_e_preparadores_de_alimentos: 7, relogios_presentes: 2135, sinalizacao_e_seguranca: 65, tablets_impressao_imagem: 31, telefonia: 1521, telefonia_fixa: 97, utilidades_domesticas: 2781
TO: audio: 1, automotivo: 16, bebes: 7, beleza_saude: 29, brinquedos: 12, cama_mesa_banho: 9, casa_conforto: 1, casa_construcao: 1, consoles_games: 3, construcao_ferramentas_iluminacao: 2, cool_stuff: 16, eletrodomesticos: 1, eletrodomesticos_2: 3, eletronicos: 6, esporte_lazer: 23, fashion_bolsas_e_acessorios: 6, fashion_calcados: 1, ferramentas_jardim: 8, industria_comercio_e_negocios: 1, informatica_acessorios: 19, instrumentos_musicais: 1, livros_interesse_geral: 1, livros_tecnicos: 2, malas_acessorios: 2, market_place: 1, moveis_cozinha_area_de_servico_jantar_e_jardim: 1, moveis_decoracao: 14, moveis_escritorio: 5, moveis_sala: 2, papelaria: 3, pcs: 1, perfumaria: 12, pet_shop: 4, portateis_casa_forno_e_cafe: 1, relogios_presentes: 27, telefonia: 20, telefonia_fixa: 2, utilidades_domesticas: 12
```

#### 📊 Metadata

- **sql:** SELECT c.customer_state AS state, p.product_category_name AS category, COUNT(DISTINCT o.order_id) AS penetration FROM analytics.orders o JOIN analytics.customers c ON o.customer_id = c.customer_id JOIN analytics.order_items oi ON o.order_id = oi.order_id JOIN analytics.products p ON oi.product_id = p.product_id GROUP BY state, category ORDER BY state, category
- **row_count:** 1394
- **limit_applied:** False
- **exec_ms:** 367.83029199989414
- **fallback_used:** True

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-16"></a>
### Query 16

#### 📝 Input

- **Query:** Analise a concentração de vendas: quantos vendedores representam 80% da receita?

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.9
- **Reason:** sales concentration analysis by seller revenue
- **Thread ID:** `bc223e78-1b37-49fc-9c01-0ef5150cefba`

#### 💬 Response

```
Um total de 561 vendedores é responsável por 80% da receita. Isso indica uma concentração significativa nas vendas, onde uma parte relativamente pequena de vendedores gera a maior parte da receita total.
```

#### 📊 Metadata

- **sql:** WITH revenue_by_seller AS (SELECT oi.seller_id, SUM(oi.price + oi.freight_value) AS total_revenue FROM analytics.order_items oi JOIN analytics.orders o ON oi.order_id = o.order_id GROUP BY oi.seller_id), cumulative_revenue AS (SELECT seller_id, total_revenue, SUM(total_revenue) OVER (ORDER BY total_revenue DESC) AS cumulative_revenue FROM revenue_by_seller) SELECT COUNT(*) AS seller_count FROM cumulative_revenue WHERE cumulative_revenue <= 0.8 * (SELECT SUM(total_revenue) FROM revenue_by_seller)
- **row_count:** 1
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-17"></a>
### Query 17

#### 📝 Input

- **Query:** Calcule o churn rate de clientes por coorte de primeira compra (mês/ano)

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.9
- **Reason:** customer churn rate by first purchase cohort
- **Thread ID:** `a45a63a4-a031-4873-9cd7-95b74a128fe8`

#### 💬 Response

```
Análise do churn rate de clientes por coorte de primeira compra:

Setembro de 2016: 50,00%
Outubro de 2016: 7,41%
Dezembro de 2016: 0,00%
Janeiro de 2017: 0,38%
Fevereiro de 2017: 0,96%
Março de 2017: 1,23%
Abril de 2017: 0,75%
Maio de 2017: 0,78%
Junho de 2017: 0,49%
Julho de 2017: 0,70%
Agosto de 2017: 0,62%
Setembro de 2017: 0,47%
Outubro de 2017: 0,56%
Novembro de 2017: 0,49%
Dezembro de 2017: 0,19%
Janeiro de 2018: 0,47%
Fevereiro de 2018: 1,09%
Março de 2018: 0,36%
Abril de 2018: 0,22%
Maio de 2018: 0,35%
Junho de 2018: 0,29%
Julho de 2018: 0,65%
Agosto de 2018: 1,29%
Setembro de 2018: 93,75%
Outubro de 2018: 100,00%

O churn rate apresenta variações significativas ao longo dos meses, com picos notáveis em setembro e outubro de 2018, indicando uma possível perda massiva de clientes nesses períodos. É importante investigar as causas desses cancelamentos para implementar estratégias de retenção eficazes.
```

#### 📊 Metadata

- **sql:** WITH first_purchase AS (SELECT customer_id, date_trunc('month', order_purchase_timestamp) AS cohort_month FROM analytics.orders GROUP BY customer_id, cohort_month), churned_customers AS (SELECT fp.cohort_month, COUNT(DISTINCT o.customer_id) AS churned_count FROM first_purchase fp JOIN analytics.orders o ON fp.customer_id = o.customer_id WHERE o.order_purchase_timestamp > fp.cohort_month AND o.order_status LIKE '%cancel%' GROUP BY fp.cohort_month), total_customers AS (SELECT fp.cohort_month, COUNT(DISTINCT fp.customer_id) AS total_count FROM first_purchase fp GROUP BY fp.cohort_month) SELECT tc.cohort_month, COALESCE(ROUND(100.0 * cc.churned_count / NULLIF(tc.total_count, 0), 2), 0) AS churn_rate FROM total_customers tc LEFT JOIN churned_customers cc ON tc.cohort_month = cc.cohort_month ORDER BY tc.cohort_month
- **row_count:** 25
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-18"></a>
### Query 18

#### 📝 Input

- **Query:** Qual é o impacto do número de parcelas no valor médio do pedido e na taxa de aprovação?

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.75
- **Reason:** analysis of installments impact on order value and approval rate
- **Thread ID:** `e9828099-cb00-40da-b1e4-8a3ab2c8d5b3`

#### 💬 Response

```
Análise do impacto do número de parcelas no valor médio do pedido e na taxa de aprovação:

0 parcelas: R$ 94,32 (média), Taxa de aprovação: 0,00%
1 parcela: R$ 112,42 (média), Taxa de aprovação: 0,00%
2 parcelas: R$ 127,23 (média), Taxa de aprovação: 0,00%
3 parcelas: R$ 142,54 (média), Taxa de aprovação: 0,00%
4 parcelas: R$ 163,98 (média), Taxa de aprovação: 0,00%
5 parcelas: R$ 183,47 (média), Taxa de aprovação: 0,02%
6 parcelas: R$ 209,85 (média), Taxa de aprovação: 0,00%
7 parcelas: R$ 187,67 (média), Taxa de aprovação: 0,00%
8 parcelas: R$ 307,74 (média), Taxa de aprovação: 0,00%
9 parcelas: R$ 203,44 (média), Taxa de aprovação: 0,00%
10 parcelas: R$ 415,09 (média), Taxa de aprovação: 0,00%
11 parcelas: R$ 124,93 (média), Taxa de aprovação: 0,00%
12 parcelas: R$ 321,68 (média), Taxa de aprovação: 0,00%
13 parcelas: R$ 150,46 (média), Taxa de aprovação: 0,00%
14 parcelas: R$ 167,96 (média), Taxa de aprovação: 0,00%
15 parcelas: R$ 445,55 (média), Taxa de aprovação: 0,00%
16 parcelas: R$ 292,69 (média), Taxa de aprovação: 0,00%
17 parcelas: R$ 174,60 (média), Taxa de aprovação: 0,00%
18 parcelas: R$ 486,48 (média), Taxa de aprovação: 0,00%
20 parcelas: R$ 615,80 (média), Taxa de aprovação: 0,00%
21 parcelas: R$ 243,70 (média), Taxa de aprovação: 0,00%
22 parcelas: R$ 228,71 (média), Taxa de aprovação: 0,00%
23 parcelas: R$ 236,48 (média), Taxa de aprovação: 0,00%
24 parcelas: R$ 610,05 (média), Taxa de aprovação: 0,00%
```

#### 📊 Metadata

- **sql:** SELECT op.payment_installments, AVG(op.payment_value) AS avg_order_value, AVG(CASE WHEN o.order_status LIKE '%approved%' THEN 1 ELSE 0 END) AS approval_rate FROM analytics.order_payments op JOIN analytics.orders o ON op.order_id = o.order_id GROUP BY op.payment_installments ORDER BY op.payment_installments
- **row_count:** 24
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-19"></a>
### Query 19

#### 📝 Input

- **Query:** Identifique oportunidades de cross-selling analisando produtos frequentemente comprados juntos

#### 🎯 Classification

- **Agent:** `analytics`
- **Confidence:** 0.85
- **Reason:** analysis of product co-purchase patterns for cross-selling
- **Thread ID:** `9b8f85c7-04c0-4078-9616-5dca5fb702db`

#### 💬 Response

```
Análise de oportunidades de cross-selling com base em produtos frequentemente comprados juntos:

1. Produto A (ID: 05b515fdc76e888aada3c6d66c201dff) e Produto B (ID: 270516a3f41dc035aa87d220228f844c): 100 compras
2. Produto B (ID: 270516a3f41dc035aa87d220228f844c) e Produto A (ID: 05b515fdc76e888aada3c6d66c201dff): 100 compras
3. Produto C (ID: 36f60d45225e60c7da4558b070ce4b60) e Produto D (ID: e53e557d5a159f5aa2c5e995dfdf244b): 48 compras
4. Produto D (ID: e53e557d5a159f5aa2c5e995dfdf244b) e Produto C (ID: 36f60d45225e60c7da4558b070ce4b60): 48 compras
5. Produto E (ID: 62995b7e571f5760017991632bbfd311) e Produto F (ID: ac1ad58efc1ebf66bfadc09f29bdedc0): 36 compras
6. Produto G (ID: a9d9db064d4afd4458eb3e139fe29167) e Produto H (ID: 710b7c26b7a742f497bba45fab91a25f): 36 compras
7. Produto F (ID: ac1ad58efc1ebf66bfadc09f29bdedc0) e Produto E (ID: 62995b7e571f5760017991632bbfd311): 36 compras
8. Produto H (ID: 710b7c26b7a742f497bba45fab91a25f) e Produto G (ID: a9d9db064d4afd4458eb3e139fe29167): 36 compras
9. Produto I (ID: 53759a2ecddad2bb87a079a1f1519f73) e Produto J (ID: 2ef36e1cae01b86d0ff0a2f50ff2bd53): 30 compras
10. Produto K (ID: 308e4e21ae228a10f6370a243ae59995) e Produto L (ID: 90b58782fdd04cb829667fcc41fb65f5): 30 compras

Esses dados indicam quais produtos têm maior potencial para serem oferecidos juntos, aumentando assim as oportunidades de vendas adicionais.

Dados completos:
1. product_id_1: 05b515fdc76e888aada3c6d66c201dff, product_id_2: 270516a3f41dc035aa87d220228f844c, purchase_count: 100
2. product_id_1: 270516a3f41dc035aa87d220228f844c, product_id_2: 05b515fdc76e888aada3c6d66c201dff, purchase_count: 100
3. product_id_1: 36f60d45225e60c7da4558b070ce4b60, product_id_2: e53e557d5a159f5aa2c5e995dfdf244b, purchase_count: 48
4. product_id_1: e53e557d5a159f5aa2c5e995dfdf244b, product_id_2: 36f60d45225e60c7da4558b070ce4b60, purchase_count: 48
5. product_id_1: 62995b7e571f5760017991632bbfd311, product_id_2: ac1ad58efc1ebf66bfadc09f29bdedc0, purchase_count: 36
6. product_id_1: a9d9db064d4afd4458eb3e139fe29167, product_id_2: 710b7c26b7a742f497bba45fab91a25f, purchase_count: 36
7. product_id_1: ac1ad58efc1ebf66bfadc09f29bdedc0, product_id_2: 62995b7e571f5760017991632bbfd311, purchase_count: 36
8. product_id_1: 710b7c26b7a742f497bba45fab91a25f, product_id_2: a9d9db064d4afd4458eb3e139fe29167, purchase_count: 36
9. product_id_1: 53759a2ecddad2bb87a079a1f1519f73, product_id_2: 2ef36e1cae01b86d0ff0a2f50ff2bd53, purchase_count: 30
10. product_id_1: 308e4e21ae228a10f6370a243ae59995, product_id_2: 90b58782fdd04cb829667fcc41fb65f5, purchase_count: 30
11. product_id_1: 99a4788cb24856965c36a24e339b6058, product_id_2: 35afc973633aaeb6b877ff57b2793310, purchase_count: 30
12. product_id_1: 90b58782fdd04cb829667fcc41fb65f5, product_id_2: 308e4e21ae228a10f6370a243ae59995, purchase_count: 30
13. product_id_1: 2ef36e1cae01b86d0ff0a2f50ff2bd53, product_id_2: 53759a2ecddad2bb87a079a1f1519f73, purchase_count: 30
14. product_id_1: 35afc973633aaeb6b877ff57b2793310, product_id_2: 99a4788cb24856965c36a24e339b6058, purchase_count: 30
15. product_id_1: dbb67791e405873b259e4656bf971246, product_id_2: 18486698933fbb64af6c0a255f7dd64c, purchase_count: 26
16. product_id_1: 18486698933fbb64af6c0a255f7dd64c, product_id_2: dbb67791e405873b259e4656bf971246, purchase_count: 26
17. product_id_1: 872db866d615db59612ac933f43d6b22, product_id_2: 58efb9b638561ce132216a9a612513e2, purchase_count: 25
18. product_id_1: 58efb9b638561ce132216a9a612513e2, product_id_2: 872db866d615db59612ac933f43d6b22, purchase_count: 25
19. product_id_1: e6b314a2236c162ede1a879f1075430f, product_id_2: ad4b5def91ac7c575dbdf65b5be311f4, purchase_count: 24
20. product_id_1: 0db4869ac8a908414823d44d742f5ba3, product_id_2: 47920da896bbd89e851429c78a7a7a8b, purchase_count: 24
21. product_id_1: 54d7ad85b648d3cb2b7069ed446d7f35, product_id_2: 82758517d6c9cc65c509781f1e14e9f2, purchase_count: 24
22. product_id_1: 47920da896bbd89e851429c78a7a7a8b, product_id_2: 0db4869ac8a908414823d44d742f5ba3, purchase_count: 24
23. product_id_1: ad4b5def91ac7c575dbdf65b5be311f4, product_id_2: e6b314a2236c162ede1a879f1075430f, purchase_count: 24
24. product_id_1: 82758517d6c9cc65c509781f1e14e9f2, product_id_2: 54d7ad85b648d3cb2b7069ed446d7f35, purchase_count: 24
25. product_id_1: 389d119b48cf3043d311335e499d9c6b, product_id_2: 422879e10f46682990de24d770e7f83d, purchase_count: 19
26. product_id_1: 422879e10f46682990de24d770e7f83d, product_id_2: 389d119b48cf3043d311335e499d9c6b, purchase_count: 19
27. product_id_1: 3f14d740544f37ece8a9e7bc8349797e, product_id_2: 36f60d45225e60c7da4558b070ce4b60, purchase_count: 18
28. product_id_1: 8509049c56caff468e3f35c4eefb6035, product_id_2: ac11c132793524428ef353a3e4956ed9, purchase_count: 18
29. product_id_1: ac11c132793524428ef353a3e4956ed9, product_id_2: 8509049c56caff468e3f35c4eefb6035, purchase_count: 18
30. product_id_1: 36f60d45225e60c7da4558b070ce4b60, product_id_2: 3f14d740544f37ece8a9e7bc8349797e, purchase_count: 18
31. product_id_1: f4f67ccaece962d013a4e1d7dc3a61f7, product_id_2: 4fcb3d9a5f4871e8362dfedbdb02b064, purchase_count: 17
32. product_id_1: 422879e10f46682990de24d770e7f83d, product_id_2: 53759a2ecddad2bb87a079a1f1519f73, purchase_count: 17
33. product_id_1: 53759a2ecddad2bb87a079a1f1519f73, product_id_2: 422879e10f46682990de24d770e7f83d, purchase_count: 17
34. product_id_1: 4fcb3d9a5f4871e8362dfedbdb02b064, product_id_2: f4f67ccaece962d013a4e1d7dc3a61f7, purchase_count: 17
35. product_id_1: 33c18a3e86c00fca807265cf34354996, product_id_2: d90e83fe1a0e31440db1dc015f1c1512, purchase_count: 16
36. product_id_1: 078e8db43688ea060cf754e7bd2b92e7, product_id_2: 96d1c06692244e2fed6e1f9aa9552770, purchase_count: 16
37. product_id_1: d90e83fe1a0e31440db1dc015f1c1512, product_id_2: 33c18a3e86c00fca807265cf34354996, purchase_count: 16
38. product_id_1: 96d1c06692244e2fed6e1f9aa9552770, product_id_2: 078e8db43688ea060cf754e7bd2b92e7, purchase_count: 16
39. product_id_1: 53759a2ecddad2bb87a079a1f1519f73, product_id_2: 389d119b48cf3043d311335e499d9c6b, purchase_count: 15
40. product_id_1: c2b534c5a4a6cbfc41aeaf362fb0c060, product_id_2: 7a5b821fca01c5a75fa33c06f249e0f5, purchase_count: 15
41. product_id_1: 7a5b821fca01c5a75fa33c06f249e0f5, product_id_2: c2b534c5a4a6cbfc41aeaf362fb0c060, purchase_count: 15
42. product_id_1: 389d119b48cf3043d311335e499d9c6b, product_id_2: 53759a2ecddad2bb87a079a1f1519f73, purchase_count: 15
43. product_id_1: 0bcc3eeca39e1064258aa1e932269894, product_id_2: 422879e10f46682990de24d770e7f83d, purchase_count: 13
44. product_id_1: 422879e10f46682990de24d770e7f83d, product_id_2: 0bcc3eeca39e1064258aa1e932269894, purchase_count: 13
45. product_id_1: 1eba879220bd0981a0e2fbab499ed4e1, product_id_2: 8ed094bfe076c568f6bb10feada3f75d, purchase_count: 12
46. product_id_1: 8ed094bfe076c568f6bb10feada3f75d, product_id_2: 1eba879220bd0981a0e2fbab499ed4e1, purchase_count: 12
47. product_id_1: 61a53738adc5c0e8d243553320f9ba1c, product_id_2: 3eef0cb94ba82de806bb30ab743c7655, purchase_count: 12
48. product_id_1: 1b7ce992a80ac036dd9ab73d08289712, product_id_2: d1c427060a0f73f6b889a5c7c61f2ac4, purchase_count: 12
49. product_id_1: 3eef0cb94ba82de806bb30ab743c7655, product_id_2: 61a53738adc5c0e8d243553320f9ba1c, purchase_count: 12
50. product_id_1: d1c427060a0f73f6b889a5c7c61f2ac4, product_id_2: 1b7ce992a80ac036dd9ab73d08289712, purchase_count: 12
51. product_id_1: b8a0d73b2a06e7910d9864dccdb0cda2, product_id_2: 9bb8ca338e5588c361e34eae02e8fad6, purchase_count: 11
52. product_id_1: 9bb8ca338e5588c361e34eae02e8fad6, product_id_2: b8a0d73b2a06e7910d9864dccdb0cda2, purchase_count: 11
53. product_id_1: 79ce45dbc2ea29b22b5a261bbb7b7ee7, product_id_2: 05b515fdc76e888aada3c6d66c201dff, purchase_count: 10
54. product_id_1: b0961721fd839e9982420e807758a2a6, product_id_2: 53759a2ecddad2bb87a079a1f1519f73, purchase_count: 10
55. product_id_1: 79ce45dbc2ea29b22b5a261bbb7b7ee7, product_id_2: 270516a3f41dc035aa87d220228f844c, purchase_count: 10
56. product_id_1: d2085f7e0f9533605386960fc7e987ec, product_id_2: dbb67791e405873b259e4656bf971246, purchase_count: 10
57. product_id_1: 05b515fdc76e888aada3c6d66c201dff, product_id_2: 79ce45dbc2ea29b22b5a261bbb7b7ee7, purchase_count: 10
58. product_id_1: 53759a2ecddad2bb87a079a1f1519f73, product_id_2: 368c6c730842d78016ad823897a372db, purchase_count: 10
59. product_id_1: dbb67791e405873b259e4656bf971246, product_id_2: d2085f7e0f9533605386960fc7e987ec, purchase_count: 10
60. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: 53759a2ecddad2bb87a079a1f1519f73, purchase_count: 10
61. product_id_1: 53759a2ecddad2bb87a079a1f1519f73, product_id_2: b0961721fd839e9982420e807758a2a6, purchase_count: 10
62. product_id_1: 270516a3f41dc035aa87d220228f844c, product_id_2: 79ce45dbc2ea29b22b5a261bbb7b7ee7, purchase_count: 10
63. product_id_1: d5991653e037ccb7af6ed7d94246b249, product_id_2: 6987398dff454a3138231540e2a6ec61, purchase_count: 9
64. product_id_1: 65bb78cf0bbc3ca6406f30e6793736f9, product_id_2: 7721582bb750762d81850267d19881c1, purchase_count: 9
65. product_id_1: 0e14941c183946f60e3b86585d05f984, product_id_2: 7cefa61c9500d9b227894dc48d8b5a0b, purchase_count: 9
66. product_id_1: 3c5ba90e09547db90868e803d139de30, product_id_2: ea3da91e6ba865972f9344cb9265296b, purchase_count: 9
67. product_id_1: e0cf79767c5b016251fe139915c59a26, product_id_2: 0a4093a4af429dc0a9334300e5c13ae5, purchase_count: 9
68. product_id_1: b6ada73818651fe7e64be10653062ea2, product_id_2: 1ba4e3fe92f16fd5a8942f7b7d804b52, purchase_count: 9
69. product_id_1: b6ada73818651fe7e64be10653062ea2, product_id_2: bf44071ef18f5c9ded039681c68b1996, purchase_count: 9
70. product_id_1: 1ba4e3fe92f16fd5a8942f7b7d804b52, product_id_2: b6ada73818651fe7e64be10653062ea2, purchase_count: 9
71. product_id_1: b6ada73818651fe7e64be10653062ea2, product_id_2: e11092e9722d1b6f8c18cd8947a1daff, purchase_count: 9
72. product_id_1: 3d85e85bcd2c0315e0db407db8f7b532, product_id_2: 5526b1ae9ab2688cf600783cece249df, purchase_count: 9
73. product_id_1: ef66e63137bdd1b2e44aa968646fc1e3, product_id_2: 281a67fd770c975ee1a7c842468fb3b5, purchase_count: 9
74. product_id_1: 1ba4e3fe92f16fd5a8942f7b7d804b52, product_id_2: e11092e9722d1b6f8c18cd8947a1daff, purchase_count: 9
75. product_id_1: 1ba4e3fe92f16fd5a8942f7b7d804b52, product_id_2: bf44071ef18f5c9ded039681c68b1996, purchase_count: 9
76. product_id_1: 5526b1ae9ab2688cf600783cece249df, product_id_2: 3d85e85bcd2c0315e0db407db8f7b532, purchase_count: 9
77. product_id_1: 281a67fd770c975ee1a7c842468fb3b5, product_id_2: ef66e63137bdd1b2e44aa968646fc1e3, purchase_count: 9
78. product_id_1: ea3da91e6ba865972f9344cb9265296b, product_id_2: 3c5ba90e09547db90868e803d139de30, purchase_count: 9
79. product_id_1: e11092e9722d1b6f8c18cd8947a1daff, product_id_2: 1ba4e3fe92f16fd5a8942f7b7d804b52, purchase_count: 9
80. product_id_1: 0a4093a4af429dc0a9334300e5c13ae5, product_id_2: e0cf79767c5b016251fe139915c59a26, purchase_count: 9
81. product_id_1: e11092e9722d1b6f8c18cd8947a1daff, product_id_2: b6ada73818651fe7e64be10653062ea2, purchase_count: 9
82. product_id_1: bf44071ef18f5c9ded039681c68b1996, product_id_2: e11092e9722d1b6f8c18cd8947a1daff, purchase_count: 9
83. product_id_1: bf44071ef18f5c9ded039681c68b1996, product_id_2: b6ada73818651fe7e64be10653062ea2, purchase_count: 9
84. product_id_1: bf44071ef18f5c9ded039681c68b1996, product_id_2: 1ba4e3fe92f16fd5a8942f7b7d804b52, purchase_count: 9
85. product_id_1: e11092e9722d1b6f8c18cd8947a1daff, product_id_2: bf44071ef18f5c9ded039681c68b1996, purchase_count: 9
86. product_id_1: ead3077a141a9c800d6a4bb9d0d415b6, product_id_2: b072511d69a5b161d8e80815898ed960, purchase_count: 9
87. product_id_1: 3713f19c71c4be21ced80738e2fa49bc, product_id_2: 508d5e8ce8e79bb506f9f0c096b295c4, purchase_count: 9
88. product_id_1: 508d5e8ce8e79bb506f9f0c096b295c4, product_id_2: 3713f19c71c4be21ced80738e2fa49bc, purchase_count: 9
89. product_id_1: 6987398dff454a3138231540e2a6ec61, product_id_2: d5991653e037ccb7af6ed7d94246b249, purchase_count: 9
90. product_id_1: b072511d69a5b161d8e80815898ed960, product_id_2: ead3077a141a9c800d6a4bb9d0d415b6, purchase_count: 9
91. product_id_1: 057df564fda79ad8fa5e1928dfbe3e8c, product_id_2: e8ca14b6c60a3194f2353bbfe0287bbe, purchase_count: 9
92. product_id_1: 7cefa61c9500d9b227894dc48d8b5a0b, product_id_2: 0e14941c183946f60e3b86585d05f984, purchase_count: 9
93. product_id_1: e8ca14b6c60a3194f2353bbfe0287bbe, product_id_2: 057df564fda79ad8fa5e1928dfbe3e8c, purchase_count: 9
94. product_id_1: 7721582bb750762d81850267d19881c1, product_id_2: 65bb78cf0bbc3ca6406f30e6793736f9, purchase_count: 9
95. product_id_1: 5fc3e6a4b52b0c414458104ed4037f1c, product_id_2: 5d790355cbeded0cd60e25cbc4c527a2, purchase_count: 8
96. product_id_1: 6d1338fc8d6ac273115ea526c7a6146a, product_id_2: d2f2c2b94c6ac44ece0bd0dd202c7939, purchase_count: 8
97. product_id_1: 703d742887bb9267f89b675608ba7aa0, product_id_2: 688ad0169550f8e2eb0307b61df3ba12, purchase_count: 8
98. product_id_1: 9ad35a49eb5a417d1554e1c23f8200e4, product_id_2: 15c507fd1d486501a97bd53f82445f1e, purchase_count: 8
99. product_id_1: bff2390f68a7b76b01ef61b684888261, product_id_2: d9e7d13814ea50f9ae1f612ef6b3a1f1, purchase_count: 8
100. product_id_1: d9e7d13814ea50f9ae1f612ef6b3a1f1, product_id_2: bff2390f68a7b76b01ef61b684888261, purchase_count: 8
101. product_id_1: 8bb27b1d96be90b36b8d0c7f30931d52, product_id_2: a03e401d58a45187271718c5d7610422, purchase_count: 8
102. product_id_1: 416753943bbda356a28be0f3ba476632, product_id_2: 0ad6795586afdad1281b3884f2611ca6, purchase_count: 8
103. product_id_1: 0ad6795586afdad1281b3884f2611ca6, product_id_2: 416753943bbda356a28be0f3ba476632, purchase_count: 8
104. product_id_1: 5d790355cbeded0cd60e25cbc4c527a2, product_id_2: 5fc3e6a4b52b0c414458104ed4037f1c, purchase_count: 8
105. product_id_1: d2f2c2b94c6ac44ece0bd0dd202c7939, product_id_2: 6d1338fc8d6ac273115ea526c7a6146a, purchase_count: 8
106. product_id_1: 688ad0169550f8e2eb0307b61df3ba12, product_id_2: 703d742887bb9267f89b675608ba7aa0, purchase_count: 8
107. product_id_1: a03e401d58a45187271718c5d7610422, product_id_2: 8bb27b1d96be90b36b8d0c7f30931d52, purchase_count: 8
108. product_id_1: 15c507fd1d486501a97bd53f82445f1e, product_id_2: 9ad35a49eb5a417d1554e1c23f8200e4, purchase_count: 8
109. product_id_1: 7d00a7c029fe3cf2bddc1e8e0484c2c1, product_id_2: cec51758e9839eb5414b214934430da6, purchase_count: 8
110. product_id_1: cec51758e9839eb5414b214934430da6, product_id_2: 7d00a7c029fe3cf2bddc1e8e0484c2c1, purchase_count: 8
111. product_id_1: b0c89945c034268074f5f80b362bda34, product_id_2: ff2c1ec09b1bb340e84f0d6b21cc7dbb, purchase_count: 7
112. product_id_1: 0bcc3eeca39e1064258aa1e932269894, product_id_2: 368c6c730842d78016ad823897a372db, purchase_count: 7
113. product_id_1: 53759a2ecddad2bb87a079a1f1519f73, product_id_2: 0bcc3eeca39e1064258aa1e932269894, purchase_count: 7
114. product_id_1: 0bcc3eeca39e1064258aa1e932269894, product_id_2: b0961721fd839e9982420e807758a2a6, purchase_count: 7
115. product_id_1: b0961721fd839e9982420e807758a2a6, product_id_2: 0bcc3eeca39e1064258aa1e932269894, purchase_count: 7
116. product_id_1: 0bcc3eeca39e1064258aa1e932269894, product_id_2: 53759a2ecddad2bb87a079a1f1519f73, purchase_count: 7
117. product_id_1: ff2c1ec09b1bb340e84f0d6b21cc7dbb, product_id_2: b0c89945c034268074f5f80b362bda34, purchase_count: 7
118. product_id_1: 0bcc3eeca39e1064258aa1e932269894, product_id_2: 389d119b48cf3043d311335e499d9c6b, purchase_count: 7
119. product_id_1: 5b8a5a9417210b1b84b67b9a7aefb935, product_id_2: e5ae72c62ebfa708624f5029d609b160, purchase_count: 7
120. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: 0bcc3eeca39e1064258aa1e932269894, purchase_count: 7
121. product_id_1: e5ae72c62ebfa708624f5029d609b160, product_id_2: 5b8a5a9417210b1b84b67b9a7aefb935, purchase_count: 7
122. product_id_1: 389d119b48cf3043d311335e499d9c6b, product_id_2: 0bcc3eeca39e1064258aa1e932269894, purchase_count: 7
123. product_id_1: d25bbb182b51d1594fe3b54a27ae143e, product_id_2: 399f54c06661d06ca45c6e24ed238e0e, purchase_count: 6
124. product_id_1: 3c7c75671b25b927f05e68b233263e5f, product_id_2: 83e2059df06602e05d9bc1abf28166ac, purchase_count: 6
125. product_id_1: 399f54c06661d06ca45c6e24ed238e0e, product_id_2: d25bbb182b51d1594fe3b54a27ae143e, purchase_count: 6
126. product_id_1: 399f54c06661d06ca45c6e24ed238e0e, product_id_2: e95fb3a80ca294f39de925b6428f3a32, purchase_count: 6
127. product_id_1: a0498bf8b8ff0c35a6b8c736a71526ab, product_id_2: b5661cf46c147805adc83695fb04f487, purchase_count: 6
128. product_id_1: 3ebbc0870d51b62783c45e0e61ccb78d, product_id_2: e9b3cf27d68caa64832c4a7c460abcb9, purchase_count: 6
129. product_id_1: ad0a798e7941f3a5a2fb8139cb62ad78, product_id_2: 946344697156947d846d27fe0d503033, purchase_count: 6
130. product_id_1: fc5bf9e50dbfb45e7634bd8c045411c5, product_id_2: 01422266d7a3131403364787ef9dab11, purchase_count: 6
131. product_id_1: 389d119b48cf3043d311335e499d9c6b, product_id_2: 368c6c730842d78016ad823897a372db, purchase_count: 6
132. product_id_1: b0961721fd839e9982420e807758a2a6, product_id_2: 422879e10f46682990de24d770e7f83d, purchase_count: 6
133. product_id_1: 66e9fb73e349cba44b29951e558a6780, product_id_2: 574597aaf385996112490308e37399ce, purchase_count: 6
134. product_id_1: d315b738a6e96f4d9710af966cb7cd5b, product_id_2: f04c24eaa43e9192315d3aa0b3f00c1c, purchase_count: 6
135. product_id_1: 5a2c5357841ae997771d179eee3f2027, product_id_2: 279d5c3589fceee2a1c236fbe5287975, purchase_count: 6
136. product_id_1: 829b1d3da6a5e54d51055338281a5dfe, product_id_2: 7248b99ff380f23a1094ff737a1112fb, purchase_count: 6
137. product_id_1: 83e2059df06602e05d9bc1abf28166ac, product_id_2: 3c7c75671b25b927f05e68b233263e5f, purchase_count: 6
138. product_id_1: f2e53dd1670f3c376518263b3f71424d, product_id_2: 99a4788cb24856965c36a24e339b6058, purchase_count: 6
139. product_id_1: 389d119b48cf3043d311335e499d9c6b, product_id_2: 680874c570dad71c0a2844cfbf417054, purchase_count: 6
140. product_id_1: 3ebbc0870d51b62783c45e0e61ccb78d, product_id_2: 3bb3e5caf47c7e92ed97227247e942a8, purchase_count: 6
141. product_id_1: a50acd33ba7a8da8e9db65094fa990a4, product_id_2: dfb97c88e066dc22165f31648efe1312, purchase_count: 6
142. product_id_1: 01422266d7a3131403364787ef9dab11, product_id_2: fc5bf9e50dbfb45e7634bd8c045411c5, purchase_count: 6
143. product_id_1: 399f54c06661d06ca45c6e24ed238e0e, product_id_2: 99444c1e11fc38755dae86f5c67d3d1a, purchase_count: 6
144. product_id_1: d2085f7e0f9533605386960fc7e987ec, product_id_2: 18486698933fbb64af6c0a255f7dd64c, purchase_count: 6
145. product_id_1: e8ca14b6c60a3194f2353bbfe0287bbe, product_id_2: 3685c687db4b3d2da5085d23b408e93a, purchase_count: 6
146. product_id_1: 9ad75bd7267e5c724cb42c71ac56ca72, product_id_2: 4d0ec1e9b95fb62f9a1fbe21808bf3b1, purchase_count: 6
147. product_id_1: 3685c687db4b3d2da5085d23b408e93a, product_id_2: e8ca14b6c60a3194f2353bbfe0287bbe, purchase_count: 6
148. product_id_1: f04c24eaa43e9192315d3aa0b3f00c1c, product_id_2: d315b738a6e96f4d9710af966cb7cd5b, purchase_count: 6
149. product_id_1: 7248b99ff380f23a1094ff737a1112fb, product_id_2: 829b1d3da6a5e54d51055338281a5dfe, purchase_count: 6
150. product_id_1: 060cb19345d90064d1015407193c233d, product_id_2: 98d61056e0568ba048e5d78038790e77, purchase_count: 6
151. product_id_1: 946344697156947d846d27fe0d503033, product_id_2: ad0a798e7941f3a5a2fb8139cb62ad78, purchase_count: 6
152. product_id_1: 1bb0f142789375f5709d08b2f2355c2b, product_id_2: 193cea27ec2ebc61c91cf7dd70420fad, purchase_count: 6
153. product_id_1: ee57070aa3b24a06fdd0e02efd2d757d, product_id_2: 0d85c435fd60b277ffb9e9b0f88f927a, purchase_count: 6
154. product_id_1: 4d0ec1e9b95fb62f9a1fbe21808bf3b1, product_id_2: 9ad75bd7267e5c724cb42c71ac56ca72, purchase_count: 6
155. product_id_1: 04cb9679db724268544436f40166c3ed, product_id_2: 74a86d4a9f05585758fcf89d91f9d378, purchase_count: 6
156. product_id_1: 99444c1e11fc38755dae86f5c67d3d1a, product_id_2: 399f54c06661d06ca45c6e24ed238e0e, purchase_count: 6
157. product_id_1: c9c6fde711572c1ad99ca12728c6af00, product_id_2: 31c79131e883e5fd8c4c85fe9f7d2bb2, purchase_count: 6
158. product_id_1: 143c616ec3fe0cb065c3805cf9bd812e, product_id_2: 33c4b54c2a3e60ac5beb217d833d9f52, purchase_count: 6
159. product_id_1: 680874c570dad71c0a2844cfbf417054, product_id_2: 389d119b48cf3043d311335e499d9c6b, purchase_count: 6
160. product_id_1: b0c89945c034268074f5f80b362bda34, product_id_2: ad0a798e7941f3a5a2fb8139cb62ad78, purchase_count: 6
161. product_id_1: c403e106353e1aa40efe783ecb39ed7a, product_id_2: 35afc973633aaeb6b877ff57b2793310, purchase_count: 6
162. product_id_1: ad0a798e7941f3a5a2fb8139cb62ad78, product_id_2: b0c89945c034268074f5f80b362bda34, purchase_count: 6
163. product_id_1: 74a86d4a9f05585758fcf89d91f9d378, product_id_2: 04cb9679db724268544436f40166c3ed, purchase_count: 6
164. product_id_1: 1c27515baa5bece76d41e2353efcdd8e, product_id_2: b5661cf46c147805adc83695fb04f487, purchase_count: 6
165. product_id_1: e3b5a4c3f8512fe1315f05564e461ff4, product_id_2: bc055ae94989497c0d66bfa4263ccf61, purchase_count: 6
166. product_id_1: b5661cf46c147805adc83695fb04f487, product_id_2: 1c27515baa5bece76d41e2353efcdd8e, purchase_count: 6
167. product_id_1: f7c3fc384cd3ac71650982c2c6fcbe77, product_id_2: fd5c5a67cd369732c2ac20dbd574d1d4, purchase_count: 6
168. product_id_1: 422879e10f46682990de24d770e7f83d, product_id_2: b0961721fd839e9982420e807758a2a6, purchase_count: 6
169. product_id_1: 18486698933fbb64af6c0a255f7dd64c, product_id_2: d2085f7e0f9533605386960fc7e987ec, purchase_count: 6
170. product_id_1: bc055ae94989497c0d66bfa4263ccf61, product_id_2: e3b5a4c3f8512fe1315f05564e461ff4, purchase_count: 6
171. product_id_1: 35afc973633aaeb6b877ff57b2793310, product_id_2: c403e106353e1aa40efe783ecb39ed7a, purchase_count: 6
172. product_id_1: e9b3cf27d68caa64832c4a7c460abcb9, product_id_2: 3ebbc0870d51b62783c45e0e61ccb78d, purchase_count: 6
173. product_id_1: 279d5c3589fceee2a1c236fbe5287975, product_id_2: 5a2c5357841ae997771d179eee3f2027, purchase_count: 6
174. product_id_1: b5661cf46c147805adc83695fb04f487, product_id_2: a0498bf8b8ff0c35a6b8c736a71526ab, purchase_count: 6
175. product_id_1: 99a4788cb24856965c36a24e339b6058, product_id_2: f2e53dd1670f3c376518263b3f71424d, purchase_count: 6
176. product_id_1: fd5c5a67cd369732c2ac20dbd574d1d4, product_id_2: f7c3fc384cd3ac71650982c2c6fcbe77, purchase_count: 6
177. product_id_1: e95fb3a80ca294f39de925b6428f3a32, product_id_2: 399f54c06661d06ca45c6e24ed238e0e, purchase_count: 6
178. product_id_1: 98d61056e0568ba048e5d78038790e77, product_id_2: 060cb19345d90064d1015407193c233d, purchase_count: 6
179. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: 389d119b48cf3043d311335e499d9c6b, purchase_count: 6
180. product_id_1: 3bb3e5caf47c7e92ed97227247e942a8, product_id_2: 3ebbc0870d51b62783c45e0e61ccb78d, purchase_count: 6
181. product_id_1: 33c4b54c2a3e60ac5beb217d833d9f52, product_id_2: 143c616ec3fe0cb065c3805cf9bd812e, purchase_count: 6
182. product_id_1: 0d85c435fd60b277ffb9e9b0f88f927a, product_id_2: ee57070aa3b24a06fdd0e02efd2d757d, purchase_count: 6
183. product_id_1: 193cea27ec2ebc61c91cf7dd70420fad, product_id_2: 1bb0f142789375f5709d08b2f2355c2b, purchase_count: 6
184. product_id_1: 56b83ac081e4e6ea5f87323b4e46e85c, product_id_2: a87567bdce60de6f901e3d7c6d8df820, purchase_count: 6
185. product_id_1: a87567bdce60de6f901e3d7c6d8df820, product_id_2: 56b83ac081e4e6ea5f87323b4e46e85c, purchase_count: 6
186. product_id_1: dfb97c88e066dc22165f31648efe1312, product_id_2: a50acd33ba7a8da8e9db65094fa990a4, purchase_count: 6
187. product_id_1: 574597aaf385996112490308e37399ce, product_id_2: 66e9fb73e349cba44b29951e558a6780, purchase_count: 6
188. product_id_1: 31c79131e883e5fd8c4c85fe9f7d2bb2, product_id_2: c9c6fde711572c1ad99ca12728c6af00, purchase_count: 6
189. product_id_1: 9ad75bd7267e5c724cb42c71ac56ca72, product_id_2: 665aa1d687284a4d2d2b74c0c6724625, purchase_count: 5
190. product_id_1: a06766fec51c96d4d0bce282906735eb, product_id_2: c18dfe3165eaa55de9ec8f462cd7556f, purchase_count: 5
191. product_id_1: b7d94dc0640c7025dc8e3b46b52d8239, product_id_2: 3ce943997ff85cad84ec6770b35d6bcd, purchase_count: 5
192. product_id_1: 6e423c2d28bfb207e1fd1d6e1df84721, product_id_2: fbc1488c1a1e72ba175f53ab29a248e8, purchase_count: 5
193. product_id_1: 67fc455b96e0908bc5e0d917237b2977, product_id_2: 155815f7173905f1e5cde0b82adfc113, purchase_count: 5
194. product_id_1: 0aabfb375647d9738ad0f7b4ea3653b1, product_id_2: 6c3effec7c8ddba466d4f03f982c7aa3, purchase_count: 5
195. product_id_1: c18dfe3165eaa55de9ec8f462cd7556f, product_id_2: a06766fec51c96d4d0bce282906735eb, purchase_count: 5
196. product_id_1: 7c68e7297c7df2535c9f0dcd61007f64, product_id_2: 9b169f20f1b0ad0cd0d53d6d5f12e20f, purchase_count: 5
197. product_id_1: ab1ecbce7afd9f6e661baa24a5706c9c, product_id_2: e5433d154f98bcb2c139b9679fce0814, purchase_count: 5
198. product_id_1: 3ce943997ff85cad84ec6770b35d6bcd, product_id_2: b7d94dc0640c7025dc8e3b46b52d8239, purchase_count: 5
199. product_id_1: 1600dcf1cea8c0c83702e07b577ab231, product_id_2: e57eb018e37376580079825eb29a3419, purchase_count: 5
200. product_id_1: 665aa1d687284a4d2d2b74c0c6724625, product_id_2: 9ad75bd7267e5c724cb42c71ac56ca72, purchase_count: 5
201. product_id_1: 6c3effec7c8ddba466d4f03f982c7aa3, product_id_2: 0aabfb375647d9738ad0f7b4ea3653b1, purchase_count: 5
202. product_id_1: fbc1488c1a1e72ba175f53ab29a248e8, product_id_2: 6e423c2d28bfb207e1fd1d6e1df84721, purchase_count: 5
203. product_id_1: e57eb018e37376580079825eb29a3419, product_id_2: 1600dcf1cea8c0c83702e07b577ab231, purchase_count: 5
204. product_id_1: e5433d154f98bcb2c139b9679fce0814, product_id_2: ab1ecbce7afd9f6e661baa24a5706c9c, purchase_count: 5
205. product_id_1: 155815f7173905f1e5cde0b82adfc113, product_id_2: 67fc455b96e0908bc5e0d917237b2977, purchase_count: 5
206. product_id_1: 9b169f20f1b0ad0cd0d53d6d5f12e20f, product_id_2: 7c68e7297c7df2535c9f0dcd61007f64, purchase_count: 5
207. product_id_1: cdea4f41e1d54465e44bbe45a31fc69b, product_id_2: eb9a3adbcce4a03f2ea0394ec01a58ad, purchase_count: 4
208. product_id_1: ee3cfb33869693f2a7e8417c795d8cfc, product_id_2: bbd704063c23164b2674e893ac58d63b, purchase_count: 4
209. product_id_1: 6789e81c62b672bf413759d22ecacaf7, product_id_2: 073a5dfc26cb33ef440b2e0aa29343a8, purchase_count: 4
210. product_id_1: 6789e81c62b672bf413759d22ecacaf7, product_id_2: 200eed7d1d3482898094819dbec1cb52, purchase_count: 4
211. product_id_1: 86f024d3bdcdb9b54c9fffd92be39f54, product_id_2: 40cb7bb3d30559b9b6c4fb62bc837962, purchase_count: 4
212. product_id_1: 9b7852df1a77c9a80cf5151803db4282, product_id_2: 525d023cea7235fd59133983cc5269bf, purchase_count: 4
213. product_id_1: 9b7852df1a77c9a80cf5151803db4282, product_id_2: 8043608c406d413f7f645257cdc33f73, purchase_count: 4
214. product_id_1: 86f2416d4670e4ea3ca5494d043d9f24, product_id_2: 508d5e8ce8e79bb506f9f0c096b295c4, purchase_count: 4
215. product_id_1: 93d8b11d613a563f5a26212282bb145e, product_id_2: 38e19855caf485b504d6f33ed31a9eb4, purchase_count: 4
216. product_id_1: d678178aa4291cd25a755a90188375c8, product_id_2: 2ae5ed1d99afbb14a8b24041a81df16b, purchase_count: 4
217. product_id_1: 871cfa7d587b8305a5a0e376866323ef, product_id_2: 181b31b11ea16a87d5acab5a78320b93, purchase_count: 4
218. product_id_1: 871cfa7d587b8305a5a0e376866323ef, product_id_2: 5554c5718f820a868853dbc5ca859b3b, purchase_count: 4
219. product_id_1: 93d8b11d613a563f5a26212282bb145e, product_id_2: acebea1efbaa063642166633d247aec7, purchase_count: 4
220. product_id_1: 200eed7d1d3482898094819dbec1cb52, product_id_2: 073a5dfc26cb33ef440b2e0aa29343a8, purchase_count: 4
221. product_id_1: 64fb265487de2238627ce43fe8a67efc, product_id_2: 84f456958365164420cfc80fbe4c7fab, purchase_count: 4
222. product_id_1: 873eb5f3b8cc503730e472a14cd26616, product_id_2: 0e14941c183946f60e3b86585d05f984, purchase_count: 4
223. product_id_1: 52d5dde0ddeb4e7544b584c92a38fef8, product_id_2: 67cee25aae565b8f1182ea8c37440103, purchase_count: 4
224. product_id_1: 429e7401fafb76436f15e86498bd7364, product_id_2: 41da75141264c3bde21ecea85a4cb8b7, purchase_count: 4
225. product_id_1: c55fe8cbb36a1353e443dc9e773b80da, product_id_2: 10990aaa402c4692f9eb94cbc354e53c, purchase_count: 4
226. product_id_1: bbd704063c23164b2674e893ac58d63b, product_id_2: ee3cfb33869693f2a7e8417c795d8cfc, purchase_count: 4
227. product_id_1: 200eed7d1d3482898094819dbec1cb52, product_id_2: 6789e81c62b672bf413759d22ecacaf7, purchase_count: 4
228. product_id_1: 38e19855caf485b504d6f33ed31a9eb4, product_id_2: 93d8b11d613a563f5a26212282bb145e, purchase_count: 4
229. product_id_1: 67cee25aae565b8f1182ea8c37440103, product_id_2: 52d5dde0ddeb4e7544b584c92a38fef8, purchase_count: 4
230. product_id_1: 38e19855caf485b504d6f33ed31a9eb4, product_id_2: acebea1efbaa063642166633d247aec7, purchase_count: 4
231. product_id_1: d9e7d13814ea50f9ae1f612ef6b3a1f1, product_id_2: 91472a5abca63bed91ade04c71c203ce, purchase_count: 4
232. product_id_1: 8043608c406d413f7f645257cdc33f73, product_id_2: 525d023cea7235fd59133983cc5269bf, purchase_count: 4
233. product_id_1: 8043608c406d413f7f645257cdc33f73, product_id_2: 9b7852df1a77c9a80cf5151803db4282, purchase_count: 4
234. product_id_1: 5526b1ae9ab2688cf600783cece249df, product_id_2: 1427b126f61597524866770b05d4eed2, purchase_count: 4
235. product_id_1: 67fc455b96e0908bc5e0d917237b2977, product_id_2: 08ef02b6aae73ad3a385cf1342f609c7, purchase_count: 4
236. product_id_1: e5f8f7fec18736ea009f2f7334543497, product_id_2: 84f47b7ffbd21c845d197cc0a7bc479a, purchase_count: 4
237. product_id_1: 67fc455b96e0908bc5e0d917237b2977, product_id_2: 3d870b8af7dbdc91b10cfb0139f3d44d, purchase_count: 4
238. product_id_1: 40cb7bb3d30559b9b6c4fb62bc837962, product_id_2: 86f024d3bdcdb9b54c9fffd92be39f54, purchase_count: 4
239. product_id_1: 924260f2993f33c639e6226173f07e8f, product_id_2: 5eae236b07a8c5db6299c7f9c3ba2e6e, purchase_count: 4
240. product_id_1: 43ee88561093499d9e571d4db5f20b79, product_id_2: 8aa6223e400af9c97b07c75993142721, purchase_count: 4
241. product_id_1: 93e6c730cc84ef7cfdd20cdfb2269144, product_id_2: a0f3c43b288de04ccb40d26cf26c639d, purchase_count: 4
242. product_id_1: 0bcc3eeca39e1064258aa1e932269894, product_id_2: 4b5df063d69ffafb87c279672ecb4191, purchase_count: 4
243. product_id_1: dea564fb3ed59db512cb4df9c491c1ef, product_id_2: d191e54bd50ba045ac5bc9336572886f, purchase_count: 4
244. product_id_1: 553e0e7590d3116a072507a3635d2877, product_id_2: adc48fd26eea311ca6856b58dfc3ca21, purchase_count: 4
245. product_id_1: f2e53dd1670f3c376518263b3f71424d, product_id_2: 35afc973633aaeb6b877ff57b2793310, purchase_count: 4
246. product_id_1: 1dc7685f4fdb9622d84ae2ec658d5bbf, product_id_2: e256d05115f9eb3766f3ab752132a4e2, purchase_count: 4
247. product_id_1: 5554c5718f820a868853dbc5ca859b3b, product_id_2: 181b31b11ea16a87d5acab5a78320b93, purchase_count: 4
248. product_id_1: 5554c5718f820a868853dbc5ca859b3b, product_id_2: 871cfa7d587b8305a5a0e376866323ef, purchase_count: 4
249. product_id_1: 810e2944bca9850b934e1570ba372e7d, product_id_2: 5d6bea33648f018dbb563f3a2fab09f3, purchase_count: 4
250. product_id_1: 3d870b8af7dbdc91b10cfb0139f3d44d, product_id_2: 08ef02b6aae73ad3a385cf1342f609c7, purchase_count: 4
251. product_id_1: 3d870b8af7dbdc91b10cfb0139f3d44d, product_id_2: 155815f7173905f1e5cde0b82adfc113, purchase_count: 4
252. product_id_1: 3d870b8af7dbdc91b10cfb0139f3d44d, product_id_2: 67fc455b96e0908bc5e0d917237b2977, purchase_count: 4
253. product_id_1: a5647c44af977b148e0a3a4751a09e2e, product_id_2: d6fe3b4ddecd4a8393c6a1385de3bfb6, purchase_count: 4
254. product_id_1: 812f428f6757ab16c46cffc68f2e90c5, product_id_2: cc3e0004237b0c02f8fd95f943e1cebf, purchase_count: 4
255. product_id_1: 00ba6d766f0b1d7b78a5ce3e1e033263, product_id_2: ff95ac47246ef13e48712ea1ff8df0d9, purchase_count: 4
256. product_id_1: c857b96593773e940454e76efa8eabb3, product_id_2: 9fc98e39f04be8e382d8aa5e259f5489, purchase_count: 4
257. product_id_1: 216bfe821826c195bf9da55b12a6c296, product_id_2: cadb69af336c16aba5c5223599821245, purchase_count: 4
258. product_id_1: 10990aaa402c4692f9eb94cbc354e53c, product_id_2: c55fe8cbb36a1353e443dc9e773b80da, purchase_count: 4
259. product_id_1: 8973d773c115b9e347c34a248f17bc92, product_id_2: 32bb152336c896d906a6344cdbe1993c, purchase_count: 4
260. product_id_1: 91472a5abca63bed91ade04c71c203ce, product_id_2: d9e7d13814ea50f9ae1f612ef6b3a1f1, purchase_count: 4
261. product_id_1: 5aad359a63cbb4fc35ead44346a3eeb4, product_id_2: 2548af3e6e77a690cf3eb6368e9ab61e, purchase_count: 4
262. product_id_1: 924c635d837c240da3956f3c28c1e6f4, product_id_2: bfa8fb32cecbf90899f6f517b77a766f, purchase_count: 4
263. product_id_1: 7703b8cb5b77fbb36518ea91e2ca734f, product_id_2: 186fe07c8b8005ec6a498587ffbc1352, purchase_count: 4
264. product_id_1: 7a0f37fda63d1cd7dac2451494eb6e69, product_id_2: 665aa1d687284a4d2d2b74c0c6724625, purchase_count: 4
265. product_id_1: f4d705aa95ccca448e5b0deb6e5290ba, product_id_2: c211ff3068fcd2f8898192976d8b3a32, purchase_count: 4
266. product_id_1: a79e27ad902bfc67386ea63ed1ef7a08, product_id_2: 16d096faa27582985f849f08370cf1ed, purchase_count: 4
267. product_id_1: 41da75141264c3bde21ecea85a4cb8b7, product_id_2: 429e7401fafb76436f15e86498bd7364, purchase_count: 4
268. product_id_1: 8aa6223e400af9c97b07c75993142721, product_id_2: 43ee88561093499d9e571d4db5f20b79, purchase_count: 4
269. product_id_1: 0fa81e7123fd0ebe03adbbe99d912827, product_id_2: fb783e3e545937820b57fe539b2c5a6c, purchase_count: 4
270. product_id_1: 99444c1e11fc38755dae86f5c67d3d1a, product_id_2: d25bbb182b51d1594fe3b54a27ae143e, purchase_count: 4
271. product_id_1: 4b5df063d69ffafb87c279672ecb4191, product_id_2: 0bcc3eeca39e1064258aa1e932269894, purchase_count: 4
272. product_id_1: adc48fd26eea311ca6856b58dfc3ca21, product_id_2: 553e0e7590d3116a072507a3635d2877, purchase_count: 4
273. product_id_1: 99444c1e11fc38755dae86f5c67d3d1a, product_id_2: e95fb3a80ca294f39de925b6428f3a32, purchase_count: 4
274. product_id_1: 027325f946f1b3d8f94c3496e9a59a10, product_id_2: 482c25dc8512547962854dfff5ac057b, purchase_count: 4
275. product_id_1: cadb69af336c16aba5c5223599821245, product_id_2: 216bfe821826c195bf9da55b12a6c296, purchase_count: 4
276. product_id_1: 1bfb290d7273a442c874dbe74b4abae6, product_id_2: 3eef0cb94ba82de806bb30ab743c7655, purchase_count: 4
277. product_id_1: 378f61e89b6c50bd26a0a74c6ca046f0, product_id_2: a9490f0e069790ddb7d8e7935ea3584a, purchase_count: 4
278. product_id_1: 205cf43d203186d5eb440a791a5b7404, product_id_2: f908d3bf313a1308bfb2a46ea2685347, purchase_count: 4
279. product_id_1: d6fe3b4ddecd4a8393c6a1385de3bfb6, product_id_2: a5647c44af977b148e0a3a4751a09e2e, purchase_count: 4
280. product_id_1: 1f792af77962621fcc80d95c2897bb19, product_id_2: 8c6d562d9dde3d9658cf7496f61c1bc0, purchase_count: 4
281. product_id_1: 2548af3e6e77a690cf3eb6368e9ab61e, product_id_2: 140a8324a66db81d299b24b30d93098e, purchase_count: 4
282. product_id_1: 2548af3e6e77a690cf3eb6368e9ab61e, product_id_2: 5aad359a63cbb4fc35ead44346a3eeb4, purchase_count: 4
283. product_id_1: e95fb3a80ca294f39de925b6428f3a32, product_id_2: 99444c1e11fc38755dae86f5c67d3d1a, purchase_count: 4
284. product_id_1: e95fb3a80ca294f39de925b6428f3a32, product_id_2: d25bbb182b51d1594fe3b54a27ae143e, purchase_count: 4
285. product_id_1: e9b3cf27d68caa64832c4a7c460abcb9, product_id_2: 3bb3e5caf47c7e92ed97227247e942a8, purchase_count: 4
286. product_id_1: 38021cef829efa264df6f9d21c4df6e9, product_id_2: d7a3cfa08519494aa1ad181e803617ec, purchase_count: 4
287. product_id_1: 0de59eddc63167215c972b0d785ffa7b, product_id_2: 309dd69eb83cea38c51709d62befe1a4, purchase_count: 4
288. product_id_1: cc3e0004237b0c02f8fd95f943e1cebf, product_id_2: 812f428f6757ab16c46cffc68f2e90c5, purchase_count: 4
289. product_id_1: a8eed0daf7e2db5e074d2d4f65046946, product_id_2: a8f6fefd2f6ad22952337438aa1bfce5, purchase_count: 4
290. product_id_1: a8f6fefd2f6ad22952337438aa1bfce5, product_id_2: a8eed0daf7e2db5e074d2d4f65046946, purchase_count: 4
291. product_id_1: 1c27515baa5bece76d41e2353efcdd8e, product_id_2: a0498bf8b8ff0c35a6b8c736a71526ab, purchase_count: 4
292. product_id_1: 5c5585c687a0293f10bb748c13cacc71, product_id_2: 4e58e4bd671d463cef30fa0bab322f9a, purchase_count: 4
293. product_id_1: 2265e8aa066cc6c4528d4be900eb5b64, product_id_2: 4275f85d0173354d8ca336b70a87aa6a, purchase_count: 4
294. product_id_1: b88d27345de2feed45475bb48cca74b1, product_id_2: ff6caf9340512b8bf6d2a2a6df032cfa, purchase_count: 4
295. product_id_1: a9490f0e069790ddb7d8e7935ea3584a, product_id_2: 378f61e89b6c50bd26a0a74c6ca046f0, purchase_count: 4
296. product_id_1: 32bb152336c896d906a6344cdbe1993c, product_id_2: 8973d773c115b9e347c34a248f17bc92, purchase_count: 4
297. product_id_1: 155815f7173905f1e5cde0b82adfc113, product_id_2: 08ef02b6aae73ad3a385cf1342f609c7, purchase_count: 4
298. product_id_1: 155815f7173905f1e5cde0b82adfc113, product_id_2: 3d870b8af7dbdc91b10cfb0139f3d44d, purchase_count: 4
299. product_id_1: 181b31b11ea16a87d5acab5a78320b93, product_id_2: 5554c5718f820a868853dbc5ca859b3b, purchase_count: 4
300. product_id_1: 8c6d562d9dde3d9658cf7496f61c1bc0, product_id_2: 1f792af77962621fcc80d95c2897bb19, purchase_count: 4
301. product_id_1: 16d096faa27582985f849f08370cf1ed, product_id_2: a79e27ad902bfc67386ea63ed1ef7a08, purchase_count: 4
302. product_id_1: f908d3bf313a1308bfb2a46ea2685347, product_id_2: 205cf43d203186d5eb440a791a5b7404, purchase_count: 4
303. product_id_1: bfa8fb32cecbf90899f6f517b77a766f, product_id_2: 924c635d837c240da3956f3c28c1e6f4, purchase_count: 4
304. product_id_1: 3eef0cb94ba82de806bb30ab743c7655, product_id_2: 1bfb290d7273a442c874dbe74b4abae6, purchase_count: 4
305. product_id_1: 2ced45a3059cbb128a8b8b6508809746, product_id_2: 662276c22ed1b925786d19da6677e19d, purchase_count: 4
306. product_id_1: 060f0122cdc8f25db4a0d7359fdae7b0, product_id_2: 57f2bc497c1a3ebe41ba7a06d78ed159, purchase_count: 4
307. product_id_1: d7a3cfa08519494aa1ad181e803617ec, product_id_2: 38021cef829efa264df6f9d21c4df6e9, purchase_count: 4
308. product_id_1: 181b31b11ea16a87d5acab5a78320b93, product_id_2: 871cfa7d587b8305a5a0e376866323ef, purchase_count: 4
309. product_id_1: 173255396ec907ab516d3848dbcc98da, product_id_2: 30ac6df06dc59ad72cf2f158fc2d904c, purchase_count: 4
310. product_id_1: 073a5dfc26cb33ef440b2e0aa29343a8, product_id_2: 200eed7d1d3482898094819dbec1cb52, purchase_count: 4
311. product_id_1: 9fc98e39f04be8e382d8aa5e259f5489, product_id_2: c857b96593773e940454e76efa8eabb3, purchase_count: 4
312. product_id_1: 12760bcacfaaf1457bc36e601e26dc79, product_id_2: 83fb98f2457985e6333f2e307adc5864, purchase_count: 4
313. product_id_1: 662276c22ed1b925786d19da6677e19d, product_id_2: 2ced45a3059cbb128a8b8b6508809746, purchase_count: 4
314. product_id_1: 1d3f55c00acdb29bd959f2760abc8b7d, product_id_2: 0c9ff9d8ed9b9bdd825487b3a66e05f5, purchase_count: 4
315. product_id_1: 8378dd5a08699f8c95ea6f6c147d4e83, product_id_2: 609c35bf8122d5ab8186ed7a6bfcd843, purchase_count: 4
316. product_id_1: fb783e3e545937820b57fe539b2c5a6c, product_id_2: 0fa81e7123fd0ebe03adbbe99d912827, purchase_count: 4
317. product_id_1: 337c81a0f9e751b6cbdf56680a33c365, product_id_2: 6bb50785f82871dde37ed1666da54bf3, purchase_count: 4
318. product_id_1: 35afc973633aaeb6b877ff57b2793310, product_id_2: f2e53dd1670f3c376518263b3f71424d, purchase_count: 4
319. product_id_1: 08ef02b6aae73ad3a385cf1342f609c7, product_id_2: 155815f7173905f1e5cde0b82adfc113, purchase_count: 4
320. product_id_1: 2ae5ed1d99afbb14a8b24041a81df16b, product_id_2: d678178aa4291cd25a755a90188375c8, purchase_count: 4
321. product_id_1: e256d05115f9eb3766f3ab752132a4e2, product_id_2: 1dc7685f4fdb9622d84ae2ec658d5bbf, purchase_count: 4
322. product_id_1: 6bb50785f82871dde37ed1666da54bf3, product_id_2: 337c81a0f9e751b6cbdf56680a33c365, purchase_count: 4
323. product_id_1: 073a5dfc26cb33ef440b2e0aa29343a8, product_id_2: 6789e81c62b672bf413759d22ecacaf7, purchase_count: 4
324. product_id_1: 525d023cea7235fd59133983cc5269bf, product_id_2: 8043608c406d413f7f645257cdc33f73, purchase_count: 4
325. product_id_1: 609c35bf8122d5ab8186ed7a6bfcd843, product_id_2: 8378dd5a08699f8c95ea6f6c147d4e83, purchase_count: 4
326. product_id_1: 5d6bea33648f018dbb563f3a2fab09f3, product_id_2: 810e2944bca9850b934e1570ba372e7d, purchase_count: 4
327. product_id_1: 0e14941c183946f60e3b86585d05f984, product_id_2: 873eb5f3b8cc503730e472a14cd26616, purchase_count: 4
328. product_id_1: a0498bf8b8ff0c35a6b8c736a71526ab, product_id_2: 1c27515baa5bece76d41e2353efcdd8e, purchase_count: 4
329. product_id_1: 5d6bea33648f018dbb563f3a2fab09f3, product_id_2: 9ada4c8f4e072df42ff63b30520b6975, purchase_count: 4
330. product_id_1: eb9a3adbcce4a03f2ea0394ec01a58ad, product_id_2: cdea4f41e1d54465e44bbe45a31fc69b, purchase_count: 4
331. product_id_1: cfe6e9c01d0bbb5df9a75f0e3286baa9, product_id_2: 7893c68e0a8b6e58a70390551e8a84d9, purchase_count: 4
332. product_id_1: 4275f85d0173354d8ca336b70a87aa6a, product_id_2: 2265e8aa066cc6c4528d4be900eb5b64, purchase_count: 4
333. product_id_1: 525d023cea7235fd59133983cc5269bf, product_id_2: 9b7852df1a77c9a80cf5151803db4282, purchase_count: 4
334. product_id_1: 5eae236b07a8c5db6299c7f9c3ba2e6e, product_id_2: 924260f2993f33c639e6226173f07e8f, purchase_count: 4
335. product_id_1: 140a8324a66db81d299b24b30d93098e, product_id_2: 2548af3e6e77a690cf3eb6368e9ab61e, purchase_count: 4
336. product_id_1: 08ef02b6aae73ad3a385cf1342f609c7, product_id_2: 3d870b8af7dbdc91b10cfb0139f3d44d, purchase_count: 4
337. product_id_1: 08ef02b6aae73ad3a385cf1342f609c7, product_id_2: 67fc455b96e0908bc5e0d917237b2977, purchase_count: 4
338. product_id_1: 83fb98f2457985e6333f2e307adc5864, product_id_2: 12760bcacfaaf1457bc36e601e26dc79, purchase_count: 4
339. product_id_1: 665aa1d687284a4d2d2b74c0c6724625, product_id_2: 7a0f37fda63d1cd7dac2451494eb6e69, purchase_count: 4
340. product_id_1: 0c9ff9d8ed9b9bdd825487b3a66e05f5, product_id_2: 1d3f55c00acdb29bd959f2760abc8b7d, purchase_count: 4
341. product_id_1: 186fe07c8b8005ec6a498587ffbc1352, product_id_2: 7703b8cb5b77fbb36518ea91e2ca734f, purchase_count: 4
342. product_id_1: d05bb6074b45c20f7a516c239c0a1c43, product_id_2: 9ad35a49eb5a417d1554e1c23f8200e4, purchase_count: 4
343. product_id_1: 1427b126f61597524866770b05d4eed2, product_id_2: 5526b1ae9ab2688cf600783cece249df, purchase_count: 4
344. product_id_1: 57f2bc497c1a3ebe41ba7a06d78ed159, product_id_2: 060f0122cdc8f25db4a0d7359fdae7b0, purchase_count: 4
345. product_id_1: c211ff3068fcd2f8898192976d8b3a32, product_id_2: f4d705aa95ccca448e5b0deb6e5290ba, purchase_count: 4
346. product_id_1: 9ad35a49eb5a417d1554e1c23f8200e4, product_id_2: d05bb6074b45c20f7a516c239c0a1c43, purchase_count: 4
347. product_id_1: 482c25dc8512547962854dfff5ac057b, product_id_2: 027325f946f1b3d8f94c3496e9a59a10, purchase_count: 4
348. product_id_1: a0f3c43b288de04ccb40d26cf26c639d, product_id_2: 93e6c730cc84ef7cfdd20cdfb2269144, purchase_count: 4
349. product_id_1: d191e54bd50ba045ac5bc9336572886f, product_id_2: dea564fb3ed59db512cb4df9c491c1ef, purchase_count: 4
350. product_id_1: 84f456958365164420cfc80fbe4c7fab, product_id_2: 64fb265487de2238627ce43fe8a67efc, purchase_count: 4
351. product_id_1: 3bb3e5caf47c7e92ed97227247e942a8, product_id_2: e9b3cf27d68caa64832c4a7c460abcb9, purchase_count: 4
352. product_id_1: 84f47b7ffbd21c845d197cc0a7bc479a, product_id_2: e5f8f7fec18736ea009f2f7334543497, purchase_count: 4
353. product_id_1: 4e58e4bd671d463cef30fa0bab322f9a, product_id_2: 5c5585c687a0293f10bb748c13cacc71, purchase_count: 4
354. product_id_1: 309dd69eb83cea38c51709d62befe1a4, product_id_2: 0de59eddc63167215c972b0d785ffa7b, purchase_count: 4
355. product_id_1: 9ada4c8f4e072df42ff63b30520b6975, product_id_2: 5d6bea33648f018dbb563f3a2fab09f3, purchase_count: 4
356. product_id_1: acebea1efbaa063642166633d247aec7, product_id_2: 38e19855caf485b504d6f33ed31a9eb4, purchase_count: 4
357. product_id_1: acebea1efbaa063642166633d247aec7, product_id_2: 93d8b11d613a563f5a26212282bb145e, purchase_count: 4
358. product_id_1: 7893c68e0a8b6e58a70390551e8a84d9, product_id_2: cfe6e9c01d0bbb5df9a75f0e3286baa9, purchase_count: 4
359. product_id_1: ff6caf9340512b8bf6d2a2a6df032cfa, product_id_2: b88d27345de2feed45475bb48cca74b1, purchase_count: 4
360. product_id_1: 30ac6df06dc59ad72cf2f158fc2d904c, product_id_2: 173255396ec907ab516d3848dbcc98da, purchase_count: 4
361. product_id_1: ff95ac47246ef13e48712ea1ff8df0d9, product_id_2: 00ba6d766f0b1d7b78a5ce3e1e033263, purchase_count: 4
362. product_id_1: 508d5e8ce8e79bb506f9f0c096b295c4, product_id_2: 86f2416d4670e4ea3ca5494d043d9f24, purchase_count: 4
363. product_id_1: d25bbb182b51d1594fe3b54a27ae143e, product_id_2: 99444c1e11fc38755dae86f5c67d3d1a, purchase_count: 4
364. product_id_1: d25bbb182b51d1594fe3b54a27ae143e, product_id_2: e95fb3a80ca294f39de925b6428f3a32, purchase_count: 4
365. product_id_1: 786733d317255508bd4d648585977611, product_id_2: 7b83c11ac78f11bde67542beb12e8163, purchase_count: 3
366. product_id_1: effa78286556d5e79cda2b4aba96a534, product_id_2: cfb133b7458336455fa60b97ac3aaba9, purchase_count: 3
367. product_id_1: 134a6fc4a713a799266ebd6a4f4008d4, product_id_2: 2bd57c183094130d215a333ea80c8b62, purchase_count: 3
368. product_id_1: 2136c70bbe723d338fab53da3c03e6dc, product_id_2: 5c692818d313aa12864b48ac0c2472c2, purchase_count: 3
369. product_id_1: f40876e0ef3cd5f9132b1f16b04b1346, product_id_2: 9bb8ca338e5588c361e34eae02e8fad6, purchase_count: 3
370. product_id_1: 0dce4f5243207cc33533e133b634ae5f, product_id_2: 58b365b0859f884f4d07490d902af193, purchase_count: 3
371. product_id_1: 7c1bd920dbdf22470b68bde975dd3ccf, product_id_2: 154e7e31ebfa092203795c972e5804a6, purchase_count: 3
372. product_id_1: 643a66b1dc5dad3de6cb5a41549e72f1, product_id_2: c5cb254d666e4420d56b5dc67ff59d29, purchase_count: 3
373. product_id_1: 5d61fa9714218b033b42ca6cbf0f2570, product_id_2: 0d9cceec564febe77a44f8123dc2279b, purchase_count: 3
374. product_id_1: be127a8a979cd5d591ea345f10bba28c, product_id_2: 3eb2d78dda82bc83c9b047fbba954dbe, purchase_count: 3
375. product_id_1: 09b0d15a8cc9a84e7af7e0225f67dc45, product_id_2: 066cc58255ee9ccb3e6da9d3edd02a7e, purchase_count: 3
376. product_id_1: 55bfa0307d7a46bed72c492259921231, product_id_2: e2cac69b319c0f8a21dbf04b925121bf, purchase_count: 3
377. product_id_1: 55bfa0307d7a46bed72c492259921231, product_id_2: b9900407a55cb2b306ae612415c3340e, purchase_count: 3
378. product_id_1: 0437850bd55b9b2b9cf104b59a611666, product_id_2: fedbf77eb491dfc9ac276b9ea9ee10c6, purchase_count: 3
379. product_id_1: a02d0123079f4ae96001ba2010d1a2df, product_id_2: 924c635d837c240da3956f3c28c1e6f4, purchase_count: 3
380. product_id_1: a62e25e09e05e6faf31d90c6ec1aa3d1, product_id_2: 368c6c730842d78016ad823897a372db, purchase_count: 3
381. product_id_1: ed38e11473775cde0d65f698aa0a4d27, product_id_2: 7b83c11ac78f11bde67542beb12e8163, purchase_count: 3
382. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: a62e25e09e05e6faf31d90c6ec1aa3d1, purchase_count: 3
383. product_id_1: cf54cbfe4e33bc8f7b34a65da576497c, product_id_2: c403e106353e1aa40efe783ecb39ed7a, purchase_count: 3
384. product_id_1: 2e5bddcf20a946aad0394cf0a62743f4, product_id_2: 0294e314a033317e28ecc40aee9025e8, purchase_count: 3
385. product_id_1: 924c635d837c240da3956f3c28c1e6f4, product_id_2: a02d0123079f4ae96001ba2010d1a2df, purchase_count: 3
386. product_id_1: bb90206fa281c20f0b4c42a2393b54dd, product_id_2: a3f487d2926f4af42e86454a8ec474c1, purchase_count: 3
387. product_id_1: 87590844d536e6b92ecf707a50b1c2c5, product_id_2: 092eff69a9499b052a2258f502ea0775, purchase_count: 3
388. product_id_1: fedbf77eb491dfc9ac276b9ea9ee10c6, product_id_2: 0437850bd55b9b2b9cf104b59a611666, purchase_count: 3
389. product_id_1: f3720bc68555b1bff49b9ffd41b017ac, product_id_2: d5991653e037ccb7af6ed7d94246b249, purchase_count: 3
390. product_id_1: 9beabf555d105ca84a74570e39e64852, product_id_2: 2c0c951471371afa81e47d7bf8d20522, purchase_count: 3
391. product_id_1: b9900407a55cb2b306ae612415c3340e, product_id_2: 55bfa0307d7a46bed72c492259921231, purchase_count: 3
392. product_id_1: cfb133b7458336455fa60b97ac3aaba9, product_id_2: effa78286556d5e79cda2b4aba96a534, purchase_count: 3
393. product_id_1: eb8c629f70275fd1c4f809116cce1efc, product_id_2: dc4f0da054d6a37385d337699c7ab043, purchase_count: 3
394. product_id_1: 8d944f9367ba7f153e0ab5b6dc7d063b, product_id_2: 73f835584b88d706c12bb3e9298a733c, purchase_count: 3
395. product_id_1: e3e6af2b9a779d64b3589a5b56102d16, product_id_2: 597d26435e8ef77bb0fcd26f6c07d486, purchase_count: 3
396. product_id_1: 7b83c11ac78f11bde67542beb12e8163, product_id_2: ed38e11473775cde0d65f698aa0a4d27, purchase_count: 3
397. product_id_1: e3e6af2b9a779d64b3589a5b56102d16, product_id_2: ca140156f7f81f8e406cc66cb8f12a67, purchase_count: 3
398. product_id_1: d1c427060a0f73f6b889a5c7c61f2ac4, product_id_2: c4baedd846ed09b85f78a781b522f126, purchase_count: 3
399. product_id_1: 55610b8b7d48294e69fc23f513dfbe98, product_id_2: a0ed74d31fcb470d85786e7f17794599, purchase_count: 3
400. product_id_1: 58b365b0859f884f4d07490d902af193, product_id_2: 0dce4f5243207cc33533e133b634ae5f, purchase_count: 3
401. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: a5341e3f8155dbb3e62323d3ea289729, purchase_count: 3
402. product_id_1: fc5dd987f12a7b823a76a44aa1ba88f6, product_id_2: 07ffc018eaf23e086370dea42c74077b, purchase_count: 3
403. product_id_1: a5341e3f8155dbb3e62323d3ea289729, product_id_2: 368c6c730842d78016ad823897a372db, purchase_count: 3
404. product_id_1: 4006da5107400e5ac48dbcc829a36c42, product_id_2: 3c7c75671b25b927f05e68b233263e5f, purchase_count: 3
405. product_id_1: fc5dd987f12a7b823a76a44aa1ba88f6, product_id_2: 7eaf66aca1ed54df09b3c864b7416110, purchase_count: 3
406. product_id_1: 480be8d20c4b6a7df1eae0f2c17f2db2, product_id_2: 0cfc9fea40ee0f7006d150fbdf3fa808, purchase_count: 3
407. product_id_1: 3c7c75671b25b927f05e68b233263e5f, product_id_2: 281905b21f01db1009fd7c01b10dd1d4, purchase_count: 3
408. product_id_1: b9900407a55cb2b306ae612415c3340e, product_id_2: e2cac69b319c0f8a21dbf04b925121bf, purchase_count: 3
409. product_id_1: 98b22c1129886cbd7fcae69d1c93e442, product_id_2: 42a2bd596fda1baef5719cb74f73030c, purchase_count: 3
410. product_id_1: f2ecbb02b6da187a9f14b8ac5781faec, product_id_2: 017692475c1c954ff597feda05131d73, purchase_count: 3
411. product_id_1: 2c0c951471371afa81e47d7bf8d20522, product_id_2: 9beabf555d105ca84a74570e39e64852, purchase_count: 3
412. product_id_1: a06766fec51c96d4d0bce282906735eb, product_id_2: 8b45810da2ef9860496d56f62435fc40, purchase_count: 3
413. product_id_1: 6549e167bd865197f8bc7ce7f82aec55, product_id_2: ca5f4739dfdcd4d73b210a344b426076, purchase_count: 3
414. product_id_1: 9bb8ca338e5588c361e34eae02e8fad6, product_id_2: f40876e0ef3cd5f9132b1f16b04b1346, purchase_count: 3
415. product_id_1: 400e2ea46d0af06d91c744b624ed8a59, product_id_2: ecbe1ef7e2903ff8b1d704ba78fa264d, purchase_count: 3
416. product_id_1: c4baedd846ed09b85f78a781b522f126, product_id_2: d1c427060a0f73f6b889a5c7c61f2ac4, purchase_count: 3
417. product_id_1: 59536eeb13a52ef81966f81b91fb481e, product_id_2: 7001d71d1ad858e07e5a341649412e76, purchase_count: 3
418. product_id_1: 3c7c75671b25b927f05e68b233263e5f, product_id_2: 4006da5107400e5ac48dbcc829a36c42, purchase_count: 3
419. product_id_1: 399f54c06661d06ca45c6e24ed238e0e, product_id_2: 6a0713a63e990052795623e76cc2995e, purchase_count: 3
420. product_id_1: e2cac69b319c0f8a21dbf04b925121bf, product_id_2: 55bfa0307d7a46bed72c492259921231, purchase_count: 3
421. product_id_1: 399f54c06661d06ca45c6e24ed238e0e, product_id_2: 17d8b8e9c21ec0fc5b33724e32fe422e, purchase_count: 3
422. product_id_1: e2cac69b319c0f8a21dbf04b925121bf, product_id_2: b9900407a55cb2b306ae612415c3340e, purchase_count: 3
423. product_id_1: 7b83c11ac78f11bde67542beb12e8163, product_id_2: 786733d317255508bd4d648585977611, purchase_count: 3
424. product_id_1: 553e0e7590d3116a072507a3635d2877, product_id_2: 33489f0140308d65c48a7659b05bdba1, purchase_count: 3
425. product_id_1: a2a91fe6d8762e0371abd964cef88ec6, product_id_2: 100260bf9206d859dc8db128c8c5afc9, purchase_count: 3
426. product_id_1: 092eff69a9499b052a2258f502ea0775, product_id_2: 87590844d536e6b92ecf707a50b1c2c5, purchase_count: 3
427. product_id_1: 0294e314a033317e28ecc40aee9025e8, product_id_2: 2e5bddcf20a946aad0394cf0a62743f4, purchase_count: 3
428. product_id_1: 2136c70bbe723d338fab53da3c03e6dc, product_id_2: a84d0660dbffebf352aefbf1a6b18d00, purchase_count: 3
429. product_id_1: 2d27434c710806b971a721da337a112a, product_id_2: 86c43103446290e7efacad3701cd654d, purchase_count: 3
430. product_id_1: 07ffc018eaf23e086370dea42c74077b, product_id_2: fc5dd987f12a7b823a76a44aa1ba88f6, purchase_count: 3
431. product_id_1: a2a1a65832c02f8a82d82c12aa0dbea9, product_id_2: fd91e23b4465803725f329b39afe018a, purchase_count: 3
432. product_id_1: c45d02cc82cd779835094de9b29272cb, product_id_2: 4e3550b4ebca5e32ccc3d32b3470e31f, purchase_count: 3
433. product_id_1: 0d9cceec564febe77a44f8123dc2279b, product_id_2: 5d61fa9714218b033b42ca6cbf0f2570, purchase_count: 3
434. product_id_1: 976738868bdcc86e959ba2a7b726d4d5, product_id_2: db61ac5970110fba38fe6caf8844dbf5, purchase_count: 3
435. product_id_1: c6e513054b982283c1cbbb2a45d02d83, product_id_2: c5cb254d666e4420d56b5dc67ff59d29, purchase_count: 3
436. product_id_1: 40263263ca0cba325e7d97ada30b8dc6, product_id_2: ed00a8453145186b3f071f1e3edef33d, purchase_count: 3
437. product_id_1: 6d2fde7d12bb6ff367dbda120ba8828e, product_id_2: fb29f48bfea41db52e349454f433340e, purchase_count: 3
438. product_id_1: 42a2bd596fda1baef5719cb74f73030c, product_id_2: 98b22c1129886cbd7fcae69d1c93e442, purchase_count: 3
439. product_id_1: 73f835584b88d706c12bb3e9298a733c, product_id_2: 8d944f9367ba7f153e0ab5b6dc7d063b, purchase_count: 3
440. product_id_1: 42a2bd596fda1baef5719cb74f73030c, product_id_2: 3cc4b421c1f28dd22e86fc4aaafb600e, purchase_count: 3
441. product_id_1: c6336fa91fbd87c359e44f5dca5a90ed, product_id_2: b584de1994f604fa7dfd0b6b9c6c1b99, purchase_count: 3
442. product_id_1: a3f487d2926f4af42e86454a8ec474c1, product_id_2: bb90206fa281c20f0b4c42a2393b54dd, purchase_count: 3
443. product_id_1: a0ed74d31fcb470d85786e7f17794599, product_id_2: 55610b8b7d48294e69fc23f513dfbe98, purchase_count: 3
444. product_id_1: 7eaf66aca1ed54df09b3c864b7416110, product_id_2: fc5dd987f12a7b823a76a44aa1ba88f6, purchase_count: 3
445. product_id_1: 422879e10f46682990de24d770e7f83d, product_id_2: 368c6c730842d78016ad823897a372db, purchase_count: 3
446. product_id_1: 87d780fa7d2cf3710aa02dc4ca8db985, product_id_2: 8a443635fdf9759915c9be5be2e3b862, purchase_count: 3
447. product_id_1: e5897f494af72d083f3899808f341659, product_id_2: fa814ebf85f1640b2acea3c4378d40f9, purchase_count: 3
448. product_id_1: e5897f494af72d083f3899808f341659, product_id_2: d40ab3a40d37ebabeaf061efefb4a40d, purchase_count: 3
449. product_id_1: fd91e23b4465803725f329b39afe018a, product_id_2: a2a1a65832c02f8a82d82c12aa0dbea9, purchase_count: 3
450. product_id_1: 100260bf9206d859dc8db128c8c5afc9, product_id_2: a2a91fe6d8762e0371abd964cef88ec6, purchase_count: 3
451. product_id_1: 4ed8030b452688a37d26044e966eff12, product_id_2: e5897f494af72d083f3899808f341659, purchase_count: 3
452. product_id_1: 4e3550b4ebca5e32ccc3d32b3470e31f, product_id_2: c45d02cc82cd779835094de9b29272cb, purchase_count: 3
453. product_id_1: c5cb254d666e4420d56b5dc67ff59d29, product_id_2: c6e513054b982283c1cbbb2a45d02d83, purchase_count: 3
454. product_id_1: eebbed5ed3b134eceb717496c47652ba, product_id_2: 99a4788cb24856965c36a24e339b6058, purchase_count: 3
455. product_id_1: 4f88323d03ffaf090b8fb0116b33c95e, product_id_2: 3e5201fe0d1ba474d9b90152c83c706c, purchase_count: 3
456. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: 27c0cea4dc76549f5bd124d9cad0ae3b, purchase_count: 3
457. product_id_1: ecbe1ef7e2903ff8b1d704ba78fa264d, product_id_2: 400e2ea46d0af06d91c744b624ed8a59, purchase_count: 3
458. product_id_1: c403e106353e1aa40efe783ecb39ed7a, product_id_2: cf54cbfe4e33bc8f7b34a65da576497c, purchase_count: 3
459. product_id_1: c5cb254d666e4420d56b5dc67ff59d29, product_id_2: 643a66b1dc5dad3de6cb5a41549e72f1, purchase_count: 3
460. product_id_1: 8f2c823e12d58a9eec1a9191e3c34718, product_id_2: b2083bcfc8768380dd0e31d612e96d08, purchase_count: 3
461. product_id_1: b6cefe1d620b9208fe6fae76b2c72887, product_id_2: aa0568a1b7093748a1922993f5817983, purchase_count: 3
462. product_id_1: 017692475c1c954ff597feda05131d73, product_id_2: f2ecbb02b6da187a9f14b8ac5781faec, purchase_count: 3
463. product_id_1: ea413ac4e120d19ac3473fb659db1c9a, product_id_2: 368c6c730842d78016ad823897a372db, purchase_count: 3
464. product_id_1: 3eb2d78dda82bc83c9b047fbba954dbe, product_id_2: be127a8a979cd5d591ea345f10bba28c, purchase_count: 3
465. product_id_1: 5c692818d313aa12864b48ac0c2472c2, product_id_2: 2136c70bbe723d338fab53da3c03e6dc, purchase_count: 3
466. product_id_1: 0cfc9fea40ee0f7006d150fbdf3fa808, product_id_2: 480be8d20c4b6a7df1eae0f2c17f2db2, purchase_count: 3
467. product_id_1: db61ac5970110fba38fe6caf8844dbf5, product_id_2: 976738868bdcc86e959ba2a7b726d4d5, purchase_count: 3
468. product_id_1: f8077831f3c3f393fb67b93c5acd8daf, product_id_2: f04c24eaa43e9192315d3aa0b3f00c1c, purchase_count: 3
469. product_id_1: 56cdfe67fbda57c1dcc752f5f361f981, product_id_2: e53e557d5a159f5aa2c5e995dfdf244b, purchase_count: 3
470. product_id_1: 2078312a2dcf1fcd8a38eabcf5dd033a, product_id_2: 05cd024f2c54923c3396db4156fdaa44, purchase_count: 3
471. product_id_1: c403e106353e1aa40efe783ecb39ed7a, product_id_2: 9fc98e39f04be8e382d8aa5e259f5489, purchase_count: 3
472. product_id_1: 09b0d15a8cc9a84e7af7e0225f67dc45, product_id_2: 4cceacaeb21aa22aa51b4c724de3758d, purchase_count: 3
473. product_id_1: 17d8b8e9c21ec0fc5b33724e32fe422e, product_id_2: 399f54c06661d06ca45c6e24ed238e0e, purchase_count: 3
474. product_id_1: 6a0713a63e990052795623e76cc2995e, product_id_2: 399f54c06661d06ca45c6e24ed238e0e, purchase_count: 3
475. product_id_1: 8b51c6ccc9c0548c951214e1cd1547ff, product_id_2: 5bd7e57735a44e529bf066fee83a9c60, purchase_count: 3
476. product_id_1: 0be487faac01dd57fd7ed17cfbdf2dee, product_id_2: 4d272fe20c57c64dc74b3db191fc31ef, purchase_count: 3
477. product_id_1: b0c89945c034268074f5f80b362bda34, product_id_2: 946344697156947d846d27fe0d503033, purchase_count: 3
478. product_id_1: 8b45810da2ef9860496d56f62435fc40, product_id_2: a06766fec51c96d4d0bce282906735eb, purchase_count: 3
479. product_id_1: 5bd7e57735a44e529bf066fee83a9c60, product_id_2: 8b51c6ccc9c0548c951214e1cd1547ff, purchase_count: 3
480. product_id_1: aa0568a1b7093748a1922993f5817983, product_id_2: b6cefe1d620b9208fe6fae76b2c72887, purchase_count: 3
481. product_id_1: 066cc58255ee9ccb3e6da9d3edd02a7e, product_id_2: 09b0d15a8cc9a84e7af7e0225f67dc45, purchase_count: 3
482. product_id_1: 3e5201fe0d1ba474d9b90152c83c706c, product_id_2: 4f88323d03ffaf090b8fb0116b33c95e, purchase_count: 3
483. product_id_1: a84d0660dbffebf352aefbf1a6b18d00, product_id_2: 2136c70bbe723d338fab53da3c03e6dc, purchase_count: 3
484. product_id_1: 703d742887bb9267f89b675608ba7aa0, product_id_2: 7d2e5a2c70a96151cd14274d426589d5, purchase_count: 3
485. product_id_1: 3e5201fe0d1ba474d9b90152c83c706c, product_id_2: 056d012d264624accb7f73d31caee034, purchase_count: 3
486. product_id_1: b584de1994f604fa7dfd0b6b9c6c1b99, product_id_2: c6336fa91fbd87c359e44f5dca5a90ed, purchase_count: 3
487. product_id_1: 7001d71d1ad858e07e5a341649412e76, product_id_2: 59536eeb13a52ef81966f81b91fb481e, purchase_count: 3
488. product_id_1: 99a4788cb24856965c36a24e339b6058, product_id_2: eebbed5ed3b134eceb717496c47652ba, purchase_count: 3
489. product_id_1: 4cceacaeb21aa22aa51b4c724de3758d, product_id_2: 09b0d15a8cc9a84e7af7e0225f67dc45, purchase_count: 3
490. product_id_1: b2083bcfc8768380dd0e31d612e96d08, product_id_2: 8f2c823e12d58a9eec1a9191e3c34718, purchase_count: 3
491. product_id_1: fa814ebf85f1640b2acea3c4378d40f9, product_id_2: e5897f494af72d083f3899808f341659, purchase_count: 3
492. product_id_1: 154e7e31ebfa092203795c972e5804a6, product_id_2: 7c1bd920dbdf22470b68bde975dd3ccf, purchase_count: 3
493. product_id_1: e5897f494af72d083f3899808f341659, product_id_2: 4ed8030b452688a37d26044e966eff12, purchase_count: 3
494. product_id_1: 056d012d264624accb7f73d31caee034, product_id_2: 3e5201fe0d1ba474d9b90152c83c706c, purchase_count: 3
495. product_id_1: 27c0cea4dc76549f5bd124d9cad0ae3b, product_id_2: 368c6c730842d78016ad823897a372db, purchase_count: 3
496. product_id_1: 9fc98e39f04be8e382d8aa5e259f5489, product_id_2: c403e106353e1aa40efe783ecb39ed7a, purchase_count: 3
497. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: 422879e10f46682990de24d770e7f83d, purchase_count: 3
498. product_id_1: 33489f0140308d65c48a7659b05bdba1, product_id_2: 553e0e7590d3116a072507a3635d2877, purchase_count: 3
499. product_id_1: 3cc4b421c1f28dd22e86fc4aaafb600e, product_id_2: 42a2bd596fda1baef5719cb74f73030c, purchase_count: 3
500. product_id_1: 597d26435e8ef77bb0fcd26f6c07d486, product_id_2: e3e6af2b9a779d64b3589a5b56102d16, purchase_count: 3
501. product_id_1: ca5f4739dfdcd4d73b210a344b426076, product_id_2: 6549e167bd865197f8bc7ce7f82aec55, purchase_count: 3
502. product_id_1: 7d2e5a2c70a96151cd14274d426589d5, product_id_2: 703d742887bb9267f89b675608ba7aa0, purchase_count: 3
503. product_id_1: d5991653e037ccb7af6ed7d94246b249, product_id_2: f3720bc68555b1bff49b9ffd41b017ac, purchase_count: 3
504. product_id_1: ca140156f7f81f8e406cc66cb8f12a67, product_id_2: e3e6af2b9a779d64b3589a5b56102d16, purchase_count: 3
505. product_id_1: fb29f48bfea41db52e349454f433340e, product_id_2: 6d2fde7d12bb6ff367dbda120ba8828e, purchase_count: 3
506. product_id_1: 946344697156947d846d27fe0d503033, product_id_2: b0c89945c034268074f5f80b362bda34, purchase_count: 3
507. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: ea413ac4e120d19ac3473fb659db1c9a, purchase_count: 3
508. product_id_1: 9fe67dbcc33795d7fafe354d7c850115, product_id_2: 3e00f726a0e1eab8f2ae5137bf9bf54a, purchase_count: 3
509. product_id_1: d40ab3a40d37ebabeaf061efefb4a40d, product_id_2: e5897f494af72d083f3899808f341659, purchase_count: 3
510. product_id_1: dc4f0da054d6a37385d337699c7ab043, product_id_2: eb8c629f70275fd1c4f809116cce1efc, purchase_count: 3
511. product_id_1: ed00a8453145186b3f071f1e3edef33d, product_id_2: 40263263ca0cba325e7d97ada30b8dc6, purchase_count: 3
512. product_id_1: fb55982be901439613a95940feefd9ee, product_id_2: 058b372f969b59e8c4a27e224243909c, purchase_count: 3
513. product_id_1: 05cd024f2c54923c3396db4156fdaa44, product_id_2: 2078312a2dcf1fcd8a38eabcf5dd033a, purchase_count: 3
514. product_id_1: 86c43103446290e7efacad3701cd654d, product_id_2: 2d27434c710806b971a721da337a112a, purchase_count: 3
515. product_id_1: 8a443635fdf9759915c9be5be2e3b862, product_id_2: 87d780fa7d2cf3710aa02dc4ca8db985, purchase_count: 3
516. product_id_1: e53e557d5a159f5aa2c5e995dfdf244b, product_id_2: 56cdfe67fbda57c1dcc752f5f361f981, purchase_count: 3
517. product_id_1: 2bd57c183094130d215a333ea80c8b62, product_id_2: 134a6fc4a713a799266ebd6a4f4008d4, purchase_count: 3
518. product_id_1: 281905b21f01db1009fd7c01b10dd1d4, product_id_2: 3c7c75671b25b927f05e68b233263e5f, purchase_count: 3
519. product_id_1: 3e00f726a0e1eab8f2ae5137bf9bf54a, product_id_2: 9fe67dbcc33795d7fafe354d7c850115, purchase_count: 3
520. product_id_1: f04c24eaa43e9192315d3aa0b3f00c1c, product_id_2: f8077831f3c3f393fb67b93c5acd8daf, purchase_count: 3
521. product_id_1: 4d272fe20c57c64dc74b3db191fc31ef, product_id_2: 0be487faac01dd57fd7ed17cfbdf2dee, purchase_count: 3
522. product_id_1: 058b372f969b59e8c4a27e224243909c, product_id_2: fb55982be901439613a95940feefd9ee, purchase_count: 3
523. product_id_1: c2ece64199af7a53793ed9612a89a8cd, product_id_2: d3e112316bd3ae29280cec26bd3059fd, purchase_count: 2
524. product_id_1: 309dd69eb83cea38c51709d62befe1a4, product_id_2: 21b524c4c060169fa75ccf08c7da4627, purchase_count: 2
525. product_id_1: a1dd59756b92c62cd39375d0b0222698, product_id_2: 06edb72f1e0c64b14c5b79353f7abea3, purchase_count: 2
526. product_id_1: a1dd59756b92c62cd39375d0b0222698, product_id_2: 113f80f12c8892f0c59206f70b862b40, purchase_count: 2
527. product_id_1: 6cc859e89d080218ff4416539ffa030c, product_id_2: 8e0aa05a387182c8ef3cd13b6131e60f, purchase_count: 2
528. product_id_1: 85b6cd7f57f7a06d180c93e8c74f6381, product_id_2: e906fa76a27488f805ba8584a4c10cba, purchase_count: 2
529. product_id_1: 309dd69eb83cea38c51709d62befe1a4, product_id_2: 4a5c3967bfd3629fe07ef4d0cc8c3818, purchase_count: 2
530. product_id_1: 309dd69eb83cea38c51709d62befe1a4, product_id_2: 5dae498eff2d80057f56122235a36aff, purchase_count: 2
531. product_id_1: c32b1155b886162db8e1ec114699a799, product_id_2: bd6e6fce9ada76ea2db0f1912e8e478f, purchase_count: 2
532. product_id_1: 309dd69eb83cea38c51709d62befe1a4, product_id_2: 678c229b41c0e497d35a25a8be1cc631, purchase_count: 2
533. product_id_1: 85df978207ed4024ea16570dbb64fd6e, product_id_2: f3ef6902655917c2db06698cc2d765a0, purchase_count: 2
534. product_id_1: 3c839ed874f2e0444a38bfc8daf5ad5e, product_id_2: 1cac29154057b66c1cfcb6ff58e2fdbf, purchase_count: 2
535. product_id_1: 4901f0f8eba79934ba3cdfa1fbc02893, product_id_2: 653b6b1217fba117599afcc015ffd50a, purchase_count: 2
536. product_id_1: 30ad9d2c8a8e788a606a6c23e07260a9, product_id_2: c06f7984550cc89a7d76e51e936e714f, purchase_count: 2
537. product_id_1: 281905b21f01db1009fd7c01b10dd1d4, product_id_2: 83e2059df06602e05d9bc1abf28166ac, purchase_count: 2
538. product_id_1: 592962829d5a715304344e656e39108a, product_id_2: 056d012d264624accb7f73d31caee034, purchase_count: 2
539. product_id_1: 4910917f05092f331bf3a477f791cc01, product_id_2: e8c6039a25765995ac7c1ec2cbef5765, purchase_count: 2
540. product_id_1: ee4a5109a6b0bf0dd3a3347b73955c95, product_id_2: 10717ff440b2320081989126e858b220, purchase_count: 2
541. product_id_1: ee72ae8f6d0b11d7f04230fc894d7e39, product_id_2: 5ef336462ba740ddd4727319e26207e6, purchase_count: 2
542. product_id_1: 86c43103446290e7efacad3701cd654d, product_id_2: 8264f2dcca3aa83cb217d7f09e9c8cf8, purchase_count: 2
543. product_id_1: 592962829d5a715304344e656e39108a, product_id_2: 4f88323d03ffaf090b8fb0116b33c95e, purchase_count: 2
544. product_id_1: a25583531530c0913ea4dee2c5c73685, product_id_2: 521527593ca1726b992318e034dd5690, purchase_count: 2
545. product_id_1: 86f024d3bdcdb9b54c9fffd92be39f54, product_id_2: ce98361ef1341e15087ae4b1b2c53fdd, purchase_count: 2
546. product_id_1: c43ab4269cbf91b373263db4c2973cad, product_id_2: c03d44fcdfabbabd5185c8eb60f77aea, purchase_count: 2
547. product_id_1: c43ab4269cbf91b373263db4c2973cad, product_id_2: d65b6607952f9e0d705b1cbdc92ac027, purchase_count: 2
548. product_id_1: eeba3ee5aa7d1d571752248eb4c81c20, product_id_2: 2265e8aa066cc6c4528d4be900eb5b64, purchase_count: 2
549. product_id_1: 86f2416d4670e4ea3ca5494d043d9f24, product_id_2: 7c898e0b8ea203dd94ba846627fc34d1, purchase_count: 2
550. product_id_1: 6d3d8ade6b793a08b041b6bc653c08ca, product_id_2: ff26009ac6b838dc6cffa2d589cdbefb, purchase_count: 2
551. product_id_1: eef398550dd9575d23eb2d8be74bd45a, product_id_2: 88ca370ef97df0526aeaea6932a38bdd, purchase_count: 2
552. product_id_1: ef1c671d636510846d72e7aa3af1e0a5, product_id_2: 31c79131e883e5fd8c4c85fe9f7d2bb2, purchase_count: 2
553. product_id_1: 15c507fd1d486501a97bd53f82445f1e, product_id_2: d05bb6074b45c20f7a516c239c0a1c43, purchase_count: 2
554. product_id_1: a2ba5bcfe3ee03832bf8f324caa32dad, product_id_2: 2ce17ef87d6bb64be1a0b36a4a614ced, purchase_count: 2
555. product_id_1: 6d59a3fe3140425fb175cdd1e688dc2e, product_id_2: b89603272c5e7806893eb03712a0b937, purchase_count: 2
556. product_id_1: 873eb5f3b8cc503730e472a14cd26616, product_id_2: 7cefa61c9500d9b227894dc48d8b5a0b, purchase_count: 2
557. product_id_1: 2136c70bbe723d338fab53da3c03e6dc, product_id_2: 555cdc8ae3abc9870afa02367539b799, purchase_count: 2
558. product_id_1: efa91c03c750cf82e0e9fc5523aca73c, product_id_2: d57df0660328af2e535fa009f227d575, purchase_count: 2
559. product_id_1: a3309868978f986b3865b8a3729192e2, product_id_2: c0737ec7b87906c79f130f39cec3d3ee, purchase_count: 2
560. product_id_1: 3c9f96101518a345e28a86181196b45a, product_id_2: 882ebbd926d1093b09ff76e976866954, purchase_count: 2
561. product_id_1: 494e28e86f2b12df2d95e9d55266ef4a, product_id_2: fcf311603fa276d415c006188e7bd070, purchase_count: 2
562. product_id_1: a3349ee806d1e1e98d582a2aba5cedcd, product_id_2: a52ed2fb26d435066d6613134afcb439, purchase_count: 2
563. product_id_1: 30ed2f5bb848bade9d8906ef78dd880a, product_id_2: 56c0a9eb43edf8247a0a2ef0f08af0f5, purchase_count: 2
564. product_id_1: f03db1ea02e265f0f1a5ae2a5e0984a7, product_id_2: f09f6223e88af7f6de46dec6a437458b, purchase_count: 2
565. product_id_1: 87cb507e0daa37bbf34956fd59eba832, product_id_2: 186fe07c8b8005ec6a498587ffbc1352, purchase_count: 2
566. product_id_1: 87cb507e0daa37bbf34956fd59eba832, product_id_2: 2136c70bbe723d338fab53da3c03e6dc, purchase_count: 2
567. product_id_1: c589625c8ccc7bfd2e8f1fb041e24c4a, product_id_2: 4167a7ae0930579d1f27d465a1a042f0, purchase_count: 2
568. product_id_1: a3816405c56f1df398541ee9c498b056, product_id_2: 6f86fa71a6aa21f45e317590aacd0c3f, purchase_count: 2
569. product_id_1: c589625c8ccc7bfd2e8f1fb041e24c4a, product_id_2: aa70ae9ee9a798d44ae6e00ce6d82cb1, purchase_count: 2
570. product_id_1: 599dc392f7a23273471b068d72408224, product_id_2: e86b81dcac341ea01df0260077cdf082, purchase_count: 2
571. product_id_1: 3cc4b421c1f28dd22e86fc4aaafb600e, product_id_2: 283dc451ad3918badb976d56ff887289, purchase_count: 2
572. product_id_1: f09f6223e88af7f6de46dec6a437458b, product_id_2: f03db1ea02e265f0f1a5ae2a5e0984a7, purchase_count: 2
573. product_id_1: 0bcc3eeca39e1064258aa1e932269894, product_id_2: 3773a3773f5978591cff7b3e614989b3, purchase_count: 2
574. product_id_1: 31352e05b5f8620929e1b8bbbeda5578, product_id_2: 9b89ab91efbb4750c39864ed0262711f, purchase_count: 2
575. product_id_1: c5b72065154ec27c2d1ed8a654c3348f, product_id_2: ba74c6b75d2ad7503175809688d5a03c, purchase_count: 2
576. product_id_1: f0bb82bede57b520480ce892667bb71d, product_id_2: 0ec96e6d31a1493b0475805c9ae1a0a2, purchase_count: 2
577. product_id_1: 87d780fa7d2cf3710aa02dc4ca8db985, product_id_2: 0fa81e7123fd0ebe03adbbe99d912827, purchase_count: 2
578. product_id_1: a3a10562c9d134b92f04b8cce298d037, product_id_2: 61b6e5d2e3ee58d2b341b8ef1a652b26, purchase_count: 2
579. product_id_1: a3a10562c9d134b92f04b8cce298d037, product_id_2: d3a386ad58b99f0ddcc216ed9efb03c3, purchase_count: 2
580. product_id_1: a3a10562c9d134b92f04b8cce298d037, product_id_2: d64738c7b2e2d1778a51e835d8f02568, purchase_count: 2
581. product_id_1: a3a10562c9d134b92f04b8cce298d037, product_id_2: d80fce9f775927c7d602c2de926759f1, purchase_count: 2
582. product_id_1: a3a10562c9d134b92f04b8cce298d037, product_id_2: ddbf57e4559f03c003fc3708d4860c5e, purchase_count: 2
583. product_id_1: 283dc451ad3918badb976d56ff887289, product_id_2: 3cc4b421c1f28dd22e86fc4aaafb600e, purchase_count: 2
584. product_id_1: 87d780fa7d2cf3710aa02dc4ca8db985, product_id_2: 9d32095f76b97762307e86cfc18dd7a0, purchase_count: 2
585. product_id_1: 59b215ecd21969237a8ebb0f8a2bffc2, product_id_2: e27e689c4ce425f2fe7e2a270fd4d2db, purchase_count: 2
586. product_id_1: a3fd6c4ecde9035c3e8dd4e0fd8b8048, product_id_2: ed4dfdaab6c24770fc6f34ad50c89ac1, purchase_count: 2
587. product_id_1: 283dc451ad3918badb976d56ff887289, product_id_2: 42a2bd596fda1baef5719cb74f73030c, purchase_count: 2
588. product_id_1: f1b067568bb39768f754b0d1ab1abcf6, product_id_2: 3ae116a20336cc3eb1b3d0b9b0a94d3d, purchase_count: 2
589. product_id_1: 2136c70bbe723d338fab53da3c03e6dc, product_id_2: 87cb507e0daa37bbf34956fd59eba832, purchase_count: 2
590. product_id_1: a41d69926dcf58caff228aa637ffea2f, product_id_2: 2b0ee2d07306f7c9ac55a43166e9bb4b, purchase_count: 2
591. product_id_1: a41e356c76fab66334f36de622ecbd3a, product_id_2: 765a8070ece0f1383d0f5faf913dfb9b, purchase_count: 2
592. product_id_1: 880be32f4db1d9f6e2bec38fb6ac23ab, product_id_2: 14dffa241a078aeaebaef48a49e807ca, purchase_count: 2
593. product_id_1: 3ceb44c75e6981ff0987bb90c95694c0, product_id_2: 57c580a8fbf3d8374b06bee7b6f4ce31, purchase_count: 2
594. product_id_1: a44edbb4226328a7a816f3460556d638, product_id_2: 5b7e1c33e4e9e477847a8a031353ff40, purchase_count: 2
595. product_id_1: a44edbb4226328a7a816f3460556d638, product_id_2: 65b183dcbb9689b176730d709a0003dd, purchase_count: 2
596. product_id_1: a44edbb4226328a7a816f3460556d638, product_id_2: 757172573ef8a2cc354243f3da4fa565, purchase_count: 2
597. product_id_1: 3158c44b08596ff51ee3560fad16cc09, product_id_2: 1ae28ef6d0421f92f2e4e6d407e90347, purchase_count: 2
598. product_id_1: 880be32f4db1d9f6e2bec38fb6ac23ab, product_id_2: dd6a505f83dd3c6326aa9856519e0978, purchase_count: 2
599. product_id_1: a46875fb5b8d19ac3cff18deb9bae57e, product_id_2: 1dc7685f4fdb9622d84ae2ec658d5bbf, purchase_count: 2
600. product_id_1: 315c6373ff469f7b7f60bbb36c319f7b, product_id_2: 4680d0c534e54990d8579f41dd239901, purchase_count: 2
601. product_id_1: a46875fb5b8d19ac3cff18deb9bae57e, product_id_2: e256d05115f9eb3766f3ab752132a4e2, purchase_count: 2
602. product_id_1: 8814a3da37fb9673a5ac06f82a2a00a9, product_id_2: 52b668edc0d0c20cd9319bfda4019597, purchase_count: 2
603. product_id_1: c7079d23bead81759eb7c670b96728bc, product_id_2: 04a4e9d8c0dc6b2b4b8e24ea78a8f318, purchase_count: 2
604. product_id_1: 1179867d805886591809f49767db9ecd, product_id_2: 33e503f68fb60fe165ed992965f2c737, purchase_count: 2
605. product_id_1: 882ebbd926d1093b09ff76e976866954, product_id_2: 3c9f96101518a345e28a86181196b45a, purchase_count: 2
606. product_id_1: 28447390cfd2a411fcb8c008b6163da2, product_id_2: b65214d387c754bb0f858a4a5a0f41ad, purchase_count: 2
607. product_id_1: 6e7df7f4622d4360261995dbd5e787d0, product_id_2: 8374b39a15882a19ce4558f13064b55c, purchase_count: 2
608. product_id_1: 2136c70bbe723d338fab53da3c03e6dc, product_id_2: e7890707ac0e4e190a74aa46c92e2c94, purchase_count: 2
609. product_id_1: 887dba291adc295b57b5778ebc8b4060, product_id_2: d498e8a880bdf3d26e2b9b3e92c4f424, purchase_count: 2
610. product_id_1: 0bcc3eeca39e1064258aa1e932269894, product_id_2: 4e1346d7b7e02c737a366b086462e33e, purchase_count: 2
611. product_id_1: 1600dcf1cea8c0c83702e07b577ab231, product_id_2: 0bdd9a52d192d64770e33ae559512478, purchase_count: 2
612. product_id_1: 88bd8458fdc2ceec3e71ef1d867a7b45, product_id_2: 5f0bdec2fb222061ed8fe52586a5957d, purchase_count: 2
613. product_id_1: a50acd33ba7a8da8e9db65094fa990a4, product_id_2: 98d61056e0568ba048e5d78038790e77, purchase_count: 2
614. product_id_1: c784a651cf319526cc7cf854f83cb941, product_id_2: 2ccd049c8e7ea210e079a1aa8ad92477, purchase_count: 2
615. product_id_1: 88c20c5a22f2ca169af8cfc2df00a7a2, product_id_2: 2174a02a3c42e648e408c9b3505c54d3, purchase_count: 2
616. product_id_1: a50c606310374ff8660bbe03010e021b, product_id_2: d191e54bd50ba045ac5bc9336572886f, purchase_count: 2
617. product_id_1: a50c606310374ff8660bbe03010e021b, product_id_2: dea564fb3ed59db512cb4df9c491c1ef, purchase_count: 2
618. product_id_1: c7b3cf9de7be95b3e09e7a63315685eb, product_id_2: f71973c922ccaab05514a36a8bc741b8, purchase_count: 2
619. product_id_1: 88c20c5a22f2ca169af8cfc2df00a7a2, product_id_2: 3625fbaf8284047185fb0351f2f84ae3, purchase_count: 2
620. product_id_1: a519511d5c5c1153c9f636288e50f819, product_id_2: 924c635d837c240da3956f3c28c1e6f4, purchase_count: 2
621. product_id_1: a519511d5c5c1153c9f636288e50f819, product_id_2: bfa8fb32cecbf90899f6f517b77a766f, purchase_count: 2
622. product_id_1: 88c20c5a22f2ca169af8cfc2df00a7a2, product_id_2: 7413f40201dadc558699e8de1cbfa922, purchase_count: 2
623. product_id_1: a52ed2fb26d435066d6613134afcb439, product_id_2: a3349ee806d1e1e98d582a2aba5cedcd, purchase_count: 2
624. product_id_1: 88ca370ef97df0526aeaea6932a38bdd, product_id_2: eef398550dd9575d23eb2d8be74bd45a, purchase_count: 2
625. product_id_1: 6eba58100f906fe0965290b28ca3c45f, product_id_2: b90973ce80ba5d1fbc046fd8471acaef, purchase_count: 2
626. product_id_1: 6ed93af03d1f53308d3a9c6555a94d08, product_id_2: aecdd1c18af2379312e946f33280fe25, purchase_count: 2
627. product_id_1: a57878a3c4874b342d09d163ae63e596, product_id_2: 820e8f306dc9ffcf6d0957516084cca1, purchase_count: 2
628. product_id_1: 6ee1607bacba780139e7f7fcd316c1d0, product_id_2: 3a05a947f28cf46d789adedc107d7595, purchase_count: 2
629. product_id_1: 89039f76a4c1ed8e4c13f4b531f158ca, product_id_2: 0b5c0ecd14105464e2b879a307092e3f, purchase_count: 2
630. product_id_1: 0bcc3eeca39e1064258aa1e932269894, product_id_2: 774e21c631ca26cba7b5606bdca7460f, purchase_count: 2
631. product_id_1: 00ba6d766f0b1d7b78a5ce3e1e033263, product_id_2: b931645cdc2d9868f01544e8db63f5ab, purchase_count: 2
632. product_id_1: f39288f58793ce5e6985b3f7832af88c, product_id_2: ac5e164e2eda939ffa46593f90077f9a, purchase_count: 2
633. product_id_1: 014a8a503291921f7b004a5215bb3c36, product_id_2: dd6a505f83dd3c6326aa9856519e0978, purchase_count: 2
634. product_id_1: 892bc3e900a6ad3cba5112ccdb33466f, product_id_2: 8ed3ae310714d18ee990923aeb411508, purchase_count: 2
635. product_id_1: 2174a02a3c42e648e408c9b3505c54d3, product_id_2: 88c20c5a22f2ca169af8cfc2df00a7a2, purchase_count: 2
636. product_id_1: 289d248f6a9046a0f0be47cda2b45537, product_id_2: 09f6dccfebfa0688abfc1af640b69e61, purchase_count: 2
637. product_id_1: 4a5c3967bfd3629fe07ef4d0cc8c3818, product_id_2: 0de59eddc63167215c972b0d785ffa7b, purchase_count: 2
638. product_id_1: f3ae4ce1b63810f2921ff353ddbec67d, product_id_2: e9dd44f105ffdcb98405c94f1d0bbdd9, purchase_count: 2
639. product_id_1: 161ccc972b7b25a5e2d43376b8b333c5, product_id_2: d34efb58e1930773fcde9b951892b1b1, purchase_count: 2
640. product_id_1: 3dc7db1edfac20883ed35ecfec05a3cc, product_id_2: 24baefeed71136f90df0149ca1e85c49, purchase_count: 2
641. product_id_1: 5a883fb296ab66ac6a1e68e6ba2175c3, product_id_2: a140e83c184347be1aa71694fe525537, purchase_count: 2
642. product_id_1: 4a5c3967bfd3629fe07ef4d0cc8c3818, product_id_2: 309dd69eb83cea38c51709d62befe1a4, purchase_count: 2
643. product_id_1: 6f3b5b605d91b7439c5e3f5a8dffeea7, product_id_2: b3c13ca98fb6f9dd5c6aec8b1d353506, purchase_count: 2
644. product_id_1: 6f46359e56f51d5deded13adcd1c255c, product_id_2: 7486542600afc050d20740e976ff87f8, purchase_count: 2
645. product_id_1: f3ef6902655917c2db06698cc2d765a0, product_id_2: 85df978207ed4024ea16570dbb64fd6e, purchase_count: 2
646. product_id_1: c8a4cbaafa1f0579063ec64cf40ae153, product_id_2: 3f4269f81421aadbfc643a23d5dbf3ff, purchase_count: 2
647. product_id_1: 5aad359a63cbb4fc35ead44346a3eeb4, product_id_2: af35be35db4ad0dc288b571453337376, purchase_count: 2
648. product_id_1: c8b96022819f31119f1404ad2c3c1059, product_id_2: a996a150a7fd0eba6a177ec84b939b51, purchase_count: 2
649. product_id_1: a669398f595527fc03acc1ebda6b3cce, product_id_2: 189e539d996a9b8ba4bba1a140a024a7, purchase_count: 2
650. product_id_1: 4a5c3967bfd3629fe07ef4d0cc8c3818, product_id_2: 4255ef536732efe235477ace2dccd393, purchase_count: 2
651. product_id_1: 5ac4f7986643a944501c66a2257bdd73, product_id_2: d04bbac48960ecb7ea311b00ca6e1cb7, purchase_count: 2
652. product_id_1: 3dd2a17168ec895c781a9191c1e95ad7, product_id_2: 909b87db6cb3a7ab26bd03cc59860136, purchase_count: 2
653. product_id_1: 31c79131e883e5fd8c4c85fe9f7d2bb2, product_id_2: ef1c671d636510846d72e7aa3af1e0a5, purchase_count: 2
654. product_id_1: 0a28355911f72609e396a3dc10b11c90, product_id_2: d017a2151d543a9885604dc62a3d9dcc, purchase_count: 2
655. product_id_1: 5b1f3328a2c6f837ecce21bca1489939, product_id_2: 26facbccf840188b92bcc8cb89fe1f64, purchase_count: 2
656. product_id_1: a6b56b20f93907299eef6ea711338269, product_id_2: 3bbacbe586e957acbf26c63b3ed532a3, purchase_count: 2
657. product_id_1: 6f7400c1577bd99fb7c9cd196edb6ae2, product_id_2: 9a98180ffbd0765e89f11cc8dd2385f4, purchase_count: 2
658. product_id_1: 6f86fa71a6aa21f45e317590aacd0c3f, product_id_2: a3816405c56f1df398541ee9c498b056, purchase_count: 2
659. product_id_1: 06edb72f1e0c64b14c5b79353f7abea3, product_id_2: a1dd59756b92c62cd39375d0b0222698, purchase_count: 2
660. product_id_1: 1b97621fc0e6ac58cfb272d5ccf8c15b, product_id_2: 66bd6e465a87926adb15dec604948867, purchase_count: 2
661. product_id_1: a743637eea3be2e0ab81acc155c9cce2, product_id_2: 8aa87bc5f3053b4df2b05a2d3059790b, purchase_count: 2
662. product_id_1: c9b8a74a8865b966e660cc1f7b4e32a9, product_id_2: a03e401d58a45187271718c5d7610422, purchase_count: 2
663. product_id_1: a7742a00e1d286b7f7d4d81e90d8acc9, product_id_2: 577fd304233fe9412349ef6a4a3f6ae6, purchase_count: 2
664. product_id_1: a787d9cee40e9de33b13d740c32359e8, product_id_2: ed61f9d2b8837c3aeebb563b7305ef78, purchase_count: 2
665. product_id_1: f4d705aa95ccca448e5b0deb6e5290ba, product_id_2: 4025ee582ef6b8c478af3b44cf89054b, purchase_count: 2
666. product_id_1: 321cea6c65a44a9abde31f677f976c63, product_id_2: e0ce26ae52c9ab0b8c8e42129d6c1996, purchase_count: 2
667. product_id_1: a79c0d179a6de79b23a81b64b3980c04, product_id_2: 5bf57bdef224b9486b45ebba37ec6191, purchase_count: 2
668. product_id_1: 163e6400e6dadd0fe04775c5e9331fda, product_id_2: 2fb0efd1f61f186ffdda9e8ec70f27f2, purchase_count: 2
669. product_id_1: 21b524c4c060169fa75ccf08c7da4627, product_id_2: 0de59eddc63167215c972b0d785ffa7b, purchase_count: 2
670. product_id_1: 02623b0e4e6b951aefb23575de1f3886, product_id_2: ec2d43cc59763ec91694573b31f1c29a, purchase_count: 2
671. product_id_1: 5b4c8ab4477bb00b57cd5edb1af9aff8, product_id_2: 6845447c5d4495dcddca6e6b494df3e7, purchase_count: 2
672. product_id_1: 8aa87bc5f3053b4df2b05a2d3059790b, product_id_2: a743637eea3be2e0ab81acc155c9cce2, purchase_count: 2
673. product_id_1: 8ab78b6f871fd72d1ef38097498b70b7, product_id_2: 1d1e5ff7c1fe84990f92d41f7425b789, purchase_count: 2
674. product_id_1: ca9b2caa4f7ec65aeda5825e09dcf99c, product_id_2: 0c6f417a4037ab082ea5fe9a4e7da299, purchase_count: 2
675. product_id_1: f59871b3d9da4c64cbe41ad3dd04dc14, product_id_2: 5599be6fe59cd2257edfdec9d45442e0, purchase_count: 2
676. product_id_1: 21b524c4c060169fa75ccf08c7da4627, product_id_2: 309dd69eb83cea38c51709d62befe1a4, purchase_count: 2
677. product_id_1: 0a4093a4af429dc0a9334300e5c13ae5, product_id_2: aadff88486740e0b0ebe2be6c09476ae, purchase_count: 2
678. product_id_1: 5b7e1c33e4e9e477847a8a031353ff40, product_id_2: a44edbb4226328a7a816f3460556d638, purchase_count: 2
679. product_id_1: cad2db5e318d7283a234c517b2f28a42, product_id_2: 9ad75bd7267e5c724cb42c71ac56ca72, purchase_count: 2
680. product_id_1: 3e5201fe0d1ba474d9b90152c83c706c, product_id_2: 665aa1d687284a4d2d2b74c0c6724625, purchase_count: 2
681. product_id_1: 8b3a9476f74f5297f7ff0ec6d95fe1ea, product_id_2: d902ca64b614964dc31d6b0372e800ac, purchase_count: 2
682. product_id_1: 3e5201fe0d1ba474d9b90152c83c706c, product_id_2: 7a0f37fda63d1cd7dac2451494eb6e69, purchase_count: 2
683. product_id_1: 120fa011365fc39efe382cba4e50999e, product_id_2: 372645c7439f9661fbbacfd129aa92ec, purchase_count: 2
684. product_id_1: 3e5201fe0d1ba474d9b90152c83c706c, product_id_2: 99a4788cb24856965c36a24e339b6058, purchase_count: 2
685. product_id_1: a88124e0b1d42ca7b0813a78ff630437, product_id_2: 4255ef536732efe235477ace2dccd393, purchase_count: 2
686. product_id_1: 32459442f3b850918e20febc47c9edfb, product_id_2: 1a1607ff3b9bced214efc0a8cdfb2510, purchase_count: 2
687. product_id_1: 29b18b99ca3c94cea05efa9e11465440, product_id_2: b2775a101dfacb48184ed1c1cb4a278b, purchase_count: 2
688. product_id_1: f6e3aeb40c00aec24ade8333c2ac1b20, product_id_2: db7f3f42ccab32fa6328b3063b278bcc, purchase_count: 2
689. product_id_1: 29bc923d3ecb389b5b1b6fe2a6e4799a, product_id_2: b63ecf99904f905e0d594b11ac06281e, purchase_count: 2
690. product_id_1: cb5d3d2427c53fde437c52bde24840e8, product_id_2: 2d37d1dbcba865841a1c8cfab20ab9a1, purchase_count: 2
691. product_id_1: 5bf57bdef224b9486b45ebba37ec6191, product_id_2: a79c0d179a6de79b23a81b64b3980c04, purchase_count: 2
692. product_id_1: 29e4631be78811ab993ae12613053b53, product_id_2: 98d61056e0568ba048e5d78038790e77, purchase_count: 2
693. product_id_1: f71973c922ccaab05514a36a8bc741b8, product_id_2: c7b3cf9de7be95b3e09e7a63315685eb, purchase_count: 2
694. product_id_1: 0bdd9a52d192d64770e33ae559512478, product_id_2: 1600dcf1cea8c0c83702e07b577ab231, purchase_count: 2
695. product_id_1: 0bdd9a52d192d64770e33ae559512478, product_id_2: 186fe07c8b8005ec6a498587ffbc1352, purchase_count: 2
696. product_id_1: cbdb9bf611328898bd4b32a384506b3a, product_id_2: feb4ade62e32b8d74c6f69f635057964, purchase_count: 2
697. product_id_1: a8bf9a06bef0fe4106c1fc0df21a5eb6, product_id_2: 5421431a9abfbdac3006e7aa925c0213, purchase_count: 2
698. product_id_1: a8bf9a06bef0fe4106c1fc0df21a5eb6, product_id_2: 5ed1d686373e3b3a2ddd9a4ce44f3fb2, purchase_count: 2
699. product_id_1: a8d2af10596b8acd5f45c720fe9745aa, product_id_2: 113f80f12c8892f0c59206f70b862b40, purchase_count: 2
700. product_id_1: cbefecd2f12e002078d38c62d665278f, product_id_2: 122f396fa6d0f9070c6e721f8d833d2b, purchase_count: 2
701. product_id_1: 8b90be4893a4277a9f33c5b2348cf9c6, product_id_2: fa94f25a73969e3a25d52706e246dfcc, purchase_count: 2
702. product_id_1: 4bc15899b2cd7ade6db2fb0a5188cd24, product_id_2: c0400a62c5019cdc69bfc76d39b1cfb4, purchase_count: 2
703. product_id_1: 1c1dda7d5b3d50618aadda35edc2acd6, product_id_2: 407a9382e8c7e321e8ecee388edf0f7b, purchase_count: 2
704. product_id_1: 03bb06cda40712fb8473f7962fb7d198, product_id_2: fec565c4e3ad965c73fb1a21bb809257, purchase_count: 2
705. product_id_1: f7c7bd3105bd26ce0de4072af7159f84, product_id_2: aa8d767a6316127a012fc3d16b84dc7f, purchase_count: 2
706. product_id_1: 3e7d7087ff8bbc0e9568b56ba3504a34, product_id_2: 8ee57a1f636eb2e009706bbdb0818ecc, purchase_count: 2
707. product_id_1: f8077831f3c3f393fb67b93c5acd8daf, product_id_2: d315b738a6e96f4d9710af966cb7cd5b, purchase_count: 2
708. product_id_1: cc59cf334461196527f790e5c9191ece, product_id_2: 4e5dc46fe4e31dd605f374ee43f0268e, purchase_count: 2
709. product_id_1: a92930c327948861c015c919a0bcb4a8, product_id_2: dc52f0f5d3ec37a93eaf956cde4e5d2c, purchase_count: 2
710. product_id_1: 7185389e32acf9c5c5f61e6a23c0ab3a, product_id_2: ec2d43cc59763ec91694573b31f1c29a, purchase_count: 2
711. product_id_1: 2265e8aa066cc6c4528d4be900eb5b64, product_id_2: eeba3ee5aa7d1d571752248eb4c81c20, purchase_count: 2
712. product_id_1: f879fadd73c7b81f0b278dacc880cf08, product_id_2: de37ff8068c8e7b1164a19f0f4d05619, purchase_count: 2
713. product_id_1: cce679660c66e6fbd5c8091dfd29e9cd, product_id_2: cf6514025ef5d3a93d69d2a7bfa4036b, purchase_count: 2
714. product_id_1: 122f396fa6d0f9070c6e721f8d833d2b, product_id_2: cbefecd2f12e002078d38c62d665278f, purchase_count: 2
715. product_id_1: 71a8be2937fd926b330febe100effd02, product_id_2: 6c3effec7c8ddba466d4f03f982c7aa3, purchase_count: 2
716. product_id_1: 71b157e39523e25558ed9cc1960c3fbd, product_id_2: 02ed3b595447e948efc3eac897e4df0e, purchase_count: 2
717. product_id_1: f8cd8a989b03ce1808d9d8d76668ea51, product_id_2: ebe9e593dfd269670a40a0ee90a8764e, purchase_count: 2
718. product_id_1: cd2ea14a901da3b47b33516f3ca6929e, product_id_2: 1a4247b6eddc27c68f7995dcc68b01e2, purchase_count: 2
719. product_id_1: a996a150a7fd0eba6a177ec84b939b51, product_id_2: c8b96022819f31119f1404ad2c3c1059, purchase_count: 2
720. product_id_1: f940327804bdcb40342a12c93de069b8, product_id_2: 020a80cb704bf65f38761fcedf2af192, purchase_count: 2
721. product_id_1: f95d9369ebf76f811194c72bd22ff244, product_id_2: fc831da5307b1a3e23ed0259a2b6b2a1, purchase_count: 2
722. product_id_1: 4c3ae5db49258df0784827bdacf3b396, product_id_2: fb7a100ec8c7b34f60cec22b1a9a10e0, purchase_count: 2
723. product_id_1: cd3de1984e1a77b441e1b39b8e334330, product_id_2: 665aa1d687284a4d2d2b74c0c6724625, purchase_count: 2
724. product_id_1: cd3de1984e1a77b441e1b39b8e334330, product_id_2: 7a0f37fda63d1cd7dac2451494eb6e69, purchase_count: 2
725. product_id_1: a996a4fecaea5e7e2638d2c5078ebf4b, product_id_2: b9adb834b99082140e354bdd3bda7eb5, purchase_count: 2
726. product_id_1: 32dfa38395ccd47d7b320470b0514fee, product_id_2: 05df88a280f9c6edca3b2f5f9b3e75ad, purchase_count: 2
727. product_id_1: cd489785324bc65510f5a0ea2382f1d3, product_id_2: 00ba6d766f0b1d7b78a5ce3e1e033263, purchase_count: 2
728. product_id_1: cd489785324bc65510f5a0ea2382f1d3, product_id_2: ff95ac47246ef13e48712ea1ff8df0d9, purchase_count: 2
729. product_id_1: cd58b9f614170d691ae0b6049f842894, product_id_2: fb31d5d2acd4bf37057330c1a96af712, purchase_count: 2
730. product_id_1: 04a4e9d8c0dc6b2b4b8e24ea78a8f318, product_id_2: c7079d23bead81759eb7c670b96728bc, purchase_count: 2
731. product_id_1: 3eef0cb94ba82de806bb30ab743c7655, product_id_2: 0a9bdadab17a9b0f258f64d11a0adf7b, purchase_count: 2
732. product_id_1: cda960fc8a8987dd224a17dddfffdaa5, product_id_2: b791d5d05f0c974d148d358efcd21d84, purchase_count: 2
733. product_id_1: f9bdcb274f479aa71dd34e8bccdd9a82, product_id_2: 37318ccebb2ced72bd1b548b55ab4e31, purchase_count: 2
734. product_id_1: 3eef0cb94ba82de806bb30ab743c7655, product_id_2: daf84c8f6a77308759733b317cf20666, purchase_count: 2
735. product_id_1: 0a4f9f421af66d2ea061fbb8883419f7, product_id_2: 43b54d1fc56ff394092a3dff6be2d39f, purchase_count: 2
736. product_id_1: fa243e761ae871597627e917611eeb23, product_id_2: be59d6c35e43e4bae41772d4b87136a4, purchase_count: 2
737. product_id_1: cdc4af478fef19f03f1d0353c00271cd, product_id_2: a140e83c184347be1aa71694fe525537, purchase_count: 2
738. product_id_1: cdd68c0ef3e507db79631336cf9ec285, product_id_2: dfdbfd7997881adc15da4916717e46aa, purchase_count: 2
739. product_id_1: ce003d873dc7d3c9482b894f2f2cc3e3, product_id_2: 1fe7076c53248559454a7e1d6c1037f9, purchase_count: 2
740. product_id_1: 0ec96e6d31a1493b0475805c9ae1a0a2, product_id_2: f0bb82bede57b520480ce892667bb71d, purchase_count: 2
741. product_id_1: 3321ad579f19476d0d668f726f8dffec, product_id_2: fec565c4e3ad965c73fb1a21bb809257, purchase_count: 2
742. product_id_1: 1c56f826f3a1fdf255e3fb5fa7637d3e, product_id_2: db1d1a4569fdbae28a0d3340d907f7af, purchase_count: 2
743. product_id_1: fa94f25a73969e3a25d52706e246dfcc, product_id_2: 8b90be4893a4277a9f33c5b2348cf9c6, purchase_count: 2
744. product_id_1: fa94f25a73969e3a25d52706e246dfcc, product_id_2: b01cedfa96d891427058852f0625e9ee, purchase_count: 2
745. product_id_1: 3f4269f81421aadbfc643a23d5dbf3ff, product_id_2: c8a4cbaafa1f0579063ec64cf40ae153, purchase_count: 2
746. product_id_1: 171b509779ad4fe0cbed2a3d95d10c68, product_id_2: ed2067a9c1f79553088a3c67b99a9f97, purchase_count: 2
747. product_id_1: 1c8c80454d9a8829112d5be9fe885fab, product_id_2: 781afe929e3016a667f5f439afd55fce, purchase_count: 2
748. product_id_1: 8cf22b2cc9465d64474a09853b62f5b2, product_id_2: b6b220a6c539cb65be34eed6fea8fe63, purchase_count: 2
749. product_id_1: 3fa864b2eb9bb60d23bfe315213bb5d9, product_id_2: 407a9382e8c7e321e8ecee388edf0f7b, purchase_count: 2
750. product_id_1: 1269d60fc5efbcf03e7eea49213091c6, product_id_2: 7b49e585ac8c80b14c9b2815d4db465f, purchase_count: 2
751. product_id_1: 8d070077591cb06503a4933e5050bc69, product_id_2: b73f6899a58fe7a37e55149e9a11c717, purchase_count: 2
752. product_id_1: fb2f2ec90b4ee90ad257bbf89d01247e, product_id_2: 1d0b9497ac4f258fbd822c52ff61b5f4, purchase_count: 2
753. product_id_1: ce98361ef1341e15087ae4b1b2c53fdd, product_id_2: 40cb7bb3d30559b9b6c4fb62bc837962, purchase_count: 2
754. product_id_1: ce98361ef1341e15087ae4b1b2c53fdd, product_id_2: 86f024d3bdcdb9b54c9fffd92be39f54, purchase_count: 2
755. product_id_1: fb31d5d2acd4bf37057330c1a96af712, product_id_2: cd58b9f614170d691ae0b6049f842894, purchase_count: 2
756. product_id_1: aa70ae9ee9a798d44ae6e00ce6d82cb1, product_id_2: c589625c8ccc7bfd2e8f1fb041e24c4a, purchase_count: 2
757. product_id_1: aa70ae9ee9a798d44ae6e00ce6d82cb1, product_id_2: d13a4acdb64c202e774e815db547e108, purchase_count: 2
758. product_id_1: cec09725da5ed01471d9a505e7389d37, product_id_2: 368c6c730842d78016ad823897a372db, purchase_count: 2
759. product_id_1: aa8d767a6316127a012fc3d16b84dc7f, product_id_2: f7c7bd3105bd26ce0de4072af7159f84, purchase_count: 2
760. product_id_1: 8d28eb3a7309368ca0de19e016266251, product_id_2: 7486542600afc050d20740e976ff87f8, purchase_count: 2
761. product_id_1: 232a5adb0fc1881bbfeb03560c639c31, product_id_2: 64fc6010136aa59736e148c404e77a54, purchase_count: 2
762. product_id_1: fb7a100ec8c7b34f60cec22b1a9a10e0, product_id_2: 4c3ae5db49258df0784827bdacf3b396, purchase_count: 2
763. product_id_1: 2ae501b303a5a8e6f75c8c36f366b2d5, product_id_2: d8c0c707d3724304033f593878cbf1e6, purchase_count: 2
764. product_id_1: aadff88486740e0b0ebe2be6c09476ae, product_id_2: 0a4093a4af429dc0a9334300e5c13ae5, purchase_count: 2
765. product_id_1: 0c6f417a4037ab082ea5fe9a4e7da299, product_id_2: ca9b2caa4f7ec65aeda5825e09dcf99c, purchase_count: 2
766. product_id_1: cf0d29a0ea1464f4c3e5594d0746c51b, product_id_2: 57fcacc3434a1f2f2b039c1b4e61f5e1, purchase_count: 2
767. product_id_1: cf1d8e226162a1d0ad61f29b7ed72d82, product_id_2: 1d1183a8de24782a216dc5066d7421bf, purchase_count: 2
768. product_id_1: cf1d8e226162a1d0ad61f29b7ed72d82, product_id_2: e9b3cf27d68caa64832c4a7c460abcb9, purchase_count: 2
769. product_id_1: fbc1488c1a1e72ba175f53ab29a248e8, product_id_2: 0f91b6a95a57a43203a9b17de98960d9, purchase_count: 2
770. product_id_1: ab169b33d13e5041b9b9d4a2fafce9d9, product_id_2: 457cd0a99cfa977993e4eb6d98d95abb, purchase_count: 2
771. product_id_1: 8d4dac6177fb8134f26fb4c5cc6c0aff, product_id_2: 4f0abfbee7569e43b80f9aaa256a9bf8, purchase_count: 2
772. product_id_1: cf54cbfe4e33bc8f7b34a65da576497c, product_id_2: 35afc973633aaeb6b877ff57b2793310, purchase_count: 2
773. product_id_1: 731599825523e54feea5f4678ca8f54f, product_id_2: 96ea4f32befa14bd8ab36fd6827a5e3f, purchase_count: 2
774. product_id_1: cf6514025ef5d3a93d69d2a7bfa4036b, product_id_2: cce679660c66e6fbd5c8091dfd29e9cd, purchase_count: 2
775. product_id_1: 33e503f68fb60fe165ed992965f2c737, product_id_2: 03d817e5e392e78674ed0bd8195f9159, purchase_count: 2
776. product_id_1: 33e503f68fb60fe165ed992965f2c737, product_id_2: 1179867d805886591809f49767db9ecd, purchase_count: 2
777. product_id_1: 5d6bea33648f018dbb563f3a2fab09f3, product_id_2: 7b5d8be0e04080e4c8ee6a7ec2f1f597, purchase_count: 2
778. product_id_1: 8d7d29e5fb9ff5333009326c87fc04e9, product_id_2: 516ccdc0667fe7e260156d1998ef9546, purchase_count: 2
779. product_id_1: fc1d8637c0268af3db482c14b7ef8e75, product_id_2: 06ecc3d4006ad6eb293a1b93ec3c7183, purchase_count: 2
780. product_id_1: fc1d8637c0268af3db482c14b7ef8e75, product_id_2: 9a0620ddaf3055b7e588e936e036a529, purchase_count: 2
781. product_id_1: fc22eb7bba78fd67da33c9acf162d592, product_id_2: 27d0fc55e3d2fe698088f2603e0a2ab6, purchase_count: 2
782. product_id_1: fc2d17e60bdd3349a25f3ca6a802a91e, product_id_2: d199462b8361a3e047e64595bce5b6ea, purchase_count: 2
783. product_id_1: 33e503f68fb60fe165ed992965f2c737, product_id_2: 993ac19aa975075775c16ba15426f8be, purchase_count: 2
784. product_id_1: cfe6e9c01d0bbb5df9a75f0e3286baa9, product_id_2: ec8ae427905e10052ee4f1e9993b6763, purchase_count: 2
785. product_id_1: cfe9e8e1f0400c8cc665d41722f34086, product_id_2: 962a6951154f98f2c8e9a5b8b2bcf4a9, purchase_count: 2
786. product_id_1: 8d98dedc3c19de17f1a090195e85d6b6, product_id_2: d5b703c271f43f9c588a6f512a00f77e, purchase_count: 2
787. product_id_1: 4006da5107400e5ac48dbcc829a36c42, product_id_2: 83e2059df06602e05d9bc1abf28166ac, purchase_count: 2
788. product_id_1: d011223de539cd224b5c5c8082313d46, product_id_2: 09c3a2ea33f044aebffecd6681e00133, purchase_count: 2
789. product_id_1: d017a2151d543a9885604dc62a3d9dcc, product_id_2: 0a28355911f72609e396a3dc10b11c90, purchase_count: 2
790. product_id_1: fc831da5307b1a3e23ed0259a2b6b2a1, product_id_2: 8ed094bfe076c568f6bb10feada3f75d, purchase_count: 2
791. product_id_1: fc831da5307b1a3e23ed0259a2b6b2a1, product_id_2: f95d9369ebf76f811194c72bd22ff244, purchase_count: 2
792. product_id_1: 33e503f68fb60fe165ed992965f2c737, product_id_2: da7813106f94601e6022f50017299e2f, purchase_count: 2
793. product_id_1: 2b0ee2d07306f7c9ac55a43166e9bb4b, product_id_2: a41d69926dcf58caff228aa637ffea2f, purchase_count: 2
794. product_id_1: 0a80f03007af9e2c5ac5065d6742e1b2, product_id_2: 820fa146b7ccfe19c80e999cf4a77668, purchase_count: 2
795. product_id_1: 1cac29154057b66c1cfcb6ff58e2fdbf, product_id_2: 3c839ed874f2e0444a38bfc8daf5ad5e, purchase_count: 2
796. product_id_1: 5dae498eff2d80057f56122235a36aff, product_id_2: 0de59eddc63167215c972b0d785ffa7b, purchase_count: 2
797. product_id_1: 8e0aa05a387182c8ef3cd13b6131e60f, product_id_2: 6cc859e89d080218ff4416539ffa030c, purchase_count: 2
798. product_id_1: abe2c60707c1e11cfa710dc7328b4bf6, product_id_2: 113f80f12c8892f0c59206f70b862b40, purchase_count: 2
799. product_id_1: fcf311603fa276d415c006188e7bd070, product_id_2: 494e28e86f2b12df2d95e9d55266ef4a, purchase_count: 2
800. product_id_1: 4025ee582ef6b8c478af3b44cf89054b, product_id_2: bb42f37fc3d9130e4a4339d24a47dd7c, purchase_count: 2
801. product_id_1: d04bbac48960ecb7ea311b00ca6e1cb7, product_id_2: 5ac4f7986643a944501c66a2257bdd73, purchase_count: 2
802. product_id_1: 4025ee582ef6b8c478af3b44cf89054b, product_id_2: c211ff3068fcd2f8898192976d8b3a32, purchase_count: 2
803. product_id_1: 4dfffeaa9522a9ba71cdc9e7d43212d0, product_id_2: 48282b524c93e69ec5653481e2b8a237, purchase_count: 2
804. product_id_1: 5dae498eff2d80057f56122235a36aff, product_id_2: 309dd69eb83cea38c51709d62befe1a4, purchase_count: 2
805. product_id_1: d05bb6074b45c20f7a516c239c0a1c43, product_id_2: 15c507fd1d486501a97bd53f82445f1e, purchase_count: 2
806. product_id_1: 4025ee582ef6b8c478af3b44cf89054b, product_id_2: f4d705aa95ccca448e5b0deb6e5290ba, purchase_count: 2
807. product_id_1: 5dae498eff2d80057f56122235a36aff, product_id_2: 678c229b41c0e497d35a25a8be1cc631, purchase_count: 2
808. product_id_1: 2b3ded25b94fa59143322115fce48003, product_id_2: b627957ffcd19ace5037a5df4230d1fa, purchase_count: 2
809. product_id_1: d102ed54656bd3eaf5bd365494e08bf6, product_id_2: 427a9f5e8a9d47c60adc5ae34e2657d2, purchase_count: 2
810. product_id_1: 0c9ff9d8ed9b9bdd825487b3a66e05f5, product_id_2: 4fcb3d9a5f4871e8362dfedbdb02b064, purchase_count: 2
811. product_id_1: 40376ad8bd1bd1066449dbb09440dc43, product_id_2: ac5e164e2eda939ffa46593f90077f9a, purchase_count: 2
812. product_id_1: 74006af1917b5e79f78f35767fa221ba, product_id_2: 3c14f8a3874197fe07fe94b4d5d9af86, purchase_count: 2
813. product_id_1: 7413f40201dadc558699e8de1cbfa922, product_id_2: 88c20c5a22f2ca169af8cfc2df00a7a2, purchase_count: 2
814. product_id_1: 4e1346d7b7e02c737a366b086462e33e, product_id_2: 0bcc3eeca39e1064258aa1e932269894, purchase_count: 2
815. product_id_1: 741a31499a578979be85db7f80139e62, product_id_2: 8338cef8355d238f43711dcb9c0657b2, purchase_count: 2
816. product_id_1: d13a4acdb64c202e774e815db547e108, product_id_2: aa70ae9ee9a798d44ae6e00ce6d82cb1, purchase_count: 2
817. product_id_1: fd91e23b4465803725f329b39afe018a, product_id_2: bcda9424eac9dd4c6f2d739e92c0a2ab, purchase_count: 2
818. product_id_1: 4e1346d7b7e02c737a366b086462e33e, product_id_2: 422879e10f46682990de24d770e7f83d, purchase_count: 2
819. product_id_1: ac5e164e2eda939ffa46593f90077f9a, product_id_2: 39a0578866cba21bcead91f5221af2a8, purchase_count: 2
820. product_id_1: ac5e164e2eda939ffa46593f90077f9a, product_id_2: 40376ad8bd1bd1066449dbb09440dc43, purchase_count: 2
821. product_id_1: fdbd77fe1773263558126c16e0b4b67c, product_id_2: 99a4788cb24856965c36a24e339b6058, purchase_count: 2
822. product_id_1: ac5e164e2eda939ffa46593f90077f9a, product_id_2: 834df04774f3aa4b60bfd6f839f448bc, purchase_count: 2
823. product_id_1: ac5e164e2eda939ffa46593f90077f9a, product_id_2: f39288f58793ce5e6985b3f7832af88c, purchase_count: 2
824. product_id_1: d191e54bd50ba045ac5bc9336572886f, product_id_2: 38cd38029795797c97b73421fdad08cf, purchase_count: 2
825. product_id_1: d191e54bd50ba045ac5bc9336572886f, product_id_2: a50c606310374ff8660bbe03010e021b, purchase_count: 2
826. product_id_1: ac7e981115ad47f0e051f1b8b97e73b1, product_id_2: 1fd3bb291e0dba9d6081eb914303993b, purchase_count: 2
827. product_id_1: 00ba6d766f0b1d7b78a5ce3e1e033263, product_id_2: cd489785324bc65510f5a0ea2382f1d3, purchase_count: 2
828. product_id_1: fe55c83c8471a2fca643b9291c1f105e, product_id_2: 52faaea7e7d55dfe5aa81f0b5f79d7b9, purchase_count: 2
829. product_id_1: d199462b8361a3e047e64595bce5b6ea, product_id_2: fc2d17e60bdd3349a25f3ca6a802a91e, purchase_count: 2
830. product_id_1: 3439529926df110506c6752e8f16d358, product_id_2: fe61253e50ad6ee9f1d180da22ce5eef, purchase_count: 2
831. product_id_1: 40639ced9d62eca7f4637b1be4ccdf44, product_id_2: 748b719f4cbfdcb99cae90bf4bb16217, purchase_count: 2
832. product_id_1: fe61253e50ad6ee9f1d180da22ce5eef, product_id_2: 3439529926df110506c6752e8f16d358, purchase_count: 2
833. product_id_1: fe6f03cedd96bcbc5c8726c5963fd35c, product_id_2: 01ef0716b68c8493434ad32430c24e18, purchase_count: 2
834. product_id_1: d1b1a0e78589ee89279d0be1e4a8b905, product_id_2: 47ea90e9a2976bc290c3cdf3b5e0573d, purchase_count: 2
835. product_id_1: 4e5dc46fe4e31dd605f374ee43f0268e, product_id_2: cc59cf334461196527f790e5c9191ece, purchase_count: 2
836. product_id_1: 8ed094bfe076c568f6bb10feada3f75d, product_id_2: fc831da5307b1a3e23ed0259a2b6b2a1, purchase_count: 2
837. product_id_1: 8ed3ae310714d18ee990923aeb411508, product_id_2: 2b9b580cdc992e165ca0336a078d695f, purchase_count: 2
838. product_id_1: feb4ade62e32b8d74c6f69f635057964, product_id_2: cbdb9bf611328898bd4b32a384506b3a, purchase_count: 2
839. product_id_1: 8ed3ae310714d18ee990923aeb411508, product_id_2: 892bc3e900a6ad3cba5112ccdb33466f, purchase_count: 2
840. product_id_1: 8ed3ae310714d18ee990923aeb411508, product_id_2: b86d1f2c052bc4749ee88bb74688d814, purchase_count: 2
841. product_id_1: 5ddab10d5e0a23acb99acf56b62b3276, product_id_2: ebf9bc6cd600eadd681384e3116fda85, purchase_count: 2
842. product_id_1: fec565c4e3ad965c73fb1a21bb809257, product_id_2: 03bb06cda40712fb8473f7962fb7d198, purchase_count: 2
843. product_id_1: fec565c4e3ad965c73fb1a21bb809257, product_id_2: 3321ad579f19476d0d668f726f8dffec, purchase_count: 2
844. product_id_1: d1c427060a0f73f6b889a5c7c61f2ac4, product_id_2: 52c80cedd4e90108bf4fa6a206ef6b03, purchase_count: 2
845. product_id_1: 345ebf31824c3871cbb94c377190d6f9, product_id_2: 3743820de2227103b72b029a352fb98b, purchase_count: 2
846. product_id_1: 056d012d264624accb7f73d31caee034, product_id_2: 592962829d5a715304344e656e39108a, purchase_count: 2
847. product_id_1: 747152211829957938862c1c57a30f16, product_id_2: 7dfced4c66ef7bd85f2e30eec92e1b34, purchase_count: 2
848. product_id_1: 8ee57a1f636eb2e009706bbdb0818ecc, product_id_2: 3e7d7087ff8bbc0e9568b56ba3504a34, purchase_count: 2
849. product_id_1: 7486542600afc050d20740e976ff87f8, product_id_2: 6f46359e56f51d5deded13adcd1c255c, purchase_count: 2
850. product_id_1: ff26009ac6b838dc6cffa2d589cdbefb, product_id_2: 6d3d8ade6b793a08b041b6bc653c08ca, purchase_count: 2
851. product_id_1: d1fbb5683c8e93f314d0f2bf40d07761, product_id_2: 382db2ed3015c04d4b844d2a0712494c, purchase_count: 2
852. product_id_1: acebea1efbaa063642166633d247aec7, product_id_2: be0e6c61c2bcdd9a4d022ba67fd66189, purchase_count: 2
853. product_id_1: 7486542600afc050d20740e976ff87f8, product_id_2: 7698c2e9ec5dc2b70af8c1c8ac245cae, purchase_count: 2
854. product_id_1: 7486542600afc050d20740e976ff87f8, product_id_2: 7f9e40aa498f8f6edf4cc51215ecce9e, purchase_count: 2
855. product_id_1: 7486542600afc050d20740e976ff87f8, product_id_2: 8d28eb3a7309368ca0de19e016266251, purchase_count: 2
856. product_id_1: ff6caf9340512b8bf6d2a2a6df032cfa, product_id_2: 90a57d62c9b9f884fae33a10dff953b4, purchase_count: 2
857. product_id_1: d23750d75ff07de540c45749fbd8de45, product_id_2: 7868a64aa111bbb4f41f8e1146c0becb, purchase_count: 2
858. product_id_1: 748b719f4cbfdcb99cae90bf4bb16217, product_id_2: 40639ced9d62eca7f4637b1be4ccdf44, purchase_count: 2
859. product_id_1: ad0a798e7941f3a5a2fb8139cb62ad78, product_id_2: 23ab7bb9eac81e85ec43ed71064cf7ce, purchase_count: 2
860. product_id_1: 2b4609f8948be18874494203496bc318, product_id_2: b1acb7e8152c90c9619897753a75c973, purchase_count: 2
861. product_id_1: d25bbb182b51d1594fe3b54a27ae143e, product_id_2: 17d8b8e9c21ec0fc5b33724e32fe422e, purchase_count: 2
862. product_id_1: d25bbb182b51d1594fe3b54a27ae143e, product_id_2: 6a0713a63e990052795623e76cc2995e, purchase_count: 2
863. product_id_1: ff95ac47246ef13e48712ea1ff8df0d9, product_id_2: cd489785324bc65510f5a0ea2382f1d3, purchase_count: 2
864. product_id_1: ad0a798e7941f3a5a2fb8139cb62ad78, product_id_2: ae7fbf136a49b58f2d38fafb2f3205b8, purchase_count: 2
865. product_id_1: 74939659dbb10592e383bebf2f78272c, product_id_2: 23ab7bb9eac81e85ec43ed71064cf7ce, purchase_count: 2
866. product_id_1: 0cf1296fa38622de944eb05701b4ff34, product_id_2: a0627b01409b61f4076a920265b86665, purchase_count: 2
867. product_id_1: 407a9382e8c7e321e8ecee388edf0f7b, product_id_2: 1c1dda7d5b3d50618aadda35edc2acd6, purchase_count: 2
868. product_id_1: 407a9382e8c7e321e8ecee388edf0f7b, product_id_2: 3fa864b2eb9bb60d23bfe315213bb5d9, purchase_count: 2
869. product_id_1: 8f7ae8d7845cdabafb4b6f20d8bc5a43, product_id_2: 44e6ec37a142be331fe0241006d0b389, purchase_count: 2
870. product_id_1: 407a9382e8c7e321e8ecee388edf0f7b, product_id_2: d69b7880f262ed14de5f8149d2f0931d, purchase_count: 2
871. product_id_1: 23ab7bb9eac81e85ec43ed71064cf7ce, product_id_2: 74939659dbb10592e383bebf2f78272c, purchase_count: 2
872. product_id_1: 23ab7bb9eac81e85ec43ed71064cf7ce, product_id_2: 946344697156947d846d27fe0d503033, purchase_count: 2
873. product_id_1: 40a4dfa74a737d541b3c2413edf9cdf6, product_id_2: ec2d43cc59763ec91694573b31f1c29a, purchase_count: 2
874. product_id_1: d2c7a1e57b8f3e74095798f867334b36, product_id_2: 69523f67543ff9ea6b1a15858fb59b3b, purchase_count: 2
875. product_id_1: 5ed1d686373e3b3a2ddd9a4ce44f3fb2, product_id_2: a8bf9a06bef0fe4106c1fc0df21a5eb6, purchase_count: 2
876. product_id_1: 8fbf10c92c593a27da5034795db5d8b6, product_id_2: b729b323907bd67bdadd1920e349cb25, purchase_count: 2
877. product_id_1: 5ed9eaf534f6936b51d0b6c5e4d5c2e9, product_id_2: 0cf41187284d7f099adc8415a743ebbd, purchase_count: 2
878. product_id_1: 756feaccd3c677658c9e70bf09ef43b9, product_id_2: 48282b524c93e69ec5653481e2b8a237, purchase_count: 2
879. product_id_1: 23ab7bb9eac81e85ec43ed71064cf7ce, product_id_2: ad0a798e7941f3a5a2fb8139cb62ad78, purchase_count: 2
880. product_id_1: 0152f69b6cf919bcdaf117aa8c43e5a2, product_id_2: 642a40d4d73b4b2604968937de13634a, purchase_count: 2
881. product_id_1: 5ef336462ba740ddd4727319e26207e6, product_id_2: ee72ae8f6d0b11d7f04230fc894d7e39, purchase_count: 2
882. product_id_1: 1ce5b88456351c3b986532265a56d223, product_id_2: 35afc973633aaeb6b877ff57b2793310, purchase_count: 2
883. product_id_1: ae52eeb8383b94455f0a08b1f88ad002, product_id_2: e3323b0d3f79bdf85b58561d2218bc12, purchase_count: 2
884. product_id_1: 757172573ef8a2cc354243f3da4fa565, product_id_2: a44edbb4226328a7a816f3460556d638, purchase_count: 2
885. product_id_1: d315b738a6e96f4d9710af966cb7cd5b, product_id_2: f8077831f3c3f393fb67b93c5acd8daf, purchase_count: 2
886. product_id_1: d31604dc8480ff739e226bdf88d5000e, product_id_2: af25257adf28d8a0c281173073c2f2da, purchase_count: 2
887. product_id_1: 1d0b9497ac4f258fbd822c52ff61b5f4, product_id_2: fb2f2ec90b4ee90ad257bbf89d01247e, purchase_count: 2
888. product_id_1: 759d6e247dae636cc8e135f50052865e, product_id_2: b73f6899a58fe7a37e55149e9a11c717, purchase_count: 2
889. product_id_1: 5f0bdec2fb222061ed8fe52586a5957d, product_id_2: 88bd8458fdc2ceec3e71ef1d867a7b45, purchase_count: 2
890. product_id_1: 4f0abfbee7569e43b80f9aaa256a9bf8, product_id_2: 3a362c0e7f9a69276e2d95869a3e143b, purchase_count: 2
891. product_id_1: 17d8b8e9c21ec0fc5b33724e32fe422e, product_id_2: 99444c1e11fc38755dae86f5c67d3d1a, purchase_count: 2
892. product_id_1: ae7fbf136a49b58f2d38fafb2f3205b8, product_id_2: ad0a798e7941f3a5a2fb8139cb62ad78, purchase_count: 2
893. product_id_1: 4f0abfbee7569e43b80f9aaa256a9bf8, product_id_2: 5f42d57952b7815098979a5c4fa6f82a, purchase_count: 2
894. product_id_1: 5f42d57952b7815098979a5c4fa6f82a, product_id_2: 4f0abfbee7569e43b80f9aaa256a9bf8, purchase_count: 2
895. product_id_1: 5f42d57952b7815098979a5c4fa6f82a, product_id_2: 6463e442310f2f4f321c83a32d8c662b, purchase_count: 2
896. product_id_1: d34efb58e1930773fcde9b951892b1b1, product_id_2: 161ccc972b7b25a5e2d43376b8b333c5, purchase_count: 2
897. product_id_1: 4f0abfbee7569e43b80f9aaa256a9bf8, product_id_2: 8d4dac6177fb8134f26fb4c5cc6c0aff, purchase_count: 2
898. product_id_1: 75c06ee06b201f9b6301d2b5e72993f8, product_id_2: 005030ef108f58b46b78116f754d8d38, purchase_count: 2
899. product_id_1: 5f6906793eb1d554d76c39398ce08693, product_id_2: d41a23bd2bc3ec10cfffc66c0611a290, purchase_count: 2
900. product_id_1: aecdd1c18af2379312e946f33280fe25, product_id_2: 6ed93af03d1f53308d3a9c6555a94d08, purchase_count: 2
901. product_id_1: 90916a1ae9ea5e3c8c15c37b51834f37, product_id_2: 1a06a6a66ab23d70e02b8f92650e268f, purchase_count: 2
902. product_id_1: 1d1183a8de24782a216dc5066d7421bf, product_id_2: cf1d8e226162a1d0ad61f29b7ed72d82, purchase_count: 2
903. product_id_1: 909b87db6cb3a7ab26bd03cc59860136, product_id_2: 3dd2a17168ec895c781a9191c1e95ad7, purchase_count: 2
904. product_id_1: d3a386ad58b99f0ddcc216ed9efb03c3, product_id_2: a3a10562c9d134b92f04b8cce298d037, purchase_count: 2
905. product_id_1: 40cb7bb3d30559b9b6c4fb62bc837962, product_id_2: ce98361ef1341e15087ae4b1b2c53fdd, purchase_count: 2
906. product_id_1: 17d8b8e9c21ec0fc5b33724e32fe422e, product_id_2: d25bbb182b51d1594fe3b54a27ae143e, purchase_count: 2
907. product_id_1: 40f9995eecfc68f54991ca49582e9885, product_id_2: 9e10eb05d9f369d5c38c475425cc2ee9, purchase_count: 2
908. product_id_1: 90a57d62c9b9f884fae33a10dff953b4, product_id_2: b88d27345de2feed45475bb48cca74b1, purchase_count: 2
909. product_id_1: 90a57d62c9b9f884fae33a10dff953b4, product_id_2: ff6caf9340512b8bf6d2a2a6df032cfa, purchase_count: 2
910. product_id_1: 1d1e5ff7c1fe84990f92d41f7425b789, product_id_2: 8ab78b6f871fd72d1ef38097498b70b7, purchase_count: 2
911. product_id_1: 34b91723112fa9ebf6b4d6b4db4a6741, product_id_2: 98669593a93035fced33e5280aa30641, purchase_count: 2
912. product_id_1: af25257adf28d8a0c281173073c2f2da, product_id_2: d31604dc8480ff739e226bdf88d5000e, purchase_count: 2
913. product_id_1: 17d8b8e9c21ec0fc5b33724e32fe422e, product_id_2: e95fb3a80ca294f39de925b6428f3a32, purchase_count: 2
914. product_id_1: af35be35db4ad0dc288b571453337376, product_id_2: 2548af3e6e77a690cf3eb6368e9ab61e, purchase_count: 2
915. product_id_1: af35be35db4ad0dc288b571453337376, product_id_2: 5aad359a63cbb4fc35ead44346a3eeb4, purchase_count: 2
916. product_id_1: 90b58782fdd04cb829667fcc41fb65f5, product_id_2: 508d5e8ce8e79bb506f9f0c096b295c4, purchase_count: 2
917. product_id_1: 2b9b580cdc992e165ca0336a078d695f, product_id_2: 8ed3ae310714d18ee990923aeb411508, purchase_count: 2
918. product_id_1: d3e112316bd3ae29280cec26bd3059fd, product_id_2: c2ece64199af7a53793ed9612a89a8cd, purchase_count: 2
919. product_id_1: 3512f777c335f8297b5ad43416b69cf8, product_id_2: 7f9f228320c43765cfe30cdc090e0be4, purchase_count: 2
920. product_id_1: 90ed53d34bfcb4fa1e90656068dd04bc, product_id_2: 65650c84064ff1a79e4a05988f4c3e9f, purchase_count: 2
921. product_id_1: 4f88323d03ffaf090b8fb0116b33c95e, product_id_2: 592962829d5a715304344e656e39108a, purchase_count: 2
922. product_id_1: 0cf2faf9749f53924cea652a09d8e327, product_id_2: 0de59eddc63167215c972b0d785ffa7b, purchase_count: 2
923. product_id_1: 91472a5abca63bed91ade04c71c203ce, product_id_2: 82cff05560eae73466f8778690b037fa, purchase_count: 2
924. product_id_1: d41a23bd2bc3ec10cfffc66c0611a290, product_id_2: 5f6906793eb1d554d76c39398ce08693, purchase_count: 2
925. product_id_1: 765a8070ece0f1383d0f5faf913dfb9b, product_id_2: a41e356c76fab66334f36de622ecbd3a, purchase_count: 2
926. product_id_1: 414c53fa9c5cc4a0390682aeb2e25ec1, product_id_2: 158102fe543dbaeb84d87811bfe06d0d, purchase_count: 2
927. product_id_1: 134afbb1d3ef60a407f8e4491dd63622, product_id_2: e27e689c4ce425f2fe7e2a270fd4d2db, purchase_count: 2
928. product_id_1: 4167a7ae0930579d1f27d465a1a042f0, product_id_2: c589625c8ccc7bfd2e8f1fb041e24c4a, purchase_count: 2
929. product_id_1: d498e8a880bdf3d26e2b9b3e92c4f424, product_id_2: 887dba291adc295b57b5778ebc8b4060, purchase_count: 2
930. product_id_1: 7698c2e9ec5dc2b70af8c1c8ac245cae, product_id_2: 7486542600afc050d20740e976ff87f8, purchase_count: 2
931. product_id_1: 0a9bdadab17a9b0f258f64d11a0adf7b, product_id_2: 3eef0cb94ba82de806bb30ab743c7655, purchase_count: 2
932. product_id_1: 4fcb3d9a5f4871e8362dfedbdb02b064, product_id_2: 0c9ff9d8ed9b9bdd825487b3a66e05f5, purchase_count: 2
933. product_id_1: d4dccae17c83ffbaafc50d763503e9eb, product_id_2: bb3a346d0fc86850244000d0fe5bf5dd, purchase_count: 2
934. product_id_1: b01cedfa96d891427058852f0625e9ee, product_id_2: fa94f25a73969e3a25d52706e246dfcc, purchase_count: 2
935. product_id_1: 4fe644d766c7566dbc46fb851363cb3b, product_id_2: 78efe838c04bbc568be034082200ac20, purchase_count: 2
936. product_id_1: 0cf2faf9749f53924cea652a09d8e327, product_id_2: 309dd69eb83cea38c51709d62befe1a4, purchase_count: 2
937. product_id_1: d4fa7c305b2ffd07d12ae5a886b6cb0f, product_id_2: 2d78dc9b1f4a5d1ceb28287b82d85b86, purchase_count: 2
938. product_id_1: 35afc973633aaeb6b877ff57b2793310, product_id_2: 1ce5b88456351c3b986532265a56d223, purchase_count: 2
939. product_id_1: 1dc7685f4fdb9622d84ae2ec658d5bbf, product_id_2: a46875fb5b8d19ac3cff18deb9bae57e, purchase_count: 2
940. product_id_1: 1dc7685f4fdb9622d84ae2ec658d5bbf, product_id_2: b7d2c90f9161dc69fa75d22572003bc4, purchase_count: 2
941. product_id_1: b0528299d65ab35e3ed853f6a853b8b8, product_id_2: 6abd84909e8ed79ef808c16f90b91093, purchase_count: 2
942. product_id_1: 924c635d837c240da3956f3c28c1e6f4, product_id_2: a519511d5c5c1153c9f636288e50f819, purchase_count: 2
943. product_id_1: d55d2479e56093f23ebcf313ceb3bcfe, product_id_2: 43f1e9b31236ad9ef63197b36bf00dbc, purchase_count: 2
944. product_id_1: 41da75141264c3bde21ecea85a4cb8b7, product_id_2: 9ddd762ee8a13576a809dc66f22aa2b5, purchase_count: 2
945. product_id_1: d57df0660328af2e535fa009f227d575, product_id_2: efa91c03c750cf82e0e9fc5523aca73c, purchase_count: 2
946. product_id_1: 7703b8cb5b77fbb36518ea91e2ca734f, product_id_2: 6c55ba2343f9df32c7f88a468352ff22, purchase_count: 2
947. product_id_1: b0961721fd839e9982420e807758a2a6, product_id_2: 368c6c730842d78016ad823897a372db, purchase_count: 2
948. product_id_1: b0961721fd839e9982420e807758a2a6, product_id_2: 389d119b48cf3043d311335e499d9c6b, purchase_count: 2
949. product_id_1: 7703b8cb5b77fbb36518ea91e2ca734f, product_id_2: 7dac8901a50cf3317d5372cbd3186ecd, purchase_count: 2
950. product_id_1: b09790edda54333116f9cf1decc580a1, product_id_2: 422b4786464320e3645a7e018ba60d8e, purchase_count: 2
951. product_id_1: 35afc973633aaeb6b877ff57b2793310, product_id_2: cf54cbfe4e33bc8f7b34a65da576497c, purchase_count: 2
952. product_id_1: d5b703c271f43f9c588a6f512a00f77e, product_id_2: 8d98dedc3c19de17f1a090195e85d6b6, purchase_count: 2
953. product_id_1: 7736ea239e147291f6adb766c992beb1, product_id_2: 642a40d4d73b4b2604968937de13634a, purchase_count: 2
954. product_id_1: 60a8d8f0434c4531bf310eebf9f19cfe, product_id_2: e30aaafe45e34ce07003ef0cfcb6e49d, purchase_count: 2
955. product_id_1: 774e21c631ca26cba7b5606bdca7460f, product_id_2: 0bcc3eeca39e1064258aa1e932269894, purchase_count: 2
956. product_id_1: 42155695adbe665066ad812855fe523a, product_id_2: 372645c7439f9661fbbacfd129aa92ec, purchase_count: 2
957. product_id_1: 0f91b6a95a57a43203a9b17de98960d9, product_id_2: fbc1488c1a1e72ba175f53ab29a248e8, purchase_count: 2
958. product_id_1: d64738c7b2e2d1778a51e835d8f02568, product_id_2: a3a10562c9d134b92f04b8cce298d037, purchase_count: 2
959. product_id_1: 775cbb352638cb5e59cea1637da006cc, product_id_2: 48282b524c93e69ec5653481e2b8a237, purchase_count: 2
960. product_id_1: d65b6607952f9e0d705b1cbdc92ac027, product_id_2: c43ab4269cbf91b373263db4c2973cad, purchase_count: 2
961. product_id_1: d678178aa4291cd25a755a90188375c8, product_id_2: 7b5d8be0e04080e4c8ee6a7ec2f1f597, purchase_count: 2
962. product_id_1: 93d8b11d613a563f5a26212282bb145e, product_id_2: be0e6c61c2bcdd9a4d022ba67fd66189, purchase_count: 2
963. product_id_1: d678178aa4291cd25a755a90188375c8, product_id_2: eb8c629f70275fd1c4f809116cce1efc, purchase_count: 2
964. product_id_1: 508d5e8ce8e79bb506f9f0c096b295c4, product_id_2: 90b58782fdd04cb829667fcc41fb65f5, purchase_count: 2
965. product_id_1: 2c3f424b5643b03663e0f5861dde2bfe, product_id_2: 39b146e69c32ffe0a469e95a71585843, purchase_count: 2
966. product_id_1: 422879e10f46682990de24d770e7f83d, product_id_2: 4e1346d7b7e02c737a366b086462e33e, purchase_count: 2
967. product_id_1: 944a8fa6055b8213f9e715720d4e2d5c, product_id_2: 1a06a6a66ab23d70e02b8f92650e268f, purchase_count: 2
968. product_id_1: 0fa81e7123fd0ebe03adbbe99d912827, product_id_2: 1eaf224c19e07b6e50bf0119eea1dd26, purchase_count: 2
969. product_id_1: d69b7880f262ed14de5f8149d2f0931d, product_id_2: 407a9382e8c7e321e8ecee388edf0f7b, purchase_count: 2
970. product_id_1: 186fe07c8b8005ec6a498587ffbc1352, product_id_2: 0bdd9a52d192d64770e33ae559512478, purchase_count: 2
971. product_id_1: 2c446ef2d2415f2c802a41573824282d, product_id_2: dca43bf1f5d44f76105f0633b7fd7ea1, purchase_count: 2
972. product_id_1: 946344697156947d846d27fe0d503033, product_id_2: 23ab7bb9eac81e85ec43ed71064cf7ce, purchase_count: 2
973. product_id_1: b114bf337c0626166abe574eee9e3f32, product_id_2: b9311d581f5f341576a5a2892168355c, purchase_count: 2
974. product_id_1: 03d817e5e392e78674ed0bd8195f9159, product_id_2: 33e503f68fb60fe165ed992965f2c737, purchase_count: 2
975. product_id_1: 3625fbaf8284047185fb0351f2f84ae3, product_id_2: 88c20c5a22f2ca169af8cfc2df00a7a2, purchase_count: 2
976. product_id_1: 61b6e5d2e3ee58d2b341b8ef1a652b26, product_id_2: a3a10562c9d134b92f04b8cce298d037, purchase_count: 2
977. product_id_1: 422b4786464320e3645a7e018ba60d8e, product_id_2: 2647221a6a477afe2d0268b378f1fdcd, purchase_count: 2
978. product_id_1: 422b4786464320e3645a7e018ba60d8e, product_id_2: b09790edda54333116f9cf1decc580a1, purchase_count: 2
979. product_id_1: 0fa81e7123fd0ebe03adbbe99d912827, product_id_2: 87d780fa7d2cf3710aa02dc4ca8db985, purchase_count: 2
980. product_id_1: 1eaf224c19e07b6e50bf0119eea1dd26, product_id_2: 0fa81e7123fd0ebe03adbbe99d912827, purchase_count: 2
981. product_id_1: 61fd556e5319f0e1dfed3ecb8d3bb778, product_id_2: 47fafa6908e75ae62b8a36a9eb3b9234, purchase_count: 2
982. product_id_1: 61fd556e5319f0e1dfed3ecb8d3bb778, product_id_2: 7ee8a1b1807716291e12649b1d617896, purchase_count: 2
983. product_id_1: 2481a472d98c582b46bc2dfeae6f539f, product_id_2: 665aa1d687284a4d2d2b74c0c6724625, purchase_count: 2
984. product_id_1: b1acb7e8152c90c9619897753a75c973, product_id_2: 2b4609f8948be18874494203496bc318, purchase_count: 2
985. product_id_1: d730dcd6017ae7bc8a4b5561f18c6d59, product_id_2: e389381479408ccdcdd406d8d3049e45, purchase_count: 2
986. product_id_1: 3685c687db4b3d2da5085d23b408e93a, product_id_2: b9e247fc923da7d723c2545b76efe01e, purchase_count: 2
987. product_id_1: 6217dab6fce05a4924116e90d7f301c1, product_id_2: d9339c5714743c460a9470730f79f6c5, purchase_count: 2
988. product_id_1: 4255ef536732efe235477ace2dccd393, product_id_2: 18fa9cc25ea8b54f32d029f261673c0f, purchase_count: 2
989. product_id_1: 4255ef536732efe235477ace2dccd393, product_id_2: 4a5c3967bfd3629fe07ef4d0cc8c3818, purchase_count: 2
990. product_id_1: 4255ef536732efe235477ace2dccd393, product_id_2: a88124e0b1d42ca7b0813a78ff630437, purchase_count: 2
991. product_id_1: 2481a472d98c582b46bc2dfeae6f539f, product_id_2: 7a0f37fda63d1cd7dac2451494eb6e69, purchase_count: 2
992. product_id_1: d80fce9f775927c7d602c2de926759f1, product_id_2: a3a10562c9d134b92f04b8cce298d037, purchase_count: 2
993. product_id_1: 94972ba3b1856e8453d8a0b4d522aa36, product_id_2: 46d9734c42793de762a7ca5db95ecdd1, purchase_count: 2
994. product_id_1: 186fe07c8b8005ec6a498587ffbc1352, product_id_2: 6c55ba2343f9df32c7f88a468352ff22, purchase_count: 2
995. product_id_1: 781afe929e3016a667f5f439afd55fce, product_id_2: 1c8c80454d9a8829112d5be9fe885fab, purchase_count: 2
996. product_id_1: 51250f90d798d377a1928e8a4e2e9ae1, product_id_2: 005030ef108f58b46b78116f754d8d38, purchase_count: 2
997. product_id_1: 427a9f5e8a9d47c60adc5ae34e2657d2, product_id_2: d102ed54656bd3eaf5bd365494e08bf6, purchase_count: 2
998. product_id_1: d85ee6b5fa57f68444d86f77b51ae69d, product_id_2: dde1e366db6c0e996f4e1d92122b431c, purchase_count: 2
999. product_id_1: b2775a101dfacb48184ed1c1cb4a278b, product_id_2: 29b18b99ca3c94cea05efa9e11465440, purchase_count: 2
1000. product_id_1: 186fe07c8b8005ec6a498587ffbc1352, product_id_2: 7dac8901a50cf3317d5372cbd3186ecd, purchase_count: 2
1001. product_id_1: d8c0c707d3724304033f593878cbf1e6, product_id_2: 2ae501b303a5a8e6f75c8c36f366b2d5, purchase_count: 2
1002. product_id_1: 628d0ba951ebb8fd1edc5ab3934468e0, product_id_2: e0eb83f5cf9560ca3b976eea5dcfdfde, purchase_count: 2
1003. product_id_1: 020a80cb704bf65f38761fcedf2af192, product_id_2: f940327804bdcb40342a12c93de069b8, purchase_count: 2
1004. product_id_1: 24baefeed71136f90df0149ca1e85c49, product_id_2: 3dc7db1edfac20883ed35ecfec05a3cc, purchase_count: 2
1005. product_id_1: b2b938c46aafdbf702d73e7edb9cb263, product_id_2: def59eb2e17b32b980b5341984f6b500, purchase_count: 2
1006. product_id_1: d902ca64b614964dc31d6b0372e800ac, product_id_2: 8b3a9476f74f5297f7ff0ec6d95fe1ea, purchase_count: 2
1007. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: 0b13080e2bf193c4ff096b09e0758c7d, purchase_count: 2
1008. product_id_1: 7868a64aa111bbb4f41f8e1146c0becb, product_id_2: d23750d75ff07de540c45749fbd8de45, purchase_count: 2
1009. product_id_1: d9339c5714743c460a9470730f79f6c5, product_id_2: 6217dab6fce05a4924116e90d7f301c1, purchase_count: 2
1010. product_id_1: d93e0523fc2cc1c5a81d432364ed2d06, product_id_2: 6610dc3cac3b77009d969495cc2d7037, purchase_count: 2
1011. product_id_1: b2e7c39bb137bb4b3651862c6b611468, product_id_2: 7bf115809ab249f1bf0fa92d72e0baf8, purchase_count: 2
1012. product_id_1: 7893c68e0a8b6e58a70390551e8a84d9, product_id_2: ec8ae427905e10052ee4f1e9993b6763, purchase_count: 2
1013. product_id_1: 78efe838c04bbc568be034082200ac20, product_id_2: 4fe644d766c7566dbc46fb851363cb3b, purchase_count: 2
1014. product_id_1: 516ccdc0667fe7e260156d1998ef9546, product_id_2: 8d7d29e5fb9ff5333009326c87fc04e9, purchase_count: 2
1015. product_id_1: 5173e870df52b09d6b76f88504a1991d, product_id_2: 271a16e4751b04867238b601ad652692, purchase_count: 2
1016. product_id_1: 429e7401fafb76436f15e86498bd7364, product_id_2: 9ddd762ee8a13576a809dc66f22aa2b5, purchase_count: 2
1017. product_id_1: 62d8daeee0db3a60c234c2d1bfd10651, product_id_2: 9cbe4a1fd4db99c14512e9b2ff033ec4, purchase_count: 2
1018. product_id_1: d9e7d13814ea50f9ae1f612ef6b3a1f1, product_id_2: 82cff05560eae73466f8778690b037fa, purchase_count: 2
1019. product_id_1: 42a2bd596fda1baef5719cb74f73030c, product_id_2: 283dc451ad3918badb976d56ff887289, purchase_count: 2
1020. product_id_1: 42a2bd596fda1baef5719cb74f73030c, product_id_2: 430f4c8e02bd4e1fe6330c38689b54f3, purchase_count: 2
1021. product_id_1: da051bd767b7457572d55aba23fd846a, product_id_2: c0295f791bfc794623d0ea811cca82d5, purchase_count: 2
1022. product_id_1: 9614dd0585b52cd086cbdcc2dd5fcda4, product_id_2: 79fca321dbd3453bd8211690e39f1659, purchase_count: 2
1023. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: 8273821fd2a32fbbc77ad8b743b2a1b9, purchase_count: 2
1024. product_id_1: da7813106f94601e6022f50017299e2f, product_id_2: 33e503f68fb60fe165ed992965f2c737, purchase_count: 2
1025. product_id_1: 186fe07c8b8005ec6a498587ffbc1352, product_id_2: 87cb507e0daa37bbf34956fd59eba832, purchase_count: 2
1026. product_id_1: 13befae9b3fb34c439cf4744fd18dfa7, product_id_2: 38956cecc0bc8d8837371d0aeeefeb59, purchase_count: 2
1027. product_id_1: 962a6951154f98f2c8e9a5b8b2bcf4a9, product_id_2: b532349fe46b38fbc7bb3914c1bdae07, purchase_count: 2
1028. product_id_1: 962a6951154f98f2c8e9a5b8b2bcf4a9, product_id_2: cfe9e8e1f0400c8cc665d41722f34086, purchase_count: 2
1029. product_id_1: b3c13ca98fb6f9dd5c6aec8b1d353506, product_id_2: 6f3b5b605d91b7439c5e3f5a8dffeea7, purchase_count: 2
1030. product_id_1: b3cf0a98f31b76ed0cec13d9c77102c4, product_id_2: 9d0bb30eed80184666c8acad23921283, purchase_count: 2
1031. product_id_1: 79fca321dbd3453bd8211690e39f1659, product_id_2: 9614dd0585b52cd086cbdcc2dd5fcda4, purchase_count: 2
1032. product_id_1: 7a0f37fda63d1cd7dac2451494eb6e69, product_id_2: 2481a472d98c582b46bc2dfeae6f539f, purchase_count: 2
1033. product_id_1: 7a0f37fda63d1cd7dac2451494eb6e69, product_id_2: 3e5201fe0d1ba474d9b90152c83c706c, purchase_count: 2
1034. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: b0961721fd839e9982420e807758a2a6, purchase_count: 2
1035. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: be0a8cb3c50011daec32f4d8ecdccb28, purchase_count: 2
1036. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: cec09725da5ed01471d9a505e7389d37, purchase_count: 2
1037. product_id_1: daf84c8f6a77308759733b317cf20666, product_id_2: 3eef0cb94ba82de806bb30ab743c7655, purchase_count: 2
1038. product_id_1: 7a0f37fda63d1cd7dac2451494eb6e69, product_id_2: cd3de1984e1a77b441e1b39b8e334330, purchase_count: 2
1039. product_id_1: db123b35396aafabb2d5b476557abed5, product_id_2: 7c65bcd66be0ad761948bfeda4e7bd2f, purchase_count: 2
1040. product_id_1: 0cf41187284d7f099adc8415a743ebbd, product_id_2: 5ed9eaf534f6936b51d0b6c5e4d5c2e9, purchase_count: 2
1041. product_id_1: db1d1a4569fdbae28a0d3340d907f7af, product_id_2: 1c56f826f3a1fdf255e3fb5fa7637d3e, purchase_count: 2
1042. product_id_1: 51edddbbc47a477259e672bd291feed6, product_id_2: ec2d43cc59763ec91694573b31f1c29a, purchase_count: 2
1043. product_id_1: 430f4c8e02bd4e1fe6330c38689b54f3, product_id_2: 42a2bd596fda1baef5719cb74f73030c, purchase_count: 2
1044. product_id_1: 36ba5561e351eef68d3554697132a9a8, product_id_2: 53c61580d8e5c4941a358ee0335c1d5c, purchase_count: 2
1045. product_id_1: 2ccd049c8e7ea210e079a1aa8ad92477, product_id_2: c784a651cf319526cc7cf854f83cb941, purchase_count: 2
1046. product_id_1: 0cf41187284d7f099adc8415a743ebbd, product_id_2: c2a9f8aeb7a51580fccc2d1c4f8bceaf, purchase_count: 2
1047. product_id_1: 2ce17ef87d6bb64be1a0b36a4a614ced, product_id_2: a2ba5bcfe3ee03832bf8f324caa32dad, purchase_count: 2
1048. product_id_1: db7f3f42ccab32fa6328b3063b278bcc, product_id_2: f6e3aeb40c00aec24ade8333c2ac1b20, purchase_count: 2
1049. product_id_1: b532349fe46b38fbc7bb3914c1bdae07, product_id_2: 962a6951154f98f2c8e9a5b8b2bcf4a9, purchase_count: 2
1050. product_id_1: 0950783476d3f6529a03b28fcac219d1, product_id_2: 6bd4c564d1f96b0db5d02d376b4daed6, purchase_count: 2
1051. product_id_1: b53f20c2b12a4b9821ce57f46a7d1cae, product_id_2: b8ded693eefc7fd6fae337f6c202093e, purchase_count: 2
1052. product_id_1: 521527593ca1726b992318e034dd5690, product_id_2: a25583531530c0913ea4dee2c5c73685, purchase_count: 2
1053. product_id_1: 02ed3b595447e948efc3eac897e4df0e, product_id_2: 71b157e39523e25558ed9cc1960c3fbd, purchase_count: 2
1054. product_id_1: b57469faf40b556e16b9a49308953700, product_id_2: b8411dee248601bc460bac8e1fb8a102, purchase_count: 2
1055. product_id_1: 524d0ebe9a59d96dfaa2983b54a50c15, product_id_2: 47b0f8596ee6dafbb4438cac16fa6275, purchase_count: 2
1056. product_id_1: b5a47689050b1900fd74aa6b431579a7, product_id_2: 38f894aa22356ddb9e98478fbc016083, purchase_count: 2
1057. product_id_1: b5a47689050b1900fd74aa6b431579a7, product_id_2: bff2390f68a7b76b01ef61b684888261, purchase_count: 2
1058. product_id_1: 96b0a882d11b17ce51238420ec63e3a1, product_id_2: dce24381876a1d59ccc9d00d3dbade56, purchase_count: 2
1059. product_id_1: 642a40d4d73b4b2604968937de13634a, product_id_2: 0152f69b6cf919bcdaf117aa8c43e5a2, purchase_count: 2
1060. product_id_1: 014a8a503291921f7b004a5215bb3c36, product_id_2: 14dffa241a078aeaebaef48a49e807ca, purchase_count: 2
1061. product_id_1: 2d15b61e2962412ec20c326895c4603a, product_id_2: 37318ccebb2ced72bd1b548b55ab4e31, purchase_count: 2
1062. product_id_1: 642a40d4d73b4b2604968937de13634a, product_id_2: 7736ea239e147291f6adb766c992beb1, purchase_count: 2
1063. product_id_1: 0981ba54d8ddc68299f7c7a7d23bb2c9, product_id_2: 6522b16614da30655a6a5ce4c8f2fb8b, purchase_count: 2
1064. product_id_1: dc52f0f5d3ec37a93eaf956cde4e5d2c, product_id_2: a92930c327948861c015c919a0bcb4a8, purchase_count: 2
1065. product_id_1: 96ea4f32befa14bd8ab36fd6827a5e3f, product_id_2: 731599825523e54feea5f4678ca8f54f, purchase_count: 2
1066. product_id_1: b627957ffcd19ace5037a5df4230d1fa, product_id_2: 2b3ded25b94fa59143322115fce48003, purchase_count: 2
1067. product_id_1: dca43bf1f5d44f76105f0633b7fd7ea1, product_id_2: 2c446ef2d2415f2c802a41573824282d, purchase_count: 2
1068. product_id_1: 96ea4f32befa14bd8ab36fd6827a5e3f, product_id_2: bf477d995ee4444807afc574cfbcc1c1, purchase_count: 2
1069. product_id_1: 6463e442310f2f4f321c83a32d8c662b, product_id_2: 5f42d57952b7815098979a5c4fa6f82a, purchase_count: 2
1070. product_id_1: dce24381876a1d59ccc9d00d3dbade56, product_id_2: 96b0a882d11b17ce51238420ec63e3a1, purchase_count: 2
1071. product_id_1: b63ecf99904f905e0d594b11ac06281e, product_id_2: 29bc923d3ecb389b5b1b6fe2a6e4799a, purchase_count: 2
1072. product_id_1: b65214d387c754bb0f858a4a5a0f41ad, product_id_2: 28447390cfd2a411fcb8c008b6163da2, purchase_count: 2
1073. product_id_1: dd0dcee76f9c12fff4bc0eb641d57c7f, product_id_2: 474bb6b54fc608ca71059a6c4f7ecda3, purchase_count: 2
1074. product_id_1: 372645c7439f9661fbbacfd129aa92ec, product_id_2: 120fa011365fc39efe382cba4e50999e, purchase_count: 2
1075. product_id_1: 7b49e585ac8c80b14c9b2815d4db465f, product_id_2: 1269d60fc5efbcf03e7eea49213091c6, purchase_count: 2
1076. product_id_1: 2d37d1dbcba865841a1c8cfab20ab9a1, product_id_2: cb5d3d2427c53fde437c52bde24840e8, purchase_count: 2
1077. product_id_1: 7b49e585ac8c80b14c9b2815d4db465f, product_id_2: 55363f487ca324087a49ddfcfb91b971, purchase_count: 2
1078. product_id_1: 7b5d8be0e04080e4c8ee6a7ec2f1f597, product_id_2: 5d6bea33648f018dbb563f3a2fab09f3, purchase_count: 2
1079. product_id_1: 7b5d8be0e04080e4c8ee6a7ec2f1f597, product_id_2: d678178aa4291cd25a755a90188375c8, purchase_count: 2
1080. product_id_1: 43b54d1fc56ff394092a3dff6be2d39f, product_id_2: 0a4f9f421af66d2ea061fbb8883419f7, purchase_count: 2
1081. product_id_1: 5292d2a10d727811b78d5b7dfb6c96b3, product_id_2: bdc1cae635cc5a6a09d9481495b890c6, purchase_count: 2
1082. product_id_1: 372645c7439f9661fbbacfd129aa92ec, product_id_2: 42155695adbe665066ad812855fe523a, purchase_count: 2
1083. product_id_1: dd6a505f83dd3c6326aa9856519e0978, product_id_2: 014a8a503291921f7b004a5215bb3c36, purchase_count: 2
1084. product_id_1: dd6a505f83dd3c6326aa9856519e0978, product_id_2: 880be32f4db1d9f6e2bec38fb6ac23ab, purchase_count: 2
1085. product_id_1: b6b220a6c539cb65be34eed6fea8fe63, product_id_2: 8cf22b2cc9465d64474a09853b62f5b2, purchase_count: 2
1086. product_id_1: 976ab50ce2361a9f99aaf9fd4037a00a, product_id_2: 9cc50a8fd6a69a4d287d62d52ee5d009, purchase_count: 2
1087. product_id_1: 52b668edc0d0c20cd9319bfda4019597, product_id_2: 8814a3da37fb9673a5ac06f82a2a00a9, purchase_count: 2
1088. product_id_1: 52c80cedd4e90108bf4fa6a206ef6b03, product_id_2: d1c427060a0f73f6b889a5c7c61f2ac4, purchase_count: 2
1089. product_id_1: 37318ccebb2ced72bd1b548b55ab4e31, product_id_2: 2d15b61e2962412ec20c326895c4603a, purchase_count: 2
1090. product_id_1: ddb9028236525b8ab493fc24f99e8d1a, product_id_2: e61c78a7343d82c0539d27df0f7dfc31, purchase_count: 2
1091. product_id_1: 7bf115809ab249f1bf0fa92d72e0baf8, product_id_2: b2e7c39bb137bb4b3651862c6b611468, purchase_count: 2
1092. product_id_1: ddbf57e4559f03c003fc3708d4860c5e, product_id_2: a3a10562c9d134b92f04b8cce298d037, purchase_count: 2
1093. product_id_1: 07c055536ebf10dfbb6c6db6dbfc36e5, product_id_2: 8338cef8355d238f43711dcb9c0657b2, purchase_count: 2
1094. product_id_1: 64fc6010136aa59736e148c404e77a54, product_id_2: 232a5adb0fc1881bbfeb03560c639c31, purchase_count: 2
1095. product_id_1: 37318ccebb2ced72bd1b548b55ab4e31, product_id_2: f9bdcb274f479aa71dd34e8bccdd9a82, purchase_count: 2
1096. product_id_1: dde1e366db6c0e996f4e1d92122b431c, product_id_2: d85ee6b5fa57f68444d86f77b51ae69d, purchase_count: 2
1097. product_id_1: 6522b16614da30655a6a5ce4c8f2fb8b, product_id_2: 0981ba54d8ddc68299f7c7a7d23bb2c9, purchase_count: 2
1098. product_id_1: 52faaea7e7d55dfe5aa81f0b5f79d7b9, product_id_2: fe55c83c8471a2fca643b9291c1f105e, purchase_count: 2
1099. product_id_1: 653b6b1217fba117599afcc015ffd50a, product_id_2: 4901f0f8eba79934ba3cdfa1fbc02893, purchase_count: 2
1100. product_id_1: b729b323907bd67bdadd1920e349cb25, product_id_2: 8fbf10c92c593a27da5034795db5d8b6, purchase_count: 2
1101. product_id_1: 145140d23f166a1166dc4437107df8cc, product_id_2: c2ad928095a0d199c4d44b2194119ce2, purchase_count: 2
1102. product_id_1: de17feec1983829fec4bc58cadaa43f3, product_id_2: 83bfae859f4a37b048a3abcecb17c506, purchase_count: 2
1103. product_id_1: 7c65bcd66be0ad761948bfeda4e7bd2f, product_id_2: db123b35396aafabb2d5b476557abed5, purchase_count: 2
1104. product_id_1: 189e539d996a9b8ba4bba1a140a024a7, product_id_2: a669398f595527fc03acc1ebda6b3cce, purchase_count: 2
1105. product_id_1: de37ff8068c8e7b1164a19f0f4d05619, product_id_2: f879fadd73c7b81f0b278dacc880cf08, purchase_count: 2
1106. product_id_1: b73f6899a58fe7a37e55149e9a11c717, product_id_2: 759d6e247dae636cc8e135f50052865e, purchase_count: 2
1107. product_id_1: b73f6899a58fe7a37e55149e9a11c717, product_id_2: 8d070077591cb06503a4933e5050bc69, purchase_count: 2
1108. product_id_1: 98669593a93035fced33e5280aa30641, product_id_2: 34b91723112fa9ebf6b4d6b4db4a6741, purchase_count: 2
1109. product_id_1: 7c6ae4d12d2754ca0826ad17792c554e, product_id_2: 9feeadd6b97835152e83e1b25b46f5c4, purchase_count: 2
1110. product_id_1: de92134fd940e9302d27c31af4581fbd, product_id_2: 457cd0a99cfa977993e4eb6d98d95abb, purchase_count: 2
1111. product_id_1: dea564fb3ed59db512cb4df9c491c1ef, product_id_2: 38cd38029795797c97b73421fdad08cf, purchase_count: 2
1112. product_id_1: dea564fb3ed59db512cb4df9c491c1ef, product_id_2: a50c606310374ff8660bbe03010e021b, purchase_count: 2
1113. product_id_1: 2d78dc9b1f4a5d1ceb28287b82d85b86, product_id_2: a0ef8572cd061badd81ffc48dc04d1fa, purchase_count: 2
1114. product_id_1: 43f1e9b31236ad9ef63197b36bf00dbc, product_id_2: d55d2479e56093f23ebcf313ceb3bcfe, purchase_count: 2
1115. product_id_1: 7c898e0b8ea203dd94ba846627fc34d1, product_id_2: 86f2416d4670e4ea3ca5494d043d9f24, purchase_count: 2
1116. product_id_1: 7ca5f56188492e30c50ba64de188aae7, product_id_2: 0152f69b6cf919bcdaf117aa8c43e5a2, purchase_count: 2
1117. product_id_1: def59eb2e17b32b980b5341984f6b500, product_id_2: b2b938c46aafdbf702d73e7edb9cb263, purchase_count: 2
1118. product_id_1: b791d5d05f0c974d148d358efcd21d84, product_id_2: cda960fc8a8987dd224a17dddfffdaa5, purchase_count: 2
1119. product_id_1: 2d78dc9b1f4a5d1ceb28287b82d85b86, product_id_2: d4fa7c305b2ffd07d12ae5a886b6cb0f, purchase_count: 2
1120. product_id_1: 65650c84064ff1a79e4a05988f4c3e9f, product_id_2: 90ed53d34bfcb4fa1e90656068dd04bc, purchase_count: 2
1121. product_id_1: 656bf6da1eeb7dd128b9b567eea3ca3e, product_id_2: 679a3e5e1d2bb68982be5734c6e55e63, purchase_count: 2
1122. product_id_1: 98d61056e0568ba048e5d78038790e77, product_id_2: 29e4631be78811ab993ae12613053b53, purchase_count: 2
1123. product_id_1: 98d61056e0568ba048e5d78038790e77, product_id_2: a50acd33ba7a8da8e9db65094fa990a4, purchase_count: 2
1124. product_id_1: b7d2c90f9161dc69fa75d22572003bc4, product_id_2: 1dc7685f4fdb9622d84ae2ec658d5bbf, purchase_count: 2
1125. product_id_1: b7d2c90f9161dc69fa75d22572003bc4, product_id_2: e256d05115f9eb3766f3ab752132a4e2, purchase_count: 2
1126. product_id_1: 7cefa61c9500d9b227894dc48d8b5a0b, product_id_2: 873eb5f3b8cc503730e472a14cd26616, purchase_count: 2
1127. product_id_1: dfdbfd7997881adc15da4916717e46aa, product_id_2: cdd68c0ef3e507db79631336cf9ec285, purchase_count: 2
1128. product_id_1: b7d94dc0640c7025dc8e3b46b52d8239, product_id_2: 6c90c0f6c2d89eb816b9e205b9d6a36a, purchase_count: 2
1129. product_id_1: 4419a003d42a243227478f2a949722d8, product_id_2: 0b3de7b77f38988388362460d76d884f, purchase_count: 2
1130. product_id_1: 3743820de2227103b72b029a352fb98b, product_id_2: 345ebf31824c3871cbb94c377190d6f9, purchase_count: 2
1131. product_id_1: 37583bbe907fb493b9b2efdc7b24ab54, product_id_2: e7593e3c84b3302e1531a715f1ded8b2, purchase_count: 2
1132. product_id_1: 3773a3773f5978591cff7b3e614989b3, product_id_2: 0bcc3eeca39e1064258aa1e932269894, purchase_count: 2
1133. product_id_1: 993ac19aa975075775c16ba15426f8be, product_id_2: 33e503f68fb60fe165ed992965f2c737, purchase_count: 2
1134. product_id_1: 99444c1e11fc38755dae86f5c67d3d1a, product_id_2: 17d8b8e9c21ec0fc5b33724e32fe422e, purchase_count: 2
1135. product_id_1: 99444c1e11fc38755dae86f5c67d3d1a, product_id_2: 6a0713a63e990052795623e76cc2995e, purchase_count: 2
1136. product_id_1: b8411dee248601bc460bac8e1fb8a102, product_id_2: b57469faf40b556e16b9a49308953700, purchase_count: 2
1137. product_id_1: e0ce26ae52c9ab0b8c8e42129d6c1996, product_id_2: 321cea6c65a44a9abde31f677f976c63, purchase_count: 2
1138. product_id_1: 65b183dcbb9689b176730d709a0003dd, product_id_2: a44edbb4226328a7a816f3460556d638, purchase_count: 2
1139. product_id_1: 18fa9cc25ea8b54f32d029f261673c0f, product_id_2: 4255ef536732efe235477ace2dccd393, purchase_count: 2
1140. product_id_1: 2548af3e6e77a690cf3eb6368e9ab61e, product_id_2: af35be35db4ad0dc288b571453337376, purchase_count: 2
1141. product_id_1: b86d1f2c052bc4749ee88bb74688d814, product_id_2: 8ed3ae310714d18ee990923aeb411508, purchase_count: 2
1142. product_id_1: b88d27345de2feed45475bb48cca74b1, product_id_2: 90a57d62c9b9f884fae33a10dff953b4, purchase_count: 2
1143. product_id_1: b89603272c5e7806893eb03712a0b937, product_id_2: 6d59a3fe3140425fb175cdd1e688dc2e, purchase_count: 2
1144. product_id_1: e0eb83f5cf9560ca3b976eea5dcfdfde, product_id_2: 628d0ba951ebb8fd1edc5ab3934468e0, purchase_count: 2
1145. product_id_1: 99a4788cb24856965c36a24e339b6058, product_id_2: 3e5201fe0d1ba474d9b90152c83c706c, purchase_count: 2
1146. product_id_1: 2584d5fa1ac792c8c26168eca51bb4d0, product_id_2: e5989cd466f0714e1439b95bf6a279da, purchase_count: 2
1147. product_id_1: 0152f69b6cf919bcdaf117aa8c43e5a2, product_id_2: 7ca5f56188492e30c50ba64de188aae7, purchase_count: 2
1148. product_id_1: 7dac8901a50cf3317d5372cbd3186ecd, product_id_2: 186fe07c8b8005ec6a498587ffbc1352, purchase_count: 2
1149. product_id_1: 1065e0ebef073787a7bf691924c60eeb, product_id_2: 0de59eddc63167215c972b0d785ffa7b, purchase_count: 2
1150. product_id_1: 65e3848513c9ab70bf542e5d694cf072, product_id_2: 44f90f085c7a825863cbf867990e1513, purchase_count: 2
1151. product_id_1: b8c89bc5fa5dc01a5d0e9d7ff0c6ecdb, product_id_2: 9f683084a0b0211109fef6e538cb4767, purchase_count: 2
1152. product_id_1: 7dac8901a50cf3317d5372cbd3186ecd, product_id_2: 6c55ba2343f9df32c7f88a468352ff22, purchase_count: 2
1153. product_id_1: 7dac8901a50cf3317d5372cbd3186ecd, product_id_2: 7703b8cb5b77fbb36518ea91e2ca734f, purchase_count: 2
1154. product_id_1: 0129d1e9b29d3fe6833cc922374cd252, product_id_2: 9f14f401fce2d9ddd450e7ce60cb7f5f, purchase_count: 2
1155. product_id_1: 1065e0ebef073787a7bf691924c60eeb, product_id_2: 309dd69eb83cea38c51709d62befe1a4, purchase_count: 2
1156. product_id_1: b8ded693eefc7fd6fae337f6c202093e, product_id_2: b53f20c2b12a4b9821ce57f46a7d1cae, purchase_count: 2
1157. product_id_1: e1901d5d99ca951543717ea5d1940a36, product_id_2: 81e7937893af4703d4d14ca3e3765b59, purchase_count: 2
1158. product_id_1: 7dfced4c66ef7bd85f2e30eec92e1b34, product_id_2: 747152211829957938862c1c57a30f16, purchase_count: 2
1159. product_id_1: 14dffa241a078aeaebaef48a49e807ca, product_id_2: 014a8a503291921f7b004a5215bb3c36, purchase_count: 2
1160. product_id_1: b9023d686fca0dca3ac844814e92e92b, product_id_2: 308a7360ee2e0ecfb6aa7708428692af, purchase_count: 2
1161. product_id_1: b90973ce80ba5d1fbc046fd8471acaef, product_id_2: 6eba58100f906fe0965290b28ca3c45f, purchase_count: 2
1162. product_id_1: 99a4788cb24856965c36a24e339b6058, product_id_2: fdbd77fe1773263558126c16e0b4b67c, purchase_count: 2
1163. product_id_1: 6610dc3cac3b77009d969495cc2d7037, product_id_2: d93e0523fc2cc1c5a81d432364ed2d06, purchase_count: 2
1164. product_id_1: 53c61580d8e5c4941a358ee0335c1d5c, product_id_2: 07ffc018eaf23e086370dea42c74077b, purchase_count: 2
1165. product_id_1: 53c61580d8e5c4941a358ee0335c1d5c, product_id_2: 36ba5561e351eef68d3554697132a9a8, purchase_count: 2
1166. product_id_1: 1fd3bb291e0dba9d6081eb914303993b, product_id_2: ac7e981115ad47f0e051f1b8b97e73b1, purchase_count: 2
1167. product_id_1: b9311d581f5f341576a5a2892168355c, product_id_2: b114bf337c0626166abe574eee9e3f32, purchase_count: 2
1168. product_id_1: b9311d581f5f341576a5a2892168355c, product_id_2: e56f102e763165e7e32d0f9955f8ee4a, purchase_count: 2
1169. product_id_1: b931645cdc2d9868f01544e8db63f5ab, product_id_2: 00ba6d766f0b1d7b78a5ce3e1e033263, purchase_count: 2
1170. product_id_1: 382db2ed3015c04d4b844d2a0712494c, product_id_2: d1fbb5683c8e93f314d0f2bf40d07761, purchase_count: 2
1171. product_id_1: e256d05115f9eb3766f3ab752132a4e2, product_id_2: a46875fb5b8d19ac3cff18deb9bae57e, purchase_count: 2
1172. product_id_1: e256d05115f9eb3766f3ab752132a4e2, product_id_2: b7d2c90f9161dc69fa75d22572003bc4, purchase_count: 2
1173. product_id_1: 197f7d1d3a8b0bf0c8f0394ff71b574b, product_id_2: 67fcc72a4cfd0ac826c0158ce5c98ae6, purchase_count: 2
1174. product_id_1: 0b13080e2bf193c4ff096b09e0758c7d, product_id_2: 368c6c730842d78016ad823897a372db, purchase_count: 2
1175. product_id_1: 665aa1d687284a4d2d2b74c0c6724625, product_id_2: 2481a472d98c582b46bc2dfeae6f539f, purchase_count: 2
1176. product_id_1: e27e689c4ce425f2fe7e2a270fd4d2db, product_id_2: 134afbb1d3ef60a407f8e4491dd63622, purchase_count: 2
1177. product_id_1: e27e689c4ce425f2fe7e2a270fd4d2db, product_id_2: 59b215ecd21969237a8ebb0f8a2bffc2, purchase_count: 2
1178. product_id_1: 9a0620ddaf3055b7e588e936e036a529, product_id_2: fc1d8637c0268af3db482c14b7ef8e75, purchase_count: 2
1179. product_id_1: b9adb834b99082140e354bdd3bda7eb5, product_id_2: a996a4fecaea5e7e2638d2c5078ebf4b, purchase_count: 2
1180. product_id_1: b9e247fc923da7d723c2545b76efe01e, product_id_2: 3685c687db4b3d2da5085d23b408e93a, purchase_count: 2
1181. product_id_1: 665aa1d687284a4d2d2b74c0c6724625, product_id_2: 3e5201fe0d1ba474d9b90152c83c706c, purchase_count: 2
1182. product_id_1: 14dffa241a078aeaebaef48a49e807ca, product_id_2: 880be32f4db1d9f6e2bec38fb6ac23ab, purchase_count: 2
1183. product_id_1: e2f1ccf86759df28dd1e9f2e0e3242d4, product_id_2: eb9b44e05684527fbfdfd0ff5cb86250, purchase_count: 2
1184. product_id_1: 665aa1d687284a4d2d2b74c0c6724625, product_id_2: cd3de1984e1a77b441e1b39b8e334330, purchase_count: 2
1185. product_id_1: 38956cecc0bc8d8837371d0aeeefeb59, product_id_2: 13befae9b3fb34c439cf4744fd18dfa7, purchase_count: 2
1186. product_id_1: e30aaafe45e34ce07003ef0cfcb6e49d, product_id_2: 60a8d8f0434c4531bf310eebf9f19cfe, purchase_count: 2
1187. product_id_1: 7eaf66aca1ed54df09b3c864b7416110, product_id_2: 07ffc018eaf23e086370dea42c74077b, purchase_count: 2
1188. product_id_1: e3323b0d3f79bdf85b58561d2218bc12, product_id_2: ae52eeb8383b94455f0a08b1f88ad002, purchase_count: 2
1189. product_id_1: 19884358087155dcb193ae99f344fa30, product_id_2: c2a9f8aeb7a51580fccc2d1c4f8bceaf, purchase_count: 2
1190. product_id_1: 9a98180ffbd0765e89f11cc8dd2385f4, product_id_2: 6f7400c1577bd99fb7c9cd196edb6ae2, purchase_count: 2
1191. product_id_1: 07ffc018eaf23e086370dea42c74077b, product_id_2: 53c61580d8e5c4941a358ee0335c1d5c, purchase_count: 2
1192. product_id_1: 1fe7076c53248559454a7e1d6c1037f9, product_id_2: ce003d873dc7d3c9482b894f2f2cc3e3, purchase_count: 2
1193. product_id_1: 66bd6e465a87926adb15dec604948867, product_id_2: 1b97621fc0e6ac58cfb272d5ccf8c15b, purchase_count: 2
1194. product_id_1: 2647221a6a477afe2d0268b378f1fdcd, product_id_2: 422b4786464320e3645a7e018ba60d8e, purchase_count: 2
1195. product_id_1: ba74c6b75d2ad7503175809688d5a03c, product_id_2: c5b72065154ec27c2d1ed8a654c3348f, purchase_count: 2
1196. product_id_1: e389381479408ccdcdd406d8d3049e45, product_id_2: d730dcd6017ae7bc8a4b5561f18c6d59, purchase_count: 2
1197. product_id_1: 44e6ec37a142be331fe0241006d0b389, product_id_2: 8f7ae8d7845cdabafb4b6f20d8bc5a43, purchase_count: 2
1198. product_id_1: 7ee8a1b1807716291e12649b1d617896, product_id_2: 61fd556e5319f0e1dfed3ecb8d3bb778, purchase_count: 2
1199. product_id_1: e3af4b7c220aca1535b34416de24dfb7, product_id_2: 6b00cb3fe05c73d0acef3fd949a34c0f, purchase_count: 2
1200. product_id_1: 9ad75bd7267e5c724cb42c71ac56ca72, product_id_2: cad2db5e318d7283a234c517b2f28a42, purchase_count: 2
1201. product_id_1: e3f7b3cbb0ccf1f1e361e6974b22e346, product_id_2: 681ac28f018f90684e23492046fcdb76, purchase_count: 2
1202. product_id_1: e3f7b3cbb0ccf1f1e361e6974b22e346, product_id_2: 80ec2c3e9b6567d1b32714e79282d57f, purchase_count: 2
1203. product_id_1: 5421431a9abfbdac3006e7aa925c0213, product_id_2: a8bf9a06bef0fe4106c1fc0df21a5eb6, purchase_count: 2
1204. product_id_1: 44eceb92060ff42ba1b3716acd052645, product_id_2: 39a1a3b9314738724fce4b2907ae6686, purchase_count: 2
1205. product_id_1: e3ffa5b25f4a372e7ccf597b6ceb6c90, product_id_2: e5d6523f4cd63e1347ca8407deda4ba3, purchase_count: 2
1206. product_id_1: 44f90f085c7a825863cbf867990e1513, product_id_2: 65e3848513c9ab70bf542e5d694cf072, purchase_count: 2
1207. product_id_1: 05df88a280f9c6edca3b2f5f9b3e75ad, product_id_2: 32dfa38395ccd47d7b320470b0514fee, purchase_count: 2
1208. product_id_1: 0b3de7b77f38988388362460d76d884f, product_id_2: 4419a003d42a243227478f2a949722d8, purchase_count: 2
1209. product_id_1: bb17b2343c9b332cce4ffbb8f51a67ca, product_id_2: 48282b524c93e69ec5653481e2b8a237, purchase_count: 2
1210. product_id_1: 389d119b48cf3043d311335e499d9c6b, product_id_2: b0961721fd839e9982420e807758a2a6, purchase_count: 2
1211. product_id_1: 678c229b41c0e497d35a25a8be1cc631, product_id_2: 0de59eddc63167215c972b0d785ffa7b, purchase_count: 2
1212. product_id_1: 7f97636768f5bb7b8f2843974b48a1e8, product_id_2: bf730d49d016a80c9c66b4c1768a7933, purchase_count: 2
1213. product_id_1: bb3a346d0fc86850244000d0fe5bf5dd, product_id_2: d4dccae17c83ffbaafc50d763503e9eb, purchase_count: 2
1214. product_id_1: 9b89ab91efbb4750c39864ed0262711f, product_id_2: 31352e05b5f8620929e1b8bbbeda5578, purchase_count: 2
1215. product_id_1: bb42f37fc3d9130e4a4339d24a47dd7c, product_id_2: 4025ee582ef6b8c478af3b44cf89054b, purchase_count: 2
1216. product_id_1: 10717ff440b2320081989126e858b220, product_id_2: ee4a5109a6b0bf0dd3a3347b73955c95, purchase_count: 2
1217. product_id_1: 09c3a2ea33f044aebffecd6681e00133, product_id_2: d011223de539cd224b5c5c8082313d46, purchase_count: 2
1218. product_id_1: 678c229b41c0e497d35a25a8be1cc631, product_id_2: 309dd69eb83cea38c51709d62befe1a4, purchase_count: 2
1219. product_id_1: 7f9e40aa498f8f6edf4cc51215ecce9e, product_id_2: 7486542600afc050d20740e976ff87f8, purchase_count: 2
1220. product_id_1: 457cd0a99cfa977993e4eb6d98d95abb, product_id_2: ab169b33d13e5041b9b9d4a2fafce9d9, purchase_count: 2
1221. product_id_1: 457cd0a99cfa977993e4eb6d98d95abb, product_id_2: de92134fd940e9302d27c31af4581fbd, purchase_count: 2
1222. product_id_1: 7f9f228320c43765cfe30cdc090e0be4, product_id_2: 3512f777c335f8297b5ad43416b69cf8, purchase_count: 2
1223. product_id_1: 38cd38029795797c97b73421fdad08cf, product_id_2: d191e54bd50ba045ac5bc9336572886f, purchase_count: 2
1224. product_id_1: 678c229b41c0e497d35a25a8be1cc631, product_id_2: 5dae498eff2d80057f56122235a36aff, purchase_count: 2
1225. product_id_1: 38cd38029795797c97b73421fdad08cf, product_id_2: dea564fb3ed59db512cb4df9c491c1ef, purchase_count: 2
1226. product_id_1: 45a9a8115c62ad1ce34845e5ec4cfd48, product_id_2: 1ac09f60f3c3bc2021c637ef23fa3248, purchase_count: 2
1227. product_id_1: 679a3e5e1d2bb68982be5734c6e55e63, product_id_2: 656bf6da1eeb7dd128b9b567eea3ca3e, purchase_count: 2
1228. product_id_1: e56f102e763165e7e32d0f9955f8ee4a, product_id_2: b9311d581f5f341576a5a2892168355c, purchase_count: 2
1229. product_id_1: 38e19855caf485b504d6f33ed31a9eb4, product_id_2: be0e6c61c2bcdd9a4d022ba67fd66189, purchase_count: 2
1230. product_id_1: e5989cd466f0714e1439b95bf6a279da, product_id_2: 2584d5fa1ac792c8c26168eca51bb4d0, purchase_count: 2
1231. product_id_1: 07ffc018eaf23e086370dea42c74077b, product_id_2: 7eaf66aca1ed54df09b3c864b7416110, purchase_count: 2
1232. product_id_1: 1a06a6a66ab23d70e02b8f92650e268f, product_id_2: 90916a1ae9ea5e3c8c15c37b51834f37, purchase_count: 2
1233. product_id_1: 38f894aa22356ddb9e98478fbc016083, product_id_2: b5a47689050b1900fd74aa6b431579a7, purchase_count: 2
1234. product_id_1: e5d6523f4cd63e1347ca8407deda4ba3, product_id_2: e3ffa5b25f4a372e7ccf597b6ceb6c90, purchase_count: 2
1235. product_id_1: bcda9424eac9dd4c6f2d739e92c0a2ab, product_id_2: fd91e23b4465803725f329b39afe018a, purchase_count: 2
1236. product_id_1: 1a06a6a66ab23d70e02b8f92650e268f, product_id_2: 944a8fa6055b8213f9e715720d4e2d5c, purchase_count: 2
1237. product_id_1: 55363f487ca324087a49ddfcfb91b971, product_id_2: 7b49e585ac8c80b14c9b2815d4db465f, purchase_count: 2
1238. product_id_1: 67fcc72a4cfd0ac826c0158ce5c98ae6, product_id_2: 197f7d1d3a8b0bf0c8f0394ff71b574b, purchase_count: 2
1239. product_id_1: e61c78a7343d82c0539d27df0f7dfc31, product_id_2: ddb9028236525b8ab493fc24f99e8d1a, purchase_count: 2
1240. product_id_1: 9cbe4a1fd4db99c14512e9b2ff033ec4, product_id_2: 62d8daeee0db3a60c234c2d1bfd10651, purchase_count: 2
1241. product_id_1: 1a1607ff3b9bced214efc0a8cdfb2510, product_id_2: 32459442f3b850918e20febc47c9edfb, purchase_count: 2
1242. product_id_1: 681ac28f018f90684e23492046fcdb76, product_id_2: e3f7b3cbb0ccf1f1e361e6974b22e346, purchase_count: 2
1243. product_id_1: 9cc50a8fd6a69a4d287d62d52ee5d009, product_id_2: 976ab50ce2361a9f99aaf9fd4037a00a, purchase_count: 2
1244. product_id_1: 80ec2c3e9b6567d1b32714e79282d57f, product_id_2: e3f7b3cbb0ccf1f1e361e6974b22e346, purchase_count: 2
1245. product_id_1: 9d0bb30eed80184666c8acad23921283, product_id_2: b3cf0a98f31b76ed0cec13d9c77102c4, purchase_count: 2
1246. product_id_1: 6845447c5d4495dcddca6e6b494df3e7, product_id_2: 5b4c8ab4477bb00b57cd5edb1af9aff8, purchase_count: 2
1247. product_id_1: 555cdc8ae3abc9870afa02367539b799, product_id_2: 2136c70bbe723d338fab53da3c03e6dc, purchase_count: 2
1248. product_id_1: 9d32095f76b97762307e86cfc18dd7a0, product_id_2: 39aa98469aa7460a9764311b3f8efb12, purchase_count: 2
1249. product_id_1: bd6e6fce9ada76ea2db0f1912e8e478f, product_id_2: c32b1155b886162db8e1ec114699a799, purchase_count: 2
1250. product_id_1: 9d32095f76b97762307e86cfc18dd7a0, product_id_2: 87d780fa7d2cf3710aa02dc4ca8db985, purchase_count: 2
1251. product_id_1: e7593e3c84b3302e1531a715f1ded8b2, product_id_2: 37583bbe907fb493b9b2efdc7b24ab54, purchase_count: 2
1252. product_id_1: bdc1cae635cc5a6a09d9481495b890c6, product_id_2: 5292d2a10d727811b78d5b7dfb6c96b3, purchase_count: 2
1253. product_id_1: 0b5c0ecd14105464e2b879a307092e3f, product_id_2: 89039f76a4c1ed8e4c13f4b531f158ca, purchase_count: 2
1254. product_id_1: 39a0578866cba21bcead91f5221af2a8, product_id_2: ac5e164e2eda939ffa46593f90077f9a, purchase_count: 2
1255. product_id_1: 4680d0c534e54990d8579f41dd239901, product_id_2: 315c6373ff469f7b7f60bbb36c319f7b, purchase_count: 2
1256. product_id_1: e7890707ac0e4e190a74aa46c92e2c94, product_id_2: 2136c70bbe723d338fab53da3c03e6dc, purchase_count: 2
1257. product_id_1: 4680d0c534e54990d8579f41dd239901, product_id_2: bff2390f68a7b76b01ef61b684888261, purchase_count: 2
1258. product_id_1: 39a1a3b9314738724fce4b2907ae6686, product_id_2: 44eceb92060ff42ba1b3716acd052645, purchase_count: 2
1259. product_id_1: 005030ef108f58b46b78116f754d8d38, product_id_2: 75c06ee06b201f9b6301d2b5e72993f8, purchase_count: 2
1260. product_id_1: 39aa98469aa7460a9764311b3f8efb12, product_id_2: 9d32095f76b97762307e86cfc18dd7a0, purchase_count: 2
1261. product_id_1: 5599be6fe59cd2257edfdec9d45442e0, product_id_2: f59871b3d9da4c64cbe41ad3dd04dc14, purchase_count: 2
1262. product_id_1: 39b146e69c32ffe0a469e95a71585843, product_id_2: 2c3f424b5643b03663e0f5861dde2bfe, purchase_count: 2
1263. product_id_1: be0a8cb3c50011daec32f4d8ecdccb28, product_id_2: 368c6c730842d78016ad823897a372db, purchase_count: 2
1264. product_id_1: be0e6c61c2bcdd9a4d022ba67fd66189, product_id_2: 38e19855caf485b504d6f33ed31a9eb4, purchase_count: 2
1265. product_id_1: be0e6c61c2bcdd9a4d022ba67fd66189, product_id_2: 93d8b11d613a563f5a26212282bb145e, purchase_count: 2
1266. product_id_1: be0e6c61c2bcdd9a4d022ba67fd66189, product_id_2: acebea1efbaa063642166633d247aec7, purchase_count: 2
1267. product_id_1: 26facbccf840188b92bcc8cb89fe1f64, product_id_2: 5b1f3328a2c6f837ecce21bca1489939, purchase_count: 2
1268. product_id_1: 01ef0716b68c8493434ad32430c24e18, product_id_2: fe6f03cedd96bcbc5c8726c5963fd35c, purchase_count: 2
1269. product_id_1: 09f6dccfebfa0688abfc1af640b69e61, product_id_2: 289d248f6a9046a0f0be47cda2b45537, purchase_count: 2
1270. product_id_1: 9ddd762ee8a13576a809dc66f22aa2b5, product_id_2: 41da75141264c3bde21ecea85a4cb8b7, purchase_count: 2
1271. product_id_1: 9ddd762ee8a13576a809dc66f22aa2b5, product_id_2: 429e7401fafb76436f15e86498bd7364, purchase_count: 2
1272. product_id_1: 46d9734c42793de762a7ca5db95ecdd1, product_id_2: 94972ba3b1856e8453d8a0b4d522aa36, purchase_count: 2
1273. product_id_1: e86b81dcac341ea01df0260077cdf082, product_id_2: 599dc392f7a23273471b068d72408224, purchase_count: 2
1274. product_id_1: be59d6c35e43e4bae41772d4b87136a4, product_id_2: fa243e761ae871597627e917611eeb23, purchase_count: 2
1275. product_id_1: 1a4247b6eddc27c68f7995dcc68b01e2, product_id_2: cd2ea14a901da3b47b33516f3ca6929e, purchase_count: 2
1276. product_id_1: 3a05a947f28cf46d789adedc107d7595, product_id_2: 6ee1607bacba780139e7f7fcd316c1d0, purchase_count: 2
1277. product_id_1: 69523f67543ff9ea6b1a15858fb59b3b, product_id_2: d2c7a1e57b8f3e74095798f867334b36, purchase_count: 2
1278. product_id_1: 271a16e4751b04867238b601ad652692, product_id_2: 5173e870df52b09d6b76f88504a1991d, purchase_count: 2
1279. product_id_1: 2fb0efd1f61f186ffdda9e8ec70f27f2, product_id_2: 163e6400e6dadd0fe04775c5e9331fda, purchase_count: 2
1280. product_id_1: 06ecc3d4006ad6eb293a1b93ec3c7183, product_id_2: fc1d8637c0268af3db482c14b7ef8e75, purchase_count: 2
1281. product_id_1: 81e7937893af4703d4d14ca3e3765b59, product_id_2: e1901d5d99ca951543717ea5d1940a36, purchase_count: 2
1282. product_id_1: 0de59eddc63167215c972b0d785ffa7b, product_id_2: 0cf2faf9749f53924cea652a09d8e327, purchase_count: 2
1283. product_id_1: 820e8f306dc9ffcf6d0957516084cca1, product_id_2: a57878a3c4874b342d09d163ae63e596, purchase_count: 2
1284. product_id_1: e8c6039a25765995ac7c1ec2cbef5765, product_id_2: 4910917f05092f331bf3a477f791cc01, purchase_count: 2
1285. product_id_1: 9e10eb05d9f369d5c38c475425cc2ee9, product_id_2: 40f9995eecfc68f54991ca49582e9885, purchase_count: 2
1286. product_id_1: 820fa146b7ccfe19c80e999cf4a77668, product_id_2: 0a80f03007af9e2c5ac5065d6742e1b2, purchase_count: 2
1287. product_id_1: 0de59eddc63167215c972b0d785ffa7b, product_id_2: 1065e0ebef073787a7bf691924c60eeb, purchase_count: 2
1288. product_id_1: 3a362c0e7f9a69276e2d95869a3e143b, product_id_2: 4f0abfbee7569e43b80f9aaa256a9bf8, purchase_count: 2
1289. product_id_1: 0de59eddc63167215c972b0d785ffa7b, product_id_2: 21b524c4c060169fa75ccf08c7da4627, purchase_count: 2
1290. product_id_1: e906fa76a27488f805ba8584a4c10cba, product_id_2: 85b6cd7f57f7a06d180c93e8c74f6381, purchase_count: 2
1291. product_id_1: 56c0a9eb43edf8247a0a2ef0f08af0f5, product_id_2: 30ed2f5bb848bade9d8906ef78dd880a, purchase_count: 2
1292. product_id_1: 2ff995aead9c63a1f37a07b3664ead37, product_id_2: 6a23ae3187f1dac41b7210a8c7739d6b, purchase_count: 2
1293. product_id_1: 6a0713a63e990052795623e76cc2995e, product_id_2: 99444c1e11fc38755dae86f5c67d3d1a, purchase_count: 2
1294. product_id_1: 6a0713a63e990052795623e76cc2995e, product_id_2: d25bbb182b51d1594fe3b54a27ae143e, purchase_count: 2
1295. product_id_1: e95fb3a80ca294f39de925b6428f3a32, product_id_2: 17d8b8e9c21ec0fc5b33724e32fe422e, purchase_count: 2
1296. product_id_1: e95fb3a80ca294f39de925b6428f3a32, product_id_2: 6a0713a63e990052795623e76cc2995e, purchase_count: 2
1297. product_id_1: 8264f2dcca3aa83cb217d7f09e9c8cf8, product_id_2: 86c43103446290e7efacad3701cd654d, purchase_count: 2
1298. product_id_1: 6a0713a63e990052795623e76cc2995e, product_id_2: e95fb3a80ca294f39de925b6428f3a32, purchase_count: 2
1299. product_id_1: 8273821fd2a32fbbc77ad8b743b2a1b9, product_id_2: 368c6c730842d78016ad823897a372db, purchase_count: 2
1300. product_id_1: bf477d995ee4444807afc574cfbcc1c1, product_id_2: 96ea4f32befa14bd8ab36fd6827a5e3f, purchase_count: 2
1301. product_id_1: e9b3cf27d68caa64832c4a7c460abcb9, product_id_2: cf1d8e226162a1d0ad61f29b7ed72d82, purchase_count: 2
1302. product_id_1: e9dd44f105ffdcb98405c94f1d0bbdd9, product_id_2: f3ae4ce1b63810f2921ff353ddbec67d, purchase_count: 2
1303. product_id_1: 6a23ae3187f1dac41b7210a8c7739d6b, product_id_2: 2ff995aead9c63a1f37a07b3664ead37, purchase_count: 2
1304. product_id_1: 9ecadb84c81da840dbf3564378b586e9, product_id_2: eb8c629f70275fd1c4f809116cce1efc, purchase_count: 2
1305. product_id_1: 0de59eddc63167215c972b0d785ffa7b, product_id_2: 4a5c3967bfd3629fe07ef4d0cc8c3818, purchase_count: 2
1306. product_id_1: 474bb6b54fc608ca71059a6c4f7ecda3, product_id_2: dd0dcee76f9c12fff4bc0eb641d57c7f, purchase_count: 2
1307. product_id_1: bf730d49d016a80c9c66b4c1768a7933, product_id_2: 7f97636768f5bb7b8f2843974b48a1e8, purchase_count: 2
1308. product_id_1: 9f14f401fce2d9ddd450e7ce60cb7f5f, product_id_2: 0129d1e9b29d3fe6833cc922374cd252, purchase_count: 2
1309. product_id_1: 0de59eddc63167215c972b0d785ffa7b, product_id_2: 5dae498eff2d80057f56122235a36aff, purchase_count: 2
1310. product_id_1: bfa8fb32cecbf90899f6f517b77a766f, product_id_2: a519511d5c5c1153c9f636288e50f819, purchase_count: 2
1311. product_id_1: 82cff05560eae73466f8778690b037fa, product_id_2: 91472a5abca63bed91ade04c71c203ce, purchase_count: 2
1312. product_id_1: 82cff05560eae73466f8778690b037fa, product_id_2: d9e7d13814ea50f9ae1f612ef6b3a1f1, purchase_count: 2
1313. product_id_1: 0de59eddc63167215c972b0d785ffa7b, product_id_2: 678c229b41c0e497d35a25a8be1cc631, purchase_count: 2
1314. product_id_1: 113f80f12c8892f0c59206f70b862b40, product_id_2: a1dd59756b92c62cd39375d0b0222698, purchase_count: 2
1315. product_id_1: 113f80f12c8892f0c59206f70b862b40, product_id_2: a8d2af10596b8acd5f45c720fe9745aa, purchase_count: 2
1316. product_id_1: 3ae116a20336cc3eb1b3d0b9b0a94d3d, product_id_2: f1b067568bb39768f754b0d1ab1abcf6, purchase_count: 2
1317. product_id_1: bff2390f68a7b76b01ef61b684888261, product_id_2: 4680d0c534e54990d8579f41dd239901, purchase_count: 2
1318. product_id_1: 9f683084a0b0211109fef6e538cb4767, product_id_2: b8c89bc5fa5dc01a5d0e9d7ff0c6ecdb, purchase_count: 2
1319. product_id_1: bff2390f68a7b76b01ef61b684888261, product_id_2: b5a47689050b1900fd74aa6b431579a7, purchase_count: 2
1320. product_id_1: 158102fe543dbaeb84d87811bfe06d0d, product_id_2: 414c53fa9c5cc4a0390682aeb2e25ec1, purchase_count: 2
1321. product_id_1: 8338cef8355d238f43711dcb9c0657b2, product_id_2: 07c055536ebf10dfbb6c6db6dbfc36e5, purchase_count: 2
1322. product_id_1: 8338cef8355d238f43711dcb9c0657b2, product_id_2: 741a31499a578979be85db7f80139e62, purchase_count: 2
1323. product_id_1: 6abd84909e8ed79ef808c16f90b91093, product_id_2: b0528299d65ab35e3ed853f6a853b8b8, purchase_count: 2
1324. product_id_1: 113f80f12c8892f0c59206f70b862b40, product_id_2: abe2c60707c1e11cfa710dc7328b4bf6, purchase_count: 2
1325. product_id_1: c0295f791bfc794623d0ea811cca82d5, product_id_2: da051bd767b7457572d55aba23fd846a, purchase_count: 2
1326. product_id_1: c03d44fcdfabbabd5185c8eb60f77aea, product_id_2: c43ab4269cbf91b373263db4c2973cad, purchase_count: 2
1327. product_id_1: c0400a62c5019cdc69bfc76d39b1cfb4, product_id_2: 4bc15899b2cd7ade6db2fb0a5188cd24, purchase_count: 2
1328. product_id_1: c06f7984550cc89a7d76e51e936e714f, product_id_2: 30ad9d2c8a8e788a606a6c23e07260a9, purchase_count: 2
1329. product_id_1: c0737ec7b87906c79f130f39cec3d3ee, product_id_2: a3309868978f986b3865b8a3729192e2, purchase_count: 2
1330. product_id_1: 1ac09f60f3c3bc2021c637ef23fa3248, product_id_2: 45a9a8115c62ad1ce34845e5ec4cfd48, purchase_count: 2
1331. product_id_1: 834df04774f3aa4b60bfd6f839f448bc, product_id_2: ac5e164e2eda939ffa46593f90077f9a, purchase_count: 2
1332. product_id_1: ead6d52e3dc075669af5d7a1958b0f07, product_id_2: 1ac09f60f3c3bc2021c637ef23fa3248, purchase_count: 2
1333. product_id_1: 577fd304233fe9412349ef6a4a3f6ae6, product_id_2: a7742a00e1d286b7f7d4d81e90d8acc9, purchase_count: 2
1334. product_id_1: 9feeadd6b97835152e83e1b25b46f5c4, product_id_2: 7c6ae4d12d2754ca0826ad17792c554e, purchase_count: 2
1335. product_id_1: 1ac09f60f3c3bc2021c637ef23fa3248, product_id_2: ead6d52e3dc075669af5d7a1958b0f07, purchase_count: 2
1336. product_id_1: 8374b39a15882a19ce4558f13064b55c, product_id_2: 6e7df7f4622d4360261995dbd5e787d0, purchase_count: 2
1337. product_id_1: 6b00cb3fe05c73d0acef3fd949a34c0f, product_id_2: e3af4b7c220aca1535b34416de24dfb7, purchase_count: 2
1338. product_id_1: 1ae28ef6d0421f92f2e4e6d407e90347, product_id_2: 3158c44b08596ff51ee3560fad16cc09, purchase_count: 2
1339. product_id_1: 47b0f8596ee6dafbb4438cac16fa6275, product_id_2: 524d0ebe9a59d96dfaa2983b54a50c15, purchase_count: 2
1340. product_id_1: eb048e296b8db6cd64b1bafd9500786c, product_id_2: 113f80f12c8892f0c59206f70b862b40, purchase_count: 2
1341. product_id_1: 57c580a8fbf3d8374b06bee7b6f4ce31, product_id_2: 3ceb44c75e6981ff0987bb90c95694c0, purchase_count: 2
1342. product_id_1: 113f80f12c8892f0c59206f70b862b40, product_id_2: eb048e296b8db6cd64b1bafd9500786c, purchase_count: 2
1343. product_id_1: 27d0fc55e3d2fe698088f2603e0a2ab6, product_id_2: fc22eb7bba78fd67da33c9acf162d592, purchase_count: 2
1344. product_id_1: 47ea90e9a2976bc290c3cdf3b5e0573d, product_id_2: d1b1a0e78589ee89279d0be1e4a8b905, purchase_count: 2
1345. product_id_1: 6bb50785f82871dde37ed1666da54bf3, product_id_2: c21d0cfb10ff3cef881d63e1be43f260, purchase_count: 2
1346. product_id_1: 47fafa6908e75ae62b8a36a9eb3b9234, product_id_2: 61fd556e5319f0e1dfed3ecb8d3bb778, purchase_count: 2
1347. product_id_1: a03e401d58a45187271718c5d7610422, product_id_2: c9b8a74a8865b966e660cc1f7b4e32a9, purchase_count: 2
1348. product_id_1: eb8c629f70275fd1c4f809116cce1efc, product_id_2: 9ecadb84c81da840dbf3564378b586e9, purchase_count: 2
1349. product_id_1: eb8c629f70275fd1c4f809116cce1efc, product_id_2: d678178aa4291cd25a755a90188375c8, purchase_count: 2
1350. product_id_1: eb9b44e05684527fbfdfd0ff5cb86250, product_id_2: e2f1ccf86759df28dd1e9f2e0e3242d4, purchase_count: 2
1351. product_id_1: ebe9e593dfd269670a40a0ee90a8764e, product_id_2: f8cd8a989b03ce1808d9d8d76668ea51, purchase_count: 2
1352. product_id_1: 83bfae859f4a37b048a3abcecb17c506, product_id_2: de17feec1983829fec4bc58cadaa43f3, purchase_count: 2
1353. product_id_1: a0627b01409b61f4076a920265b86665, product_id_2: 0cf1296fa38622de944eb05701b4ff34, purchase_count: 2
1354. product_id_1: 005030ef108f58b46b78116f754d8d38, product_id_2: 51250f90d798d377a1928e8a4e2e9ae1, purchase_count: 2
1355. product_id_1: 83e2059df06602e05d9bc1abf28166ac, product_id_2: 281905b21f01db1009fd7c01b10dd1d4, purchase_count: 2
1356. product_id_1: ebf9bc6cd600eadd681384e3116fda85, product_id_2: 5ddab10d5e0a23acb99acf56b62b3276, purchase_count: 2
1357. product_id_1: 83e2059df06602e05d9bc1abf28166ac, product_id_2: 4006da5107400e5ac48dbcc829a36c42, purchase_count: 2
1358. product_id_1: ec2d43cc59763ec91694573b31f1c29a, product_id_2: 02623b0e4e6b951aefb23575de1f3886, purchase_count: 2
1359. product_id_1: ec2d43cc59763ec91694573b31f1c29a, product_id_2: 40a4dfa74a737d541b3c2413edf9cdf6, purchase_count: 2
1360. product_id_1: ec2d43cc59763ec91694573b31f1c29a, product_id_2: 51edddbbc47a477259e672bd291feed6, purchase_count: 2
1361. product_id_1: 6bd4c564d1f96b0db5d02d376b4daed6, product_id_2: 0950783476d3f6529a03b28fcac219d1, purchase_count: 2
1362. product_id_1: 308a7360ee2e0ecfb6aa7708428692af, product_id_2: b9023d686fca0dca3ac844814e92e92b, purchase_count: 2
1363. product_id_1: 48282b524c93e69ec5653481e2b8a237, product_id_2: 4dfffeaa9522a9ba71cdc9e7d43212d0, purchase_count: 2
1364. product_id_1: ec2d43cc59763ec91694573b31f1c29a, product_id_2: 7185389e32acf9c5c5f61e6a23c0ab3a, purchase_count: 2
1365. product_id_1: 48282b524c93e69ec5653481e2b8a237, product_id_2: 756feaccd3c677658c9e70bf09ef43b9, purchase_count: 2
1366. product_id_1: 6c3effec7c8ddba466d4f03f982c7aa3, product_id_2: 71a8be2937fd926b330febe100effd02, purchase_count: 2
1367. product_id_1: c211ff3068fcd2f8898192976d8b3a32, product_id_2: 4025ee582ef6b8c478af3b44cf89054b, purchase_count: 2
1368. product_id_1: 48282b524c93e69ec5653481e2b8a237, product_id_2: 775cbb352638cb5e59cea1637da006cc, purchase_count: 2
1369. product_id_1: 48282b524c93e69ec5653481e2b8a237, product_id_2: bb17b2343c9b332cce4ffbb8f51a67ca, purchase_count: 2
1370. product_id_1: 6c55ba2343f9df32c7f88a468352ff22, product_id_2: 186fe07c8b8005ec6a498587ffbc1352, purchase_count: 2
1371. product_id_1: a0ef8572cd061badd81ffc48dc04d1fa, product_id_2: 2d78dc9b1f4a5d1ceb28287b82d85b86, purchase_count: 2
1372. product_id_1: ec8ae427905e10052ee4f1e9993b6763, product_id_2: 7893c68e0a8b6e58a70390551e8a84d9, purchase_count: 2
1373. product_id_1: ec8ae427905e10052ee4f1e9993b6763, product_id_2: cfe6e9c01d0bbb5df9a75f0e3286baa9, purchase_count: 2
1374. product_id_1: c21d0cfb10ff3cef881d63e1be43f260, product_id_2: 6bb50785f82871dde37ed1666da54bf3, purchase_count: 2
1375. product_id_1: 6c55ba2343f9df32c7f88a468352ff22, product_id_2: 7703b8cb5b77fbb36518ea91e2ca734f, purchase_count: 2
1376. product_id_1: 6c55ba2343f9df32c7f88a468352ff22, product_id_2: 7dac8901a50cf3317d5372cbd3186ecd, purchase_count: 2
1377. product_id_1: 3bbacbe586e957acbf26c63b3ed532a3, product_id_2: a6b56b20f93907299eef6ea711338269, purchase_count: 2
1378. product_id_1: c2a9f8aeb7a51580fccc2d1c4f8bceaf, product_id_2: 0cf41187284d7f099adc8415a743ebbd, purchase_count: 2
1379. product_id_1: c2a9f8aeb7a51580fccc2d1c4f8bceaf, product_id_2: 19884358087155dcb193ae99f344fa30, purchase_count: 2
1380. product_id_1: c2ad928095a0d199c4d44b2194119ce2, product_id_2: 145140d23f166a1166dc4437107df8cc, purchase_count: 2
1381. product_id_1: ed2067a9c1f79553088a3c67b99a9f97, product_id_2: 171b509779ad4fe0cbed2a3d95d10c68, purchase_count: 2
1382. product_id_1: 57fcacc3434a1f2f2b039c1b4e61f5e1, product_id_2: cf0d29a0ea1464f4c3e5594d0746c51b, purchase_count: 2
1383. product_id_1: 6c90c0f6c2d89eb816b9e205b9d6a36a, product_id_2: b7d94dc0640c7025dc8e3b46b52d8239, purchase_count: 2
1384. product_id_1: a140e83c184347be1aa71694fe525537, product_id_2: 5a883fb296ab66ac6a1e68e6ba2175c3, purchase_count: 2
1385. product_id_1: ed4dfdaab6c24770fc6f34ad50c89ac1, product_id_2: a3fd6c4ecde9035c3e8dd4e0fd8b8048, purchase_count: 2
1386. product_id_1: 309dd69eb83cea38c51709d62befe1a4, product_id_2: 0cf2faf9749f53924cea652a09d8e327, purchase_count: 2
1387. product_id_1: a140e83c184347be1aa71694fe525537, product_id_2: cdc4af478fef19f03f1d0353c00271cd, purchase_count: 2
1388. product_id_1: 3c14f8a3874197fe07fe94b4d5d9af86, product_id_2: 74006af1917b5e79f78f35767fa221ba, purchase_count: 2
1389. product_id_1: 309dd69eb83cea38c51709d62befe1a4, product_id_2: 1065e0ebef073787a7bf691924c60eeb, purchase_count: 2
1390. product_id_1: ed61f9d2b8837c3aeebb563b7305ef78, product_id_2: a787d9cee40e9de33b13d740c32359e8, purchase_count: 2
1391. product_id_1: 33edceeb3ecaca6ed4cdaf8085a21b3d, product_id_2: f4c3e41f8c0ac64d1be09e1b92327ac0, purchase_count: 1
1392. product_id_1: 33f38661c7e75dfddb833dc4cd2f1c27, product_id_2: fbcd9b07bda0301e7e776fc1ab26fdfe, purchase_count: 1
1393. product_id_1: 340f33bdf4103eba89df5d5153beff7e, product_id_2: adf24c4c9e90e7054d07309a04c419d0, purchase_count: 1
1394. product_id_1: 341c7cf0d9806592075c3090658f5c81, product_id_2: 073afdaeb2d71d4da3ce0c6935614289, purchase_count: 1
1395. product_id_1: 34239894e175b17d8c84edc6c73b4dad, product_id_2: cfe99a31516679fb9515881d25891570, purchase_count: 1
1396. product_id_1: 3458b4c1fcbe46e2eedb48e00960a60e, product_id_2: 99a4788cb24856965c36a24e339b6058, purchase_count: 1
1397. product_id_1: 3462cfbd316346049256b3b3242f8dfa, product_id_2: 7825a7c4f9edb6b219eb94c29e86e7b9, purchase_count: 1
1398. product_id_1: 347492a8e06a539c0861eea7e527fdaf, product_id_2: 0a56efd5f050d3f861a04c6f005d1128, purchase_count: 1
1399. product_id_1: 347492a8e06a539c0861eea7e527fdaf, product_id_2: 2480fca3af4f5221cf3596c257be308b, purchase_count: 1
1400. product_id_1: 347492a8e06a539c0861eea7e527fdaf, product_id_2: 7e9b52ab8c9b4c0fa93e431e8c3975e4, purchase_count: 1
1401. product_id_1: 3477030902c7c383db840003051d8115, product_id_2: 8a443635fdf9759915c9be5be2e3b862, purchase_count: 1
1402. product_id_1: 3477030902c7c383db840003051d8115, product_id_2: f97a136cf6e5f5d9333b513afc8b153e, purchase_count: 1
1403. product_id_1: 3487b8d662448326a09da14416640170, product_id_2: 8ffc89162cccaef5a98a4c0bcd241a0e, purchase_count: 1
1404. product_id_1: 3487b8d662448326a09da14416640170, product_id_2: a65c82cfb533f379a9d1ff76b78ce9ee, purchase_count: 1
1405. product_id_1: 3487b8d662448326a09da14416640170, product_id_2: ba37ce1b5e0638cf45fd59f63ada0093, purchase_count: 1
1406. product_id_1: 3487b8d662448326a09da14416640170, product_id_2: c22dc992a198753e51e4a25f83957b9b, purchase_count: 1
1407. product_id_1: 3489d3fae282f7944399bc697554a1e5, product_id_2: 9153ddefe47e356b46bffa5e9cd8cc3b, purchase_count: 1
1408. product_id_1: 348ea09800ea8b415f488cef882bb755, product_id_2: e19c8e70d39de9646d64163a66051797, purchase_count: 1
1409. product_id_1: 349ce46a0e2e20054aa9d80c48af8816, product_id_2: 8af5b5f4f89849cc4dce36dee73dd9de, purchase_count: 1
1410. product_id_1: 349ce46a0e2e20054aa9d80c48af8816, product_id_2: a39cc58c1b5926b6f9f378daa89f1315, purchase_count: 1
1411. product_id_1: 34b2f2ad489d0598df09cab99e17c928, product_id_2: 19f1647ffc7e4a8ea74bf2dc45ac8e44, purchase_count: 1
1412. product_id_1: 34c8873cadb5465f46b7a20b6eb0215b, product_id_2: 96bdf83ce8bcf48510e8a8ab8b5fb660, purchase_count: 1
1413. product_id_1: 34dabb8af33b3756cf72df05fb327011, product_id_2: 7f1a77bec0639e473392e91a504272a5, purchase_count: 1
1414. product_id_1: 34dfc6386b7550503bd2e582ef45d041, product_id_2: 0521fe3eb04940304b489d0fb49a37dd, purchase_count: 1
1415. product_id_1: 3516632e8f52b679ff83d1665ecc990e, product_id_2: 42ef2bdec0493fd90852352fcfbf2c24, purchase_count: 1
1416. product_id_1: 3516632e8f52b679ff83d1665ecc990e, product_id_2: 566f6035da0eb2a5d974ac66ae6d148c, purchase_count: 1
1417. product_id_1: 3516632e8f52b679ff83d1665ecc990e, product_id_2: 70906e04da1eebf3d1b8791bd09ffe85, purchase_count: 1
1418. product_id_1: 351eb84de99fb5e43d8706bc3f41fbff, product_id_2: 03d4233b9e3382adaed9e5c58626f1dc, purchase_count: 1
1419. product_id_1: 351eb84de99fb5e43d8706bc3f41fbff, product_id_2: ac3f48d9dfd6ebdf8e871702ee91ee83, purchase_count: 1
1420. product_id_1: 351eb84de99fb5e43d8706bc3f41fbff, product_id_2: e0d3e5cf1969f20bd69e052ec6cf8f8f, purchase_count: 1
1421. product_id_1: 3528876f41132ca5604b505343619412, product_id_2: 10c2160beca6757676b447aab88e5129, purchase_count: 1
1422. product_id_1: 3560066ba5a5b4f87a8d5de6da565792, product_id_2: dccab0aeed5632473aa1fccf14846b3a, purchase_count: 1
1423. product_id_1: 356260965b761056864ff939baeb4b22, product_id_2: b917d488bd4ad4225f8d046a32e2d122, purchase_count: 1
1424. product_id_1: 356bc9278252d4fb0c566e64612fc83e, product_id_2: 9239c49d7d0e542d0e12a9023771ef51, purchase_count: 1
1425. product_id_1: 35997e7b3823b0bb5947dce1986cfb61, product_id_2: 68ad45d48d69404aeb71ce87e1b2c948, purchase_count: 1
1426. product_id_1: 35afc973633aaeb6b877ff57b2793310, product_id_2: 056d012d264624accb7f73d31caee034, purchase_count: 1
1427. product_id_1: 35afc973633aaeb6b877ff57b2793310, product_id_2: 50e1b118f266b655f613f753914c42db, purchase_count: 1
1428. product_id_1: 35afc973633aaeb6b877ff57b2793310, product_id_2: 635041fb8431d6de8a42741bab6caa9f, purchase_count: 1
1429. product_id_1: 35afc973633aaeb6b877ff57b2793310, product_id_2: 996ae0a67e63b78b427a1f8d07543e86, purchase_count: 1
1430. product_id_1: 35afc973633aaeb6b877ff57b2793310, product_id_2: a0644c97f9915e9f442b94b4a5a2fa1b, purchase_count: 1
1431. product_id_1: 35bc6c77029697004675d3a2ce505916, product_id_2: 98354ddeaeae40bd6b705381191a9ffc, purchase_count: 1
1432. product_id_1: 35bd74b6319ba18ae4f30d8b54144fd2, product_id_2: dc82d7e8f99966cb4c641f7ea5590eaf, purchase_count: 1
1433. product_id_1: 361d8cb449a8b6a7c58b4a0c8ef23888, product_id_2: 82f142f09dd26762af87b2a889f6ed58, purchase_count: 1
1434. product_id_1: 361ecd8e68cab4a2fc502803a9dd790f, product_id_2: 5467d6901b698f1fe968337ee39c5dfd, purchase_count: 1
1435. product_id_1: 362052fcdf7c9e3596a0a6c97536cdc3, product_id_2: 00faa46f36261af8bbf3a4d37fa4841b, purchase_count: 1
1436. product_id_1: 362052fcdf7c9e3596a0a6c97536cdc3, product_id_2: 63094ac128b54dd72d511043411df079, purchase_count: 1
1437. product_id_1: 3625fbaf8284047185fb0351f2f84ae3, product_id_2: 2174a02a3c42e648e408c9b3505c54d3, purchase_count: 1
1438. product_id_1: 3625fbaf8284047185fb0351f2f84ae3, product_id_2: 332842d24e84234cd91299a225de76ab, purchase_count: 1
1439. product_id_1: 363218ba55c610b750224f90bdd34be1, product_id_2: 4cee4c57bf2e00c0c0e10918245491c1, purchase_count: 1
1440. product_id_1: 363218ba55c610b750224f90bdd34be1, product_id_2: ed5122a6a757a4fea8f32a6fb95a5135, purchase_count: 1
1441. product_id_1: 364e789259da982f5b7e43aaea7be615, product_id_2: 50e1b118f266b655f613f753914c42db, purchase_count: 1
1442. product_id_1: 3651da23518f818b7da19d3ec6c69f5e, product_id_2: 0bd7e7a520ec0ac94f95b47cecc844d6, purchase_count: 1
1443. product_id_1: 36696562bef043d7e07305d62baf5ca7, product_id_2: 2b50a33b93e3b489f648b9166a62e13d, purchase_count: 1
1444. product_id_1: 368645a47a15770520ad12d9ea77c2f2, product_id_2: 27761f21b03a32be1aad6ebaebddd747, purchase_count: 1
1445. product_id_1: 368645a47a15770520ad12d9ea77c2f2, product_id_2: 5caaa02918381c4ad59d38fdcd4a28b9, purchase_count: 1
1446. product_id_1: 368645a47a15770520ad12d9ea77c2f2, product_id_2: 5dcd17b12ed2175d4fe6157e047d7be2, purchase_count: 1
1447. product_id_1: 368645a47a15770520ad12d9ea77c2f2, product_id_2: b6e406be1aa00db8be5dd3ec6b524d4d, purchase_count: 1
1448. product_id_1: 368645a47a15770520ad12d9ea77c2f2, product_id_2: f2bec64d5d795250be5e5ec2d38a19b6, purchase_count: 1
1449. product_id_1: 368ab9ae54053acc2a79f2e9f5fb4cbf, product_id_2: e34f7accdfa3f3f2ab0c16db77858f6d, purchase_count: 1
1450. product_id_1: 368aefcea6b2454dff5ce8156ea6766b, product_id_2: ec268f069320a08af47861967e4d7bee, purchase_count: 1
1451. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: 09b0d15a8cc9a84e7af7e0225f67dc45, purchase_count: 1
1452. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: 96f8ecb5e5705b3b726d7e3022622575, purchase_count: 1
1453. product_id_1: 368c6c730842d78016ad823897a372db, product_id_2: a39cc58c1b5926b6f9f378daa89f1315, purchase_count: 1
1454. product_id_1: 36940188c2ad1a212b94931a08cc3c29, product_id_2: 7dfaf5d5673b7663f59e93262a2e393b, purchase_count: 1
1455. product_id_1: 36ba5561e351eef68d3554697132a9a8, product_id_2: 07ffc018eaf23e086370dea42c74077b, purchase_count: 1
1456. product_id_1: 36ba5561e351eef68d3554697132a9a8, product_id_2: cc71cac6380211ba2e17e2b35459488b, purchase_count: 1
1457. product_id_1: 36bd3e4daa4604d112f17dccd24ee59e, product_id_2: f0b543161e745b6c80a79c368db167a5, purchase_count: 1
1458. product_id_1: 36e0d84a068074deed2e9b527917f468, product_id_2: bf7f941911c1e02d8dd6c637811b6127, purchase_count: 1
1459. product_id_1: 36e76b21975cb010ce431815283898dc, product_id_2: 58bde724a1c7fa581fc432dda14450dc, purchase_count: 1
1460. product_id_1: 36e76b21975cb010ce431815283898dc, product_id_2: b046862b2553fe4962392cdc93a2ae93, purchase_count: 1
1461. product_id_1: 36e89a9ec56f96288ea7fbb266132288, product_id_2: 566a14211efb01bf3e8ac11007379e93, purchase_count: 1
1462. product_id_1: 36eabbbffe429d2997d5bf9b40695335, product_id_2: 7b2fc344801b7bd210743493b0cf9385, purchase_count: 1
1463. product_id_1: 36ed32627110790264cb94c9d49ffea1, product_id_2: d0c54febdabb86e59080ec565c461d1e, purchase_count: 1
1464. product_id_1: 36f60d45225e60c7da4558b070ce4b60, product_id_2: 99f5b2240b82bf9387e5cf2fc0335b08, purchase_count: 1
1465. product_id_1: 36f60d45225e60c7da4558b070ce4b60, product_id_2: d5991653e037ccb7af6ed7d94246b249, purchase_count: 1
1466. product_id_1: 371fa349d92646bbeea5873df0bcdc5a, product_id_2: c20a3f598c16d77249da67e81caa8317, purchase_count: 1
1467. product_id_1: 371fa349d92646bbeea5873df0bcdc5a, product_id_2: f70dd37d94cc7026ca198b9d7574c7bc, purchase_count: 1
1468. product_id_1: 372124d6931c4bc48dd0d56075ebee7c, product_id_2: cf28a2b7bc92809a0574cf07772c88c4, purchase_count: 1
1469. product_id_1: 372124d6931c4bc48dd0d56075ebee7c, product_id_2: f4d705aa95ccca448e5b0deb6e5290ba, purchase_count: 1
1470. product_id_1: 372645c7439f9661fbbacfd129aa92ec, product_id_2: 2b10e945dae5434075c8bb2be0d17325, purchase_count: 1
1471. product_id_1: 372645c7439f9661fbbacfd129aa92ec, product_id_2: 3ea30fb7b4c6d17f44c1594a713c224c, purchase_count: 1
1472. product_id_1: 372645c7439f9661fbbacfd129aa92ec, product_id_2: 525947dbe3304ac32bf51602f9557c12, purchase_count: 1
1473. product_id_1: 372645c7439f9661fbbacfd129aa92ec, product_id_2: eb53f94fdc60278efcef123bb275658a, purchase_count: 1
1474. product_id_1: 37318ccebb2ced72bd1b548b55ab4e31, product_id_2: 80826ebdc7be9086c467cb10e61a24c6, purchase_count: 1
1475. product_id_1: 3731a08877914ac1dbf9b7c995854f84, product_id_2: 216ac797639b7734f0b125861ea845ae, purchase_count: 1
1476. product_id_1: 373449943bcfafb2d3ff7423408a1c9d, product_id_2: 6d83ca45d94919027131b87caf3b2a6c, purchase_count: 1
1477. product_id_1: 373449943bcfafb2d3ff7423408a1c9d, product_id_2: 948bd3e9180acc7aa263ae14a2075717, purchase_count: 1
1478. product_id_1: 3736d232d7b439822cdb4cfee973fba0, product_id_2: 01c2e91674406ebaca6a1bbf7f61c3f0, purchase_count: 1
1479. product_id_1: 3736d232d7b439822cdb4cfee973fba0, product_id_2: 44a064a339782c3cdd7e457b169ef0b0, purchase_count: 1
1480. product_id_1: 3736d232d7b439822cdb4cfee973fba0, product_id_2: b07499163c612b591ce1621452672e69, purchase_count: 1
1481. product_id_1: 378bb6601c068c842ca65be6c5e45ccd, product_id_2: 99a4788cb24856965c36a24e339b6058, purchase_count: 1
1482. product_id_1: 37933ba010cb5d5f231585d26287bed3, product_id_2: 20531b0644a0719b8d506c4db3c56609, purchase_count: 1
1483. product_id_1: 37c269354554b312f0c614582c19cf91, product_id_2: a475fdcc33516e3be47806479b670256, purchase_count: 1
1484. product_id_1: 37ca4ae4320cdda8a0ef625049f4cb88, product_id_2: bee84ad17517656f609763f0b124c7e6, purchase_count: 1
1485. product_id_1: 37cdd2e6cf19b94999e23e10cc95cdde, product_id_2: e1a5774894b0dcbed9a61bb82b96b3fd, purchase_count: 1
1486. product_id_1: 37d6f8bf938208f8a2268dd49c2e7c45, product_id_2: f3bc8b0c346a5171a82585b880ba6f29, purchase_count: 1
1487. product_id_1: 37d83d294c825fd69de0dea08933cf40, product_id_2: 967b4ef12fac107d62481097944bc634, purchase_count: 1
1488. product_id_1: 37dffde0476450e75dae423136954b0f, product_id_2: 8a2d3285de64b2117fbf83784acd09fc, purchase_count: 1
1489. product_id_1: 380b4664ba5bb18cc9db78ee6bac3558, product_id_2: 15557c53492889a2b63e65df34a738ab, purchase_count: 1
1490. product_id_1: 380b4664ba5bb18cc9db78ee6bac3558, product_id_2: 16bf176650a888512655cc94f61860e3, purchase_count: 1
1491. product_id_1: 380b4664ba5bb18cc9db78ee6bac3558, product_id_2: 9c7ce59c96e74dfdfc51f13a4a6c3869, purchase_count: 1
1492. product_id_1: 380b4664ba5bb18cc9db78ee6bac3558, product_id_2: c708ba7c6269161f89ce0683cdd7c432, purchase_count: 1
1493. product_id_1: 381169576b9f3c083a1c3261da161a3b, product_id_2: 0fc6914383c2bea767a9562c9d8b43a1, purchase_count: 1
1494. product_id_1: 381fea04c0d7c8bdbcb05f03727a1c07, product_id_2: 81d34fb425382e189529a619f8f2c077, purchase_count: 1
1495. product_id_1: 38273c03eb0f88327f62c1d521260623, product_id_2: 2b8db93524783231aa75136bb201e659, purchase_count: 1
1496. product_id_1: 38273c03eb0f88327f62c1d521260623, product_id_2: 8a9efe06f7135fd2dfc7b84b30144bda, purchase_count: 1
1497. product_id_1: 385a33a408e9c35c9fbc2025c12f3784, product_id_2: b0c8da302d49498d2ce6be8c631e4e20, purchase_count: 1
1498. product_id_1: 386486367c1f9d4f587a8864ccb6902b, product_id_2: 5f2d2e225329430182f0d167faa3779b, purchase_count: 1
1499. product_id_1: 386486367c1f9d4f587a8864ccb6902b, product_id_2: bd5b04e67f3659248acfb0c61c08a9c1, purchase_count: 1
1500. product_id_1: 386eebb43722ab502f04f7900bd2451b, product_id_2: 9e10ae46a3021a02f1692448ef9fa1db, purchase_count: 1
1501. product_id_1: 386eebb43722ab502f04f7900bd2451b, product_id_2: b66270a5d5b3a8585f8314b2f14420fb, purchase_count: 1
1502. product_id_1: 38956cecc0bc8d8837371d0aeeefeb59, product_id_2: 1b1bde24cbdf36a390e1abd717b2f7b0, purchase_count: 1
1503. product_id_1: 3898ab895c82d9286015bde372510180, product_id_2: 9478ba3a27de728ec65cf5048a23f34c, purchase_count: 1
1504. product_id_1: 38991d9514cf1298f8ac1d66d8aefeba, product_id_2: 4310ea4cadd7d41398ba376aa7383f82, purchase_count: 1
1505. product_id_1: 389c2351d11b4f543c93ceb7e966315d, product_id_2: 18bbc803715ffa8ec1b58bd3f737fdca, purchase_count: 1
1506. product_id_1: 389d119b48cf3043d311335e499d9c6b, product_id_2: 774e21c631ca26cba7b5606bdca7460f, purchase_count: 1
1507. product_id_1: 389d119b48cf3043d311335e499d9c6b, product_id_2: 87838c210d9c925acac2619548950502, purchase_count: 1
1508. product_id_1: 389d119b48cf3043d311335e499d9c6b, product_id_2: 97759b2e2035fcd87986a43119b56c7d, purchase_count: 1
1509. product_id_1: 389d119b48cf3043d311335e499d9c6b, product_id_2: abda62f854cffdc94184e6bccadc2286, purchase_count: 1
1510. product_id_1: 389d119b48cf3043d311335e499d9c6b, product_id_2: d1c427060a0f73f6b889a5c7c61f2ac4, purchase_count: 1
1511. product_id_1: 38add59349dc5b9c3effc6b93925cb97, product_id_2: 007c63ae4b346920756b5adcad8095de, purchase_count: 1
1512. product_id_1: 38cd38029795797c97b73421fdad08cf, product_id_2: a50c606310374ff8660bbe03010e021b, purchase_count: 1
1513. product_id_1: 38dbc385d6da7b0e6bd58a90e069653b, product_id_2: e13f46cf68d356e0ac0f32058af20911, purchase_count: 1
1514. product_id_1: 38ef617a023fc4398829dd8c2b9e8be6, product_id_2: 6358f5d1f8bea46b44615a9eaad26f81, purchase_count: 1
1515. product_id_1: 38ef617a023fc4398829dd8c2b9e8be6, product_id_2: ceeb8b2d571b23399910f1b83980c973, purchase_count: 1
1516. product_id_1: 38f894aa22356ddb9e98478fbc016083, product_id_2: bff2390f68a7b76b01ef61b684888261, purchase_count: 1
1517. product_id_1: 3904e66405ea8ec8d104534682a38c6d, product_id_2: ed5f0d58e27cf65a07283c251747936f, purchase_count: 1
1518. product_id_1: 393564b0bcdda0d8c4ada9d780ebcebe, product_id_2: 84f456958365164420cfc80fbe4c7fab, purchase_count: 1
1519. product_id_1: 39397cf4e7567e4360d1cdef4e29744c, product_id_2: 29fd9022374ff3fef2e8f82c39b4133e, purchase_count: 1
1520. product_id_1: 39a0578866cba21bcead91f5221af2a8, product_id_2: 40376ad8bd1bd1066449dbb09440dc43, purchase_count: 1
1521. product_id_1: 39a0578866cba21bcead91f5221af2a8, product_id_2: 834df04774f3aa4b60bfd6f839f448bc, purchase_count: 1
1522. product_id_1: 39a1a3b9314738724fce4b2907ae6686, product_id_2: 168b1b45c68037b0490157ee10540349, purchase_count: 1
1523. product_id_1: 39aa98469aa7460a9764311b3f8efb12, product_id_2: 06edb72f1e0c64b14c5b79353f7abea3, purchase_count: 1
1524. product_id_1: 39b7e02eed5da67f370cfd3f1518fe6c, product_id_2: 59d6e6082548af8b6dbabaceb115c676, purchase_count: 1
1525. product_id_1: 39b86f4e3aedf22731990099a660a6f5, product_id_2: a1250bbcaa645885c9165eab1573b5c6, purchase_count: 1
1526. product_id_1: 39c077875cf3aa49a65aabe97ea0c0d8, product_id_2: 25055c4ea763803958c5c79b99a00439, purchase_count: 1
1527. product_id_1: 39c1ee864a1e202ce16e57becca2f68a, product_id_2: 4e44cdda9e34fe16c6403ae9c67ac7ef, purchase_count: 1
1528. product_id_1: 39cdb64dad488a6037d828d1cd514255, product_id_2: 3a1d2391ad7b58b404bce1939446332b, purchase_count: 1
1529. product_id_1: 39fda099b9edc21f85a80d14021579b5, product_id_2: 696d4f2eb9788764b5872ee5a07a249d, purchase_count: 1
1530. product_id_1: 3a07f82957867a5eb477dc7f2f60c2aa, product_id_2: 87cb507e0daa37bbf34956fd59eba832, purchase_count: 1
1531. product_id_1: 3a12fe499b9342f78cb827ee18393e7f, product_id_2: 96b200840d3b01d948ee9d507f6bcb3e, purchase_count: 1
1532. product_id_1: 3a156bd35ef75525c9b43dbed71a9734, product_id_2: 59dbefe045e850ce6df6b1fd5dce14ba, purchase_count: 1
1533. product_id_1: 3a1d2391ad7b58b404bce1939446332b, product_id_2: 39cdb64dad488a6037d828d1cd514255, purchase_count: 1
1534. product_id_1: 3a22eb30c7bdd30bf0a4729ed8614d82, product_id_2: 9feeadd6b97835152e83e1b25b46f5c4, purchase_count: 1
1535. product_id_1: 3a3232c5a8df0895d04012fb058f4bbe, product_id_2: a0045b8457877b5981ed6c79b9b0765a, purchase_count: 1
1536. product_id_1: 3a3502ecc84a931af1064f5a82ed267a, product_id_2: 99a4788cb24856965c36a24e339b6058, purchase_count: 1
1537. product_id_1: 3a362c0e7f9a69276e2d95869a3e143b, product_id_2: 43b54d1fc56ff394092a3dff6be2d39f, purchase_count: 1
1538. product_id_1: 3a362c0e7f9a69276e2d95869a3e143b, product_id_2: 80c8ded77011b1d2c8e3bdbff65eab23, purchase_count: 1
1539. product_id_1: 3a362c0e7f9a69276e2d95869a3e143b, product_id_2: 99563e23b641c8a43e04e528c10002e9, purchase_count: 1
1540. product_id_1: 3a8b4f569449a1671e0d172023030113, product_id_2: 09d16c9d49e1616a733d22e77507d91d, purchase_count: 1
1541. product_id_1: 3a95236711511b32855804d3a6287595, product_id_2: 0d69c82f1bc2991a5ec6fff3d803876b, purchase_count: 1
1542. product_id_1: 3a98bcea866c31f53b35a41d3822f908, product_id_2: 010a3a47c14f1295796c08419f32cef6, purchase_count: 1
1543. product_id_1: 3a98bcea866c31f53b35a41d3822f908, product_id_2: 16fdfb4f828bedbe3ad9a00162bd5339, purchase_count: 1
1544. product_id_1: 3aaf169c291f3a9e57cae0428e82e545, product_id_2: c1e4bd7e1144f99ac576aedc324a5cb3, purchase_count: 1
1545. product_id_1: 3ab181ea2f9cc4be74bad27ef8a03492, product_id_2: 99a4788cb24856965c36a24e339b6058, purchase_count: 1
1546. product_id_1: 3ab4b1931a4bb6cbef302ea76254e850, product_id_2: d2f5484cbffe4ca766301b21ab9246dd, purchase_count: 1
1547. product_id_1: 3abb0e27cb9374f334c59074d868bcbe, product_id_2: 4715eb4e21b1833327567e8c62ce5790, purchase_count: 1
1548. product_id_1: 3abb0e27cb9374f334c59074d868bcbe, product_id_2: f0c1c1d5ec61ce4c4846abd4283631df, purchase_count: 1
1549. product_id_1: 3ac52f93c2299daa201fbb7ff36546f7, product_id_2: 4ce9ab528124f89e091b17d11aa2e97c, purchase_count: 1
1550. product_id_1: 3ac5a9834cdb5e3a4e47c3535adbff74, product_id_2: 014d94f219fbff1166b9cf700eee36b2, purchase_count: 1
1551. product_id_1: 3af242f6518c23ebab15619fdc356e43, product_id_2: 4cfb235f669979ac1f6a7f9705c1ee81, purchase_count: 1
1552. product_id_1: 3af4f5bb8b0616387fe23646fa94e256, product_id_2: a02d0123079f4ae96001ba2010d1a2df, purchase_count: 1
1553. product_id_1: 3af4f5bb8b0616387fe23646fa94e256, product_id_2: fe9c4b2cf9c3adbaf3644880fb72254d, purchase_count: 1
1554. product_id_1: 3af5874bd2429ed183a5445d1432fcde, product_id_2: df4bcf4a328103951507064660c445e9, purchase_count: 1
1555. product_id_1: 3b037eb584c1cf92fb419eab507121c6, product_id_2: e59dd207c69d86e890febadc796d1078, purchase_count: 1
1556. product_id_1: 3b068029db5363533440150014d95d9b, product_id_2: 09c083c98ccb0062e23ddfa6f70adf13, purchase_count: 1
1557. product_id_1: 3b0f7951038b105522c2d566b54421f7, product_id_2: 2691bad4b1d8eb94ea5f2ccbbd582fca, purchase_count: 1
1558. product_id_1: 3b0f7951038b105522c2d566b54421f7, product_id_2: 5dbf50af9485478b933f1028e108640d, purchase_count: 1
1559. product_id_1: 3b0f7951038b105522c2d566b54421f7, product_id_2: e12b3c9c9c2dd369393d99e021901220, purchase_count: 1
1560. product_id_1: 3b0f7951038b105522c2d566b54421f7, product_id_2: f0b543161e745b6c80a79c368db167a5, purchase_count: 1
1561. product_id_1: 3b17f6528c9e2a01b2f75f844a60ddae, product_id_2: 4a266296cc64880551c3efad9739fb2e, purchase_count: 1
1562. product_id_1: 3b4db17ce4f2c8731f83b093db7aa0b1, product_id_2: cf1d8e226162a1d0ad61f29b7ed72d82, purchase_count: 1
1563. product_id_1: 3b4db17ce4f2c8731f83b093db7aa0b1, product_id_2: e9b3cf27d68caa64832c4a7c460abcb9, purchase_count: 1
1564. product_id_1: 3b94e26edc496743bbce82c42f0a9903, product_id_2: 20531b0644a0719b8d506c4db3c56609, purchase_count: 1
1565. product_id_1: 3b94e26edc496743bbce82c42f0a9903, product_id_2: 78514b0a0cec96621010b7b6a2bfd6c6, purchase_count: 1
1566. product_id_1: 3b9ae31f0791d281038b3ed1e1fe91d5, product_id_2: 68bf40b3abd5ffc25981c25df9ed9087, purchase_count: 1
1567. product_id_1: 3bcf64d8d26d6e06bd568d27fe31d8e8, product_id_2: 6856ab01ef22301e08a45d5842ccb247, purchase_count: 1
1568. product_id_1: 3bf87d2001b8176e6a3ad804b80774b4, product_id_2: 30de9bc2bc110c6a584cacba9c17d88a, purchase_count: 1
1569. product_id_1: 3c025396e63ff6925a3b68781e8b3456, product_id_2: 5415fa4d6c000c97cddafcf0419b09f7, purchase_count: 1
1570. product_id_1: 3c025396e63ff6925a3b68781e8b3456, product_id_2: f59ff3f667dc8dc2b42117736585c1ba, purchase_count: 1
1571. product_id_1: 3c260c3a756ae318837fad7286073c77, product_id_2: db49506c4a19ed884c7df231e08c564f, purchase_count: 1
1572. product_id_1: 3c261802e239d1f2dcda5ed49aa14220, product_id_2: 014a8a503291921f7b004a5215bb3c36, purchase_count: 1
1573. product_id_1: 3c261802e239d1f2dcda5ed49aa14220, product_id_2: a029ecbeadd18685578725691cb11160, purchase_count: 1
1574. product_id_1: 3c44881c6f1115b3a16f8281bb2a83ff, product_id_2: 40c19ad8081c5efe90d93d945287adb8, purchase_count: 1
1575. product_id_1: 3c44881c6f1115b3a16f8281bb2a83ff, product_id_2: e53197022fd9f554e01b9cf4f3c9f249, purchase_count: 1
1576. product_id_1: 3c516e321c28ec378c4342e1845c4332, product_id_2: b992409279b9ab0681b346f1e551ff8d, purchase_count: 1
1577. product_id_1: 3c839ed874f2e0444a38bfc8daf5ad5e, product_id_2: 625218e2e2b4668a47d08911e0def1a4, purchase_count: 1
1578. product_id_1: 3c85232d9c97c6784684288a275f48e0, product_id_2: 48109ec66664d0980876acb3f06a8521, purchase_count: 1
1579. product_id_1: 3c883b9d3fd2d0ce448d4136349dc0a4, product_id_2: 446cf7e594fa3103f5d26069356b55e2, purchase_count: 1
1580. product_id_1: 3c883b9d3fd2d0ce448d4136349dc0a4, product_id_2: e0cf79767c5b016251fe139915c59a26, purchase_count: 1
1581. product_id_1: 3c95f0e78d88cdfb8af7f72dd586a4a0, product_id_2: e89672a9d3b43c622e5301b36eb87cda, purchase_count: 1
1582. product_id_1: 3cb27db8c8015afcf219721d4fc10148, product_id_2: f75eb66dc82bccecabd706bd441cfd3a, purchase_count: 1
1583. product_id_1: 3cc4b421c1f28dd22e86fc4aaafb600e, product_id_2: 16dd49ee10e688f75c41e83b4863f85b, purchase_count: 1
1584. product_id_1: 3cc4b421c1f28dd22e86fc4aaafb600e, product_id_2: 430f4c8e02bd4e1fe6330c38689b54f3, purchase_count: 1
1585. product_id_1: 3cc4b421c1f28dd22e86fc4aaafb600e, product_id_2: 98b22c1129886cbd7fcae69d1c93e442, purchase_count: 1
1586. product_id_1: 3cc4b421c1f28dd22e86fc4aaafb600e, product_id_2: e0cf79767c5b016251fe139915c59a26, purchase_count: 1
1587. product_id_1: 3ce943997ff85cad84ec6770b35d6bcd, product_id_2: 330a8a8d810e84c45bf6fece44e082c8, purchase_count: 1
1588. product_id_1: 3ce943997ff85cad84ec6770b35d6bcd, product_id_2: 716fce31a0173fb20b8b729d68f1446a, purchase_count: 1
1589. product_id_1: 3ce943997ff85cad84ec6770b35d6bcd, product_id_2: b40ec43bdfc6d6fdd65e882066a5c895, purchase_count: 1
1590. product_id_1: 3ceb44c75e6981ff0987bb90c95694c0, product_id_2: 59a0529af96d3d459965f044c5cd1296, purchase_count: 1
1591. product_id_1: 3ceb44c75e6981ff0987bb90c95694c0, product_id_2: 71bd788b998b8394fa883c302c04b08c, purchase_count: 1
1592. product_id_1: 3cebb9158a3aa0b3f78ee0f934c9f032, product_id_2: 694e58e56c74114ee0628c25f3f26f8c, purchase_count: 1
1593. product_id_1: 3cef8174403f4fdedbf24fa67fa9f132, product_id_2: 773a9c97b7435492ec93014cd43ecf77, purchase_count: 1
1594. product_id_1: 3cfabfc4cf61ee4c29199d346f5653c1, product_id_2: 2a97ccde48b4f516a7a76352d03eff88, purchase_count: 1
1595. product_id_1: 3d17d0ed8da715ae25763ce8225b50a3, product_id_2: 32539e75c9d0748f5e063f60e395cc57, purchase_count: 1
1596. product_id_1: 3d50229001636cd5e9851e53383c6b8a, product_id_2: f2ed77847f3b2e104b246bef65f15d0c, purchase_count: 1
1597. product_id_1: 3d59253b36345baaf95246491607ab6e, product_id_2: 3e78cdf699d65e94e6a716be72fb4472, purchase_count: 1
1598. product_id_1: 3d59253b36345baaf95246491607ab6e, product_id_2: f7a5131ee6e422257630fe35c9b7875a, purchase_count: 1
1599. product_id_1: 3d74d787086b0e22ac320ae43b240aea, product_id_2: 70e0c10acc3dd72e17f2136ddb027317, purchase_count: 1
1600. product_id_1: 3d92b609f553af0ae89982e4fae15b1f, product_id_2: 236c8998f9a6e6150cdfb75fed83c15d, purchase_count: 1
1601. product_id_1: 3da76d120922f2c5c94b3ec02db563c9, product_id_2: 530d9436af6fa4960e9754ce4128b468, purchase_count: 1
1602. product_id_1: 3dac223b855944e271f439d6bc318bce, product_id_2: 53759a2ecddad2bb87a079a1f1519f73, purchase_count: 1
1603. product_id_1: 3dac223b855944e271f439d6bc318bce, product_id_2: 77922dd87928c2cf9225946dac2a27a7, purchase_count: 1
1604. product_id_1: 3db10af4436918fa150bb41ae578d812, product_id_2: 2f0f230a6d1c2189c346d0992df870fa, purchase_count: 1
1605. product_id_1: 3dba03040674bea93fb80023b8f72c95, product_id_2: 0333795efd58e3c33c5850b92721c3e4, purchase_count: 1
1606. product_id_1: 3dba03040674bea93fb80023b8f72c95, product_id_2: 5add6c33b03c128b413ddfb2ac185a56, purchase_count: 1
1607. product_id_1: 3dba03040674bea93fb80023b8f72c95, product_id_2: 76397820b3556e99a4a2e3056eca24e5, purchase_count: 1
1608. product_id_1: 3dc0d4afe9ff68f23ee2791a1ac909f4, product_id_2: 573722511f4fc28539f3d8810a50ea1c, purchase_count: 1
1609. product_id_1: 3dc95ebe4e59153d4655472acb2c0785, product_id_2: aeb2f7fc62c8a2a56ae6e2f1b04d4e62, purchase_count: 1
1610. product_id_1: 3dcb77af8b9587985d046b195e105475, product_id_2: 70cd303f8e2dc6c00f5908aa72acdea6, purchase_count: 1
1611. product_id_1: 3dd519e4024a114cdf2825caa88c6091, product_id_2: 12fd8665371236b5b586ea4e448902c8, purchase_count: 1
1612. product_id_1: 3dd7de1b6e3362ad26c1879acc292f19, product_id_2: a4d0871577d73bc394c482dd0998af7d, purchase_count: 1
1613. product_id_1: 3dd7de1b6e3362ad26c1879acc292f19, product_id_2: e044a6c8994164db4e2446054a374b9a, purchase_count: 1
1614. product_id_1: 3dd7de1b6e3362ad26c1879acc292f19, product_id_2: e892e0e01990e737eb81a57db12f8c8c, purchase_count: 1
1615. product_id_1: 3de0f67a3747dbf94f485e9f5843b02d, product_id_2: c4c508eec81b6f7eb8153419004c6450, purchase_count: 1
1616. product_id_1: 3e1fdf945aae119091586c0d20212562, product_id_2: 8a4667ce8c036b0d54dd65a38298bfc0, purchase_count: 1
1617. product_id_1: 3e224d87f9ed6e9ac1b36889371dfe49, product_id_2: 7353d65237c6a5d28f5781889cc58fee, purchase_count: 1
1618. product_id_1: 3e362e76af5b6669122b87d6f0a38eca, product_id_2: d6b80738418fd3491b89c8d2cf5f8256, purchase_count: 1
1619. product_id_1: 3e44b19563ef5a25f4b7e0fdfc3657c3, product_id_2: 26479f7e6b832d2e19a14dd8393bb30f, purchase_count: 1
1620. product_id_1: 3e44b19563ef5a25f4b7e0fdfc3657c3, product_id_2: 41376d63d4c45fe6c7407e838a2befa3, purchase_count: 1
1621. product_id_1: 3e44b19563ef5a25f4b7e0fdfc3657c3, product_id_2: 9648b0bf87f29f78dd9fcbfe58d0e6a6, purchase_count: 1
1622. product_id_1: 3e44b19563ef5a25f4b7e0fdfc3657c3, product_id_2: ad00a218e16f65efb3dfebe514994ca1, purchase_count: 1
1623. product_id_1: 3e45fc327c9740f1ae03383a8e201968, product_id_2: 0042f1a9a7e0edd1400c6cd0fda065f8, purchase_count: 1
1624. product_id_1: 3e5201fe0d1ba474d9b90152c83c706c, product_id_2: 2481a472d98c582b46bc2dfeae6f539f, purchase_count: 1
1625. product_id_1: 3e5201fe0d1ba474d9b90152c83c706c, product_id_2: 2827ebfb043a328a13a06ca9165cad0a, purchase_count: 1
1626. product_id_1: 3e5201fe0d1ba474d9b90152c83c706c, product_id_2: 4d38e93bf8056fbb01a32e72f0257df8, purchase_count: 1
1627. product_id_1: 3e5201fe0d1ba474d9b90152c83c706c, product_id_2: 592962829d5a715304344e656e39108a, purchase_count: 1
1628. product_id_1: 3e5201fe0d1ba474d9b90152c83c706c, product_id_2: 84f456958365164420cfc80fbe4c7fab, purchase_count: 1
1629. product_id_1: 3e5201fe0d1ba474d9b90152c83c706c, product_id_2: 9ad75bd7267e5c724cb42c71ac56ca72, purchase_count: 1
1630. product_id_1: 3e5201fe0d1ba474d9b90152c83c706c, product_id_2: c0293bb52f87cea29cbf4cfa3fa873bc, purchase_count: 1
1631. product_id_1: 3e5201fe0d1ba474d9b90152c83c706c, product_id_2: cd3de1984e1a77b441e1b39b8e334330, purchase_count: 1
1632. product_id_1: 3e5201fe0d1ba474d9b90152c83c706c, product_id_2: eebbed5ed3b134eceb717496c47652ba, purchase_count: 1
1633. product_id_1: 3e6849c6e53482c55a97363674027b4a, product_id_2: c43b672f48eaccbecc94cdf6b4f53485, purchase_count: 1
1634. product_id_1: 3e6d2bde9274ac275013aa90d7e2bf16, product_id_2: 186fe07c8b8005ec6a498587ffbc1352, purchase_count: 1
1635. product_id_1: 3e78cdf699d65e94e6a716be72fb4472, product_id_2: 3d59253b36345baaf95246491607ab6e, purchase_count: 1
1636. product_id_1: 3e78cdf699d65e94e6a716be72fb4472, product_id_2: f7a5131ee6e422257630fe35c9b7875a, purchase_count: 1
1637. product_id_1: 3e7ec3672e5549ba74cf635752bfc70b, product_id_2: 06a7a571bc9fbb103a9c2eb90f89432c, purchase_count: 1
1638. product_id_1: 3ea30fb7b4c6d17f44c1594a713c224c, product_id_2: 372645c7439f9661fbbacfd129aa92ec, purchase_count: 1
1639. product_id_1: 3ea7e516d573a0445abc7cab48949be0, product_id_2: 57a2ee969286488b5437acce27b74259, purchase_count: 1
1640. product_id_1: 3ead2a8b3b92444cfac54979d56c7993, product_id_2: 1b0e9a414e59a00b13262ffb248ed9b4, purchase_count: 1
1641. product_id_1: 3ead2a8b3b92444cfac54979d56c7993, product_id_2: 2b7bb91ceee2bfa598986638fb136ba4, purchase_count: 1
1642. product_id_1: 3ead2a8b3b92444cfac54979d56c7993, product_id_2: 779e74ce337266c06bf392935ab34bc8, purchase_count: 1
1643. product_id_1: 3ead2a8b3b92444cfac54979d56c7993, product_id_2: eeab31cd2a4bcd64e6b249e0a674b3a8, purchase_count: 1
1644. product_id_1: 3eb3d01a76a4cbaff641de8a47e4ebec, product_id_2: 51f3e4065d72846204cb4f46d8d241cf, purchase_count: 1
1645. product_id_1: 3eb3d01a76a4cbaff641de8a47e4ebec, product_id_2: aa39d59b0fe9c8b0162f5d855833c97d, purchase_count: 1
1646. product_id_1: 3ec2984cb2de1675a0306bfc60dbe5a5, product_id_2: 4f27f86d1573b8b74b0928ca649abeac, purchase_count: 1
1647. product_id_1: 3ef9c686c9865f2cfe88cd7f9976fd38, product_id_2: 09ec9df2cf3708ca52a4a6cb64e464f6, purchase_count: 1
1648. product_id_1: 3f1361100ad34281edf04ce745f62b89, product_id_2: a39cc58c1b5926b6f9f378daa89f1315, purchase_count: 1
1649. product_id_1: 3f14d740544f37ece8a9e7bc8349797e, product_id_2: 56cdfe67fbda57c1dcc752f5f361f981, purchase_count: 1
1650. product_id_1: 3f14d740544f37ece8a9e7bc8349797e, product_id_2: 720ebc8cf4ff92f142d18b2cc3615ec3, purchase_count: 1
1651. product_id_1: 3f14d740544f37ece8a9e7bc8349797e, product_id_2: 8e42c31b4ca1afbb6bbe17efdd666cf5, purchase_count: 1
1652. product_id_1: 3f14d740544f37ece8a9e7bc8349797e, product_id_2: f293514e0176006f3af40d473cf24a1e, purchase_count: 1
1653. product_id_1: 3f37f32e535d54ae9b3c1cf62aa76c43, product_id_2: b3e40ff639c185b9d726b4b19c17e6cd, purchase_count: 1
1654. product_id_1: 3f55ca21769e7535d3ba989450207285, product_id_2: 0dda66cf50e9782e3b4499568095bba2, purchase_count: 1
1655. product_id_1: 3f6cfbf79bad1fd33c65e65cde20ab67, product_id_2: fd1061ebebbb9892c59897096066dec5, purchase_count: 1
1656. product_id_1: 3f7965eac71911314776d32209c84483, product_id_2: 26db948671a4ad63637c2d2065477f00, purchase_count: 1
1657. product_id_1: 3f9db4ff95890df33167856d315a05bc, product_id_2: 31fa8a1e88207a7ca942495d88e590c2, purchase_count: 1
1658. product_id_1: 3fa864b2eb9bb60d23bfe315213bb5d9, product_id_2: 1c1dda7d5b3d50618aadda35edc2acd6, purchase_count: 1
1659. product_id_1: 3fa864b2eb9bb60d23bfe315213bb5d9, product_id_2: d69b7880f262ed14de5f8149d2f0931d, purchase_count: 1
1660. product_id_1: 3faadd91c89ff779e6cd1fd09a46ee39, product_id_2: 7d0e0214a0852cf0c90032c7992cf27f, purchase_count: 1
1661. product_id_1: 3fae92f8d0ebb3317991934a6d717c47, product_id_2: 9b02b650be0a39d8590be7d35be443f9, purchase_count: 1
1662. product_id_1: 3fae92f8d0ebb3317991934a6d717c47, product_id_2: fe6f03cedd96bcbc5c8726c5963fd35c, purchase_count: 1
1663. product_id_1: 3fbc0ef745950c7932d5f2a446189725, product_id_2: b2b2279a0174bb3ce78d8b668f8fe27d, purchase_count: 1
1664. product_id_1: 3fbc0ef745950c7932d5f2a446189725, product_id_2: e887a6dd92133f40be82741d1998b9de, purchase_count: 1
1665. product_id_1: 3fce2ec89543bd1ecbc0a87d599bf4f7, product_id_2: 99647594018d3d18ef5c6cc75080a150, purchase_count: 1
1666. product_id_1: 3fd04b238d42b022434a07519d30a354, product_id_2: 32267de030005084d4b6af64f22143b8, purchase_count: 1
1667. product_id_1: 3ff490445b099b53cba94a2dab6f814d, product_id_2: 0786b87f44a44896ee0a59373edfcc50, purchase_count: 1
1668. product_id_1: 3ff90de8afa748b1f8441607fb2b1e49, product_id_2: 0d86ff0b639e969a11a7b3dce67e181c, purchase_count: 1
1669. product_id_1: 3ffa02e2ee2ce17abb51b4545f367e7f, product_id_2: 14dffa241a078aeaebaef48a49e807ca, purchase_count: 1
1670. product_id_1: 3ffc8b6c3ae2afbf307cbd802bfb5e4c, product_id_2: c8078bb7927143cdb008e3563230ca61, purchase_count: 1
1671. product_id_1: 3ffc8b6c3ae2afbf307cbd802bfb5e4c, product_id_2: f52b6b9e0bc35ec9d682eea89b27ef38, purchase_count: 1
1672. product_id_1: 4006da5107400e5ac48dbcc829a36c42, product_id_2: 281905b21f01db1009fd7c01b10dd1d4, purchase_count: 1
1673. product_id_1: 400e2ea46d0af06d91c744b624ed8a59, product_id_2: 40a13d0a09a3d1334e8537ce3194f0ec, purchase_count: 1
1674. product_id_1: 401717fdb76bea40aad511f64ab03c92, product_id_2: 0011c512eb256aa0dbbb544d8dffcf6e, purchase_count: 1
1675. product_id_1: 401717fdb76bea40aad511f64ab03c92, product_id_2: 5a6849f9db912b68be72145d959d61d2, purchase_count: 1
1676. product_id_1: 401717fdb76bea40aad511f64ab03c92, product_id_2: cae8c962ad47ff05a508e6fec4146e1a, purchase_count: 1
1677. product_id_1: 4025ee582ef6b8c478af3b44cf89054b, product_id_2: 10adb53d8faa890ca7c2f0cbcb68d777, purchase_count: 1
1678. product_id_1: 4025ee582ef6b8c478af3b44cf89054b, product_id_2: 31c1d1dfbb4b2730140b8bd9248bcd58, purchase_count: 1
1679. product_id_1: 4025ee582ef6b8c478af3b44cf89054b, product_id_2: cf28a2b7bc92809a0574cf07772c88c4, purchase_count: 1
1680. product_id_1: 40376ad8bd1bd1066449dbb09440dc43, product_id_2: 39a0578866cba21bcead91f5221af2a8, purchase_count: 1
1681. product_id_1: 40376ad8bd1bd1066449dbb09440dc43, product_id_2: 834df04774f3aa4b60bfd6f839f448bc, purchase_count: 1
1682. product_id_1: 404a57563d487aecbc2b1a01d9b89aab, product_id_2: 54f4b6d719759dc811ee18cc95104ed2, purchase_count: 1
1683. product_id_1: 40562621def0bbc3080d94f54b9d1f61, product_id_2: 655110abedc57d73d3b2150d8ba2092a, purchase_count: 1
1684. product_id_1: 40562621def0bbc3080d94f54b9d1f61, product_id_2: 8cc117b0bec16e2f0b683e40846ad09c, purchase_count: 1
1685. product_id_1: 40678c9096047877fa74a25cc6f0a726, product_id_2: 76f520fa5e8912001989fa3fd6530d94, purchase_count: 1
1686. product_id_1: 40678c9096047877fa74a25cc6f0a726, product_id_2: 77d86f9e64c28aa93e3d46f4047646d7, purchase_count: 1
1687. product_id_1: 40678c9096047877fa74a25cc6f0a726, product_id_2: fef0dd8c53552d0f784b7cc5375a3ffe, purchase_count: 1
1688. product_id_1: 4079a95ae53890e5c268117864020aa8, product_id_2: 441f80632def2e872e95a3e474226119, purchase_count: 1
1689. product_id_1: 40a13d0a09a3d1334e8537ce3194f0ec, product_id_2: 400e2ea46d0af06d91c744b624ed8a59, purchase_count: 1
1690. product_id_1: 40a4dfa74a737d541b3c2413edf9cdf6, product_id_2: 02623b0e4e6b951aefb23575de1f3886, purchase_count: 1
1691. product_id_1: 40b6762970c412b5b5392cd0d4c006b1, product_id_2: 05805f52cdeb93d7684f871e599f0078, purchase_count: 1
1692. product_id_1: 40b6762970c412b5b5392cd0d4c006b1, product_id_2: abe171a94bee936786955f928bd764ab, purchase_count: 1
1693. product_id_1: 40b6762970c412b5b5392cd0d4c006b1, product_id_2: c64fe38b4cd06cf7160d9505aa87b8c4, purchase_count: 1
1694. product_id_1: 40c19ad8081c5efe90d93d945287adb8, product_id_2: 3c44881c6f1115b3a16f8281bb2a83ff, purchase_count: 1
1695. product_id_1: 40c6502218c2b8ae624cd1576aac13c1, product_id_2: a3b68fbd8f68d8fdff1dd36cf1336b6b, purchase_count: 1
1696. product_id_1: 40c7fdb4c192c7df52431d1b079f9026, product_id_2: 2136c70bbe723d338fab53da3c03e6dc, purchase_count: 1
1697. product_id_1: 40c9f84a8919516ca9b0d6a9f5ad27f4, product_id_2: a82a1fcaf427ceabe9df656409d7acdb, purchase_count: 1
1698. product_id_1: 40cb7bb3d30559b9b6c4fb62bc837962, product_id_2: b74d57e3377dd78aace6d070fc48cc88, purchase_count: 1
1699. product_id_1: 40cc62bf0cf7aacfd12d865c196baa55, product_id_2: 56d708cb5ce58c2040a3b18a0cb33497, purchase_count: 1
1700. product_id_1: 410d5b211dce5611e7a6412bf0cc30fa, product_id_2: 207bb2d8180c2c7654872f6fab96e40e, purchase_count: 1
1701. product_id_1: 410d5b211dce5611e7a6412bf0cc30fa, product_id_2: 964011954f788aa4bd0dcf7b04056d81, purchase_count: 1
1702. product_id_1: 41225bba70a14ede03816d7baf0a88f8, product_id_2: 96af56bb52888927abc509b1d84bde36, purchase_count: 1
1703. product_id_1: 41376d63d4c45fe6c7407e838a2befa3, product_id_2: 26479f7e6b832d2e19a14dd8393bb30f, purchase_count: 1
1704. product_id_1: 41376d63d4c45fe6c7407e838a2befa3, product_id_2: 3e44b19563ef5a25f4b7e0fdfc3657c3, purchase_count: 1
1705. product_id_1: 41376d63d4c45fe6c7407e838a2befa3, product_id_2: 9648b0bf87f29f78dd9fcbfe58d0e6a6, purchase_count: 1
1706. product_id_1: 41376d63d4c45fe6c7407e838a2befa3, product_id_2: ad00a218e16f65efb3dfebe514994ca1, purchase_count: 1
1707. product_id_1: 41483859d76267ad9a2c8d0af4a76266, product_id_2: 70431405f38dc4a0ee25fbfba20dbd16, purchase_count: 1
1708. product_id_1: 41483859d76267ad9a2c8d0af4a76266, product_id_2: b6665355b9d865e088250a5c8d7b36c1, purchase_count: 1
1709. product_id_1: 414c53fa9c5cc4a0390682aeb2e25ec1, product_id_2: cd98dfe8c9e4a7e14da489ba34f3a845, purchase_count: 1
1710. product_id_1: 415dfa57292b8b7360d3f4cf2f9bff06, product_id_2: 9d0aa87e8df1bdbe0f79353520a2d538, purchase_count: 1
1711. product_id_1: 4167a7ae0930579d1f27d465a1a042f0, product_id_2: 4713819035a9ef628d084f8ff4fa71f2, purchase_count: 1
1712. product_id_1: 4167a7ae0930579d1f27d465a1a042f0, product_id_2: 656e6ea7d86cf0008e67b693d33cc357, purchase_count: 1
1713. product_id_1: 4167a7ae0930579d1f27d465a1a042f0, product_id_2: d13a4acdb64c202e774e815db547e108, purchase_count: 1
1714. product_id_1: 417edf1693aef3f86b922c6a1a52daef, product_id_2: a5b15c8b0abb9a1e7eb10546441925d0, purchase_count: 1
1715. product_id_1: 419365ae77de855075ecb3c55d2ebc10, product_id_2: 65e6eb6259c9963d133eae35ca1ee2cd, purchase_count: 1
1716. product_id_1: 419ad775cb3c503c2ef135826f81065d, product_id_2: e9dd44f105ffdcb98405c94f1d0bbdd9, purchase_count: 1
1717. product_id_1: 41b43381a92451746dc1374dbbd4c43e, product_id_2: 2a5806f10d0f00e5ad032dd2e3c8806e, purchase_count: 1
1718. product_id_1: 41b4baff1ceec845ba126eaeb07efa4a, product_id_2: dd60cac04e6bcbc919cb1c7dcc473211, purchase_count: 1
1719. product_id_1: 41c24b8ce92d1a2cac62db5edfd088b2, product_id_2: 0a57f7d2c983bcf8188589a5fea4a8da, purchase_count: 1
1720. product_id_1: 41c24b8ce92d1a2cac62db5edfd088b2, product_id_2: 2ffdf10e724b958c0f7ea69e97d32f64, purchase_count: 1
1721. product_id_1: 41c24b8ce92d1a2cac62db5edfd088b2, product_id_2: 7a10781637204d8d10485c71a6108a2e, purchase_count: 1
1722. product_id_1: 41ce18e06273b50422ebf6149066fa23, product_id_2: ec72556b5da399d24fe06338e816a9ac, purchase_count: 1
1723. product_id_1: 41db6d8062fcd38410c699743ccc0265, product_id_2: a35a9f46dcee0a67c8c7ad8493eb4135, purchase_count: 1
1724. product_id_1: 41db6d8062fcd38410c699743ccc0265, product_id_2: eba9c1e37886a1be0cb4bbb39321e914, purchase_count: 1
1725. product_id_1: 41e153b95adc3c7f781b583292f312cd, product_id_2: b386ba93c190eb3114ed44584a207b10, purchase_count: 1
1726. product_id_1: 41e69d7f18786d26805f7067f605e675, product_id_2: 826990bc0af28681bde1dcd66a336763, purchase_count: 1
1727. product_id_1: 41f5f13f79496717b1d90ef30551333b, product_id_2: 014a8a503291921f7b004a5215bb3c36, purchase_count: 1
1728. product_id_1: 4228398e19ac96e84e14924449bac556, product_id_2: 5f504b3a1c75b73d6151be81eb05bdc9, purchase_count: 1
1729. product_id_1: 422879e10f46682990de24d770e7f83d, product_id_2: 4c183b9527d3fc69a4d5587b11f5fced, purchase_count: 1
1730. product_id_1: 422879e10f46682990de24d770e7f83d, product_id_2: 88e40881adf08ea3b87cb1d65c8c1d83, purchase_count: 1
1731. product_id_1: 422879e10f46682990de24d770e7f83d, product_id_2: a6be3b3eaae040735e86e4376ea77515, purchase_count: 1
1732. product_id_1: 422879e10f46682990de24d770e7f83d, product_id_2: ba92b5a0701d2f820ba6ca8f8c86294f, purchase_count: 1
1733. product_id_1: 422879e10f46682990de24d770e7f83d, product_id_2: d363e421b1d15376b299089946fed127, purchase_count: 1
1734. product_id_1: 422879e10f46682990de24d770e7f83d, product_id_2: e11092e9722d1b6f8c18cd8947a1daff, purchase_count: 1
1735. product_id_1: 422879e10f46682990de24d770e7f83d, product_id_2: eb6c2ecde53034fc9ec47741b3232c9d, purchase_count: 1
1736. product_id_1: 422879e10f46682990de24d770e7f83d, product_id_2: f45cf520fba787f057d57c5c8138668f, purchase_count: 1
1737. product_id_1: 4231002e80d2a25aed31d65b4b91f479, product_id_2: 72de34cc9f1e580f4c11d830be654271, purchase_count: 1
1738. product_id_1: 4231002e80d2a25aed31d65b4b91f479, product_id_2: a54f350cdb1f303fe39221171d003852, purchase_count: 1
1739. product_id_1: 423508a562a915a6a9454374fb6a4c70, product_id_2: 89b121bee266dcd25688a1ba72eefb61, purchase_count: 1
1740. product_id_1: 423b46d7ff817b1cd19ab195c7b76546, product_id_2: 6fd82d8f842424334fedf31190e54d24, purchase_count: 1
1741. product_id_1: 423b46d7ff817b1cd19ab195c7b76546, product_id_2: eccec1984cb1d214cc91f3168b113958, purchase_count: 1
1742. product_id_1: 4244733e06e7ecb4970a6e2683c13e61, product_id_2: 436c8d57ff8d4aa254318e9bd9b48c83, purchase_count: 1
1743. product_id_1: 425cfc055cf3bee60a67ee33dc577c95, product_id_2: 76ddffabf65608c9e0cfce92e390a193, purchase_count: 1
1744. product_id_1: 42697582a754e573f9e3e9e78752252c, product_id_2: 0aa186c65b07e61f5ac114182ab92a2b, purchase_count: 1
1745. product_id_1: 42697582a754e573f9e3e9e78752252c, product_id_2: ff285e6c96040323d3763dd184924018, purchase_count: 1
1746. product_id_1: 42874c3f68eae9f0408dc1027edcaa6f, product_id_2: d918b3f4aa5272c2c3cd088d087ca069, purchase_count: 1
1747. product_id_1: 428f4b96ba9f630e761b333673039ae6, product_id_2: 1a428b685ede76217c9efb550c4aaa59, purchase_count: 1
1748. product_id_1: 4293865e4ead3d446609086b4cfedb4f, product_id_2: 0fa81e7123fd0ebe03adbbe99d912827, purchase_count: 1
1749. product_id_1: 4293865e4ead3d446609086b4cfedb4f, product_id_2: 87d780fa7d2cf3710aa02dc4ca8db985, purchase_count: 1
1750. product_id_1: 4293865e4ead3d446609086b4cfedb4f, product_id_2: c211ff3068fcd2f8898192976d8b3a32, purchase_count: 1
1751. product_id_1: 4298b7e67dc399c200662b569563a2b2, product_id_2: eaa26a34984cbfedc19b1e45f09f3c9a, purchase_count: 1
1752. product_id_1: 4299211de0fa49785bb3115aa2b25c61, product_id_2: 14ff2fd93669cee55ac37385a7409d5d, purchase_count: 1
1753. product_id_1: 4299cf45bc9aa8ef5bd9337035c286e5, product_id_2: 1c5b28beb34835f960261f45ba22a136, purchase_count: 1
1754. product_id_1: 429e7401fafb76436f15e86498bd7364, product_id_2: eb53f94fdc60278efcef123bb275658a, purchase_count: 1
1755. product_id_1: 42a2bd596fda1baef5719cb74f73030c, product_id_2: 0fa81e7123fd0ebe03adbbe99d912827, purchase_count: 1
1756. product_id_1: 42a2bd596fda1baef5719cb74f73030c, product_id_2: 1a2d00b771a438bee7055bbd0086e003, purchase_count: 1
1757. product_id_1: 42a2bd596fda1baef5719cb74f73030c, product_id_2: 99a4788cb24856965c36a24e339b6058, purchase_count: 1
1758. product_id_1: 42a2c92a0979a949ca4ea89ec5c7b934, product_id_2: 31fd02b02c33827cbde22902cf80338c, purchase_count: 1
1759. product_id_1: 42a2c92a0979a949ca4ea89ec5c7b934, product_id_2: fe6a9515d655fa7936b8a7c841039f34, purchase_count: 1
1760. product_id_1: 42af75da4dff5f8f6be029c5bdd5f08f, product_id_2: 7aa53bb43cb5b12d70be2a69d1e3c364, purchase_count: 1
1761. product_id_1: 42c28e0e09e582dfd979242c53111e6e, product_id_2: 1ef5ef43b311a978115840517ac78943, purchase_count: 1
1762. product_id_1: 42ca857208d059f51c317b503000c385, product_id_2: 208c1210f363c82510f5609d5feb0341, purchase_count: 1
1763. product_id_1: 42ef2bdec0493fd90852352fcfbf2c24, product_id_2: 3516632e8f52b679ff83d1665ecc990e, purchase_count: 1
1764. product_id_1: 42f14eda412436b96cde4f4025ed5f25, product_id_2: e146dbd6493fdfb50152400fc162f25a, purchase_count: 1
1765. product_id_1: 42faf2e98f0486405f5dfac48e5cba7d, product_id_2: 686f5682d2be7689714c5fae465de396, purchase_count: 1
1766. product_id_1: 42faf2e98f0486405f5dfac48e5cba7d, product_id_2: 6fb42788c5ef9affaa2fec30ca8b6053, purchase_count: 1
1767. product_id_1: 430f4c8e02bd4e1fe6330c38689b54f3, product_id_2: 3cc4b421c1f28dd22e86fc4aaafb600e, purchase_count: 1
1768. product_id_1: 430f4c8e02bd4e1fe6330c38689b54f3, product_id_2: a04f52ded97b5530e8783e3c002b90f0, purchase_count: 1
1769. product_id_1: 4310ea4cadd7d41398ba376aa7383f82, product_id_2: 38991d9514cf1298f8ac1d66d8aefeba, purchase_count: 1
1770. product_id_1: 432357855585cf634fc9923523ce5e4a, product_id_2: aeecb1d0e5d4d5ccc3fcfe6fe91103b6, purchase_count: 1
1771. product_id_1: 432357855585cf634fc9923523ce5e4a, product_id_2: e2f1ccf86759df28dd1e9f2e0e3242d4, purchase_count: 1
1772. product_id_1: 43423cdffde7fda63d0414ed38c11a73, product_id_2: 2136c70bbe723d338fab53da3c03e6dc, purchase_count: 1
1773. product_id_1: 43423cdffde7fda63d0414ed38c11a73, product_id_2: 7703b8cb5b77fbb36518ea91e2ca734f, purchase_count: 1
1774. product_id_1: 43423cdffde7fda63d0414ed38c11a73, product_id_2: 87cb507e0daa37bbf34956fd59eba832, purchase_count: 1
1775. product_id_1: 43423cdffde7fda63d0414ed38c11a73, product_id_2: a84d0660dbffebf352aefbf1a6b18d00, purchase_count: 1
1776. product_id_1: 43423cdffde7fda63d0414ed38c11a73, product_id_2: f4387cd405b21509803344d044ac2c3c, purchase_count: 1
1777. product_id_1: 43521df044c196283191f87529d1663f, product_id_2: f5790565f09ac993cd58c68bc58c2daa, purchase_count: 1
1778. product_id_1: 436c8d57ff8d4aa254318e9bd9b48c83, product_id_2: 4244733e06e7ecb4970a6e2683c13e61, purchase_count: 1
1779. product_id_1: 436c8d57ff8d4aa254318e9bd9b48c83, product_id_2: 7f1a77bec0639e473392e91a504272a5, purchase_count: 1
1780. product_id_1: 4374f5c6e8ab35133a8dbc5517ec0388, product_id_2: fad4c004f68304a86535ea71c79cfaa4, purchase_count: 1
1781. product_id_1: 438b5ad4eda7949fae4a4b834a69bcd6, product_id_2: b66270a5d5b3a8585f8314b2f14420fb, purchase_count: 1
1782. product_id_1: 438b5ad4eda7949fae4a4b834a69bcd6, product_id_2: cec09725da5ed01471d9a505e7389d37, purchase_count: 1
1783. product_id_1: 4390e4e834a8679a940d6795b52b5e58, product_id_2: 6cd26b425f717a6d9202bc287c9d5e6d, purchase_count: 1
1784. product_id_1: 4395690ceee4379785f481610bf962ac, product_id_2: 5594eb45b3ced02488aaf71edfb32d92, purchase_count: 1
1785. product_id_1: 439d0c278b77ddc4b1488de210c8df35, product_id_2: 0e71c6a889baea05c4c9ce1b0d58114d, purchase_count: 1
1786. product_id_1: 439d0c278b77ddc4b1488de210c8df35, product_id_2: 4487261e208ce5d3a8d1a997ccd99dcf, purchase_count: 1
1787. product_id_1: 43a888fc6acdffc23011578f63d5f045, product_id_2: 8e87f0e6eb7e5a27568309035f4fc854, purchase_count: 1
1788. product_id_1: 43b069f855679eb3d3589e55dcfe968e, product_id_2: 6ddc8b938d09dc6cdc48aff7252e5f0e, purchase_count: 1
1789. product_id_1: 43b54d1fc56ff394092a3dff6be2d39f, product_id_2: 3a362c0e7f9a69276e2d95869a3e143b, purchase_count: 1
1790. product_id_1: 43b54d1fc56ff394092a3dff6be2d39f, product_id_2: 4f0abfbee7569e43b80f9aaa256a9bf8, purchase_count: 1
1791. product_id_1: 43b54d1fc56ff394092a3dff6be2d39f, product_id_2: 656e6ea7d86cf0008e67b693d33cc357, purchase_count: 1
1792. product_id_1: 43b54d1fc56ff394092a3dff6be2d39f, product_id_2: c589625c8ccc7bfd2e8f1fb041e24c4a, purchase_count: 1
1793. product_id_1: 43b54d1fc56ff394092a3dff6be2d39f, product_id_2: f889fb87b505b73de10c18b93352469f, purchase_count: 1
1794. product_id_1: 43c78a3f875907bf2e94679f591c4724, product_id_2: 10aecaf5be4119fd6b8b9e2e8a5a1454, purchase_count: 1
1795. product_id_1: 43c9506443a52a22cace92d7eef9cfcb, product_id_2: 93d9ed4fb2b32cec509eae4f1860687d, purchase_count: 1
1796. product_id_1: 43df79876ad10b1a273644d9e177da75, product_id_2: 03624ffc0958f7ea385b6d4e088532b0, purchase_count: 1
1797. product_id_1: 43ee88561093499d9e571d4db5f20b79, product_id_2: e7593e3c84b3302e1531a715f1ded8b2, purchase_count: 1
1798. product_id_1: 4407440c06d8c11ce1b2e61c4382a8f3, product_id_2: a1e33e0a3ead282527fab4ff0f72706b, purchase_count: 1
1799. product_id_1: 441293f432282ea2ab9c82fe5f0fb875, product_id_2: 817e1c2d22418c36386406ccacfa53e8, purchase_count: 1
1800. product_id_1: 441293f432282ea2ab9c82fe5f0fb875, product_id_2: 9163c7e81fd68452472912c4cde810aa, purchase_count: 1
1801. product_id_1: 441f80632def2e872e95a3e474226119, product_id_2: 4079a95ae53890e5c268117864020aa8, purchase_count: 1
1802. product_id_1: 442484911e00b4bff85ece3e10c1dc1f, product_id_2: 53759a2ecddad2bb87a079a1f1519f73, purchase_count: 1
1803. product_id_1: 4428c8810d85a949afe441cc0d33f756, product_id_2: 783caabd539c4079ec08423e30719fba, purchase_count: 1
1804. product_id_1: 44291e25afe160dfe5f844da1b0f8b15, product_id_2: 017692475c1c954ff597feda05131d73, purchase_count: 1
1805. product_id_1: 44291e25afe160dfe5f844da1b0f8b15, product_id_2: f2ecbb02b6da187a9f14b8ac5781faec, purchase_count: 1
1806. product_id_1: 4432acdc80e1b1f73f9f355f12ecd60f, product_id_2: b842a6c9c2c51a699729d378d8d674fc, purchase_count: 1
1807. product_id_1: 446607005fbc439a9439caed96867e26, product_id_2: 82254d93b897fde054504b15f8fe923c, purchase_count: 1
1808. product_id_1: 446a112adf10992c2e26eb566a68bd46, product_id_2: 0d86ab499a2af7f2352d18e2a6be12f4, purchase_count: 1
1809. product_id_1: 446a112adf10992c2e26eb566a68bd46, product_id_2: eac61d05154fde75066aa2e1758ecdb1, purchase_count: 1
1810. product_id_1: 446a60562915e8223780cd142b8dc26d, product_id_2: 0c80d4d910506b4e1db996ff1fa5c658, purchase_count: 1
1811. product_id_1: 446a60562915e8223780cd142b8dc26d, product_id_2: 3017341f6eb19840f64bd672370a91cc, purchase_count: 1
1812. product_id_1: 446cf7e594fa3103f5d26069356b55e2, product_id_2: 3c883b9d3fd2d0ce448d4136349dc0a4, purchase_count: 1
1813. product_id_1: 4473f3e5c65952b074ef987fa5c24662, product_id_2: 57d79905de06d8897872c551bfd09358, purchase_count: 1
1814. product_id_1: 4487261e208ce5d3a8d1a997ccd99dcf, product_id_2: 439d0c278b77ddc4b1488de210c8df35, purchase_count: 1
1815. product_id_1: 44a064a339782c3cdd7e457b169ef0b0, product_id_2: 01c2e91674406ebaca6a1bbf7f61c3f0, purchase_count: 1
1816. product_id_1: 44a064a339782c3cdd7e457b169ef0b0, product_id_2: 3736d232d7b439822cdb4cfee973fba0, purchase_count: 1
1817. product_id_1: 44a064a339782c3cdd7e457b169ef0b0, product_id_2: b07499163c612b591ce1621452672e69, purchase_count: 1
1818. product_id_1: 44a6af14e39124bee07dc2eb2df39a54, product_id_2: a8949536a84721e346d7814fd81aafbe, purchase_count: 1
1819. product_id_1: 44a6af14e39124bee07dc2eb2df39a54, product_id_2: b2b938c46aafdbf702d73e7edb9cb263, purchase_count: 1
1820. product_id_1: 44a6af14e39124bee07dc2eb2df39a54, product_id_2: def59eb2e17b32b980b5341984f6b500, purchase_count: 1
1821. product_id_1: 44a6e4ecf7b48f87481c243383b1c4cf, product_id_2: 9b9d1c4bd979b93c138044e032f99780, purchase_count: 1
1822. product_id_1: 44a6e4ecf7b48f87481c243383b1c4cf, product_id_2: bdef40d64bf3de5f773c8f461b0bf167, purchase_count: 1
1823. product_id_1: 44aadbb26d5c81d9846b0c48bc00d7a3, product_id_2: 06edb72f1e0c64b14c5b79353f7abea3, purchase_count: 1
1824. product_id_1: 44ae8d3edf5612ff7a39d629d5bbb8ae, product_id_2: be59f0b9bd1d08d096188f98168fc987, purchase_count: 1
1825. product_id_1: 44ae8d3edf5612ff7a39d629d5bbb8ae, product_id_2: f353779abb6114db5f8f79fbad12e375, purchase_count: 1
1826. product_id_1: 44b63b148b673cb9a06672f06683b9b4, product_id_2: 727017cd91a0361b8ae4cfcff15e9682, purchase_count: 1
1827. product_id_1: 44b6fc0101a9341e43ad3342a51ef75b, product_id_2: 6fb9118651534879ecb3654b56a48a4c, purchase_count: 1
1828. product_id_1: 44d097d59e8430f88a67517cd0c4f865, product_id_2: 5d7c23067ed3fc8c6e699b9373d5890b, purchase_count: 1
1829. product_id_1: 44d097d59e8430f88a67517cd0c4f865, product_id_2: a38e6346616a8f362c328b9537b1ca4d, purchase_count: 1
1830. product_id_1: 44d097d59e8430f88a67517cd0c4f865, product_id_2: d017a2151d543a9885604dc62a3d9dcc, purchase_count: 1
1831. product_id_1: 44d958961868395bfe852e70d48081f4, product_id_2: 6b00cb3fe05c73d0acef3fd949a34c0f, purchase_count: 1
1832. product_id_1: 44d958961868395bfe852e70d48081f4, product_id_2: e3af4b7c220aca1535b34416de24dfb7, purchase_count: 1
1833. product_id_1: 44e8945e17aef03daaecbc4bbab7f730, product_id_2: 4dfb5b21cf54e026b36472ea52d67e6d, purchase_count: 1
1834. product_id_1: 44f33e4105880d97c9db2506954dbfa3, product_id_2: c2d28f0e9e7925b59ea575da70e8f884, purchase_count: 1
1835. product_id_1: 44f90f085c7a825863cbf867990e1513, product_id_2: 1fe8e6e01596885617fa1c90d29c2f81, purchase_count: 1
1836. product_id_1: 44f90f085c7a825863cbf867990e1513, product_id_2: 4c8541293fb2d3359cf52485b4d59b8e, purchase_count: 1
1837. product_id_1: 44f90f085c7a825863cbf867990e1513, product_id_2: f0fe4af158ebc28426b794c0b54d3df1, purchase_count: 1
1838. product_id_1: 44feb28a74abb0f2f303412d60160750, product_id_2: d8f1b415091ab79b62ac80443d865ca6, purchase_count: 1
1839. product_id_1: 451482edc91f59c001a5a3a0e4d594bf, product_id_2: 21d2fdced5c69bfc6539b67908a4ad28, purchase_count: 1
1840. product_id_1: 451482edc91f59c001a5a3a0e4d594bf, product_id_2: 6962734c72522e70e852a2a77d21a730, purchase_count: 1
1841. product_id_1: 4525ba25c6fe12c6c01f869b3226d8e4, product_id_2: dff2d533131f407db58a34fd3f832821, purchase_count: 1
1842. product_id_1: 452f66a0f164cac57802e2cea93188ac, product_id_2: 801e1758675639e98967a271d92f4054, purchase_count: 1
1843. product_id_1: 454ae5002aaf2821ecb6ad6035b78498, product_id_2: b74e40daa954e92be8e5d3b342fa8863, purchase_count: 1
1844. product_id_1: 4563095e06df1fa67de2eade86f4f01b, product_id_2: 2ff995aead9c63a1f37a07b3664ead37, purchase_count: 1
1845. product_id_1: 457cd0a99cfa977993e4eb6d98d95abb, product_id_2: a8d952e8e5436a6fe36d24c402d100de, purchase_count: 1
1846. product_id_1: 457d976782cfef787ee35098bc9e4624, product_id_2: a6e9ad7f801066f00bf59e348ec8f3d6, purchase_count: 1
1847. product_id_1: 45817bdb08cc2ba11a384d7428d95da9, product_id_2: d720657d6b64788e2b9e29f9a07f5797, purchase_count: 1
1848. product_id_1: 45cfee87da128a8f939226bedd92a72d, product_id_2: 99f8a7e47970133c14b3d79c27d921c8, purchase_count: 1
1849. product_id_1: 45dc66388e0aeec2e8baab5572f2fa44, product_id_2: 0aabfb375647d9738ad0f7b4ea3653b1, purchase_count: 1
1850. product_id_1: 45e9db074ca64dc81ee6f06185544d6e, product_id_2: 9c7bdf67b06b419aefb93cfdfc96c55d, purchase_count: 1
1851. product_id_1: 45f0310974e6082deeda855f91984347, product_id_2: 87351480a75abfcf15ec67af64f28ee6, purchase_count: 1
1852. product_id_1: 45fc964dc03d16147f82dbe844e2cdf1, product_id_2: ea3da91e6ba865972f9344cb9265296b, purchase_count: 1
1853. product_id_1: 460a66fcc404a3d7306d5f50fcb2d18a, product_id_2: cbe73e033835920bea2c769177237510, purchase_count: 1
1854. product_id_1: 4610f9bc86835033aab4160bcb1c3d27, product_id_2: 98cd3776d33bddd0ebf8ad8b4732d1b4, purchase_count: 1
1855. product_id_1: 461ad76d92ef0858a087d05f96b7d6e5, product_id_2: 8c35dc99b37ba51780800ba049ed3616, purchase_count: 1
1856. product_id_1: 461f43be3bdf8844e65b62d9ac2c7a5a, product_id_2: 1b474c650cb9407d32a1e066937b68fd, purchase_count: 1
1857. product_id_1: 461f43be3bdf8844e65b62d9ac2c7a5a, product_id_2: 6eb70dfb283dc3f645ed7b03c990dc72, purchase_count: 1
1858. product_id_1: 4621f88827b983332c2a833d49c2ae35, product_id_2: 0160785b697a5ea87d52949bd097ce05, purchase_count: 1
1859. product_id_1: 4630761de87581e8b659dc77bb7eb4ee, product_id_2: ca753b1e379d59868172ac9d8d62d14f, purchase_count: 1
1860. product_id_1: 464a2bd11ce5cf1fcfb4f609dedcf914, product_id_2: 1c55a8be0613dd888ed9c039cea3d660, purchase_count: 1
1861. product_id_1: 464a2bd11ce5cf1fcfb4f609dedcf914, product_id_2: caf9add3dcd98d688be0064d9faf65b1, purchase_count: 1
1862. product_id_1: 4650fae75d852ddfada4751f6f02481a, product_id_2: 0f6e214a2c5baab8c1ccb053a0829f13, purchase_count: 1
1863. product_id_1: 4650fae75d852ddfada4751f6f02481a, product_id_2: 274d4e727ddbeb7c392ea2e551e3a77d, purchase_count: 1
1864. product_id_1: 4650fae75d852ddfada4751f6f02481a, product_id_2: 521527593ca1726b992318e034dd5690, purchase_count: 1
1865. product_id_1: 4650fae75d852ddfada4751f6f02481a, product_id_2: 75bc68276acddf2f0940f421a54338ee, purchase_count: 1
1866. product_id_1: 4650fae75d852ddfada4751f6f02481a, product_id_2: a25583531530c0913ea4dee2c5c73685, purchase_count: 1
1867. product_id_1: 4660b448a9e1499945013a9fb3f11ec4, product_id_2: cc63d91555437d9d8d9ae7bf007a1f2c, purchase_count: 1
1868. product_id_1: 4689718bc1b839a9baeaa91d2c278598, product_id_2: 30caacf4dfc199dc577a9627395a881d, purchase_count: 1
1869. product_id_1: 4697e1b622324d38a8989bff2bdc1c84, product_id_2: 786248c98cab9ad5cccdb751909da1af, purchase_count: 1
1870. product_id_1: 4697e1b622324d38a8989bff2bdc1c84, product_id_2: bbdf7b7e937d9526d3acd9854d7e939b, purchase_count: 1
1871. product_id_1: 4697e1b622324d38a8989bff2bdc1c84, product_id_2: e82b2802625252b6d72b3e1d36f82670, purchase_count: 1
1872. product_id_1: 46ae1c0789fb281be43fdb50797c9f2e, product_id_2: ddc46156c31a0339508eecfab975f4f6, purchase_count: 1
1873. product_id_1: 46b48281eb6d663ced748f324108c733, product_id_2: e04dcf463871a7c73df38d4bcc245686, purchase_count: 1
1874. product_id_1: 46b609a28b05ef9d5179026a055c5121, product_id_2: 9f684ef1e31358afd3d4ce991c576e2e, purchase_count: 1
1875. product_id_1: 46b609a28b05ef9d5179026a055c5121, product_id_2: bf6c420d93ff5c0a5d8fd3b6c975dbd5, purchase_count: 1
1876. product_id_1: 46bc787381b2bee84ed87b4ebce24505, product_id_2: 53b660897772d156d1b39afcd576663f, purchase_count: 1
1877. product_id_1: 46e24ce614899e36617e37ea1e4aa6ff, product_id_2: 2b4609f8948be18874494203496bc318, purchase_count: 1
1878. product_id_1: 46e477d89da734ac9f6b12073503711a, product_id_2: 5bd7e57735a44e529bf066fee83a9c60, purchase_count: 1
1879. product_id_1: 46e477d89da734ac9f6b12073503711a, product_id_2: 8b51c6ccc9c0548c951214e1cd1547ff, purchase_count: 1
1880. product_id_1: 46e477d89da734ac9f6b12073503711a, product_id_2: e9e1e0a297e5a8f045e8c0395c4c745b, purchase_count: 1
1881. product_id_1: 46e4940f28c9231a801873e62ca55c53, product_id_2: 4ad4cf9cb1cce9af79caf2426fd9ab93, purchase_count: 1
1882. product_id_1: 46e4940f28c9231a801873e62ca55c53, product_id_2: e9ed063dacf96b73a9567bf943e5f708, purchase_count: 1
1883. product_id_1: 46ed0917b696c5c8c934e368da2fec36, product_id_2: e25a1bed3de19f42a0719cff1c771436, purchase_count: 1
1884. product_id_1: 4713819035a9ef628d084f8ff4fa71f2, product_id_2: 4167a7ae0930579d1f27d465a1a042f0, purchase_count: 1
1885. product_id_1: 4715eb4e21b1833327567e8c62ce5790, product_id_2: 3abb0e27cb9374f334c59074d868bcbe, purchase_count: 1
1886. product_id_1: 4715eb4e21b1833327567e8c62ce5790, product_id_2: f0c1c1d5ec61ce4c4846abd4283631df, purchase_count: 1
1887. product_id_1: 471e714759273827991f1746906737d1, product_id_2: d017a2151d543a9885604dc62a3d9dcc, purchase_count: 1
1888. product_id_1: 4720b3e7d949046722aaa29eb7c29d9f, product_id_2: 8fbcb15797c830eb81cb3368ffe4a851, purchase_count: 1
1889. product_id_1: 4737840499dd8ffb4c3e54caf8a3ab9a, product_id_2: 497afaeae8d825d8938d01e92007f654, purchase_count: 1
1890. product_id_1: 473795a355d29305c3ea6b156833adf5, product_id_2: 6ae7f4ef0ca670ca2609d039af87d057, purchase_count: 1
1891. product_id_1: 473795a355d29305c3ea6b156833adf5, product_id_2: 7cd29da0653abeb444703cc5a957f479, purchase_count: 1
1892. product_id_1: 473ecd4c15ecda05e4044ef14f1f4c2e, product_id_2: 1fc6e1729d564ec77eeeb9df95fca74f, purchase_count: 1
1893. product_id_1: 474bb6b54fc608ca71059a6c4f7ecda3, product_id_2: 566a4f2c4385f36d15c00dfcaae132d1, purchase_count: 1
1894. product_id_1: 4754d89182db4010eabbf20da5fb7191, product_id_2: 24aba57735be13fd785bc04d1a8812e4, purchase_count: 1
1895. product_id_1: 477aa9a85d7002688bae2cbbd93198f8, product_id_2: 23ab7bb9eac81e85ec43ed71064cf7ce, purchase_count: 1
1896. product_id_1: 477aa9a85d7002688bae2cbbd93198f8, product_id_2: 3234b4f9542a9f6a450e988820390fab, purchase_count: 1
1897. product_id_1: 477aa9a85d7002688bae2cbbd93198f8, product_id_2: 99c88c191bbed92f5be4ca3b00eb1a42, purchase_count: 1
1898. product_id_1: 477aa9a85d7002688bae2cbbd93198f8, product_id_2: b0c89945c034268074f5f80b362bda34, purchase_count: 1
1899. product_id_1: 477aa9a85d7002688bae2cbbd93198f8, product_id_2: d16c0ea701551e609316c77d5c533591, purchase_count: 1
1900. product_id_1: 477aa9a85d7002688bae2cbbd93198f8, product_id_2: fc6b299cf83fa76632dd1b0a2c611f33, purchase_count: 1
1901. product_id_1: 47859fca9dd7485cbd93c3e8993bb74f, product_id_2: 542d6af4881a5a647cde02c201f43916, purchase_count: 1
1902. product_id_1: 479d5974c7824b584a62c88885c957b4, product_id_2: ffb2e8c1ddc7c3e590d2bc4c91de53e1, purchase_count: 1
1903. product_id_1: 47a3fbd41bb53db64dacc4562ba3aa52, product_id_2: a5502e9954017124d95f7bce4c89d339, purchase_count: 1
1904. product_id_1: 47a3fbd41bb53db64dacc4562ba3aa52, product_id_2: e2e426d1332240070b0a836a854d057b, purchase_count: 1
1905. product_id_1: 47a83ac845f953b889154d9963dbc1f8, product_id_2: 501c6da13fd2e5d497c42b29eeddc95d, purchase_count: 1
1906. product_id_1: 47a83ac845f953b889154d9963dbc1f8, product_id_2: ceef29d2526ec891ccbd57a80997b5c8, purchase_count: 1
1907. product_id_1: 47ae44a186225b8a87ebb7bf39cc1444, product_id_2: 093f502d13b400c7acad57562017a149, purchase_count: 1
1908. product_id_1: 47afe56948e4dea1c15bf6c808da1a22, product_id_2: ee459f46c41c7314be5b18a4cad901de, purchase_count: 1
1909. product_id_1: 47b627a984bc4bde1b90fcb73fe0fd3c, product_id_2: 6a83aaaaace0f050ef46ecf0fbb32854, purchase_count: 1
1910. product_id_1: 47cad419b0ad5dc9d2305bf795c3c16f, product_id_2: ea1d9847778160f2d0c74950812fd8d0, purchase_count: 1
1911. product_id_1: 47de5f36ace720b578ca1b30d0b45b8d, product_id_2: 7605fbdad270936646b0ce6c3427b295, purchase_count: 1
1912. product_id_1: 47ea90e9a2976bc290c3cdf3b5e0573d, product_id_2: 0152f69b6cf919bcdaf117aa8c43e5a2, purchase_count: 1
1913. product_id_1: 47fafa6908e75ae62b8a36a9eb3b9234, product_id_2: 7ee8a1b1807716291e12649b1d617896, purchase_count: 1
1914. product_id_1: 480e6d74b9b908faec73816883591ee4, product_id_2: 9c46567584228684abb9695a398d0f18, purchase_count: 1
1915. product_id_1: 48109ec66664d0980876acb3f06a8521, product_id_2: 3c85232d9c97c6784684288a275f48e0, purchase_count: 1
1916. product_id_1: 481aad97c80d6786a7c6096991003274, product_id_2: a62e25e09e05e6faf31d90c6ec1aa3d1, purchase_count: 1
1917. product_id_1: 4821fcfd5ac4f89ee295f3ac1f20c7a3, product_id_2: 88703479ede641552b11881f0d2a6f6b, purchase_count: 1
1918. product_id_1: 4845d1421cd53de09a405f5f869add3c, product_id_2: f05901e010ebaa3924276751a35e6004, purchase_count: 1
1919. product_id_1: 4858799008e3cd4fcab9c61fbc63a2a0, product_id_2: f1136b963c743b647b6c0b3d86effe08, purchase_count: 1
1920. product_id_1: 48972c4d034d78bb520475d037515238, product_id_2: b7605b5b483063d12bd90a772bff9d21, purchase_count: 1
1921. product_id_1: 48972c4d034d78bb520475d037515238, product_id_2: c667317c8619402c91347027f2dadbce, purchase_count: 1
1922. product_id_1: 489b5af4a311587c81ed419dced92dba, product_id_2: 801abf9ab81269e94b64dd62fbd50fc2, purchase_count: 1
1923. product_id_1: 489b5af4a311587c81ed419dced92dba, product_id_2: 8999ae93f98ab5d5b5f5efbd4c2b8f88, purchase_count: 1
1924. product_id_1: 489f5d51b1c23a85ccfa4062d0cb021b, product_id_2: 553c5116d8f8866d39a1281071b3776f, purchase_count: 1
1925. product_id_1: 489f5d51b1c23a85ccfa4062d0cb021b, product_id_2: d22a5221a26ff421ad353360421f799a, purchase_count: 1
1926. product_id_1: 48a12f318432c4b6a1fdfd5d79372e66, product_id_2: 66e08854f9319c6aa4874ca435598331, purchase_count: 1
1927. product_id_1: 48a12f318432c4b6a1fdfd5d79372e66, product_id_2: d48e56be99464cbf285a9da17f618165, purchase_count: 1
1928. product_id_1: 48a12f318432c4b6a1fdfd5d79372e66, product_id_2: fd440fd792fd8a4b681f1eb258c25445, purchase_count: 1
1929. product_id_1: 48cd33248ca35fac04a3b751ac966810, product_id_2: 4c303e0fd131aa3fe487c108b5aa8c06, purchase_count: 1
1930. product_id_1: 48e501c433fdd2f8b2622bb9c658ffe3, product_id_2: b04aad9dbf15eae09db4376ff7590cff, purchase_count: 1
1931. product_id_1: 48ee9be392f28ae3a64518a070f4d06a, product_id_2: 29fd9022374ff3fef2e8f82c39b4133e, purchase_count: 1
1932. product_id_1: 48ee9be392f28ae3a64518a070f4d06a, product_id_2: 6cbfc716ebf92d25d1047a5fe47af5de, purchase_count: 1
1933. product_id_1: 48ee9be392f28ae3a64518a070f4d06a, product_id_2: cbdb9bf611328898bd4b32a384506b3a, purchase_count: 1
1934. product_id_1: 48ee9be392f28ae3a64518a070f4d06a, product_id_2: d75ee8bd2f182827d5a26a09ed584c9a, purchase_count: 1
1935. product_id_1: 48ee9be392f28ae3a64518a070f4d06a, product_id_2: e4c7ed7a832858c17d60ad5e38b00aba, purchase_count: 1
1936. product_id_1: 48fb8c1ee3265ce23502eaba1bd413df, product_id_2: 0ca16017057f20d572b8c01fcd7c5c28, purchase_count: 1
1937. product_id_1: 4910917f05092f331bf3a477f791cc01, product_id_2: 8d441ed10f519b5a689d263b009ebf85, purchase_count: 1
1938. product_id_1: 4910917f05092f331bf3a477f791cc01, product_id_2: 907539b8216ca1250e5e974b4047699d, purchase_count: 1
1939. product_id_1: 491c6b0ec61399a890b22a6ed2d9a4b0, product_id_2: b62a475bcfd309c66d84a1a93aa75fd8, purchase_count: 1
1940. product_id_1: 491c6b0ec61399a890b22a6ed2d9a4b0, product_id_2: d2347fba1e60ea51f533960fc555baff, purchase_count: 1
1941. product_id_1: 491c6b0ec61399a890b22a6ed2d9a4b0, product_id_2: f16e5b7883c1349e57bc5e92ba9e0d96, purchase_count: 1
1942. product_id_1: 491efdd8025d870ef06034b0bc39c3b7, product_id_2: c92af8ae65f217933c222f02ab10e73b, purchase_count: 1
1943. product_id_1: 4952dd34839fd7134ceada5de831810d, product_id_2: 6fc29f9edcdf5b8a70c15131501620e7, purchase_count: 1
1944. product_id_1: 4954affcf6b8e0fbd3b4780a9baab238, product_id_2: 9e75c1e76e60e7ddab5d73da0e216234, purchase_count: 1
1945. product_id_1: 49650e49c3af7ccc896f634d039cd921, product_id_2: 0e35a413d832e63c5d46101b7c88de0f, purchase_count: 1
1946. product_id_1: 49650e49c3af7ccc896f634d039cd921, product_id_2: 154696c4f8e96ed48f0c191eb09c0683, purchase_count: 1
1947. product_id_1: 49650e49c3af7ccc896f634d039cd921, product_id_2: 5d1d8ec5b31c5c359f10c4b23b819170, purchase_count: 1
1948. product_id_1: 49650e49c3af7ccc896f634d039cd921, product_id_2: 8ccaa3f8b171b199e37294ece30815a3, purchase_count: 1
1949. product_id_1: 49650e49c3af7ccc896f634d039cd921, product_id_2: 9474f3c0da0c4fd0bdf88cf6ac1b5d04, purchase_count: 1
1950. product_id_1: 49650e49c3af7ccc896f634d039cd921, product_id_2: daef10c972d7295283e377d5fd9985f1, purchase_count: 1
1951. product_id_1: 496f6bd86011e5a9ddea8dc96e802340, product_id_2: 75d67b030a777f5f1081b8830606abb5, purchase_count: 1
1952. product_id_1: 496f6bd86011e5a9ddea8dc96e802340, product_id_2: d4a8ab90e626911fa92af68c07228390, purchase_count: 1
1953. product_id_1: 496f6bd86011e5a9ddea8dc96e802340, product_id_2: f08c59bc335a381d2b015c4efdc6dae3, purchase_count: 1
1954. product_id_1: 496fb4187952616c8f21a127c1dd1c4e, product_id_2: 8bd9ea581812a401d20fdccc7b8abb1a, purchase_count: 1
1955. product_id_1: 497afaeae8d825d8938d01e92007f654, product_id_2: 4737840499dd8ffb4c3e54caf8a3ab9a, purchase_count: 1
1956. product_id_1: 498171cf871cdd1f5e7f8508884601b0, product_id_2: 8f8cb7e4a7f16d339f87f8aa2711a003, purchase_count: 1
1957. product_id_1: 4991aed650384274b2e7bce99caff130, product_id_2: 033ccb3016d3b24bc724629b8df41f94, purchase_count: 1
1958. product_id_1: 499bf152a2df4c2caa45d1c34342ddec, product_id_2: 6869b7e59ba6dd738b6ad254e6794b1d, purchase_count: 1
1959. product_id_1: 49adae85b53072da0eb9a88c3f0d2c7b, product_id_2: e4ad97ce352e46bebac92018f6ed976d, purchase_count: 1
1960. product_id_1: 49d05515656ae5bacab920395f834244, product_id_2: 21e72a490cbe93ed7aa675d2b1ae105a, purchase_count: 1
1961. product_id_1: 49d05515656ae5bacab920395f834244, product_id_2: 54c9eeb3eec23150e817e2048c9c4c31, purchase_count: 1
1962. product_id_1: 49d05515656ae5bacab920395f834244, product_id_2: b811b7a802d2bc88a918a9b785a6c18a, purchase_count: 1
1963. product_id_1: 49d2e2460386273b195e7e59b43587c3, product_id_2: c982dbea53b864f4d27c1d36f14b6053, purchase_count: 1
1964. product_id_1: 49d703d64ccd635b04ed7ed75d0f427b, product_id_2: 1c9c1e9c68e2311f81258433b7e0092b, purchase_count: 1
1965. product_id_1: 49d703d64ccd635b04ed7ed75d0f427b, product_id_2: 4d4321549f8f978a19a4d17588b1e770, purchase_count: 1
1966. product_id_1: 49eeae59754cbcf1abeeffb8f51184ee, product_id_2: 6421588f55f75de28cb3357e07723d14, purchase_count: 1
1967. product_id_1: 49eeb31f95c522d5db1c2d6044c23c46, product_id_2: 57552a168008a60472e3e6bb351422e7, purchase_count: 1
1968. product_id_1: 49f57e8347e394d0ddfcc1c8acaf9b2d, product_id_2: 7eb2e1637a623d3491843dff3bad4836, purchase_count: 1
1969. product_id_1: 49f906609418f32ad932aa7a24396268, product_id_2: 90b86c830114ddc888f6380a223ee285, purchase_count: 1
1970. product_id_1: 49feeab25d6531f4bbd4e9e7c926cf36, product_id_2: 5a2a2db3896d33beec6828b898812ad5, purchase_count: 1
1971. product_id_1: 4a0103d2363d388d3b209cea1773c254, product_id_2: 90ba60817ac3ba85da42f002b2eb1360, purchase_count: 1
1972. product_id_1: 4a1ccd2d546bbea7809a0cf98863eb50, product_id_2: b046862b2553fe4962392cdc93a2ae93, purchase_count: 1
1973. product_id_1: 4a266296cc64880551c3efad9739fb2e, product_id_2: 3b17f6528c9e2a01b2f75f844a60ddae, purchase_count: 1
1974. product_id_1: 4a37bc772078a013df64fd661ae5ee6c, product_id_2: caf1466f581875d1c2d9d94be70b4dbc, purchase_count: 1
1975. product_id_1: 4a534b5650f13219a0de4ce5af039d2c, product_id_2: bc055ae94989497c0d66bfa4263ccf61, purchase_count: 1
1976. product_id_1: 4a5c3967bfd3629fe07ef4d0cc8c3818, product_id_2: 0cf2faf9749f53924cea652a09d8e327, purchase_count: 1
1977. product_id_1: 4a5c3967bfd3629fe07ef4d0cc8c3818, product_id_2: 1065e0ebef073787a7bf691924c60eeb, purchase_count: 1
1978. product_id_1: 4a5c3967bfd3629fe07ef4d0cc8c3818, product_id_2: 18fa9cc25ea8b54f32d029f261673c0f, purchase_count: 1
1979. product_id_1: 4a5c3967bfd3629fe07ef4d0cc8c3818, product_id_2: 21b524c4c060169fa75ccf08c7da4627, purchase_count: 1
1980. product_id_1: 4a5c3967bfd3629fe07ef4d0cc8c3818, product_id_2: 4c8fae70c244a7ff63b9c1f73fb0a987, purchase_count: 1
1981. product_id_1: 4a5c3967bfd3629fe07ef4d0cc8c3818, product_id_2: 5dae498eff2d80057f56122235a36aff, purchase_count: 1
1982. product_id_1: 4a5c3967bfd3629fe07ef4d0cc8c3818, product_id_2: 678c229b41c0e497d35a25a8be1cc631, purchase_count: 1
1983. product_id_1: 4a5c3967bfd3629fe07ef4d0cc8c3818, product_id_2: a88124e0b1d42ca7b0813a78ff630437, purchase_count: 1
1984. product_id_1: 4a9947ec1fcec2b3321193ed5590e8cb, product_id_2: 6f0f907c9cf458139bac7f01777b9bbf, purchase_count: 1
1985. product_id_1: 4aa9d80ccc87b67668f804143617c43e, product_id_2: c5dfa757c5ae7662e178e990e39362e0, purchase_count: 1
1986. product_id_1: 4aabcc5cb08a8a919cc46a2a7a7d1bd9, product_id_2: 54b391a91c3b1a1e22af86434155834d, purchase_count: 1
1987. product_id_1: 4ac50dbde931c0a5ed8c33d3dc047351, product_id_2: b795524e6ddbae40e910d169242dbcd7, purchase_count: 1
1988. product_id_1: 4ad4cf9cb1cce9af79caf2426fd9ab93, product_id_2: 46e4940f28c9231a801873e62ca55c53, purchase_count: 1
1989. product_id_1: 4ad4cf9cb1cce9af79caf2426fd9ab93, product_id_2: e9ed063dacf96b73a9567bf943e5f708, purchase_count: 1
1990. product_id_1: 4ae634441e444ca4bc85903cafe98d73, product_id_2: ab9cf155f8280c3739b09fe341a185e8, purchase_count: 1
1991. product_id_1: 4ae634441e444ca4bc85903cafe98d73, product_id_2: ccbfd10b578c52f55cb6f510a89f1030, purchase_count: 1
1992. product_id_1: 4afba85a48ad3d91d79215ba93ddb023, product_id_2: b7c82520f8817fc72f7f5ac962035260, purchase_count: 1
1993. product_id_1: 4b15c9a92a5637d71143577edd7718b1, product_id_2: 8213da1c8eae3aa3fa5c70d87fc1581c, purchase_count: 1
1994. product_id_1: 4b15c9a92a5637d71143577edd7718b1, product_id_2: bb09cce52b336261572a5a7e25a33795, purchase_count: 1
1995. product_id_1: 4b2422ebbc6723e80f355b11b4d8fba0, product_id_2: 5d686bbd116b2de2ea1a4e1056501240, purchase_count: 1
1996. product_id_1: 4b54b3c4276e14492c3b466f49583f72, product_id_2: 81e5968d5cc613a7fb67502880db9946, purchase_count: 1
1997. product_id_1: 4b5df063d69ffafb87c279672ecb4191, product_id_2: afbe1e973aefbf72a330e3bc72d4b476, purchase_count: 1
1998. product_id_1: 4b63219873a41d0f93899f71f7a80a60, product_id_2: 9c80faf015584ca6ea94e6d59148c4a8, purchase_count: 1
1999. product_id_1: 4b6c44983d57ae2a934d661aca96d267, product_id_2: 6cc44821f36f3156c782da72dd634e47, purchase_count: 1
2000. product_id_1: 4b7460bb7ecdf2e9177bdf7bec466a4a, product_id_2: c7182d82bf8681373385017d2b516bd6, purchase_count: 1
```

#### 📊 Metadata

- **sql:** SELECT oi1.product_id AS product_id_1, oi2.product_id AS product_id_2, COUNT(*) AS purchase_count FROM analytics.order_items oi1 JOIN analytics.order_items oi2 ON oi1.order_id = oi2.order_id AND oi1.product_id <> oi2.product_id GROUP BY product_id_1, product_id_2 ORDER BY purchase_count DESC
- **row_count:** 2000
- **limit_applied:** False

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-20"></a>
### Query 20

#### 📝 Input

- **Query:** Qual é a elasticidade-preço da demanda para as principais categorias de produtos?

#### 🎯 Classification

- **Agent:** `knowledge`
- **Confidence:** 0.6
- **Reason:** conceptual question about price elasticity in product categories
- **Thread ID:** `427df7d5-68d2-464f-a8eb-2894b306a97b`

#### 💬 Response

```
A elasticidade-preço da demanda varia de acordo com a categoria de produtos. Por exemplo, o setor de Cosméticos e Perfumaria/Saúde está entre as cinco categorias com maior volume de pedidos online, o que indica uma demanda relativamente inelástica nesse segmento. Já para outros produtos, como móveis, roupas e serviços de beleza, a elasticidade-preço pode ser diferente. É importante analisar cada categoria separadamente para compreender melhor como a demanda reage às mudanças de preço.
```

#### 📚 Citations

1. `SP_guiadeecommerce_16`
2. `5777`
3. `ebook_potencialize_suas_vendas_com_a_estrategia_data_driven_compressed`
4. `como vender pela internet`
5. `5051`

#### 📄 Document Chunks

**1. SP_guiadeecommerce_16**

```
vendido, em geral, em uma frase apenas.
Vitrines virtuais – São “vitrines” como das lojas convencionais, mas dentro do e-commer-
ce ou lojas virtuais. Ganham este nome por estarem dentro da home da sua loja virtual, 
tendo um grande destaque e publicando as melhores ofertas ou suas promoções, dai o 
nome, vitrine virtual.
98
Guia de e-Commerce da APADi - 1a Edição - Março de 2013
Projeto editorial e conteúdo: 
Cláudio Coelho, CEO da Nocaute  
Presidente da APADi
Cyllas Elia, CEO da 00K e-busines...
```

**2. 5777**

```
er móveis, que é diferente de vender roupas 
que, também, é diferente de comercializar produtos e serviços de beleza e bem-estar.
Sendo assim, esta cartilha tem como objetivo apresentar de forma objetiva e direta os princi-
pais pontos que devem ser observados por quem já possui ou pretende abrir um e-commerce 
no segmento de Saúde. Como amenizar trocas e devoluções? Quais são os principais aspectos 
da legislação para a venda online de produtos voltados para a saúde? Posso fazer publicidade 
do...
```

**3. ebook_potencialize_suas_vendas_com_a_estrategia_data_driven_compressed**

```
E-commerce
POTENCIALIZE SUAS VENDAS COM 
A ESTRATÉGIA DATA DRIVEN
Com o avanço da tecnologia, o setor de dados tem ganhado 
grande destaque, e está cada vez mais em alta. Você, por acaso, já 
ouviu a frase "Data is the new oil"? A famosa frase do matemático 
inglês, Clive Humby, revela que “os dados são o novo petróleo”. 
O conceito contemporâneo mudou completamente a visão de 
empreendedores e líderes por todo o mundo na tomada de 
decisões. E em um curto período de tempo, o termo ganhou força ...
```

**4. como vender pela internet**

```
deria postar diversos looks de suas roupas;
• Facebook – plataforma em que conseguiria conversar melhor 
com suas clientes e também fazer postagem relacionadas à 
moda e às tendências.
Cinemercado - Parte 415
42
COMO VENDER PELA INTERNET?
Camila também adquiriu um número de celular para atendimento 
exclusivo à suas clientes via WhatsApp, em que agenda encontros 
para entrega de produto, envia às clientes mensagens sobre a 
chegada de novas coleções e também sobre promoções. Vale 
ressaltar que ...
```

**5. 5051**

```
ormações necessárias ao pleno exercício do 
direito de escolha do consumidor, como o tipo de contratação (compra e 
venda ou prestação de serviços), condições de pagamento escolhidas, prazo 
de entrega ou execução, vencimento de obrigações (fornecer determinado 
dado, agendar determinado serviço etc.), condições para rescisão contratual, 
entre outras informações, com destaque às cláusulas que limitem direitos.
Sumário é uma espécie de resumo do contrato de compra e venda 
ou de prestação de ser...
```


#### 📊 Metadata

- **citations_count:** 5
- **hits_considered:** 5
- **chunks_count:** 5

**[⬆️ Back to Top](#table-of-contents)**

---

