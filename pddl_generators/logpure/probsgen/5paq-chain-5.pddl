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
(at obj0 pos6)
(at obj1 pos0)
(at obj2 pos5)
(at obj3 pos5)
(at obj4 pos3)
)
(:goal (and
(at obj0 pos0)
(at obj1 pos5)
(at obj2 pos5)
(at obj3 pos3)
(at obj4 pos0)
))
)
