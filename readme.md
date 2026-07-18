# Sistema de Gestão - Desafio na Cozinha (Chef Jacquin)

**Disciplina:** Algoritmos e Estruturas de Dados II  
**Instituição:** Universidade Federal de Pelotas (UFPel)  
**Desenvolvedores:** Henrique Weege Voigt e Samuel Bottermund Flores  
**Turma:** M2  
**Repositório do Projeto:** [https://github.com/henriquevoigt/Desafio-Na-Cozinha](https://github.com/henriquevoigt/Desafio-Na-Cozinha)

---

## Sobre o Projeto

Este projeto implementa um sistema inteligente de gerenciamento de receitas para mitigar problemas de desorganização, sabotagem culinária e gargalos logísticos em uma cozinha profissional e seu respectivo sistema de delivery. O sistema atende e supera todos os requisitos propostos nos Trabalhos 1 e 2, utilizando estruturas de dados desenvolvidas do zero para garantir buscas de alto desempenho, validação de integridade criptográfica, otimização de tempo de preparo, persistência avançada de dados em memória secundária, resolução de dependências de produção, e roteamento logístico em malhas viárias.

---

## Fonte de Dados

A fonte de dados escolhida para popular o sistema culinário foi a API pública DummyJSON. Para garantir estabilidade e evitar problemas de rede durante a avaliação (conforme recomendado nas instruções), o sistema faz o download estático de 50 receitas no primeiro carregamento e as salva no diretório local `data/receitas.json`. As receitas contêm informações padronizadas como ID, nome, ingredientes, categoria, custo, valor de venda, e dependências de preparo.

Para o módulo logístico, foi modelada uma rede viária baseada nos bairros da cidade de Pelotas, armazenada em `data/mapa.json`. O grafo computacional contém exatamente **30 vértices** (bairros/pontos de interesse) e **51 arestas** (conexões com pesos baseados no tempo de trânsito), cumprindo rigorosamente os requisitos de dimensionalidade da disciplina.

---

## Instruções de Execução

1. **Pré-requisitos:** Certifique-se de ter o Python 3.x instalado em sua máquina. Nenhuma biblioteca externa é necessária, o projeto utiliza apenas pacotes nativos da linguagem.
2. **Executando o sistema:** Navegue até a raiz do projeto no terminal e execute o arquivo principal rodando o comando: `python main.py`
3. **Interação (Dual Boot):** O sistema iniciará com um Gerenciador de Boot.
    * Escolha a **Opção 1** para carregar o sistema completo na memória RAM (Tries, Hash, PD, Grafos).
    * Escolha a **Opção 2** para testar o modo de recuperação (Árvore B com leitura direta no disco físico, sem carregar o JSON).
4. O sistema criará automaticamente as pastas `data/` e `data/btree_nodos/` (para a persistência da Árvore B) na primeira execução.

---

## Estruturas de Dados e Algoritmos Implementados

O projeto implementa do zero **todas as 4 estruturas base sugeridas no T1**, além das **modelagens de redes e otimizações algorítmicas exigidas no T2**.

### 1. Árvore Trie (Módulo 2 - Consulta Rápida)
* **Onde foi aplicada:** No "Modo Consulta Rápida" para buscas por Nome, ID e Categoria.
* **Justificativa Técnica:** Em vez de varrer arrays inteiros para buscar prefixos textuais (o que custaria O(N × M)), a Trie permite a recuperação instantânea das informações em tempo O(L), onde L é o comprimento da palavra digitada. A arquitetura foi desenhada instanciando três Tries independentes na memória para evitar conflitos de tipos de dados.

### 2. Tabela Hash Manual (Módulo 3 e Investigação)
* **Onde foi aplicada:** Na indexação de ingredientes e no "Modo Investigação" para detectar sabotagens culinárias.
* **Justificativa Técnica:** A classe `HashTable` foi construída do zero, utilizando função Hash Polinomial (multiplicação por fator primo 31) para minimizar colisões, e encadeamento (Chaining) com listas dinâmicas. O redimensionamento (Resize) ocorre dinamicamente quando o fator de carga atinge 1.0. A validação gera a assinatura concatenando dados vitais; qualquer alteração muda a assinatura, alertando o sistema.

### 3. Algoritmo Guloso (Módulo 5 - Modo Chef)
* **Onde foi aplicado:** No "Modo Chef" para recomendação de pratos sob restrição de tempo.
* **Justificativa Técnica:** Para maximizar a quantidade de pratos diferentes dentro de um tempo limite, o algoritmo ordena o banco de dados pela soma do tempo de preparo e cozimento em ordem crescente, consumindo as receitas mais rápidas primeiro (Escolha Ótima Local) até estourar a capacidade total informada.

### 4. Árvore B (Modo de Recuperação e Persistência)
* **Onde foi aplicada:** No "Boot 2" do sistema, provando a busca física diretamente na memória secundária.
* **Justificativa Técnica:** Implementada para demonstrar o conceito de paginação em disco. O sistema gerencia o split matemático de nós e salva cada bloco em um arquivo `.dat` usando `pickle`. Durante a execução, o código abre estritamente os arquivos necessários pelo caminho percorrido na árvore, comprovando isolamento de memória eficiente.

### 5. Ordenação Topológica em Grafos (Módulo 5 - Oficina de Produção)
* **Onde foi aplicada:** Na análise da esteira de produção para organizar a ordem de preparo baseada nas dependências entre receitas.
* **Justificativa Técnica:** Utilizou-se o **Algoritmo de Kahn** baseado no cálculo contínuo de graus de entrada. Ele não apenas garante uma ordem viável de execução para o cardápio, mas também detecta ciclos (paradoxos de preparo) antes de iniciar a operação, impedindo que a cozinha trave por dependências circulares intransponíveis.

### 6. Programação Dinâmica (Módulo 6 - Menu Degustação VIP)
* **Onde foi aplicada:** Na seleção do cardápio VIP para maximizar o lucro total respeitando um orçamento rigoroso.
* **Justificativa Técnica:** O problema foi modelado e resolvido utilizando a técnica da **Mochila 0/1 (Knapsack Problem)**. Uma matriz bidimensional foi construída multiplicando os custos por 10 (para contornar a limitação de ponto flutuante em DP e lidar com casas decimais). A técnica garante a solução globalmente ótima que seria impossível de ser garantida por uma heurística gulosa neste cenário de capacidade x valor.

### 7. Algoritmos de Caminho Mínimo e Árvore Geradora Mínima (Módulo 7 - Logística)
* **Onde foram aplicados:** No roteamento de entregas bairro a bairro e no planejamento da infraestrutura de Pontos de Retirada.
* **Justificativa Técnica:** O **Algoritmo de Dijkstra** calcula a rota mais rápida partindo do Restaurante (origem única) até o cliente, sendo processado eficientemente com uma fila de prioridades (`heapq`). Para minimizar os custos de interligação de novas filiais na malha viária, aplicou-se o **Algoritmo de Prim** (MST), garantindo conectividade total entre os pontos com a menor quilometragem/tempo de rede possível.

### 8. Heurística para o Caixeiro Viajante - TSP (Módulo 8 - Laboratório de Inovação)
* **Onde foi aplicada:** Na otimização avançada da rota do motoboy para múltiplas entregas simultâneas em uma única viagem.
* **Justificativa Técnica:** Dado que o TSP é de classe NP-Difícil, implementou-se a **Heurística do Vizinho Mais Próximo (Nearest Neighbor)** combinada com os pesos gerados via Dijkstra. O sistema recalcula dinamicamente o caminho mais curto até o próximo destino pendente, retornando à base (Restaurante) ao final do trajeto. Essa abordagem entrega soluções altamente viáveis e eficientes computacionalmente para períodos de pico no delivery.

### 9. Backtracking com Poda (Desafio Extra - Menu Dia dos Namorados)
* **Onde foi aplicada:** Na geração automática de combinações perfeitas e viáveis (Entrada, Principal, Sobremesa) limitadas por um orçamento máximo imposto pelo Chef.
* **Justificativa Técnica:** A árvore de possibilidades por força bruta cresceria exponencialmente. A implementação via Backtracking utiliza técnica de **Poda (Pruning)**: caso a soma parcial do custo da entrada e do prato principal já ultrapasse o orçamento na árvore de recursão, a ramificação inteira das sobremesas é sumariamente ignorada. As combinações finais válidas são salvas e ranqueadas por maior potencial de valor de venda ao restaurante.

---

## Arquitetura do Projeto
O código-fonte foi cuidadosamente estruturado seguindo boas práticas de separação de responsabilidades (uma adaptação direta do padrão MVC) com pastas dedicadas para modularidade total e facilidade de avaliação:
* `models/`: Classes de dados e lógicas estruturais brutas (`receita.py`, `trie.py`, `hash_table.py`, `btree_disco.py`).
* `utils/`: Bibliotecas matemáticas e motores algorítmicos (`grafos.py`, `otimizacao.py`, `rotas.py`).
* `controllers/`: Regras de negócio (montar as árvores, orquestrar PD, grafos e o gerenciador de boot primário em `boot.py`).
* `views/`: Gerencia exclusivamente as entradas, saídas visuais e tratamentos de erro no terminal interativo (`menu.py`).
* `data/`: Bases de dados JSON estáticas (`receitas.json`, `mapa.json`) e o diretório de serialização `btree_nodos/`.