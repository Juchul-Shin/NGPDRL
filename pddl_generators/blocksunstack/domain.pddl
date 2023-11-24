;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; 4 Op-blocks world
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain BLOCKS)
  (:requirements :strips)
  (:predicates (on ?x ?y)
	       (ontable ?x)
	       (clear ?x)
	       (handempty)
	       (holding ?x)
	       (stack)
		(nbuilding)
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


  (:action pickup
	     :parameters (?x)
	     :precondition (and (nada1) (clear ?x) (ontable ?x) (handempty))
	     :effect
	     (and (not (ontable ?x))
		   (not (clear ?x))
		   (not (handempty))
		   (holding ?x)))

  (:action putdown
	     :parameters (?x)
	     :precondition (and (nada1) (holding ?x))
	     :effect
	     (and (not (holding ?x))
		   (clear ?x)
		   (handempty)
		   (ontable ?x)))
  (:action stack
	     :parameters (?x ?y)
	     :precondition (and (nada1) (holding ?x) (clear ?y))
	     :effect
	     (and  (not (stack))
		   (not (holding ?x))
		   (not (clear ?y))
		   (clear ?x)
		   (handempty)
		   (on ?x ?y)))
  (:action unstack
	     :parameters (?x ?y)
	     :precondition (and (nada1) (on ?x ?y) (clear ?x) (handempty) (stack) )
	     :effect
	     (and (holding ?x)
		   (clear ?y)
		   (not (clear ?x))
		   (not (handempty))
		   (not (on ?x ?y)))))
