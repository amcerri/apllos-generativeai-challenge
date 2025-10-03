# Batch Query Results

## Summary

- **Generated:** 2025-10-03 16:45:36
- **Total Queries:** 8
- **Successful:** 7
- **Failed:** 1

<a id="table-of-contents"></a>
## 📋 Table of Contents

1. [Analise este documento comercial](#query-1) - `commerce`
2. [Processe este pedido de compra](#query-2) - `commerce`
3. [Extraia as informações deste pedido](#query-3) - `commerce`
4. [Analise este documento internacional](#query-4) - `Unknown`
5. [Processe esta ordem de construção](#query-5) - `commerce`
6. [Analise este pedido médico](#query-6) - `commerce`
7. [Processe este pedido de catering](#query-7) - `commerce`
8. [Analise este documento incompleto](#query-8) - `commerce`

---

## Results

<a id="query-1"></a>
### Query 1

#### 📝 Input

- **Query:** Analise este documento comercial
- **Attachment:** `data/samples/orders/Simple Order.txt`

#### 🎯 Classification

- **Agent:** `commerce`
- **Confidence:** 0.95
- **Reason:** analyze commercial order document with items and prices; commerce guard
- **Thread ID:** `d9584057-4e7e-4eaa-9ac2-568e24b7d08d`

#### 💬 Response

```
INFORMAÇÕES DO DOCUMENTO
==================================================
Tipo: Order Form
ID: #12345
Moeda: BRL

DATAS
------------------------------
Emissão: 2025-01-15

VALORES TOTAIS
------------------------------
Subtotal: R$ 2.800,00
Frete: R$ 25,00
TOTAL GERAL: R$ 2.825,00

ITENS PRINCIPAIS
------------------------------
1. Notebook Dell Inspiron 15
   Quantidade: 1,00
   Preço unitário: R$ 2.500,00
   Total da linha: R$ 2.500,00

2. Teclado mecânico
   Quantidade: 1,00
   Preço unitário: R$ 200,00
   Total da linha: R$ 200,00

3. Mouse sem fio
   Quantidade: 2,00
   Preço unitário: R$ 50,00
   Total da linha: R$ 100,00

INTERAÇÃO
------------------------------
Gostaria de alguma análise específica sobre este pedido?
Posso ajudar com comparações, simulações ou análises detalhadas.
```

#### 📊 Metadata

- **doc_type:** order_form
- **doc_id:** #12345
- **currency:** BRL
- **item_count:** 3
- **grand_total:** 2825.0
- **risks_count:** 0

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-2"></a>
### Query 2

#### 📝 Input

- **Query:** Processe este pedido de compra
- **Attachment:** `data/samples/orders/Complex Order.docx`

#### 🎯 Classification

- **Agent:** `commerce`
- **Confidence:** 0.9
- **Reason:** process purchase order with attachment; commerce guard
- **Thread ID:** `aa212ca7-8e98-41c3-9e28-abbd1ebd7693`

#### 💬 Response

```
❌ Erro ao processar documento.
```

#### 📊 Metadata

- **error:** no_document

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-3"></a>
### Query 3

#### 📝 Input

- **Query:** Extraia as informações deste pedido
- **Attachment:** `data/samples/orders/Messy Order.txt`

#### 🎯 Classification

- **Agent:** `commerce`
- **Confidence:** 0.95
- **Reason:** extract order details from attached messy order text; commerce guard
- **Thread ID:** `06fadbf1-cbbf-4d3e-b58d-84d22780ca1d`

#### 💬 Response

```
INFORMAÇÕES DO DOCUMENTO
==================================================
Tipo: Order Form
ID: PO-URG-001
Moeda: BRL

VALORES TOTAIS
------------------------------
Subtotal: R$ 4.555,00
Frete: R$ 35,00
TOTAL GERAL: R$ 4.590,00

ITENS PRINCIPAIS
------------------------------
1. Laptop HP Pavilion 15
   Quantidade: 1,00
   Preço unitário: R$ 3.200,00
   Total da linha: R$ 3.200,00

2. Monitor 24"
   Quantidade: 1,00
   Preço unitário: R$ 800,00
   Total da linha: R$ 800,00

3. Teclado USB
   Quantidade: 2,00
   Preço unitário: R$ 120,00
   Total da linha: R$ 240,00

4. Webcam HD
   Quantidade: 1,00
   Preço unitário: R$ 180,00
   Total da linha: R$ 180,00

5. Mouse Logitech
   Quantidade: 3,00
   Preço unitário: R$ 45,00
   Total da linha: R$ 135,00

INTERAÇÃO
------------------------------
Gostaria de alguma análise específica sobre este pedido?
Posso ajudar com comparações, simulações ou análises detalhadas.
```

#### 📊 Metadata

- **doc_type:** order_form
- **doc_id:** PO-URG-001
- **currency:** BRL
- **item_count:** 5
- **grand_total:** 4590.0
- **risks_count:** 0

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-4"></a>
### Query 4

#### 📝 Input

- **Query:** Analise este documento internacional
- **Attachment:** `data/samples/orders/International Order.txt`

#### ❌ Error

```
Timeout waiting for response
```

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-5"></a>
### Query 5

#### 📝 Input

- **Query:** Processe esta ordem de construção
- **Attachment:** `data/samples/orders/Construction Order.txt`

#### 🎯 Classification

- **Agent:** `commerce`
- **Confidence:** 0.95
- **Reason:** process construction order with attached document; commerce guard
- **Thread ID:** `5d505a22-64d0-478e-98da-20acaa52a401`

#### 💬 Response

```
INFORMAÇÕES DO DOCUMENTO
==================================================
Tipo: Order Form
ID: (sem ID)
Moeda: BRL

VALORES TOTAIS
------------------------------
Subtotal: R$ 112.000,00
Frete: R$ 2.500,00
TOTAL GERAL: R$ 171.472,00

ITENS PRINCIPAIS
------------------------------
1. Fundação e Estrutura
   Quantidade: ?
   Preço unitário: (não informado)
   Total da linha: R$ 45.000,00

2. Alvenaria e Revestimentos
   Quantidade: ?
   Preço unitário: (não informado)
   Total da linha: R$ 28.500,00

3. Pisos e Acabamentos
   Quantidade: ?
   Preço unitário: (não informado)
   Total da linha: R$ 18.000,00

4. Instalações Elétricas
   Quantidade: ?
   Preço unitário: (não informado)
   Total da linha: R$ 12.000,00

5. Instalações Hidráulicas
   Quantidade: ?
   Preço unitário: (não informado)
   Total da linha: R$ 8.500,00

INTERAÇÃO
------------------------------
Gostaria de alguma análise específica sobre este pedido?
Posso ajudar com comparações, simulações ou análises detalhadas.
```

#### 📊 Metadata

- **doc_type:** order_form
- **doc_id:** None
- **currency:** BRL
- **item_count:** 5
- **grand_total:** 171472.0
- **risks_count:** 0

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-6"></a>
### Query 6

#### 📝 Input

- **Query:** Analise este pedido médico
- **Attachment:** `data/samples/orders/Medical Order.txt`

#### 🎯 Classification

- **Agent:** `commerce`
- **Confidence:** 0.95
- **Reason:** analyze medical order with attachment; commerce guard
- **Thread ID:** `8357e370-c48e-4d02-8aed-9c8e5a9f2bda`

#### 💬 Response

```
INFORMAÇÕES DO DOCUMENTO
==================================================
Tipo: Order Form
ID: (sem ID)
Moeda: BRL

VALORES TOTAIS
------------------------------
Subtotal: R$ 526.500,00
Frete: R$ 10.000,00
TOTAL GERAL: R$ 738.150,00

ITENS PRINCIPAIS
------------------------------
1. VENTILADOR MECANICO
   Quantidade: 2,00
   Preço unitário: R$ 120.000,00
   Total da linha: R$ 240.000,00

2. MONITOR CARDIACO MULTIPARAMETRICO
   Quantidade: 3,00
   Preço unitário: R$ 45.000,00
   Total da linha: R$ 135.000,00

3. ELETROCARDIOGRAFO
   Quantidade: 2,00
   Preço unitário: R$ 25.000,00
   Total da linha: R$ 50.000,00

4. DESFIBRILADOR AUTOMATICO
   Quantidade: 5,00
   Preço unitário: R$ 8.500,00
   Total da linha: R$ 42.500,00

5. BOMBA DE INFUSAO
   Quantidade: 10,00
   Preço unitário: R$ 3.200,00
   Total da linha: R$ 32.000,00

... e mais 9 itens

RISCOS E ALERTAS
------------------------------
- sum_mismatch: A soma dos itens não confere com o subtotal declarado

INTERAÇÃO
------------------------------
Gostaria de alguma análise específica sobre este pedido?
Posso ajudar com comparações, simulações ou análises detalhadas.
```

#### 📊 Metadata

- **doc_type:** order_form
- **doc_id:** None
- **currency:** BRL
- **item_count:** 14
- **grand_total:** 738150.0
- **risks_count:** 1

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-7"></a>
### Query 7

#### 📝 Input

- **Query:** Processe este pedido de catering
- **Attachment:** `data/samples/orders/Restaurant Order.docx`

#### 🎯 Classification

- **Agent:** `commerce`
- **Confidence:** 0.9
- **Reason:** process catering order with attachment; commerce guard
- **Thread ID:** `4960f690-d931-45ee-9d04-72335341f09a`

#### 💬 Response

```
❌ Erro ao processar documento.
```

#### 📊 Metadata

- **error:** no_document

**[⬆️ Back to Top](#table-of-contents)**

---

<a id="query-8"></a>
### Query 8

#### 📝 Input

- **Query:** Analise este documento incompleto
- **Attachment:** `data/samples/orders/Incomplete Order.txt`

#### 🎯 Classification

- **Agent:** `commerce`
- **Confidence:** 0.9
- **Reason:** analyze incomplete order document with item details; commerce guard
- **Thread ID:** `3c51a890-382c-4c91-ba53-1b97817c7769`

#### 💬 Response

```
INFORMAÇÕES DO DOCUMENTO
==================================================
Tipo: Order Form
ID: (sem ID)
Moeda: (não informada)

VALORES TOTAIS
------------------------------
Subtotal: (não informado)
Frete: (não informado)
TOTAL GERAL: (não informado)

ITENS PRINCIPAIS
------------------------------
1. Notebook
   Quantidade: 1,00
   Preço unitário: (não informado)
   Total da linha: (não informado)

2. Mouse
   Quantidade: 2,00
   Preço unitário: (não informado)
   Total da linha: (não informado)

3. Teclado
   Quantidade: 1,00
   Preço unitário: (não informado)
   Total da linha: (não informado)

RISCOS E ALERTAS
------------------------------
- missing_core_fields: Campos essenciais como ID, data ou valores estão ausentes
- incomplete_lines: Alguns itens não possuem informações completas

INTERAÇÃO
------------------------------
Este documento apresenta algumas inconsistências nos valores.
Posso ajudar a investigar ou analisar os dados disponíveis.
```

#### 📊 Metadata

- **doc_type:** order_form
- **doc_id:** None
- **currency:** None
- **item_count:** 3
- **grand_total:** None
- **risks_count:** 2

**[⬆️ Back to Top](#table-of-contents)**

---

