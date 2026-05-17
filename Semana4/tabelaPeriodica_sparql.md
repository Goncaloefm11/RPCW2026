#Queries sobre a Tabela Periodica

1. Quero uma lista dos elementos com os campos nome e número atomico ordenado por número

SELECT ?nome ?num WHERE {
    ?elemento a :Element;
    		:name ?nome ;
            :atomicNumber ?num .
}ORDER BY (?num)


2. Lista dos grupos de elementos


3. Distribuição dos elementos por grupo(quantos elementos tem um grupo)
4. Distribuição dos elementos por periodo

SELECT ?p (count (?elem) as ?nelems) WHERE {
    ?p a :Period;
    :element ?elem.
}GROUP BY ?p
 ORDER BY ?p