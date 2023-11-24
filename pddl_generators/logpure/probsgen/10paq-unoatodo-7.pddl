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
obj5 - package
obj6 - package
obj7 - package
obj8 - package
obj9 - package
)
(:init
(load)
(nfull)
(att pos5)
(at obj0 pos6)
(at obj1 pos6)
(at obj2 pos6)
(at obj3 pos6)
(at obj4 pos6)
(at obj5 pos6)
(at obj6 pos6)
(at obj7 pos6)
(at obj8 pos6)
(at obj9 pos6)
)
(:goal (and
(at obj0 pos5)
(at obj1 pos4)
(at obj2 pos1)
(at obj3 pos6)
(at obj4 pos3)
(at obj5 pos7)
(at obj6 pos7)
(at obj7 pos1)
(at obj8 pos5)
(at obj9 pos0)
))
)
