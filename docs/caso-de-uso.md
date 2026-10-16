# Caso de uso: analisando o processo de chamados de suporte

Este documento mostra o mapeador sendo usado do começo ao fim em um processo real, com
uma leitura de **AS-IS** (como é hoje), propostas de **TO-BE** (como deveria ser) e os
indicadores para acompanhar se a mudança pegou.

O processo usado é o do exemplo do repositório
([`processos/chamado-suporte-ti.toml`](../processos/chamado-suporte-ti.toml)), mas o
raciocínio vale para qualquer processo que passe por mais de uma área.

---

## 1. O desenho do processo hoje (AS-IS)

O processo tem quatro áreas: **Usuário**, **Service Desk (N1)**, **Equipe Técnica (N2)**
e **Gestão de TI**.

```
Usuário abre o chamado
   ↓
N1 faz a triagem e tenta resolver
   ├── resolveu?  ── Sim ──▶ registra a solução
   └── não ──▶ encaminha para o N2
                  ↓
            N2 diagnostica e corrige
               ├── depende de peça? ── Sim ──▶ Gestão de TI compra
               └── não
                  ↓
            N1 encerra e confirma com o usuário
```

## 2. O que os números dizem

Gerando a análise com `python mapeador.py processos/chamado-suporte-ti.toml`:

| Indicador | Valor |
| --- | --- |
| Tempo de execução (trabalho efetivo) | 2,9 h |
| Tempo de espera | **2,0 dias** |
| Lead time total | 2,1 dias |
| Trocas de área (handoffs) | 5 |
| Etapas automatizáveis | 3 de 7 (43%) |

**A leitura principal:** o chamado leva **2,1 dias** para ser resolvido, mas só **2,9
horas** disso é trabalho de alguém. Ou seja, **mais de 95% do tempo o chamado está
parado** — em fila ou esperando terceiros.

Isso muda a conversa. Se o problema fosse "a equipe é lenta", a solução seria contratar
ou cobrar produtividade. Como o problema é espera, a solução é atacar a espera.

### Onde a espera está

| Etapa | Onde trava | Espera |
| --- | --- | --- |
| Comprar peça ou acionar fornecedor | Processo de compra e prazo do fornecedor | 2,0 dias |

Praticamente **toda a espera do processo está em um único ponto**: quando o
conserto depende de uma peça que não está em estoque.

### Os 5 handoffs

O processo troca de mão cinco vezes. Cada troca é uma chance de a informação se perder:
o novo responsável precisa reler o chamado, entender o que já foi testado e, às vezes,
refazer o diagnóstico.

## 3. O que dá para melhorar (TO-BE)

As propostas estão em ordem de impacto, com a estimativa de quanto cada uma vale. São
estimativas a validar com dados reais — a ferramenta serve justamente para isso: você
muda o `.toml` e vê o efeito nos números.

### 3.1. Estoque mínimo das peças mais trocadas — o maior ganho

Hoje o chamado para por **2 dias** esperando a compra. Se a instituição mantiver em
estoque os itens de maior giro (memória, fonte, SSD, teclado), boa parte desses chamados
deixa de parar.

Com estoque, a etapa de compra sai do caminho comum e sobra o tempo de troca da peça.
Estimativa: **lead time cai de 2,1 dias para cerca de 6 horas**, sem contratar ninguém.

### 3.2. Triagem automática

A classificação do chamado por categoria e palavra-chave pode ser feita pelo próprio
sistema, com o N1 revisando o que vier com baixa confiança. Isso tira 8 minutos por
chamado e — mais importante — reduz o encaminhamento errado, que gera handoff extra.

### 3.3. Roteamento automático

Se o chamado já chega classificado, o encaminhamento para o N2 é uma regra, não uma
tarefa. Some 5 minutos por chamado e **elimina uma troca de área**.

### 3.4. Base de soluções conhecidas

Uma boa parte dos chamados se repete. Um catálogo de soluções, consultável pelo próprio
usuário antes de abrir o chamado, aumenta a resolução no primeiro atendimento — e cada
chamado que morre no N1 não passa pelo N2 nem pela compra.

### 3.5. Acompanhamento do pedido de compra

Enquanto o estoque não resolve tudo, vale ter alerta de prazo no pedido. Não diminui a
espera por si só, mas evita o chamado esquecido, que é espera que ninguém percebe.

### Efeito combinado (estimativa)

| | AS-IS | TO-BE estimado |
| --- | --- | --- |
| Lead time | 2,1 dias | ~6 h |
| Trocas de área | 5 | 3 |
| Etapas automatizáveis executadas por sistema | 0 | 3 |

## 4. Como saber se funcionou

Melhoria sem indicador vira opinião. Estes são os números para acompanhar:

| Indicador | O que revela | Meta inicial |
| --- | --- | --- |
| **Lead time médio** | O tempo que o usuário sente | reduzir 50% |
| **% resolvido no N1** | Se a base de soluções está sendo usada | aumentar |
| **Tempo de espera médio** | Se o gargalo saiu da compra | cair para menos de 4 h |
| **Trocas de área por chamado** | Se o roteamento automático pegou | 5 → 3 |
| **% de chamados reabertos** | Se a pressa está gerando retrabalho | não subir |

O ideal é medir **antes** de mudar, para ter a linha de base. Um mês de coleta já dá um
panorama.

## 5. Sobre conduzir a mudança

Algumas coisas que aprendi observando processos de perto:

- **Quem executa precisa participar do desenho.** As regras de roteamento automático
  que funcionam são as que o próprio N1 ajudou a escrever.
- **Comece por uma categoria só.** Rodar a mudança inteira de uma vez torna impossível
  saber o que funcionou.
- **O número é para decidir, não para vigiar.** Se o indicador vira cobrança individual,
  as pessoas passam a trabalhar para o indicador, não para o processo.
- **Documente o antes.** Sem o AS-IS registrado, ninguém consegue provar depois que
  melhorou — e a mudança perde força na próxima gestão.

---

## Como reproduzir esta análise

```bash
# gera o diagrama, o relatório e o painel do exemplo
python mapeador.py processos/chamado-suporte-ti.toml

# agora edite o .toml com os números da sua realidade e gere de novo
python mapeador.py processos/chamado-suporte-ti.toml
```

O diagrama (`.bpmn`) abre em <https://bpmn.io/>, o relatório (`.md`) é texto e o painel
(`.html`) abre no navegador com dois cliques.
