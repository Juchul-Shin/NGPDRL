(define (domain droneworld_simple)
  (:requirements :typing)

(:types
    unit
    position
)
  
(:predicates
    (at ?u - unit ?p - position)
    (adjacent ?from ?to - position)
)

(:action move
    :parameters (?from ?to - position)
    :precondition (and 
        (at drone ?from)
        (adjacent ?from ?to)
    )
    :effect (and 
        (not (at drone ?from))
        (at drone ?to)
    )
)

)
