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
	       (building)
		(nbuilding)
 		(stack)
		(ontop ?x)
	       )

  (:action pickup
	     :parameters (?x)
	     :precondition (and (clear ?x) (ontable ?x) (handempty))
	     :effect
	     (and (not (ontable ?x))
		   (not (clear ?x))
		   (not (handempty))
		   (holding ?x)))

  (:action putdown
	     :parameters (?x)
	     :precondition (holding ?x)
	     :effect
	     (and (not (holding ?x))
		   (clear ?x)
		   (handempty)
		   (ontable ?x)))
  (:action stack
	     :parameters (?x ?y)
	     :precondition (and (holding ?x) (ontable ?y) (clear ?y) (nbuilding))
	     :effect
	     (and (not (stack))
			(ontop ?x)
			(building)
			(not (nbuilding))
		   (not (holding ?x))
		   (not (clear ?y))
		   (clear ?x)
		   (handempty)
		   (on ?x ?y)))

  (:action stack2
	     :parameters (?x ?y)
	     :precondition (and (holding ?x) (clear ?y) (building) (ontop ?y) )
	     :effect
	     (and (not (stack))
			(ontop ?x)
			(not (ontop ?y))
		   (not (holding ?x))
		   (not (clear ?y))
		   (clear ?x)
		   (handempty)
		   (on ?x ?y)))

  (:action towerfinish
	     :parameters ( ?x )
	     :precondition (and (building) (ontop ?x))
	     :effect
	     (and (not (building)) (nbuilding) (not (ontop ?x)) )
	)

  (:action unstack
	     :parameters (?x ?y)
	     :precondition (and (on ?x ?y) (clear ?x) (handempty))
	     :effect
	     (and (holding ?x)
		(not (building)) (stack) (not (ontop ?x))
		   (clear ?y)
		   (not (clear ?x))
		   (not (handempty))
		   (not (on ?x ?y)))))

