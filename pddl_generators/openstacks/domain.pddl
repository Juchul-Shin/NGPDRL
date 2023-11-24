(define (domain openstacks)
(:requirements :typing)
(:types order product count)

(:predicates 
	(includes ?o - order ?p - product)
    (included ?p - product ?o - order)
	(waiting ?o - order)
	(started ?o - order)
	(shipped ?o - order)
	(made ?p - product)
	(not-made ?p - product)
	(stacks-avail ?s - count)
	(next ?s ?next_s - count)
    (order-started ?p - product ?c - count)
    (necessary-to-make ?p - product ?c - count)
    (verified ?o - order ?c - count)
    (necessary-to-ship ?o - order ?c - count)
    (nada1)
    (nada2)
)

(:action nada1
        :parameters (?x)
        :precondition (and (nada1))
        :effect
        (and (nada2) (not (nada1))))

(:action nada2
        :parameters (?x)
        :precondition (and (nada2))
        :effect
        (and (nada1) (not (nada2))))


;abre un stack para tener espacio
(:action open-new-stack
:parameters (?s ?next_s - count)
:precondition (and 
    (nada1)
    (stacks-avail ?s)
    (next ?s ?next_s)
    )
:effect (and 
    (not (stacks-avail ?s))
    (stacks-avail ?next_s)
    )
)

;empieza un order cogiendo un stack
(:action start-order
:parameters (?o - order ?pre_s ?s - count)
:precondition (and 
    (nada1)
    (waiting ?o)
    (stacks-avail ?s)
    (next ?pre_s ?s)
    )
:effect (and 
    (not (waiting ?o))
    (started ?o)
    (not (stacks-avail ?s))
    (stacks-avail ?pre_s)
    )
)

;order-started empieza a cero y se va aumentando conforme aumentan los pedidos
;tenemos un numero necessary para poder hacer el producto que se debe satisfacer
;que se satisface cuando todos los order que necesitan del producto estan started

(:action include-product
:parameters (?p - product ?o - order ?s - count ?next_s - count)
:precondition (and 
    (nada1)
    (includes ?o ?p)
    (order-started ?p ?s)
    (next ?s ?next_s) 
    (started ?o)
    )
:effect (and 
    (not (includes ?o ?p)) 
    (included ?p ?o)
    (not (order-started ?p ?s)) 
    (order-started ?p ?next_s))
    )


;cuando se alcanza el numero necesario de productos, es decir, el correspondiente
;a todos los order que lo contienen, podemos hacer el producto

(:action make-product 
:parameters (?p - product ?s - count)
:precondition (and 
    (nada1)
    (not-made ?p)
    (order-started ?p ?s)
    (necessary-to-make ?p ?s)
    )
:effect (and 
    (not (not-made ?p)) 
    (made ?p)
    )
)

;verifico que estan los productos hechos

(:action verify-product
:parameters (?o - order ?p - product ?s - count ?next_s - count)
:precondition (and
    (nada1)
    (included ?p ?o)
    (made ?p)
    (verified ?o ?s)
    (next ?s ?next_s)
    )
:effect (and
    (not (included ?p ?o))
    (not (verified ?o ?s))
    (verified ?o ?next_s)
    )
)

;cuando envio un pedido aumento el numero de pilas disponibles y compruebo que están todos
;los productos necesarios

(:action ship-order
:parameters (?o - order ?s - count ?next_s - count ?v - count)
:precondition (and
    (nada1)
    (started ?o)
    (stacks-avail ?s)
    (next ?s ?next_s)
    (verified ?o ?v)
    (necessary-to-ship ?o ?v)
    )
:effect (and
    (not (started ?o))
    (not (stacks-avail ?s))
    (stacks-avail ?next_s)
    (shipped ?o)
    )

)


)
