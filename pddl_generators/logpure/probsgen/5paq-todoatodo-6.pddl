(define (problem logistics-generated)
(:domain logistics)
(:objects
pos0 - place
pos1 - place
pos2 - place
pos3 - place
pos4 - place
obj0 - package
obj1 - package
obj2 - package
obj3 - package
obj4 - package
)
(:init
(load)
(nfull)
(att pos1)
(at obj0 pos1)
(at obj1 pos2)
(at obj2 pos4)
(at obj3 pos3)
(at obj4 pos1)
)
(:goal (and
(at obj0 pos0)
(at obj1 pos0)
(at obj2 pos3)
(at obj3 pos2)
(at obj4 pos4)
))
)