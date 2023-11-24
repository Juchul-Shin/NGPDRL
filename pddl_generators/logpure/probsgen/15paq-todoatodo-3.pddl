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
pos10 - place
pos11 - place
pos12 - place
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
(att pos10)
(at obj0 pos12)
(at obj1 pos8)
(at obj2 pos5)
(at obj3 pos5)
(at obj4 pos3)
(at obj5 pos6)
(at obj6 pos2)
(at obj7 pos10)
(at obj8 pos11)
(at obj9 pos3)
(at obj10 pos8)
(at obj11 pos0)
(at obj12 pos0)
(at obj13 pos5)
(at obj14 pos7)
)
(:goal (and
(at obj0 pos8)
(at obj1 pos7)
(at obj2 pos10)
(at obj3 pos7)
(at obj4 pos4)
(at obj5 pos2)
(at obj6 pos11)
(at obj7 pos3)
(at obj8 pos9)
(at obj9 pos12)
(at obj10 pos1)
(at obj11 pos12)
(at obj12 pos4)
(at obj13 pos6)
(at obj14 pos9)
))
)
