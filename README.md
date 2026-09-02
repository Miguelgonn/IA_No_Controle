# Núcleo Cognitivo da Aurora Siger (NCAS)

Protótipo desenvolvido para a Atividade Integradora, responsável por registrar, organizar, consultar e interpretar informações operacionais de uma colônia espacial fictícia — a *Aurora Siger*. O sistema roda em terminal, com menu interativo, e utiliza arquivos texto e JSON como forma de armazenamento persistente.

## 1. Descrição Geral

O NCAS simula o núcleo cognitivo de controle de uma colônia espacial. Ele permite:

- Consultar e atualizar o status dos módulos da colônia;
- Registrar e visualizar alertas operacionais;
- Registrar e visualizar solicitações da tripulação;
- Registrar ocorrências técnicas de manutenção;
- Consultar um histórico de interações com um assistente simulado;
- Fazer perguntas a um assistente cognitivo simplificado, que responde com base nos dados salvos;
- Consultar logs de acesso ao sistema.

Todas as ações relevantes (registro de alertas, manutenções, solicitações, interações, atualização de status) geram automaticamente uma entrada no log de acesso, garantindo rastreabilidade das operações.

## 2. Estrutura de Arquivos do Projeto

| Arquivo | Tipo | Conteúdo |
|---|---|---|
| `modulos_colonia.json` | JSON | Status dos módulos da colônia |
| `alertas.json` | JSON | Alertas operacionais registrados |
| `solicitacoes_tripulacao.json` | JSON | Pedidos feitos pela tripulação |
| `interacoes.json` | JSON | Histórico de perguntas e respostas do assistente |
| `registros_manutencao.txt` | Texto | Log cronológico de ocorrências técnicas |
| `logs_acesso.txt` | Texto | Log cronológico de ações realizadas no sistema |

### Por que JSON e por que TXT?

- **JSON** foi usado para dados que têm **estrutura, campos fixos e precisam ser consultados/atualizados por identificador** (ex.: buscar o módulo `MOD-01` e alterar seu status, ou listar todos os alertas de prioridade alta). Isso exige dicionários com chaves nomeadas, o que o JSON representa naturalmente.
- **Texto (TXT)** foi usado para dados que são essencialmente **sequenciais e cronológicos, apenas para leitura em ordem** (manutenções e logs de acesso). Não é necessário buscar por campo específico nem atualizar um registro antigo — apenas adicionar linhas novas (modo `a`, append) e exibi-las em sequência. Um TXT simples é suficiente e mais leve para esse caso.

## 3. Manipulação de Arquivos

O sistema centraliza a manipulação de arquivos em funções genéricas, reaproveitadas por todas as funcionalidades específicas:

- `gravar_registro_texto()` — grava/sobrescreve um arquivo texto (`open(..., "w")`);
- `ler_registro_texto()` — lê todo o conteúdo de um arquivo texto (`open(..., "r")`);
- `adicionar_registro_texto()` — adiciona uma linha ao final de um arquivo (`open(..., "a")`);
- `carregar_json()` — lê um arquivo JSON e retorna um dicionário/lista Python;
- `salvar_json()` — salva um dicionário/lista Python em um arquivo JSON;
- `exibir_dados()` — imprime na tela dados de texto ou estruturas JSON formatadas.

Todas as funções usam o gerenciador de contexto `with open(...) as arquivo:`, garantindo o fechamento correto do arquivo mesmo em caso de erro.

A partir dessas funções genéricas, o sistema implementa funcionalidades específicas do projeto, como `registrar_alerta()`, `registrar_manutencao()`, `atualizar_status_modulo()`, entre outras — cada uma decidindo *o quê* gravar, enquanto a lógica de *como* gravar fica isolada nas funções genéricas.

## 4. Estrutura JSON (exemplo)

Exemplo de estrutura esperada em `alertas.json`:

```json
{
  "alertas": [
    {
      "id": "ALT-001",
      "modulo": "Suporte de Vida",
      "tipo_ocorrencia": "Consumo elevado de oxigênio",
      "prioridade": "alta",
      "data_registro": "2026-09-01",
      "mensagem": "Consumo de O2 acima do limite operacional no setor B."
    }
  ]
}
```

Estrutura equivalente é usada em `modulos_colonia.json` (lista de módulos com `id`, `nome`, `status`, `ultima_manutencao`), `solicitacoes_tripulacao.json` (pedidos com `id`, `tripulante`, `modulo_relacionado`, `tipo_solicitacao`, `descricao`, `status`, `data_solicitacao`) e `interacoes.json` (perguntas/respostas com `id`, `tripulante`, `pergunta`, `resposta`, `data_hora`).

## 5. Regra Lógica e Simplificação Booleana

**Regra de negócio:** um alerta deve ser classificado como **crítico** se a ocorrência for uma falha E (o módulo estiver com prioridade alta OU o módulo for de suporte de vida).

Forma original:

```
CRITICO = (FALHA AND PRIORIDADE_ALTA) OR (FALHA AND SUPORTE_VIDA)
```

Aplicando o **teorema da distributividade / fatoração** (equivalente ao processo inverso de De Morgan sobre um fator comum):

