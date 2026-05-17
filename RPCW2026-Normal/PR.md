## Metodologia de Migração

Para o povoamento da ontologia, foi desenvolvido um script em Python utilizando a biblioteca `rdflib`. 

O script automatiza o processo da seguinte forma:
1. Carrega a estrutura base a partir do ficheiro `sapientia_base.ttl`.
2. Lê e processa sequencialmente os ficheiros de dados fornecidos (`conceitos.json`, `disciplinas.json`, `mestres.json`, `obras.json` e o dataset específico do aluno).
3. Trata a integridade dos dados: tal como exigido no enunciado, sempre que um recurso é referenciado numa relação mas não existe no dataset principal (ex: um conceito mencionado numa disciplina), o script cria automaticamente o indivíduo na ontologia apenas com o predicado `nome`, garantindo que nenhuma relação se perde.
4. Exporta o resultado final consolidado para o ficheiro `sapientia_ind.ttl`.

O script encontra-se na raiz deste repositório para livre consulta e replicação do cenário de correção.