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
obj5 - package
obj6 - package
obj7 - package
obj8 - package
obj9 - package
)
(:init
(load)
(nfull)
(att pos7)
(at obj0 pos0)
(at obj1 pos8)
(at obj2 pos6)
(at obj3 pos7)
(at obj4 pos2)
(at obj5 pos5)
(at obj6 pos0)
(at obj7 pos3)
(at obj8 pos2)
(at obj9 pos2)
)
(:goal (and
(at obj0 pos7)
(at obj1 pos4)
(at obj2 pos8)
(at obj3 pos0)
(at obj4 pos4)
(at obj5 pos7)
(at obj6 pos3)
(at obj7 pos3)
(at obj8 pos3)
(at obj9 pos8)
))
)