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
pos9 - place
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
(att pos4)
(at obj0 pos3)
(at obj1 pos3)
(at obj2 pos3)
(at obj3 pos8)
(at obj4 pos8)
(at obj5 pos8)
(at obj6 pos8)
(at obj7 pos8)
(at obj8 pos8)
(at obj9 pos8)
)
(:goal (and
(at obj0 pos7)
(at obj1 pos7)
(at obj2 pos7)
(at obj3 pos7)
(at obj4 pos7)
(at obj5 pos7)
(at obj6 pos2)
(at obj7 pos2)
(at obj8 pos2)
(at obj9 pos2)
))
)
