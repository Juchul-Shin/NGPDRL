(define (domain ascensor)

	(:types ascensor persona bloque planta)

	(:predicates 
		(at_persona ?x - persona ?pl - planta)
		(at_ascensor ?a - ascensor ?pl - planta)
		(pertenece ?as - ascensor ?bl - bloque)
		(dentro ?pe - persona ?as - ascensor)
		(corresponde ?pl - planta ?bl - bloque))

	(:action entra_pasajero 
		:parameters ( ?pe - persona ?as - ascensor ?pl - planta )
		:precondition (and
			(at_persona ?pe ?pl)
			(at_ascensor ?as ?pl) )
		:effect (and
			(dentro ?pe ?as)
			(not (at_persona ?pe ?pl)) ))
	
	(:action sale_pasajero
		:parameters ( ?pe - persona ?as - ascensor ?pl - planta )	
		:precondition (and
			(at_ascensor ?as ?pl)
			(dentro ?pe ?as) )
		:effect (and
			(not (dentro ?pe ?as))
			(at_persona ?pe ?pl) ))

	(:action mover_ascensor
		:parameters ( ?as - ascensor ?actual - planta ?destino - planta ?bl - bloque )
		:precondition (and
			(at_ascensor ?as ?actual)
			(pertenece ?as ?bl)
			(corresponde ?destino ?bl) )
		:effect (and
			(not (at_ascensor ?as ?actual))
			(at_ascensor ?as ?destino) ))
)
