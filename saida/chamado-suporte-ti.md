# Análise do processo: Abertura e tratamento de chamado de suporte de TI

Processo do dia a dia de uma equipe de suporte: o usuário abre o chamado, o
Service Desk faz a triagem e tenta resolver. O que não se resolve no primeiro
atendimento vai para a equipe técnica e, se depender de peça, passa pela compra.


> Relatório gerado automaticamente pelo `mapeador.py` a partir da descrição do
> processo em TOML. O diagrama correspondente está no arquivo `.bpmn`.

## Indicadores

| Indicador | Valor |
| --- | --- |
| Etapas mapeadas | 11 |
| Tempo de execução (mão de obra) | 2.9 h |
| Tempo de espera | 2.0 dias |
| **Lead time total** | **2.1 dias** |
| Trocas de área (handoffs) | 5 |
| Etapas automatizáveis | 3 de 7 (43%) |
| Ganho estimado com automação | 13 min por ciclo |

## Etapas

| # | Etapa | Área | Tipo | Execução | Espera | Sistema |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Problema identificado | Usuário | Início | 0 min | 0 min | - |
| 2 | Abrir chamado no portal | Usuário | Tarefa (automatizável) | 5 min | 0 min | Portal de chamados |
| 3 | Triar e classificar o chamado | Service Desk (N1) | Tarefa (automatizável) | 8 min | 0 min | Service Desk |
| 4 | Resolvido no primeiro atendimento? | Service Desk (N1) | Decisão | 0 min | 0 min | - |
| 5 | Resolver e registrar a solução | Service Desk (N1) | Tarefa | 15 min | 0 min | - |
| 6 | Encaminhar para a equipe técnica | Service Desk (N1) | Tarefa (automatizável) | 5 min | 0 min | - |
| 7 | Diagnosticar e corrigir | Equipe Técnica (N2) | Tarefa | 1.5 h | 0 min | - |
| 8 | Depende de peça ou fornecedor? | Equipe Técnica (N2) | Decisão | 0 min | 0 min | - |
| 9 | Comprar peça ou acionar fornecedor | Gestão de TI | Tarefa | 40 min | 2.0 dias | - |
| 10 | Encerrar o chamado e confirmar com o usuário | Service Desk (N1) | Tarefa | 10 min | 0 min | - |
| 11 | Chamado encerrado | Service Desk (N1) | Fim | 0 min | 0 min | - |

## Oportunidades de automação

- **Abrir chamado no portal** (Usuário) — 5 min por ciclo
- **Triar e classificar o chamado** (Service Desk (N1)) — 8 min por ciclo
- **Encaminhar para a equipe técnica** (Service Desk (N1)) — 5 min por ciclo

## Gargalos (maior tempo de espera)

- **Comprar peça ou acionar fornecedor** — espera de 2.0 dias

## Como ler estes números

- **Tempo de execução** é o trabalho efetivo; **espera** é o tempo parado em fila
  ou aguardando terceiros. O lead time é a soma dos dois — e é o que o usuário
  sente.
- **Handoff** é cada passagem do processo de uma área para outra. Quanto mais
  trocas, maior a chance de retrabalho e de perda de informação.
- **Ganho estimado** é conservador: considera 70% do tempo da etapa automatizada.
