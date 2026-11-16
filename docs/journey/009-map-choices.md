# uso da função map no registro ocorrencias

- o persistence pega os valores do banco e guarda as categorias disponiveis

- o map é usado dentro de um list que é usado no choices do inquirer, 
basicamente o map está executando uma função para cada categoria disponível
essa função tem um parametro x (o valor da categoria), ela retorna um Choice com o nome e valor da categoria.
