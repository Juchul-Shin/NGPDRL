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
)
(:init
(load)
(nfull)
(att pos1)
(at obj0 pos6)
(at obj1 pos2)
(at obj2 pos14)
(at obj3 pos12)
(at obj4 pos3)
(at obj5 pos12)
(at obj6 pos3)
(at obj7 pos1)
(at obj8 pos10)
(at obj9 pos14)
)
(:goal (and
(at obj0 pos8)
(at obj1 pos8)
(at obj2 pos8)
(at obj3 pos8)
(at obj4 pos8)
(at obj5 pos8)
(at obj6 pos8)
(at obj7 pos8)
(at obj8 pos8)
(at obj9 pos8)
))
)
