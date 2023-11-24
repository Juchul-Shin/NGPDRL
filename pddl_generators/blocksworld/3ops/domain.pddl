(define (domain blocksworld)
(:predicates (clear ?x)
             (ontable ?x)
             (on ?x ?y))

(:action move_block_to_block
  :parameters (?bm ?bf ?bt)
  :precondition (and (clear ?bm) (clear ?bt) (on ?bm ?bf))
  :effect (and (not (clear ?bt)) (not (on ?bm ?bf))
               (on ?bm ?bt) (clear ?bf)))

(:action move_block_to_table
  :parameters (?bm ?bf)
  :precondition (and (clear ?bm) (on ?bm ?bf))
  :effect (and (not (on ?bm ?bf))
               (ontable ?bm) (clear ?bf)))

(:action move_table_to_block
  :parameters (?bm ?bt)
  :precondition (and (clear ?bm) (clear ?bt) (ontable ?bm))
  :effect (and (not (clear ?bt)) (not (ontable ?bm))
               (on ?bm ?bt))))

