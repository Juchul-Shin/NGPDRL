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
(at obj0 pos1)
(at obj1 pos1)
(at obj2 pos1)
(at obj3 pos1)
(at obj4 pos1)
(at obj5 pos0)
(at obj6 pos0)
(at obj7 pos0)
(at obj8 pos0)
(at obj9 pos0)
(at obj10 pos5)
(at obj11 pos5)
(at obj12 pos5)
(at obj13 pos5)
(at obj14 pos5)
)
(:goal (and
(at obj0 pos7)
(at obj1 pos7)
(at obj2 pos7)
(at obj3 pos7)
(at obj4 pos7)
(at obj5 pos8)
(at obj6 pos8)
(at obj7 pos8)
(at obj8 pos8)
(at obj9 pos8)
(at obj10 pos6)
(at obj11 pos6)
(at obj12 pos6)
(at obj13 pos6)
(at obj14 pos6)
))
)
