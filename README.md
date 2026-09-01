# 🧠 NCAS — Núcleo Cognitivo da Aurora Siger

## 📌 Sobre o projeto

O **NCAS (Núcleo Cognitivo da Aurora Siger)** é um protótipo desenvolvido em Python para auxiliar no gerenciamento e na interpretação de informações operacionais de uma colônia espacial.

O sistema permite **registrar, armazenar, consultar e analisar informações**, utilizando arquivos de texto, arquivos JSON, regras de lógica booleana e prompts estruturados para simular uma interação com um assistente inteligente.

O projeto foi desenvolvido como parte da atividade integradora da **Aurora Siger**.

---

## 🎯 Objetivos

O projeto tem como principais objetivos:

* Registrar informações operacionais da colônia;
* Armazenar dados utilizando arquivos `.txt` e `.json`;
* Consultar informações previamente armazenadas;
* Utilizar regras de lógica booleana para tomada de decisão;
* Aplicar simplificação de expressões lógicas;
* Criar prompts utilizando técnicas de engenharia de prompts;
* Simular respostas de um assistente inteligente;
* Demonstrar conceitos de memória, armazenamento e fluxo de dados;
* Refletir sobre ética, diversidade e responsabilidade no uso de IA.

---

## ⚙️ Funcionalidades

O sistema possui um menu interativo no terminal com as seguintes opções:

### 1. Cadastrar alerta operacional

Permite registrar um novo alerta informando:

* Módulo afetado;
* Tipo de ocorrência;
* Prioridade;
* Descrição do problema.

Os dados são armazenados no arquivo `dados_colonia.json` e também registrados no arquivo `registros_colonia.txt`.

### 2. Consultar alertas

Exibe os alertas previamente registrados no sistema, recuperando as informações armazenadas no arquivo JSON.

### 3. Cadastrar solicitação da tripulação

Permite registrar solicitações realizadas pela tripulação, contendo:

* Setor;
* Pedido;
* Nível de urgência;
* Data do registro.

### 4. Validação lógica

O sistema analisa um alerta utilizando uma regra booleana.

A regra utilizada é:

```text
ALERTA = (FALHA AND CRITICO) OR (FALHA AND NOT CRITICO)
```

Após a simplificação:

```text
ALERTA = FALHA
```

Dessa forma, o sistema consegue verificar se uma falha deve gerar um alerta operacional.

### 5. Prompts estruturados

O sistema apresenta exemplos de:

* Zero-shot Prompting;
* Few-shot Prompting;
* Saída estruturada em JSON.

### 6. Simulação de IA

O projeto simula o funcionamento de um assistente inteligente utilizando regras e respostas predefinidas.

Não é necessária uma API externa de inteligência artificial para executar o projeto.

---

## 🗂️ Estrutura dos arquivos

```text
NCAS_Aurora_Siger/
│
├── codigo_fonte.py
├── dados_colonia.json
├── registros_colonia.txt
├── regras_logicas.txt
├── prompts_utilizados.txt
├── etica_diversidade.txt
├── memoria_armazenamento.txt
├── otimizacao.txt
├── roteiro_video.txt
└── link_video.txt
```

Na entrega final, os arquivos obrigatórios seguem a estrutura solicitada pela atividade:

```text
codigo_fonte.py
dados_colonia.json
registros_colonia.txt
regras_logicas.pdf
prompts_utilizados.pdf
link_video.txt
```

---

## 💾 Armazenamento de dados

O projeto utiliza dois formatos principais de armazenamento.

### JSON

O arquivo `dados_colonia.json` é utilizado para armazenar informações estruturadas, como:

* Módulos da colônia;
* Alertas;
* Solicitações da tripulação.

Exemplo:

```json
{
    "modulos": [
        {
            "nome": "Energia",
            "status": "ativo"
        }
    ],
    "alertas": [
        {
            "id": 1,
            "modulo": "Energia",
            "tipo": "falha",
            "prioridade": "critica"
        }
    ]
}
```

### TXT

O arquivo `registros_colonia.txt` funciona como um registro de eventos do sistema, armazenando informações como alertas, solicitações e respostas simuladas.

---

## 🧠 Lógica Booleana

A regra utilizada pelo NCAS é:

```text
ALERTA = (FALHA AND CRITICO) OR (FALHA AND NOT CRITICO)
```

Aplicando a propriedade distributiva:

```text
ALERTA = FALHA AND (CRITICO OR NOT CRITICO)
```

Como:

```text
CRITICO OR NOT CRITICO = VERDADEIRO
```

Temos:

```text
ALERTA = FALHA AND VERDADEIRO
```

Portanto:

