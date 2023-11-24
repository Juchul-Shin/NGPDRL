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
obj10 - package
obj11 - package
obj12 - package
obj13 - package
obj14 - package
)
(:init
(load)
(nfull)
(att pos2)
(at obj0 pos2)
(at obj1 pos2)
(at obj2 pos2)
(at obj3 pos2)
(at obj4 pos2)
(at obj5 pos2)
(at obj6 pos2)
(at obj7 pos2)
(at obj8 pos2)
(at obj9 pos2)
(at obj10 pos2)
(at obj11 pos2)
(at obj12 pos2)
(at obj13 pos2)
(at obj14 pos2)
)
(:goal (and
(at obj0 pos8)
(at obj1 pos8)
(at obj2 pos4)
(at obj3 pos0)
(at obj4 pos5)
(at obj5 pos2)
(at obj6 pos2)
(at obj7 pos7)
(at obj8 pos6)
(at obj9 pos8)
(at obj10 pos0)
(at obj11 pos6)
(at obj12 pos5)
(at obj13 pos7)
(at obj14 pos5)
))
)
