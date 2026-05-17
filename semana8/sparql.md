Lista de cidades, ordenada alfabeticamente pelo nome
```sparql
PREFIX : <http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/>

select ?ncidade where {
	?c a :Cidade ;
    	:temNome ?ncidade .
} orderby ?ncidade
```

Distribuição das cidades por distrito: lista de distritos ordenada alfabeticamente em que para
cada um se indica quantas cidades tem;
```sparql
PREFIX : <http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/>

select ?ndistrito (COUNT(?c) as ?nc) where {
    ?d a :Distrito ;
    :temNome ?ndistrito ;
    :temCidade ?nc .
} 
    group by ?ndistrito 
	order by ?ndistrito
```

Que cidades têm ligações diretas com Braga cidade? (Considera Braga como origem mas também
como destino)
```
PREFIX : <http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/>

select ?ncidade where {
	?c a :Cidade ;
    :temNome "Braga" .
    {?l a :Ligacao ;
        :temOrigem ?c ;
        :temDestino/:temNome ?ncidade . }
    union
    {?l a :Ligacao ;
		:temDestino ?c ;
    	:temOrigem/:temNome ?ncidade .   
    }
} 
```
Partindo de Braga, que cidades se conseguem visitar? (Apresenta uma lista de cidades
ordenada alfabeticamente)
```sparql
PREFIX : <http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/>
construct {
    ?cidadeOrigem :ligadaA ?cidadeDestino . 
}
where {
    ?cidadeOrigem a :Cidade  . 
    ?l a :Ligacao ;
        :temOrigem ?cidadeOrigem;
        :temDestino ?cidadeDestino . 
}
```

Através duma query CONSTRUCT cria uma ligação direta entre Braga e todas as cidades que
se conseguem visitar a partir dela.
```sparql
PREFIX : <http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/>
construct {
    ?braga :ligacaoDireta ?cidadeDestino . 
}
where {
    ?braga a :Cidade ;
    	:temNome "Braga" . 
    ?l a :Ligacao ;
        :temOrigem ?braga ;
        :temDestino ?cidadeDestino . 
}
```
