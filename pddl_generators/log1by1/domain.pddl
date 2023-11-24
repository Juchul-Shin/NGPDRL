;; logistics domain Typed version.
;;

(define (domain logistics)
  (:requirements :strips :typing) 
  (:types package
          place - object)
  
  (:predicates	(at ?obj - package ?loc - place)
		(in ?pkg - package)
		(att ?loc - place) 
		(nfull) (full) (load) )
  
(:action LOAD-TRUCK
   :parameters    (?pkg - package ?loc - place)
   :precondition  (and (att ?loc) (at ?pkg ?loc) (nfull) )
   :effect        (and (not (at ?pkg ?loc)) (in ?pkg) ( full ) (not (nfull)) ))

(:action UNLOAD-TRUCK
  :parameters   (?pkg - package ?loc - place)
  :precondition (and (att ?loc) (in ?pkg) (full) )
  :effect       (and (not (in ?pkg)) (at ?pkg ?loc) (nfull) (not (full)) ))


(:action DRIVE-TRUCK
  :parameters (?loc-from - place ?loc-to - place )
  :precondition
   (and (att ?loc-from))
  :effect
   (and (not (att ?loc-from)) (att ?loc-to)))


)