```
CRITICO = FALHA AND (PRIORIDADE_ALTA OR SUPORTE_VIDA)
```

**Por que a simplificação mantém o mesmo resultado?** Nos dois casos, `CRITICO` só é verdadeiro quando existe uma `FALHA` **e** pelo menos uma das duas condições agravantes (`PRIORIDADE_ALTA` ou `SUPORTE_VIDA`) é verdadeira. A forma original testa a mesma condição duas vezes (uma para cada agravante), enquanto a forma simplificada extrai o fator comum `FALHA` e testa as duas condições agravantes juntas em um único `OR`. A tabela-verdade das duas expressões é idêntica; a versão simplificada apenas reduz o número de operações lógicas necessárias, tornando a implementação mais eficiente.

> Essa regra pode ser plugada na função `registrar_alerta()` ou em uma nova função `analisar_alerta()`, marcando o alerta como crítico automaticamente antes de salvá-lo no JSON.

## 6. Prompts Estruturados (simulação de IA generativa)

O assistente é simulado pela função `gerar_resposta_simulada()`, que interpreta palavras-chave da pergunta (nome de módulo ou a palavra "alerta") e responde com base nos dados atuais salvos em JSON — sem uso de IA real, apenas lógica condicional, conforme permitido pela atividade.

**Prompt zero-shot** (sem exemplos, direto ao ponto):
```
Resuma o alerta abaixo em até 2 frases, destacando módulo, prioridade e ação recomendada:
{dados_do_alerta_em_json}
```

**Prompt few-shot** (com exemplos para guiar o formato de resposta):
```
Classifique a solicitação da tripulação em uma das categorias: URGENTE, ROTINA ou INFORMATIVA.

Exemplo 1:
Solicitação: "Vazamento de ar no módulo de cultivo"
Categoria: URGENTE

Exemplo 2:
Solicitação: "Solicito troca de filtro de água na próxima manutenção"
Categoria: ROTINA

Agora classifique:
Solicitação: "{descricao_da_solicitacao}"
Categoria:
```

**Prompt de saída estruturada (structured output)**:
```
Gere a resposta padronizada para o centro de controle usando exatamente este formato JSON,
sem texto adicional fora do JSON:

{
  "modulo": "",
  "prioridade": "",
  "resumo": "",
  "acao_recomendada": ""
}

Dados do alerta: {dados_do_alerta}
```

Esses prompts representam o que seria enviado a um modelo de linguagem real; no sistema atual, a mesma lógica é aproximada por `gerar_resposta_simulada()`.

## 7. Memória, Armazenamento e Fluxo de Dados

Mesmo trabalhando apenas com Python e arquivos locais, os dados do NCAS não ficam "soltos": ao chamar `salvar_json()` ou `adicionar_registro_texto()`, o Python monta a estrutura em **memória RAM** e a função `open()` solicita ao sistema operacional a escrita física dos bytes em **disco** (armazenamento persistente). Quando o sistema é reiniciado, `carregar_json()`/`ler_registro_texto()` fazem o caminho inverso: os bytes do disco são lidos e trazidos de volta para a memória, reconstruindo dicionários e listas que o código Python pode manipular.

Esse fluxo (memória → processamento → escrita em disco → leitura posterior → memória novamente) é o que garante que um alerta registrado hoje continue disponível mesmo depois que o programa for encerrado e executado de novo — é a diferença entre dado volátil (só na RAM, perdido ao fechar o programa) e dado persistente (gravado em armazenamento físico).

## 8. Diversidade, Ética e Responsabilidade

O assistente do NCAS trabalha com respostas pré-definidas e dados objetivos dos módulos, mas isso não elimina o risco de viés: se os dados de entrada (descrições de alertas, classificações de prioridade) forem registrados por poucas pessoas ou com vocabulário tendencioso, o sistema pode reforçar interpretações injustas ao longo do tempo. Por isso, o projeto assume que:

- Decisões automatizadas (como classificar um alerta como crítico) devem sempre poder ser revisadas por um humano responsável;
- A linguagem usada nas mensagens do sistema deve ser neutra e não discriminatória;
- Equipes diversas tendem a identificar vieses e pontos cegos que um grupo homogêneo não perceberia, o que é especialmente importante em sistemas que afetam a segurança de uma tripulação;
- A IA (real ou simulada) é uma ferramenta de apoio à decisão, e a responsabilidade final por ações críticas continua sendo humana.

## 9. Como Executar

```bash
python codigo_fonte.py
```

Não são necessárias bibliotecas externas — o projeto usa apenas módulos padrão do Python (`json`, `os`, `datetime`). Ao rodar, o menu interativo é exibido no terminal e os arquivos de dados (`.json` e `.txt`) são criados/atualizados automaticamente na mesma pasta do script conforme o uso.

## 10. Menu de Funcionalidades

```
 1  - Ver status dos módulos
 2  - Atualizar status de um módulo
 3  - Ver alertas operacionais
 4  - Registrar novo alerta
 5  - Ver solicitações da tripulação
 6  - Registrar nova solicitação
 7  - Ver histórico de interações
 8  - Fazer uma pergunta ao assistente
 9  - Ver registros de manutenção
10  - Registrar nova manutenção
11  - Ver logs de acesso
 0  - Sair
```