```text
ALERTA = FALHA
```

A simplificação mantém o mesmo resultado lógico da expressão original, mas torna a regra mais simples e fácil de implementar.

---

## 🤖 Engenharia de Prompts

O projeto utiliza diferentes técnicas de engenharia de prompts.

### Zero-shot

O sistema fornece uma instrução sem apresentar exemplos anteriores.

Exemplo:

```text
Analise o alerta operacional abaixo e produza uma resposta objetiva
para o centro de controle. Identifique o problema, a prioridade e
a ação recomendada.
```

### Few-shot

O sistema apresenta exemplos de entradas e respostas antes de solicitar uma nova análise.

Exemplo:

```text
Entrada:
Falha no sistema de oxigênio. Prioridade: crítica.

Saída:
Risco crítico. Isolar o módulo e acionar a equipe de manutenção.

Agora analise:
Falha no módulo de energia. Prioridade: alta.
```

### Saída estruturada

A resposta pode ser organizada em JSON:

```json
{
    "problema": "Falha no módulo de energia",
    "prioridade": "alta",
    "acao_recomendada": "Verificar o módulo e acionar manutenção",
    "status": "atenção"
}
```

---

## 🧮 Otimização

Uma das melhorias implementadas no projeto é a simplificação da regra lógica.

A expressão:

```text
(FALHA AND CRITICO) OR (FALHA AND NOT CRITICO)
```

pode ser reduzida para:

```text
FALHA
```

Isso diminui a quantidade de operações necessárias e facilita a compreensão e manutenção do código.

Também é utilizada uma estrutura organizada de saída para facilitar a interpretação das respostas simuladas.

---

## 💾 Memória e armazenamento

O fluxo de dados do sistema pode ser representado da seguinte forma:

```text
Entrada do usuário
       ↓
     Python
       ↓
     Memória
       ↓
Escrita no arquivo
       ↓
  Armazenamento
       ↓
Leitura dos dados
       ↓
Processamento
       ↓
Saída no terminal
```

Os arquivos permitem que as informações continuem disponíveis mesmo depois que o programa é encerrado.

---

## ⚖️ Ética e responsabilidade

O NCAS também considera aspectos relacionados ao uso responsável da inteligência artificial.

Sistemas inteligentes podem apresentar respostas enviesadas ou utilizar linguagem inadequada. Por isso, é importante considerar:

* Diversidade durante o desenvolvimento;
* Prevenção de linguagem discriminatória;
* Possíveis vieses nas respostas;
* Impactos de decisões automatizadas;
* Responsabilidade humana.

No contexto do NCAS, a inteligência artificial simulada funciona como uma ferramenta de apoio. A decisão final em situações críticas continua sendo responsabilidade dos operadores da colônia.

---

## ▶️ Como executar

### Requisitos

* Python 3.x
* Nenhuma biblioteca externa é necessária.

### Execução

Abra o terminal na pasta do projeto e execute:

```bash
python codigo_fonte.py
```

O sistema apresentará um menu semelhante a:

```text
====================================
   NCAS - AURORA SIGER
====================================

1 - Cadastrar alerta operacional
2 - Consultar alertas
3 - Cadastrar solicitação da tripulação
4 - Validar alerta com regra lógica
5 - Exibir prompts estruturados
6 - Simular resposta do assistente
0 - Sair
```

Escolha uma opção digitando o número correspondente.

---

## 🎥 Apresentação

A apresentação do projeto deve demonstrar o funcionamento do sistema, incluindo:

1. Apresentação do NCAS;
2. Dados armazenados;
3. Leitura e gravação de arquivos;
4. Funcionamento do JSON;
5. Regra lógica e simplificação;
6. Prompts;
7. Simulação do assistente inteligente;
8. Otimização;
9. Ética e responsabilidade;
10. Execução prática do sistema.

O vídeo deve possuir no máximo **5 minutos** e ser publicado no YouTube como **"Não listado"**.

O link da apresentação deve ser colocado no arquivo:

```text
link_video.txt
```

---

## 👥 Equipe

**Aurora Siger — NCAS**

Projeto desenvolvido para a atividade integradora.

---

## 📚 Tecnologias utilizadas

* Python
* JSON
* Arquivos TXT
* Lógica Booleana
* Engenharia de Prompts
* Simulação de IA Generativa

---

## 🚀 Conclusão

O NCAS demonstra como conceitos de programação, armazenamento de dados, lógica booleana e engenharia de prompts podem ser integrados em um único sistema.

O projeto permite que informações da colônia sejam registradas e recuperadas, além de utilizar regras lógicas e uma simulação de assistente inteligente para apoiar a interpretação de situações operacionais.
