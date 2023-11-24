;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; 4 op-blocks world
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain blocks)
    (:requirements :strips :typing)
    (:types block robot)
    (:predicates 
        (on ?x - block ?y - block)
        (ontable ?x - block)
        (clear ?x - block)
        (handempty ?x - robot)
        (handfull ?x - robot)
        (holding ?x - block ?r - robot)
    )

    ; (:actions pickup putdown stack unstack)

    (:action pick-up
        :parameters (?x - block ?robot - robot)
        :precondition (and
            (clear ?x) 
            (ontable ?x) 
            (handempty ?robot)
        )
        :effect (and
            (not (ontable ?x))
            (not (clear ?x))
            (not (handempty ?robot))
            (handfull ?robot)
            (holding ?x ?robot)
        )
    )

    (:action put-down
        :parameters (?x - block ?robot - robot)
        :precondition (and 
            (holding ?x ?robot)
            (handfull ?robot)
        )
        :effect (and 
            (not (holding ?x ?robot))
            (clear ?x)
            (handempty ?robot)
            (not (handfull ?robot))
            (ontable ?x))
        )

    (:action stack
        :parameters (?x - block ?y - block ?robot - robot)
        :precondition (and
            (holding ?x ?robot) 
            (clear ?y)
            (handfull ?robot)
        )
        :effect (and 
            (not (holding ?x ?robot))
            (not (clear ?y))
            (clear ?x)
            (handempty ?robot)
            (not (handfull ?robot))
            (on ?x ?y)
        )
    )

    (:action unstack
        :parameters (?x - block ?y - block ?robot - robot)
        :precondition (and
            (on ?x ?y)
            (clear ?x)
            (handempty ?robot)
        )
        :effect (and 
            (holding ?x ?robot)
            (clear ?y)
            (not (clear ?x))
            (not (handempty ?robot))
            (handfull ?robot)
            (not (on ?x ?y))
        )
    )
)
