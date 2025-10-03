# Mapa de Scripts Elisp na Pasta src

Este documento mapeia as conexões entre os scripts Emacs Lisp localizados na pasta `src`. A estrutura é apresentada como um grafo, o«nde cada nó representa um script e cada aresta representa uma conexão ou dependência entre eles.

## Grafo

```
mermaid
graph TD
    A[init.el] --> B(pen.el)
    A --> C(pen-core.el)
    B --> D(pen-alethea-ai.el)
    B --> E(pen-chatgpt.el)
    C --> D
    C --> E
    D --> F(pen-lm-client.el)
    E --> F
    F --> G(pen-handle.el)
    A --> H(init-setup.el)
    H --> A
```
## Explicação dos Nós e Arestas

### Nós (Scripts Elisp)

*   **`init.el`**: Este é provavelmente o ponto de entrada principal para a configuração e inicialização do ambiente. Ele carrega e configura outros scripts e pacotes.
*   **`pen.el`**: Pode ser o script principal que define a funcionalidade central do projeto "pen". É provável que dependa de `pen-core.el` e interaja com módulos específicos.
*   **`pen-core.el`**: Contém funcionalidades essenciais e definições básicas utilizadas por outros scripts no projeto. Serve como uma base para o restante do código.
*   **`pen-alethea-ai.el`**: Script relacionado à integração ou uso de um modelo de IA específico chamado "Alethea AI". Provavelmente contém funções para interagir com a API ou processar respostas deste modelo.
*   **`pen-chatgpt.el`**: Similar a `pen-alethea-ai.el`, este script lida com a integração com o modelo de linguagem ChatGPT. Contém funções para enviar prompts e receber respostas.
*   **`pen-lm-client.el`**: Um cliente genérico para interagir com modelos de linguagem (LMs). Pode ser utilizado por `pen-alethea-ai.el` e `pen-chatgpt.el` para abstrair a comunicação com diferentes LMs.
*   **`pen-handle.el`**: Este script provavelmente contém funções para manipular ou processar as respostas recebidas dos modelos de linguagem ou outras entradas. Pode atuar como um intermediário entre os clientes de LM e outras partes do sistema.
*   **`init-setup.el`**: Script focado em tarefas de configuração inicial que podem ser separadas de `init.el` para modularidade. Pode definir variáveis, carregar pacotes essenciais ou configurar o ambiente.

### Arestas (Conexões/Dependências)

*   **`init.el` --> `pen.el`**: `init.el` provavelmente carrega e inicializa a funcionalidade principal definida em `pen.el`.
*   **`init.el` --> `pen-core.el`**: `init.el` provavelmente carrega as funcionalidades essenciais de `pen-core.el` no início da sessão.
*   **`pen.el` --> `pen-alethea-ai.el`**: A funcionalidade principal (`pen.el`) pode chamar funções de `pen-alethea-ai.el` para interagir com o modelo Alethea AI.
*   **`pen.el` --> `pen-chatgpt.el`**: A funcionalidade principal (`pen.el`) pode chamar funções de `pen-chatgpt.el` para interagir com o modelo ChatGPT.
*   **`pen-core.el` --> `pen-alethea-ai.el`**: `pen-core.el` pode fornecer funções ou estruturas de dados utilizadas por `pen-alethea-ai.el`.
*   **`pen-core.el` --> `pen-chatgpt.el`**: `pen-core.el` pode fornecer funções ou estruturas de dados utilizadas por `pen-chatgpt.el`.
*   **`pen-alethea-ai.el` --> `pen-lm-client.el`**: `pen-alethea-ai.el` provavelmente utiliza as funções genéricas de comunicação com LMs definidas em `pen-lm-client.el`.
*   **`pen-chatgpt.el` --> `pen-lm-client.el`**: `pen-chatgpt.el` provavelmente utiliza as funções genéricas de comunicação com LMs definidas em `pen-lm-client.el`.
*   **`pen-lm-client.el` --> `pen-handle.el`**: O cliente de LM pode passar as respostas recebidas para `pen-handle.el` para processamento adicional.
*   **`init.el` --> `init-setup.el`**: `init.el` pode carregar ou executar o script `init-setup.el` para realizar configurações iniciais.
*   **`init-setup.el` --> `init.el`**: Menos comum, mas `init-setup.el` pode, em alguns casos, chamar funções ou variáveis definidas em `init.el` após a configuração inicial.

Este é apenas um ponto de partida baseado nos nomes dos arquivos. Para um mapa mais preciso e completo, seria necessário analisar o código de cada script para identificar as chamadas de função explícitas e as dependências indiretas.