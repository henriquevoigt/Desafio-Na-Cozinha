# Sistema de Gestão - Desafio na Cozinha (Chef Jacquin)

**Disciplina:** Algoritmos e Estruturas de Dados II  
**Instituição:** Universidade Federal de Pelotas (UFPel)  
**Desenvolvedores:** Henrique Weege Voigt e Samuel Bottermund Flores 
**Turma:** M2 
**Repositório do Projeto:** [https://github.com/henriquevoigt/Desafio-Na-Cozinha]  

---

## Sobre o Projeto

Este projeto implementa um sistema inteligente de gerenciamento de receitas para mitigar problemas de desorganização e sabotagem culinária em uma cozinha profissional. O sistema atende e supera todos os requisitos propostos, utilizando estruturas de dados desenvolvidas do zero para garantir buscas de alto desempenho, validação de integridade criptográfica, otimização de tempo de preparo e persistência avançada de dados em memória secundária.

---

## Fonte de Dados

A fonte de dados escolhida para popular o sistema foi a API pública DummyJSON (`https://dummyjson.com/recipes?limit=50`).  

Para garantir estabilidade e evitar problemas de rede durante a avaliação (conforme recomendado nas instruções), o sistema faz o download estático das 50 receitas no primeiro carregamento e as salva no diretório local `data/receitas.json`. As receitas contêm informações padronizadas como ID, nome, ingredientes, categoria e o tempo de preparo em minutos.

---

## Instruções de Execução

1. **Pré-requisitos:** Certifique-se de ter o Python 3.x instalado em sua máquina. Nenhuma biblioteca externa é necessária, o projeto utiliza apenas pacotes nativos da linguagem.
2. **Executando o sistema:** Navegue até a raiz do projeto no seu terminal e execute o arquivo principal rodando o comando: `python main.py`
3. **Interação (Dual Boot):** O sistema iniciará com um Gerenciador de Boot. 
    * Escolha a **Opção 1** para carregar o sistema completo na memória RAM (Tries, Hash, Guloso).
    * Escolha a **Opção 2** para testar o modo de recuperação (Árvore B com leitura direta no disco físico, sem carregar o JSON).
4. O sistema criará automaticamente as pastas `data/` e `data/btree_nodos/` (para a persistência da Árvore B) na primeira execução.

---

## Estruturas de Dados e Algoritmos Implementados

O projeto implementa do zero **todas as 4 estruturas sugeridas**: Árvore Trie, Tabela Hash, Algoritmo Guloso e Árvore B.

### 1. Árvore Trie (Módulo 2 - Consulta Rápida)
* **Onde foi aplicada:** No "Modo Consulta Rápida" para buscas por Nome, ID e Categoria.
* **Justificativa Técnica:** Em vez de varrer arrays inteiros para buscar prefixos textuais (o que custaria O(N x M)), a Trie permite a recuperação instantânea das informações em tempo O(L), onde L é o comprimento da palavra digitada. Para evitar conflitos de tipos de dados (ex: buscar um nome que contém um número e retornar um ID), a arquitetura foi desenhada instanciando três Tries independentes na memória.

### 2. Tabela Hash Manual (Módulos 3 e Investigação)
* **Onde foi aplicada:** Na indexação de ingredientes ("Consulta Rápida") e no "Modo Investigação" para detectar sabotagens culinárias.
* **Justificativa Técnica:** O uso do dicionário nativo do Python foi evitado em favor da criação de uma classe `HashTable` construída do zero. A estrutura utiliza:
    * **Função Hash Polinomial:** Multiplicação por fator primo (31) para garantir ampla distribuição de strings e minimizar colisões.
    * **Tratamento de Colisões:** Encadeamento (Chaining) utilizando listas dinâmicas.
    * **Redimensionamento (Resize):** Acompanhamento do fator de carga; se a razão entre itens e capacidade chegar a 1.0, a tabela dobra de tamanho.
    * **Validação de Integridade:** O Hash é gerado concatenando nome, ingredientes e tempo. Qualquer alteração indevida nestes campos (sabotagem) muda a assinatura final da receita, alertando o sistema instantaneamente.

### 3. Algoritmo Guloso (Módulo 5 - Modo Chef)
* **Onde foi aplicado:** No "Modo Chef" para recomendação de pratos sob restrição de tempo.
* **Justificativa Técnica:** O objetivo é maximizar a quantidade de pratos diferentes que o Chef pode preparar dentro de um limite de tempo máximo estipulado. A estratégia gulosa modela o problema classicamente através da "Escolha Ótima Local": o algoritmo ordena todo o banco de dados pela soma do tempo de preparo e cozimento em ordem crescente e vai "consumindo" as receitas mais rápidas primeiro até estourar a capacidade total de tempo fornecida pelo usuário.

### 4. Árvore B (Modo de Recuperação e Persistência)
* **Onde foi aplicada:** No "Boot 2" do sistema, isolada da memória RAM principal, provando a busca física diretamente na memória secundária.
* **Justificativa Técnica:** Implementada para demonstrar o funcionamento de paginação em disco. Em vez de carregar o banco de dados inteiro na memória, a Árvore B gerencia o split matemático de nós e salva cada bloco em um arquivo `.dat` independente (utilizando o módulo nativo `pickle`). Durante a busca, o sistema abre estritamente os arquivos necessários pelo caminho percorrido, comprovando um isolamento de memória eficiente e recuperação de dados sem sobrecarga de RAM.

---

## Arquitetura do Projeto
O código foi estruturado seguindo boas práticas de separação de responsabilidades (MVC adaptado):
* `models/`: Contém as lógicas brutas das Estruturas de Dados (`receita.py`, `trie.py`, `hash_table.py`, `btree_disco.py`).
* `controllers/`: Faz a ponte de regras de negócio (montar árvores, matemática gulosa, gerenciar o boot primário no `boot.py`).
* `views/`: Gerencia exclusivamente as entradas e saídas visuais no terminal (`menu.py`).
* `data/`: Onde repousa o cache principal `.json` e o diretório `btree_nodos/` contendo os blocos binários persistidos.