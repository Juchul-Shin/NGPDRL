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
(att pos12)
(at obj0 pos12)
(at obj1 pos10)
(at obj2 pos10)
(at obj3 pos7)
(at obj4 pos0)
(at obj5 pos2)
(at obj6 pos4)
(at obj7 pos9)
(at obj8 pos2)
(at obj9 pos11)
(at obj10 pos11)
(at obj11 pos6)
(at obj12 pos5)
(at obj13 pos9)
(at obj14 pos4)
)
(:goal (and
(at obj0 pos10)
(at obj1 pos10)
(at obj2 pos7)
(at obj3 pos0)
(at obj4 pos2)
(at obj5 pos4)
(at obj6 pos9)
(at obj7 pos2)
(at obj8 pos11)
(at obj9 pos11)
(at obj10 pos6)
(at obj11 pos5)
(at obj12 pos9)
(at obj13 pos4)
(at obj14 pos10)
))
)
