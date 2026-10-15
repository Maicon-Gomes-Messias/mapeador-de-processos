# Análise do processo: Compra de equipamento de TI

Da necessidade identificada até a nota fiscal lançada: o solicitante abre o
pedido, a Gestão de TI valida orçamento, Compras cota e recebe o material, e o
Financeiro confere a nota.


> Relatório gerado automaticamente pelo `mapeador.py` a partir da descrição do
> processo em TOML. O diagrama correspondente está no arquivo `.bpmn`.

## Indicadores

| Indicador | Valor |
| --- | --- |
| Etapas mapeadas | 9 |
| Tempo de execução (mão de obra) | 2.6 h |
| Tempo de espera | 4.3 dias |
| **Lead time total** | **4.4 dias** |
| Trocas de área (handoffs) | 5 |
| Etapas automatizáveis | 3 de 6 (50%) |
| Ganho estimado com automação | 32 min por ciclo |

## Etapas

| # | Etapa | Área | Tipo | Execução | Espera | Sistema |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Necessidade identificada | Solicitante | Início | 0 min | 0 min | - |
| 2 | Abrir solicitação de compra | Solicitante | Tarefa (automatizável) | 10 min | 0 min | Sistema de compras |
| 3 | Validar necessidade e orçamento | Gestão de TI | Tarefa | 20 min | 8.0 h | - |
| 4 | Compra aprovada? | Gestão de TI | Decisão | 0 min | 0 min | - |
| 5 | Cotar com fornecedores | Compras | Tarefa | 1.0 h | 1.0 dias | - |
| 6 | Emitir pedido e receber o material | Compras | Tarefa | 30 min | 3.0 dias | - |
| 7 | Conferir e lançar a nota fiscal | Financeiro | Tarefa (automatizável) | 25 min | 0 min | - |
| 8 | Comunicar o solicitante e encerrar | Gestão de TI | Tarefa (automatizável) | 10 min | 0 min | - |
| 9 | Compra concluída | Financeiro | Fim | 0 min | 0 min | - |

## Oportunidades de automação

- **Abrir solicitação de compra** (Solicitante) — 10 min por ciclo
- **Conferir e lançar a nota fiscal** (Financeiro) — 25 min por ciclo
- **Comunicar o solicitante e encerrar** (Gestão de TI) — 10 min por ciclo

## Gargalos (maior tempo de espera)

- **Emitir pedido e receber o material** — espera de 3.0 dias
- **Cotar com fornecedores** — espera de 1.0 dias

## Como ler estes números

- **Tempo de execução** é o trabalho efetivo; **espera** é o tempo parado em fila
  ou aguardando terceiros. O lead time é a soma dos dois — e é o que o usuário
  sente.
- **Handoff** é cada passagem do processo de uma área para outra. Quanto mais
  trocas, maior a chance de retrabalho e de perda de informação.
- **Ganho estimado** é conservador: considera 70% do tempo da etapa automatizada.
