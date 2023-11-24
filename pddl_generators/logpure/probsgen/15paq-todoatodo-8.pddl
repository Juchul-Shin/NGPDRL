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
(att pos1)
(at obj0 pos7)
(at obj1 pos5)
(at obj2 pos7)
(at obj3 pos3)
(at obj4 pos7)
(at obj5 pos9)
(at obj6 pos4)
(at obj7 pos5)
(at obj8 pos0)
(at obj9 pos0)
(at obj10 pos1)
(at obj11 pos2)
(at obj12 pos10)
(at obj13 pos9)
(at obj14 pos6)
)
(:goal (and
(at obj0 pos1)
(at obj1 pos2)
(at obj2 pos2)
(at obj3 pos9)
(at obj4 pos1)
(at obj5 pos3)
(at obj6 pos10)
(at obj7 pos9)
(at obj8 pos1)
(at obj9 pos5)
(at obj10 pos0)
(at obj11 pos9)
(at obj12 pos0)
(at obj13 pos3)
(at obj14 pos9)
))
)
