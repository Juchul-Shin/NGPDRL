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
pos15 - place
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
(att pos9)
(at obj0 pos10)
(at obj1 pos10)
(at obj2 pos10)
(at obj3 pos10)
(at obj4 pos10)
(at obj5 pos12)
(at obj6 pos12)
(at obj7 pos12)
(at obj8 pos12)
(at obj9 pos12)
(at obj10 pos0)
(at obj11 pos0)
(at obj12 pos0)
(at obj13 pos0)
(at obj14 pos0)
)
(:goal (and
(at obj0 pos11)
(at obj1 pos11)
(at obj2 pos11)
(at obj3 pos11)
(at obj4 pos11)
(at obj5 pos6)
(at obj6 pos6)
(at obj7 pos6)
(at obj8 pos6)
(at obj9 pos6)
(at obj10 pos14)
(at obj11 pos14)
(at obj12 pos14)
(at obj13 pos14)
(at obj14 pos14)
))
)