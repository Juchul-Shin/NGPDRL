(define (problem logistics-generated)
(:domain logistics)
(:objects
pos0 - place
pos1 - place
pos2 - place
pos3 - place
pos4 - place
pos5 - place
pos6 - place
pos7 - place
pos8 - place
obj0 - package
obj1 - package
obj2 - package
obj3 - package
obj4 - package
)
(:init
(load)
(nfull)
(att pos2)
(at obj0 pos3)
(at obj1 pos8)
(at obj2 pos2)
(at obj3 pos1)
(at obj4 pos8)
)
(:goal (and
(at obj0 pos5)
(at obj1 pos6)
(at obj2 pos2)
(at obj3 pos4)
(at obj4 pos2)
))
)
