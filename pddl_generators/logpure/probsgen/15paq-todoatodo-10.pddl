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
pos13 - place
pos14 - place
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
(att pos5)
(at obj0 pos7)
(at obj1 pos7)
(at obj2 pos3)
(at obj3 pos11)
(at obj4 pos6)
(at obj5 pos8)
(at obj6 pos10)
(at obj7 pos7)
(at obj8 pos11)
(at obj9 pos14)
(at obj10 pos14)
(at obj11 pos14)
(at obj12 pos8)
(at obj13 pos7)
(at obj14 pos11)
)
(:goal (and
(at obj0 pos12)
(at obj1 pos8)
(at obj2 pos0)
(at obj3 pos14)
(at obj4 pos12)
(at obj5 pos12)
(at obj6 pos14)
(at obj7 pos0)
(at obj8 pos0)
(at obj9 pos7)
(at obj10 pos3)
(at obj11 pos5)
(at obj12 pos7)
(at obj13 pos1)
(at obj14 pos2)
))
)
